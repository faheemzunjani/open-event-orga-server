import json
import logging
import os
from datetime import datetime

from flask import request, url_for, flash
from flask.ext.restplus import abort
from flask.ext import login
from flask_admin import BaseView, expose
from markupsafe import Markup
from werkzeug.utils import redirect, secure_filename

from open_event.helpers.data import DataManager
from ...helpers.data_getter import DataGetter

def get_published_event_or_abort(event_id):
    event = DataGetter.get_event(event_id=event_id)
    if not event or (event.state != u'Published' and event.state != 'Published'):
        user = login.current_user
        if not login.current_user.is_authenticated or (not user.is_organizer(event_id) and not
                                                       user.is_coorganizer(event_id) and not
                                                       user.is_track_organizer(event_id)):
            abort(404)
    return event

class EventDetailView(BaseView):

    @expose('/')
    def display_default(self):
        return redirect("/browse")

    @expose('/<int:event_id>/')
    def display_event_detail_home(self, event_id):
        call_for_speakers = DataGetter.get_call_for_papers(event_id).first()
        event = get_published_event_or_abort(event_id)
        accepted_sessions = DataGetter.get_sessions(event_id)
        return self.render('/gentelella/guest/event/details.html', event=event, accepted_sessions=accepted_sessions, call_for_speakers=call_for_speakers)

    @expose('/<int:event_id>/sessions/')
    def display_event_sessions(self, event_id):
        call_for_speakers = DataGetter.get_call_for_papers(event_id).first()
        event = get_published_event_or_abort(event_id)
        tracks = DataGetter.get_tracks(event_id)
        return self.render('/gentelella/guest/event/sessions.html', event=event, tracks=tracks, call_for_speakers=call_for_speakers)

    @expose('/<int:event_id>/schedule/')
    def display_event_schedule(self, event_id):
        call_for_speakers = DataGetter.get_call_for_papers(event_id).first()
        event = get_published_event_or_abort(event_id)
        if not event.schedule_published_on:
            abort(404)
        return self.render('/gentelella/guest/event/schedule.html', event=event, call_for_speakers=call_for_speakers)

    @expose('/<int:event_id>/cfs/', methods=('GET',))
    def display_event_cfs(self, event_id):
        event = get_published_event_or_abort(event_id)
        call_for_speakers = DataGetter.get_call_for_papers(event_id).first()

        if not call_for_speakers:
            abort(404)

        form_elems = DataGetter.get_custom_form_elements(event_id).first()
        speaker_form = json.loads(form_elems.speaker_form)
        session_form = json.loads(form_elems.session_form)

        now = datetime.now()
        state = "now"
        if call_for_speakers.end_date < now:
            state = "past"
        elif call_for_speakers.start_date > now:
            sate = "future"

        return self.render('/gentelella/guest/event/cfs.html', event=event, speaker_form=speaker_form,
                           session_form=session_form, call_for_speakers=call_for_speakers, state=state)

    @expose('/<int:event_id>/cfs/', methods=('POST',))
    def process_event_cfs(self, event_id):
        email = request.form['email']
        speaker_img_file = ""
        slide_file = ""
        video_file = ""
        audio_file = ""
        if 'slides' in request.files and request.files['slides'].filename != '':
            slide_file = request.files['slides']
        if 'video' in request.files and request.files['video'].filename != '':
            video_file = request.files['video']
        if 'audio' in request.files and request.files['audio'].filename != '':
            audio_file = request.files['audio']
        if 'photo' in request.files and request.files['photo'].filename != '':
            speaker_img_file = request.files['photo']
        DataManager.add_session_to_event(request.form, event_id, speaker_img_file,
                                         slide_file, audio_file, video_file)
        if login.current_user.is_authenticated:
            flash("Your session proposal has been submitted", "success")
            return redirect(url_for('my_sessions.display_my_sessions_view', event_id=event_id))
        else:
            flash(Markup("Your session proposal has been submitted. Please login/register with <strong><u>" + email + "</u></strong> to manage it."), "success")
            return redirect(url_for('admin.login_view', next=url_for('my_sessions.display_my_sessions_view')))

    # SLUGGED PATHS

    @expose('/<int:event_id>/<slug>/')
    def display_event_detail_home_slugged(self, event_id, slug):
        return self.display_event_detail_home(event_id)

    @expose('/<int:event_id>/<slug>/sessions/')
    def display_event_sessions_slugged(self, event_id, slug):
        return self.display_event_sessions(event_id)

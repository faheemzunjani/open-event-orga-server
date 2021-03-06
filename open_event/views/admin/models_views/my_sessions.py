import json

import flask_login
from flask import flash, redirect, url_for, request
from flask.ext.restplus import abort
from flask_admin import BaseView, expose

from open_event.helpers.data import DataManager
from ....helpers.data_getter import DataGetter

class MySessionView(BaseView):

    @expose('/')
    @flask_login.login_required
    def display_my_sessions_view(self):
        upcoming_events_sessions = DataGetter.get_sessions_of_user(upcoming_events=True)
        past_events_sessions = DataGetter.get_sessions_of_user(upcoming_events=False)
        page_content = {"tab_upcoming_events": "Upcoming Events",
                        "tab_past_events": "Upcoming Events",
                        "title": "My Session Proposals"}
        return self.render('/gentelella/admin/mysessions/mysessions_list.html',
                           upcoming_events_sessions=upcoming_events_sessions, past_events_sessions=past_events_sessions,
                           page_content=page_content)

    @expose('/<int:session_id>/', methods=('GET',))
    @flask_login.login_required
    def display_session_view(self, session_id):
        session = DataGetter.get_sessions_of_user_by_id(session_id)
        if not session:
            abort(404)
        form_elems = DataGetter.get_custom_form_elements(session.event_id).first()
        if not form_elems:
            flash("Speaker and Session forms have been incorrectly configured for this event."
                  " Session creation has been disabled", "danger")
            return redirect(url_for('.display_my_sessions_view', event_id=session.event_id))
        speaker_form = json.loads(form_elems.speaker_form)
        session_form = json.loads(form_elems.session_form)
        event = DataGetter.get_event(session.event_id)

        return self.render('/gentelella/admin/mysessions/mysession_detail.html', session=session,
                           speaker_form=speaker_form, session_form=session_form, event=event)

    @expose('/<int:session_id>/', methods=('POST',))
    @flask_login.login_required
    def process_session_view(self, session_id):
        session = DataGetter.get_sessions_of_user_by_id(session_id)
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

        DataManager.edit_session(request.form, session, slide_file, audio_file, video_file)
        flash("The session has been updated successfully", "success")
        return redirect(url_for('.display_session_view', event_id=session.event_id, session_id=session_id))

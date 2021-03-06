"""
This file contains sample POST data
"""

POST_EVENT_DATA = {
    "color": "red",
    "email": "event@gmail.com",
    "end_time": "2016-05-30 12:12:43",
    "latitude": 0,
    "location_name": "TestEvent",
    "logo": "http://imgur.com/image.png",
    "longitude": 0,
    "name": "TestEvent",
    'event_url': "http://site.com",
    'background_url': "http://imgur.com/image.png",
    'description': "blah blah",
    "start_time": "2016-05-25 12:12:43",
    "closing_datetime": "2016-05-22 12:12:43",
    "organizer_name": "FOSSASIA",
    "organizer_description": "Promoting Open Source culture around the world",
    "state": "pending",
    "type": "Conference",
    "topic": "Science & Technology",
    "privacy": "public",
    "ticket_url": "http://site.com/tickets"
}

POST_MICROLOCATION_DATA = {
    "floor": 1,
    "latitude": 1,
    "longitude": 1,
    "name": "TestMicrolocation",
    "room": "TestRoom"
}

POST_SESSION_DATA = {
    "short_abstract": "TestSession",
    "long_abstract": "TestSession",
    "end_time": "2016-05-30 09:47:37",
    "microlocation_id": None,
    "speaker_ids": [],
    "start_time": "2016-05-30 08:47:37",
    "subtitle": "TestSession",
    "comments": "Comments",
    "title": "TestSession",
    "track_id": None,
    "language": "German",
    "slides": "http://example.com/slides",
    "video": "http://example.com/video",
    "audio": "http://example.com/audio",
    "signup_url": "http://example.com/signup",
    "session_type_id": None
}

POST_SPEAKER_DATA = {
    "short_biography": "TestSpeaker",
    "long_biography": "TestSpeaker",
    "country": "TestSpeaker",
    "email": "speaker@gmail.com",
    "mobile": "speaker@gmail.com",
    "facebook": "http://facebook.com/user",
    "github": "http://github.com/user",
    "linkedin": "http://in.linkedin.com/user",
    "name": "TestSpeaker",
    "organisation": "TestSession",
    "photo": "http://imgur.com/skds.png",
    "position": "TestSession",
    "twitter": "http://twitter.com/user",
    "website": "http://website.com"
}

POST_SPONSOR_DATA = {
    "logo": "http://imgur.com/image.png",
    "name": "TestSponsor",
    "url": "http://sponsor.com",
    "description": "Big Sponsor",
    "level": "TestSponsor",
    "sponsor_type": "Gold",
}

POST_TRACK_DATA = {
    "description": "TestTrack",
    "name": "TestTrack",
    "color": "red",
    "track_image_url": "http://imgur.com/image.png",
    "location": "Some Street, Some City",
}

POST_USER_DATA = {
    "email": "test@gmail.com",
    "password": "test"
}

PUT_USER_DATA = {
    "email": "email@domain.com",
    "user_detail": {
        "avatar": "http://website.com/image.ext",
        "contact": "string",
        "details": "TestUser",
        "facebook": "string",
        "fullname": "TestUser",
        "twitter": "string"
    }
}

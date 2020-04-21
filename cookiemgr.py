from flask import json,session

from models import db,Resources

def addmedia(request):
    # mediatype = request.values['mediatype']
    mediaid = request.values['mediaid']
    mediatype = db.session.query(Resources.res_type).filter(Resources.resource_id == mediaid).first().res_type
    current_contents = sessioinToContents()
    content = {}

    content['mediatype'] = mediatype
    content['mediaid'] = mediaid
    if mediatype == 'video':
        content['duration'] = 0
    else:
        content['duration'] = 3
    current_contents.append(content)
    jsonstr = json.dumps(current_contents)
    return jsonstr


def duration(request):
    mediaid = request.values['mediaid']
    duration = request.values['duration']
    current_contents = sessioinToContents()
    for content in current_contents:
        if content['mediaid'] == mediaid:
            content['duration'] = duration
    jsonstr = json.dumps(current_contents)
    return jsonstr
def delete(request):
    mediaid = request.values['mediaid']
    current_contents = sessioinToContents()
    for content in current_contents:
        if content['mediaid'] == mediaid:
            current_contents.remove(content)
            break
    jsonstr = json.dumps(current_contents)
    return jsonstr
def cookieToContents(cookie):
    current_contents = []
    current_contents_json = cookie.get('currentcontents')
    if None != current_contents_json and "" != current_contents_json:
        current_contents = json.loads(current_contents_json)

    return current_contents
def sessioinToContents():
    current_contents = []
    current_contents_json = session.get('currentcontents')
    if None != current_contents_json and "" != current_contents_json:
        current_contents = json.loads(current_contents_json)

    return current_contents
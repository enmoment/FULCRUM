from moviepy.editor import *
from flask import json
import dbmgr


def create(jobid, contents_json):
    contents = json.loads(contents_json)
    clips = []
    i = 0
    size = (0, 0)
    for content in contents:
        respath = dbmgr.get_res_path(content['mediaid'])
        duration = content['duration']
        if content['mediatype'] == 'pic':
            imgclip = ImageClip(img=respath, duration=duration)

            if i == 0:
                size = imgclip.size
                clips.append(imgclip.fadeout(0.5, (1, 1, 1)))
            else:
                clips.append(imgclip.resize(size).fadeout(0.5, (1, 1, 1)).fadein(1, (1, 1, 1)))

            i += 1
    finalclip = concatenate_videoclips(clips)
    filename = "%s.mp4" % str(jobid)

    finalclip.write_videofile(os.path.join('output', filename), fps=25)
    dbmgr.update_job_status(jobid=jobid, status='1', filename=filename)

# create(1, contentstr)

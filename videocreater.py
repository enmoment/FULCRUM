from moviepy.editor import *
from flask import json
import dbmgr


def create(jobid, contents_json):
    contents = json.loads(contents_json)
    clips = []
    i = 0 #尺寸初始化标志
    size = (0, 0)
    for content in contents:
        respath = dbmgr.get_res_path(content['mediaid'])
        duration = content['duration']
        #clip = None
        mediatype = content['mediatype']
        if  mediatype == 'pic':
            clip = getpicClip(size=size,respath=respath,duration=duration)

        elif mediatype == 'video':
            clip = getvideoClip(size=size,respath=respath,duration=duration)

        if i == 0:
            size = clip[0].size
        clips.extend(clip)

        i += 1
    finalclip = concatenate_videoclips(clips)
    filename = "%s.mp4" % str(jobid)

    finalclip.write_videofile(os.path.join('output', filename), fps=25)
    dbmgr.update_job_status(jobid=jobid, status='1', filename=filename)

# create(1, contentstr)
def getpicClip(size,respath,duration):
    clips = []
    clip = ImageClip(img=respath, duration=duration)
    clips.append(clipTrans(size=size,clip=clip))
    return clips
def getvideoClip(size,respath,duration):
    clips = []
    clip = VideoFileClip(filename=respath)
    if duration != 0:
        #按duration截取视频
        timestamps = duration.split('|')
        for time in timestamps:
            sub = time.split(',')
            clips.append(clipTrans(size,clip.subclip(float(sub[0]),float(sub[1]))))
    else:
        clips.append(clipTrans(size=size,clip=clip))

    return clips
def clipTrans(size,clip):
    if size != (0, 0):
        return clip.resize(size).fadeout(0.5, (1, 1, 1)).fadein(1, (1, 1, 1))
    else:
        return clip.fadeout(0.5, (1, 1, 1))
from moviepy.editor import *
from flask import json
import dbmgr
from config import Config

def create(jobid, contents_json,jobname):
    contents = json.loads(contents_json)
    clips = []
    i = 0  # 尺寸初始化标志
    size = (0, 0)
    for content in contents:
        respath = dbmgr.get_res_path(content['mediaid'])
        duration = content['duration']
        # clip = None
        mediatype = content['mediatype']
        if mediatype == 'pic':
            clip = getpicClip(size=size, respath=respath, duration=duration)

        elif mediatype == 'video':
            clip = getvideoClip(size=size, respath=respath, duration=duration)

        if i == 0:
            size = clip[0].size
        clips.extend(clip)

        i += 1
    finalclip = concatenate_videoclips(clips)
    txt_clip = TextClip(str(jobname), fontsize=70, color='white')
    txt_clip = txt_clip.set_pos(lambda t: ('center', 150+t)).set_duration(3)
    finalclip = CompositeVideoClip([finalclip, txt_clip])
    dir = Config.VIDEO_OUTPUT_FOLDER
    filename = str(jobid)+'.mp4'
    thumbnail = str(jobid)+'.png'
    finalclip.write_videofile(filename=os.path.join(dir, filename), fps=24, remove_temp=True)
    finalclip.save_frame(os.path.join(dir,thumbnail))
    finalclip.close()
    # save output info
    dbmgr.update_job_status(jobid=jobid, status='1', filename=filename,thumbnail=thumbnail)


# create(1, contentstr)
def getpicClip(size, respath, duration):
    clips = []
    clip = ImageClip(img=respath, duration=float(duration))
    clips.append(clipTrans(size=size, clip=clip))
    return clips


def getvideoClip(size, respath, duration):
    clips = []
    clip = VideoFileClip(filename=respath)
    if duration != 0:
        # 按duration截取视频
        timestamps = duration.split('|')
        for time in timestamps:
            sub = time.split(',')
            clips.append(clipTrans(size, clip.subclip(float(sub[0]), float(sub[1]))))
    else:
        clips.append(clipTrans(size=size, clip=clip))

    return clips


def clipTrans(size, clip):
    if size != (0, 0):
        return clip.resize(size).fadeout(0.5, (1, 1, 1)).fadein(1, (1, 1, 1))
    else:
        return clip.fadeout(0.5, (1, 1, 1))

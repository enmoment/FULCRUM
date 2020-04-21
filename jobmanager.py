from models import db, Resources,Jobs
import videocreater


import _thread
def start(jobid):
    try:
        contents_json = db.session.query(Jobs.contents).filter(Jobs.job_id == jobid).first()
        _thread.start_new_thread(videocreater.create,(jobid,contents_json[0]))
        return 'success'
    except:
        return None

# def getResPath(mediaid):
#     respath = db.session.query(Resources.res_path,Resources.file_name).filter(Resources.resource_id == mediaid).first()
#     path = os.path.join(respath[0],respath[1])
#     return path

def savejob(jobname,contents_str,username):
    job = Jobs(job_name=jobname,contents=contents_str,username=username)
    try:
        db.session.add(job)
        db.session.commit()
        return job.job_id
    except:
        return None
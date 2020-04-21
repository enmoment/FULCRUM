# from app import db
from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()


class Resources(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    res_type = db.Column(db.Integer, primary_key=False, nullable=False)
    res_class = db.Column(db.String(500), primary_key=False, nullable=False)
    res_subclass = db.Column(db.String(500), primary_key=False, nullable=False)
    res_title = db.Column(db.String(500), primary_key=False, nullable=False)
    res_path = db.Column(db.String(500), primary_key=False, nullable=False)
    file_name = db.Column(db.String(500), primary_key=False, nullable=False)

    reference_count = db.Column(db.Integer, primary_key=False, nullable=True)
    res_origin = db.Column(db.String(1000), primary_key=False, nullable=True)
    imp_time = db.Column(db.String(100), primary_key=False, nullable=False)
    comment1 = db.Column(db.String(500), primary_key=False, nullable=True)
    comment2 = db.Column(db.String(500), primary_key=False, nullable=True)
    comment3 = db.Column(db.String(500), primary_key=False, nullable=True)
    comment4 = db.Column(db.String(500), primary_key=False, nullable=True)
    comment5 = db.Column(db.String(500), primary_key=False, nullable=True)

    def __init__(self, res_type='other', res_class='other', res_subclass='other', res_title='other', res_path=None,
                 file_name=None, res_origin='', comment1='', comment2='', comment3='', comment4='', comment5=''):
        self.res_type = str.strip(res_type)
        self.res_class = str.strip(res_class)
        self.res_subclass = str.strip(res_subclass)
        self.res_title = str.strip(res_title)
        self.res_path = str.strip(res_path)
        self.file_name = str.strip(file_name)
        self.reference_count = 0
        self.res_origin = str.strip(res_origin)
        self.imp_time = str(time.time())
        self.comment1 = str.strip(comment1)
        self.comment2 = str.strip(comment2)
        self.comment3 = str.strip(comment3)
        self.comment4 = str.strip(comment4)
        self.comment5 = str.strip(comment5)
        # self.resource_id =hashlib.md5(('66'+self.res_path+self.imp_time).encode(encoding='utf-8')).hexdigest()
        # print(self.resource_id)


class Jobs(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(), primary_key=False, nullable=False)
    job_status = db.Column(db.String(), primary_key=False, nullable=False)
    contents = db.Column(db.String(), primary_key=False, nullable=False)
    username = db.Column(db.String(), primary_key=False, nullable=False)
    start_date = db.Column(db.String(), primary_key=False, nullable=False)
    start_time = db.Column(db.String(), primary_key=False, nullable=False)
    finish_date = db.Column(db.String(), primary_key=False, nullable=False)
    finish_time = db.Column(db.String(), primary_key=False, nullable=False)
    outputpath = db.Column(db.String(), primary_key=False, nullable=False)
    comment = db.Column(db.String(), primary_key=False, nullable=True)

    def __init__(self, job_id='', job_name='', job_status='0', contents='',
                 username='', start_date='', stat_time='', comment=''):
        self.job_name = str.strip(job_name)
        self.job_status = str.strip(job_status)
        self.contents = str.strip(contents)
        self.username = str.strip(username)
        self.start_date = time.strftime("%Y-%m-%d", time.localtime())
        self.start_time = time.strftime("%H:%M:%S", time.localtime())
        self.comment = str.strip(comment)
        self.finish_date = ''
        self.finish_time = ''

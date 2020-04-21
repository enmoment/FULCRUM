import os
from flask_uploads import UploadSet, IMAGES,ALL
# app.secret_key = SECRET_KEY
# app.config.setdefault('BOOTSTRAP_SERVER_LOCAL',True)  os.path.join(basedir,'database.sqlite')
from datetime import timedelta


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.urandom(24)
    # 'postgresql+psycopg2://user:password@hostname/database_name'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql+psycopg2://postgres:postgres@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BOOTSTRAP_SERVER_LOCAL = True
    RESULT_SAVE_DIRECTORY = 'results'
    VIDEO_OUTPUT_FOLDER = os.path.join(basedir, 'output')

    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    RES_FOLDER = 'RES'
    UPLOADED_RESFILES_DEST = os.path.join(basedir,'upload')
    TYPES = tuple('jpg jpe jpeg png gif svg bmp avi mp4 wmv MP4'.split())
    UPLOADED_RESFILES_ALLOW = TYPES

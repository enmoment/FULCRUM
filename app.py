import numpy
from flask import (Flask, render_template, redirect, url_for, request, session, send_from_directory, json,
                   make_response)
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads
from sqlalchemy import func
import cookiemgr
import jobmanager
from config import Config
from fileImport import FileImporter
from forms import LoginForm
from models import db, Resources, Jobs

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db.init_app(app)
resfiles = UploadSet('RESFILES')
configure_uploads(app, resfiles)


@app.route('/', methods=['GET', 'POST'])
def default():
    username = request.cookies.get('username')
    session.permanent = True
    if None != username and '' != username:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = login_form.username.data
        response = redirect(url_for('index'))
        response.set_cookie('username', user)
        return response
    return render_template('login.html', title='login', loginform=login_form)


# 主页
@app.route('/index', methods=['GET', 'POST'])
def index(restype='', resclass='', subclass=''):
    types = db.session.query(Resources.res_type).group_by(Resources.res_type).all()

    return render_template('index.html', title='index', types=types)


# 获取资源大类
@app.route('/getresclass', methods=['POST'])
def getrescla():
    restype = request.values['restype']
    resclasses = db.session.query(Resources.res_class).filter(Resources.res_type == restype).group_by(
        Resources.res_class).all()

    resclass_json = dbToJson(resclasses)
    return resclass_json


# 获取资源小类
@app.route('/getressub', methods=['POST'])
def getressub():
    restype = request.values['restype']
    resclass = request.values['resclass']
    resclasses = db.session.query(Resources.res_subclass).filter(Resources.res_class == resclass,
                                                                 Resources.res_type == restype).group_by(
        Resources.res_subclass).all()
    ressubclass_json = dbToJson(resclasses)
    return ressubclass_json


# 获取标题
@app.route('/gettitles', methods=['POST'])
def gettitles():
    restype = request.values['restype']
    resclass = request.values['resclass']
    ressubclass = request.values['ressubclass']
    titles = db.session.query(Resources.res_title, func.count('1'), func.max(Resources.imp_time)).filter(
        Resources.res_type == restype,
        Resources.res_class == resclass, Resources.res_subclass == ressubclass).group_by(
        Resources.res_title).order_by(func.max(Resources.imp_time).desc()).all()
    title_json = dbToJson(titles)
    return title_json


# 获取资源明细
@app.route('/getpics/<type>/<rclass>/<subclass>/<title>', methods=['GET', 'POST'])
def getpics(type, rclass, subclass, title):
    print(request)
    reses = db.session.query(Resources).filter(
        Resources.res_type == type,
        Resources.res_class == rclass, Resources.res_subclass == subclass, Resources.res_title == title) \
        .order_by(Resources.imp_time.desc()).all()
    return render_template('picres.html', title='图片素材', pics=reses)


# 获取资源文件
@app.route('/res/<resid>', methods=['GET', 'POST'])
def res(resid):
    resPath = db.session.query(Resources).filter(Resources.resource_id == resid).first()
    return send_from_directory(resPath.res_path, resPath.file_name)


# 素材导入
@app.route('/importer', methods=['POST', 'GET'])
def importer():
    return render_template('importer.html', title='资源导入')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'resfiles' in request.files:
        resclass = request.values.get('resclass')
        ressubclass = request.values.get('ressubclass')
        title = request.values.get('title')
        for file in request.files.getlist('resfiles'):
            filename = resfiles.save(file,folder=title)
            print(filename)
        FileImporter(title,resclass,ressubclass)
    return render_template('importer.html')


# 手工导入文件
@app.route('/fileimport/<path>/<resclass>/<ressubclass>', methods=['GET'])
def fileimport(path, resclass, ressubclass):
    importer = FileImporter(path, resclass, ressubclass)
    return 'ok'


# 添加媒体文件
@app.route('/medialist', methods=['POST'])
def medialist():
    username = request.cookies.get('username')
    oprate = request.values['oprate']
    jsonstr = ''

    if oprate == 'add':
        jsonstr = cookiemgr.addmedia(request)
    elif oprate == 'duration':
        jsonstr = cookiemgr.duration(request)
    elif oprate == 'delete':
        jsonstr = cookiemgr.delete(request)

    response = make_response("success")
    # response.set_cookie('currentcontents', jsonstr)
    session['currentcontents'] = jsonstr
    return response


@app.route('/contentlist', methods=['GET', 'POST'])
def contentlist():
    current_content = cookiemgr.sessioinToContents()

    return render_template('createvideo.html', title='视频生成', contents=current_content)


# 开始生成视频
@app.route('/createvideo', methods=['GET', 'POST'])
def createvideo():
    oprate = request.values['oprate']
    if oprate == 'create':
        jobname = request.values['jobname']

        current_contents_json = session.get('currentcontents')
        username = request.cookies.get('username')
        jobid = jobmanager.savejob(jobname=jobname, contents_str=current_contents_json, username=username)
        response = make_response('Failed')
        if jobid is not None:
            jobmanager.start(jobid)
            response = make_response(str(jobid))
            session.pop('currentcontents')
        return response


# 任务清单
@app.route('/joblist', methods=['GET', 'POST'])
def joblist():
    if request.method == 'POST':
        oprate = request.values['oprate']
        jobid = request.values['jobid']
        if oprate == 'delete':
            job = db.session.query(Jobs).filter(Jobs.job_id == jobid)
            job.update({"job_status": "999"})
            db.session.commit()
            # print(job)
            return 'success'
        elif oprate == 'reload':
            job = db.session.query(Jobs).filter(Jobs.job_id == jobid).first()
            contents_json = job.contents
            if contents_json is not None and "" != contents_json:
                response = make_response("success")
                # response.set_cookie('currentcontents', contents_json)
                session['currentcontents'] = contents_json
                return response



    else:
        results = db.session.query(Jobs).filter(Jobs.job_status != '999').order_by(Jobs.job_id.desc()).all()
        return render_template('joblist.html', title='结果下载', results=results)


# 任务清单
@app.route('/downloads', methods=['GET', 'POST'])
def downloads():
    jobid = request.values['jobid']
    file = db.session.query(Jobs.outputpath).filter(Jobs.job_id == jobid).first()
    response = send_from_directory(Config.VIDEO_OUTPUT_FOLDER, file[0])
    return response


# list 转json
def dbToJson(db):
    result = []
    for r in db:
        result.append(r)
    keys = [str(x) for x in numpy.arange(len(result))]
    list_json = dict(zip(keys, result))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
    return str_json


@app.route('/initdb', methods=['GET', 'POST'])
def initdb():
    db.create_all()
    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

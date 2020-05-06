from flask_wtf import FlaskForm
from wtforms import *
from flask_wtf.file import  FileRequired
from flask_wtf.file import FileField
from wtforms.validators import  DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    # upload = FileField(validators=[FileRequired()])
    submit = SubmitField('登录')

class CreateForm(FlaskForm):

    submit = SubmitField('生成视频')

class importForm(FlaskForm):
    resclass = StringField('资源大类', validators=[DataRequired()])
    ressubclass = StringField('资源小类', validators=[DataRequired()])
    restitle = StringField('资源标题', validators=[DataRequired()])
    upload = FileField('upload',validators=[FileRequired()])
    submit = SubmitField('上传')

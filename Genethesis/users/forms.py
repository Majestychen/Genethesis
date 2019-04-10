from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from Genethesis.models import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, message="用户名至少6位。"), Length(max=20, message="用户名至多20位")])
    email = StringField('电子邮箱', validators=[DataRequired(), Email(message='这真的是个邮箱吗？我书读得少你别骗我。')])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, message='密码怎么说也得6位吧。')])
    confirmPassword = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次密码居然不一样你说气人不。')])
    submit = SubmitField('创建账户')
    
    #def validate_field(self, field):
        #if True:
            #raise ValidationError('Validation Massage')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'用户名 {username.data} 已经被捷足先登了，请直接登录或者换个名字试试。')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'电子邮箱 {email.data} 已经被注册过了，请直接登录或者换个名字试试。')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=20, message='用户名：一串您注册的时候自己随便发明的6到20位字符串。')])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, message='密码：一串您注册的时候自己随便发明的至少6位的字符串。')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self, username):
        if not username.errors:
            user = User.query.filter_by(username=username.data).first()
            if not user:
                raise ValidationError(f'我们的小本本上没有 {username.data} ，或许您可以直接注册。')


class UpdateAccountForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, message="用户名至少6位。"), Length(max=20, message="用户名至多20位")])
    email = StringField('电子邮箱', validators=[DataRequired(), Email(message='这真的是个邮箱吗？我书读得少你别骗我。')])
    firstName = StringField('名', validators=[Length(max=12, message="公安局真的可以注册这么长的名字吗？")])
    lastName = StringField('姓', validators=[Length(max=12, message="天底下真的有这么长的姓吗？")])
    university = StringField('大学', validators=[Length(max=60)])
    faculty = StringField('大学', validators=[Length(max=60)])
    grade = StringField('大学', validators=[Length(max=4, message="请输入四位数字，例如2015.")])   
    selfIntro = TextAreaField('个人简介')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'用户名 {username.data} 已经被捷足先登了，请直接登录或者换个名字试试。')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'电子邮箱 {email.data} 已经被注册过了，请直接登录或者换个名字试试。')

class PasswordChangeForm(FlaskForm):
    oldPw = PasswordField('旧密码', validators=[DataRequired(message='填一下旧密码啊……')])
    newPw = PasswordField('新密码', validators=[DataRequired(message='填一下新密码啊……'), Length(min=6, message='密码怎么说也得6位吧。')])
    confirmNewPw = PasswordField('确认新密码', validators=[DataRequired(message='确认一下新密码啊……'), EqualTo('newPw', message='两次密码居然不一样你说气人不。')])

class UserAvatarForm(FlaskForm):
    avatar = FileField('上传头像', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='这怕不是个图片吧……')])

class UserSignatureForm(FlaskForm):
    signature = FileField('上传签名', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='这怕不是个图片吧……')])
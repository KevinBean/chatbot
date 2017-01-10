# -*- coding=utf-8 -*-
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User

# 工程编辑页面
class EditProjectForm(Form):
    SystemRef_File = TextAreaField(u'输入系统提资文件')
    submit_systemref = SubmitField(u'提取系统提资信息')
    MaxCurrent_Detail = StringField(u'系统载流量提资')
    MaxCurrent_Value = StringField(u'系统载流量(A)')
    Voltage_Value = StringField(u'电压等级(kV)')
    Cable_Jiemian = StringField(u'电缆截面（mm2）')
    AutoChoose = RadioField(choices=[('value',u'自动选择'),('value_two',u'手动修改')])
    submit_autochoose = SubmitField(u'提交')




# chatbot聊天界面
class WebChatbotForm(Form):
    Chatroom = TextAreaField(u'聊天窗口')
    Input = StringField(u'请输入',validators=[Required()])
    submit = SubmitField(u'发送')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('Enter your comment', validators=[Required()])
    submit = SubmitField('Submit')

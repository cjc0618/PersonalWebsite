#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g
from wtforms import Form, SelectField, TextField, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from flask_login import current_user
from ..models import User


class MyLength(Length):
    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext('Field must be at least %(min)d character long.',
                                             'Field must be at least %(min)d characters long.', self.min)
                elif self.min == -1:
                    message = field.ngettext('Field cannot be longer than %(max)d character.',
                                             'Field cannot be longer than %(max)d characters.', self.max)
                else:
                    message = field.gettext('Field must be between %(min)d and %(max)d characters long.')

            raise ValidationError(message)


class MyEqualTo(EqualTo):
    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data != other.data:
            message = self.message
            if message is None:
                message = field.gettext('Field must be equal to %(other_name)s.')

            g.re['data']['password2'] = [2, u'']
            raise ValidationError(message)

        else:
            g.re['data']['password1'] = [0, u'密码设置正确']
            g.re['data']['password2'] = [0, u'']


class UsernameLoginForm(Form):
    username = StringField(validators=[
        DataRequired(message=[1, u'账号不能为空']),
        MyLength(2, 12, message=[1, u'请输入2-12长度的字符串或手机号码']),
        Regexp(u'^[A-Za-z\u4E00-\u9FA5]+[A-Za-z0-9\u4E00-\u9FA5_.]*$',
               0, [1, u'输入账号不合法'])])
    password = PasswordField(validators=[
        DataRequired(message=[1, u'密码不能为空']),
        MyLength(6, 12, message=[1, u'请输入6-12长度的字符串'])])

    def validate_username(self, filed):
        if g.user:
            g.re['data']['username'] = [0, u'账号正确']
            g.re['data']['login_user'] = filed.data
        else:
            raise ValidationError([2, u'账号不存在'])

    def validate_password(self, filed):
        if g.user:
            if not g.user.verify_password(filed.data):
                raise ValidationError([2, u'密码错误'])


class TelephoneLoginForm(Form):
    telephone = StringField(validators=[
        DataRequired(message=[1, u'账号不能为空']),
        MyLength(11, 11, message=[1, u'手机号码格式不对'])])
    password = PasswordField(validators=[
        DataRequired(message=[1, u'密码不能为空']),
        MyLength(6, 12, message=[1, u'请输入6-12长度的字符串'])])

    def validate_telephone(self, filed):
        if g.user:
            g.re['data']['telephone'] = [0, u'账号正确']
            g.re['data']['login_user'] = g.user.username
        else:
            raise ValidationError([2, u'账号不存在'])

    def validate_password(self, filed):
        if g.user:
            if not g.user.verify_password(filed.data):
                raise ValidationError([2, u'密码错误'])


class RegisterForm(Form):
    username = StringField(validators=[
        DataRequired(message=[2, u'用户名不能为空']),
        MyLength(2, 12, message=[2, u'请输入2-12长度的字符串']),
        Regexp(u'^[A-Za-z\u4E00-\u9FA5]+[A-Za-z0-9\u4E00-\u9FA5_.]*$',
               0, [2, u'用户名不能以数字开头'])])
    telephone = StringField(validators=[
        DataRequired(message=[2, u'手机号码不能为空']),
        MyLength(11, 11, message=[2, u'手机号码格式不对'])])
    email = StringField(validators=[
        DataRequired(message=[2, u'电子邮箱不能为空']),
        MyLength(1, 64, message=[2, u'电子邮箱格式不对']),
        Email(message=[2, u'电子邮箱格式不对'])])
    password1 = PasswordField(validators=[
        DataRequired(message=[2, u'密码不能为空']),
        MyLength(6, 12, message=[2, u'请输入6-12长度的字符串']),
        MyEqualTo('password2', message=[2, u'密码不一致'])])
    password2 = PasswordField(validators=[
        DataRequired(message=[2, u'密码不能为空']),
        MyLength(6, 12, message=[2, u'请输入6-12长度的字符串'])])

    def validate_username(self, filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError([2, u'该用户名已经注册'])
        else:
            g.re['data']['username'] = [0, u'用户名设置正确']

    def validate_telephone(self, filed):
        if User.query.filter_by(telephone=filed.data).first():
            raise ValidationError([2, u'该手机号码已经注册'])
        else:
            g.re['data']['telephone'] = [0, u'手机号码设置正确']

    def validate_email(self, filed):
        if User.query.filter_by(email=filed.data).first():
            raise ValidationError([2, u'该子邮箱已经注册'])
        else:
            g.re['data']['email'] = [0, u'子邮箱设置正确']


class ResetPasswordForm(Form):
    email = StringField(validators=[
        DataRequired(message=[2, u'电子邮箱不能为空']),
        MyLength(1, 64, message=[2, u'电子邮箱格式不对']),
        Email(message=[2, u'电子邮箱格式不对'])])
    password1 = PasswordField(validators=[
        DataRequired(message=[2, u'密码不能为空']),
        MyLength(6, 12, message=[2, u'请输入6-12长度的字符串']),
        MyEqualTo('password2', message=[2, u'密码不一致'])])
    password2 = PasswordField(validators=[
        DataRequired(message=[2, u'密码不能为空']),
        MyLength(6, 12, message=[2, u'请输入6-12长度的字符串'])])

    def validate_email(self, filed):
        if not User.query.filter_by(email=filed.data).first():
            raise ValidationError([2, u'电子邮箱未注册'])
        else:
            g.re['data']['email'] = [0, u'电子邮箱正确']


class ResetEmailForm(Form):
    oldEmail = StringField(validators=[
        DataRequired(message=[2, u'电子邮箱不能为空']),
        MyLength(1, 64, message=[2, u'电子邮箱格式不对']),
        Email(message=[2, u'电子邮箱格式不对'])])
    newEmail = StringField(validators=[
        DataRequired(message=[2, u'电子邮箱不能为空']),
        MyLength(1, 64, message=[2, u'电子邮箱格式不对']),
        Email(message=[2, u'电子邮箱格式不对'])])

    def validate_oldEmail(self, filed):
        if filed.data != current_user.email:
            raise ValidationError([2, u'该电子邮箱不是您原绑定的邮箱'])
        else:
            g.re['data']['oldEmail'] = [0, u'原电子邮箱正确']

    def validate_newEmail(self, filed):
        if filed.data == current_user.email:
            raise ValidationError([2, u'不能和原电子邮箱相同'])

        if User.query.filter_by(email=filed.data).first():
            raise ValidationError([2, u'该原电子邮箱已经注册'])

        g.re['data']['newEmail'] = [0, u'新电子邮箱设置正确']

class ArticleForm(Form):
    title = StringField(validators=[
        DataRequired(message=u'标题不能为空'),
        MyLength(2, 30, message=u'标题需要为2-30个字符组成')])
    class_name = StringField(validators=[
        DataRequired(message=u'文章类型不能为空')])
    body = TextField(validators=[
        DataRequired(message=u'文章内容不能为空')])

class QuestionForm(Form):
    title = StringField(validators=[
        DataRequired(message=u'标题不能为空'),
        MyLength(2, 30, message=u'标题需要为2-30个字符组成')])
    class_name = StringField(validators=[
        DataRequired(message=u'问题类型不能为空')])
    body = TextField(validators=[
        DataRequired(message=u'问题内容不能为空')])
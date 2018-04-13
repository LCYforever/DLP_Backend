#! /usr/bin/env python
# -*- coding: utf-8 -*-
from . import user
from ..models import User
from flask import request, jsonify, make_response
from functools import wraps
from .. import db
import json


def admin_login(func):
    """过滤器：验证token是否为管理员"""
    @wraps(func)
    def wrap(*args, **kwargs):
        u = User.verify_token(request.cookies.get('kubernetes_token'))
        if u and u.auth_level == 1:
            return func(*args, **kwargs)
        else:
            return 'you are not administrator', 400
    return wrap


@user.route('/reg', methods=['GET', 'POST'])
@admin_login
def reg():
    if request.method == 'GET':
        message_e = 'only post method is supported'
        return message_e, 404
    else:
        data = request.get_data()
        json_data = json.loads(data)
        username = json_data['username']
        password = json_data['password']
        if User.query.filter_by(username=username).first():
            message_e = 'The user has been already authorized'
            return message_e, 400
        else:
            u = User()
            u.username = username
            u.password = password
            u.auth_level = 0
            db.session.add(u)
            db.session.commit()
            message_e = 'authorize success'
            return message_e


@user.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        message_e = 'only post method is supported'
        return message_e
    else:
        data = request.get_data()
        json_data = json.loads(data)
        username = json_data['username']
        password = json_data['password']
        u = User.query.filter_by(username=username).first()
        if u is None:
            message_e = 'user is not exist'
            return message_e, 404
        if not u.verify_password(password):
            message_e = 'password incorrect'
            return message_e, 400
        else:
            return_data = {'id': u.id, 'username': username}
            rsp = make_response(jsonify(return_data))
            rsp.set_cookie('kubernetes_token', u.generate_token())
            return rsp



#! /usr/bin/env python
# -*- coding: utf-8 -*-
from . import main
from ..models import User
from ..util.authorize import admin_login
from flask import request, jsonify, make_response
from .. import db
import json


# 对用户的增删查改
@main.route('/user/', methods=['GET', 'POST', 'DELETE'])
@admin_login
def user():
    if request.method == 'GET':
        message_e = 'only post method is supported'
        return message_e, 404
    elif request.method == 'POST':
        """POST:注册用户"""
        json_data = json.loads(request.get_data())
        username = json_data['username']
        password = json_data['password']
        if User.query.filter_by(namespace=username).first():
            message_e = 'The username has been already registered'
            return jsonify({'message': message_e}), 400
        else:
            u = User()
            u.namespace = username
            u.password = password
            u.privilege = 1
            db.session.add(u)
            db.session.commit()
            return jsonify({'uid': u.id}), 200


@main.route('/auth/', methods=['GET', 'POST'])
def auth():
    """用户登录"""
    if request.method == 'POST':
        json_data = json.loads(request.get_data())
        username = json_data['username']
        password = json_data['password']
        u = User.query.filter_by(username=username).first()
        if u is None:
            message_e = 'user is not exist'
            return jsonify({'message': message_e}), 404

        if not u.verify_password(password):
            message_e = 'username or password is incorrect'
            return jsonify({'message': message_e}), 400
        else:
            return_data = {'id': u.id, 'username': username}
            resp = make_response(jsonify(return_data))
            resp.set_cookie('kubernetes_token', u.generate_token())
            return resp
    else:
        message_e = 'only post method is supported'
        return jsonify({'message': message_e})

#! /usr/bin/env python
# -*- coding: utf-8 -*-
from . import main
from ..models import User
from ..util.authorize import admin_login
from flask import request, jsonify, make_response
from .. import db
import json


"""
    对用户的增删查改
"""


@main.route('/user/', methods=['GET', 'POST', 'DELETE'])
@admin_login
def user():
    if request.method == 'GET':
        """GET:查询用户"""
        uid = request.args.get('uid')
        if uid:
            """查询单个用户"""
            u = User.query.get(uid)
            if u:
                if u.privilege == 0:
                    return jsonify(uid=u.id, username=u.namespace, role='admin')
                else:
                    return jsonify(uid=u.id, username=u.namespace)
            else:
                message_e = 'The user does not exist'
                return jsonify({'message': message_e}), 404
        else:
            """查询所有用户"""
            all_user = User.query.all()
            user_list = list()
            for u in all_user:
                if u.privilege == 0:
                    u_dict = dict(uid=u.id, username=u.namespace, role='admin')
                else:
                    u_dict = dict(uid=u.id, username=u.namespace)
                user_list.append(u_dict)
            return jsonify({'users': user_list})

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
            return jsonify({'uid': u.id})


@main.route('/auth/', methods=['GET', 'POST'])
def auth():
    """用户登录"""
    if request.method == 'POST':
        json_data = json.loads(request.get_data())
        username = json_data['username']
        password = json_data['password']
        u = User.query.filter_by(namespace=username).first()
        if u is None:
            message_e = 'the user does not exist'
            return jsonify({'message': message_e}), 404

        if not u.verify_password(password):
            message_e = 'username or password is incorrect'
            return jsonify({'message': message_e}), 400
        else:
            if u.privilege == 0:
                resp = make_response(jsonify(uid=u.id, username=username, role='admin'))
            else:
                resp = make_response(jsonify(uid=u.id, username=username))
            resp.set_cookie('kubernetes_token', u.generate_token())
            return resp
    else:
        message_e = 'only post method is supported'
        return jsonify({'message': message_e})

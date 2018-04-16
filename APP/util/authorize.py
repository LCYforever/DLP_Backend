#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ..models import User
from flask import request, jsonify
from functools import wraps


def admin_login(func):
    """过滤器：已经使用管理员身份登录"""
    @wraps(func)
    def wrap(*args, **kwargs):
        u = User.verify_token(request.cookies.get('kubernetes_token'))
        if u and u.privilege == 0:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'you are not an administrator'}), 403
    return wrap

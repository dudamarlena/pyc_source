# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\testapp\views.py
# Compiled at: 2017-09-22 02:58:12
# Size of source mod 2**32: 693 bytes
from django.shortcuts import render
from flask import Blueprint, request, render_template
testapp = Blueprint('auth', __name__, url_prefix='/auth')

@testapp.route('/hello')
def hello():
    return render_template('testapp/hello.html')


def fibPrint(n):
    a, b = (0, 1)
    while b < n:
        print(b)
        a, b = b, a + b


def fibReturn(n):
    result = []
    a, b = (0, 1)
    while b < n:
        result.append(b)
        a, b = b, a + b

    return result


def LogPrint(strMsg):
    print('msg from lib yooooooo: ', strMsg)
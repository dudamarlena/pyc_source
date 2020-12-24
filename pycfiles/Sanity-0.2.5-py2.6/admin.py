# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sanity/views/admin.py
# Compiled at: 2010-06-16 00:48:04
from functools import wraps
from flask import Module, render_template, g, request, flash, session, redirect, url_for, escape
from sanity.models import User, Task, Tag, Group
from sanity import db
admin = Module(__name__)

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        else:
            if not g.user.admin:
                return redirect(url_for('frontend.index'))
            return f(*args, **kwargs)

    return decorated_function


@admin.route('/')
@admin_required
def index():
    return 'Hello admin!'


@admin.route('/groups', methods=['GET', 'POST'])
@admin_required
def groups():
    error = ''
    if request.method == 'POST':
        name = request.form.get('name')
        if name is None:
            error = 'You must enter a group name'
        else:
            db.session.add(Group(name))
            db.session.commit()
            return redirect(url_for('index'))
    else:
        groups = Group.query.all()
    return render_template('admin/groups.html', error=error, groups=groups)


@admin.route('/tags', methods=['GET', 'POST'])
def tags():
    pass


@admin.route('/tasks', methods=['GET', 'POST'])
def tasks():
    pass


@admin.route('/users', methods=['GET', 'POST'])
def users():
    pass
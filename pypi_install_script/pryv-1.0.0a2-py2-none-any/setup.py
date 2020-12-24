# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request, session

from pryv.user import count as count_users, find as find_user, create as create_user
from pryv.config import config

controller = Blueprint('setup', 'setup', url_prefix='/setup')


@controller.route(
    '',
    methods=['GET'],
    strict_slashes=False
)
def get_setup():
    if count_users() > 0:
        return redirect(url_for('get_login'))

    return render_template(
        'explorer/setup.html',
        config=config,
        error=None,
    )


@controller.route(
    '',
    methods=['POST'],
    strict_slashes=False,
)
def post_setup():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirmpassword', '')

    if len(username) < 3:
        return render_template(
            'explorer/setup.html',
            config=config,
            error='username should be at least 3 characters long',
            username=username,
        )

    if find_user(username):
        return render_template(
            'explorer/setup.html',
            config=config,
            error='username already exists',
            username=username,
        )

    if password != confirm_password:
        return render_template(
            'explorer/setup.html',
            config=config,
            error='passwords don\'t match',
            username=username,
        )

    create_user(username, password)

    session['authenticated'] = True
    session['username'] = username

    return redirect(url_for('get_login'))


def mount(app):
    app.register_blueprint(controller)

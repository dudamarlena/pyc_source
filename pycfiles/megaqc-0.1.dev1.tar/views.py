# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ewels/GitHub/MegaQC/megaqc/user/views.py
# Compiled at: 2018-07-06 11:43:42
"""User views."""
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from megaqc.extensions import db
from megaqc.user.models import User
from megaqc.user.forms import PasswordChangeForm, AdminForm
blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

@blueprint.route('/')
@login_required
def profile():
    """Show user profile."""
    return render_template('users/profile.html')


@blueprint.route('/multiqc_config')
@login_required
def multiqc_config():
    """Instructions for MultiQC configuration."""
    return render_template('users/multiqc_config.html')


@blueprint.route('/password')
@login_required
def change_password():
    """Change user password."""
    form = PasswordChangeForm()
    return render_template('users/change_password.html', form=form)


@blueprint.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        abort(403)
    else:
        users_data = db.session.query(User).all()
        form = AdminForm()
        return render_template('users/manage_users.html', users_data=users_data, form=form)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/forms/auto.py
# Compiled at: 2015-02-11 13:44:16
import wtforms
from flask import render_template, request, Markup, abort, flash, redirect, escape, url_for, make_response
from .. import b__ as __
from .form import Form
from .fields import SubmitField

class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """
    delete = SubmitField(__('Delete'))
    cancel = SubmitField(__('Cancel'))


def render_form(form, title, message='', formid='form', submit=__('Submit'), cancel_url=None, ajax=False):
    multipart = False
    for field in form:
        if isinstance(field.widget, wtforms.widgets.FileInput):
            multipart = True

    if form.errors:
        code = 200
    else:
        code = 200
    if request.is_xhr and ajax:
        return make_response(render_template('baseframe/ajaxform.html', form=form, title=title, message=message, formid=formid, submit=submit, cancel_url=cancel_url, multipart=multipart), code)
    else:
        return make_response(render_template('baseframe/autoform.html', form=form, title=title, message=message, formid=formid, submit=submit, cancel_url=cancel_url, ajax=ajax, multipart=multipart), code)


def render_message(title, message, code=200):
    if request.is_xhr:
        return make_response(Markup('<p>%s</p>' % escape(message)), code)
    else:
        return make_response(render_template('baseframe/message.html', title=title, message=message), code)


def render_redirect(url, code=302):
    if request.is_xhr:
        return make_response(render_template('baseframe/redirect.html', url=url))
    else:
        return redirect(url, code=code)


def render_delete_sqla(obj, db, title, message, success='', next=None, cancel_url=None):
    if not obj:
        abort(404)
    form = ConfirmDeleteForm()
    if request.method in ('POST', 'DELETE') and form.validate():
        if 'delete' in request.form or request.method == 'DELETE':
            db.session.delete(obj)
            db.session.commit()
            if success:
                flash(success, 'success')
            return render_redirect(next or url_for('index'), code=303)
        else:
            return render_redirect(cancel_url or next or url_for('index'), code=303)

    return make_response(render_template('baseframe/delete.html', form=form, title=title, message=message))
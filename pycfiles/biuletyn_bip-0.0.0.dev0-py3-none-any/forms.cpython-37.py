# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/utils/forms.py
# Compiled at: 2019-09-03 15:15:23
# Size of source mod 2**32: 1552 bytes
import attr
from flask import Markup, render_template_string
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField
from ..ext import db

class Renderable:

    def render(self):
        return Markup(render_template_string((self.template), obj=self))


@attr.s
class Link(Renderable):
    href = attr.ib()
    text = attr.ib(default='klik')
    template = ''.join([
     '<a href="{{ obj.href }}">',
     '{{ obj.text }}',
     '</a>'])


@attr.s
class Button(Renderable):
    type_ = attr.ib(default='submit')
    class_ = attr.ib(default='primary')
    icon = attr.ib(default='check')
    icon_type = attr.ib(default='fas')
    text = attr.ib('ok')
    template = ''.join([
     '<button type="{{ obj.type_ }}" class="btn btn-{{ obj.class_ }}">',
     '<i class="{{ obj.icon_type }} fa-{{ obj.icon }}"></i>',
     '&nbsp;',
     '{{ obj.text }}',
     '</button>'])


class ConfirmationForm(FlaskForm):
    is_confirmed = BooleanField('potwierdź', default=False)
    buttons = [
     Button(text='potwierdź', icon='skull-crossbones')]

    def confirm(self):
        if self.is_confirmed.data:
            return True
        return False


class ObjectForm(FlaskForm):
    buttons = [
     Button(text='zapisz'),
     Link(href='javascript:history.back()', text='powrót')]

    def save(self, obj, save=True):
        self.populate_obj(obj)
        db.session.add(obj)
        if save:
            db.session.commit()
        else:
            db.session.flush()
        return obj
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/views/meta.py
# Compiled at: 2015-07-11 00:04:30
# Size of source mod 2**32: 1743 bytes
import os
from ginger import utils
from os import path

class ViewInfo(object):

    def __init__(self, app, view_name):
        super(ViewInfo, self).__init__()
        self.app = app
        self.view_name = view_name
        name = utils.camel_to_underscore(self.view_name)
        banned = {'view', 'wizard'}
        self.url_name = '_'.join(w for w in name.split('_') if w and w not in banned)

    @property
    def template_dir(self):
        folder = self.app.path
        return os.path.join(folder, 'templates')

    @property
    def template_name(self):
        name = '%s/%s.html' % (self.app.label, self.url_name)
        return name

    @property
    def template_path(self):
        return os.path.join(self.template_dir, self.template_name)

    @property
    def form_name(self):
        parts = self.url_name.split('_')
        parts.append('Form')
        return ''.join(p.capitalize() for p in parts)

    @property
    def view_module_name(self):
        return '%s.views' % (self.app.module.__name__,)

    @property
    def form_module_name(self):
        return '%s.forms' % (self.app.module.__name__,)

    @property
    def view_class_name(self):
        return '%sView' % ''.join(p.capitalize() for p in self.fragments)

    @property
    def resource_name(self):
        return '_'.join(self.fragments[:-1])

    @property
    def fragments(self):
        return self.url_name.split('_')

    @property
    def form_path(self):
        return os.path.join(self.app.path, 'forms.py')

    @property
    def verb(self):
        return self.fragments[(-1)]

    @property
    def url_verb(self):
        verb = self.verb
        if verb not in {'home', 'default', 'list', 'detail', 'index'}:
            return verb
        return ''
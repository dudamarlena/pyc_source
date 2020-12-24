# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/luyu/venv/lib/python2.7/site-packages/django_kss/pykss/modifier.py
# Compiled at: 2015-02-08 05:03:44


class Modifier(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.example = ''

    @property
    def class_name(self):
        return self.name.replace('.', ' ').replace(':', ' pseudo-class-').strip()

    def add_example(self, example):
        self.example = example.replace('$modifier_class', '%s' % self.class_name)
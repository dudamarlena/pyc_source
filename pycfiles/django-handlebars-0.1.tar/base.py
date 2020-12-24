# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergii/eclipse-workspaces/django_handlebars/django_handlebars/management/observer/base.py
# Compiled at: 2012-03-11 19:54:51
import os

class BaseObserver(object):

    def __init__(self, source_dir, compiler):
        if not os.access(source_dir, os.R_OK):
            raise OSError('Dir "%s" is not readable' % source_dir)
        self.source_dir = source_dir
        self.compiler = compiler

    def start(self):
        raise NotImplemented('Method start() must be implemented in subclass')

    def stop(self):
        raise NotImplemented('Method stop() must be implemented in subclass')
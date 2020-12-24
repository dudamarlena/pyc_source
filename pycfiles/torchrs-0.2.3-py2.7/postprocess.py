# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchrs/module/postprocess.py
# Compiled at: 2014-09-19 05:47:46
__author__ = 'Binh Vu <binh@toan2.com>'

class PostProcess(object):

    def __init__(self, module):
        self.module = module

    def execute(self, config, extra):
        if 'postexecute' in config:
            module = {'location': self.module.location, 'name': config['name'], 
               'root': extra['root']}
            exec config['postexecute']
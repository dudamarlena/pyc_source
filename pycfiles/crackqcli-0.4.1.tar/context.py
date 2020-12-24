# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/context.py
# Compiled at: 2016-12-29 01:49:52
import logging, os
from ConfigParser import ConfigParser

class Context:

    def __init__(self, db, logger, arg_namespace):
        self.db = db
        self.log = logger
        self.log.debug = logging.debug
        self.localip = None
        self.conf = ConfigParser()
        self.conf.read(os.path.expanduser('~/.cme/cme.conf'))
        for key, value in vars(arg_namespace).iteritems():
            setattr(self, key, value)

        return
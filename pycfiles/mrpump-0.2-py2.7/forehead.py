# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/forehead.py
# Compiled at: 2012-05-05 17:27:23
import logging

class Forehead(object):
    """On or in a golem's forehead is written what he is to do."""

    def __init__(self):
        self.log = logging.getLogger('Forehead')
        self.chems = []

    def add(self, chem):
        self.chems.append(chem)

    def __call__(self, sender_screen_name, text, reply):
        text = text.lstrip('0123456789 ')
        done = False
        for c in self.chems:
            if not done and c.appliesTo(text):
                self.log.info('%r gets message %s', c, text)
                try:
                    c(sender_screen_name, text, reply)
                    done = True
                except Exception as e:
                    self.log.error('while dealing with message %r', message)
                    self.log.exception(e)

        if not done:
            reply('did not understand %s', text)
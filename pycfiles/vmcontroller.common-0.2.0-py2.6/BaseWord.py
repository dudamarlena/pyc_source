# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/BaseWord.py
# Compiled at: 2011-03-04 15:52:41
"""
BaseWord
"""
try:
    import time, pdb, stomper, inject
    from vmcontroller.common import support
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

class BaseWord(object):
    """ Initializes the Frame object with the inheriting class' name """

    @inject.param('subject')
    def __init__(self, subject):
        self.subject = subject
        self.frame = stomper.Frame()
        self.frame.cmd = 'SEND'
        self.frame.body = self.name
        headers = {}
        headers['from'] = subject.descriptor.id
        headers['timestamp'] = str(time.time())
        self.frame.headers = headers

    @property
    def name(self):
        """ Get the word's name """
        return self.__class__.__name__
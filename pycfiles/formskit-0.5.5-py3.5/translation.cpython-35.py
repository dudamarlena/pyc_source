# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/translation.py
# Compiled at: 2015-07-25 09:04:48
# Size of source mod 2**32: 807 bytes


class Translation(object):

    def __init__(self, copy=None):
        if copy:
            self.init(copy.text)
            self.args = copy.args
            self.kwargs = copy.kwargs
        else:
            self.init(None)

    def init(self, text, *args, **kwargs):
        self.text = text
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.translate().format(*self.args, **self.kwargs)

    def translate(self):
        return self.text


class Translable(object):

    def reset(self):
        """
        Remove all the messages.
        """
        self.messages = []

    def get_error_messages(self):
        """
        Get all error messages.
        """
        return [message() for message in self.messages]
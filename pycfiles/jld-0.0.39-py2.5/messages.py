# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\tools\messages.py
# Compiled at: 2009-03-16 14:55:29
""" Messages interface
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: messages.py 884 2009-03-16 18:55:28Z JeanLou.Dupont $'
import yaml, os, sys
from string import Template

class Messages(object):

    def __init__(self, path):
        """
            @param path: filesystem path to YAML messages
        """
        self.filepath = path
        self.msgs = None
        return

    def _load(self):
        """ Loads the messages from the filesystem
        """
        file = open(self.filepath, 'r')
        self.msgs = yaml.load(file)
        file.close()

    def __getitem__(self, key):
        if self.msgs is None:
            self._load()
        try:
            return self.msgs[key]
        except:
            raise RuntimeError('missing message [%s]' % key)

        return

    def render(self, key, params=None):
        """ Renders a message template with optional parameters
        
            @param key: the message key
            @param params: the optional parameters
            @return: the rendered message (string)
        """
        tpl = Template(self[key])
        return tpl.substitute(params).lstrip()

    def render2(self, key, params=None):
        """ Renders a template through the 'old' python string templating engine
            @param key: the message key
            @param params: the parameters
            @return: rendered string
        """
        tpl = self[key]
        if params:
            return tpl % params
        return tpl


if __name__ == '__main__':
    path = os.path.dirname(__file__) + os.sep + 'messages.yaml'
    msg = Messages(path)
    params = {'msg': 'message'}
    print msg.render('msg1', params)
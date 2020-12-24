# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marrabld/Projects/planarradpy/libplanarradpy/state.py
# Compiled at: 2015-01-12 02:19:09
__author__ = 'marrabld'
import ConfigParser, os

class State:

    def __init__(self):
        self.debug = ''
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(os.path.dirname(__file__), 'planarradpy.conf'))
        self.debug = conf.get('Debug', 'Level')
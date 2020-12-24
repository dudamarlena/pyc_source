# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\requests\action\container.py
# Compiled at: 2019-04-18 04:31:53
# Size of source mod 2**32: 2546 bytes
import re
from collections import defaultdict, deque
from itertools import takewhile
from scrapgo.utils.shortcuts import parse_path, queryjoin
from .actions import *

class ActionContainerMixin(object):
    LINK_RELAY = None

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.LINK_RELAY = self.LINK_RELAY or []

    def get_action(self, name, many=False):
        actions = []
        for action in self.LINK_RELAY:
            if action.name == name:
                if many == False:
                    return action
                actions.append(action)

        if actions:
            return actions
        raise ValueError('Invalid name: {}'.format(name))
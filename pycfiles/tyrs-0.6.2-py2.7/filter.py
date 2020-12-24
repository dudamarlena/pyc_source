# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/filter.py
# Compiled at: 2011-07-04 17:37:11
import re, tyrs
from utils import get_urls

class FilterStatus(object):

    def __init__(self):
        self.conf = tyrs.container['conf']

    def filter_status(self, status):
        self.setup_exception()
        try:
            if self.conf.filter['activate']:
                self.status = status
                if self.filter_without_url():
                    if self.filter_without_myself():
                        if self.filter_exception():
                            return True
            return False
        except:
            return False

    def filter_without_url(self):
        urls = get_urls(self.status.text)
        if len(urls) == 0:
            return True
        return False

    def filter_without_myself(self):
        if self.conf.filter['myself']:
            return True
        else:
            if self.conf.my_nick in self.status.text:
                return False
            return True

    def filter_exception(self):
        nick = self.status.user.screen_name
        if self.conf.filter['behavior'] == 'all':
            if nick not in self.exception:
                return True
        elif nick in self.exception:
            return True
        return False

    def setup_exception(self):
        self.exception = self.conf.filter['except']
        self.exception.append(self.conf.my_nick)
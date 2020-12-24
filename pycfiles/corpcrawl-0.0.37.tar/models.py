# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/corpcrawl_env/corpcrawl/corpcrawl/models/models.py
# Compiled at: 2013-03-14 02:37:00


class Company(object):
    name = None
    location = None
    business_address = None
    mailing_address = None
    subsidiaries = []

    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

    def __str__(self):
        return 'Name: %s  mailing: %s \nsubs: %s' % (
         self.name, self.mailing_address, ('\n').join([ sub.name for sub in self.subsidiaries ]))
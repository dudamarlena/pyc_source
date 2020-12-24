# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
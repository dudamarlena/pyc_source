# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/route53/status.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1841 bytes


class Status(object):

    def __init__(self, route53connection, change_dict):
        self.route53connection = route53connection
        for key in change_dict:
            if key == 'Id':
                self.__setattr__(key.lower(), change_dict[key].replace('/change/', ''))
            else:
                self.__setattr__(key.lower(), change_dict[key])

    def update(self):
        """ Update the status of this request."""
        status = self.route53connection.get_change(self.id)['GetChangeResponse']['ChangeInfo']['Status']
        self.status = status
        return status

    def __repr__(self):
        return '<Status:%s>' % self.status
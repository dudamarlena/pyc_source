# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/errors.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 623 bytes


class FlamingoError(Exception):
    pass


class DataModelError(FlamingoError):
    pass


class MultipleObjectsReturned(DataModelError):

    def __init__(self, query, *args, **kwargs):
        self.query = query
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return 'multiple objects returned for query {}'.format(self.query)


class ObjectDoesNotExist(DataModelError):

    def __init__(self, query, *args, **kwargs):
        self.query = query
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return 'no object returned for query {}'.format(self.query)
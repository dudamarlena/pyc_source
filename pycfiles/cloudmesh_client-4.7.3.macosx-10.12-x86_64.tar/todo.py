# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/todo.py
# Compiled at: 2017-04-23 10:30:41


class TODO(object):

    @classmethod
    def implement(cls, msg='Please implement'):
        """temporary function to use to indicate that the code is not
           yet implemented"""
        raise NotImplementedError(msg)
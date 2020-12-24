# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/nova.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function

class Nova(object):

    @classmethod
    def remove_subjectAltName_warning(cls, content):
        result = []
        for line in content.split('\n'):
            if 'subjectAltName' in line:
                pass
            elif 'SubjectAltNameWarning' in line:
                pass
            else:
                result.append(line)

        return ('\n').join(result)
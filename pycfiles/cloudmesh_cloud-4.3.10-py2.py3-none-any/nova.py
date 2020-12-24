# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
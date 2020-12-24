# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/user.py
# Compiled at: 2014-12-30 09:45:44
"""
User model helper methods.
"""
from coaster.utils import md5sum

def avatar_url(user, size=None):
    if user.avatar:
        if isinstance(size, (list, tuple)):
            size = ('x').join(size)
        if size:
            return user.avatar + '?size=' + unicode(size)
        return user.avatar
    if user.email:
        if isinstance(user.email, basestring):
            hash = md5sum(user.email)
        else:
            hash = user.email.md5sum
        gravatar = '//www.gravatar.com/avatar/' + hash + '?d=mm'
        if size:
            gravatar += '&s=' + unicode(size)
        return gravatar
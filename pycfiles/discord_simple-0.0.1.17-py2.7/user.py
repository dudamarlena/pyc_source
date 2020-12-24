# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/discord_simple/models/user.py
# Compiled at: 2016-09-09 14:48:23
""" Todo """

class User:
    """ Todo """
    id = None
    discriminator = None
    avatar = None
    verified = None
    bot = None
    username = None

    def __init__(self, data):
        """ Todo """
        self.id = data.get('id', 0)
        self.username = data.get('username', '')
        self.avatar = data.get('avatar', None)
        self.discriminator = int(data.get('discriminator', 0))
        return

    def __repr__(self):
        """ Todo """
        return '<User %s#%04i>' % (self.username, self.discriminator)

    def __str__(self):
        """ Todo """
        return '%s#%04i' % (self.username, self.discriminator)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/static_boards.py
# Compiled at: 2018-09-19 16:34:26
# Size of source mod 2**32: 975 bytes
"""Defines static boards that are common to every user.

Static boards act like users' boards except that they are shared by every users
and they don't only rely on feed tags to filter articles.
"""
from django.urls import reverse
from .models import Board

class StaticBoard:
    __doc__ = 'Class that mimics the Board model interface.'
    is_static = True

    def __init__(self, pk, name, view_name):
        self.pk = pk
        self.name = name
        self.tags = list()
        self._view_name = view_name

    def get_absolute_url(self):
        return reverse('reader:' + self._view_name)


static_boards = {'all':StaticBoard('all', 'All articles', 'home'), 
 'starred':StaticBoard('starred', 'Stars', 'starred')}

def get_boards_for_user(user) -> list:
    """Retrieve all boards a user has access to: his and the static ones."""
    user_boards = Board.objects.filter(reader=(user.reader_profile))
    return list(static_boards.values()) + list(user_boards)
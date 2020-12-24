# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/context_processors.py
# Compiled at: 2010-06-14 19:51:42
from mousedb.groups.models import Group

def group_info(request):
    """This context processor provides group information to all templates."""
    group = Group.objects.get(pk=1)
    return {'group': group}
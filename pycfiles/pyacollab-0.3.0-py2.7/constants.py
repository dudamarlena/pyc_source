# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/activecollab/constants.py
# Compiled at: 2011-09-27 18:50:29
AC_COMMANDS = ('projects', 'people', 'calendar')
AC_SUBCOMMAND = ('tickets', 'discussions', 'milestones', 'files', 'pages', 'time',
                 'comment')
AC_COMMAND_ELEMENT = {'projects': 'project', 
   'people': 'company', 
   'discussions': 'topic', 
   'tickets': 'ticket', 
   'milestones': 'milestone', 
   'time': 'time_record', 
   'page': 'category', 
   'comments': 'comment', 
   'files': 'file'}
AC_BASE_FIELDS = ('id', 'name', 'permalink')
AC_SUB_FIELDS = {'tickets': ('ticket_id', )}
AC_FIELD_SEP = ': '
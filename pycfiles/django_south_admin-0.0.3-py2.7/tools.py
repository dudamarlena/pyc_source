# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/south_admin/tools.py
# Compiled at: 2012-07-10 03:57:21
from StringIO import StringIO
import sys, traceback
from django.core import management
from django.shortcuts import render_to_response
import object_tools
from south.models import MigrationHistory

class Migrate(object_tools.ObjectTool):
    name = 'migrate'
    label = 'Migrate'

    def view(self, request, extra_context=None):
        orig_stdout = sys.stdout
        sys.stdout = output = StringIO()
        try:
            management.call_command('migrate', verbosity=1)
        except:
            traceback.print_exc(file=sys.stdout)

        sys.stdout = orig_stdout
        output.seek(0)
        context = {'title': 'South Migrate Result', 
           'output': output.read(), 
           'request': request}
        return render_to_response('south_admin/migrate.html', context)


object_tools.tools.register(Migrate, MigrationHistory)
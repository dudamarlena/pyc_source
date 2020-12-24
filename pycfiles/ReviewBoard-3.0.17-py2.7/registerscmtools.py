# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/management/commands/registerscmtools.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import pkg_resources, sys
from django.core.management.base import NoArgsCommand
from reviewboard.scmtools.models import Tool

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        registered_tools = {}
        for tool in Tool.objects.all():
            registered_tools[tool.class_name] = True

        for entry in pkg_resources.iter_entry_points(b'reviewboard.scmtools'):
            try:
                scmtool_class = entry.load()
            except Exception as e:
                sys.stderr.write(b'Unable to load SCMTool %s: %s\n' % (
                 entry, e))
                continue

            class_name = b'%s.%s' % (scmtool_class.__module__,
             scmtool_class.__name__)
            if class_name not in registered_tools:
                registered_tools[class_name] = True
                name = scmtool_class.name or scmtool_class.__name__.replace(b'Tool', b'')
                self.stdout.write(b'Registering new SCM Tool %s (%s) in database' % (
                 name, class_name))
                Tool.objects.create(name=name, class_name=class_name)
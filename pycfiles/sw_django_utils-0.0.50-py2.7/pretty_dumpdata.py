# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djutils/management/commands/pretty_dumpdata.py
# Compiled at: 2016-02-28 02:57:00
from io import StringIO
from django.core.management.commands.dumpdata import Command as Dumpdata

class Command(Dumpdata):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **kwargs):
        orig_stdout = self.stdout
        self.stdout = StringIO()
        super(Command, self).handle(*args, **kwargs)
        data = self.stdout.getvalue()
        data = data.encode('utf-8').decode('unicode_escape')
        orig_stdout.write(data)
        return data
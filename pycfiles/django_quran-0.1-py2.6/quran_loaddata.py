# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/quran/management/commands/quran_loaddata.py
# Compiled at: 2009-12-05 17:10:32
from django.core.management.base import NoArgsCommand
from quran.data import *

class Command(NoArgsCommand):
    help = 'Load initial Quran data.'

    def handle_noargs(self, **options):
        if Aya.objects.count() > 0:
            print 'The quran database must be empty before running quran_loaddata. Running tests.'
            test_data(verbosity=options['verbosity'])
            return
        print '----- importing quran data (Tanzil) -----'
        import_quran()
        print '----- done importing quran data (Tanzil). starting translations -----'
        import_translations()
        print '----- done importing translations. starting morphology -----'
        import_morphology()
        print '----- done importing morphology. running tests -----'
        test_data(verbosity=options['verbosity'])
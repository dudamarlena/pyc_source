# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo89/mogo/dex/terminal/commands.py
# Compiled at: 2017-12-26 08:37:47
# Size of source mod 2**32: 1233 bytes
from term.commands import Command, rprint
from django.core.management import call_command
from django.utils.six import StringIO
from dex.export import Exporter
from django.urls.base import reverse

def replicatedb(request, cmd_args):
    ex = Exporter()
    ex.archive_replicas()
    out = StringIO()
    rprint('Migrating replica, please wait ...')
    call_command('migrate', '--database=replica', '--no-color', stdout=out)
    res = out.getvalue()
    endres = res.split('\n')
    for r in endres:
        rprint(r)

    ex.clone('default', 'replica', None)
    url = reverse('dex-dl')
    rprint('<a href="' + url + '">Download the replica</a>')


def replicatemedia(request, cmd_args):
    ex = Exporter()
    out = StringIO()
    ex.remove_media_archive()
    res = out.getvalue()
    endres = res.split('\n')
    for r in endres:
        rprint(r)

    rprint('Archiving media directory, please wait ...')
    ex.zipdir()
    rprint('[Ok] Media directory zipped')
    url = reverse('dex-media')
    rprint('<a href="' + url + '">Download the media files</a>')


c1 = Command('replicatedb', replicatedb, 'Replicate the database')
c2 = Command('getmedia', replicatemedia, 'Zip and download the media files')
COMMANDS = [
 c1, c2]
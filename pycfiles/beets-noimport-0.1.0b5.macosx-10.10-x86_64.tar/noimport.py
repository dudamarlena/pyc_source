# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/beetsplug/noimport.py
# Compiled at: 2015-05-24 19:03:35
"""
add directories to the incremental import skip list
"""
import logging, os.path
from beets import plugins, ui, importer
from beets.util import syspath, normpath, displayable_path
log = logging.getLogger('beets')

class NoImportPlugin(plugins.BeetsPlugin):

    def __init__(self):
        super(NoImportPlugin, self).__init__()
        self._command = ui.Subcommand('noimport', help='add directories to the incremental import skip list')
        self._command.parser.add_option('-r', '--reverse', action='store_true', dest='reverse', default=None, help='remove directories from the skip list')
        return

    def commands(self):

        def func(lib, opts, args):
            paths = args
            if not paths:
                raise ui.UserError('no path specified')
            self.noimport_files(lib, paths, opts)

        self._command.func = func
        return [self._command]

    def noimport_files(self, lib, paths, opts):
        for path in paths:
            if not os.path.exists(syspath(normpath(path))):
                raise ui.UserError(('no such file or directory: {0}').format(displayable_path(path)))

        state = importer._open_state()
        if 'taghistory' not in state:
            state['taghistory'] = set()
        for path in paths:
            added = 0
            for dirs, paths_in_dir in importer.albums_in_dir(path):
                dirs_tuple = tuple(map(normpath, dirs))
                if not opts.reverse:
                    if dirs_tuple not in state['taghistory']:
                        state['taghistory'].add(dirs_tuple)
                        added += 1
                elif dirs_tuple in state['taghistory']:
                    state['taghistory'].remove(dirs_tuple)
                    added += 1

        importer._save_state(state)
        if not opts.reverse:
            log.info('Added {0} paths to the skip list', added)
        else:
            log.info('Removed {0} paths from the skip list', added)
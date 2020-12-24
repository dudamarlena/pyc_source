# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/importer.py
# Compiled at: 2015-10-20 16:27:01
import logging
log = logging.getLogger('bta.importer')

def importer_for(path):

    def import_all(path=path, stop_on_error=False):
        import os, pkgutil
        folder = os.path.dirname(path)
        for importer, name, _ in pkgutil.iter_modules([folder]):
            loader = importer.find_module(name)
            try:
                loader.load_module(name)
            except ImportError as e:
                if stop_on_error:
                    raise
                log.warning('Cannot load BTA plugin [%s]. Root cause: %s' % (name, e))

    return import_all
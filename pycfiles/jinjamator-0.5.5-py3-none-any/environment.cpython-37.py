# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/environment.py
# Compiled at: 2020-04-24 07:59:04
# Size of source mod 2**32: 184 bytes
import logging
log = logging.getLogger()

def site_path():
    log.debug(self._parent._configuration._data)
    return self._parent._configuration.get('jinjamator_site_path', None)
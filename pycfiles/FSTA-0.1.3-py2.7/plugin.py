# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FSTA/plugin.py
# Compiled at: 2016-12-11 04:36:52
import time, logging

class plugin(object):
    """Plugin for FSTA
        """

    def __init__(self, file_name):
        """Initialisation
                        - file_name
                        - modified_date
                """
        self.file_name = file_name
        self.loaded_date = time.time()

    def load(self, maison):
        """Load the plugin with 'maison' as installation name
                """
        logging.info('Load the plugin %s ...' % self.file_name)
        try:
            execfile(maison.plugin_path + '/' + self.file_name, globals(), locals())
            logging.info('\tplugin loaded.')
        except Exception as e:
            logging.error('\tError on plugin %s : %s' % (self.file_name, e))
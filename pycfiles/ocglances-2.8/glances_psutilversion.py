# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_psutilversion.py
# Compiled at: 2017-02-11 10:25:25
from ocglances import psutil_version_info
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Get the psutil version for client/server purposes.

    stats is a tuple
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = None
        return

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the stats."""
        self.reset()
        if self.input_method == 'local':
            try:
                self.stats = psutil_version_info
            except NameError:
                pass

        return self.stats
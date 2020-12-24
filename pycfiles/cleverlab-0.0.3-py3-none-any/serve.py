# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/plugins/serve.py
# Compiled at: 2006-08-02 05:57:50
from harold.lib import detect_config
from paste.script.serve import ServeCommand

class ServeHarold(ServeCommand):
    __module__ = __name__
    min_args = 0
    max_args = 2
    takes_config_file = 0

    def command(self):
        if len(self.args) > 1:
            pass
        else:
            config = detect_config()
            if config:
                self.args.insert(0, config)
        app_name = self.options.app_name
        if app_name is None:
            self.options.reload = True
        ServeCommand.command(self)
        return
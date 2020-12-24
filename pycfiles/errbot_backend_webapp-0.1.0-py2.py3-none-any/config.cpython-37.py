# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/attakei/works/errbot/devel-plugins/backends/webapp/build/lib/errbot_backend_webapp/config.py
# Compiled at: 2019-06-23 09:59:46
# Size of source mod 2**32: 317 bytes


class WebappConfig(object):
    __doc__ = 'Webapp server configuration\n    '

    def __init__(self, bot_config):
        conf = getattr(bot_config, 'BOT_IDENTITY', {})
        self.host = conf.get('host', 'localhost')
        self.port = conf.get('port', 8080)
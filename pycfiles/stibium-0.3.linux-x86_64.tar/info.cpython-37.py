# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/stibium/contrib/info.py
# Compiled at: 2019-09-02 08:41:04
# Size of source mod 2**32: 2581 bytes
import os, time, datetime
from ..handlers import CommandHandler
from ..dataclasses import Message
from .. import __version__
from .._i18n import _

class InfoCommand(CommandHandler):
    __doc__ = "\n    Bot information command\n\n    This handler creates a command responding with information\n    about the bot. The command is by default called 'info',\n    but this can be changed with the `command` kwarg.\n    Sent information can be customized by the `options` kwarg.\n    Available options:\n    name stibium prefix user hostname pid uptime\n    "
    options = {'name':True, 
     'stibium':True, 
     'prefix':True, 
     'user':True, 
     'hostname':False, 
     'pid':False, 
     'uptime':True, 
     'owner':True}
    starttime = None

    def __init__(self, command='info', options=None):
        super().__init__(handler=None, command=command)
        if options is not None:
            for k, v in options.items():
                if k in self.options:
                    self.options[k] = v

    def setup(self, bot):
        super().setup(bot)
        self.starttime = time.time()

    def _get_data(self, x, bot):
        if x == 'name':
            return bot.name
        if x == 'stibium':
            return _('running Stibium v{version}').format(version=__version__)
        if x == 'prefix':
            return _('Prefix: {prefix}').format(prefix=(repr(bot.prefix)))
        if x == 'user':
            uid = bot.fbchat_client.uid
            username = bot.get_user_name(uid)
            return _('Logged in as {username} ({uid})').format(username=username, uid=uid)
        if x == 'hostname':
            return _('Server: {hostname}').format(hostname=(os.uname()[1]))
        if x == 'pid':
            return _('PID: {pid}').format(pid=(os.getpid()))
        if x == 'uptime':
            return _('Uptime: {uptime}').format(uptime=datetime.timedelta(seconds=(int(time.time() - self.starttime))))
        if x == 'owner':
            if bot.owner is None:
                return _('Owner not set!')
            return _('Owner: {username} ({uid})').format(uid=(bot.owner.id_),
              username=(bot.get_user_name(bot.owner.id_)))

    def handlerfn(self, message: Message, bot):
        response = []
        for k, v in self.options.items():
            if v:
                response.append(self._get_data(k, bot))

        message.reply('\n'.join(response))
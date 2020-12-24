# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/permissions.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 4277 bytes
__doc__ = 'This module provides the Permissions contrib class'
import types, json
from ..handlers import CommandHandler
from ..dataclasses import Thread
from .._i18n import _

class Permissions(object):
    """Permissions"""
    _db = {}
    _admin = None
    _db_file = None
    _manage_cmd = None

    def __init__(self, db_file, admin, manage_cmd='manage'):
        self._admin = Thread.from_user_uid(admin).id_
        self._db_file = db_file
        self._manage_cmd = manage_cmd
        self._load()

    def _load(self):
        with open(self._db_file) as (fd):
            self._db = json.load(fd)

    def _save(self):
        with open(self._db_file, 'w') as (fd):
            json.dump(self._db, fd)

    def block(self, group, handler=None, notify=True):
        """
        Block members of `group` from using a command.
        Can be used as a decorator, if handler=None.
        If notify is True, user blocked from using a command
        will receive a message telling them they can't use
        the command.
        """
        self._assert_group(group)
        if not notify:

            def wrapper(han):
                oldcheck = han.check

                def hook(self_, event, bot):
                    if event.uid in self._db[group]:
                        return False
                    return oldcheck(event, bot)

                setattr(han, 'check', types.MethodType(hook, han))
                return han

        else:

            def wrapper(han):
                oldexec = han.execute

                def hook(self_, event, bot):
                    if event.uid in self._db[group]:
                        event.reply(_("You can't use this command."))
                        return
                    return oldexec(event, bot)

                setattr(han, 'execute', types.MethodType(hook, han))
                return han

        if handler:
            return wrapper(handler)
        return wrapper

    def _assert_group(self, group):
        if group not in self._db:
            self._db[group] = []
            self._save()

    def _manage(self, message, bot):
        if message.uid != self._admin:
            message.reply(_("You can't use this command."))
            return
            args = message.args.split()
            if len(args) != 3:
                message.reply(_('Not enough arguments.\n{prefix}{cmd} [add|ban|remove|unban] <group> [reply|<uid>]').format(prefix=(bot.prefix),
                  cmd=(self._manage_cmd)))
                return
        else:
            if args[2] == 'reply':
                uid = message.replied_to.uid
            else:
                uid = args[2]
            self._assert_group(args[1])
            if args[0] in ('add', 'ban'):
                self._db[args[1]].append(uid)
                message.reply(_('Added {uid} to group {group!r}').format(uid=uid, group=(args[1])))
            elif args[0] in ('remove', 'unban'):
                if uid in self._db[args[1]]:
                    self._db[args[1]].remove(uid)
                    message.reply(_('Removed {uid} from group {group!r}').format(uid=uid, group=(args[1])))
                else:
                    message.reply(_('User {uid} was not in group.').format(uid=uid))
            else:
                message.reply(_('Unknown subcommand'))
        self._save()

    def handler(self):
        """Returns a handler which needs to be registered"""
        return CommandHandler(self._manage, self._manage_cmd)
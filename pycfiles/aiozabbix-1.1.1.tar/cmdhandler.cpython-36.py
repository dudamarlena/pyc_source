# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\cmdhandler.py
# Compiled at: 2017-03-02 21:01:17
# Size of source mod 2**32: 7190 bytes
import inspect, logging, traceback
from .oyoyo.parse import parse_nick
from .oyoyo.cmdhandler import CommandError, NoSuchCommandError, ProtectedCommandError, IRCClientError
from . import helpers

def protected(func):
    """Decorator to protect functions from being called as commands"""
    func.protected = True
    return func


class CommandHandler(object):
    """CommandHandler"""

    def __init__(self, client):
        self.client = client

    @protected
    def get(self, in_command_parts):
        """Finds a command
        commands may be dotted. each command part is checked that it does
        not start with and underscore and does not have an attribute
        "protected". if either of these is true, ProtectedCommandError
        is raised.
        its possible to pass both "command.sub.func" and
        ["command", "sub", "func"].
        """
        if isinstance(in_command_parts, bytes):
            in_command_parts = in_command_parts.split('.'.encode())
        else:
            if isinstance(in_command_parts, str):
                in_command_parts = in_command_parts.split('.')
        command_parts = in_command_parts[:]
        p = self
        while command_parts:
            cmd = command_parts.pop(0)
            if type(cmd) is bytes:
                cmd = cmd.decode()
            if cmd.startswith('_'):
                raise ProtectedCommandError(in_command_parts)
            try:
                f = getattr(p, cmd)
            except AttributeError:
                raise NoSuchCommandError(in_command_parts)

            if hasattr(f, 'protected'):
                raise ProtectedCommandError(in_command_parts)
            if isinstance(f, CommandHandler):
                if command_parts:
                    return f.get(command_parts)
            p = f

        return f

    @protected
    async def run(self, command, *args):
        """Finds and runs a command"""
        logging.debug('processCommand %s(%s)' % (command, args))
        logging.info('processCommand %s(%s)' % (command, args))
        try:
            f = self.get(command)
        except NoSuchCommandError:
            (self.__unhandled__)(command, *args)
            return
        else:
            logging.debug('f %s' % f)
            try:
                await f(self.client, *args)
            except Exception as e:
                logging.error('command raised %s' % e)
                logging.error(traceback.format_exc())
                raise CommandError(command)

    @protected
    def __unhandled__(self, cmd, *args):
        """The default handler for commands. Override this method to
        apply custom behavior (example, printing) unhandled commands.
        """
        logging.debug('unhandled command %s(%s)' % (cmd, args))


class DefaultCommandHandler(CommandHandler):
    """DefaultCommandHandler"""

    async def ping(self, prefix, server):
        """Called on PING command, sends back PONG"""
        self.client.send('PONG', server)


class DefaultBotCommandHandler(CommandHandler):
    """DefaultBotCommandHandler"""

    @protected
    def getVisibleCommands(self, obj=None):
        """Gets all visible commands, protected"""
        test = lambda x: isinstance(x, CommandHandler) or inspect.ismethod(x) or inspect.isfunction(x)
        members = inspect.getmembers(obj or self, test)
        return [m for m, _ in members if not m.startswith('_') if not hasattr(getattr(obj, m), 'protected')]

    async def help(self, sender, dest, arg=None):
        """List all available commands or get help on a specific command"""
        logging.info('help sender=%s dest=%s arg=%s' % (sender, dest, arg))
        if not arg:
            commands = self.getVisibleCommands()
            commands.sort()
            await helpers.msg(self.client, dest, 'available commands: %s' % ' '.join(commands))
        else:
            try:
                f = self.get(arg)
            except CommandError as e:
                await helpers.msg(self.client, dest, str(e))
                return

            doc = f.__doc__.strip() if f.__doc__ else 'No help available'
            if not inspect.ismethod(f):
                subcommands = self.getVisibleCommands(f)
                if subcommands:
                    doc += ' [sub commands: %s]' % ' '.join(subcommands)
            await helpers.msg(self.client, dest, '%s: %s' % (arg, doc))


class BotCommandHandler(DefaultCommandHandler):
    """BotCommandHandler"""

    def __init__(self, client, command_handler):
        DefaultCommandHandler.__init__(self, client)
        self.command_handler = command_handler

    async def privmsg(self, prefix, dest, msg):
        """Called when privmsg command is received, just awaits
        BotCommandHandler.tryBotCommand with the same args"""
        await self.tryBotCommand(prefix, dest, msg)

    @protected
    async def tryBotCommand(self, prefix, dest, msg):
        """Tests a command to see if its a command for the bot, returns True
        and calls self.processBotCommand(cmd, sender) if its is.
        """
        logging.debug("tryBotCommand('%s' '%s' '%s')" % (prefix, dest, msg))
        if dest == self.client.nick:
            dest = parse_nick(prefix)[0]
        else:
            if msg.startswith(self.client.nick):
                msg = msg[len(self.client.nick) + 1:]
            else:
                return False
        msg = msg.strip()
        parts = msg.split(' ', 1)
        command = parts[0]
        arg = parts[1:]
        try:
            await (self.command_handler.run)(command, prefix, dest, *arg)
        except CommandError as e:
            await helpers.msg(self.client, dest, str(e))

        return True
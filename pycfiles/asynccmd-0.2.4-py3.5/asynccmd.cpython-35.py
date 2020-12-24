# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asynccmd/asynccmd.py
# Compiled at: 2017-01-02 10:39:03
# Size of source mod 2**32: 5883 bytes
import asyncio, string, sys
from contextlib import suppress

class Cmd:
    __doc__ = '\n    TODO: need documentation\n    TODO: need to review\n    TODO: need to refactor in doc like ->\n    TODO: need to refactor protected methods\n    Reader not supported in Win32\n\n    '
    loop = None
    mode = 'Reader'
    run_loop = False
    prompt = 'asynccmd > '
    intro = 'asynccmd ready to serve'
    currentcmd = ''
    lastcmd = ''
    allowedchars = string.ascii_letters + string.digits + '_'
    stdin = sys.stdin
    stdout = sys.stdout

    @staticmethod
    def do_test(arg):
        print('Called buildin function do_test with args:', arg)

    def do_help(self, arg):
        print('Default help handler. Have arg :', arg, ', but ignore its.')
        print('Available command list: ')
        for i in dir(self.__class__):
            if i.startswith('do_'):
                print(' - ', i[3:])

    def do_exit(self, arg):
        print('Rescue exit!!')
        raise KeyboardInterrupt

    def __init__(self, mode='Reader', run_loop=False):
        self.mode = mode
        self.run_loop = run_loop

    def cmdloop(self, loop=None):
        self._start_controller(loop)

    def _start_controller(self, loop):
        """
        Control structure to start new cmd
        :param loop: event loop
        :return: None
        """
        if loop is None:
            if sys.platform == 'win32':
                self.loop = asyncio.ProactorEventLoop()
            else:
                self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        if self.mode == 'Reader':
            self._start_reader()
        else:
            if self.mode == 'Run':
                self._start_run()
            else:
                raise TypeError('self.mode is not Reader or Run.')
        if self.run_loop:
            try:
                print('Cmd._start_controller start loop inside Cmd object!')
                self.stdout.flush()
                self.loop.run_forever()
            except KeyboardInterrupt:
                print('Cmd._start_controller stop loop. Bye.')
                self.loop.stop()
                pending = asyncio.Task.all_tasks(loop=self.loop)
                print(asyncio.Task.all_tasks(loop=self.loop))
                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        self.loop.run_until_complete(task)

    def _start_run(self):
        if self.loop is None:
            raise TypeError('self.loop is None.')
        self.loop.create_task(self._read_line())
        self.loop.create_task(self._greeting())

    def _start_reader(self):
        if self.loop is None:
            raise TypeError('self.loop is None.')
        self.loop.add_reader(self.stdin.fileno(), self.reader)
        self.loop.create_task(self._greeting())

    def reader(self):
        line = sys.stdin.readline()
        self._exec_cmd(line)
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

    async def _read_line(self):
        while True:
            line = await self.loop.run_in_executor(None, sys.stdin.readline)
            self._exec_cmd(line)
            print(self.prompt)
            sys.stdout.flush()

    def _exec_cmd(self, line):
        command, arg, line = self.parseline(line=line)
        if not line:
            return self._emptyline(line)
        else:
            if command is None:
                return self._default(line)
            else:
                self.lastcmd = line
                if line == 'EOF':
                    self.lastcmd = ''
                if command == '':
                    pass
                return self._default(line)
            try:
                func = getattr(self, 'do_' + command)
            except AttributeError:
                return self._default(line)
            except KeyboardInterrupt:
                return func(arg)

            return func(arg)

    def parseline(self, line):
        line = line.strip()
        if not line:
            return (None, None, line)
        if line[0] == '?':
            line = 'help ' + line[1:]
        else:
            if line[0] == '!':
                if hasattr(self, 'do_shell'):
                    line = 'shell ' + line[1:]
            else:
                return (
                 None, None, line)
        iline, nline = 0, len(line)
        while iline < nline and line[iline] in self.allowedchars:
            iline += 1

        command = line[:iline]
        arg = line[iline:].strip()
        return (command, arg, line)

    @staticmethod
    def _default(line):
        print('Invalid command: ', line)

    async def _greeting(self):
        print(self.intro)
        self.stdout.write(self.prompt)
        self.stdout.flush()

    def _emptyline(self, line):
        """
        handler for empty line if entered.
        :param line: this is unused arg (TODO: remove)
        :return: None
        """
        if self.lastcmd:
            print('Empty line. Try to repeat last command.', line)
            self._exec_cmd(self.lastcmd)
            return
        else:
            print('Empty line. Nothing happen.', line)
            return
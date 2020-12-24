# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/PyCommand.py
# Compiled at: 2017-04-23 10:30:41
from code import InteractiveConsole
import sys
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, CometPluginCommand

class EmbeddedConsoleExit(SystemExit):
    pass


class Statekeeper(object):

    def __init__(self, obj, attribs):
        self.obj = obj
        self.attribs = attribs
        if self.obj:
            self.save()

    def save(self):
        for attrib in self.attribs:
            setattr(self, attrib, getattr(self.obj, attrib))

    def restore(self):
        if self.obj:
            for attrib in self.attribs:
                setattr(self.obj, attrib, getattr(self, attrib))


class PyCommand(PluginCommand, ShellPluginCommand, CometPluginCommand):
    pystate = {}
    locals_in_py = True
    topics = {'open': 'shell'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print 'init command browser'
        self.locals_in_py = True
        self.pystate['self'] = self

    def do_py(self, arg):
        """
        ::

            Usage:
                py
                py COMMAND

            Arguments:
                COMMAND   the command to be executed

            Description:

                The command without a parameter will be executed and the
                interactive python mode is entered. The python mode can be
                ended with ``Ctrl-D`` (Unix) / ``Ctrl-Z`` (Windows),
                ``quit()``,'`exit()``. Non-python commands can be issued with
                ``cmd("your command")``.  If the python code is located in an
                external file it can be run with ``run("filename.py")``.

                In case a COMMAND is provided it will be executed and the
                python interpreter will return to the command shell.

                This code is copied from Cmd2.
        """
        self.pystate['self'] = self
        arg = arg.strip()
        localvars = self.locals_in_py and self.pystate or {}
        interp = InteractiveConsole(locals=localvars)
        interp.runcode('import sys, os;sys.path.insert(0, os.getcwd())')
        if arg:
            interp.runcode(arg)
        else:

            def quit():
                raise EmbeddedConsoleExit

            def onecmd(arg):
                return self.onecmd(arg + '\n')

            def run(arg):
                try:
                    f = open(arg)
                    interp.runcode(f.read())
                    f.close()
                except IOError as e:
                    self.perror(e)

            self.pystate['quit'] = quit
            self.pystate['exit'] = quit
            self.pystate['cmd'] = onecmd
            self.pystate['run'] = run
            try:
                cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
                keepstate = Statekeeper(sys, ('stdin', 'stdout'))
                sys.stdout = self.stdout
                sys.stdin = self.stdin
                interp.interact(banner='Python %s on %s\n%s\n(%s)\n%s' % (
                 sys.version, sys.platform, cprt, self.__class__.__name__, self.do_py.__doc__))
            except EmbeddedConsoleExit:
                pass

            keepstate.restore()
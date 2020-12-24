# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/shell/fgShellUtils.py
# Compiled at: 2012-09-06 11:03:15
"""
FutureGrid Command Line Interface

Some code has been taken from Cyberade CoG kit shell (http://cogkit.svn.sourceforge.net/viewvc/cogkit/trunk)
"""
__author__ = 'Javier Diaz'
import os, readline, atexit, sys, textwrap
from cmd2 import Cmd
import pkgutil, string

class fgShellUtils(Cmd):

    def __init__(self):
        """initialize the fgshellutils"""
        self._script = False
        self._scriptList = []
        self._scriptFile = self._conf.getScriptFile()

    def getArgs(self, args):
        """Convert the string args to a list of arguments."""
        aux = args.strip()
        argsList = []
        if aux != '':
            values = aux.split(' ')
            for i in values:
                istriped = i.strip()
                if istriped != '':
                    argsList.append(istriped)

        return argsList

    def do_script(self, arg):
        """executs the script"""
        args = self.getArgs(arg)
        if not self._script:
            self._scriptList = []
            if len(args) == 0:
                if not os.path.isfile(self._scriptFile):
                    print 'Script module activated'
                    self._script = True
                else:
                    print 'File ' + self._scriptFile + ' exists. Use argument force to overwrite it'
            elif len(args) == 1:
                if args[0] == 'end':
                    print 'Script is not active.'
                elif args[0] == 'force':
                    print 'Script module activated '
                    self._script = True
                else:
                    print 'Script module activated'
                    self._scriptFile = os.path.expanduser(args[0])
                    if not os.path.isfile(self._scriptFile):
                        self._script = True
                    else:
                        print 'File ' + self._scriptFile + ' exists. Use argument force to overwrite it'
            elif len(args) == 2:
                if args[0] == 'force':
                    print 'Script module activated'
                    self._scriptFile = os.path.expanduser(args[1])
                    self._script = True
                if args[1] == 'force':
                    print 'Script module activated'
                    self._scriptFile = os.path.expanduser(args[0])
                    self._script = True
            else:
                self.help_script()
        elif len(args) == 1:
            if args[0] == 'end':
                print 'Ending Script module and storing...'
                self._script = False
                with open(self._scriptFile, 'w') as (f):
                    for line in self._scriptList:
                        f.write(line + '\n')

            else:
                print 'Script is activated. To finish it use: script end'
        else:
            print 'Script is activated. To finish it use: script end'

    def help_script(self):
        """help message for the script"""
        message = ' When Script is active, all commands executed are stored ' + 'in a file. Activate it by executing: script [file]. If no argument is ' + "provided, the file will be called 'script' and will be located in your " + 'current directory. To finish and store the commands use: script end'
        self.print_man('script [file]', message)

    def print_man(self, name, msg):
        """print the manual"""
        print '\n'
        print '----------------------------------------------------------------------'
        print '%s' % name
        print '----------------------------------------------------------------------'
        man_lines = textwrap.wrap(textwrap.dedent(msg), 64)
        for line in man_lines:
            print '    %s' % line

        print ''

    def do_manual(self, args):
        """print all manual pages"""
        print '######################################################################'
        print 'Generic commands (available in any context)\n'
        print '######################################################################'
        for i in self._docHelp:
            try:
                func = getattr(self, 'help_' + i)
                func()
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + i).__doc__
                    if doc:
                        print '----------------------------------------------------------------------'
                        print '%s' % i
                        print '----------------------------------------------------------------------'
                        self.stdout.write('%s\n' % str(doc))
                        print ''
                except AttributeError:
                    pass

        for cntxt in self.env:
            if cntxt.strip() != '':
                bold = '\x1b[1m'
                reset = '\x1b[0;0m'
                print '######################################################################'
                print '\nSpecific Commands for the context: ' + bold + cntxt + reset
                print '######################################################################'
                self.getDocUndoc(cntxt)
                for i in self._specdocHelp:
                    if i.strip().startswith(cntxt):
                        i = i[len(cntxt):]
                    try:
                        func = getattr(self, 'help_' + cntxt + i)
                        func()
                    except AttributeError:
                        try:
                            doc = getattr(self, 'do_' + cntxt + i).__doc__
                            if doc:
                                print '----------------------------------------------------------------------'
                                print '%s' % i
                                print '----------------------------------------------------------------------'
                                self.stdout.write('%s\n' % str(doc))
                        except AttributeError:
                            pass
                        except:
                            print 'General exception: ' + str(sys.exc_info())

                    except SystemExit:
                        pass
                    except:
                        print 'General exception: ' + str(sys.exc_info())

    def generic_error(self):
        """print the generic error"""
        print '    Please select a CONTEXT by executing use <context_name>.\n' + "    Execute 'contexts' command to see the available context names. \n" + '    Help information is also different depending on the context. \n' + '    Note that this command may not be available in all CONTEXTS.'

    def generic_help(self):
        """help message for the generic command"""
        msg = 'Generic command that changes its behaviour depending on the CONTEXT. '
        for line in textwrap.wrap(msg, 64):
            print '    %s' % line

        print ''
        self.generic_error()

    def do_get(self, args):
        """TODO: get"""
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'get("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no get method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_get = generic_help

    def do_modify(self, args):
        """TODO: modify"""
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'modify("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no modify method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_modify = generic_help

    def do_setpermission(self, args):
        """set permissions"""
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'setpermission("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no setpermission method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_setpermission = generic_help

    def do_put(self, args):
        """TODO: put"""
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'put("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no put method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_put = generic_help

    def do_remove(self, args):
        """TODO: remove"""
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'remove("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no remove method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_remove = generic_help

    def do_list(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'list("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no list method in any of the active contexts (' + str(self._requirements)
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_list = generic_help

    def do_user(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'user("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no user method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_user = generic_help

    def do_histimg(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'histimg("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no histimg method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_histimg = generic_help

    def do_histuser(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'histuser("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no histuser method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_histuser = generic_help

    def do_move(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'move("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no move method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_move = generic_help

    def do_group(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'group("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no group method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_group = generic_help

    def do_register(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'register("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no register method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_register = generic_help

    def do_deregister(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'deregister("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no deregister method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_register = generic_help

    def do_generate(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'generate("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no generate method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_generate = generic_help

    def do_launch(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                print prefix
                command = 'self.do_' + prefix + 'launch("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    print str(sys.exc_info())

            if not found:
                print 'There is no launch method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_launch = generic_help

    def do_launchhadoop(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                print prefix
                command = 'self.do_' + prefix + 'launchhadoop("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    print str(sys.exc_info())

            if not found:
                print 'There is no launchhadoop method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_launchhadoop = generic_help

    def do_hpclist(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'hpclist("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no hpclist method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_hpclist = generic_help

    def do_hpclistkernels(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'hpclistkernels("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no hpclistkernels method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_hpclistkernels = generic_help

    def do_cloudlist(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'cloudlist("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no cloudlist method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_cloudlist = generic_help

    def do_cloudlistkernels(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'cloudlistkernels("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no cloudlistkernels method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_cloudlistkernels = generic_help

    def do_listsites(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'listsites("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no listsites method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_cloudlistkernels = generic_help

    def do_cloudinstancesterminate(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'cloudinstancesterminate("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no cloudinstancesterminate method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_terminatecloudinstances = generic_help

    def do_hpcjobsterminate(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'hpcjobsterminate("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no hpcjobsterminate method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_terminatehpcjobs = generic_help

    def do_cloudinstanceslist(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'cloudinstanceslist("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no cloudinstanceslist method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_listcloudinstances = generic_help

    def do_hpcjobslist(self, args):
        if self._use != '':
            found = False
            for i in self._requirements:
                prefix = string.lower(i)
                command = 'self.do_' + prefix + 'hpcjobslist("' + args + '")'
                try:
                    eval(command)
                    found = True
                    break
                except AttributeError:
                    pass

            if not found:
                print 'There is no hpcjobslist method in any of the active contexts (' + str(self._requirements) + ' )'
                self._log.error(str(sys.exc_info()))
        else:
            self.generic_error()

    help_listhpcjobs = generic_help

    def do_exec(self, script_file):
        """execute the script"""
        if script_file.strip() == '':
            self.help_exec()
            return
        if os.path.exists(script_file):
            with open(script_file, 'r') as (f):
                for line in f:
                    print '>', line
                    self.onecmd(line)

    def help_exec(self):
        msg = 'Runs the specified script file. Lines from the script file are ' + "printed out with a '>' preceding them, for clarity."
        self.print_man('exec <script_file>', msg)

    def loadhist(self, arguments):
        """Load history from the $HOME/.fg/hist.txt file
        """
        histfile = self._conf.getHistFile()
        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)

    def loadBanner(self):
        """Load banner from a file"""
        banner = pkgutil.get_data('futuregrid.shell', 'banner.txt') + '\nWelcome to the FutureGrid Shell\n' + '-------------------------------\n'
        return banner
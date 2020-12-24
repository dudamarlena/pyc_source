# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/tools/dev_environment.py
# Compiled at: 2011-01-13 01:48:00
import time
try:
    import IPython, __builtin__

    class IPyShell(IPython.iplib.InteractiveShell):

        def interact(self, banner=None):
            """Closely emulate the interactive Python console.

            The optional banner argument specify the banner to print
            before the first interaction; by default it prints a banner
            similar to the one printed by the real Python interpreter,
            followed by the current class name in parentheses (so as not
            to confuse this with the real interpreter -- since it's so
            close!).

            """
            cprt = 'Type "copyright", "credits" or "license" for more information.'
            if banner is None:
                self.write('Python %s on %s\n%s\n(%s)\n' % (
                 sys.version, sys.platform, cprt,
                 self.__class__.__name__))
            else:
                self.write(banner)
            more = 0
            __builtin__.__dict__['__IPYTHON__active'] += 1
            self.exit_now = False
            while not self.exit_now:
                if more:
                    prompt = self.outputcache.prompt2
                    if self.autoindent:
                        self.readline_startup_hook(self.pre_readline)
                else:
                    prompt = self.outputcache.prompt1
                try:
                    line = self.raw_input(prompt, more)
                    if self.autoindent:
                        self.readline_startup_hook(None)
                except KeyboardInterrupt:
                    self.write('\nKeyboardInterrupt\n')
                    self.resetbuffer()
                    self.outputcache.prompt_count -= 1
                    if self.autoindent:
                        self.indent_current_nsp = 0
                    more = 0
                except EOFError:
                    if self.autoindent:
                        self.readline_startup_hook(None)
                    self.write('\n')
                    while self.httpd_thread.isAlive():
                        self.httpd.stop()

                    self.exit()
                except bdb.BdbQuit:
                    warn('The Python debugger has exited with a BdbQuit exception.\nBecause of how pdb handles the stack, it is impossible\nfor IPython to properly format this particular exception.\nIPython will resume normal operation.')
                except:
                    self.showtraceback()
                else:
                    more = self.push(line)
                    if self.SyntaxTB.last_syntax_error and self.rc.autoedit_syntax:
                        self.edit_syntax_error()

            __builtin__.__dict__['__IPYTHON__active'] -= 1
            return


except:
    import code

def make_shell():
    import run_server
    (HTTPD, HTTPD_THREAD, loggers) = run_server.main()
    import browser_tools, server_tools
    browser = browser_tools.setup_browser()
    print 'browser should be coming up'
    try:
        import IPython
        shell = IPython.Shell.IPShell(user_ns=locals(), shell_class=IPyShell)
        shell.mainloop()
    except:
        import code
        code.interact(local=locals())
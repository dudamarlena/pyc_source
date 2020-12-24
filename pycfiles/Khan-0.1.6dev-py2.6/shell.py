# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/scripts/shell.py
# Compiled at: 2010-05-12 10:25:54
"""
本命令修改自 Pylons <http://www.pylonshq.com>_
"""
import sys, code
from khan.command import ProjectCommand

class ShellCommand(ProjectCommand):
    """
    Open an interactive shell with the khan.deploy based app loaded

    This allows you to test your Khan app, models, and simulate web requests
    using ``webtest.TestApp``.

    Example1::

        $ paster khan.shell -p myproject
    
    Example2::

        $ paster khan.shell -z myproject.zcml
    """
    parser = ProjectCommand.standard_parser(simulate=True)
    parser.add_option('-d', '--disable-ipython', action='store_true', dest='disable_ipython', help="Don't use IPython if it is available")

    def execute(self, app, deploy_context):
        locs = dict(__name__='KhanShell')
        if self.package:
            banner = '  All objects from `%s` are available\n\n' % self.package.__name__
            banner += '  Additional Objects:\n'
            locs.update(self.get_symbal_from_package(self.package))
        else:
            banner = '  Additional Objects available in shell :\n'
        banner += '  * %-10s -  %s\n' % ('wsgiapp', 'WSGI App instance')
        banner += '  * %-10s -  %s\n' % ('app', 'paste.fixture.TestApp wrapped around wsgiapp')
        banner += '  * %-10s -  %s\n' % ('context', 'khan.deploy context')
        locs.update(dict(wsgiapp=app.app, app=app, context=deploy_context))
        try:
            if self.options.disable_ipython:
                raise ImportError()
            newbanner = 'Khan Interactive Shell\n\n'
            banner = newbanner + banner
            import bpython
            bpython.embed(locals_=locs, args=self.args, banner=banner)
        except ImportError:
            py_prefix = sys.platform.startswith('java') and 'J' or 'P'
            newbanner = 'Khan Interactive Shell\n%sython %s\n\n' % (py_prefix, sys.version)
            banner = newbanner + banner
            shell = code.InteractiveConsole(locals=locs)
            try:
                import readline
            except ImportError:
                pass
            else:
                shell.interact(banner)

    def get_symbal_from_package(self, package):
        locs = {}
        base_public = [ __name for __name in dir(package) if not __name.startswith('_') or __name == '_' ]
        for name in base_public:
            locs[name] = getattr(package, name)

        return locs
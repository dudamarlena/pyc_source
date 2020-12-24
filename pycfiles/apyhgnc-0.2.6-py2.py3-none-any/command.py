# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/command.py
# Compiled at: 2007-12-05 07:14:05
__doc__ = "\n    Apydia command line tool (and distutils command)\n    ------------------------------------------------\n    \n    Use the ``apydia`` command to generate API reference documentation:\n    \n        Usage: apydia [options] [modules]\n\n        Apydia API Documentation Generator\n\n        Options:\n          --version             show program's version number and exit\n          -h, --help            show this help message and exit\n          -c CONFIGFILE, --config=CONFIGFILE\n                                specify config file\n          -d DESTINATION, --destination=DESTINATION\n                                specify output directory\n          -o, --open            open in browser\n          -f FORMAT, --format=FORMAT\n                                rendering format (xhtml or html, defaults to xhtml)\n          -s THEME, --style=THEME\n                                Choose a theme\n          -p DOCFORMAT, --parser=DOCFORMAT\n                                docstring parser (markdown, textile, restucturedtext,\n                                html, ...)\n          -b TRAC_BROWSER_URL, --trac-browser-url=TRAC_BROWSER_URL\n                                trac browser url (path to root module)\n          -q, --quiet           silent mode\n          -t TITLE, --title=TITLE\n                                title of project\n          -x EXCLUDE_MODULES, --exclude-modules=EXCLUDE_MODULES\n                                exclude modules\n\n    \n    Or run it through distutils by configuring your project's setup.cfg\n    appropriately (see documentation) and issuing from your project root:\n        \n        python setup.py apydia\n"
import logging, sys, os
from optparse import OptionParser
from apydia import release
from apydia.project import Project
import warnings
log = logging.getLogger(__name__)
__all__ = [
 'main', 'apydia']
try:
    import distutils.cmd

    class apydia(distutils.cmd.Command):
        """
            ``apydia`` command
            ==================
            
            The ``apydia``-command as an extension to distutils.
            
            Run by typing
                
                python setup.py apydia
            
            
            Availlable options are:

                --title (-t)             The name of your project
                --destination (-d)       Target directory where the apidocs go
                --theme (-t)             Choose an Apydia theme
                --docformat              Set this to the docstring's format (eg. markdown,
                                       textile, reStrucuturedText)
                --format (-f)            XHTML or HTML, defaults to xhtml
                --modules                Include the given modules in documentation
                --exclude-modules (-x)   Don't generate documentation for the given modules
                --trac-browser-url (-b)  URL to Trac's sourcecode browser
                --open (-o)              Open generated files in browser when done
            
            
            It is recommended to supply options through an
            ``[apydia]``-section in the target project's ``setup.cfg``.
            See the documentation of the ``apydia.command`` module for
            more information.
        """
        __module__ = __name__
        description = 'Generate API Reference Documentations using Apydia'
        user_options = [
         ('title=', 't', 'The name of your project'), ('destination=', 'd', 'Target directory where the apidocs go'), ('theme=', 't', 'Choose an Apydia theme'), ('docformat=', None, "Set this to the docstring's format (eg. markdown, textile, reStrucuturedText)"), ('format=', 'f', 'XHTML or HTML, defaults to xhtml'), ('modules=', None, 'Include the given modules in documentation'), ('exclude-modules=', 'x', "Don't generate documentation for the given modules"), ('trac-browser-url=', 'b', "URL to Trac's sourcecode browser"), ('open', 'o', 'Open generated files in browser when done')]

        def initialize_options(self):
            self.title = ''
            self.destination = 'apydocs'
            self.theme = 'default'
            self.docformat = ''
            self.format = 'xhtml'
            self.modules = []
            self.exclude_modules = []
            self.trac_browser_url = ''
            self.open = False

        def finalize_options(self):
            self.ensure_string_list('modules')
            self.ensure_string_list('exclude_modules')
            self.ensure_string('title')
            self.ensure_string('theme')
            self.ensure_string('trac_browser_url')

        def run(self):

            def generate():
                project = Project(self)
                project.generate()
                if self.open and str(self.open).lower() in ('1', 'true', 'yes'):
                    project.open_in_browser()

            self.execute(generate, (), msg='Generating API reference documentation.')


except ImportError:
    warnings.warn('distutils not installed.')

def main():
    """
        Generate api reference documentation from the command line
        
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua.
        
            #!python
            class CodeExample(object):
                def __init__(self):
                    pass
        
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
        culpa qui officia deserunt mollit anim id est laborum.
    """
    sys.path.insert(0, os.getcwd())
    optparser = OptionParser(usage='%prog [options] [modules]', description=release.description, version=release.version)
    optparser.set_defaults(title='', destination='apydocs', theme='default', verbose=True, open=False, format='xhtml', docformat='restructuredtext', modules='', exclude_modules='', trac_browser_url='')
    optparser.add_option('-c', '--config', dest='configfile', help='specify config file')
    optparser.add_option('-d', '--destination', dest='destination', help='specify output directory')
    optparser.add_option('-o', '--open', dest='open', action='store_true', help='open in browser')
    optparser.add_option('-f', '--format', dest='format', help='rendering format (xhtml or html, defaults to xhtml)')
    optparser.add_option('-s', '--style', dest='theme', help='Choose a theme')
    optparser.add_option('-p', '--parser', dest='docformat', help='docstring parser (markdown, textile, restucturedtext, html, ...)')
    optparser.add_option('-b', '--trac-browser-url', dest='trac_browser_url', help='trac browser url (path to root module)')
    optparser.add_option('-q', '--quiet', action='store_false', dest='verbose', help='silent mode')
    optparser.add_option('-t', '--title', dest='title', help='title of project')
    optparser.add_option('-x', '--exclude-modules', dest='exclude_modules', help='exclude modules')
    (options, args) = optparser.parse_args()
    if options.configfile:
        from ConfigParser import ConfigParser
        cfgparser = ConfigParser()
        cfgparser.read(options.configfile)
        cfgopts = dict(cfgparser.items('apydia'))
        optparser.set_defaults(**cfgopts)
    (options, args) = optparser.parse_args()
    try:
        options.modules = [ m.strip() for m in options.modules.split(',') if m.strip() ] + args
    except AttributeError:
        optparser.print_help()
        return

    options.exclude_modules = [ m.strip() for m in options.exclude_modules.split(',') if m.strip() ]
    logger_settings = dict(format='%(asctime)s %(levelname)-8s %(message)s')
    if options.verbose:
        logger_settings['level'] = logging.DEBUG
    logging.basicConfig(**logger_settings)
    project = Project(options)
    project.generate()
    if options.open:
        project.open_in_browser()


if __name__ == '__main__':
    main()
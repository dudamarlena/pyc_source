# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/cli.py
# Compiled at: 2006-03-14 16:35:23
"""Command line interface."""
usage = '\nGenerate documentation for Python projects.\n\nOPTIONS:\n\n  -d, --dest=DIR     Directory where documentation should be generated.\n  -i, --documents=FILE...\n                     Comma seperated list of files\n  -c, --title=TEXT   The title of the documentation set. This is used in\n                     various places in generated documentation and defaults\n                     to "Module Reference". If you include a document named\n                     "index", the title from that document is used.\n  -f, --force        Force creation of documentation files even if source\n                     files are older or the same age.\n      --license=NAME Include a standard license document. Current options\n                     are "gnu" for the GNU Free Documentation License and\n                     "cc" for a Creative Commons Attribution, NonCommercial,\n                     Copyleft license.\n  -x, --xhtml        Generate XHTML 1.0 instead of HTML 4.01.\n                     HTML 4.01 is the default due to browser compatibility\n                     issues with XHTML 1.0.\n  -e, --ext=TEXT     The file extension to use when writing (X)HTML files.\n                     The default is \'.html\'\n      --stages=LIST  Specify the list of stages that should be performed.\n                     This allows only portions of the generation to take\n                     place. Available stages are: copy, docs, reference,\n                     index, and source.\n  -t, --templates=.. The directory where we should look for templates. See\n                     the \'pudge.templates\' package directory for the default\n                     template set.\n      --theme=NAME   The name of a built-in theme (overrides --templates).\n      --trac=URL     Adds navigational links to a Trac site.\n      \n  -v, --verbose      Verbose output.\n  -q, --quiet        Shutup unless something important happens.\n  -h, --help         print this help screen.\n\nExamples:\n\nGenerate documentation for \'foo\' to current directory:\n\n  $ pudge -m foo\n\nGenerate documentation for \'foo\' module/package and two documents to \'build/doc\':\n\n  $ pudge --modules=foo --documents=docs/guide.rst,docs/reference.rst           --dest=build/doc\n\nGenerate documentation for the \'foo\' module/package and license the work\nunder the GNU Free Documentation License:\n\n  $ pudge --license=gnu --modules=foo\n\nPudge is Copyright (c) 2005 by Ryan Tomayko <http://naeblis.cx/rtomayko/>\n'
import sys, getopt, logging, pudge, pudge.generator

def main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    pudge.log.addHandler(handler)
    pudge.log.setLevel(logging.INFO)
    command = PudgeCommand()
    command.process_command()


class PudgeCommand:
    """Handles command line invocation."""
    __module__ = __name__

    def __init__(self, command=None, args=[]):
        self.command = command or sys.argv[0]
        self.args = args or sys.argv[1:]

    def usage(self, msg=None, exit_with=None):
        if msg:
            print msg
            print '  try: %s --help' % (self.command,)
        else:
            print 'usage: %s [OPTIONS]' % (self.command,)
            print usage.strip()
        if exit_with is not None:
            sys.exit(exit_with)
        return

    def parse_arguments(self):
        (opts, args) = getopt.getopt(self.args, 'hfxqve:d:i:l:m:t:', [
         'help', 'force', 'xhtml', 'quiet', 'verbose', 'ext=', 'dest=', 'documents=', 'license=', 'trac=', 'title=', 'theme=', 'modules=', 'templates='])
        generator = pudge.generator.Generator()
        for (o, a) in opts:
            if o in ('-h', '--help'):
                return self.usage
            elif o in ('-d', '--dest'):
                generator.dest = a
            elif o in ('-e', '--ext'):
                generator.file_extension = a
            elif o in ('-f', '--force'):
                generator.force = 1
            elif o in ('-q', '--quiet'):
                pudge.log.setLevel(logging.WARN)
            elif o in ('-v', '--verbose'):
                pudge.log.setLevel(logging.DEBUG)
            elif o in ('-l', '--title'):
                generator.title = a
            elif o == '--license':
                assert a in ('gnu', 'cc'), "--license should be 'gnu' or 'cc'"
                generator.license = a
            elif o in ('-m', '--modules'):
                generator.modules = a.split(',')
            elif o in ('-i', '--documents'):
                generator.document_files = a.split(',')
            elif o in ('-t', '--templates'):
                generator.template_dir = a
            elif o in ('--theme', ):
                generator.theme = a
            elif o in ('-x', '--xhtml'):
                generator.xhtml = 1
            elif o == '--trac':
                generator.trac_url = a

        if not generator.modules and not generator.document_files:
            self.usage('Must specify --modules or --documents.', exit_with=99)
            return
        return generator

    def process_command(self):
        try:
            command = self.parse_arguments()
        except Exception, e:
            raise
            self.usage(str(e), exit_with=2)
        else:
            command()


__all__ = ['PudgeCommand']
__author__ = 'Ryan Tomayko <rtomayko@gmail.com>'
__date__ = '$Date: 2005-07-01 05:09:30 -0700 (Fri, 01 Jul 2005) $'
__revision__ = '$Revision: 54 $'
__url__ = '$URL: svn://lesscode.org/pudge/trunk/pudge/cli.py $'
__copyright__ = 'Copyright 2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
if __name__ == '__main__':
    main()
# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Lib\_4xupdate.py
# Compiled at: 2006-12-03 00:43:10
__doc__ = "\nImplementation of '4xupdate' command\n(functions defined here are used by the Ft.Lib.CommandLine framework)\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n"
import sys, cStringIO
from Ft.Lib import UriException, CloseStream
from Ft.Lib.CommandLine import CommandLineApp, Options, Arguments
from Ft.Lib.CommandLine.CommandLineUtil import SourceArgToInputSource
from Ft.Xml import Domlette, XUpdate
from Ft.Xml.InputSource import DefaultFactory

class XUpdateCommandLineApp(CommandLineApp.CommandLineApp):
    __module__ = __name__
    from Ft.__config__ import NAME as project_name, VERSION as project_version, URL as project_url
    name = '4xupdate'
    summary = 'command-line tool for performing XUpdates on XML documents'
    description = '4XUpdate command-line application'
    options = [
     Options.Option('o', 'outfile=FILE', 'Write the result to the given output file')]
    arguments = [
     Arguments.RequiredArgument('source-uri', 'The URI of the XML document to which to apply the XUpdate, or "-" to indicate standard input.'),
     Arguments.RequiredArgument('xupdate-uri', 'The URI of the XML document containing XUpdate instructions, or "-" to indicate standard input.')]

    def validate_arguments(self, args):
        msg = ''
        if len(args) < 2:
            msg = 'A source URI argument and an XUpdate URI argument are required.'
        elif len(filter(lambda arg: arg == '-', args)) > 1:
            msg = 'Standard input may be used for only 1 document.'
        if msg:
            raise SystemExit('%s\nSee "4xupdate -h" for usage info.' % msg)
        return CommandLineApp.CommandLineApp.validate_arguments(self, args)

    def run(self, options, arguments):
        return Run(options, arguments)


def Run(options, args):
    out_file = options.has_key('outfile') and open(options['outfile'], 'wb') or sys.stdout
    source_arg = args['source-uri']
    xupdate_arg = args['xupdate-uri']
    try:
        source_isrc = SourceArgToInputSource(source_arg, factory=DefaultFactory)
        xupdate_isrc = SourceArgToInputSource(xupdate_arg, factory=DefaultFactory)
    except Exception, e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.flush()
        return

    try:
        xml_reader = Domlette.NonvalidatingReader
        xupdate_reader = XUpdate.Reader()
        processor = XUpdate.Processor()
        source_doc = xml_reader.parse(source_isrc)
        CloseStream(source_isrc, quiet=True)
        compiled_xupdate = xupdate_reader.fromSrc(xupdate_isrc)
        CloseStream(xupdate_isrc, quiet=True)
        processor.execute(source_doc, compiled_xupdate)
        Domlette.Print(source_doc, stream=out_file)
    except Exception, e:
        import traceback
        traceback.print_exc(1000, sys.stderr)
        raise

    try:
        if out_file.isatty():
            out_file.flush()
            sys.stderr.write('\n')
        else:
            out_file.close()
    except (IOError, ValueError):
        pass

    return
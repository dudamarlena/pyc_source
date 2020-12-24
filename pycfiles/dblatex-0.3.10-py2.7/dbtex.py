# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/core/dbtex.py
# Compiled at: 2017-04-03 18:58:57
import sys, os, re, shlex, tempfile, shutil, urllib, glob, imp
from optparse import OptionParser
from dbtexmf.core.txtparser import texinputs_parse, texstyle_parse
from dbtexmf.core.confparser import DbtexConfig
from dbtexmf.xslt import xslt
import dbtexmf.core.logger as logger
from dbtexmf.core.error import signal_error, failed_exit, dump_stack

def suffix_replace(path, oldext, newext=''):
    root, ext = os.path.splitext(path)
    if ext == oldext:
        return root + newext
    else:
        return path + newext


def path_to_uri(path):
    if os.name == 'nt':
        return 'file:' + urllib.pathname2url(path).replace('|', ':', 1)
    else:
        return urllib.pathname2url(path)


class Document():
    """
    Wrapper structure of the files built during the compilation per document
    """

    def __init__(self, filename, binfmt='pdf'):
        self.inputname = filename
        self.basename = os.path.splitext(filename)[0]
        self.rawfile = self.basename + '.rtex'
        self.texfile = self.basename + '.tex'
        self.binfile = self.basename + '.' + binfmt

    def has_subext(self, ext):
        return os.path.splitext(self.basename)[1] == ext

    def __cmp__(self, other):
        """
        Comparaison method mainly to check if the document is in a list
        """
        if cmp(self.rawfile, other) == 0:
            return 0
        if cmp(self.texfile, other) == 0:
            return 0
        if cmp(self.binfile, other) == 0:
            return 0
        return -1


class DbTex():
    USE_MKLISTINGS = 1
    xsl_header = '<?xml version="1.0"?>\n<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n                xmlns:m="http://www.w3.org/1998/Math/MathML"\n                version="1.0">\n                \n'

    def __init__(self, base=''):
        self.name = None
        self.debug = 0
        self.verbose = 0
        if base:
            self.set_base(base)
        self.xslopts = []
        self.xslparams = []
        self.xslusers = []
        self.flags = self.USE_MKLISTINGS
        self.stdindir = ''
        self.inputdir = ''
        self.input = ''
        self.input_format = 'xml'
        self.outputdir = ''
        self.output = ''
        self.format = 'pdf'
        self.tmpdir = ''
        self.tmpdir_user = None
        self.fig_paths = []
        self.bib_paths = []
        self.bst_paths = []
        self.texinputs = []
        self.texbatch = 1
        self.texpost = ''
        self.fig_format = ''
        self.backend = ''
        self.documents = []
        self.interms = []
        self.included = []
        self.basefile = ''
        self.rawfile = ''
        self.runtex = None
        self.rawtex = None
        self.xsltproc = None
        self.sgmlxml = None
        return

    def set_base(self, topdir):
        self.topdir = os.path.realpath(topdir)
        self.xslmain = os.path.join(self.topdir, 'xsl', 'docbook.xsl')
        self.xsllist = os.path.join(self.topdir, 'xsl', 'common', 'mklistings.xsl')
        self.xslset = os.path.join(self.topdir, 'xsl', 'common', 'mkdoclist.xsl')
        self.texdir = os.path.join(self.topdir, 'texstyle')
        self.texlocal = ''
        self.confdir = os.path.join(self.topdir, 'confstyle')

    def update_texinputs(self):
        sep = os.pathsep
        ti = []
        for t in self.texinputs:
            ti += t.split(sep)

        ti_opts = ti + [self.texdir + '//']
        texinputs = os.getenv('TEXINPUTS') or ''
        ti_env = texinputs.split(sep)
        try:
            syspos = ti_env.index('')
        except:
            ti_env = [
             ''] + ti_env
            syspos = 0

        ti_before = ti_env[:syspos]
        ti_after = ti_env[syspos + 1:]
        ti_after = ti_opts + ti_after
        if self.texlocal:
            ti_before = [
             self.texlocal + '//'] + ti_before
        texinputs = sep.join(ti_before + [''] + ti_after)
        os.environ['TEXINPUTS'] = texinputs

    def set_xslt(self, xsltmod=None):
        if not xsltmod:
            if self.xsltproc:
                return
            xsltmod = 'xsltproc'
        self.xsltproc = xslt.load(xsltmod)

    def set_backend(self):
        if self.backend:
            self.runtex.set_backend(self.backend)
        else:
            self.backend = self.runtex.get_backend()

    def set_format(self, format):
        if format not in ('rtex', 'tex', 'dvi', 'ps', 'pdf'):
            raise ValueError("unknown format '%s'" % format)
        else:
            self.format = format

    def unset_flags(self, what):
        self.flags &= ~what

    def get_version(self):
        f = file(os.path.join(self.topdir, 'xsl', 'version.xsl'))
        versions = re.findall('<xsl:variable[^>]*>([^<]*)<', f.read())
        f.close()
        if versions:
            return versions[0].strip()
        else:
            return 'unknown'

    def build_stylesheet(self, wrapper='custom.xsl'):
        if not (self.xslparams or self.xslusers):
            self.xslbuild = self.xslmain
            return
        f = file(wrapper, 'w')
        f.write(self.xsl_header)
        f.write('<xsl:import href="%s"/>\n' % path_to_uri(self.xslmain))
        for xsluser in self.xslusers:
            f.write('<xsl:import href="%s"/>\n' % path_to_uri(xsluser))

        self.xslparams.reverse()
        for param in self.xslparams:
            v = param.split('=', 1)
            f.write('<xsl:param name="%s">' % v[0])
            if len(v) == 2:
                f.write('%s' % v[1])
            f.write('</xsl:param>\n')

        f.write('</xsl:stylesheet>\n')
        f.close()
        self.xslbuild = os.path.realpath(wrapper)

    def make_xml(self):
        self.log.info('Build the XML file...')
        xmlfile = self.basefile + '.xml'
        self.sgmlxml.run(self.input, xmlfile)
        self.input = xmlfile

    def make_listings(self):
        self.listings = os.path.join(self.tmpdir, 'listings.xml')
        if self.flags & self.USE_MKLISTINGS:
            self.log.info('Build the listings...')
            param = {'current.dir': self.inputdir}
            self.xsltproc.use_catalogs = 0
            self.xsltproc.run(self.xsllist, self.input, self.listings, opts=self.xslopts, params=param)
        else:
            self.log.info('No external file support')
            f = file(self.listings, 'w')
            f.write('<listings/>\n')
            f.close()

    def _single_setup(self):
        if not self.output:
            output = suffix_replace(self.input, '.' + self.input_format, '.%s' % self.format)
            self.output = output
        self.documents.append(Document(self.basefile + '.' + self.input_format, binfmt=self.format))

    def _multiple_setup(self, doclist):
        if not self.outputdir:
            self.log.info('No specified output dir (-O). Use the working directory')
            self.outputdir = self.cwdir
        f = open(doclist)
        books = f.readlines()
        f.close()
        for b in books:
            d = Document(b.strip() + '.tex', binfmt=self.format)
            self.documents.append(d)

    def build_doclist(self):
        self.log.info('Build the book set list...')
        xslset = 'doclist.xsl'
        f = file(xslset, 'w')
        f.write(self.xsl_header)
        f.write('<xsl:import href="%s"/>\n' % path_to_uri(self.xslbuild))
        f.write('<xsl:import href="%s"/>\n' % path_to_uri(self.xslset))
        f.write('</xsl:stylesheet>\n')
        f.close()
        doclist = os.path.join(self.tmpdir, 'doclist.txt')
        self.xsltproc.use_catalogs = 0
        self.xsltproc.run(xslset, self.input, doclist, opts=self.xslopts)
        if os.path.isfile(doclist) and os.path.getsize(doclist) > 0:
            self._multiple_setup(doclist)
        else:
            self._single_setup()

    def make_rawtex(self):
        if len(self.documents) == 1:
            self.rawfile = self.documents[0].rawfile
        else:
            self.rawfile = 'output.rtex'
        param = {'listings.xml': self.listings, 'current.dir': self.inputdir}
        self.xsltproc.use_catalogs = 1
        self.xsltproc.run(self.xslbuild, self.input, self.rawfile, opts=self.xslopts, params=param)
        rawfiles = glob.glob('*.rtex')
        for rawfile in rawfiles:
            if rawfile not in self.documents:
                d = Document(rawfile, binfmt=self.format)
                if d.has_subext('.input'):
                    self.included.append(d)
                else:
                    self.interms.append(d)

    def make_tex(self):
        self.rawtex.set_format(self.format, self.backend)
        if self.fig_format:
            self.rawtex.fig_format(self.fig_format)
        self.rawtex.set_fig_paths([self.inputdir] + self.fig_paths)
        for d in self.documents + self.interms + self.included:
            self.rawtex.parse(d.rawfile, d.texfile)

    def make_bin(self):
        self.runtex.texpost = self.texpost
        self.runtex.set_fig_paths([self.inputdir] + self.fig_paths)
        self.runtex.set_bib_paths([self.inputdir] + self.bib_paths, [
         self.inputdir] + self.bst_paths)
        for d in self.interms + self.documents:
            self.log.info('Build %s' % d.binfile)
            self.runtex.compile(d.texfile, d.binfile, self.format, batch=self.texbatch)
            self.runtex.reinit()

    def compile(self):
        self.set_xslt()
        self.set_backend()
        self.cwdir = os.getcwd()
        self.tmpdir = self.tmpdir_user or tempfile.mkdtemp()
        if self.input:
            self.inputdir = os.path.dirname(self.input)
        else:
            self._stdin_write()
        os.chdir(self.tmpdir)
        try:
            donefiles = self._compile()
            if len(donefiles) == 1:
                shutil.move(donefiles[0], self.output)
                self.log.info("'%s' successfully built" % os.path.basename(self.output))
            else:
                for d in donefiles:
                    shutil.move(d, self.outputdir)

                donefiles.sort()
                self.log.info("Files successfully built in '%s':\n%s" % (
                 self.outputdir, ('\n').join(donefiles)))
        finally:
            os.chdir(self.cwdir)
            if not self.debug:
                shutil.rmtree(self.tmpdir)
            else:
                self.log.info('%s not removed' % self.tmpdir)

    def _stdin_write(self):
        self.inputdir = self.stdindir or self.cwdir
        self.input = os.path.join(self.tmpdir, 'stdin.xml')
        f = open(self.input, 'w')
        for line in sys.stdin:
            f.write(line)

        f.close()

    def _compile(self):
        tmpout = os.path.basename(self.input)
        for s in (' ', '\t'):
            tmpout = tmpout.replace(s, '_')

        self.basefile = suffix_replace(tmpout, '.' + self.input_format)
        if self.input_format == 'sgml':
            self.make_xml()
        self.build_stylesheet()
        self.build_doclist()
        self.update_texinputs()
        if self.debug and os.environ.has_key('TEXINPUTS'):
            if os.name != 'nt':
                f = file('env_tex', 'w')
                f.write('TEXINPUTS=%s\nexport TEXINPUTS\n' % os.environ['TEXINPUTS'])
                f.close()
            else:
                f = file('env_tex.bat', 'w')
                f.write('set TEXINPUTS=%s\n' % os.environ['TEXINPUTS'])
                f.close()
        self.make_listings()
        self.make_rawtex()
        if self.format == 'rtex':
            return [ d.rawfile for d in self.documents ]
        self.make_tex()
        if self.format == 'tex':
            return [ d.texfile for d in self.documents ]
        self.make_bin()
        return [ d.binfile for d in self.documents ]


class DbTexCommand():

    def __init__(self, base):
        prog = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        usage = '%s [options] file' % prog
        parser = OptionParser(usage=usage)
        parser.add_option('-b', '--backend', help="Backend driver to use. The available drivers are 'pdftex' (default), 'dvips' and 'xetex'.")
        parser.add_option('-B', '--no-batch', action='store_true', help='All the tex output is printed')
        parser.add_option('-c', '-S', '--config', action='append', help='Configuration file')
        parser.add_option('-C', '--changedir', help='Standard input working directory')
        parser.add_option('-d', '--debug', action='store_true', help='Debug mode. Keep the temporary directory in which %s actually works' % prog)
        parser.add_option('-D', '--dump', action='store_true', help='Dump error stack (debug purpose)')
        parser.add_option('-e', '--indexstyle', help='Index Style file to pass to makeindex')
        parser.add_option('-f', '--fig-format', help='Input figure format, used when not deduced from figure extension')
        parser.add_option('-F', '--input-format', help='Input file format: sgml, xml. (default=xml)')
        parser.add_option('-i', '--texinputs', action='append', help='Path added to TEXINPUTS')
        parser.add_option('-I', '--fig-path', action='append', dest='fig_paths', metavar='FIG_PATH', help='Additional lookup path of the figures')
        parser.add_option('-l', '--bst-path', action='append', dest='bst_paths', metavar='BST_PATH', help='Bibliography style file path')
        parser.add_option('-L', '--bib-path', action='append', dest='bib_paths', metavar='BIB_PATH', help='BibTeX database path')
        parser.add_option('-m', '--xslt', help='XSLT engine to use. (default=xsltproc)')
        parser.add_option('-o', '--output', dest='output', help='Output filename. When not used, the input filename is used, with the suffix of the output format')
        parser.add_option('-O', '--output-dir', help='Output directory for the built books. When not defined, the current working directory is used. Option used only for a document having a <set>')
        parser.add_option('-p', '--xsl-user', action='append', help='XSL user configuration file to use')
        parser.add_option('-P', '--param', dest='xslparams', action='append', metavar='PARAM=VALUE', help='Set an XSL parameter value from command line')
        parser.add_option('-q', '--quiet', action='store_true', help='Less verbose, showing only error messages')
        parser.add_option('-r', '--texpost', metavar='SCRIPT', help='Script called at the very end of the tex compilation. Its role is to modify the tex file or one of the compilation file before the last round.')
        parser.add_option('-s', '--texstyle', metavar='STYFILE', help="Latex style to apply. It can be a package name, or directly a package path that must ends with '.sty'")
        parser.add_option('-t', '--type', dest='format', help='Output format. Available formats:\ntex, dvi, ps, pdf (default=pdf)')
        parser.add_option('--dvi', action='store_true', dest='format_dvi', help='DVI output. Equivalent to -tdvi')
        parser.add_option('--pdf', action='store_true', dest='format_pdf', help='PDF output. Equivalent to -tpdf')
        parser.add_option('--ps', action='store_true', dest='format_ps', help='PostScript output. Equivalent to -tps')
        parser.add_option('-T', '--style', help='Predefined output style')
        parser.add_option('--tmpdir', help='Temporary working directory to use (for debug only)')
        parser.add_option('-v', '--version', action='store_true', help='Print the %s version' % prog)
        parser.add_option('-V', '--verbose', action='store_true', help='Verbose mode, showing the running commands')
        parser.add_option('-x', '--xslt-opts', dest='xslopts', action='append', metavar='XSLT_OPTIONS', help='Arguments directly passed to the XSLT engine')
        parser.add_option('-X', '--no-external', action='store_true', help='Disable the external text file support used for some callout processing')
        self.parser = parser
        self.base = base
        self.prog = prog
        self.run = None
        return

    def load_plugin(self, pathname):
        moddir, modname = os.path.split(pathname)
        try:
            filemod, path, descr = imp.find_module(modname, [moddir])
        except ImportError:
            try:
                filemod, path, descr = imp.find_module(modname)
            except ImportError:
                failed_exit("Error: '%s' module not found" % modname)

        mod = imp.load_module(modname, filemod, path, descr)
        filemod.close()
        return mod

    def run_setup(self, options):
        run = self.run
        if not options.format:
            if options.format_pdf:
                options.format = 'pdf'
            elif options.format_ps:
                options.format = 'ps'
            elif options.format_dvi:
                options.format = 'dvi'
        if options.format:
            try:
                run.set_format(options.format)
            except Exception as e:
                failed_exit('Error: %s' % e)

        try:
            run.set_xslt(options.xslt)
        except Exception as e:
            failed_exit('Error: %s' % e)

        if options.xslopts:
            for o in options.xslopts:
                run.xslopts += shlex.split(o)

        if options.xslparams:
            run.xslparams += options.xslparams
        if options.debug:
            run.debug = options.debug
        if options.fig_paths:
            run.fig_paths += [ os.path.realpath(p) for p in options.fig_paths ]
        if options.bib_paths:
            run.bib_paths += [ os.path.realpath(p) for p in options.bib_paths ]
        if options.bst_paths:
            run.bst_paths += [ os.path.realpath(p) for p in options.bst_paths ]
        if options.texstyle:
            try:
                xslparam, texpath = texstyle_parse(options.texstyle)
            except Exception as e:
                failed_exit('Error: %s' % e)

            run.xslparams.append(xslparam)
            if texpath:
                run.texinputs.append(texpath)
        if options.indexstyle:
            run.runtex.index_style = os.path.abspath(options.indexstyle)
        if options.texinputs:
            for texinputs in options.texinputs:
                run.texinputs += texinputs_parse(texinputs)

        if options.fig_format:
            run.fig_format = options.fig_format
        if options.input_format:
            run.input_format = options.input_format
        if options.no_batch:
            run.texbatch = 0
        if options.backend:
            run.backend = options.backend
        if options.xsl_user:
            for xfile in options.xsl_user:
                xsluser = os.path.realpath(xfile)
                if not os.path.isfile(xsluser):
                    failed_exit("Error: '%s' does not exist" % options.xsl_user)
                run.xslusers.append(xsluser)

        if options.texpost:
            is_plugin = options.texpost.startswith('plugin:')
            if is_plugin:
                path = self.load_plugin(options.texpost[len('plugin:'):])
            else:
                path = os.path.realpath(options.texpost)
                if not os.path.isfile(path):
                    failed_exit("Error: '%s' does not exist" % options.texpost)
            run.texpost = path
        if options.no_external:
            run.unset_flags(run.USE_MKLISTINGS)
        if options.verbose:
            run.verbose = options.verbose
        if options.quiet:
            run.verbose = logger.QUIET
            run.xslparams.append('output.quietly=1')
        if options.tmpdir:
            if not os.path.exists(options.tmpdir):
                try:
                    os.mkdir(options.tmpdir)
                except Exception as e:
                    failed_exit('Error: %s' % e)

            run.tmpdir_user = os.path.abspath(options.tmpdir)
        if options.dump:
            dump_stack()

    def get_config_paths(self):
        paths = [
         os.getcwd()]
        paths.append(os.path.expanduser(os.path.join('~', '.' + self.prog)))
        if 'posix' in sys.builtin_module_names:
            paths.append(os.path.join('/etc', self.prog))
        paths.append(self.run.confdir)
        conf_paths = os.getenv('DBLATEX_CONFIG_FILES')
        if not conf_paths:
            return paths
        paths += conf_paths.split(os.pathsep)
        return paths

    def main(self):
        options, args = self.parser.parse_args()
        run = self.run
        parser = self.parser
        if options.version:
            version = run.get_version()
            print '%s version %s' % (self.prog, version)
            if not args:
                sys.exit(0)
        if not args:
            parser.parse_args(args=['-h'])
        conf = DbtexConfig()
        if options.dump:
            dump_stack()
        if options.style:
            try:
                conf.paths = self.get_config_paths()
                conf.fromstyle(options.style)
            except Exception as e:
                failed_exit('Error: %s' % e)

        if options.config:
            try:
                for config in options.config:
                    conf.fromfile(config)

            except Exception as e:
                failed_exit('Error: %s' % e)

        if conf.options:
            options2, args2 = parser.parse_args(conf.options)
            self.run_setup(options2)
        self.run_setup(options)
        run.log = logger.logger(self.prog, run.verbose)
        if args[0] == '-':
            if not options.output:
                failed_exit('Error: -o expected when input from stdin')
            input = ''
            if options.changedir:
                run.stdindir = os.path.realpath(options.changedir)
        else:
            input = os.path.realpath(args[0])
        if not options.output:
            output = None
        else:
            output = os.path.realpath(options.output)
        if not options.output_dir:
            outputdir = None
        else:
            outputdir = os.path.realpath(options.output_dir)
            if not os.path.isdir(outputdir):
                failed_exit("Error: '%s' is not a directory" % options.output_dir)
            run.input = input
            run.output = output
            run.outputdir = outputdir
            try:
                run.compile()
            except Exception as e:
                signal_error(self, e)
                failed_exit('Error: %s' % e)

        return
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\pygettext\pygettext.py
# Compiled at: 2011-07-03 13:21:12
import re
try:
    import fintl
    _ = fintl.gettext
except ImportError:
    _ = lambda s: s

__doc__ = _('pygettext -- Python equivalent of xgettext(1)\n\nMany systems (Solaris, Linux, Gnu) provide extensive tools that ease the\ninternationalization of C programs. Most of these tools are independent of\nthe programming language and can be used from within Python programs.\nMartin von Loewis\' work[1] helps considerably in this regard.\n\nThere\'s one problem though; xgettext is the program that scans source code\nlooking for message strings, but it groks only C (or C++). Python\nintroduces a few wrinkles, such as dual quoting characters, triple quoted\nstrings, and raw strings. xgettext understands none of this.\n\nEnter pygettext, which uses Python\'s standard tokenize module to scan\nPython source code, generating .pot files identical to what GNU xgettext[2]\ngenerates for C and C++ code. From there, the standard GNU tools can be\nused.\n\nA word about marking Python strings as candidates for translation. GNU\nxgettext recognizes the following keywords: gettext, dgettext, dcgettext,\nand gettext_noop. But those can be a lot of text to include all over your\ncode. C and C++ have a trick: they use the C preprocessor. Most\ninternationalized C source includes a #define for gettext() to _() so that\nwhat has to be written in the source is much less. Thus these are both\ntranslatable strings:\n\n    gettext("Translatable String")\n    _("Translatable String")\n\nPython of course has no preprocessor so this doesn\'t work so well.  Thus,\npygettext searches only for _() by default, but see the -k/--keyword flag\nbelow for how to augment this.\n\n [1] http://www.python.org/workshops/1997-10/proceedings/loewis.html\n [2] http://www.gnu.org/software/gettext/gettext.html\n\nNOTE: pygettext attempts to be option and feature compatible with GNU\nxgettext where ever possible. However some options are still missing or are\nnot fully implemented. Also, xgettext\'s use of command line switches with\noption arguments is broken, and in these cases, pygettext just defines\nadditional switches.\n\nUsage: pygettext [options] inputfile ...\n\nOptions:\n\n    -a\n    --extract-all\n        Extract all strings.\n\n    -d name\n    --default-domain=name\n        Rename the default output file from messages.pot to name.pot.\n\n    -E\n    --escape\n        Replace non-ASCII characters with octal escape sequences.\n\n    -D\n    --docstrings\n        Extract module, class, method, and function docstrings.  These do\n        not need to be wrapped in _() markers, and in fact cannot be for\n        Python to consider them docstrings. (See also the -X option).\n\n    -h\n    --help\n        Print this help message and exit.\n\n    -k word\n    --keyword=word\n        Keywords to look for in addition to the default set, which are:\n        %(DEFAULTKEYWORDS)s\n\n        You can have multiple -k flags on the command line.\n\n    -K\n    --no-default-keywords\n        Disable the default set of keywords (see above).  Any keywords\n        explicitly added with the -k/--keyword option are still recognized.\n\n    --no-location\n        Do not write filename/lineno location comments.\n\n    -n\n    --add-location\n        Write filename/lineno location comments indicating where each\n        extracted string is found in the source.  These lines appear before\n        each msgid.  The style of comments is controlled by the -S/--style\n        option.  This is the default.\n\n    -o filename\n    --output=filename\n        Rename the default output file from messages.pot to filename.  If\n        filename is `-\' then the output is sent to standard out.\n\n    -p dir\n    --output-dir=dir\n        Output files will be placed in directory dir.\n\n    -S stylename\n    --style stylename\n        Specify which style to use for location comments.  Two styles are\n        supported:\n\n        Solaris  # File: filename, line: line-number\n        GNU      #: filename:line\n\n        The style name is case insensitive.  GNU style is the default.\n\n    -v\n    --verbose\n        Print the names of the files being processed.\n\n    -V\n    --version\n        Print the version of pygettext and exit.\n\n    -w columns\n    --width=columns\n        Set width of output to columns.\n\n    -x filename\n    --exclude-file=filename\n        Specify a file that contains a list of strings that are not be\n        extracted from the input files.  Each string to be excluded must\n        appear on a line by itself in the file.\n\n    -X filename\n    --no-docstrings=filename\n        Specify a file that contains a list of files (one per line) that\n        should not have their docstrings extracted.  This is only useful in\n        conjunction with the -D option above.\n\nIf `inputfile\' is -, standard input is read.\n')
import os, imp, sys, glob, time, getopt, token, tokenize, operator
try:
    import kid.parser as kid_parser
except ImportError:
    kid_parser = None

try:
    from genshi.template import MarkupTemplate as GenshiMarkupTemplate
    from genshi.filters.i18n import Translator as GenshiTranslator
except ImportError:
    GenshiMarkupTemplate = None

__version__ = '1.5'
default_keywords = [
 '_']
DEFAULTKEYWORDS = (', ').join(default_keywords)
EMPTYSTRING = ''
pot_header = _('# SOME DESCRIPTIVE TITLE.\n# Copyright (C) YEAR ORGANIZATION\n# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: PACKAGE VERSION\\n"\n"POT-Creation-Date: %(time)s\\n"\n"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n"Language-Team: LANGUAGE <LL@li.org>\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=%(charset)s\\n"\n"Content-Transfer-Encoding: %(charset)s\\n"\n"Generated-By: pygettext.py %(version)s\\n"\n\n')

def usage(code, msg=''):
    print >> sys.stderr, __doc__ % globals()
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


escapes = []

def make_escapes(pass_iso8859):
    global escapes
    if pass_iso8859:
        mod = 128
    else:
        mod = 256
    for i in range(256):
        if 32 <= i % mod <= 126:
            escapes.append(chr(i))
        else:
            escapes.append('\\%03o' % i)

    escapes[ord('\\')] = '\\\\'
    escapes[ord('\t')] = '\\t'
    escapes[ord('\r')] = '\\r'
    escapes[ord('\n')] = '\\n'
    escapes[ord('"')] = '\\"'


def escape_ascii(s):
    """Escape all non-ascii text plus control chars and Python literals."""
    s = list(s)
    for i in range(len(s)):
        s[i] = escapes[ord(s[i])]

    return EMPTYSTRING.join(s)


def escape_unicode(s):
    """Escape control chars and Python literals, leave non-ascii text intact."""
    s = s.replace('\\', '\\\\').replace('\t', '\\t').replace('\r', '\\r').replace('\n', '\\n').replace('"', '\\"')

    def repl(m):
        return '\\%03o' % ord(m.group(0))

    return re.sub('[\x01-\x1f]', repl, s)


def safe_eval(s):
    return eval(s, {'__builtins__': {}}, {})


def normalize(s, escape=False):
    lines = s.split('\n')
    if len(lines) == 1:
        s = '"' + escape_unicode(s) + '"'
    else:
        if not lines[(-1)]:
            del lines[-1]
            lines[-1] = lines[(-1)] + '\n'
        for i in range(len(lines)):
            lines[i] = escape_unicode(lines[i])

        lineterm = '\\n"\n"'
        s = '""\n"' + lineterm.join(lines) + '"'
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    if escape:

        def repl(m):
            return '\\%03o' % ord(m.group(0))

        s = re.sub(b'[\x80-\xff]', repl, s)
    return s


def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [ c in str for c in set ]


def _visit_pyfiles(list, dirname, names):
    """Helper for getFilesForName()."""
    global _py_ext
    if '_py_ext' not in globals():
        _py_ext = [ triple[0] for triple in imp.get_suffixes() if triple[2] == imp.PY_SOURCE ][0]
    if 'CVS' in names:
        names.remove('CVS')
    if '.svn' in names:
        names.remove('.svn')
    list.extend([ os.path.join(dirname, file) for file in names if os.path.splitext(file)[1] == _py_ext ])


def _get_modpkg_path(dotted_name, pathlist=None):
    """Get the filesystem path for a module or a package.

    Return the file system path to a file for a module, and to a directory for
    a package. Return None if the name is not found, or is a builtin or
    extension module.
    """
    parts = dotted_name.split('.', 1)
    if len(parts) > 1:
        try:
            (file, pathname, description) = imp.find_module(parts[0], pathlist)
            if file:
                file.close()
        except ImportError:
            return
        else:
            if description[2] == imp.PKG_DIRECTORY:
                pathname = _get_modpkg_path(parts[1], [pathname])
            else:
                pathname = None
    else:
        try:
            (file, pathname, description) = imp.find_module(dotted_name, pathlist)
            if file:
                file.close()
            if description[2] not in [imp.PY_SOURCE, imp.PKG_DIRECTORY]:
                pathname = None
        except ImportError:
            pathname = None

    return pathname


def getFilesForName(name):
    """Get a list of module files for a filename, a module or package name,
    or a directory.
    """
    if not os.path.exists(name):
        if containsAny(name, '*?[]'):
            files = glob.glob(name)
            list = []
            for file in files:
                list.extend(getFilesForName(file))

            return list
        name = _get_modpkg_path(name)
        if not name:
            return []
    if os.path.isdir(name):
        list = []
        os.path.walk(name, _visit_pyfiles, list)
        return list
    elif os.path.exists(name):
        return [name]
    return []


def extract_genshi_strings(filename, options=None):
    """Extract translatable strings from a Genshi template.

    The extractor will get all the text inside all elements which are
    not in the ignore list (see options) and the values of all
    attributes named in the include list.

    Options:

    `ignore_tags` -- `'script style'`
        List of element names. Content inside elements named in
        this list is not extracted as translatable text. Can be a
        space-separated string or a list of string.
    `include_attrs` -- `'abbr alt label prompt standby summary title'`
        List of attribute names. Only values of the attributes named in this
        list are extracted as translatable text. Can be a space-separated
        string or a list of string.

    See http://genshi.edgewall.org/wiki/Documentation/0.5.x/i18n.html for
    more information.

    """
    if not GenshiMarkupTemplate:
        raise ImportError('Genshi templating is not installed.')
    if options is None:
        options = {}
    try:
        stream = GenshiMarkupTemplate(open(filename), filename=filename, filepath='.').stream
        translator = GenshiTranslator(**options)
        return translator.extract(stream)
    except Exception:
        print >> sys.stderr, 'Extracting from Genshi template', filename
        raise

    return


class TokenEater:
    __module__ = __name__

    def __init__(self, options):
        self.__options = options
        self.__messages = {}
        self.__state = self.__waiting
        self.__data = []
        self.__lineno = -1
        self.__freshmodule = 1
        self.__curfile = None
        self.__encoding = None
        return

    def __call__(self, ttype, tstring, stup, etup, line):
        self.__state(ttype, tstring, stup[0])

    def __waiting(self, ttype, tstring, lineno):
        opts = self.__options
        if opts.docstrings and not opts.nodocstrings.get(self.__curfile):
            if self.__freshmodule:
                if ttype == tokenize.STRING:
                    self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
                    self.__freshmodule = 0
                elif ttype not in (tokenize.COMMENT, tokenize.NL):
                    self.__freshmodule = 0
                return
            if ttype == tokenize.NAME and tstring in ('class', 'def'):
                self.__state = self.__suiteseen
                return
        if ttype == tokenize.NAME and tstring in opts.keywords:
            self.__state = self.__keywordseen

    def __suiteseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == ':':
            self.__state = self.__suitedocstring

    def __suitedocstring(self, ttype, tstring, lineno):
        if ttype == tokenize.STRING:
            self.__addentry(safe_eval(tstring), lineno, isdocstring=1)
            self.__state = self.__waiting
        elif ttype not in (tokenize.NEWLINE, tokenize.INDENT, tokenize.COMMENT):
            self.__state = self.__waiting

    def __keywordseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == '(':
            self.__data = []
            self.__lineno = lineno
            self.__state = self.__openseen
        else:
            self.__state = self.__waiting

    def __openseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == ',':
            if self.__data:
                self.__addentry(EMPTYSTRING.join(self.__data))
            self.__state = self.__waiting
        elif ttype == tokenize.OP and tstring == ')':
            if self.__data:
                self.__addentry(EMPTYSTRING.join(self.__data))
            self.__state = self.__waiting
        elif ttype == tokenize.STRING:
            self.__data.append(safe_eval(tstring))
        elif ttype not in [tokenize.COMMENT, token.INDENT, token.DEDENT, token.NEWLINE, tokenize.NL]:
            print >> sys.stderr, _('*** %(file)s:%(lineno)s: Seen unexpected token "%(token)s"') % {'token': tstring, 'file': self.__curfile, 'lineno': self.__lineno}
            self.__state = self.__waiting

    def __addentry(self, msg, lineno=None, isdocstring=0, istemplatestring=0):
        """The tokenize module always returns unicode strings even when they
        are in fact coded string instances. To deal with this we use a hack:
        evaluate string's representation without leading "u" to force
        interpration as a coded string, then we decode it using the already
        known file encoding.

        """
        if not istemplatestring:
            if type(msg) is str:
                msg = eval(repr(msg))
            else:
                msg = eval(repr(msg)[1:])
            msg = msg.decode(self.__encoding)
        if lineno is None:
            lineno = self.__lineno
        if msg not in self.__options.toexclude:
            entry = (
             self.__curfile, lineno)
            self.__messages.setdefault(msg, {})[entry] = isdocstring
        return

    def set_filename(self, filename):
        self.__curfile = filename
        self.__freshmodule = 1

    def set_file_encoding(self, fp):
        """Search for -*- coding: -*- magic comment to find out file encoding"""
        self.__encoding = 'utf-8'
        for line in fp.readlines()[:5]:
            m = re.match('#\\s*-\\*-\\s+coding:\\s+(\\w+)\\s+-\\*-', line)
            if m:
                self.__encoding = m.group(1)
                break

        fp.seek(0)

    def __contains_inline_python(self, msg):
        return '${' in msg and '$${' not in msg

    def __strip_namespace_uri(self, tag):
        return tag.split('}', 1)[(-1)]

    def extract_genshi_strings(self):
        """Extract translatable strings from a Genshi template.

        See the docstring of the eponymous module function for documentation.

        """
        if self.__curfile:
            for msg in extract_genshi_strings(self.__curfile):
                lineno, text = msg[0], msg[2]
                if text:
                    if isinstance(text, tuple):
                        for subtext in text:
                            if subtext:
                                self.__addentry(subtext, lineno, istemplatestring=1)

                    else:
                        self.__addentry(text, lineno, istemplatestring=1)

    def extract_kid_strings(self):
        if not self.__curfile:
            return
        if not kid_parser:
            raise ImportError('Kid templating is not installed.')
        tag = None
        tags = []
        for (ev, item) in kid_parser.document(self.__curfile):
            if ev == kid_parser.TEXT:
                if tag:
                    item = item.strip()
                    if item and not self.__contains_inline_python(item):
                        self.__addentry(item, tag, istemplatestring=1)
            elif ev == kid_parser.START:
                tag = item.tag
                if isinstance(tag, basestring):
                    tag = self.__strip_namespace_uri(tag)
                    if tag in ('script', 'style'):
                        tag = None
                else:
                    tag = None
                tags.append(tag)
            elif ev == kid_parser.END:
                if tags:
                    tag = tags.pop()

        return

    def write(self, fp):
        options = self.__options
        timestamp = time.strftime('%Y-%m-%d %H:%M')
        t = {'time': timestamp, 'version': __version__, 'charset': 'utf-8'}
        print >> fp, pot_header % t
        reverse = {}
        for (k, v) in self.__messages.items():
            keys = v.keys()
            keys.sort()
            reverse.setdefault(tuple(keys), []).append((k, v))

        rkeys = reverse.keys()
        rkeys.sort()
        for rkey in rkeys:
            rentries = reverse[rkey]
            rentries.sort()
            for (k, v) in rentries:
                isdocstring = 0
                if reduce(operator.__add__, v.values()):
                    isdocstring = 1
                v = v.keys()
                v.sort()
                if not options.writelocations:
                    pass
                if options.locationstyle == options.SOLARIS:
                    for (filename, lineno) in v:
                        d = {'filename': filename, 'lineno': lineno}
                        print >> fp, _('# File: %(filename)s, line: %(lineno)s') % d

                elif options.locationstyle == options.GNU:
                    locline = '#:'
                    for (filename, lineno) in v:
                        d = {'filename': filename, 'lineno': lineno}
                        s = _(' %(filename)s:%(lineno)s') % d
                        if len(locline) + len(s) <= options.width:
                            locline += s
                        else:
                            print >> fp, locline
                            locline = '#:' + s

                    if len(locline) > 2:
                        print >> fp, locline
                if isdocstring:
                    print >> fp, '#, docstring'
                if k:
                    print >> fp, 'msgid', normalize(k, options.escape)
                    print >> fp, 'msgstr ""\n'


def main():
    global default_keywords
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'ad:UDEhk:Kno:p:S:Vvw:x:X:', [
         'extract-all', 'default-domain=', 'escape', 'help', 'keyword=', 'no-default-keywords', 'add-location', 'no-location', 'output=', 'output-dir=', 'style=', 'verbose', 'version', 'width=', 'exclude-file=', 'docstrings', 'no-docstrings', 'support-unicode'])
    except getopt.error, msg:
        usage(1, msg)

    class Options:
        __module__ = __name__
        GNU = 1
        SOLARIS = 2
        extractall = 0
        escape = 0
        keywords = []
        outpath = ''
        outfile = 'messages.pot'
        writelocations = 1
        locationstyle = GNU
        verbose = 0
        width = 78
        excludefilename = ''
        docstrings = 0
        nodocstrings = {}

    options = Options()
    locations = {'gnu': options.GNU, 'solaris': options.SOLARIS}
    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-a', '--extract-all'):
            options.extractall = 1
        elif opt in ('-d', '--default-domain'):
            options.outfile = arg + '.pot'
        elif opt in ('-E', '--escape'):
            options.escape = 1
        elif opt in ('-D', '--docstrings'):
            options.docstrings = 1
        elif opt in ('-k', '--keyword'):
            options.keywords.append(arg)
        elif opt in ('-K', '--no-default-keywords'):
            default_keywords = []
        elif opt in ('-n', '--add-location'):
            options.writelocations = 1
        elif opt in ('--no-location', ):
            options.writelocations = 0
        elif opt in ('-S', '--style'):
            options.locationstyle = locations.get(arg.lower())
            if options.locationstyle is None:
                usage(1, _('Invalid value for --style: %s') % arg)
        elif opt in ('-o', '--output'):
            options.outfile = arg
        elif opt in ('-p', '--output-dir'):
            options.outpath = arg
        elif opt in ('-v', '--verbose'):
            options.verbose = 1
        elif opt in ('-V', '--version'):
            print _('pygettext.py (xgettext for Python) %s') % __version__
            sys.exit(0)
        elif opt in ('-w', '--width'):
            try:
                options.width = int(arg)
            except ValueError:
                usage(1, _('--width argument must be an integer: %s') % arg)

        elif opt in ('-x', '--exclude-file'):
            options.excludefilename = arg
        elif opt in ('-X', '--no-docstrings'):
            fp = open(arg)
            try:
                while 1:
                    line = fp.readline()
                    if not line:
                        break
                    options.nodocstrings[line[:-1]] = 1

            finally:
                fp.close()

    make_escapes(0)
    options.keywords.extend(default_keywords)
    if options.excludefilename:
        try:
            fp = open(options.excludefilename)
            options.toexclude = fp.readlines()
            fp.close()
        except IOError:
            print >> sys.stderr, _("Can't read --exclude-file: %s") % options.excludefilename
            sys.exit(1)

    else:
        options.toexclude = []
    expanded = []
    for arg in args:
        if arg == '-':
            expanded.append(arg)
        else:
            expanded.extend(getFilesForName(arg))

    args = expanded
    eater = TokenEater(options)
    for filename in args:
        if filename == '-':
            if options.verbose:
                print _('Reading standard input')
            fp = sys.stdin
            closep = 0
        else:
            if options.verbose:
                print _('Working on %s') % filename
            fp = open(filename)
            eater.set_file_encoding(fp)
            closep = 1
        try:
            eater.set_filename(filename)
            if os.path.splitext(filename)[(-1)].lower() == '.kid':
                try:
                    eater.extract_kid_strings()
                except Exception, e:
                    print >> sys.stderr, 'Kid eater exception:', e

            elif os.path.splitext(filename)[(-1)].lower() == '.html':
                try:
                    eater.extract_genshi_strings()
                except Exception, e:
                    print >> sys.stderr, 'Genshi eater exception:', e

            else:
                try:
                    tokenize.tokenize(fp.readline, eater)
                except tokenize.TokenError, e:
                    print >> sys.stderr, '%s: %s, line %d, column %d' % (e[0], filename, e[1][0], e[1][1])

        finally:
            if closep:
                fp.close()

    if options.outfile == '-':
        fp = sys.stdout
        closep = 0
    else:
        if options.outpath:
            options.outfile = os.path.join(options.outpath, options.outfile)
        fp = open(options.outfile, 'w+')
        closep = 1
    try:
        eater.write(fp)
    finally:
        if closep:
            fp.close()
    return


if __name__ == '__main__':
    main()
    _('a unicode string')
    _('*** Seen unexpected token "%(token)s"') % {'token': 'test'}
    _('morethanonestring')
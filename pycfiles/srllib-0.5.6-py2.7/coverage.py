# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\testing\coverage.py
# Compiled at: 2012-05-11 12:09:02
r"""Usage:

coverage.py -x [-p] MODULE.py [ARG1 ARG2 ...]
    Execute module, passing the given command-line arguments, collecting
    coverage data. With the -p option, write to a temporary file containing
    the machine name and process ID.

coverage.py -e
    Erase collected coverage data.

coverage.py -c
    Collect data from multiple coverage files (as created by -p option above)
    and store it into a single file representing the union of the coverage.

coverage.py -r [-m] [-o dir1,dir2,...] FILE1 FILE2 ...
    Report on the statement coverage for the given files.  With the -m
    option, show line numbers of the statements that weren't executed.

coverage.py -a [-d dir] [-o dir1,dir2,...] FILE1 FILE2 ...
    Make annotated copies of the given files, marking statements that
    are executed with > and statements that are missed with !.  With
    the -d option, make the copies in that directory.  Without the -d
    option, make each copy in the same directory as the original.

-o dir,dir2,...
  Omit reporting or annotating files when their filename path starts with
  a directory listed in the omit list.
  e.g. python coverage.py -i -r -o c:\python23,lib\enthought\traits

Coverage data is saved in the file .coverage by default.  Set the
COVERAGE_FILE environment variable to save it somewhere else."""
__version__ = '2.6.20060823'
import compiler, compiler.visitor, os, re, string, sys, threading, types
from socket import gethostname

class StatementFindingAstVisitor(compiler.visitor.ASTVisitor):

    def __init__(self, statements, excluded, suite_spots):
        compiler.visitor.ASTVisitor.__init__(self)
        self.statements = statements
        self.excluded = excluded
        self.suite_spots = suite_spots
        self.excluding_suite = 0

    def doRecursive(self, node):
        self.recordNodeLine(node)
        for n in node.getChildNodes():
            self.dispatch(n)

    visitStmt = visitModule = doRecursive

    def doCode(self, node):
        if hasattr(node, 'decorators') and node.decorators:
            self.dispatch(node.decorators)
            self.recordAndDispatch(node.code)
        else:
            self.doSuite(node, node.code)

    visitFunction = visitClass = doCode

    def getFirstLine(self, node):
        lineno = node.lineno
        for n in node.getChildNodes():
            f = self.getFirstLine(n)
            if lineno and f:
                lineno = min(lineno, f)
            else:
                lineno = lineno or f

        return lineno

    def getLastLine(self, node):
        lineno = node.lineno
        for n in node.getChildNodes():
            lineno = max(lineno, self.getLastLine(n))

        return lineno

    def doStatement(self, node):
        self.recordLine(self.getFirstLine(node))

    visitAssert = visitAssign = visitAssTuple = visitDiscard = visitPrint = visitPrintnl = visitRaise = visitSubscript = visitDecorators = doStatement

    def recordNodeLine(self, node):
        return self.recordLine(node.lineno)

    def recordLine(self, lineno):
        if lineno:
            if lineno in self.suite_spots:
                lineno = self.suite_spots[lineno][0]
            if self.excluding_suite:
                self.excluded[lineno] = 1
                return 0
            if self.excluded.has_key(lineno) or self.suite_spots.has_key(lineno) and self.excluded.has_key(self.suite_spots[lineno][1]):
                return 0
            self.statements[lineno] = 1
            return 1
        return 0

    default = recordNodeLine

    def recordAndDispatch(self, node):
        self.recordNodeLine(node)
        self.dispatch(node)

    def doSuite(self, intro, body, exclude=0):
        exsuite = self.excluding_suite
        if exclude or intro and not self.recordNodeLine(intro):
            self.excluding_suite = 1
        self.recordAndDispatch(body)
        self.excluding_suite = exsuite

    def doPlainWordSuite(self, prevsuite, suite):
        lastprev = self.getLastLine(prevsuite)
        firstelse = self.getFirstLine(suite)
        for l in range(lastprev + 1, firstelse):
            if self.suite_spots.has_key(l):
                self.doSuite(None, suite, exclude=self.excluded.has_key(l))
                break
        else:
            self.doSuite(None, suite)

        return

    def doElse(self, prevsuite, node):
        if node.else_:
            self.doPlainWordSuite(prevsuite, node.else_)

    def visitFor(self, node):
        self.doSuite(node, node.body)
        self.doElse(node.body, node)

    def visitIf(self, node):
        self.doSuite(node, node.tests[0][1])
        for t, n in node.tests[1:]:
            self.doSuite(t, n)

        self.doElse(node.tests[(-1)][1], node)

    def visitWhile(self, node):
        self.doSuite(node, node.body)
        self.doElse(node.body, node)

    def visitTryExcept(self, node):
        self.doSuite(node, node.body)
        for i in range(len(node.handlers)):
            a, b, h = node.handlers[i]
            if not a:
                if i > 0:
                    prev = node.handlers[(i - 1)][2]
                else:
                    prev = node.body
                self.doPlainWordSuite(prev, h)
            else:
                self.doSuite(a, h)

        self.doElse(node.handlers[(-1)][2], node)

    def visitTryFinally(self, node):
        self.doSuite(node, node.body)
        self.doPlainWordSuite(node.body, node.final)

    def visitGlobal(self, node):
        pass


the_coverage = None

class CoverageException(Exception):
    pass


class coverage():
    cache_default = '.coverage'
    cache_env = 'COVERAGE_FILE'
    c = {}
    cexecuted = {}
    analysis_cache = {}
    canonical_filename_cache = {}

    def __init__(self):
        global the_coverage
        if the_coverage:
            raise CoverageException, 'Only one coverage object allowed.'
        self.usecache = 1
        self.cache = None
        self.exclude_re = ''
        self.nesting = 0
        self.cstack = []
        self.xstack = []
        self.relative_dir = os.path.normcase(os.path.abspath(os.curdir) + os.path.sep)
        return

    def t(self, f, w, a):
        if w == 'line':
            self.c[(f.f_code.co_filename, f.f_lineno)] = 1
            for c in self.cstack:
                c[(f.f_code.co_filename, f.f_lineno)] = 1

        return self.t

    def help(self, error=None):
        if error:
            print error
            print
        print __doc__
        sys.exit(1)

    def command_line(self, argv, help=None):
        import getopt
        help = help or self.help
        settings = {}
        optmap = {'-a': 'annotate', 
           '-c': 'collect', 
           '-d:': 'directory=', 
           '-e': 'erase', 
           '-h': 'help', 
           '-i': 'ignore-errors', 
           '-m': 'show-missing', 
           '-p': 'parallel-mode', 
           '-r': 'report', 
           '-x': 'execute', 
           '-o:': 'omit='}
        short_opts = string.join(map(lambda o: o[1:], optmap.keys()), '')
        long_opts = optmap.values()
        options, args = getopt.getopt(argv, short_opts, long_opts)
        for o, a in options:
            if optmap.has_key(o):
                settings[optmap[o]] = 1
            elif optmap.has_key(o + ':'):
                settings[optmap[(o + ':')]] = a
            elif o[2:] in long_opts:
                settings[o[2:]] = 1
            elif o[2:] + '=' in long_opts:
                settings[o[2:] + '='] = a

        if settings.get('help'):
            help()
        for i in ['erase', 'execute']:
            for j in ['annotate', 'report', 'collect']:
                if settings.get(i) and settings.get(j):
                    help("You can't specify the '%s' and '%s' options at the same time." % (
                     i, j))

        args_needed = settings.get('execute') or settings.get('annotate') or settings.get('report')
        action = settings.get('erase') or settings.get('collect') or args_needed
        if not action:
            help('You must specify at least one of -e, -x, -c, -r, or -a.')
        if not args_needed and args:
            help('Unexpected arguments: %s' % (' ').join(args))
        self.get_ready(settings.get('parallel-mode'))
        self.exclude('#pragma[: ]+[nN][oO] [cC][oO][vV][eE][rR]')
        if settings.get('erase'):
            self.erase()
        if settings.get('execute'):
            if not args:
                help('Nothing to do.')
            sys.argv = args
            self.start()
            import __main__
            sys.path[0] = os.path.dirname(sys.argv[0])
            execfile(sys.argv[0], __main__.__dict__)
        if settings.get('collect'):
            self.collect()
        if not args:
            args = self.cexecuted.keys()
        ignore_errors = settings.get('ignore-errors')
        show_missing = settings.get('show-missing')
        directory = settings.get('directory=')
        omit = settings.get('omit=')
        if omit is not None:
            omit = omit.split(',')
        else:
            omit = []
        if settings.get('report'):
            self.report(args, show_missing, ignore_errors, omit_prefixes=omit)
        if settings.get('annotate'):
            self.annotate(args, directory, ignore_errors, omit_prefixes=omit)
        return

    def use_cache(self, usecache, cache_file=None):
        self.usecache = usecache
        if cache_file and not self.cache:
            self.cache_default = cache_file

    def get_ready(self, parallel_mode=False):
        if self.usecache and not self.cache:
            self.cache = os.environ.get(self.cache_env, self.cache_default)
            if parallel_mode:
                self.cache += '.' + gethostname() + '.' + str(os.getpid())
            self.restore()
        self.analysis_cache = {}

    def start(self, parallel_mode=False):
        self.get_ready(parallel_mode)
        if self.nesting == 0:
            sys.settrace(self.t)
            if hasattr(threading, 'settrace'):
                threading.settrace(self.t)
        self.nesting += 1

    def stop(self):
        self.nesting -= 1
        if self.nesting == 0:
            sys.settrace(None)
            if hasattr(threading, 'settrace'):
                threading.settrace(None)
        return

    def erase(self):
        self.c = {}
        self.analysis_cache = {}
        self.cexecuted = {}
        if self.cache and os.path.exists(self.cache):
            os.remove(self.cache)
        self.exclude_re = ''

    def exclude(self, re):
        if self.exclude_re:
            self.exclude_re += '|'
        self.exclude_re += '(' + re + ')'

    def begin_recursive(self):
        self.cstack.append(self.c)
        self.xstack.append(self.exclude_re)

    def end_recursive(self):
        self.c = self.cstack.pop()
        self.exclude_re = self.xstack.pop()

    def save(self):
        if self.usecache and self.cache:
            self.canonicalize_filenames()
            cache = open(self.cache, 'wb')
            import marshal
            marshal.dump(self.cexecuted, cache)
            cache.close()

    def restore(self):
        self.c = {}
        self.cexecuted = {}
        assert self.usecache
        if os.path.exists(self.cache):
            self.cexecuted = self.restore_file(self.cache)

    def restore_file(self, file_name):
        try:
            cache = open(file_name, 'rb')
            import marshal
            cexecuted = marshal.load(cache)
            cache.close()
            if isinstance(cexecuted, types.DictType):
                return cexecuted
            return {}
        except:
            return {}

    def collect(self):
        cache_dir, local = os.path.split(self.cache)
        for file in os.listdir(cache_dir):
            if not file.startswith(local):
                continue
            full_path = os.path.join(cache_dir, file)
            cexecuted = self.restore_file(full_path)
            self.merge_data(cexecuted)

    def merge_data(self, new_data):
        for file_name, file_data in new_data.items():
            if self.cexecuted.has_key(file_name):
                self.merge_file_data(self.cexecuted[file_name], file_data)
            else:
                self.cexecuted[file_name] = file_data

    def merge_file_data(self, cache_data, new_data):
        for line_number in new_data.keys():
            if not cache_data.has_key(line_number):
                cache_data[line_number] = new_data[line_number]

    def canonical_filename(self, filename):
        if not self.canonical_filename_cache.has_key(filename):
            f = filename
            if os.path.isabs(f) and not os.path.exists(f):
                f = os.path.basename(f)
            if not os.path.isabs(f):
                for path in [os.curdir] + sys.path:
                    g = os.path.join(path, f)
                    if os.path.exists(g):
                        f = g
                        break

            cf = os.path.normcase(os.path.abspath(f))
            self.canonical_filename_cache[filename] = cf
        return self.canonical_filename_cache[filename]

    def canonicalize_filenames(self):
        for filename, lineno in self.c.keys():
            f = self.canonical_filename(filename)
            if not self.cexecuted.has_key(f):
                self.cexecuted[f] = {}
            self.cexecuted[f][lineno] = 1

        self.c = {}

    def morf_filename(self, morf):
        if isinstance(morf, types.ModuleType):
            if not hasattr(morf, '__file__'):
                raise CoverageException, 'Module has no __file__ attribute.'
            file = morf.__file__
        else:
            file = morf
        return self.canonical_filename(file)

    def analyze_morf(self, morf):
        if self.analysis_cache.has_key(morf):
            return self.analysis_cache[morf]
        filename = self.morf_filename(morf)
        ext = os.path.splitext(filename)[1]
        if ext == '.pyc':
            if not os.path.exists(filename[0:-1]):
                raise CoverageException, "No source for compiled code '%s'." % filename
            filename = filename[0:-1]
        elif ext != '.py':
            raise CoverageException, "File '%s' not Python source." % filename
        source = open(filename, 'r')
        lines, excluded_lines = self.find_executable_statements(source.read(), exclude=self.exclude_re)
        source.close()
        result = (filename, lines, excluded_lines)
        self.analysis_cache[morf] = result
        return result

    def get_suite_spots(self, tree, spots):
        import symbol, token
        for i in range(1, len(tree)):
            if type(tree[i]) == type(()):
                if tree[i][0] == symbol.suite:
                    lineno_colon = lineno_word = None
                    for j in range(i - 1, 0, -1):
                        if tree[j][0] == token.COLON:
                            lineno_colon = tree[j][2]
                        elif tree[j][0] == token.NAME:
                            if tree[j][1] == 'elif':
                                t = tree[(j + 1)]
                                while t and token.ISNONTERMINAL(t[0]):
                                    t = t[1]

                                if t:
                                    lineno_word = t[2]
                            else:
                                lineno_word = tree[j][2]
                            break
                        elif tree[j][0] == symbol.except_clause:
                            if tree[j][1][0] == token.NAME:
                                lineno_word = tree[j][1][2]
                                break

                    if lineno_colon and lineno_word:
                        for l in range(lineno_word, lineno_colon + 1):
                            spots[l] = (lineno_word, lineno_colon)

                self.get_suite_spots(tree[i], spots)

        return

    def find_executable_statements(self, text, exclude=None):
        excluded = {}
        suite_spots = {}
        if exclude:
            reExclude = re.compile(exclude)
            lines = text.split('\n')
            for i in range(len(lines)):
                if reExclude.search(lines[i]):
                    excluded[i + 1] = 1

        import parser
        tree = parser.suite(text + '\n\n').totuple(1)
        self.get_suite_spots(tree, suite_spots)
        statements = {}
        ast = compiler.parse(text + '\n\n')
        visitor = StatementFindingAstVisitor(statements, excluded, suite_spots)
        compiler.walk(ast, visitor, walker=visitor)
        lines = statements.keys()
        lines.sort()
        excluded_lines = excluded.keys()
        excluded_lines.sort()
        return (lines, excluded_lines)

    def format_lines(self, statements, lines):
        pairs = []
        i = 0
        j = 0
        start = None
        pairs = []
        while i < len(statements) and j < len(lines):
            if statements[i] == lines[j]:
                if start == None:
                    start = lines[j]
                end = lines[j]
                j = j + 1
            elif start:
                pairs.append((start, end))
                start = None
            i = i + 1

        if start:
            pairs.append((start, end))

        def stringify(pair):
            start, end = pair
            if start == end:
                return '%d' % start
            else:
                return '%d-%d' % (start, end)

        return string.join(map(stringify, pairs), ', ')

    def analysis(self, morf):
        f, s, _, m, mf = self.analysis2(morf)
        return (f, s, m, mf)

    def analysis2(self, morf):
        filename, statements, excluded = self.analyze_morf(morf)
        self.canonicalize_filenames()
        if not self.cexecuted.has_key(filename):
            self.cexecuted[filename] = {}
        missing = []
        for line in statements:
            if not self.cexecuted[filename].has_key(line):
                missing.append(line)

        return (
         filename, statements, excluded, missing,
         self.format_lines(statements, missing))

    def relative_filename(self, filename):
        """ Convert filename to relative filename from self.relative_dir.
        """
        return filename.replace(self.relative_dir, '')

    def morf_name(self, morf):
        """ Return the name of morf as used in report.
        """
        if isinstance(morf, types.ModuleType):
            return morf.__name__
        else:
            return self.relative_filename(os.path.splitext(morf)[0])

    def filter_by_prefix(self, morfs, omit_prefixes):
        """ Return list of morfs where the morf name does not begin
            with any one of the omit_prefixes.
        """
        filtered_morfs = []
        for morf in morfs:
            for prefix in omit_prefixes:
                if self.morf_name(morf).startswith(prefix):
                    break
            else:
                filtered_morfs.append(morf)

        return filtered_morfs

    def morf_name_compare(self, x, y):
        return cmp(self.morf_name(x), self.morf_name(y))

    def report(self, morfs, show_missing=1, ignore_errors=0, file=None, omit_prefixes=[]):
        if not isinstance(morfs, types.ListType):
            morfs = [
             morfs]
        morfs = self.filter_by_prefix(morfs, omit_prefixes)
        morfs.sort(self.morf_name_compare)
        max_name = max([5] + map(len, map(self.morf_name, morfs)))
        fmt_name = '%%- %ds  ' % max_name
        fmt_err = fmt_name + '%s: %s'
        header = fmt_name % 'Name' + ' Stmts   Exec  Cover'
        fmt_coverage = fmt_name + '% 6d % 6d % 5d%%'
        if show_missing:
            header = header + '   Missing'
            fmt_coverage = fmt_coverage + '   %s'
        if not file:
            file = sys.stdout
        print >> file, header
        print >> file, '-' * len(header)
        total_statements = 0
        total_executed = 0
        for morf in morfs:
            name = self.morf_name(morf)
            try:
                _, statements, _, missing, readable = self.analysis2(morf)
                n = len(statements)
                m = n - len(missing)
                if n > 0:
                    pc = 100.0 * m / n
                else:
                    pc = 100.0
                args = (
                 name, n, m, pc)
                if show_missing:
                    args = args + (readable,)
                print >> file, fmt_coverage % args
                total_statements = total_statements + n
                total_executed = total_executed + m
            except KeyboardInterrupt:
                raise
            except:
                if not ignore_errors:
                    type, msg = sys.exc_info()[0:2]
                    print >> file, fmt_err % (name, type, msg)

        if len(morfs) > 1:
            print >> file, '-' * len(header)
            if total_statements > 0:
                pc = 100.0 * total_executed / total_statements
            else:
                pc = 100.0
            args = (
             'TOTAL', total_statements, total_executed, pc)
            if show_missing:
                args = args + ('', )
            print >> file, fmt_coverage % args

    blank_re = re.compile('\\s*(#|$)')
    else_re = re.compile('\\s*else\\s*:\\s*(#|$)')

    def annotate(self, morfs, directory=None, ignore_errors=0, omit_prefixes=[]):
        morfs = self.filter_by_prefix(morfs, omit_prefixes)
        for morf in morfs:
            try:
                filename, statements, excluded, missing, _ = self.analysis2(morf)
                self.annotate_file(filename, statements, excluded, missing, directory)
            except KeyboardInterrupt:
                raise
            except:
                if not ignore_errors:
                    raise

    def annotate_file(self, filename, statements, excluded, missing, directory=None):
        source = open(filename, 'r')
        if directory:
            dest_file = os.path.join(directory, os.path.basename(filename) + ',cover')
        else:
            dest_file = filename + ',cover'
        dest = open(dest_file, 'w')
        lineno = 0
        i = 0
        j = 0
        covered = 1
        while 1:
            line = source.readline()
            if line == '':
                break
            lineno = lineno + 1
            while i < len(statements) and statements[i] < lineno:
                i = i + 1

            while j < len(missing) and missing[j] < lineno:
                j = j + 1

            if i < len(statements) and statements[i] == lineno:
                covered = j >= len(missing) or missing[j] > lineno
            if self.blank_re.match(line):
                dest.write('  ')
            elif self.else_re.match(line):
                if i >= len(statements) and j >= len(missing):
                    dest.write('! ')
                elif i >= len(statements) or j >= len(missing):
                    dest.write('> ')
                elif statements[i] == missing[j]:
                    dest.write('! ')
                else:
                    dest.write('> ')
            elif lineno in excluded:
                dest.write('- ')
            elif covered:
                dest.write('> ')
            else:
                dest.write('! ')
            dest.write(line)

        source.close()
        dest.close()


the_coverage = coverage()

def use_cache(*args, **kw):
    return the_coverage.use_cache(*args, **kw)


def start(*args, **kw):
    return the_coverage.start(*args, **kw)


def stop(*args, **kw):
    return the_coverage.stop(*args, **kw)


def erase(*args, **kw):
    return the_coverage.erase(*args, **kw)


def begin_recursive(*args, **kw):
    return the_coverage.begin_recursive(*args, **kw)


def end_recursive(*args, **kw):
    return the_coverage.end_recursive(*args, **kw)


def exclude(*args, **kw):
    return the_coverage.exclude(*args, **kw)


def analysis(*args, **kw):
    return the_coverage.analysis(*args, **kw)


def analysis2(*args, **kw):
    return the_coverage.analysis2(*args, **kw)


def report(*args, **kw):
    return the_coverage.report(*args, **kw)


def annotate(*args, **kw):
    return the_coverage.annotate(*args, **kw)


def annotate_file(*args, **kw):
    return the_coverage.annotate_file(*args, **kw)


try:
    import atexit
    atexit.register(the_coverage.save)
except ImportError:
    sys.exitfunc = the_coverage.save

if __name__ == '__main__':
    the_coverage.command_line(sys.argv[1:])
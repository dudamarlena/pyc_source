# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/pycount.py
# Compiled at: 2007-08-08 19:58:56
__doc__ = 'pycount.py -- A very initial effort to Python code metrics.\n\nThis program started as a hack, bending and twisting pylint.py \nby Tim Peters. At that time I was interested on code metrics\nand thought let\'s do something quick and dirty. pycount then\nand today scans a Python file and reports back various cate-\ngories of lines it thinks it has found, like comments, doc\nstrings, blank lines and, sometimes, real code as well.\n\nThe output can be either as a table with only the number of\nlines found for each file or as a listing of the file(s)\nprefixed with some running numbers and classification for\neach line.\n\nThe former is useful to scan a whole project e.g. when you\nneed to know if the project is documented well or at all and\nwhere this info can be found. The latter is at least a nice\nnew view to your own sources or that of others if nothing\nelse!\n\nThere are a couple of minor known bugs with pycount like:\nDoc strings must be tripple-quoted ones otherwise they are\nclassified as normal source code. Continuation lines ending\nwith a backslash are not treated at all. Complex regular ex-\npressions (as in pycount itself) can knock the parser down,\nquickly. There is a built-in quick-and-dirty solution to\nthis which might work whenever the problem is on one line\nonly. But in "most cases" it works...\n\nUsage::\n\n    pycount.py [-v] <file1> [<file2> ...]\n    pycount.py [-v] <expr>\n    pycount.py [-F] <linetypes> <file>\n    pycount.py [-R] <expr>\n\n    where <fileN>     is a Python file (usually ending in .py),\n          <linetypes> is a comma-seperated list of python line\n                      type codes (code, comment, doc string, blank)\n                      e.g. \'###\' or \'DOC,###,---\'\n          <expr>      is a shell expression with meta-characters\n                      (note that for -R you must quote it)\n          -v          verbose flag, listing the source\n          -F          filter flag, listing the filtered source\n          -R          apply recursively on subdirectories \n        \nTODO\n-----\n\n- Don\'t filter first line if \'#!<path> python\'(?).\n- De-obfuscate top-level if-stmt in main().\n- Improve usage as as a module.\n- Print statistics as percentage figures, maybe.\n- Write some test cases using pyunit.\n\nDONE\n----\n\n- Replace Unix \'find\' with Python os.path.walk / fnmatch.\n- Scanning should also work recursively (-R option).\n- Test stdin case for single files.\n- Return total count per category when run on multiple files.\n- Add a feature to uncomment files.\n\nHISTORY\n-------\n\n- 0.0.1   : 1997-??-?? : copy/past from Tim Peter\'s pylint\n- 0.0.2   : 1997-??-?? : included some refinements by Tim\n- 0.0.3   : 1997-07-22 : doc & (C) (borrowed from M.-A. Lemburg)\n- 0.0.4   : 1998-08-25 : replaced regex/regsub with re module,\n                         added a global line counter in -v mode\n- 0.0.5   : 1998-11-25 : code embellishments, recursive on files, ...\n- 0.0.6   : 2000-07-04 : fixed typos, improved doc\n\nFUTURE\n------\n\n- The future is always uncertain...\n\n-----------------------------------------------------------------------------\n\nCopyright by Dinu C. Gherman, 1998, gherman@europemail.com \n\n\tPermission to use, copy, modify, and distribute this software and its\n\tdocumentation without fee and for any purpose, except direct commerial \n\tadvantage, is hereby granted, provided that the above copyright notice \n\tappear in all copies and that both that copyright notice and this \n\tpermission notice appear in supporting documentation.\n\n\tTHE AUTHOR DINU C. GHERMAN DISCLAIMS ALL WARRANTIES WITH REGARD TO\n\tTHIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\n\tFITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,\n\tINDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING\n\tFROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\n\tNEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\n\tWITH THE USE OR PERFORMANCE OF THIS SOFTWARE!\n\n\tDinu C. Gherman,\n\n\t2000-07-04\n\n'
__version__ = (0, 0, 6)
import sys, os, re, string, getopt, fnmatch
_squote3_finder = re.compile("([^\\']|\\.|'[^\\']|'\\.|''[^\\']|''\\.)*'''")
_dquote3_finder = re.compile('([^\\"]|\\.|"[^\\"]|"\\.|""[^\\"]|""\\.)*"""')
_dquote1_finder = re.compile('"([^"]|\\.)*"')
_squote1_finder = re.compile("'([^']|\\.)*'")
_is_comment = re.compile('^[ \\t]*#').match
_is_blank = re.compile('^[ \\t]*$').match
_has_nightmare = re.compile('[\\"\'#]').search
_is_doc_candidate = re.compile('^[ \\t]*(\'\'\'|\\"\\"\\")')
del re
(doc_type, comment_type, cod_type, blank_type) = ('DOC', '###', 'COD', '---')

class Formatter:
    """Sort of a formatter class for filtering Python source code."""
    __module__ = __name__

    def __init__(self, showLineNums=1):
        """Init."""
        self.showLineNums = showLineNums
        self.showLineType = 0
        self.showLine = 0
        self.filterLineTypes = []

    def print_line(self, gnum, cnum, type, line):
        """Print a line, prefixed with some type and count information."""
        if self.filterLineTypes and type in self.filterLineTypes:
            return
        if self.filterLineTypes:
            print '%s' % line,
            return
        if self.showLineNums and self.showLineType:
            if self.showLine and not self.filterLineTypes:
                print '%5d %5d %3s %s' % (gnum, cnum, type, line),


def crunch(getline, filename, mode):
    """Parse the given file."""
    (is_blank, is_comment, has_nightmare, is_doc_candidate) = (
     _is_blank, _is_comment, _has_nightmare, _is_doc_candidate)
    quote3_finder = {'"': _dquote3_finder, "'": _squote3_finder}
    quote1_finder = {'"': _dquote1_finder, "'": _squote1_finder}
    from re import sub
    num_code = num_comment = num_blank = num_doc = num_ignored = 0
    in_doc = in_triple_quote = lineno = 0
    while 1:
        classified = 0
        lineno, line = lineno + 1, getline()
        if not line:
            break
        if in_triple_quote:
            if in_doc:
                num_doc = num_doc + 1
                mode.print_line(lineno, num_doc, doc_type, line)
            else:
                num_code = num_code + 1
                mode.print_line(lineno, num_code, cod_type, line)
            classified = 1
            m = in_triple_quote.match(line)
            if m == None:
                continue
            end = m.span()[1]
            line = line[end:]
            in_doc = in_triple_quote = 0
        if is_blank(line):
            if not classified:
                num_blank = num_blank + 1
                mode.print_line(lineno, num_blank, blank_type, line)
            continue
        if is_comment(line):
            if not classified:
                num_comment = num_comment + 1
                mode.print_line(lineno, num_comment, comment_type, line)
            continue
        if not classified:
            if is_doc_candidate.match(line):
                num_doc = num_doc + 1
                in_doc = 1
                mode.print_line(lineno, num_doc, doc_type, line)
            else:
                num_code = num_code + 1
                mode.print_line(lineno, num_code, cod_type, line)
        while 1:
            m = has_nightmare(line)
            if not m:
                break
            else:
                i = m.span()[0]
            ch = line[i]
            if ch == '#':
                break
            elif ch * 3 == line[i:i + 3]:
                in_triple_quote = quote3_finder[ch]
                m = in_triple_quote.match(line, i + 3)
                if m:
                    end = m.span()[1]
                    line = line[:i] + line[end:]
                    in_doc = in_triple_quote = 0
                else:
                    break
            else:
                prev_line = line[:]
                line = sub(quote1_finder[ch], ' ', line, 1)
                if prev_line == line:
                    line = ''

    answer = (
     lineno - 1, num_code, num_doc, num_comment, num_blank, filename)
    linenoSum = num_code + num_doc + num_comment + num_blank + 1 - num_ignored
    if lineno != linenoSum:
        reason = (
         'internal inconsistency in counts', lineno, answer)
        raise SystemError, reason
    return answer


def formatHeaderLine():
    format = '%8s%8s%8s%8s%8s  %s'
    return format % ('lines', 'code', 'doc', 'comment', 'blank', 'file')


def formatResultLine(resTuple):
    format = '%8s%8s%8s%8s%8s  %s'
    return format % resTuple


def collectFiles(listPatCwd, dirname, names):
    """Recursively add filenames matching a certain pattern to a list."""
    (list, pat, cwd) = listPatCwd
    l = len(cwd)
    for name in names:
        p = os.path.join(dirname, name)
        if os.path.isfile(p) and fnmatch.fnmatch(name, pat):
            list.append('.' + p[l:])


def main():
    allTuples = []
    all = [0, 0, 0, 0, 0]
    verbose = 0
    recursive = 0
    is_filtered = 0
    is_first = 1
    m = Formatter()
    (opts, args) = getopt.getopt(sys.argv[1:], 'vRF:')
    for (o, a) in opts:
        if o == '-v':
            m.showLineNums = 1
            m.showLineType = 1
            m.showLine = 1
        elif o == '-R':
            recursive = 1
        elif o == '-F':
            is_filtered = 1
            if string.find(a, ','):
                for t in string.split(a, ','):
                    m.filterLineTypes.append(t)

            else:
                m.filterLineTypes.append(a)

    if len(args) == 0:
        resTuple = crunch(sys.stdin.readline, '<stdin>', m)
        if is_first and not is_filtered:
            print formatHeaderLine()
        if not is_filtered:
            print formatResultLine(resTuple)
        return
    if recursive:
        pat, cwd = args[0], os.getcwd()
        args = []
        os.path.walk(cwd, collectFiles, (args, pat, cwd))
    for path in args:
        try:
            f = open(path, 'r')
        except IOError, details:
            print "couldn't open %s: %s" % (path, details)
        else:
            try:
                resTuple = crunch(f.readline, path, m)
                allTuples.append(resTuple)
                if is_first and not is_filtered:
                    print formatHeaderLine()
                if not is_filtered:
                    print formatResultLine(resTuple)
            finally:
                is_first = 0
                f.close()

    if len(args) > 1:
        for t in allTuples:
            for i in (0, 1, 2, 3, 4):
                all[i] = all[i] + t[i]

        all.append('total')
        print formatResultLine(tuple(all))


if __name__ == '__main__':
    main()
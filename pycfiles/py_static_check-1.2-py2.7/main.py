# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/py_static_check/main.py
# Compiled at: 2011-12-19 15:58:48
import sys, os, _ast, pyflakes, getopt
from modified_checker import Checker
STAR_IMPORTS = None
IGNORE_UNUSED_IMPORT = False

def check(codeString, filename):
    """
    Check the Python source given by C{codeString} for flakes.

    @param codeString: The Python source to check.
    @type codeString: C{str}

    @param filename: The name of the file the source came from, used to report
        errors.
    @type filename: C{str}

    @return: The number of warnings emitted.
    @rtype: C{list}
    """
    global STAR_IMPORTS
    try:
        tree = compile(codeString, filename, 'exec', _ast.PyCF_ONLY_AST)
    except SyntaxError as value:
        msg = value.args[0]
        lineno, offset, text = value.lineno, value.offset, value.text
        if text is None:
            print >> sys.stderr, '%s: problem decoding source' % (filename,)
        else:
            line = text.splitlines()[(-1)]
            if offset is not None:
                offset = offset - (len(text) - len(line))
            print >> sys.stderr, '%s:%d: %s' % (filename, lineno, msg)
            print >> sys.stderr, line
            if offset is not None:
                print >> sys.stderr, ' ' * offset, '^'
        return []

    w = Checker(tree, filename, STAR_IMPORTS)
    return w.messages
    return


def print_messages(messages):
    global IGNORE_UNUSED_IMPORT
    type_messages = {}
    for m in messages:
        str_type = str(type(m))
        if IGNORE_UNUSED_IMPORT:
            if 'UnusedImport' in str_type:
                continue
            if 'RedefinedWhileUnused' in str_type:
                continue
        lst = type_messages.setdefault(str_type, [])
        lst.append(m)

    sorted_by_type = {}
    for e_type, messages in type_messages.items():
        sort_tuple = ((m.filename, m.lineno, m) for m in messages)
        sorted_messages = (t[2] for t in sorted(sort_tuple))
        sorted_by_type[e_type] = sorted_messages

    types = sorted_by_type.keys()
    types.sort(reverse=True)
    for t in types:
        for w in sorted_by_type[t]:
            print w


def check_path(filename):
    return check(file(filename).read(), filename)


def usage():
    print 'py_static_check a Lint-like tool for Python. It is focused on identifying common errors quickly without executing Python code.'
    print 'py_static_check is based on pyflakes and offers some additioanl features such as handling of star imports.'
    print ''
    print 'Usage:'
    print '    py_static_check file.py directory/'
    print ''
    print 'Options:'
    print '    -h, --help: Displays this message'
    print '    -i, --ignore_unused_imports: Ignore unused imports warning'
    print '    -s, --star_imports: Define a Python file that resolves star imports'
    print '                        this file should export a dictionary (STAR_IMPORTS)'
    print '                        that maps from module_name to a list of names it exports, e.g.'
    print "                        STAR_IMPORTS = {'os': ['path', 'uname']}"
    sys.exit(2)


def run():
    global IGNORE_UNUSED_IMPORT
    global STAR_IMPORTS
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'his:', [
         'help', 'ignore_unused_imports', 'star_imports='])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-s', '--star_imports'):
            d = {}
            execfile(arg, d)
            star_imports = d.get('STAR_IMPORTS')
            if not star_imports:
                print '%s does not export STAR_IMPORTS!' % d
                sys.exit(-1)
            if type(star_imports) != type({}):
                print "%s's STAR_IMPORTS is not a dictionary!" % d
                sys.exit(-1)
            STAR_IMPORTS = d['STAR_IMPORTS']
        if opt in ('-i', '--ignore_unused_imports'):
            IGNORE_UNUSED_IMPORT = True

    messages = []
    if args:
        for arg in args:
            if os.path.isdir(arg):
                for dirpath, dirnames, filenames in os.walk(arg):
                    for filename in filenames:
                        if filename.endswith('.py'):
                            messages.extend(check_path(os.path.join(dirpath, filename)))

            else:
                messages.extend(check_path(arg))

    else:
        messages.extend(check(sys.stdin.read(), '<stdin>'))
    print_messages(messages)


if __name__ == '__main__':
    run()
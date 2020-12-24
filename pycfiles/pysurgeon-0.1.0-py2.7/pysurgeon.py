# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/pysurgeon.py
# Compiled at: 2018-07-26 23:39:37
import os, argparse, ast
DEBUG = False
NODE_TYPES = {ast.ClassDef: 'Class', 
   ast.FunctionDef: 'Function/Method', 
   ast.Module: 'Module'}

def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-f', '--filepath', dest='filepath', help='file to add docstring')
    required.add_argument('-c', '--configuration', dest='configuration', help='configuration file that contains docstring')
    parser.add_argument('-v', '--verbosity', dest='verbosity', action='store_true', help='if set, more verbose outputs will be printed')
    parser.add_argument('-a', '--append-changes', dest='append', action='store_true', help='if set, changes are saved into original source')
    args = parser.parse_args()
    DEBUG = args.verbosity
    man_options = [
     'filepath', 'configuration']
    for m in man_options:
        if not args.__dict__[m]:
            parser.print_help()
            return 1

    if not os.path.isfile(args.filepath):
        print "File doesn't exist. Exiting."
        return 1
    else:
        with open(args.filepath, 'r') as (f):
            source = f.read()
        with open(args.configuration, 'r') as (f):
            template = f.read()
        try:
            code = ast.parse(source)
        except SyntaxError:
            print 'File contains a syntatical error. Fix before running again'
            return 1

        no_docstring_lines = []
        for node in code.body:
            if isinstance(node, tuple(NODE_TYPES)):
                docstring = ast.get_docstring(node)
                if docstring is None:
                    lineno = getattr(node, 'lineno', None)
                    if DEBUG:
                        print ('\nFound node line no. with no docstring: {}').format(lineno)
                    no_docstring_lines.append(lineno)
                elif DEBUG and docstring is not None:
                    print ('\n\n{}').format(node.name)
                    print '------------------------------'
                    print ('Available Docstring:\n"{}"').format(docstring)

        if DEBUG:
            print ('\n\n{} nodes have no docstrings.').format(len(no_docstring_lines))
        with open(args.filepath, 'r') as (buf_file):
            buf = buf_file.readlines()
        i = 0
        for line in no_docstring_lines:
            buf.insert(line + i, template)
            i += 1

        if DEBUG:
            print '\n\n===================================='
            print 'Final docstring-linted code:\n'
            print ('').join(buf)
        if args.append:
            with open(args.filepath, 'w') as (f_write):
                f_write.write(('').join(buf))
        print '\nSuccess! Added docstrings to code'
        return 0


if __name__ == '__main__':
    main()
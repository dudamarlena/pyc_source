# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smartreplace/__init__.py
# Compiled at: 2019-01-16 08:08:01
import fnmatch, os, re, difflib, sys
from smartreplace.colors import bcolors

def user_input(text):
    print text,
    return sys.stdin.readline()


def colorize_diff(difftext):
    return ('\n').join([ bcolors.OKGREEN + line + bcolors.ENDC if line[0] == '+' else bcolors.FAIL + line + bcolors.ENDC if line[0] == '-' else line for line in difftext.splitlines()
                       ])


def _unidiff_output(expected, actual):
    return ('').join(difflib.unified_diff(expected.splitlines(1), actual.splitlines(1)))


def sreplace(regex, replacer, file_query='*.py'):
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, file_query):
            fname = os.path.join(root, filename)
            contents = open(fname).read()
            new_contents = re.sub(regex, replacer, contents)
            diff = _unidiff_output(contents, new_contents)
            if not diff:
                continue
            print colorize_diff(diff)
            ans = user_input(('[{}] Write? (y/n)').format(bcolors.OKGREEN + fname + bcolors.ENDC))
            if ans.strip().lower() == 'y':
                open(fname, 'w+').write(new_contents)
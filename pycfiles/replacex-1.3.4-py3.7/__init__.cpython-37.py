# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/replacex/__init__.py
# Compiled at: 2019-11-12 07:18:53
# Size of source mod 2**32: 1431 bytes
import os, re, sys

def replace(filename, original, updated):
    print('%s' % filename)
    fo = open(filename + '.bk', 'w')
    fo.write(original)
    fo.close()
    fi = open(filename, 'w')
    fi.write(updated)
    fi.close()
    os.remove(filename + '.bk')


def rep_folder(path, from_re, to_re, file_re):
    print('Current Path: {}'.format(path))
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            if re.search(file_re, filename):
                infile = os.path.join(dirpath, filename)
                try:
                    original = open(infile).read()
                    updated = re.sub(from_re, to_re, original, flags=(re.M))
                    if updated != original:
                        replace(infile, original, updated)
                except Exception as e:
                    try:
                        print('! Error when reading file {} with exception {}'.format(infile, e))
                    finally:
                        e = None
                        del e


def main():
    nums = len(sys.argv)
    if nums not in (3, 4):
        print('Usage: replacex FROM_REGEX TO_REGEX [FILENAME_REGEX]')
        exit()
    path = os.getcwd()
    from_regex = sys.argv[1]
    to_regex = sys.argv[2]
    filename_regex = '^[^.].*\\.(h|m|mm|md|cpp|java|yml|json|inl|def|txt|php|tpl|css|js|py|go)$' if nums == 3 else sys.argv[3]
    rep_folder(path, from_regex, to_regex, filename_regex)
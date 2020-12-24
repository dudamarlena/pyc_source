# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/djinter/lint.py
# Compiled at: 2014-05-07 07:40:36
import glob, os, re, sys
from djinter.utils import grep

def lint_migrations(path):
    results = []
    message = 'Possible import of app models in migration {filename}:\n{matches}'
    match_pattern = re.compile('from .+models import ')
    dont_match_pattern = re.compile('^\\s*\\#')
    for dirpath, dirnames, files in os.walk(path):
        for filename in glob.glob(os.path.join(dirpath, './migrations/*.py')):
            matches = grep(filename, match_pattern, dont_match_pattern)
            if matches:
                results.append({'severity': 'critical', 
                   'message': message.format(filename=filename, matches=matches)})

    return results


def lint_project(path):
    results = []
    results.extend(lint_migrations(path))
    return results
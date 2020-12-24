# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/bin/unique-messages.py
# Compiled at: 2018-07-11 18:15:30
import os, sys

def unique_messages():
    basedir = None
    if os.path.isdir(os.path.join('conf', 'locale')):
        basedir = os.path.abspath(os.path.join('conf', 'locale'))
    else:
        if os.path.isdir('locale'):
            basedir = os.path.abspath('locale')
        else:
            print 'This script should be run from the Django Git tree or your project or app tree.'
            sys.exit(1)
        for dirpath, dirnames, filenames in os.walk(basedir):
            for f in filenames:
                if f.endswith('.po'):
                    sys.stderr.write('processing file %s in %s\n' % (f, dirpath))
                    pf = os.path.splitext(os.path.join(dirpath, f))[0]
                    cmd = 'msguniq "%s.po"' % pf
                    stdout = os.popen(cmd)
                    msg = stdout.read()
                    with open('%s.po' % pf, 'w') as (fp):
                        fp.write(msg)

    return


if __name__ == '__main__':
    unique_messages()
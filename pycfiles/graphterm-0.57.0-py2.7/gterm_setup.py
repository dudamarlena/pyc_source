# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/gterm_setup.py
# Compiled at: 2014-05-09 14:09:59
import os, sys, about
BINDIR = 'bin'

def main():
    pkg_dir = os.path.dirname(__file__)
    for dirname in sys.path:
        if not dirname:
            continue
        if os.path.isfile(os.path.join(dirname, 'graphterm', '__init__.py')):
            pkg_dir = dirname
            break

    Exec_path = os.path.join(os.path.abspath(dirname), 'graphterm', BINDIR)
    try:
        for dirpath, dirnames, filenames in os.walk(Exec_path):
            for filename in filenames:
                if not filename.startswith('.') and not filename.endswith('.pyc'):
                    os.chmod(os.path.join(dirpath, filename), 493)

        print >> sys.stderr, 'COMPLETED gterm_setup for path', Exec_path
    except Exception as excp:
        pass

    try:
        profile_path = os.path.join(Exec_path, 'gprofile')
        profile_lines = '\n# Appended by GraphTerm %s installer\n[ -r %s ] && source %s\n' % (about.version, profile_path, profile_path)
        aliases_path = os.path.join(Exec_path, 'galiases')
        aliases_lines = '\n# Appended by GraphTerm %s installer\n[ -r %s ] && source %s\n' % (about.version, aliases_path, aliases_path)
        pfile, afile = ('', '')
        if os.geteuid():
            pfile = os.path.join(os.path.expanduser('~'), '.profile')
            afile = os.path.join(os.path.expanduser('~'), '.bashrc')
        else:
            if os.path.isfile('/etc/profile'):
                pfile = '/etc/profile'
            if os.path.isfile('/etc/bashrc'):
                afile = '/etc/bashrc'
            elif os.path.isfile('/etc/bash.bashrc'):
                afile = '/etc/bash.bashrc'
        if 0 and pfile:
            try:
                with open(pfile, 'a') as (f):
                    f.write(profile_lines)
                print >> sys.stderr, 'Appended shell environment setup to', pfile
            except Exception as excp:
                pass

        if 0 and afile:
            try:
                with open(afile, 'a') as (f):
                    f.write(aliases_lines)
                print >> sys.stderr, 'Appended shell aliases setup to', afile
            except Exception as excp:
                pass

    except Exception as excp:
        print >> sys.stderr, 'Error in updating shell setup', excp


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/cli/tfacctbak.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 1381 bytes
import sys, os.path
from messidge import default_location, KeyPair
bash_template = "echo 'mkdir -p ~/.20ft\ncat > ~/.20ft/%s << EOF\n%s\nEOF\ncat > ~/.20ft/%s.pub << EOF\n%s\nEOF\ncat > ~/.20ft/%s.spub << EOF\n%s\nEOF\ncat > ~/.20ft/default_location << EOF\n%s\nEOF\n\nchmod 400 ~/.20ft/%s*' | /bin/sh\n"

def main():
    loc = default_location(prefix='~/.20ft') if len(sys.argv) == 1 else sys.argv[1]
    kp = KeyPair(loc, prefix='~/.20ft')
    with open(os.path.expanduser('~/.20ft/%s.spub' % loc)) as (f):
        spub = f.read()
    print(bash_template % (loc, kp.secret.decode(), loc, kp.public.decode(), loc, spub, loc, loc))


if __name__ == '__main__':
    main()
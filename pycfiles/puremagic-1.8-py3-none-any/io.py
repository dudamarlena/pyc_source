# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/envs/purelyjs/lib/python2.7/site-packages/purelyjs/io.py
# Compiled at: 2014-04-27 15:28:58
import fnmatch, os, subprocess, sys

def expand_patterns(patterns):
    files = []
    for pattern in patterns:
        dir, pat = os.path.split(pattern)
        dir = dir if dir else '.'
        fs = os.listdir(dir)
        fs = fnmatch.filter(fs, pat)
        fs = [ os.path.join(dir, f) for f in fs ]
        files.extend(fs)

    return files


def invoke(args, cwd=None):
    popen = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = popen.communicate()
    out = out.strip()
    err = err.strip()
    ret = popen.returncode
    return (
     ret == 0, out, err)


def write(line):
    sys.stderr.write(line)
    sys.stderr.flush()


def writeln(line=''):
    if not line.endswith('\n'):
        line = '%s\n' % line
    write(line)
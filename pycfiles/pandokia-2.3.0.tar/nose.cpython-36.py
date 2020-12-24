# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/runners/nose.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 2427 bytes
import os

def command(env):
    return 'pdknose --pdk --with-doctest --doctest-tests %(PDK_FILE)s' % env


def lst(env):
    import pandokia.helpers.process as process, pandokia.helpers.filecomp as filecomp
    tmpfile = 'pdk.runner.tmp'
    try:
        os.unlink(tmpfile)
    except OSError:
        pass

    s = 'pdknose --pdk --with-doctest --doctest-tests --collect-only %(PDK_FILE)s' % env
    env = env.copy()
    env['PDK_LOG'] = tmpfile
    process.run_process((s.split()), env, output_file='pdknose.tmp')
    l = []
    f = open(tmpfile, 'r')
    for line in f:
        line = line.strip().split('=')
        if line[0] == 'test_name':
            l.append(line[1])

    f.close()
    filecomp.safe_rm('pdknose.tmp')
    filecomp.safe_rm(tmpfile)
    return l
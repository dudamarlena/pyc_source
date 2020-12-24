# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/data/runner.py
# Compiled at: 2015-09-24 08:42:53
if __name__ == '__main__':
    import sys, subprocess, shlex
    cmdfile = sys.argv[1]
    errfile = sys.argv[2]
    resfile = sys.argv[3]
    cmdline = open(cmdfile).read()
    errfh = open(errfile, 'w')
    resfh = open(resfile, 'w')
    result = subprocess.call(shlex.split(cmdline), shell=False, stdout=resfh, stderr=errfh)
    errfh.close()
    resfh.close()
    errfh = open(errfile, 'r')
    err = errfh.read()
    errfh.close()
    res = None
    if result == 0 and err.strip() != 'OK':
        res = 'OK'
    if result != 0 and err == '':
        res = 'ERROR: %d' % result
    if res != None:
        errfh = open(errfile, 'w')
        errfh.write(res)
        errfh.close()
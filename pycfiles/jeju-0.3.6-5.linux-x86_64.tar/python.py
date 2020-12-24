# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jeju/executor/python.py
# Compiled at: 2016-11-09 20:33:52
import subprocess, string, uuid, logging, sys, jeju
TEMP_DIR = '/tmp'

def replaceable(code, kv):
    keys = kv.keys()
    for key in keys:
        nkey = '${%s}' % key
        code = string.replace(code, nkey, kv[key])

    logging.debug('####################' + '\n%s' % code)
    logging.debug('####################')
    return code


def execute_python(**kwargs):
    code = kwargs['code']
    kv = kwargs['kv']
    import os
    rcode = replaceable(code, kv)
    temp = uuid.uuid1()
    temp_file = '%s/%s' % (TEMP_DIR, str(temp))
    fp = open(temp_file, 'w')
    fp.write(rcode)
    fp.close()
    print jeju.__logging__
    cmd2 = 'python %s' % temp_file
    if jeju.__logging__ == 'file':
        proc = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
        out = ''
        while proc.poll() is None:
            line = proc.stdout.readline()
            print line
            out = out + line

    else:
        proc = subprocess.Popen(cmd2, shell=True)
        out, err = proc.communicate()
        out = '#### Displayed by Console ####'
    os.remove(temp_file)
    return {'input': rcode, 'output': out, 'error': err}
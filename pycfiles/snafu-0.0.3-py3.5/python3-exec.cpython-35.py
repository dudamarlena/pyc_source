# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/python3-exec.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1225 bytes
import sys, os, time, json, base64, pickle

class Context:

    def __init__(self):
        self.SnafuContext = self


def execute(filename, func, funcargs, envvars):
    funcargs = json.loads(funcargs)
    envvars = json.loads(envvars)
    for i, funcarg in enumerate(funcargs):
        if type(funcarg) == str and funcarg.startswith('pickle:'):
            sys.modules['lib'] = Context()
            sys.modules['lib.snafu'] = Context()
            funcarg = None

    sys.path.append('.')
    os.chdir(os.path.dirname(filename))
    mod = __import__(os.path.basename(filename[:-3]))
    func = getattr(mod, func)
    for envvar in envvars:
        os.environ[envvar] = envvars[envvar]

    stime = time.time()
    try:
        res = func(*funcargs)
        success = True
    except Exception as e:
        res = e
        success = False

    dtime = (time.time() - stime) * 1000
    return '{} {} {}'.format(dtime, success, '{}'.format(res).replace("'", '"'))


print(execute(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
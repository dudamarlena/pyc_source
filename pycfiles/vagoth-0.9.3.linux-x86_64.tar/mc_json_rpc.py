# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/virt/utils/mc_json_rpc.py
# Compiled at: 2013-10-03 03:30:30
from subprocess import Popen, PIPE
from os.path import abspath, dirname, join
import json

class MCollectiveException(Exception):
    pass


def mcollective_call(agent, action, identity=None, timeout=None, **kwargs):
    mcdict = {'agent': agent, 
       'action': action, 
       'arguments': kwargs}
    if identity is not None:
        mcdict['identity'] = identity
    if timeout is not None:
        mcdict['timeout'] = timeout
    mcjson = json.dumps(mcdict)
    ruby_script = join(abspath(dirname(__file__)), 'mc_json_rpc.rb')
    process = Popen([ruby_script, '-'], stdin=PIPE, stdout=PIPE)
    process.stdin.write(mcjson)
    process.stdin.close()
    result = process.stdout.read()
    process.stdout.close()
    process.wait()
    if process.returncode == 0:
        return json.loads(result)
    else:
        raise MCollectiveException(('mc-json-rpc.rb exited with {0}: {1}').format(process.returncode, result))
        return
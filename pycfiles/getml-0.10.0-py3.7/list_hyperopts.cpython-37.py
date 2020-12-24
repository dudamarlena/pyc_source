# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/hyperopt/list_hyperopts.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 2087 bytes
import getml.communication as comm

def list_hyperopts():
    """Get a list of the session_names of all hyperparameter optimization
    sessions started in the current project.

    Return:
        List[str]: all session names

    """
    print('Not supported yet!')
    return
    json_str = comm.recv_string(sock)
    sock.close()
    return json.loads(json_str)
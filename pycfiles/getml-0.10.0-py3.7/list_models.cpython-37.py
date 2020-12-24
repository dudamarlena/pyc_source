# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/list_models.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 2738 bytes
import json
import getml.communication as comm

def list_models():
    """Lists all models present in the engine.

    Note that this function only lists models which are part of the
    current project. See :func:`~getml.engine.set_project` for
    changing projects and :mod:`~getml.models` for more details about
    the lifecycles of the models.

    To subsequently load one of them, use
    :func:`~getml.models.load_model`.

    Raises:
        IOError: If command could not be processed by the engine.

    Returns:
        dict: 
            Containing two fields.

            * 'multirel_models'
                Lists all models corresponding to the
                :class:`~getml.models.MultirelModel` handler.
            * 'relboost_models'
                Lists all models corresponding to the
                :class:`~getml.models.RelboostModel` handler.

    """
    cmd = dict()
    cmd['type_'] = 'list_models'
    cmd['name_'] = ''
    sock = comm.send_and_receive_socket(cmd)
    msg = comm.recv_string(sock)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)
    json_str = comm.recv_string(sock)
    sock.close()
    return json.loads(json_str)
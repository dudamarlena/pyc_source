# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/core/reprocessing.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2308 bytes
"""some utils function for executing reprocessing"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/18/2019'
import importlib, logging
_logger = logging.getLogger(__name__)

def get_process_instance_frm_h5_desc(desc):
    """
    
    :param dict desc: description of the process to instanciate
    :return: instance of the process to execute, configured from the description
    """
    assert 'program' in desc
    assert 'class_instance' in desc
    tmp = str(desc['class_instance']).split('.')
    module_name = '.'.join(tmp[:-1])
    class_name = tmp[(-1)]
    try:
        _module = importlib.import_module(module_name)
        instance = getattr(_module, class_name)()
    except Exception as e:
        try:
            _logger.warning(' '.join(('Fail to instanciate', module_name, class_name,
             'reason is', e)))
            instance = None
        finally:
            e = None
            del e

    else:
        if 'configuration' in desc:
            instance.setConfiguration(desc['configuration'])
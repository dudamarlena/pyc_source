# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflow/main.py
# Compiled at: 2019-09-23 10:35:46
# Size of source mod 2**32: 1730 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/24/2019'
import logging
from scheme.scheme import Scheme
_logger = logging.getLogger(__name__)

def exec_(scheme, input_=None):
    """

    :param Scheme scheme: 
    :param input_: workflow input if any
    """
    assert isinstance(scheme, Scheme)
    scheme._start_actor.trigger(input_)
    scheme._end_actor.join()
    return scheme._end_actor.outData
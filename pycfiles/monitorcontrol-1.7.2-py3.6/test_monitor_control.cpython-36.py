# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/test_monitor_control/test_monitor_control.py
# Compiled at: 2019-11-29 22:50:00
# Size of source mod 2**32: 5118 bytes
import pytest
from unittest.mock import patch
from typing import Tuple, Union, Type, List, Iterable
from .. import vcp
from ..monitor_control import Monitor, get_vcps, get_monitors, iterate_monitors
USE_ATTACHED_MONITORS = False

class UnitTestVCP(vcp.VCP):

    def __init__(self, vcp_dict):
        self.vcp = vcp_dict

    def open(self):
        pass

    def close(self):
        pass

    def set_vcp_feature(self, code: int, value: int):
        self.vcp[code]['current'] = value

    def get_vcp_feature(self, code: int) -> Tuple[(int, int)]:
        return (self.vcp[code]['current'], self.vcp[code]['maximum'])


def test_get_vcps():
    get_vcps()
    with patch('sys.platform', 'darwin'):
        with pytest.raises(NotImplementedError):
            get_vcps()


def test_get_monitors():
    get_monitors()


def test_iterate_monitors():
    iterate_monitors()


def get_test_vcps() -> List[Type[vcp.VCP]]:
    if USE_ATTACHED_MONITORS:
        return get_vcps()
    else:
        unit_test_vcp_dict = {16:{'current':50, 
          'maximum':100}, 
         214:{'current':1, 
          'maximum':5}}
        return [
         UnitTestVCP(unit_test_vcp_dict)]


@pytest.fixture(scope='module', params=(get_test_vcps()))
def monitor(request) -> Iterable[Monitor]:
    monitor = Monitor(request.param)
    monitor.open()
    yield monitor
    monitor.close()


def test_get_code_maximum_type_error(monitor: Monitor):
    code = vcp.get_vcp_code_definition('image_factory_default')
    with pytest.raises(TypeError):
        monitor._get_code_maximum(code)


def test_set_vcp_feature_type_error(monitor: Monitor):
    code = vcp.get_vcp_code_definition('active_control')
    with pytest.raises(TypeError):
        monitor._set_vcp_feature(code, 1)


def test_get_vcp_feature_type_error(monitor: Monitor):
    code = vcp.get_vcp_code_definition('image_factory_default')
    with pytest.raises(TypeError):
        monitor._get_vcp_feature(code)


@pytest.mark.parametrize('luminance, expected', [(100, 100), (0, 0), (50, 50), (101, ValueError)])
def test_luminance(monitor: Monitor, luminance: int, expected: Union[(int, Type[Exception])]):
    original = monitor.luminance
    try:
        if isinstance(expected, int):
            monitor.luminance = luminance
            assert monitor.luminance == expected
        else:
            if isinstance(expected, type(Exception)):
                with pytest.raises(expected):
                    monitor.luminance = luminance
    finally:
        monitor.luminance = original


@pytest.mark.skipif(USE_ATTACHED_MONITORS,
  reason='not going to turn off your monitors')
@pytest.mark.parametrize('mode, expected', [
 ('on', 1),
 (1, 1),
 (
  'INVALID', KeyError),
 (
  [
   'on'], TypeError),
 (
  0, ValueError),
 (
  6, ValueError),
 ('standby', 2),
 ('suspend', 3),
 ('off_soft', 4),
 ('off_hard', 5)])
def test_get_power_mode--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'expected'
                4  LOAD_GLOBAL              int
                6  LOAD_GLOBAL              str
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_FALSE    72  'to 72'

 L. 148        14  LOAD_FAST                'mode'
               16  LOAD_FAST                'monitor'
               18  STORE_ATTR               power_mode

 L. 149        20  LOAD_FAST                'monitor'
               22  LOAD_ATTR                power_mode
               24  STORE_FAST               'power_mode'

 L. 150        26  LOAD_FAST                'expected'
               28  LOAD_CONST               1
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_FALSE    56  'to 56'

 L. 153        34  LOAD_FAST                'power_mode'
               36  LOAD_FAST                'expected'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_TRUE     70  'to 70'
               42  LOAD_FAST                'power_mode'
               44  LOAD_CONST               0
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_TRUE     70  'to 70'
               50  LOAD_ASSERT              AssertionError
               52  RAISE_VARARGS_1       1  'exception'
               54  JUMP_ABSOLUTE       114  'to 114'
               56  ELSE                     '70'

 L. 155        56  LOAD_FAST                'monitor'
               58  LOAD_ATTR                power_mode
               60  LOAD_FAST                'expected'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_TRUE    114  'to 114'
               66  LOAD_GLOBAL              AssertionError
               68  RAISE_VARARGS_1       1  'exception'
             70_0  COME_FROM            48  '48'
             70_1  COME_FROM            40  '40'
               70  JUMP_FORWARD        114  'to 114'
               72  ELSE                     '114'

 L. 156        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'expected'
               76  LOAD_GLOBAL              type
               78  LOAD_GLOBAL              Exception
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  POP_JUMP_IF_FALSE   114  'to 114'

 L. 157        86  LOAD_GLOBAL              pytest
               88  LOAD_ATTR                raises
               90  LOAD_FAST                'expected'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  SETUP_WITH          108  'to 108'
               96  POP_TOP          

 L. 158        98  LOAD_FAST                'mode'
              100  LOAD_FAST                'monitor'
              102  STORE_ATTR               power_mode
              104  POP_BLOCK        
              106  LOAD_CONST               None
            108_0  COME_FROM_WITH       94  '94'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      
            114_0  COME_FROM            84  '84'
            114_1  COME_FROM            70  '70'
            114_2  COME_FROM            64  '64'

Parse error at or near `COME_FROM' instruction at offset 114_1


def test_context_manager(monitor: Monitor):
    monitor.close()
    with monitor:
        pass
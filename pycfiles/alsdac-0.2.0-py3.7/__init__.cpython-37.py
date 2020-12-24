# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alsdac/__init__.py
# Compiled at: 2018-10-04 11:12:23
# Size of source mod 2**32: 8296 bytes
import sys, trio
from typing import Union, Tuple, List
import numpy as np, re
from operator import itemgetter, mul
from functools import reduce, wraps
import os
PORT = 55000
BUFSIZE = 163840
RECEIVE_ENCODING = 'ascii'
SEND_ENCODING = 'ascii'
SERVER_ADDRESS = '131.243.163.42'
READ_ONLY = os.environ.get('ALSDAC_READ_ONLY', True)

def set_server_address(host):
    global SERVER_ADDRESS
    SERVER_ADDRESS = host


def set_port(port):
    global PORT
    PORT = port


def stream_size(b):
    m = re.match(b'(?P<_0>\\d*) Points by (?P<_1>\\d*) channels', b)
    if m:
        map(itemgetter(1), sorted(m.groupdict().items()))
        return map(int, m.groups())
    return (None, None)


def get(data: str, SEND_ENCODING=SEND_ENCODING, RECEIVE_ENCODING=RECEIVE_ENCODING) -> bytes:
    """
    Starts sender and receiver asynchronous sockets. The sender sends a tcp/ip command to the LabView host system. The
    receiver waits to receive a response.

    """

    async def _get(data):
        result = None

        async def sender(client_sock, data):
            print('sent:', data.strip())
            await client_sock.send_all(bytes(data, SEND_ENCODING))

        async def receiver(client_sock):
            nonlocal result
            _data = await client_sock.receive_some(BUFSIZE)
            expcols, exprows = stream_size(_data)
            if exprows:
                if expcols:
                    while not _data.endswith(b'\r\n\r\n'):
                        _data += await client_sock.receive_some(BUFSIZE)

            if not data:
                sys.exit()
            result = _data
            if RECEIVE_ENCODING:
                print('received:', str(_data, RECEIVE_ENCODING).strip())

        with trio.socket.socket() as (client_sock):
            await client_sock.connect((SERVER_ADDRESS, PORT))
            client_sock = trio.SocketStream(client_sock)
            async with trio.open_nursery() as nursery:
                nursery.start_soon(sender, client_sock, data)
                nursery.start_soon(receiver, client_sock)
        return result

    return trio.run(_get, data)


def write_required(func):

    @wraps(func)
    def execute_if_write_permitted(*args, **kwargs):
        if READ_ONLY:
            raise PermissionError('Write access is disabled by default to prevent mishaps.\nTo enable write access set alsdac.READ_ONLY = False')
        else:
            return func(*args, **kwargs)

    return execute_if_write_permitted


def AtPreset(presetname: str) -> bool:
    return bool(get(f"AtPreset({presetname})\r\n"))


def AtTrajectory(trajname: str) -> bool:
    return bool(get(f"AtTrajectory({trajname})\r\n"))


@write_required
def DisableMotor(motorname: str) -> bool:
    return bool(get(f"DisableMotor({motorname})\r\n"))


@write_required
def EnableMotor(motorname: str) -> bool:
    return bool(get(f"EnableMotor({motorname})\r\n"))


def GetMotor(motorname: str):
    pos, hex, datetime = get(f"GetMotor({motorname})\r\n").split(b' ', 2)
    pos = float(pos)
    hex = str(hex, RECEIVE_ENCODING)
    datetime = str(datetime, RECEIVE_ENCODING)
    return (pos, hex, datetime)


def GetMotorPos(motorname: str) -> float:
    return float(get(f"GetMotorPos({motorname})\r\n"))


def GetMotorStatus(motorname: str) -> bool:
    return get(f"GetMotorStat({motorname})\r\n").startswith(b'Move finished')


def GetSoftLimits(motorname: str) -> Tuple[(float, float)]:
    return tuple(map(float, get(f"GetSoftLimits({motorname})\r\n").split(b' ')))[:2]


def GetFlyingPositions(motorname: str) -> str:
    return np.frombuffer((get(f"GetFlyingPositions({motorname})\r\n").strip()), dtype=(np.single))


def ListMotors() -> List[str]:
    return str(get('ListMotors\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


def ListPresets() -> List[str]:
    return str(get('ListPresets\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


def ListTrajectories() -> List[str]:
    return str(get('ListTrajectories\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


def NumberMotors() -> int:
    return int(get('NumberMotors\r\n'))


@write_required
def MoveMotor(motorname: str, pos: Union[(float, int)]) -> bool:
    return bool(get(f"MoveMotor({motorname}, {pos})\r\n"))


@write_required
def StopMotor(motorname: str):
    return get(f"StopMotor({motorname})\r\n") == b'Motor Stopped\r\n'


@write_required
def HomeMotor(motorname: str):
    return get(f"HomeMotor({motorname})\r\n") == b'OK!0 \r\n'


@write_required
def MoveToPreset(presetname: str) -> bool:
    return bool(get(f"MoveToPreset({presetname})\r\n"))


@write_required
def MoveToTrajectory(trajname: str) -> bool:
    return bool(get(f"MoveToTrajectory({trajname})\r\n"))


@write_required
def SetBreakpoints(motorname: str, first_bp: float, bp_step: float, num_points: int):
    return get(f"SetBreakpoints({motorname}, {first_bp}, {bp_step}, {num_points})\r\n")


@write_required
def DisableBreakpoints(motorname: str) -> bool:
    return bool(get(f"DisableBreakpoints({motorname})\r\n"))


def GetMotorVelocity(motorname: str) -> float:
    return float(get(f"GetMotorVelocity({motorname})\r\n"))


def GetOrigMotorVelocity(motorname: str) -> float:
    return float(get(f"GetOrigMotorVelocity({motorname})\r\n"))


@write_required
def SetMotorVelocity(motorname: str, vel: float) -> float:
    return float(get(f"GetMotorVelocity({motorname}, {vel})\r\n"))


def GetFreerun(ainame) -> float:
    return float(get(f"GetFreerun({ainame})\r\n"))


def ListAIs() -> List[str]:
    return str(get('ListAIs\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


def ListDIOs() -> List[str]:
    return str(get('ListDIOs\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


@write_required
def StartAcquire(time: float, counts: int):
    return bool(get(f"StartAcquire({time},{counts}\r\n"))


def GetInstrumentStatus(instrumentname) -> List[str]:
    return str(get(f"GetInstrumentStatus({instrumentname})\r\n"), RECEIVE_ENCODING).strip().split('\r\n')


def ListInstruments() -> List[str]:
    return str(get('ListInstruments\r\n'), RECEIVE_ENCODING).strip().split('\r\n')


@write_required
def StartInstrumentAcquire(instrumentname, time):
    return str(get(f"StartInstrumentAcquire({instrumentname}, {time})\r\n"))


def GetInstrumentAcquired1D(instrumentname):
    return str(get(f"GetInstrumentAcquired1D({instrumentname})\r\n"))


def GetInstrumentAcquired2D(instrumentname):
    b = get(f"GetInstrumentAcquired2D({instrumentname})\r\n")
    expcols, exprows = stream_size(b)
    s = str(b, RECEIVE_ENCODING)
    arr = np.fromstring((s.split('\r\n', maxsplit=1)[1].replace('\r\n', '\t')), count=(expcols * exprows), sep='\t', dtype=int)
    return arr.reshape((exprows, expcols))


def GetInstrumentAcquired2DBinary(instrumentname):
    b = get(f"GetInstrumentAcquired2DBinary({instrumentname})\r\n", RECEIVE_ENCODING='')
    expcols, exprows = stream_size(b)
    s = str(b, RECEIVE_ENCODING)
    return b


def GetInstrumentAcquired3D(instrumentname):
    return str(get(f"GetInstrumentAcquired3D({instrumentname})\r\n"))
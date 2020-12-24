# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyosci/commands.py
# Compiled at: 2017-02-16 04:14:43
# Size of source mod 2**32: 5782 bytes
"""
A namespace for oscilloscope string commands. The commands are send as ASCII
to the scope using a socket connection
"""
query = lambda cmd: cmd + '?'

def add_arg(cmd, arg):
    """
    Add an argument to a command string. Concat the two.

    Args:
        cmd (str): The base command
        arg (str): An argument

    Returns:
        str
    """
    if not isinstance(arg, str):
        arg = str(arg)
    if len(cmd.split()) != 1:
        cmd = cmd + ',' + arg
    else:
        cmd = cmd + ' ' + arg
    return cmd


def concat(*cmd):
    """
    Combine several commands

    Args:
        cmd: list of commands

    Returns:
        str
    """
    cmd = list(cmd)
    cmd[0].replace(':', '')
    concated = cmd[0] + ';'
    cmd.remove(cmd[0])
    for c in cmd:
        concated += ':' + str(c) + '; '

    return concated


def clean_response(response):
    """
    Remove some EOL remainders from the resulting scope response

    Args:
        response (str): response from the scope

    Returns:
        str
    """
    response = response.replace('\r\n>', '')
    response = response.replace('\r\n', '')
    response = response.replace('\n\r', '')
    response = response.replace('>', '')
    response = response.replace('<', '')
    response = response.replace('\n', '')
    return response


def parse_curve_data(header, curve):
    """
    Make sense out of that what is returned by CURVE. This works only
    if the scope is set to return the data in ASCII, not binary.

    Args:
        header (dict): a parsed header
        curv (str): returned by CURVE?

    Returns:
        tuple: np.ndarray xs, np.ndarray values
    """
    curve.replace('#', '')


def histbox_coordinates(left, top, right, bottom):
    """
    Create a string for the box coordinates for the
    histogram set up by the scope itself. The result
    can be send to the scope to set the box.

    Args:
        left (int):
        top (int):
        right (int):
        bottom (int):

    Returns:
        str
    """
    command = concat([left, top, right, bottom])
    return command


WHOAMI = '*IDN?'
SOURCE = 'DATa:SOUrce'
DATA_START = 'DATa:STARt'
DATA_STOP = 'DATa:STOP'
DATA_STARTQ = query(DATA_START)
DATA_STOPQ = query(DATA_STOP)
SOURCEQ = query(SOURCE)
HISTSTART = 'HIStogram:STARt'
HISTEND = 'HIStogram:END'
HISTDATA = 'HIStogram:DATa?'
WAVEFORM = 'WAVFrm?'
CURVE = 'CURVe?'
WF_OUTPREQ = 'WFMOutre?'
WF_XINCRQ = 'WFMOutpre:XINcr?'
WF_XUNITQ = 'WFMOutpre:XUNit?'
WF_XZEROQ = 'WFMOutpre:XZEro?'
WF_YOFFQ = 'WFMOutpre:YOFf?'
WF_YZEROQ = 'WFMOutpre:YZEro?'
WF_YMULTQ = 'WFMOutpre:YMUlt?'
WF_YUNITQ = 'WFMOutpre:YUNit?'
WF_ENC = 'WFMOutpre:ENCdg'
WF_ENCQ = query(WF_ENC)
WF_NPOINTS = 'WFMOutpre:NR_Pt'
WF_NPOINTSQ = query(WF_NPOINTS)
ACQUIRE = 'ACQuire'
ACQUIRE_FAST_STATE = 'ACQuire:FASTAcq:STATE'
ACQUIRE_MAX_SAMPLERATEQ = 'ACQuire:MAXSamplerate?'
RUN = 'ACQuire:STATE'
WF_BYTQ = 'WFMOutpre:BYT_Nr?'
ACQUIRE_STOP = 'ACQuire:STOPAfter'
HISTBOX = 'HIStogram:BOX'
TRG_RATEQ = 'TRIGger:FREQuency?'
RUN_CONTINOUS = 'RUNSTop'
RUN_SINGLE = 'SEQ'
START_ACQUISITIONS = 'RUN'
STOP_ACQUISITIONS = 'STOP'
N_ACQUISITIONS = 'ACQuire:NUMACq?'
ACQUIRE_ONE = 'ON'
SNAP = 'SNAP'
DATA = 'DATA'
OFF = '0'
ON = '1'
ASCII = 'ASCii'
BINARY = 'BINary'
SINGLE_ACQUIRE = '1'

class TektronixDPO4104BCommands(object):
    __doc__ = '\n    Namespace for the commands for the TektronixDP04104B\n    '
    WF_HEADER = concat(WF_BYTQ, WF_ENCQ, WF_NPOINTSQ, WF_XZEROQ, WF_XINCRQ, WF_YZEROQ, WF_YOFFQ, WF_YMULTQ, WF_XUNITQ, WF_YUNITQ)
    CH1 = 'CH1'
    CH2 = 'CH2'
    CH3 = 'CH3'
    CH4 = 'CH4'
    ON = 'ON'
    OFF = 'OFF'
    ONE = '1'
    ZERO = '0'
    TRIGGER_FREQUENCY_ENABLED = 'DISplay:TRIGFrequency'
    TRIGGER_FREQUENCYQ = 'TRIGger:FREQuency?'
    ACQUISITON_MODE = 'ACQuire:STOPAfter'


class RhodeSchwarzRTO1044Commands(object):
    __doc__ = '\n    Namespace for the commands for the RhodeSchwarz oscilloscope\n    '
    CH1 = 'CHAN1'
    CH2 = 'CHAN2'
    CH3 = 'CHAN3'
    CH4 = 'CHAN4'
    WAVEFORM = 'DATA?'
    WF_HEADER = 'DATA:HEADer?'
    CURVE = 'DATA:VALues?'


class KeysightE3631APowerSupplyCommands(object):
    __doc__ = '\n    Namespace for the commands of the KeysightE3631APowerSupply\n    '
    ERROR_STATEQ = 'SYST:ERR?'
    OUTPUT = 'OUTPUT:STATE'
    ON = 'ON'
    OFF = 'OFF'
    P6 = 'P6V'
    P25 = 'P25V'
    N25 = 'N25V'
    APPLY = 'APPLY'
    CHANNEL = 'INST'
    VOLT = 'VOLT'
    MEASURE = 'MEASURE'
    CURRENT = 'CURRENT'
    DC = 'DC'
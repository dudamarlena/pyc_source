# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/l0/ss9rqt5j7xbg0x2bpvmjx_k40000gp/T/pip-install-n2xwwglt/workstation/workstation/server/helpers.py
# Compiled at: 2019-09-24 08:15:55
# Size of source mod 2**32: 1348 bytes
import json, sys, traceback
JSON_ERROR = None
if sys.version_info > (3, 4):
    JSON_ERROR = ValueError
else:
    JSON_ERROR = json.decoder.JSONDecodeError

def get_frozen_root():
    """
    :return: Returns app path when app is packaged by pyInstaller
    """
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS


def run_protocol(robot, code: str, mode='simulate') -> tuple:
    """
    :param robot: robot instance for protocol
    :param code: str of protocol
    :return:
    """
    robot.set_connection(mode)
    exception_msg = ''
    commands = []
    try:
        try:
            robot.reset()
            robot.app_run_mode = True
            exec(code, globals())
            commands = robot._commands
        except Exception as e:
            try:
                stop_exc_msg = 'Received a STOP signal and exited from movements'
                if not (e.args and e.args[0] == stop_exc_msg):
                    exception_msg = 'Error in: ' + traceback.format_exc()
            finally:
                e = None
                del e

    finally:
        robot.app_run_mode = False

    robot.set_connection('live')
    return (commands, exception_msg)


def timestamp(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d:%02d:%02d' % (hours, minutes, seconds)
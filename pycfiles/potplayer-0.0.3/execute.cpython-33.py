# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\shu\Documents\PythonWorkSpace\py3\py33_projects\potplayer-project\potplayer\execute.py
# Compiled at: 2016-10-03 17:18:57
# Size of source mod 2**32: 1657 bytes
import os, site, subprocess
EXECUTABLE_PATH = None

def find_executable():
    """Automatically find PotPlayer executable file path and process name.
    It depends on your system.
    """
    x86 = 'C:\\Program Files (x86)\\DAUM\\PotPlayer\\PotPlayerMini.exe'
    x64 = 'C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe'
    if os.path.exists(x86):
        return (x86, os.path.basename(x86))
    if os.path.exists(x64):
        return (x64, os.path.basename(x64))
    try:
        process_name = os.path.basename(EXECUTABLE_PATH)
        if process_name not in ('PotPlayerMini.exe', 'PotPlayerMini64.exe'):
            raise ValueError("Cannot find potplayer executable! Please edit '%s' to add the valid path.")
        return (EXECUTABLE_PATH, process_name)
    except:
        raise ValueError("Cannot find potplayer executable! Please edit '%s' to add the valid path.")


def run(path):
    """Open a playlist/a video/a audio/a image with PotPlayer.
    Python will pause while potplayer is playing.
    """
    executable, _ = find_executable()
    abspath = os.path.abspath(path)
    subprocess.Popen('"%s" "%s"' % (executable, abspath))


def kill():
    """Kill PotPlayer. Find the subprocess in task manager and kill it.
    """
    _, process_name = find_executable()
    subprocess.call('TASKKILL /F /IM %s' % process_name)
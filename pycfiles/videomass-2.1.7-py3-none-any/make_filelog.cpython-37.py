# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_io/make_filelog.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 2450 bytes
import time, os

def write_log(logfile, logdir):
    """
    Before starting the process, a log file stored in the conventional
    path of the OS is created, see `vdms_sys/ctrl_run.py` .

    - logfile è il nome del pannello da cui è stato composto il comando
    """
    if not os.path.isdir(logdir):
        try:
            os.makedirs(logdir, mode=511)
        except OSError as error:
            try:
                print(error)
                return error
            finally:
                error = None
                del error

    current_date = time.strftime('%c')
    path = os.path.join(logdir, logfile)
    with open(path, 'w') as (log):
        log.write("[PYTHON] CURRENT DATE/TIME:\n%s\n\n-----------------------------------------\n[VIDEOMASS] INFO FOR USERS:\n-----------------------------------------\nAll FFmpeg and FFplay output messages are on stderr (excluse ffprobe),\nand include both information messages and error messages.\nChanging the logging level into setting dialog would also change the\nbehavior of the output on log messages.\n-----------------------------------------\nOn Videomass default ffmpeg loglevel is fixed to 'warning';\nffplay to 'error' .\nFor more details, see videomass.conf or videomassWin32.conf\ninto configuration directory.\n-----------------------------------------\n\n[VIDEOMASS] COMMAND LINE:\n\n" % current_date)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/titi/aha/pythonpath/eagexp/cmd.py
# Compiled at: 2012-12-04 11:48:35
from eagexp import USE_DISPLAY
from eagexp.util import norm_path
from easyprocess import Proc
from path import path
from pyvirtualdisplay import Display
import os, shutil, tempfile, time
TIMEOUT = 300

class EagleError(Exception):
    """eagexp error"""
    pass


def command_eagle(input, commands=[], timeout=TIMEOUT, showgui=False, callback=None):
    input = norm_path(input)
    if not commands:
        commands = []
    ext = os.path.splitext(input)[1]
    if ext not in ('.brd', '.sch'):
        raise ValueError('Input extension is not in [.brd, .sch], input=' + str(input))
    tmp_dir = tempfile.mkdtemp(prefix='eagexp')
    tmp_input = os.path.join(tmp_dir, os.path.split(input)[1])
    shutil.copy(input, tmp_input)
    script = ''
    for x in commands:
        script += x
        script += ';'

    cmd = [
     'eagle', '-C ' + script, tmp_input]

    def call_eagle():
        p = Proc(cmd).call(timeout=timeout)
        if p.return_code != 0:
            raise EagleError('eagle return code is not zero, proc=' + str(p))

    curdir = path.getcwd()
    curdir = norm_path(curdir)
    os.chdir(tmp_dir)
    if USE_DISPLAY:
        with Display(visible=showgui, size=(800, 600)):
            time.sleep(1)
            call_eagle()
    else:
        call_eagle()
    os.chdir(curdir)
    if callback:
        callback(tmp_dir, tmp_input)
    shutil.rmtree(tmp_dir)
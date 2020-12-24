# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\data\kungfu.py
# Compiled at: 2015-05-17 13:47:45
# Size of source mod 2**32: 618 bytes
from autohdl import manager
cfg = {'technology': 'Spartan3e', 
 'part': 'xc3s250e', 
 'package': 'tq144', 
 'speed_grade': '-5', 
 'eeprom_kilobytes': '256', 
 'src': [],  'ignore_undefined_instances': [],  'top_module': '', 
 'include_paths': [],  'webdav_src_path': 'git/hdl', 
 'webdav_build_path': 'test/distout/rtl', 
 'host': 'cs.scircus.ru', 
 'webdav_files': []}
if __name__ == '__main__':
    manager.kungfu(script_cfg=cfg)
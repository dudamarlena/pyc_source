# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/w3/yc8mtbd91vs80rp79zfgk8x00000gn/T/pip-install-aqb0355v/NetEase-MusicBox/NEMbox/__init__.py
# Compiled at: 2020-03-01 00:57:52
# Size of source mod 2**32: 278 bytes
from .utils import create_dir, create_file
from .const import Constant
create_dir(Constant.conf_dir)
create_dir(Constant.download_dir)
create_file(Constant.storage_path)
create_file((Constant.log_path), default='')
create_file((Constant.cookie_path), default='#LWP-Cookies-2.0\n')
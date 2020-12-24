# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/netort/bdk/bdk/core/config/dynamic_options.py
# Compiled at: 2018-02-26 08:30:12
import os, datetime, uuid, pwd, sys, platform
DYNAMIC_OPTIONS = {'pid': lambda : os.getpid(), 
   'cmdline': lambda : (' ').join(sys.argv), 
   'test_id': lambda : ('{date}_{uuid}').format(date=datetime.datetime.now().strftime('%Y-%m-%d'), uuid=str(uuid.uuid4())), 
   'key_date': lambda : datetime.datetime.now().strftime('%Y-%m-%d'), 
   'operator': lambda : pwd.getpwuid(os.geteuid())[0], 
   'is_darwin': lambda : True if platform.system() == 'Darwin' else False}
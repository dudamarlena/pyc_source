# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/presenzialo_config.py
# Compiled at: 2020-01-27 05:59:20
# Size of source mod 2**32: 1039 bytes
import os, datetime
version = '0.4.2'
config_path = os.path.join(os.path.expanduser('~'), '.presenzialo')
config_path_deprecated = os.path.join(os.path.expanduser('~'), '.Presenzialo')
if os.path.isdir(config_path_deprecated):
    import shutil
    shutil.move(config_path_deprecated, config_path)
if not os.path.exists(config_path):
    os.makedirs(config_path)
config_auth = os.path.join(config_path, 'auth')
config_presences = os.path.join(config_path, 'presences')
config_address = os.path.join(config_path, 'address')
config_workersid = os.path.join(config_path, 'workersid')
config_workersid_deadline = datetime.timedelta(days=7)
config_address_deadline = datetime.timedelta(days=31)

def check_file_date(config_file):
    return datetime.datetime.fromtimestamp(os.path.getmtime(config_file))


def generate_workersid_file():
    try:
        time = check_file_date(config_workersid)
    except FileNotFoundError:
        return True
    else:
        dt = datetime.datetime.now() - time
        return dt > config_workersid_deadline
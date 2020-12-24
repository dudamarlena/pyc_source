# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xasm/write_pyc.py
# Compiled at: 2020-04-24 21:51:34
import xdis
from xdis import PYTHON3
from xdis.magics import magics, magic2int
from xdis.marsh import dumps
from struct import pack
import time

def write_pycfile(fp, code_list, timestamp=None, version=xdis.PYTHON_VERSION):
    magic_bytes = magics[version]
    magic_int = magic2int(magic_bytes)
    fp.write(magic_bytes)
    if timestamp is None:
        timestamp = int(time.time())
    write_source_size = version > 3.2
    if version >= 3.7:
        if magic_int == 3393:
            fp.write(pack('I', timestamp))
            fp.write(pack('I', 0))
        else:
            fp.write(pack('<I', 0))
            fp.write(pack('<I', timestamp))
    else:
        fp.write(pack('<I', timestamp))
    if write_source_size:
        fp.write(pack('<I', 0))
    for co in code_list:
        try:
            co_obj = dumps(co, python_version=str(version))
            if PYTHON3 and version < 3.0:
                co_obj = str.encode(co_obj)
            fp.write(co_obj)
        except:
            pass

    return
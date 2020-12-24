# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\pm\src\epcpm\_build.py
# Compiled at: 2020-04-20 19:03:36
# Size of source mod 2**32: 311 bytes
try:
    from epcpm.__build import build_system, build_id, build_number, build_version, job_id, job_url
except ImportError:
    build_system = None
    build_id = None
    build_number = None
    build_version = None
    job_id = None
    job_url = None
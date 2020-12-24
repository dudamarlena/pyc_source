# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/config.py
# Compiled at: 2019-06-02 00:55:48
# Size of source mod 2**32: 176 bytes
from dataclasses import dataclass

@dataclass
class Configuration:
    smtp_host: str
    smtp_port: int
    web_host: str
    web_port: int
    develop: bool
    debug: bool
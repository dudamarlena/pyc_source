# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amureki/Development/opensource/whoisp/whoisp/__init__.py
# Compiled at: 2017-04-14 06:30:06
# Size of source mod 2**32: 447 bytes
from .parser import MainParser
from subprocess import check_output, TimeoutExpired
__author__ = 'Rustem Sayargaliev'
__version__ = '0.0.2'

def whois(domain, fail_silently=False):
    try:
        bytes_out = check_output(['whois', domain], timeout=10)
    except TimeoutExpired:
        if not fail_silently:
            raise
        bytes_out = ''

    out = bytes_out.decode(encoding='utf8')
    return MainParser.load(domain, raw_whois=out)
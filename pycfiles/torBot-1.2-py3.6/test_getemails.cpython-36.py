# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_getemails.py
# Compiled at: 2018-07-01 06:52:30
# Size of source mod 2**32: 569 bytes
import sys, os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from modules import pagereader, getemails

def test_get_emails_successful():
    soup = pagereader.read_first_page('https://www.helloaddress.com/')[0]
    test_emails = ['hello@helloaddress.com']
    emails = getemails.getMails(soup)
    assert emails == test_emails


if __name__ == '__main__':
    test_get_emails_successful()
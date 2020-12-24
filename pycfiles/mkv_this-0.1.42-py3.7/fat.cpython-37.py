# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mkv_this/fat.py
# Compiled at: 2020-04-25 19:33:20
# Size of source mod 2**32: 349 bytes
import markovify

def URL(insert):
    """ fetch a url """
    try:
        req = requests.get(insert)
        req.raise_for_status()
    except Exception as exc:
        try:
            print(f": There was a problem: {exc}.\n: Please enter a valid URL")
            sys.exit()
        finally:
            exc = None
            del exc

    else:
        print(': fetched URL.')
        return req.text
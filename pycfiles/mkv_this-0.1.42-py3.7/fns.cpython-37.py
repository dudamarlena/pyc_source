# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mkv_this/fns.py
# Compiled at: 2020-04-22 17:53:04
# Size of source mod 2**32: 505 bytes
import markovify, sys, requests, argparse

def URL(insert):
    try:
        req = requests.get(insert)
        req.raise_for_status()
    except Exception as exc:
        try:
            print(f"There was a problem: {exc}")
            sys.exit()
        finally:
            exc = None
            del exc

    else:
        print('text fetched from URL.')
        return req.text
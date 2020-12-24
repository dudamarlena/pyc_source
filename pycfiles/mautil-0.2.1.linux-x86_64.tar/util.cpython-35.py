# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/test/util.py
# Compiled at: 2019-07-25 03:41:06
# Size of source mod 2**32: 112 bytes
from mautil.util import ArgParser

def main(gl):
    args = TrainArgParser.load_args()
    gl[args.method_name]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/canvas.py
# Compiled at: 2020-01-08 09:31:39
# Size of source mod 2**32: 153 bytes
import sys
from .canvas_launcher import Launcher

def main(argv):
    Launcher().launch(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
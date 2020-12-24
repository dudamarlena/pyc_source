# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cabox/envs/tailchaser/lib/python2.7/site-packages/tailchaser/__main__.py
# Compiled at: 2016-04-30 15:51:32
"""
Entrypoint module, in case you use `python -mtailchaser`.

Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
import sys
from tailchaser.cli import main
if __name__ == '__main__':
    sys.exit(main())
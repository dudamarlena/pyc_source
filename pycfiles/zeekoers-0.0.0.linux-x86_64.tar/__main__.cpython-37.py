# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/martijn/.virtualenvs/zeekoers/lib/python3.7/site-packages/zeekoers/__main__.py
# Compiled at: 2020-02-05 09:53:42
# Size of source mod 2**32: 363 bytes
"""
Entrypoint module, in case you use `python -mzeekoers`.

Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
from zeekoers.cli import main
if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\__init__.py
# Compiled at: 2020-01-01 13:20:59
# Size of source mod 2**32: 214 bytes
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def main():
    from .core import start_app
    start_app()
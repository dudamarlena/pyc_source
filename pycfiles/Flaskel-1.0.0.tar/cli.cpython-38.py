# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Project\CLOUD\flaskel\skeleton\cli.py
# Compiled at: 2020-04-25 11:30:29
# Size of source mod 2**32: 571 bytes
from flaskel import serve_forever, default_app_factory
from blueprints import BLUEPRINTS
from flaskel.ext import EXTENSIONS

def cli():
    """

    """
    serve_forever(default_app_factory,
      blueprints=BLUEPRINTS,
      extensions=EXTENSIONS)


app = default_app_factory(blueprints=BLUEPRINTS,
  extensions=EXTENSIONS)
if __name__ == '__main__':
    cli()
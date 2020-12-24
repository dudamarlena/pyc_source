# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/workers/gaiohttp.py
# Compiled at: 2019-02-14 00:35:18
import sys
from gunicorn import util
if sys.version_info >= (3, 4):
    try:
        import aiohttp
    except ImportError:
        raise RuntimeError('You need aiohttp installed to use this worker.')
    else:
        try:
            from aiohttp.worker import GunicornWebWorker as AiohttpWorker
        except ImportError:
            from gunicorn.workers._gaiohttp import AiohttpWorker

        util.warn("The 'gaiohttp' worker is deprecated. See --worker-class documentation for more information.")
        __all__ = [
         'AiohttpWorker']

else:
    raise RuntimeError('You need Python >= 3.4 to use the gaiohttp worker')
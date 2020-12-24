# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/fastapi/middleware.py
# Compiled at: 2020-04-03 03:47:54
# Size of source mod 2**32: 1061 bytes
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.encoders import jsonable_encoder
import time
import zo.log as log
from .error import resp_error

def add_cors(app, allowed_hosts=None):
    app.add_middleware(CORSMiddleware,
      allow_origins=(allowed_hosts or ['*']),
      allow_credentials=True,
      allow_methods=[
     '*'],
      allow_headers=[
     '*'])


def add_process_time(app):

    @app.middleware('http')
    @log.catch()
    async def _add_process_time(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            try:
                log.exception(e)
                response = resp_error(request, 'Error', 'error_code', 'Error', HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                e = None
                del e

        response.headers['X-Process-Time'] = f"{(time.time() - start_time) * 1000:.3f} ms"
        return response
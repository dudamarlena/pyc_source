# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/fastapi/error.py
# Compiled at: 2020-04-03 01:28:57
# Size of source mod 2**32: 3013 bytes
from fastapi import HTTPException, FastAPI
from typing import *
from munch import munchify
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from ..log import log
from ..aa import ec

class _CustomException(Exception):

    def __init__(self, message: str, code: str, status_code: int, kwargs: dict):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.kwargs = kwargs


def resp_error(request: Request, message, code, detail, status_code):
    return JSONResponse((jsonable_encoder({'message':message, 
     'code':code, 
     'request':{'body':request.body, 
      'query':request.query_params}, 
     'url':request.url._url, 
     'detail':detail})),
      status_code=status_code)


async def _http422_error_handler(request: Request, exc: Union[(RequestValidationError, ValidationError)]) -> JSONResponse:
    message = code = 'RequestValidationError'
    detail = exc.errors()
    try:
        error = munchify(detail[0])
        message, code = f"{'.'.join(error.loc).replace('body.aa.', '')} : {error.msg}", error.type
    except Exception as e:
        try:
            log.warning([e, detail])
        finally:
            e = None
            del e

    return resp_error(request, message, code, detail, HTTP_422_UNPROCESSABLE_ENTITY)


async def _http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    message = str(exc.detail) if exc.detail else 'error'
    return resp_error(request, message, 'error_code', exc.detail, exc.status_code)


async def _custom_exception_handler(request: Request, exc: _CustomException):
    return resp_error(request, exc.message, exc.code, exc.kwargs, exc.status_code)


def add_error(app: FastAPI):
    app.add_exception_handler(HTTPException, _http_error_handler)
    app.add_exception_handler(_CustomException, _custom_exception_handler)
    app.add_exception_handler(RequestValidationError, _http422_error_handler)


def abort_if(condition, message=ec.not_exist, code='Error', status_code=400, **kwargs):
    if condition:
        log.debug(f"abort_if [{(message, code, status_code, kwargs)}]")
        raise _CustomException(message, code, status_code, kwargs)


class _ValidationError(BaseModel):
    loc: List[str]
    type: str
    url: str


class ValidationErrorMessage(BaseModel):
    message = 'Request Validation Error'
    message: str
    code = 'RequestValidationError'
    code: str
    body = {}
    body: dict
    url = ''
    url: str
    detail: List[_ValidationError]
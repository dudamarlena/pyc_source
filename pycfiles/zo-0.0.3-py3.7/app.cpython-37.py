# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/fastapi/app.py
# Compiled at: 2020-04-03 01:21:37
# Size of source mod 2**32: 2499 bytes
from fastapi import FastAPI, APIRouter, params
from starlette.types import ASGIApp
from starlette.staticfiles import StaticFiles
from starlette.responses import Response
import uvicorn, pathlib
from typing import *
from ..aa import get_env
from ..log import add_log_trace, log
from .error import add_error
from .middleware import add_process_time

def get_app(router: APIRouter) -> FastAPI:
    env = get_env()
    if env.debug:
        add_log_trace()
    app = FastAPI(title=(env.title),
      debug=(env.debug),
      version=(env.version),
      docs_url=(env.docs_url),
      redoc_url=(env.redoc_url))
    add_error(app)
    add_process_time(app)
    add_include_router(app, router, prefix=(env.api_prefix))
    return app


def run_app():
    env = get_env()
    uvicorn.run((env.run_app),
      host=(env.app_host),
      port=(env.app_port),
      reload=(env.debug),
      workers=1,
      log_level=(env.run_log_level),
      access_log=(env.run_access_log))


def add_include_router(router: APIRouter, include_router: APIRouter, prefix: str='', tags: List[str]=None, dependencies: Sequence[params.Depends]=None, responses: Dict[(Union[(int, str)], Dict[(str, Any)])]=None, default_response_class: Optional[Type[Response]]=None) -> None:
    return router and include_router or None
    responses = responses or {200:{'content': {'application/json': {'example': {'message':'ok',  'result':{},  'detail':{}}}}}, 
     422:{'description': 'Request Parameters Validation Error'}}
    router.include_router(include_router,
      prefix=prefix, tags=tags, dependencies=dependencies, responses=responses, default_response_class=default_response_class)


def add_mount(app: FastAPI, path, asgi_app: ASGIApp=None, name=None):
    """
    Args:
        app: FastAPI
        path:
        asgi_app: StaticFiles(directory="static")
        name:
    """
    if not asgi_app:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    asgi_app = asgi_app or StaticFiles(directory=path)
    name = name or path
    app.mount(f"/{path}", asgi_app, name)
    log.info(f"app mount /{path}")
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: featurize_jupyterlab/__init__.py
# Compiled at: 2019-10-01 22:58:45
from .handlers import setup_handlers
from . import core
from .proto import minetorch_pb2
from .proto import minetorch_pb2_grpc
from . import constants
from .package_manager import package_manager
from . import g
from .plugins import CorePlugin

def _jupyter_server_extension_paths():
    return [{'module': 'featurize_jupyterlab'}]


def load_jupyter_server_extension(nb_server_app):
    core.boot()
    setup_handlers(nb_server_app)
# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\__init__.py
# Compiled at: 2016-09-26 16:59:47
# Size of source mod 2**32: 1625 bytes
__doc__ = '\nCoralogix SDK initialization module.\n'
VERSION = (0, 2, 6, 6)
get_version = lambda : '.'.join(str(x) for x in VERSION)
__version__ = get_version()
TICKS_IN_SECOND = 10000000
MICROSEC_IN_SEC = 1000000
CORALOGIX_ENCODING = 'utf-8'
try:
    from urllib import request
    import ssl
    if hasattr(ssl, 'SSLContext'):
        ssl_handler = request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        ssl_opener = request.build_opener(ssl_handler)
        request.install_opener(ssl_opener)
except ImportError:
    pass

try:
    from enum import Enum, IntEnum
except ImportError:
    from enum34 import Enum, IntEnum

class Category(Enum):
    BusinessLogic, DataAccess, UILogic, UIComponents, Engine, System, Core, General, Configuration, Algorithm, Middleware, FrontEnd, BackEnd, SDK, API, Utilities, Database, Kernel, ClientSide, ServerSide, Infrastructure, Proxy = range(22)


class Severity(IntEnum):
    Debug = 1
    Verbose = 2
    Info = 3
    Warning = 4
    Error = 5
    Critical = 6


from .logger import CoralogixLogger
from coralogix.coralogix_logging import CoralogixHandler
from coralogix.coralogix_https_logging import CoralogixHTTPSHandler
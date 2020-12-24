# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/__init__.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 1296 bytes
import os
from pkg_resources import get_distribution, resource_filename
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from sovereign import config_loader
from sovereign.utils.dictupdate import merge
from sovereign.schemas import SovereignConfig, SovereignAsgiConfig, XdsTemplate
json_response_class = JSONResponse
try:
    import orjson
    from fastapi.responses import ORJSONResponse
    json_response_class = ORJSONResponse
except ImportError:
    try:
        import ujson
        from fastapi.responses import UJSONResponse
        json_response_class = UJSONResponse
    except ImportError:
        pass

else:

    def parse_raw_configuration(path: str):
        ret = dict()
        for p in path.split(','):
            ret = merge(obj_a=ret,
              obj_b=(config_loader.load(p)),
              merge_lists=True)
        else:
            return ret


    __versionstr__ = get_distribution('sovereign').version
    __version__ = tuple((int(i) for i in __versionstr__.split('.')))
    config_path = os.getenv('SOVEREIGN_CONFIG', 'file:///etc/sovereign.yaml')
    html_templates = Jinja2Templates(resource_filename('sovereign', 'templates'))
    config = SovereignConfig(**parse_raw_configuration(config_path))
    asgi_config = SovereignAsgiConfig()
    XDS_TEMPLATES = config.xds_templates
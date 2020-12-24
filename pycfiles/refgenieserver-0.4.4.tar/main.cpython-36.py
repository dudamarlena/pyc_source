# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mstolarczyk/Uczelnia/UVA/code/refgenieserver/refgenieserver/main.py
# Compiled at: 2020-01-16 11:52:57
# Size of source mod 2**32: 1859 bytes
from .const import *
from .helpers import build_parser
from .server_builder import archive
from refgenconf import RefGenConf, select_genome_config
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import logmuse, sys, uvicorn
from ubiquerg import parse_registry_path
app = FastAPI()
app.mount(('/' + STATIC_DIRNAME), StaticFiles(directory=STATIC_PATH), name=STATIC_DIRNAME)
templates = Jinja2Templates(directory=TEMPLATES_PATH)

def main():
    global _LOGGER
    global rgc
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        print('No subcommand given')
        sys.exit(1)
    else:
        logger_args = dict(name=PKG_NAME, fmt=LOG_FORMAT, level=5) if args.debug else dict(name=PKG_NAME, fmt=LOG_FORMAT)
        _LOGGER = (logmuse.setup_logger)(**logger_args)
        selected_cfg = select_genome_config(args.config)
        assert selected_cfg is not None, 'You must provide a config file or set the {} environment variable'.format('or '.join(CFG_ENV_VARS))
    rgc = RefGenConf(filepath=selected_cfg, writable=False)
    if args.command == 'archive':
        arp = [parse_registry_path(x) for x in args.asset_registry_paths] if args.asset_registry_paths is not None else None
        archive(rgc, arp, args.force, args.remove, selected_cfg, args.genomes_desc)
    elif args.command == 'serve':
        from .routers import version1, version2
        app.include_router(version1.router)
        app.include_router((version1.router), prefix='/v1')
        app.include_router((version2.router), prefix='/v2')
        uvicorn.run(app, host='0.0.0.0', port=(args.port))
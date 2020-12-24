# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dtale/__init__.py
# Compiled at: 2020-04-26 12:06:36
from flask import Blueprint
dtale = Blueprint('dtale', __name__, url_prefix='/dtale')
from dtale.app import show, get_instance, instances, offline_chart
from dtale.cli.loaders import LOADERS
for loader_name, loader in LOADERS.items():
    if hasattr(loader, 'show_loader'):
        globals()[('show_{}').format(loader_name)] = loader.show_loader
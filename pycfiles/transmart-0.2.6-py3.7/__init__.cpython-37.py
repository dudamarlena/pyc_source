# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transmart/__init__.py
# Compiled at: 2019-08-27 08:41:54
# Size of source mod 2**32: 1464 bytes
"""
* Copyright (c) 2015-2017 The Hyve B.V.
* This code is licensed under the GNU General Public License,
* version 3.
"""
from itertools import chain
import logging
logger = logging.getLogger('tm-api')
minimal = ('requests', 'click')
backend = ('pandas', 'google.protobuf', 'arrow')
full = ('whoosh', 'ipywidgets', 'IPython', 'bqplot')
missing_dependencies = set()
for dependency in chain(minimal, backend, full):
    try:
        __import__(dependency)
    except ImportError as e:
        try:
            missing_dependencies.add(dependency)
        finally:
            e = None
            del e

if missing_dependencies:
    msg = 'Missing dependencies: {}'.format(', '.join(missing_dependencies))
    logger.warning(msg)
else:
    _hard = missing_dependencies.intersection(minimal)
    if _hard:
        raise ImportError('Missing required dependencies {}'.format(_hard))
    else:
        if missing_dependencies.intersection(backend):
            logger.warning('Running in minimal dependency mode. Only administrative calls are available.')
            dependency_mode = 'MINIMAL'
        else:
            if missing_dependencies.intersection(full):
                logger.warning('No Javascript dependencies found. Running in headless mode.')
                dependency_mode = 'BACKEND'
            else:
                dependency_mode = 'FULL'
del minimal
del backend
del full
del _hard
del missing_dependencies
del chain
del dependency
del logging
from .main import get_api
__version__ = '0.2.6'
__author__ = 'The Hyve'
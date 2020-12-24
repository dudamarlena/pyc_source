# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/cov-core/cov_core_init.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2299 bytes
"""Activate coverage at python startup if appropriate.

The python site initialisation will ensure that anything we import
will be removed and not visible at the end of python startup.  However
we minimise all work by putting these init actions in this separate
module and only importing what is needed when needed.

For normal python startup when coverage should not be activated the pth
file checks a single env var and does not import or call the init fn
here.

For python startup when an ancestor process has set the env indicating
that code coverage is being collected we activate coverage based on
info passed via env vars.
"""
UNIQUE_SEP = '084031f3d2994d40a88c8b699b69e148'
import cov_core

def init():
    try:
        import os
        cov_source = os.environ.get('COV_CORE_SOURCE')
        cov_data_file = os.environ.get('COV_CORE_DATA_FILE')
        cov_config = os.environ.get('COV_CORE_CONFIG')
        if cov_data_file:
            if cov_config:
                import socket, random, coverage
                if cov_source == '':
                    cov_source = None
                else:
                    cov_source = cov_source.split(UNIQUE_SEP)
                data_suffix = '%s.%s.%s' % (socket.gethostname(),
                 os.getpid(),
                 random.randint(0, 999999))
                cov = coverage.coverage(source=cov_source, data_file=cov_data_file,
                  data_suffix=data_suffix,
                  config_file=cov_config,
                  auto_data=True)
                cov.erase()
                cov.start()
                return cov
    except Exception:
        pass
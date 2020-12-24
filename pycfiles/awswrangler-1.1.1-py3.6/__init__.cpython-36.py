# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awswrangler/__init__.py
# Compiled at: 2020-05-05 13:30:45
# Size of source mod 2**32: 468 bytes
"""Initial Module.

Source repository: https://github.com/awslabs/aws-data-wrangler
Documentation: https://aws-data-wrangler.readthedocs.io/

"""
import logging
from awswrangler import athena, catalog, cloudwatch, db, emr, exceptions, s3
from awswrangler.__metadata__ import __description__, __license__, __title__, __version__
from awswrangler._utils import get_account_id
logging.getLogger('awswrangler').addHandler(logging.NullHandler())
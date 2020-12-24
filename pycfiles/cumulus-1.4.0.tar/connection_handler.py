# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sebastian/git/skymill/cumulus/cumulus/cumulus_ds/connection_handler.py
# Compiled at: 2014-03-04 09:28:50
""" Connection handler """
import boto, logging
from boto import cloudformation
from cumulus_ds.config import CONFIG as config
logger = logging.getLogger(__name__)

def connect_s3():
    """ Connect to AWS S3

    :returns: boto.s3.connection
    """
    try:
        return boto.connect_s3(aws_access_key_id=config.get_environment_option('access-key-id'), aws_secret_access_key=config.get_environment_option('secret-access-key'))
    except Exception as err:
        logger.error(('A problem occurred connecting to AWS S3: {}').format(err))
        raise


def connect_cloudformation():
    """ Connect to AWS CloudFormation

    :returns: boto.cloudformation.connection
    """
    try:
        return cloudformation.connect_to_region(config.get_environment_option('region'), aws_access_key_id=config.get_environment_option('access-key-id'), aws_secret_access_key=config.get_environment_option('secret-access-key'))
    except Exception as err:
        logger.error(('A problem occurred connecting to AWS CloudFormation: {}').format(err))
        raise
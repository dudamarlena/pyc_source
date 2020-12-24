# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sebastian/git/skymill/cumulus/cumulus/cumulus_ds/connection_handler.py
# Compiled at: 2014-03-04 09:28:50
__doc__ = ' Connection handler '
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
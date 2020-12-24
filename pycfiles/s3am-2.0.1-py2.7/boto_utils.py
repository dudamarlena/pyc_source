# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s3am/boto_utils.py
# Compiled at: 2016-11-03 16:06:47
from __future__ import absolute_import
import logging, boto.s3
from boto.s3.connection import S3Connection
log = logging.getLogger(__name__)
old_match_hostname = None

def work_around_dots_in_bucket_names():
    """
    https://github.com/boto/boto/issues/2836
    """
    global old_match_hostname
    if old_match_hostname is None:
        import re, ssl
        try:
            old_match_hostname = ssl.match_hostname
        except AttributeError:
            log.warn('Failed to install workaround for dots in bucket names.')
        else:
            hostname_re = re.compile('^(.*?)(\\.s3(?:-[^.]+)?\\.amazonaws\\.com)$')

            def new_match_hostname(cert, hostname):
                match = hostname_re.match(hostname)
                if match:
                    hostname = match.group(1).replace('.', '') + match.group(2)
                return old_match_hostname(cert, hostname)

            ssl.match_hostname = new_match_hostname

    return


def region_to_bucket_location(region):
    if region == 'us-east-1':
        return ''
    else:
        return region


def bucket_location_to_region(location):
    if location == '':
        return 'us-east-1'
    else:
        return location


def bucket_location_to_http_url(location):
    if location:
        return 'https://s3-' + location + '.amazonaws.com'
    else:
        return 'https://s3.amazonaws.com'


def s3_connect_to_region(region):
    """
    :param str region: the region name
    :rtype: S3Connection
    """
    s3 = boto.s3.connect_to_region(region)
    if s3 is None:
        raise RuntimeError("The region name '%s' appears to be invalid.", region)
    else:
        return s3
    return


def modify_metadata_retry():
    """
    https://github.com/BD2KGenomics/s3am/issues/16
    """
    from boto import config

    def inject_default(name, default):
        section = 'Boto'
        value = config.get(section, name)
        if value != default:
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, name, default)

    inject_default('metadata_service_timeout', '5.0')
    inject_default('metadata_service_num_attempts', '3')
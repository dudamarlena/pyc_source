# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/NTFS_D/Documents/PyCharmProjects/python-geomark/geomark/config.py
# Compiled at: 2017-12-19 16:49:26
# Size of source mod 2**32: 871 bytes
import logging
LOG_LEVEL = logging.DEBUG
LOGGER = logging.getLogger('geomark')
LOGGER.setLevel(LOG_LEVEL)
_ch = logging.StreamHandler()
_formatter = logging.Formatter('%(name)s:%(levelname)s (%(asctime)s) - %(message)s')
_ch.setFormatter(_formatter)
LOGGER.addHandler(_ch)
PROTOCOL = 'https'
GEOMARK_BASE_URL = '{protocol}://apps.gov.bc.ca/pub/geomark'
GEOMARK_ID_BASE_URL = GEOMARK_BASE_URL + '/geomarks/{geomarkId}'
GEOMARK_GROUP_BASE_URL = GEOMARK_BASE_URL + '/geomarkGroups/{geomarkGroupId}'
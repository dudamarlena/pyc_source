# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/django/sc-catalog/venv/lib/python3.6/site-packages/trumbowyg/utils.py
# Compiled at: 2018-09-10 09:07:58
# Size of source mod 2**32: 469 bytes
import logging
from django.utils import six
from django.utils.text import slugify as django_slugify
from trumbowyg import settings as _settings
logger = logging.getLogger(__name__)

def slugify(value):
    if _settings.TRANSLITERATE_FILENAME:
        try:
            from unidecode import unidecode
            value = unidecode(six.text_type(value))
        except ImportError as e:
            logger.exception(e)

    return django_slugify(six.text_type(value))
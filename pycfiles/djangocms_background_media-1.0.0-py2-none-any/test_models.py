# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/website/apps/djangocms_background_media/tests/test_models.py
# Compiled at: 2016-06-23 11:11:49
from __future__ import unicode_literals
from django.core.files import File
from cms.test_utils.testcases import CMSTestCase
from filer.models import Image as FilerImage
from ..models import BackgroundMedia
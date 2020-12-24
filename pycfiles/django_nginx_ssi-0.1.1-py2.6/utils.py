# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ssi/utils.py
# Compiled at: 2011-01-25 14:12:30
from django.utils.hashcompat import md5_constructor
from django.conf import settings

def generate_ssi_cache_key(template_string):
    return md5_constructor((':').join(['ssi',
     getattr(settings, 'CACHE_SSI_KEY_PREFIX', ''),
     template_string])).hexdigest()
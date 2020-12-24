# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/cms_app.py
# Compiled at: 2012-10-05 10:11:44
from cms.apphook_pool import apphook_pool
from cms_search.cms_app import HaystackSearchApphook
apphook_pool.register(HaystackSearchApphook)
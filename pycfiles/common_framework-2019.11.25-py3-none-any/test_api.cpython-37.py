# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/tests/test_api.py
# Compiled at: 2018-02-27 12:01:31
# Size of source mod 2**32: 313 bytes
from common.tests import create_api_test_class
from common.models import MetaData, Webhook
RECIPES = {}
for model in [MetaData, Webhook]:
    create_api_test_class(model, namespace='common-api', data=(RECIPES.get(model, None)))
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/tests/test_api.py
# Compiled at: 2018-02-27 12:01:31
# Size of source mod 2**32: 313 bytes
from common.tests import create_api_test_class
from common.models import MetaData, Webhook
RECIPES = {}
for model in [MetaData, Webhook]:
    create_api_test_class(model, namespace='common-api', data=(RECIPES.get(model, None)))
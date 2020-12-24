# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/example/handlers/event/s3.py
# Compiled at: 2019-10-06 23:42:33
# Size of source mod 2**32: 550 bytes
import json
from lbdrabbit import LbdFuncConfig

def handler(event, context):
    print(event)
    return {'status_code':'200', 
     'body':json.dumps(event)}


handler.__lbd_func_config__ = LbdFuncConfig()
handler.__lbd_func_config__.s3_event_bucket_yes = True
handler.__lbd_func_config__.s3_event_bucket_basename = 'data-store'
handler.__lbd_func_config__.s3_event_lbd_config_list = [
 LbdFuncConfig.S3EventLambdaConfig(event=(LbdFuncConfig.S3EventLambdaConfig.EventEnum.created_put))]
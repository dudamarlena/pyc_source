# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/owncloud/test/config.py
# Compiled at: 2020-01-31 09:17:07
# Size of source mod 2**32: 870 bytes
import time
test_id = int(time.time())
Config = {'owncloud_url':'http://127.0.0.1/owncloud', 
 'owncloud_login':'admin', 
 'owncloud_password':'admin', 
 'owncloud_share2user':'share', 
 'test_group':'my_test_group', 
 'test_root':'pyoctestroot%s' % test_id, 
 'app_name':'pyocclient_test%s' % test_id, 
 'groups_to_create':[
  'grp1', 'grp2', 'grp3'], 
 'not_existing_group':'this_group_should_not_exist'}
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scampion/src/tamis/madlab/orqal/orqal/conf.py
# Compiled at: 2019-07-12 06:15:55
# Size of source mod 2**32: 872 bytes
import os
from pymongo import MongoClient
mongourl = os.getenv('ORQAL_MONGO_URI', 'mongodb://localhost/')
print(mongourl)
mongo = MongoClient(mongourl)
mconf = {'mongourl':'mongodb://mongo/', 
 'mongo_replicaset':None, 
 'docker_hosts':[
  'nodeA', 'nodeB'], 
 'docker_api_version':'1.40', 
 'registry_auth_config':{'username':'test', 
  'password':'65sX2-9sSXSp-hs-XeZ8'}, 
 'jobs_dir':'/scratch/jobs', 
 'nb_disp_jobs':30, 
 'contact':'orqal@example.com', 
 'services':'~/services.py', 
 'active':True}
dbconf = mongo.orqal.conf.find_one({'active': True})
if dbconf:
    mconf = {**mconf, **dbconf}
    mongo.orqal.conf.replace_one({'_id': mconf['_id']}, mconf)
else:
    mongo.orqal.conf.insert_one(mconf)
locals().update(mconf)
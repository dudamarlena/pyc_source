# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/constants.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 4260 bytes
from typing import Dict, Any

class BudgetOption:
    GPU_COUNT = 'GPU_COUNT'
    TIME_HOURS = 'TIME_HOURS'
    MODEL_TRIAL_COUNT = 'MODEL_TRIAL_COUNT'


Budget = Dict[(BudgetOption, Any)]

class InferenceBudgetOption:
    GPU_COUNT = 'GPU_COUNT'


InferenceBudget = Dict[(InferenceBudgetOption, Any)]
ModelDependencies = Dict[(str, str)]

class ModelAccessRight:
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'


class InferenceJobStatus:
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    STOPPED = 'STOPPED'


class TrainJobStatus:
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'
    ERRORED = 'ERRORED'


class TrialStatus:
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    COMPLETED = 'COMPLETED'


class UserType:
    SUPERADMIN = 'SUPERADMIN'
    ADMIN = 'ADMIN'
    MODEL_DEVELOPER = 'MODEL_DEVELOPER'
    APP_DEVELOPER = 'APP_DEVELOPER'


class ServiceType:
    TRAIN = 'TRAIN'
    ADVISOR = 'ADVISOR'
    PREDICT = 'PREDICT'
    INFERENCE = 'INFERENCE'


class ServiceStatus:
    STARTED = 'STARTED'
    DEPLOYING = 'DEPLOYING'
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    STOPPED = 'STOPPED'


class ModelDependency:
    TENSORFLOW = 'tensorflow'
    KERAS = 'Keras'
    SCIKIT_LEARN = 'scikit-learn'
    TORCH = 'torch'
    TORCHVISION = 'torchvision'
    SINGA = 'singa'
    XGBOOST = 'xgboost'
    DS_CTCDECODER = 'ds-ctcdecoder'
    NLTK = 'nltk'
    SKLEARN_CRFSUITE = 'sklearn-crfsuite'


class RequestsParameters:
    USER_CREATE = {'json': {'email':True,  'password':True,  'user_type':True}}
    LOGIN = {'json': {'email':True,  'password':True}}
    USER_BAN = {'json': {'email': True}}
    TOKEN = {'json': {'email':True,  'password':True}}
    DATASET_POST = {'files':{'dataset': False}, 
     'data':{'name':True, 
      'task':True,  'dataset_url':False}}
    MODEL_CREATE = {'files':{'model_file_bytes':True, 
      'model_pretrained_params_id':False}, 
     'data':{'name':True, 
      'task':True,  'dependencies':False,  'docker_image':False,  'model_class':True, 
      'access_right':False}}
    TRAIN_CREATE = {'json': {'app':True,  'task':True,  'train_dataset_id':True,  'val_dataset_id':True,  'budget':False, 
              'model_ids':False,  'train_args':False}}
    TRAIN_GETBY_USER = {'params': {'user_id': True}}
    TRIAL_GET_BEST = {'params': {'type':True,  'max_count':False}}
    INFERENCE_CREATE = {'json': {'app':True,  'app_version':False,  'budget':False}}
    INFERENCE_CREATEBY_CHECKOUTPOINT = {'json': {'model_name':True,  'budget':False}}
    INFERENCE_GETBY_USER = {'params': {'user_id': True}}
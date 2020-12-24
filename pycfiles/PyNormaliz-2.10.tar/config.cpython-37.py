# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/config.py
# Compiled at: 2019-05-08 19:33:43
# Size of source mod 2**32: 1367 bytes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import cachetools, os, pandas as pd
from sqlalchemy.pool import StaticPool
CONTEXT_NAMESPACE_STUB = 'norm.tmp'
USER_NAMESPACE_STUB = 'norm.user'
MAX_LIMIT = 1000000
UNICODE = 'utf-8'
VERSION_MIN_LENGTH = 6
NORM_HOME = os.environ.get('NORM_HOME', os.path.expanduser('~/.norm'))
DATA_STORAGE_ROOT = os.environ.get('NORM_DATA_STORAGE_ROOT', os.path.join(NORM_HOME, 'data'))
DB_PATH = os.environ.get('NORM_DB_PATH', os.path.join(NORM_HOME, 'db/norm.db'))
cache = cachetools.LRUCache(1024)
PUBLIC_USER = dict(first_name='norm', last_name='ai',
  username='norm',
  email='norm@reasoned.ai')
Session = sessionmaker()
try:
    engine = create_engine(('sqlite:///{}'.format(DB_PATH)), poolclass=StaticPool)
    Session.configure(bind=engine)
    session = Session()
except:
    engine = None
    session = None

context_id = str(datetime.utcnow().strftime('%m%d%Y.%H%M%S'))
pd.options.display.width = 400
pd.options.display.max_columns = 100
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/__init__.py
# Compiled at: 2014-08-27 16:21:43
import pkg_resources, logging, os, warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uta.exceptions import *
from uta import models
try:
    __version__ = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound as e:
    warnings.warn("can't get __version__ because %s package isn't installed" % __package__, Warning)
    __version__ = None

public_db_url = 'postgresql://uta_public:uta_public@uta.invitae.com/uta'
default_db_url = os.environ.get('UTA_DB_URL', public_db_url)

def connect(db_url=default_db_url):
    """
    Connect to a UTA database instance and return a UTA0 interface instance.

    When called with an explicit db_url argument, that db_url is used for connecting.

    When called without an explicit argument, the function default is
    determined by the environment variable UTA_DB_URL if it exists, or
    bdi.sources.uta0.public_db_url.

    The format of the db_url is driver://user:pass@host/database (the same
    as that used by SQLAlchemy).  Examples:

    A remote public postgresql database:
        postgresql://uta_public:uta_public@uta.invitae.com/uta'

    A local postgresql database:
        postgresql://localhost/uta
    
    A local SQLite database:
        sqlite:////tmp/uta-0.0.5.db

    SQLite database snapshots are available at:
      `https://bitbucket.org/uta/uta/downloads`_
    """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    logger = logging.getLogger(__name__)
    logger.info('connected to ' + db_url)
    return session
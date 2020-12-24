# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/loadconfiguration.py
# Compiled at: 2011-01-03 14:39:55
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dbobjects
from conf import settings

def loadData():
    pg_db = create_engine('postgres://%s:%s@%s:%s/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE), echo=settings.DEBUG_ALCHEMY)
    dbobjects.DatabaseObjects()
    Session = sessionmaker(bind=pg_db, autoflush=True)
    session = Session()
    newRec = {'vendor_name': 'BASIX_JFCS', 
       'processing_mode': 'TEST', 
       'source_id': '2', 
       'odbid': '873', 
       'providerid': '115', 
       'userid': '906'}
    dbobjects.SystemConfiguration(newRec)
    session.commit
    newRec = {'vendor_name': 'BASIX_JFCS', 
       'processing_mode': 'PROD', 
       'source_id': '2', 
       'odbid': '871', 
       'providerid': '115', 
       'userid': '906'}
    dbobjects.SystemConfiguration(newRec)
    session.commit
    newRec = {'vendor_name': 'BASIX_HEART', 
       'processing_mode': 'TEST', 
       'source_id': '1', 
       'odbid': '874', 
       'providerid': '2105', 
       'userid': '907'}
    dbobjects.SystemConfiguration(newRec)
    session.commit
    newRec = {'vendor_name': 'BASIX_HEART', 
       'processing_mode': 'PROD', 
       'source_id': '1', 
       'odbid': '872', 
       'providerid': '2105', 
       'userid': '907'}
    dbobjects.SystemConfiguration(newRec)
    session.commit
    session.flush()
    session.commit()


if __name__ == '__main__':
    loadData()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/grad03/fengl/AIMES_project/aimes.bundle/src/aimes/bundle/db/database.py
# Compiled at: 2015-09-21 09:17:23
__doc__ = 'Encapsulate mongodb related operations.\n\nBasic Rules:\n    * Collections hierarchical naming.\n    * Documents are homogeneous in each collection.\n\nExamples:\n    db.session <--metadata=[\n                            [_id=session_id,created_time,DBVersion,...]\n                           ]\n    db.session.resource <--resource_list=[\n                            [_id=x,cluster_type,login_server],\n                            [_id=y,cluster_type,login_server],\n                            ...\n                           ]\n    db.session.resource.config <--static=[\n                            [_id=x,hpc|grid|local|cloud,...],\n                            [_id=y,hpc|grid|local|cloud,...],\n                            ...\n                           ]\n    db.session.resource.workload <--dynamic=[\n                            [timestamp,x,...],\n                            [timestamp,x,...],\n                            [timestamp,y,...],\n                            ...\n                           ]\n    db.session.resource.bandwidth <--network=[\n                            [timestamp,src=x,dst=y,meas],\n                            [timestamp,src=y,dst=x,meas],\n                            ...,\n                           ]\n    db.session.bundle.bundle_manager_uid\n    db.session.bundle.bundle_manager_uid.bundle\n\nNotes:\n    In db, uid for each resource are converted by ip2id().\n'
_DBVersion = '1.0.0'
import datetime, pymongo, radical.utils as ru
from radical.pilot.utils import DBConnectionInfo

def ip2id(ip):
    return ip.replace('.', '_DOT_')


def id2ip(Id):
    return Id.replace('_DOT_', '.')


class DBException(Exception):

    def __init__(self, msg, obj=None):
        Exception.__init__(self, msg)
        self._obj = obj


class Session:
    """This class encapsulates db access methods.
    """

    def __init__(self, db_url, db_name='aimes.bundle'):
        url = ru.Url(db_url)
        if db_name:
            url.path = db_name
        mongo, db, dbname, _, _ = ru.mongodb_connect(url)
        self._client = mongo
        self._db = db
        self._dbname = dbname
        self._dburl = str(url)
        if url.username and url.password:
            self._dbauth = ('{}:{}').format(url.username, url.password)
        else:
            self._dbauth = None
        self._session_id = None
        self._s = None
        self._r = None
        self._rc = None
        self._rw = None
        self._bw = None
        return

    @staticmethod
    def new(sid, db_url, db_name='aimes.bundle'):
        """Creates a new session (factory method).
        """
        creation_time = datetime.datetime.utcnow()
        dbs = Session(db_url, db_name)
        session_metadata = dbs._create(sid, creation_time)
        connection_info = DBConnectionInfo(session_id=sid, dbname=dbs._dbname, dbauth=dbs._dbauth, dburl=dbs._dburl)
        return (
         dbs, session_metadata, connection_info)

    def _create(self, sid, creation_time):
        """Creates a new session.
        """
        if sid and self._db[sid].count() != 0:
            raise DBException(('Session {} already exists.').format(sid))
        self._session_id = sid
        self._s = self._db[sid]
        metadata = {'_id': sid, 'created': creation_time, 
           'connected': creation_time, 
           'version': _DBVersion}
        self._s.insert_one(metadata)
        self._r = self._db[('{}.resource').format(sid)]
        self._rc = self._db[('{}.resource.config').format(sid)]
        self._rw = self._db[('{}.resource.workload').format(sid)]
        self._bw = self._db[('{}.resource.bandwidth').format(sid)]

    @staticmethod
    def reconnect(sid, db_url, db_name='aimes.bundle'):
        """Reconnects to an existing session.
        """
        dbs = Session(db_url, db_name)
        session_metadata = dbs._reconnect(sid)
        connection_info = DBConnectionInfo(session_id=sid, dbname=dbs._dbname, dbauth=dbs._dbauth, dburl=dbs._dburl)
        return (
         dbs, session_metadata, connection_info)

    def _reconnect(self, sid):
        """Reconnects to an existing session (private).
        """
        if sid not in self._db.collection_names():
            raise DBException(("DB session {} doesn't exist.").format(sid))
        self._s = self._db[sid]
        if self._s.find({'_id': sid}).count() != 1:
            raise DBException(("DB session {} metadata doesn't exist.").format(sid))
        self._s.update_one({'_id': sid}, {'$set': {'connected': datetime.datetime.utcnow()}})
        self._session_id = sid
        self._r = self._db[('{}.resource').format(sid)]
        self._rc = self._db[('{}.resource.config').format(sid)]
        self._rw = self._db[('{}.resource.workload').format(sid)]
        self._bw = self._db[('{}.resource.bandwidth').format(sid)]
        return self._s.find_one({'_id': sid})

    @property
    def session_id(self):
        return self._session_id

    def add_resource_list(self, resource_list):
        """Add resource list to db.session.resource.

        The "login_server" field is used to uniquely identify
        each resource. Since mongodb _id can't contain '.', call
        ip2id() to replace '.' with '_DOT_'.
        """
        docs = resource_list.values()
        for d in docs:
            d['_id'] = ip2id(d['login_server'])

        self._r.insert_many(docs)

    def update_resource_config(self, config):
        save_id = config['_id']
        config['_id'] = ip2id(config['_id'])
        self._rc.replace_one({'_id': config['_id']}, config, upsert=True)
        config['_id'] = save_id

    def update_resource_workload(self, workload):
        self._rw.replace_one({'resource_id': workload['resource_id']}, workload, upsert=True)
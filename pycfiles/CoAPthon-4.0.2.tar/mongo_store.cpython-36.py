# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jik/.virtualenvs/coal-mine/lib/python3.6/site-packages/coal_mine/mongo_store.py
# Compiled at: 2018-10-19 12:08:46
# Size of source mod 2**32: 6589 bytes
__doc__ = '\nMongoDB store for Coal Mine\n'
from coal_mine.abstract_store import AbstractStore
import bson
from copy import copy
from logbook import Logger
from pymongo import MongoClient, IndexModel, ASCENDING
from pymongo.errors import AutoReconnect
import re, ssl, time
log = Logger('MongoStore')

class MongoStore(AbstractStore):

    def __init__(self, hosts, database, username, password, **kwargs):
        """Keyword arguments are the same as what would be passed to
        MongoClient."""
        if 'ssl_cert_reqs' in kwargs:
            if kwargs['ssl_cert_reqs'] == 'NONE':
                kwargs['ssl_cert_reqs'] = ssl.CERT_NONE
            else:
                if kwargs['ssl_cert_reqs'] == 'OPTIONAL':
                    kwargs['ssl_cert_reqs'] = ssl.CERT_OPTIONAL
                else:
                    if kwargs['ssl_cert_reqs'] == 'REQUIRED':
                        kwargs['ssl_cert_reqs'] = ssl.CERT_REQUIRED
                    else:
                        raise TypeError('ssl_cert_reqs must be NONE, OPTIONAL, or REQUIRED')
            connection = MongoClient(hosts, **kwargs)
            db = connection[database]
            if username or password:
                db.authenticate(username, password)
        else:
            self.db = db
            self.collection = self.db['canaries']
            existing_indexes = self.collection.index_information()
            try:
                id_index = existing_indexes['id_1']
                try:
                    is_unique = id_index['unique']
                except Exception:
                    is_unique = False

                if not is_unique:
                    self.collection.drop_index('id_1')
            except Exception:
                pass

        self.collection.create_indexes([
         IndexModel([('id', ASCENDING)], unique=True),
         IndexModel([('paused', ASCENDING),
          (
           'late', ASCENDING),
          (
           'deadline', ASCENDING)]),
         IndexModel([('paused', ASCENDING), ('deadline', ASCENDING)]),
         IndexModel([('late', ASCENDING), ('deadline', ASCENDING)]),
         IndexModel([('slug', ASCENDING)], unique=True)])

    def create(self, canary):
        canary['_id'] = bson.ObjectId()
        while True:
            try:
                self.collection.insert_one(canary)
                del canary['_id']
                break
            except AutoReconnect:
                log.exception('save failure, retrying')
                time.sleep(1)

    def update(self, identifier, updates):
        updates = copy(updates)
        unset = {}
        for key, value in [(k, v) for k, v in updates.items()]:
            if value is None:
                del updates[key]
                unset[key] = ''

        doc = {}
        if updates:
            doc['$set'] = updates
        if unset:
            doc['$unset'] = unset
        if not doc:
            return
        while True:
            try:
                self.collection.update_one({'id': identifier}, doc)
                return
            except AutoReconnect:
                log.exception('update failure, retrying')
                time.sleep(1)

    def get(self, identifier):
        while True:
            try:
                canary = self.collection.find_one({'id': identifier}, projection={'_id': False})
                if not canary:
                    raise KeyError('No such canary {}'.format(identifier))
                return canary
            except AutoReconnect:
                log.exception('find_one failure, retrying')
                time.sleep(1)

    def list(self, *, verbose=False, paused=None, late=None, search=None, order_by=None):
        if verbose:
            fields = {'_id': False}
        else:
            fields = {'_id':False, 
             'name':True,  'id':True}
        spec = {}
        if paused is not None:
            spec['paused'] = paused
        if late is not None:
            spec['late'] = late
        if order_by is not None:
            order_by = [
             (
              order_by, ASCENDING)]
        if search is not None:
            search = re.compile(search)
            spec['$or'] = [{'name': search}, {'slug': search}, {'id': search},
             {'emails': search}]
        skip = 0
        while True:
            try:
                for canary in self.collection.find(spec, projection=fields, sort=order_by, skip=skip):
                    yield canary

                break
            except AutoReconnect:
                log.exception('find failure, retrying')
                time.sleep(1)

    def upcoming_deadlines(self):
        return self.list(verbose=True, paused=False, late=False, order_by='deadline')

    def delete(self, identifier):
        while True:
            try:
                result = self.collection.remove({'id': identifier})
                if result['n'] == 0:
                    raise KeyError('No such canary {}'.format(identifier))
                return
            except AutoReconnect:
                log.exception('remove failure, retrying')
                time.sleep(1)

    def find_identifier(self, slug):
        while True:
            try:
                result = self.collection.find_one({'slug': slug})
                if not result:
                    raise KeyError('No such canary {}'.format(slug))
                return result['id']
            except AutoReconnect:
                log.exception('find_one failure, retrying')
                time.sleep(1)
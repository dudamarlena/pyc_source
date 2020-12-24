# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\models.py
# Compiled at: 2015-01-11 13:52:03
import datetime
from chatpy.utils import convert_to_utf8_str

class ResultSet(list):
    """A list like object that holds results from a Chatwork API query."""

    def __init__(self, max_id=None, since_id=None):
        super(ResultSet, self).__init__()
        self._max_id = max_id
        self._since_id = since_id

    @property
    def max_id(self):
        if self._max_id:
            return self._max_id
        else:
            ids = self.ids()
            if ids:
                return max(ids)
            return

    @property
    def since_id(self):
        if self._since_id:
            return self._since_id
        else:
            ids = self.ids()
            if ids:
                return min(ids)
            return

    def ids(self):
        return [ item.id for item in self if hasattr(item, 'id') ]


class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']
        except KeyError:
            pass

        return pickle

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """Parse a list of JSON objects into a result set of model instances."""
        results = ResultSet()
        for obj in json_list:
            if obj:
                results.append(cls.parse(api, obj))

        return results

    def __repr__(self):
        state = [ '%s=%s' % (k, repr(v)) for k, v in vars(self).items() ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(state))


class Account(Model):

    @classmethod
    def parse(cls, api, json):
        account = cls(api)
        for k, v in json.items():
            setattr(account, k, v)

        return account

    @property
    def room(self):
        return self._api.get_room(room_id=self.room_id)

    @property
    def contacts(self):
        return self._api.contacts()


class MyAccount(Account):

    @property
    def tasks(self):
        return self._api.tasks()

    @property
    def status(self):
        return self._api.status()


class Task(Model):

    @classmethod
    def parse(cls, api, json):
        task = cls(api)
        for k, v in json.items():
            if k in ('assigned_by_account', 'account'):
                account_model = getattr(api.parser.model_factory, 'account')
                account = account_model.parse(api, v)
                setattr(task, k, account)
            elif k == 'limit_time':
                utc_time = datetime.datetime.utcfromtimestamp(v)
                setattr(task, k, utc_time)
            else:
                setattr(task, k, v)

        return task

    def __repr__(self):
        text = (' ').join(self.body.split('\n'))
        return ('Task(id={:d}, body={})').format(self.task_id, convert_to_utf8_str(text[0:20]))


class Room(Model):

    @classmethod
    def parse(cls, api, json):
        room = cls(api)
        for k, v in json.items():
            if k == 'last_update_time':
                utc_time = datetime.datetime.utcfromtimestamp(v)
                setattr(room, k, utc_time)
            else:
                setattr(room, k, v)

        return room

    def messages(self, **kwargs):
        return self._api.messages(room_id=self.room_id, **kwargs)

    def post_message(self, body, **kwargs):
        return self._api.post_message(room_id=self.room_id, body=body, **kwargs)

    def destroy(self, **kwargs):
        return self._api.delete_room(room_id=self.room_id, **kwargs)

    @property
    def tasks(self):
        return self._api.room_tasks(room_id=self.room_id)

    @property
    def files(self):
        return self._api.files(room_id=self.room_id)


class File(Model):

    @classmethod
    def parse(cls, api, json):
        f = cls(api)
        for k, v in json.items():
            if k == 'account':
                account_model = getattr(api.parser.model_factory, 'account')
                account = account_model.parse(api, v)
                setattr(f, k, account)
            elif k == 'upload_time':
                utc_time = datetime.datetime.utcfromtimestamp(v)
                setattr(f, k, utc_time)
            else:
                setattr(f, k, v)

        return f


class Message(Model):

    @classmethod
    def parse(cls, api, json):
        message = cls(api)
        for k, v in json.items():
            setattr(message, k, v)

        return message


class Status(Model):

    @classmethod
    def parse(cls, api, json):
        status = cls(api)
        for k, v in json.items():
            setattr(status, k, v)

        return status


class JSONModel(Model):

    @classmethod
    def parse(cls, api, json):
        return json


class IDModel(Model):

    @classmethod
    def parse(cls, api, json):
        if isinstance(json, list):
            return json
        else:
            return json['ids']


class ModelFactory(object):
    """
    Used by parsers for creating instances
    of models. You may subclass this factory
    to add your own extended models.
    """
    room = Room
    account = Account
    my_account = MyAccount
    task = Task
    status = Status
    message = Message
    attachment = File
    json = JSONModel
    ids = IDModel
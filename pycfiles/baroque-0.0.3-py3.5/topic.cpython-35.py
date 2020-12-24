# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/entities/topic.py
# Compiled at: 2017-05-05 06:02:13
# Size of source mod 2**32: 2859 bytes
import uuid, hashlib, collections
from json import dumps
from baroque.datastructures.bags import EventTypesBag
from baroque.utils import timestamp as ts

class Topic:
    __doc__ = 'A distribution channel where events of specific types can be published\n    and can be seen by subscribers of the topic. Topic subscribers will attach\n    a reactor to the topic, which will be fired whenever any event of the types\n    that are supported by the topic is published on the topic itself.\n\n    Args:\n        name (str): the name of this topic\n        eventtypes (collection): the :obj:`baroque.entities.eventtype.EventType` objects that characterize this topic\n        description (str, optional): a description of this topic\n        owner (str, optional): the owner of this topic\n        tags (set, optional): the `set` of tags that describe this topic\n\n    Raises:\n        `AssertionError`: name or tags are `None` or have a wrong type\n\n    '

    def __init__(self, name, eventtypes, description=None, owner=None, tags=None):
        assert name is not None
        assert isinstance(name, str)
        self.name = name
        assert eventtypes is not None
        if len(eventtypes) != 0:
            self.types = EventTypesBag(eventtypes)
        else:
            self.types = EventTypesBag()
        self.description = description
        self.owner = owner
        if tags is not None:
            assert not isinstance(tags, str)
            assert isinstance(tags, collections.Iterable)
            self.tags = set(tags)
        else:
            self.tags = set()
        self.id = str(uuid.uuid4())
        self.timestamp = None
        self.touch()

    @property
    def eventtypes(self):
        """:obj:`baroque.datastructures.bags.EventTypesBag`: bag containing the
         event types of this topic"""
        return self.types

    def touch(self):
        """Sets the current time as timestamp of this topic"""
        self.timestamp = ts.utc_now()

    def json(self):
        """Dumps this object to a JSON string.

        Returns:
            str

        """
        data = dict(id=self.id, owner=self.owner, description=self.description, eventtypes=[str(et) for et in self.types], tags=list(self.tags), timestamp=ts.stringify(self.timestamp))
        return dumps(data)

    def md5(self):
        """Returns the MD5 hash of this object.

        Returns:
            str

        """
        m = hashlib.md5()
        m.update(self.json().encode('utf-8'))
        return m.hexdigest()

    def __repr__(self):
        return '<{}.{} - name: {} - owner: {} - eventtypes: {}>'.format(__name__, self.__class__.__name__, self.name, self.owner or 'None', ', '.join([str(et) for et in self.types]) or 'None')
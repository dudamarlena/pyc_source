# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/__init__.py
# Compiled at: 2018-07-14 05:05:32
# Size of source mod 2**32: 10893 bytes
__all__ = [
 'location', 'node', 'container', 'endpoint', 'volume', 'process', 'tunnel', 'docker']
import logging, re, weakref, shortuuid
from messidge.client.connection import Connection
from typing import Optional, Union, List
from base64 import b64encode
from _thread import allocate_lock

class Waitable:
    __doc__ = 'An object that can be waited on (until marked as ready)'

    def __init__(self, locked: Optional[bool]=True):
        self.wait_lock = allocate_lock()
        if locked:
            self.wait_lock.acquire()

    def __del__(self):
        if self.wait_lock.locked():
            self.wait_lock.release()

    def wait_until_ready(self, timeout: Optional[int]=60):
        """Blocks waiting for a (normally asynchronous) update indicating the object is ready.

        :param timeout: An optional timeout in seconds.
        :return: self"""
        acquired = self.wait_lock.acquire(timeout=timeout)
        if not acquired:
            raise TimeoutError('wait_until_ready timed out')
        self.wait_lock.release()
        return self

    def is_ready(self) -> bool:
        """:return: True if object is ready."""
        return not self.wait_lock.locked()

    def mark_as_ready(self):
        if self.wait_lock.locked():
            self.wait_lock.release()

    def mark_not_ready(self):
        if not self.wait_lock.locked():
            self.wait_lock.acquire()


class Killable:

    def __init__(self):
        self.dead = False

    def mark_as_dead(self):
        self.dead = True

    def bail_if_dead(self):
        if self.dead:
            logging.debug('Object was previously terminated (carrying on): ' + self.__repr__())
        return self.dead

    def ensure_alive(self):
        if self.dead:
            raise ValueError('Cannot call method on a terminated object: ' + self.__repr__())


class Connectable:
    __doc__ = 'A resource that can be connected to in the private IP space.'

    def __init__(self, conn: Connection, uuid: str, node, ip):
        self.conn = weakref.ref(conn)
        self.uuid = uuid
        self.node_pk = node if isinstance(node, bytes) else node.pk
        self.ip = ip

    def allow_connection_from(self, obj):
        """Allow bidirectional communication between this object and the parameter.

        :param obj: An object that has an ip."""
        self.conn().send_blocking_cmd(b'allow_connection', {'node':self.node_pk,  'container':self.uuid, 
         'ip':obj.ip})
        self.conn().send_blocking_cmd(b'ping', {'node':obj.node_pk,  'container':obj.uuid, 
         'ip':self.ip})
        logging.info('Allowed connection (from %s) on: %s' % (obj.uuid.decode(), self.uuid))

    def disallow_connection_from(self, obj):
        """Disallow bidirectional communication between this object and one that was previously allowed to connect.

        :param obj: An object that has an ip."""
        self.conn().send_cmd(b'disallow_connection', {'node':self.node_pk,  'container':self.uuid, 
         'ip':obj.ip})
        logging.info('Disallowed connection (from %s) on: %s' % (obj.uuid.decode(), self.uuid))


class Taggable:
    __doc__ = 'A resource that might have a globally advertisable tag.'
    tag_re = re.compile(b'\\A[^0-9a-z\\-_.]*\\Z')
    short_uuid_re = re.compile(b'\\A[' + shortuuid.get_alphabet().encode() + b']{22}\\Z')

    def __init__(self, user: Union[(str, bytes)], uuid: Union[(str, bytes)], tag: Optional[Union[(str, bytes)]]=None):
        if user is None or uuid is None:
            raise RuntimeError('Taggable resources must be constructed with at least a pk and uuid')
        else:
            if isinstance(user, str):
                self.user = user.encode()
            else:
                self.user = user
            if isinstance(uuid, str):
                self.uuid = uuid.encode()
            else:
                self.uuid = uuid
        self.tag = None if tag is None else Taggable.valid_tag(tag)

    def uuid_key(self) -> (
 bytes, bytes):
        """:return: the owner (user) pk and uuid of this object."""
        return (
         self.user, self.uuid)

    def tag_key(self) -> (
 bytes, bytes):
        """:return: the owner (user) pk and tag of this object (or None)."""
        if self.tag is None:
            return (None, None)
        return (
         self.user, self.tag)

    @staticmethod
    def valid_tag(tag: Union[(bytes, str)]) -> Union[(bytes, None)]:
        if tag is None:
            return
        if len(tag) == 0:
            raise ValueError('Tag passed for approval was blank')
        tag = tag.lower()
        if isinstance(tag, str):
            tag = tag.encode()
        if Taggable.tag_re.search(tag) is not None:
            raise ValueError('Tag names can only use 0-9 a-z - _ and .')
        if Taggable.short_uuid_re.match(tag) is not None:
            raise ValueError('Tag names cannot look like UUIDs')
        return tag

    def display_name(self) -> str:
        """:return: the object's uuid, or uuid:tag pair (as a string) if possible."""
        if self.tag is None:
            return self.uuid.decode()
        return self.uuid.decode() + ':' + self.tag.decode()

    def global_display_name(self) -> str:
        return b64encode(self.user).decode() + ':' + self.display_name()


class TaggedCollection:
    __doc__ = 'A collection of taggable objects.'

    def __init__(self, initial: Optional[List[Taggable]]=None):
        self.objects = {}
        self.uuid_uuidkey = {}
        self.uniques = 0
        if initial is not None:
            for init in initial:
                self.add(init)

    def __del__(self):
        for obj in self.objects.values():
            del obj

        self.objects = {}

    def __call__(self, *args, **kwargs) -> set:
        """Calling the tagged collection as if a function.

        :return: a set of unique values"""
        return self.values()

    def __len__(self) -> int:
        """Calling len on the collection.

        :return: the number of unique values."""
        return self.uniques

    def __getitem__(self, uuid: Union[(str, bytes)]):
        """Dereference the collection just as you would for a dict, passing the uuid.

        :param uuid: the uuid of the object to retrieve.
        :return: the object (or raises KeyError)."""
        if isinstance(uuid, str):
            uuidkey = self.uuid_uuidkey[uuid.encode()]
        else:
            uuidkey = self.uuid_uuidkey[uuid]
        return self.objects[uuidkey]

    def __contains__(self, uuid: Union[(str, bytes)]) -> bool:
        """Test to see if a given uuid is 'in' the collection.

        :param uuid: the uuid of the object to test for.
        :return: boolean"""
        try:
            self[uuid]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        raise RuntimeError("Tagged collection can only be inserted to with the 'add' method")

    def __iter__(self):
        raise RuntimeError('Cannot iterate over a tagged collection')

    def add(self, obj: Taggable):
        if self.will_clash(obj.user, obj.uuid, obj.tag):
            raise RuntimeError('Cannot add to TaggedCollection because there will be a namespace clash')
        self.objects[obj.uuid_key()] = obj
        self.uuid_uuidkey[obj.uuid] = obj.uuid_key()
        if obj.tag_key() is not None:
            self.objects[obj.tag_key()] = obj
        self.uniques += 1

    def get(self, user: Union[(bytes, str)], key: Union[(bytes, str)]):
        """Fetch an object given the user PK and a uuid, tag, or uuid:tag

        :param user: User PK
        :param key: Either the object uuid, tag, or 'uuid:tag' as a format.
        :return: The reference object or a KeyError."""
        if key is None:
            raise RuntimeError('Key not passed when fetching from TaggedCollection')
        else:
            if isinstance(user, str):
                user = user.encode()
            if isinstance(key, str):
                key = key.encode()
            parts = key.split(b':')
            if len(parts) > 2:
                raise ValueError('Too many parts in tag: ' + key.decode())
            try:
                return self.objects[(user, parts[0])]
            except KeyError:
                raise KeyError('Failed to get from a TaggedCollection with user=%s key=%s' % (user, key))

    def remove(self, obj: Taggable):
        del self.objects[obj.uuid_key()]
        del self.uuid_uuidkey[obj.uuid]
        if obj.tag_key() in self.objects:
            del self.objects[obj.tag_key()]
        self.uniques -= 1

    def will_clash(self, user: bytes, uuid: bytes, tag: bytes) -> bool:
        if tag is not None:
            if (
             user, tag) in self.objects:
                return True
        if (
         user, uuid) in self.objects:
            return True
        return False

    def values(self) -> set:
        """:return: A set of unique values"""
        return set(self.objects.values())

    def __repr__(self):
        return '<TaggedCollection uniques=%d>' % self.uniques
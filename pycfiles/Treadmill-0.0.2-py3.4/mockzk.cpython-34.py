# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/test/mockzk.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 7808 bytes
"""Mock Zookeeper TestCase.

Usage::

  class MyTest(MockZookeeperTestCase):

      @mock.patch('zookeeper.get', mock.Mock())
      @mock.patch('zookeeper.get_children', mock.Mock())
      def test_some_zk_ops(self):
          zkdata = {
            'foo': {
                'bar': '123'
            }
          }

          self.make_mock_zk(zkdata)

          # call funcs that will call zookeeper.get / get_children
          zkdata['foo']['bla'] = '456'

          # The watcher will be invoked, and get_children will return
          # ['bla', 'bar']
          self.notify(zookeeper.CHILD_EVENT, '/foo')

"""
import copy, queue, threading, time, unittest
from collections import namedtuple
import kazoo
from kazoo.protocol import states
import yaml

class MockZookeeperMetadata(namedtuple('MockZookeeperMetadata', [
 'czxid',
 'ctime',
 'mzxid',
 'mtime',
 'ephemeralOwner'])):
    __doc__ = 'Subset of the Zookeeper metadata we are using.'
    _BASE_ZXID = int(time.time())

    @property
    def creation_transaction_id(self):
        """creation_transaction_id getter."""
        return self.czxid

    @property
    def last_modified_transaction_id(self):
        """last_modified_transaction_id getter."""
        return self.mzxid

    @property
    def created(self):
        """created getter."""
        return self.ctime / 100.0

    @property
    def last_modified(self):
        """last_modified getter."""
        return self.mtime / 100.0

    @classmethod
    def from_dict(cls, value_dict):
        """Create a Metadata instance from dict values."""
        curr_time = time.time()
        zxid = int(cls._BASE_ZXID + curr_time)
        timestamp_ms = int(curr_time * 100)
        ctime = value_dict.get('ctime', timestamp_ms)
        czxid = value_dict.get('czxid', zxid)
        mtime = value_dict.get('mtime', timestamp_ms)
        mzxid = value_dict.get('mzxid', zxid)
        ephemeralOwner = value_dict.get('ephemeralOwner', 0)
        if 'creation_transaction_id' in value_dict:
            czxid = value_dict['creation_transaction_id']
        if 'created' in value_dict:
            ctime = int(value_dict['created'] * 100)
        if 'last_modified_transaction_id' in value_dict:
            mzxid = value_dict['last_modified_transaction_id']
        if 'last_modified' in value_dict:
            mtime = int(value_dict['last_modified'] * 100)
        return cls(ctime=ctime, czxid=czxid, mtime=mtime, mzxid=mzxid, ephemeralOwner=ephemeralOwner)


class MockZookeeperTestCase(unittest.TestCase):
    __doc__ = 'Helper class to mock Zk get[children] events.'

    def setUp(self):
        super(MockZookeeperTestCase, self).setUp()
        self.watch_events = None

    def tearDown(self):
        """Send terminate signal to mock Zk events thread."""
        if self.watch_events:
            self.watch_events.put('exit')

    def make_mock_zk(self, zk_content, events=False):
        """Constructs zk mock implementation of get based on dictionary.

        Treats dictionary as tree structure, mapping it into mock Zk instance.
        """
        watches = {}

        def mock_exists(zkpath, watch=None):
            """Mocks node exists."""
            del watch
            path = zkpath.split('/')
            path.pop(0)
            content = zk_content
            while path:
                path_component = path.pop(0)
                if path_component not in content:
                    return False
                content = content[path_component]

            return True

        def mock_delete(zkpath, recursive=False):
            """Mocks node deletion."""
            del recursive
            path = zkpath.split('/')
            path.pop(0)
            last = path.pop(-1)
            content = zk_content
            while path:
                path_component = path.pop(0)
                if path_component not in content:
                    raise kazoo.client.NoNodeError()
                content = content[path_component]

            if last not in content:
                raise kazoo.client.NoNodeError()
            else:
                del content[last]

        def mock_get(zkpath, watch=None):
            """Traverse data recursively, return the node content."""
            path = zkpath.split('/')
            path.pop(0)
            content = zk_content
            while path:
                path_component = path.pop(0)
                if path_component not in content:
                    raise kazoo.client.NoNodeError()
                content = content[path_component]

            content = copy.copy(content)
            meta_dict = {}
            if isinstance(content, dict):
                meta_values = content.pop('.metadata', {})
                meta_dict.update(meta_values)
                data = content.pop('.data', yaml.dump(content))
            else:
                data = content
            metadata = MockZookeeperMetadata.from_dict(meta_dict)
            watches[(zkpath, states.EventType.CHANGED)] = watch
            return (
             data, metadata)

        def mock_get_children(zkpath, watch=None):
            """Traverse data recursively, returns element keys."""
            path = zkpath.split('/')
            path.pop(0)
            content = zk_content
            while path:
                path_component = path.pop(0)
                content = content[path_component]

            watches[(zkpath, states.EventType.CHILD)] = watch
            if isinstance(content, dict):
                return sorted(content.keys())
            else:
                return []

        if events:
            self.watch_events = queue.Queue()

            def run_events():
                """Invoke watcher callback for each event."""
                while 1:
                    event = self.watch_events.get()
                    if event == 'exit':
                        break
                    delay, event_type, state, path = event
                    if delay:
                        time.sleep(delay)
                    watch = watches.get((path, event_type), None)
                    if watch:
                        watch(states.WatchedEvent(type=event_type, state=state, path=path))
                        continue

            threading.Thread(target=run_events).start()
        side_effects = [
         (
          kazoo.client.KazooClient.exists, mock_exists),
         (
          kazoo.client.KazooClient.get, mock_get),
         (
          kazoo.client.KazooClient.delete, mock_delete),
         (
          kazoo.client.KazooClient.get_children, mock_get_children)]
        for mthd, side_effect in side_effects:
            try:
                mthd.side_effect = side_effect
            except AttributeError:
                pass

    def notify(self, event_type, path, state=states.KazooState.CONNECTED, delay=None):
        """Notify watchers of the event."""
        self.watch_events.put((delay, event_type, state, path))
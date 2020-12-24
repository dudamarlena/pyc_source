# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/joshua/Dropbox/code/pyrostest/lib/python3.4/site-packages/pyrostest/ros_test.py
# Compiled at: 2017-10-29 18:21:06
# Size of source mod 2**32: 6335 bytes
__doc__ = "Utilities that deal with creating fake rosnodes for testing.\n\nContains tools to send and recieve data from fake nodes and topics. This is\nneeded because ROS doesn't allow you to run multiple nodes from the same\nprocess, so instead we have to set up a background process and communicate with\nit over the system.\n"
import contextlib, os, pkg_resources, subprocess, time, threading, six
from six import StringIO
from six.moves import cPickle as pickle
import unittest, pyrostest.rostest_utils
FileNotFoundError = IOError

class TimeoutError(Exception):
    """TimeoutError"""
    pass


class NoMessage(Exception):
    """NoMessage"""
    pass


class NoNode(Exception):
    """NoNode"""
    pass


def _resolve_location(binary_name):
    """Find the location of a mock node to run.
    """
    location = pkg_resources.resource_filename(__name__, binary_name)
    if not os.path.isfile(location):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(this_dir, '..', 'data')
        location = os.path.join(data_dir, binary_name)
    if not os.path.isfile(location):
        raise FileNotFoundError('{} cannot be located'.format(location))
    return location


class MockPublisher(object):
    """MockPublisher"""

    def __init__(self, topic, msg_type, queue_size):
        self.topic = topic
        self.msg_type = msg_type
        pub_data = pickle.dumps((topic, msg_type, queue_size))
        location = _resolve_location('publisher.py')
        self.proc = subprocess.Popen(['python', location, pub_data], stdin=subprocess.PIPE)

    def send(self, value):
        """Sends data to be publoshed to the mocked topic.
        """
        time.sleep(0.5)
        value.serialize(self.proc.stdin)

    def kill(self):
        """Kills the publisher ros node process.
        """
        self.proc.kill()
        self.proc.wait()


class MockSubscriber(object):
    """MockSubscriber"""

    def __init__(self, topic, msg_type, timeout):
        self.timeout = timeout
        self.topic = topic
        self.msg_type = msg_type
        self.killed = False
        location = _resolve_location('subscriber.py')
        self.proc = subprocess.Popen(['python', location,
         pickle.dumps((topic, msg_type))], stdout=subprocess.PIPE)
        self._message = None

    def kill(self):
        """Kills the subscriber ros node process.
        """
        self.proc.kill()
        self.proc.wait()

    @property
    def message(self):
        """Getter for the message property.

        Makes sure you've actually recieved a message before providing one.
        """
        if not self._message:
            msg = self.msg_type()
            sio = StringIO()
            msg.serialize(sio)

            def kill_proc():
                """Kills the proccess and sets a flag to raise an error.
                """
                self.proc.kill()
                self.killed = True

            timer = threading.Timer(self.timeout, kill_proc)
            try:
                timer.start()
                data = self.proc.stdout.read(sio.len)
            finally:
                timer.cancel()

            if self.killed:
                raise TimeoutError('No message published to {} within {} seconds. Needed {} bytes, got {}.'.format(self.topic, self.timeout, sio.len, len(data)))
            msg.deserialize(data)
            self._message = msg
        return self._message


def _check_is_availible(topic, prefix, rosmaster_uri, event):
    no_ns = topic.split('/')[(-1)]
    while not any(nn.split('/')[(-1)].startswith(''.join([prefix, '_', no_ns])) for nn in pyrostest.rostest_utils.my_get_node_names(uri=rosmaster_uri)):
        time.sleep(0.1)

    event.set()


def _await_node(topic, prefix, rosmaster_uri, timeout):
    """Helper to block until a node is availible in ROS.
    """
    is_accessed = threading.Event()
    bg = threading.Thread(name='wait for node', target=_check_is_availible, args=(
     topic, prefix, rosmaster_uri, is_accessed))
    bg.start()
    is_accessed.wait(timeout)
    if not is_accessed.isSet():
        raise NoNode('No node was created for "{}", in namespace "{}"'.format(topic, prefix))


@six.add_metaclass(pyrostest.rostest_utils.RosTestMeta)
class RosTest(unittest.TestCase):
    """RosTest"""

    def __init__(self, *args, **kwargs):
        super(RosTest, self).__init__(*args, **kwargs)
        self.LAUNCHER = dict()

    @contextlib.contextmanager
    def check_topic(self, topic, rosmsg_type, timeout=10, node_timeout=10):
        """Context manager that monitors a rostopic and gets a message sent to
        it.
        """
        test_node = MockSubscriber(topic, rosmsg_type, timeout=timeout)
        _await_node(topic, 'mock_subscribe', self.rosmaster_uri, timeout=node_timeout)
        try:
            yield test_node
        finally:
            test_node.kill()

    @contextlib.contextmanager
    def mock_pub(self, topic, rosmsg_type, queue_size=1, node_timeout=10):
        """Mocks a node and cleans it up when done.
        """
        pub = MockPublisher(topic, rosmsg_type, queue_size)
        _await_node(topic, 'mock_publish', self.rosmaster_uri, timeout=node_timeout)
        try:
            yield pub
        finally:
            pub.kill()
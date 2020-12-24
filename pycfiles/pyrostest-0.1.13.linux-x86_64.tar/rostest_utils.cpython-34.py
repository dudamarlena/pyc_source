# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joshua/Dropbox/code/pyrostest/lib/python3.4/site-packages/pyrostest/rostest_utils.py
# Compiled at: 2017-06-11 13:34:05
# Size of source mod 2**32: 3300 bytes
"""A collection of utilities to make testing with ros less painful.
"""
import os, functools, random, socket, subprocess, time, psutil, rosgraph, rosnode

def my_get_node_names(namespace=None, uri='http://localhost:11311'):
    """Monkeypatches get_node_names with a non-default ROS_MASTER_URI.
    """
    old_master = rosgraph.Master
    rosgraph.Master = functools.partial(rosgraph.Master, master_uri=uri)
    nodenames = rosnode.get_node_names(namespace=namespace)
    rosgraph.Master = old_master
    return nodenames


def rand_port():
    """Picks a random port number.

    This is potentially unsafe, but shouldn't generally be a problem.
    """
    return random.randint(10311, 12311)


class RosTestMeta(type):
    __doc__ = 'Metaclass for RosTest that adds the setup/teardown we want.\n    '

    def __new__(mcs, name, bases, dct):

        def noop(_):
            """Do nothing function.

            This is injected if there is no user-defined setUp or tearDown
            method on an instance of RosTest.
            """
            pass

        try:
            old_setup = dct['setUp']
        except KeyError:
            old_setup = noop

        try:
            old_teardown = dct['tearDown']
        except KeyError:
            old_teardown = noop

        def new_setup(self):
            """Wrapper around the user-defined setUp method that runs roscore.
            """
            self.port = rand_port()
            self.rosmaster_uri = 'http://{}:{}'.format(socket.gethostname(), self.port)
            env = {k:v for k, v in os.environ.iteritems()}
            env.update({'ROS_MASTER_URI': self.rosmaster_uri})
            roscore_initialized = False
            while not roscore_initialized:
                self.roscore = subprocess.Popen([
                 'roscore', '-p', str(self.port)], env=env)
                time.sleep(1)
                if not self.roscore.poll():
                    roscore_initialized = True
                else:
                    self.roscore.kill()
                    self.roscore = None

            old_setup(self)

        def new_teardown(self):
            """Wrapper around the user-defined tearDown method to end roscore.
            """
            proc = psutil.Process(self.roscore.pid)
            children = proc.children(recursive=True)
            old_teardown(self)
            self.roscore.kill()
            self.roscore.wait()
            self.roscore = None
            for child in children:
                try:
                    child.terminate()
                    child.wait()
                except psutil.NoSuchProcess:
                    pass

        dct['setUp'] = new_setup
        dct['tearDown'] = new_teardown
        dct['setUp'].__name__ = 'setUp'
        dct['tearDown'].__name__ = 'tearDown'
        return super(RosTestMeta, mcs).__new__(mcs, name, bases, dct)
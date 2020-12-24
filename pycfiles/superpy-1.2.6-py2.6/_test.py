# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpyTesting\_test.py
# Compiled at: 2010-06-04 07:07:10
"""Module to test some superpy stuff.
"""
import unittest, socket, time, logging, threading, re, os
from superpy.core import Tasks, Servers, PicklingXMLRPC, Process

class BasicTest(unittest.TestCase):
    """Basic test case.

>>> import sys; sys.path.insert(0,'..')
>>> import logging; logging.getLogger('').setLevel(logging.DEBUG)
>>> import _test
>>> classToTest = _test.BasicTest
>>> testNames = [n for n in dir(classToTest) if n[0:4]=='test']
>>> for name in testNames:
...     logging.debug('Testing %s' % name)
...     t = _test.BasicTest(methodName=name)
...     t.debug()
... 
Entering service loop forever or until killed...
HI
Entering service loop forever or until killed...
Entering service loop forever or until killed...
hello
Entering service loop forever or until killed...
    """
    portIncrement = 10

    def setUp(self):
        """Set up the test.

        Note that since the unittest module runs the different tests at
        unpredictable times, it is important to make sure that each time
        the setUp method is called, we use a different port.
        We also want to prevent these from conflicting with actual ports
        used by real users.
        """
        BasicTest.portIncrement += 1
        port = Servers.BasicRPCServer.defaultPort + BasicTest.portIncrement
        self.server = Servers.BasicRPCServer(cpus=1, port=port)
        self.server.serve_forever_as_thread()
        logging.debug('Starting server on port %i' % port)
        self.scheduler = Servers.Scheduler([
         (
          socket.gethostname(), self.server._port)])
        self.checkThreadCount = False

    def tearDown(self):
        """Shutdown the server after test is finished."""
        logging.debug('Terminating server')
        self.server.Terminate()
        oldtimeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(5)
        try:
            try:
                connection = PicklingXMLRPC.PicklingServerProxy('http://%s:%i' % (getattr(self.server, '_host'),
                 getattr(self.server, '_port')))
                connection.system.listMethods()
            except Exception, e:
                logging.error('Unable to contact server: %s; it probably shutdown' % str(e))

        finally:
            socket.setdefaulttimeout(oldtimeout)

        time.sleep(1)
        self.assertEqual(False, getattr(self.server, '_thread').isAlive())
        if self.checkThreadCount:
            self.assertEqual(1, threading.activeCount(), 'While running %s\n            Some non-main threads still survive: %s' % (
             self._testMethodName, str(threading.enumerate())))
        else:
            logging.warning('not checking threadcount...')
        logging.debug('Finished teardown.')

    def testMain(self):
        """Main test to see if we can submit tasks."""
        myScript = Tasks.ImportPyTask.MakeSimpleScript('\ndef Go():\n    print "hello"\n    return "hello"\n')
        task = Tasks.ImportPyTask(myScript, name='printhello')
        handle = self.scheduler.SubmitTaskToBestServer(task)
        handle = handle.WaitForUpdatedHandle()
        self.failUnless(handle.finished)
        self.assertEqual(type(handle.result), str)
        self.assertEqual('imported modName, did Go, got hello, done', handle.result.replace('\r', ''))

    def testErrorHandling(self):
        """Make sure the server can keep going despite task exceptions."""
        myScript = Tasks.ImportPyTask.MakeSimpleScript('\ndef Go():\n    frooble # cause error\n')
        task = Tasks.ImportPyTask(myScript, name='causeError')
        handle = self.scheduler.SubmitTaskToBestServer(task)
        time.sleep(3)
        handle = handle.WaitForUpdatedHandle()
        self.failUnless(handle.finished)
        self.failUnless(re.compile("Exception of type '<type '[a-zA-Z.]+NameError'>':[ ]+'global name 'frooble' is not defined").search(handle.result))
        self.assertEqual([True, True, False], [ getattr(handle, n) for n in [
         'started', 'finished', 'alive']
                                              ])
        self.assertEqual(-1, self.scheduler.hosts.values()[0].CPULoad())

    def testRemoveTask(self):
        """Make sure we can remove tasks."""
        target = Process._ExampleForTest(delay=999999)
        task = Tasks.ImpersonatingTask(target, os.getcwd(), name='mySleeper')
        handle = self.scheduler.SubmitTaskToBestServer(task)
        connection = PicklingXMLRPC.PicklingServerProxy('http://%s:%i' % (handle.host, handle.port))
        self.assertEqual(0, connection.CPULoad())
        connection.RemoveFromQueue(handle)
        self.assertEqual(-1, connection.CPULoad())

    def testCleanOldTasks(self):
        """Test the CleanOldTasks method."""
        myScript = Tasks.ImportPyTask.MakeSimpleScript("\nimport time\ndef Go():\n    print 'HI'\n    return 'HI'\n")
        task = Tasks.ImportPyTask(myScript, name='printHI')
        handle = self.scheduler.SubmitTaskToBestServer(task)
        handle = handle.WaitForUpdatedHandle()
        if not handle.finished:
            raise Exception('Waited for handle but it did not finish.')
        self.assertEqual(type(handle.result), str)
        self.assertEqual('imported modName, did Go, got HI, done', handle.result.replace('\r', ''))
        connection = PicklingXMLRPC.PicklingServerProxy('http://%s:%i' % (handle.host, handle.port))
        time.sleep(2)
        cleaned = connection.CleanOldTasks(0)
        self.assertEqual(cleaned, ['printHI'])
        self.assertEqual(connection.ShowQueue(), [])
        time.sleep(3)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
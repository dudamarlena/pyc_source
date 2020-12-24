# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/TemplateCmdLineIface.py
# Compiled at: 2019-09-22 10:12:27
try:
    from io import BytesIO, TextIOWrapper
except ImportError:
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

from tempfile import NamedTemporaryFile
import os, pickle, sys, unittest
from Cheetah.Template import Template
from Cheetah.TemplateCmdLineIface import CmdLineIface

class TestHelp(unittest.TestCase):

    def setUp(self):
        self.NULL = NULL = open(os.devnull, 'w')
        sys.stdout = NULL

    def tearDown(self):
        self.NULL.close()
        sys.stdout = sys.__stdout__

    def test_help(self):
        klass = Template.compile(source='$foo')
        t = klass()
        cmdline = CmdLineIface(t, scriptName='test', cmdLineArgs=['-h'])
        self.assertRaises(SystemExit, cmdline._processCmdLineArgs)


class TestEnv(unittest.TestCase):

    def setUp(self):
        os.environ['foo'] = 'test foo'

    def tearDown(self):
        del os.environ['foo']

    def test_env(self):
        klass = Template.compile(source='$foo')
        t = klass()
        cmdline = CmdLineIface(t, scriptName='test', cmdLineArgs=['--env'])
        cmdline._processCmdLineArgs()
        assert str(t) == 'test foo'


class TestPickleStdin(unittest.TestCase):

    def setUp(self):
        pickle_bytes = pickle.dumps({'foo': 'test foo'})
        if hasattr(sys.stdin, 'buffer'):
            sys.stdin = TextIOWrapper(BytesIO(pickle_bytes))
        else:
            sys.stdin = BytesIO(pickle_bytes)

    def tearDown(self):
        sys.stdin = sys.__stdin__

    def test_pickle_stdin(self):
        klass = Template.compile(source='$foo')
        t = klass()
        cmdline = CmdLineIface(t, scriptName='test', cmdLineArgs=[
         '--pickle=-'])
        cmdline._processCmdLineArgs()
        assert str(t) == 'test foo'


class TestPickleFile(unittest.TestCase):

    def setUp(self):
        self.pickle_file = pickle_file = NamedTemporaryFile(mode='wb', delete=False)
        pickle.dump({'foo': 'test foo'}, pickle_file)
        pickle_file.close()

    def tearDown(self):
        os.remove(self.pickle_file.name)

    def test_pickle_file(self):
        klass = Template.compile(source='$foo')
        t = klass()
        cmdline = CmdLineIface(t, scriptName='test', cmdLineArgs=[
         '--pickle', self.pickle_file.name])
        cmdline._processCmdLineArgs()
        assert str(t) == 'test foo'
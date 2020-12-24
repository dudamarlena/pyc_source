# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/test_pidbaseagent.py
# Compiled at: 2011-12-02 15:01:12
import nose.tools, os, shutil, tempfile
from inqbus.ocf.agents.pidbaseagent import PIDBaseAgent
from inqbus.ocf.generic.exits import OCF_ERR_PERM

class Param(object):
    """
            Class mocking inqbus.ocf.generig.parameter.OCFType
            """

    def __init__(self, value):
        self.value = value


TEST_CLASSES = [
 PIDBaseAgent]

class TestPidBaseAgent(object):

    def setUp(self):
        """
        Build a config Directory and a file
        """
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = tempfile.mkstemp(dir=self.temp_dir)[1]

    def teardown(self):
        """
        Remove the temp_dir recursively
        """
        os.chmod(self.temp_dir, 511)
        shutil.rmtree(self.temp_dir)

    def test_validator_good_dir(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_dir = Param(self.temp_dir)
            agent.validate_dir(param_dir)

    def test_validator_bad_dir(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_dir = Param(self.temp_dir + 'XXXX')
            error = OCF_ERR_PERM
            nose.tools.assert_raises(error, agent.validate_dir, param_dir)

    def test_validator_noread_dir(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_dir = Param(self.temp_dir + 'XXXX')
            os.chmod(self.temp_dir, 219)
            error = OCF_ERR_PERM
            nose.tools.assert_raises(error, agent.validate_dir, param_dir)

    def test_validator_good_file(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file)
            agent.validate_file(param_file)

    def test_validator_bad_file(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file + 'XXXX')
            error = OCF_ERR_PERM
            nose.tools.assert_raises(error, agent.validate_file, param_file)

    def test_validator_noread_file(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file)
            os.chmod(self.temp_file, 219)
            error = OCF_ERR_PERM

        if os.geteuid() != 0:
            nose.tools.assert_raises(error, agent.validate_file, param_file)

    def test_validator_good_executable(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file)
            os.chmod(self.temp_file, 448)
            agent.validate_executable(param_file)

    def test_validator_bad_executable(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file)
            param_file = Param(self.temp_file + 'XXXX')
            error = OCF_ERR_PERM
            nose.tools.assert_raises(error, agent.validate_executable, param_file)

    def test_validator_noexec_executable(self):
        self.TEST_CLASSES = TEST_CLASSES
        for TestClass in self.TEST_CLASSES:
            agent = TestClass()
            param_file = Param(self.temp_file)
            os.chmod(self.temp_file, 438)
            error = OCF_ERR_PERM
            nose.tools.assert_raises(error, agent.validate_executable, param_file)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/unittest_base.py
# Compiled at: 2020-04-12 16:44:21
# Size of source mod 2**32: 8869 bytes
import logging, os, platform, signal, time, subprocess, sys, unittest
from urllib.request import urlopen
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
from pyvirtualdisplay import Display
logging.basicConfig(level=(logging.WARN))
mylogger = logging.getLogger()
PORT = '8081'
HOST_ADDRESS = '127.0.0.1:' + PORT
HOST_URL = 'http://' + HOST_ADDRESS
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = sys.platform.startswith('linux')
mf = None

class ModuleFixture(unittest.TestCase):

    def __init__(self, module_path, exit_status_success=True):
        super(ModuleFixture, self).__init__()
        self.base_path = os.path.dirname(module_path)
        self.exit_status_success = exit_status_success
        if IS_WINDOWS:
            if self.base_path == '':
                self.base_path = '.'

    def setUpModule(self):
        global mf
        self.old_cwd = os.getcwd()
        os.chdir(self.base_path)
        p = subprocess.Popen([
         'runestone', 'build', '--all'],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          universal_newlines=True)
        self.build_stdout_data, self.build_stderr_data = p.communicate()
        print(self.build_stdout_data + self.build_stderr_data)
        if self.exit_status_success:
            self.assertFalse(p.returncode)
        else:
            if IS_WINDOWS:
                netstat_output = subprocess.run([
                 'netstat', '-no'],
                  universal_newlines=True,
                  stdout=(subprocess.PIPE)).stdout
                for connection in netstat_output.splitlines()[4:]:
                    proto, local_address, foreign_address, state, pid = connection.split()
                    pid = int(pid)
                    if local_address == HOST_ADDRESS and pid != 0:
                        os.kill(pid, 0)

            else:
                lsof_output = subprocess.run([
                 'lsof', '-i', ':{0}'.format(PORT)],
                  universal_newlines=True,
                  stdout=(subprocess.PIPE)).stdout
                for process in lsof_output.split('\n')[1:]:
                    data = [x for x in process.split(' ') if x != '']
                    if len(data) <= 1:
                        continue
                    ptokill = int(data[1])
                    mylogger.warn('Attempting to kill a stale runestone serve process: {}'.format(ptokill))
                    os.kill(ptokill, signal.SIGKILL)
                    time.sleep(2)
                    try:
                        os.kill(ptokill, 0)
                        pytest.exit("Stale runestone server can't kill process: {}".format(ptokill))
                    except ProcessLookupError:
                        pass
                    except PermissionError:
                        pytest.exit('Another server is using port {} process: {}'.format(PORT, ptokill))
                    except Exception:
                        pytest.exit('Unknown error while trying to kill stale runestone server')

            self.runestone_server = subprocess.Popen([
             sys.executable, '-m', 'runestone', 'serve', '--port', PORT])
            if IS_LINUX:
                self.display = Display(visible=0, size=(1280, 1024))
                self.display.start()
            else:
                self.display = None
        options = Options()
        options.add_argument('--window-size=1200,800')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        mf = self
        for tries in range(50):
            try:
                urlopen(HOST_URL, timeout=5)
            except URLError:
                time.sleep(0.1)
            else:
                break

    def tearDownModule(self):
        global mf
        self.driver.quit()
        if self.display:
            self.display.stop()
        self.runestone_server.kill()
        os.chdir(self.old_cwd)
        mf = None

    def runTest(self):
        pass


def module_fixture_maker(module_path, return_mf=False, exit_status_success=True):
    mf = ModuleFixture(module_path, exit_status_success)
    if return_mf:
        return (
         mf, mf.setUpModule, mf.tearDownModule)
    return (mf.setUpModule, mf.tearDownModule)


class RunestoneTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = mf.driver
        self.host = HOST_URL

    def tearDown(self):
        self.driver.execute_script('window.localStorage.clear();')
        self.driver.execute_script('window.sessionStorage.clear();')
        self.driver.delete_all_cookies()
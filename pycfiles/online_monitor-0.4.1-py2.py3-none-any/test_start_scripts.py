# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/testing/test_start_scripts.py
# Compiled at: 2018-07-05 04:39:41
""" Script to check the online monitor.
"""
import unittest, yaml, subprocess, time, os, psutil, online_monitor

def create_config_yaml():
    conf = {}
    devices = {}
    devices['DAQ0'] = {'backend': 'tcp://127.0.0.1:6500', 'kind': 'example_producer_sim', 
       'delay': 1}
    devices['DAQ1'] = {'backend': 'tcp://127.0.0.1:6501', 'kind': 'example_producer_sim', 
       'delay': 1}
    conf['producer_sim'] = devices
    devices = {}
    devices['DUT0'] = {'kind': 'example_converter', 
       'frontend': 'tcp://127.0.0.1:6500', 
       'backend': 'tcp://127.0.0.1:6600', 
       'threshold': 8}
    devices['DUT1'] = {'kind': 'forwarder', 
       'frontend': 'tcp://127.0.0.1:6600', 
       'backend': 'tcp://127.0.0.1:6601'}
    conf['converter'] = devices
    devices = {}
    devices['DUT0'] = {'kind': 'example_receiver', 
       'frontend': 'tcp://127.0.0.1:6600'}
    devices['DUT1'] = {'kind': 'example_receiver', 
       'frontend': 'tcp://127.0.0.1:6600'}
    conf['receiver'] = devices
    return yaml.dump(conf, default_flow_style=False)


def kill(proc):
    process = psutil.Process(proc.pid)
    for child_proc in process.children(recursive=True):
        child_proc.kill()

    process.kill()


def run_script_in_shell(script, arguments, command=None):
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0
    return subprocess.Popen('%s %s %s' % ('python' if not command else command,
     script, arguments), shell=True, creationflags=creationflags)


class TestStartScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(os.path.dirname(__file__), 'tmp_cfg_2.yml')
        with open(cls.config_path, 'w') as (outfile):
            config_file = create_config_yaml()
            outfile.write(config_file)
        if os.getenv('TRAVIS', False):
            from xvfbwrapper import Xvfb
            cls.vdisplay = Xvfb()
            cls.vdisplay.start()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.config_path)
        time.sleep(1)

    def test_start_converter(self):
        converter_process = run_script_in_shell('', self.config_path, 'start_converter')
        time.sleep(0.5)
        kill(converter_process)
        time.sleep(0.5)
        self.assertNotEqual(converter_process.poll(), None)
        return

    def test_start_producer_sim(self):
        producer_sim_process = run_script_in_shell('', self.config_path, 'start_producer_sim')
        time.sleep(0.5)
        kill(producer_sim_process)
        time.sleep(0.5)
        self.assertNotEqual(producer_sim_process.poll(), None)
        return

    def test_start_online_monitor(self):
        online_monitor_process = run_script_in_shell('', self.config_path, 'start_online_monitor')
        time.sleep(1)
        kill(online_monitor_process)
        time.sleep(1)
        self.assertNotEqual(online_monitor_process.poll(), None)
        return

    def test_online_monitor(self):
        online_monitor_process = run_script_in_shell('', self.config_path, 'online_monitor')
        time.sleep(0.5)
        kill(online_monitor_process)
        time.sleep(0.5)
        self.assertNotEqual(online_monitor_process.poll(), None)
        return


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStartScripts)
    unittest.TextTestRunner(verbosity=2).run(suite)
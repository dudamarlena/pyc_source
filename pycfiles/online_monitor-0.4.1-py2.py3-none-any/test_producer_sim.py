# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/testing/test_producer_sim.py
# Compiled at: 2019-06-26 09:06:51
""" Script to check the producer simulation of the online monitor.
"""
import unittest, yaml, subprocess, time, os, zmq, psutil, online_monitor
package_path = os.path.dirname(online_monitor.__file__)
producer_sim_script_path = os.path.join(package_path, 'start_producer_sim.py')

def create_producer_config_yaml(n_producer):
    conf, devices = {}, {}
    for index in range(n_producer):
        devices['DAQ%s' % index] = {'backend': 'tcp://127.0.0.1:55%02d' % index, 
           'kind': 'example_producer_sim', 
           'delay': 0.02}

    conf['producer_sim'] = devices
    return yaml.dump(conf, default_flow_style=False)


def kill(proc):
    process = psutil.Process(proc.pid)
    for child_proc in process.children(recursive=True):
        child_proc.kill()

    process.kill()


def run_script_in_shell(script, arguments):
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0
    return subprocess.Popen('python %s %s' % (script, arguments), shell=True, creationflags=creationflags)


def run_script_in_process(script, arguments):
    if os.name == 'nt':
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0
    return subprocess.Popen(['python', script, arguments], shell=False, creationflags=creationflags)


class TestConverter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(os.path.dirname(__file__), 'tmp_cfg_5_producer.yml')
        with open(cls.config_path, 'w') as (outfile):
            config_file = create_producer_config_yaml(5)
            outfile.write(config_file)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.config_path)

    def test_converter_communication(self):
        producer_process = run_script_in_shell(producer_sim_script_path, self.config_path)
        time.sleep(1.5)
        have_data = []
        context = zmq.Context()
        for index in range(5):
            receiver = context.socket(zmq.SUB)
            receiver.connect('tcp://127.0.0.1:55%02d' % index)
            receiver.setsockopt_string(zmq.SUBSCRIBE, '')
            time.sleep(5)
            try:
                receiver.recv_json(flags=zmq.NOBLOCK)
                have_data.append(True)
            except zmq.Again:
                have_data.append(False)

            receiver.close()

        kill(producer_process)
        time.sleep(1)
        context.term()
        time.sleep(2)
        self.assertTrue(all(have_data), 'Did not receive any data')
        self.assertNotEqual(producer_process.poll(), None)
        return


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConverter)
    unittest.TextTestRunner(verbosity=2).run(suite)
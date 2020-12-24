# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/testing/test_utils.py
# Compiled at: 2019-06-26 09:09:59
""" Script to check the online converter of the online monitor.
"""
import unittest, yaml, os, numpy as np, json
from testfixtures import log_capture
from online_monitor.utils import utils, producer_sim
from online_monitor.converter.transceiver import Transceiver
from online_monitor.receiver.receiver import Receiver

def create_forwarder_config_yaml(n_converter):
    conf, devices = {}, {}
    for index in range(n_converter):
        devices['DUT%s' % index] = {'kind': 'forwarder', 
           'frontend': 'tcp://127.0.0.1:55%02d' % index, 
           'backend': 'tcp://127.0.0.1:55%02d' % (index + 1)}

    conf['converter'] = devices
    return yaml.dump(conf, default_flow_style=False)


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config_path = os.path.join(os.path.dirname(__file__), 'tmp_cfg_10_converter.yml')
        cls.configuration = create_forwarder_config_yaml(10)
        with open(cls.config_path, 'w') as (outfile):
            outfile.write(cls.configuration)
        cls.configuration = yaml.safe_load(cls.configuration)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.config_path)

    @log_capture()
    def test_argument_parser(self, log):
        arguments = utils.parse_args(['configfile.yaml', '-l DEBUG'])
        self.assertEqual(arguments.config_file, 'configfile.yaml', 'The non positional argument is parsed wrong')
        self.assertTrue('DEBUG' in arguments.log, 'The logging argument parse fails')
        with self.assertRaises(IOError):
            utils.parse_config_file('Does_not_exist')
        configuration = utils.parse_config_file(self.config_path)
        self.assertEqual(configuration, self.configuration)
        utils.parse_config_file(self.config_path, expect_receiver=True)
        log.check(('root', 'WARNING',
         'No receiver specified, thus no data can be plotted. Change %s!' % self.config_path))

    def test_numpy_serializer(self):
        data = {'array': np.ones((100, 101))}
        data_serialized = json.dumps(data, cls=utils.NumpyEncoder)
        data_deserialized = json.loads(data_serialized, object_hook=utils.json_numpy_obj_hook)
        self.assertTrue((data['array'] == data_deserialized['array']).all())
        data = {'array': np.ones((100, 101)).T}
        data_serialized = json.dumps(data, cls=utils.NumpyEncoder)
        data_deserialized = json.loads(data_serialized, object_hook=utils.json_numpy_obj_hook)
        self.assertTrue((data['array'] == data_deserialized['array']).all())
        data = {
         'array', (1, 2, 3)}
        with self.assertRaises(TypeError):
            json.dumps(data, cls=utils.NumpyEncoder)
        data = {'array': np.ones((100, ), dtype=[('event_number', '<i8'),
                   ('trigger_number', '<u4')])}
        data_serialized = json.dumps(data, cls=utils.NumpyEncoder)
        data_deserialized = json.loads(data_serialized, object_hook=utils.json_numpy_obj_hook)
        self.assertTrue((data['array'] == data_deserialized['array']).all())

    def test_simple_encoder(self):
        data = np.ones((100, 101))
        meta = {'a': 1, 'b': '2'}
        data_buffer = utils.simple_enc(data, meta)
        data_des, meta_des = utils.simple_dec(data_buffer)
        self.assertTrue(np.all(data == data_des))
        self.assertTrue(meta == meta_des)

    def test_entity_loader(self):
        utils.load_converter('forwarder', base_class_type=Transceiver, *(), **{'frontend': '0', 'backend': '1', 
           'kind': 'forwarder', 
           'name': 'DUT'})
        utils.load_converter('example_converter', base_class_type=Transceiver, *(), **{'frontend': '0', 'backend': '1', 
           'kind': 'example_converter', 
           'name': 'DUT'})
        utils.load_receiver('example_receiver', base_class_type=Receiver, *(), **{'frontend': '0', 'kind': 'example_receiver', 
           'name': 'DUT'})
        utils.load_producer_sim('example_producer_sim', base_class_type=producer_sim.ProducerSim, *(), **{'backend': '0', 'kind': 'example_producer_sim', 
           'name': 'DUT'})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)
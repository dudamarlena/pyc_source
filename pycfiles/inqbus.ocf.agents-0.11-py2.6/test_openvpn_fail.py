# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/test/test_openvpn_fail.py
# Compiled at: 2011-12-02 14:54:57
import os, shutil, tempfile, nose.tools
from inqbus.ocf.agents.openvpn import OpenVPN
from inqbus.ocf.generic.exits import OCF_NOT_RUNNING

class TestOpenvpnRunBase:
    """
    Test the basic actions 
    """

    def setUp(self):
        """
        Installing valid filesystem information so the validation of the paramters will pass.
        """
        ovpn_name = 'test'
        self.temp_dir = tempfile.mkdtemp()
        conf_file_name = os.path.join(self.temp_dir, '%s.conf' % ovpn_name)
        log_file_name = os.path.join(self.temp_dir, '%s.log' % ovpn_name)
        stat_file_name = os.path.join(self.temp_dir, '%s.status' % ovpn_name)
        secret_file_name = os.path.join(self.temp_dir, '%s.sec' % ovpn_name)
        conf_file = open(conf_file_name, 'w')
        conf_file.write('\n    local 127.0.0.1\n    port 1194\n    proto udp\n    dev tun\n    \n    XXXXXXXXXXXXXXXXXXXX ERROR IN CONFIG FILE XXXXXXXXXXXXXXXXXXXXXXXXX\n    persist-tun\n    status %s\n    log-append %s\n    secret %s\n    verb 0\n    ' % (stat_file_name, log_file_name, secret_file_name))
        conf_file.close()
        secret_file = open(secret_file_name, 'w')
        secret_file.write('\n    #\n    # 2048 bit OpenVPN static key\n    #\n    -----BEGIN OpenVPN Static key V1-----\n    4ec99f2e9c12e1128fbfa9b3634cecfe\n    be36c1868342232a9c3332049e8c6a5d\n    cb98b91ff04a522d4ea6e59e481be70d\n    38bdead8607fc9367a1d8b7d1d558164\n    2ffa1e377f48685cf3cdfcaeef639d21\n    2ff9c6570127d34c57c6dc0e6ad1677b\n    f7f9fb15d0244b5de0a0e71083089dde\n    0e224ab5b2171a32a120a8735c9be7de\n    df277a7d90c34bcf323005f33d7fb8e7\n    3766888f3a18529059e6d7666179861a\n    a7c9119d0ef908cd45af2dcca94190fb\n    09624ac49130494e1fc72fa0d2378ba2\n    8e89f0754355742bbfd020730238cb15\n    20097756e1404de3b388f026b30d6697\n    34f232afc77004b890e8f9a945feaa81\n    641264b6c03669a1c67bd7d1098adc90\n    -----END OpenVPN Static key V1-----\n    ')
        secret_file.close()
        os.environ['OCF_RESKEY_ovpn_run_dir'] = self.temp_dir
        os.environ['OCF_RESKEY_ovpn_conf_dir'] = self.temp_dir
        os.environ['OCF_RESKEY_ovpn_pid_dir'] = self.temp_dir
        os.environ['OCF_RESKEY_ovpn_name'] = ovpn_name

    def teardown(self):
        """
        Remove the temp_dir recursively. Remove the environamt parameters
        """
        shutil.rmtree(self.temp_dir)
        del os.environ['OCF_RESKEY_ovpn_run_dir']
        del os.environ['OCF_RESKEY_ovpn_conf_dir']
        del os.environ['OCF_RESKEY_ovpn_pid_dir']
        del os.environ['OCF_RESKEY_ovpn_name']

    def test_base_actions(self):
        self.TEST_CLASSES = [
         OpenVPN]
        for TestClass in self.TEST_CLASSES:
            for sysargv in ['start']:
                yield (
                 self.do_bad_action, TestClass, sysargv)

    def do_bad_action(self, TestClass, sysargv):
        """
        worker function for test_bad_actions
        """
        nose.tools.assert_raises(OCF_NOT_RUNNING, TestClass().run, sysargv)
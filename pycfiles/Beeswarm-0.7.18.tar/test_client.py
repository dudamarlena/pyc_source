# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/tests/test_client.py
# Compiled at: 2016-11-12 07:38:04
import unittest, tempfile, shutil, os
from beeswarm.drones.client.client import Client

class ClientTests(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_client_startup(self):
        config = {'general': {'id': 1234, 'fetch_ip': True}, 'beeswarm_server': {'zmq_command_url': 'tcp://127.0.0.1:5713', 
                               'zmq_url': 'tcp://127.0.0.1:5712', 
                               'zmq_own_public': [
                                                '#   ****  Generated on 2015-01-13 21:02:44.933568 by pyzmq  ****\n',
                                                '#   ZeroMQ CURVE Public Certificate\n',
                                                '#   Exchange securely, or use a secure mechanism to verify the contents\n',
                                                '#   of this file after exchange. Store public certificates in your home\n',
                                                '#   directory, in the .curve subdirectory.\n',
                                                '\n',
                                                'metadata\n',
                                                'curve\n',
                                                '    public-key = "LeZkQ^HXijnRahQkp$&nxpu6Hh>7YHBOzbz[iJg^"\n'], 
                               'zmq_own_private': [
                                                 '#   ****  Generated on 2015-01-13 21:02:44.933568 by pyzmq  ****\n',
                                                 '#   ZeroMQ CURVE **Secret** Certificate\n',
                                                 '#   DO NOT PROVIDE THIS FILE TO OTHER USERS nor change its permissions.\n',
                                                 '\n',
                                                 'metadata\n',
                                                 'curve\n',
                                                 '    public-key = "LeZkQ^HXijnRahQkp$&nxpu6Hh>7YHBOzbz[iJg^"\n',
                                                 '    secret-key = "B{(o5Hpx{[D3}>f*O{NZ(}.e3o5Xh+eO9-fmt0tb"\n'], 
                               'zmq_server_public': [
                                                   '#   ****  Generated on 2015-01-13 20:59:19.308358 by pyzmq  ****\n',
                                                   '#   ZeroMQ CURVE Public Certificate\n',
                                                   '#   Exchange securely, or use a secure mechanism to verify the contents\n',
                                                   '#   of this file after exchange. Store public certificates in your home\n',
                                                   '#   directory, in the .curve subdirectory.\n',
                                                   '\n',
                                                   'metadata\n',
                                                   'curve\n',
                                                   '    public-key = "^xk>t(V(bj70]=zl.uX=)#@kYwlgjitkfrVo!I+="\n']}}
        client = Client(self.tmp_dir, config)
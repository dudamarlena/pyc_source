# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_base.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import os
from .. import Pyrpl, APP, user_config_dir, global_config
from ..pyrpl_utils import time
from ..async_utils import sleep as async_sleep
from ..errors import UnexpectedPyrplError, ExpectedPyrplError
logger_quamash = logging.getLogger(name='quamash')
logger_quamash.setLevel(logging.INFO)

class TestPyrpl(object):
    """ base class for all pyrpl tests """
    source_config_file = 'nosetests_source.yml'
    tmp_config_file = 'nosetests_config.yml'
    curves = []
    OPEN_ALL_DOCKWIDGETS = False

    @classmethod
    def erase_temp_file(self):
        tmp_conf = os.path.join(user_config_dir, self.tmp_config_file)
        if os.path.isfile(tmp_conf):
            try:
                os.remove(tmp_conf)
            except WindowsError:
                pass

        while os.path.exists(tmp_conf):
            pass

    @classmethod
    def setUpAll(cls):
        print '=======SETTING UP %s=============' % cls.__name__
        cls.erase_temp_file()
        cls.pyrpl = Pyrpl(config=cls.tmp_config_file, source=cls.source_config_file)
        cls.r = cls.pyrpl.rp
        N = 10
        t0 = time()
        for i in range(N):
            cls.r.hk.led

        cls.read_time = (time() - t0) / float(N)
        t0 = time()
        for i in range(N):
            cls.r.hk.led = 0

        cls.write_time = (time() - t0) / float(N)
        cls.communication_time = (cls.read_time + cls.write_time) / 2.0
        print 'Estimated time per read / write operation: %.1f ms / %.1f ms' % (
         cls.read_time * 1000.0, cls.write_time * 1000.0)
        async_sleep(0.1)
        if cls.OPEN_ALL_DOCKWIDGETS:
            for name, dock_widget in cls.pyrpl.widgets[0].dock_widgets.items():
                print 'Showing widget %s...' % name
                dock_widget.setVisible(True)

            async_sleep(3.0)
        APP.processEvents()

    def test_read_write_time(self):
        try:
            maxtime = global_config.test.max_communication_time
        except:
            raise ExpectedPyrplError('Error with global config file. Please delete the file %s and retry!' % os.path.join(user_config_dir, 'global_config.yml'))

        assert self.read_time < maxtime, 'Read operation is very slow: %e s (expected < %e s). It is highly recommended that you improve the network connection to your Red Pitaya device. ' % (
         self.read_time, maxtime)
        assert self.write_time < maxtime, 'Write operation is very slow: %e s (expected < %e s). It is highly recommended that you improve the network connection to your Red Pitaya device. ' % (
         self.write_time, maxtime)

    @classmethod
    def tearDownAll(cls):
        print '=======TEARING DOWN %s===========' % cls.__name__
        if hasattr(cls, 'curves'):
            while len(cls.curves) > 0:
                cls.curves.pop().delete()

        cls.pyrpl._clear()
        APP.processEvents()
        cls.erase_temp_file()
        APP.processEvents()

    def test_pyrpl(self):
        assert self.pyrpl is not None
        return
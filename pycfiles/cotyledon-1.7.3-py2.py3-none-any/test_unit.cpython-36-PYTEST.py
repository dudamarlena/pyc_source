# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/tests/test_unit.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 2534 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, mock, cotyledon
from cotyledon.tests import base

class FakeService(cotyledon.Service):
    pass


class SomeTest(base.TestCase):

    def setUp(self):
        super(SomeTest, self).setUp()
        cotyledon.ServiceManager._process_runner_already_created = False

    def test_forking_slowdown(self):
        sm = cotyledon.ServiceManager()
        sm.add(FakeService, workers=3)
        with mock.patch('time.sleep') as (sleep):
            sm._slowdown_respawn_if_needed()
            sm._slowdown_respawn_if_needed()
            sm._slowdown_respawn_if_needed()
            sm._slowdown_respawn_if_needed()
            sm._slowdown_respawn_if_needed()
            sm._slowdown_respawn_if_needed()
            self.assertEqual(6, len(sleep.mock_calls))

    def test_invalid_service(self):
        sm = cotyledon.ServiceManager()
        self.assertRaisesMsg(ValueError, "'service' must be a callable", sm.add, 'foo')
        self.assertRaisesMsg(ValueError,
          "'workers' must be an int >= 1, not: None (NoneType)",
          (sm.add),
          FakeService, workers=None)
        self.assertRaisesMsg(ValueError,
          "'workers' must be an int >= 1, not: -2 (int)",
          (sm.add),
          FakeService, workers=(-2))
        oid = sm.add(FakeService, workers=3)
        self.assertRaisesMsg(ValueError,
          "'workers' must be an int >= -2, not: -5 (int)",
          (sm.reconfigure),
          oid, workers=(-5))
        self.assertRaisesMsg(ValueError,
          "notexists service id doesn't exists",
          (sm.reconfigure),
          'notexists', workers=(-1))

    def assertRaisesMsg(self, exc, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exc as e:
            self.assertEqual(msg, str(e))
        else:
            self.assertFalse(True, '%r have not been raised' % exc)
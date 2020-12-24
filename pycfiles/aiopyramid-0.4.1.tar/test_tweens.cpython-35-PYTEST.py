# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/tests/test_tweens.py
# Compiled at: 2017-05-26 18:35:31
# Size of source mod 2**32: 2824 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest, asyncio, greenlet
from aiopyramid.helpers import spawn_greenlet, run_in_greenlet

class TestTweens(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def _make_tweens(self):
        from pyramid.config.tweens import Tweens
        return Tweens()

    def _async_tween_factory(self, handler, registry):

        @asyncio.coroutine
        def _async_action():
            yield from asyncio.sleep(0.2)
            return 12

        def async_tween(request):
            this = greenlet.getcurrent()
            future = asyncio.Future()
            sub_task = asyncio.ensure_future(run_in_greenlet(this, future, _async_action))
            self.assertIsInstance(sub_task, asyncio.Future)
            this.parent.switch(sub_task)
            self.assertEqual(future.result(), 12)
            return future

        return async_tween

    def _dummy_tween_factory(self, handler, registry):
        return handler

    def test_async_tween(self):
        out = self.loop.run_until_complete(spawn_greenlet(self._async_tween_factory(None, None), None))
        self.assertEqual(out, 12)

    def test_example_tween(self):
        from aiopyramid.tweens import coroutine_logger_tween_factory
        out = self.loop.run_until_complete(spawn_greenlet(coroutine_logger_tween_factory(lambda x: x, None), None))
        self.assertEqual(None, out)

    def test_sync_tween_above(self):
        tweens = self._make_tweens()
        tweens.add_implicit('async', self._async_tween_factory)
        tweens.add_implicit('sync', self._dummy_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)

    def test_sync_tween_below(self):
        tweens = self._make_tweens()
        tweens.add_implicit('sync', self._dummy_tween_factory)
        tweens.add_implicit('async', self._async_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)

    def test_sync_both(self):
        tweens = self._make_tweens()
        tweens.add_implicit('sync', self._dummy_tween_factory)
        tweens.add_implicit('async', self._async_tween_factory)
        tweens.add_implicit('sync', self._dummy_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)


class TestTweensGunicorn(unittest.TestCase):
    __doc__ = ' Test aiopyramid tweens gunicorn style. '
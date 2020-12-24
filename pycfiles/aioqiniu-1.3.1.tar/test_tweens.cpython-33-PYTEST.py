# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/tests/test_tweens.py
# Compiled at: 2014-09-25 19:04:58
# Size of source mod 2**32: 2816 bytes
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
            sub_task = asyncio.async(run_in_greenlet(this, future, _async_action))
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
        return

    def test_example_tween(self):
        from aiopyramid.tweens import coroutine_logger_tween_factory
        out = self.loop.run_until_complete(spawn_greenlet(coroutine_logger_tween_factory(lambda x: x, None), None))
        self.assertEqual(None, out)
        return

    def test_sync_tween_above(self):
        tweens = self._make_tweens()
        tweens.add_implicit('async', self._async_tween_factory)
        tweens.add_implicit('sync', self._dummy_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)
        return

    def test_sync_tween_below(self):
        tweens = self._make_tweens()
        tweens.add_implicit('sync', self._dummy_tween_factory)
        tweens.add_implicit('async', self._async_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)
        return

    def test_sync_both(self):
        tweens = self._make_tweens()
        tweens.add_implicit('sync', self._dummy_tween_factory)
        tweens.add_implicit('async', self._async_tween_factory)
        tweens.add_implicit('sync', self._dummy_tween_factory)
        chain = tweens(None, None)
        out = self.loop.run_until_complete(spawn_greenlet(chain, None))
        self.assertEqual(out, 12)
        return


class TestTweensGunicorn(unittest.TestCase):
    """TestTweensGunicorn"""
    pass
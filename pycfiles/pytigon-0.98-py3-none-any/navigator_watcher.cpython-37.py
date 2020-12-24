# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyppeteer/pyppeteer/navigator_watcher.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 5766 bytes
"""Navigator Watcher module."""
import asyncio, concurrent.futures
from typing import Any, Awaitable, Dict, List, Union
from pyppeteer import helper
from pyppeteer.errors import TimeoutError
from pyppeteer.frame_manager import FrameManager, Frame
from pyppeteer.util import merge_dict

class NavigatorWatcher:
    __doc__ = 'NavigatorWatcher class.'

    def __init__(self, frameManager: FrameManager, frame: Frame, timeout: int, options: Dict=None, **kwargs: Any) -> None:
        """Make new navigator watcher."""
        options = merge_dict(options, kwargs)
        self._validate_options(options)
        self._frameManager = frameManager
        self._frame = frame
        self._initialLoaderId = frame._loaderId
        self._timeout = timeout
        self._hasSameDocumentNavigation = False
        self._eventListeners = [
         helper.addEventListener(self._frameManager, FrameManager.Events.LifecycleEvent, self._checkLifecycleComplete),
         helper.addEventListener(self._frameManager, FrameManager.Events.FrameNavigatedWithinDocument, self._navigatedWithinDocument),
         helper.addEventListener(self._frameManager, FrameManager.Events.FrameDetached, self._checkLifecycleComplete)]
        self._loop = self._frameManager._client._loop
        self._lifecycleCompletePromise = self._loop.create_future()
        self._navigationPromise = self._loop.create_task(asyncio.wait([
         self._lifecycleCompletePromise,
         self._createTimeoutPromise()],
          return_when=(concurrent.futures.FIRST_COMPLETED)))
        self._navigationPromise.add_done_callback(lambda fut: self._cleanup())

    def _validate_options(self, options: Dict) -> None:
        if 'networkIdleTimeout' in options:
            raise ValueError('`networkIdleTimeout` option is no longer supported.')
        elif 'networkIdleInflight' in options:
            raise ValueError('`networkIdleInflight` option is no longer supported.')
        else:
            if options.get('waitUntil') == 'networkidle':
                raise ValueError('`networkidle` option is no logner supported. Use `networkidle2` instead.')
            if options.get('waitUntil') == 'documentloaded':
                import logging
                logging.getLogger(__name__).warning('`documentloaded` option is no longer supported. Use `domcontentloaded` instead.')
            _waitUntil = options.get('waitUntil', 'load')
            if isinstance(_waitUntil, list):
                waitUntil = _waitUntil
            else:
                if isinstance(_waitUntil, str):
                    waitUntil = [
                     _waitUntil]
                else:
                    raise TypeError(f"`waitUntil` option should be str or list of str, but got type {type(_waitUntil)}")
        self._expectedLifecycle = []
        for value in waitUntil:
            protocolEvent = pyppeteerToProtocolLifecycle.get(value)
            if protocolEvent is None:
                raise ValueError(f"Unknown value for options.waitUntil: {value}")
            self._expectedLifecycle.append(protocolEvent)

    def _createTimeoutPromise(self) -> Awaitable[None]:
        self._maximumTimer = self._loop.create_future()
        if self._timeout:
            errorMessage = f"Navigation Timeout Exceeded: {self._timeout} ms exceeded."

            async def _timeout_func():
                await asyncio.sleep(self._timeout / 1000)
                self._maximumTimer.set_exception(TimeoutError(errorMessage))

            self._timeout_timer = self._loop.create_task(_timeout_func())
        else:
            self._timeout_timer = self._loop.create_future()
        return self._maximumTimer

    def navigationPromise(self) -> Any:
        """Return navigation promise."""
        return self._navigationPromise

    def _navigatedWithinDocument(self, frame: Frame=None) -> None:
        if frame != self._frame:
            return
        self._hasSameDocumentNavigation = True
        self._checkLifecycleComplete()

    def _checkLifecycleComplete(self, frame: Frame=None) -> None:
        if self._frame._loaderId == self._initialLoaderId:
            if not self._hasSameDocumentNavigation:
                return
        else:
            if not self._checkLifecycle(self._frame, self._expectedLifecycle):
                return
            self._lifecycleCompletePromise.done() or self._lifecycleCompletePromise.set_result(None)

    def _checkLifecycle(self, frame: Frame, expectedLifecycle: List[str]) -> bool:
        for event in expectedLifecycle:
            if event not in frame._lifecycleEvents:
                return False

        for child in frame.childFrames:
            if not self._checkLifecycle(child, expectedLifecycle):
                return False

        return True

    def cancel(self) -> None:
        """Cancel navigation."""
        self._cleanup()

    def _cleanup(self) -> None:
        helper.removeEventListeners(self._eventListeners)
        self._lifecycleCompletePromise.cancel()
        self._maximumTimer.cancel()
        self._timeout_timer.cancel()


pyppeteerToProtocolLifecycle = {'load':'load', 
 'domcontentloaded':'DOMContentLoaded', 
 'documentloaded':'DOMContentLoaded', 
 'networkidle0':'networkIdle', 
 'networkidle2':'networkAlmostIdle'}
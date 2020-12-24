# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/pyppeteer/pyppeteer/worker.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 3588 bytes
"""Worker module."""
import logging
from typing import Any, Callable, Dict, List, TYPE_CHECKING
from pyee import EventEmitter
from pyppeteer.execution_context import ExecutionContext, JSHandle
from pyppeteer.helper import debugError
if TYPE_CHECKING:
    from pyppeteer.connection import CDPSession
logger = logging.getLogger(__name__)

class Worker(EventEmitter):
    __doc__ = "The Worker class represents a WebWorker.\n\n    The events `workercreated` and `workerdestroyed` are emitted on the page\n    object to signal the worker lifecycle.\n\n    .. code::\n\n        page.on('workercreated', lambda worker: print('Worker created:', worker.url))\n    "

    def __init__(self, client, url, consoleAPICalled, exceptionThrown):
        super().__init__()
        self._client = client
        self._url = url
        self._loop = client._loop
        self._executionContextPromise = self._loop.create_future()

        def jsHandleFactory(remoteObject: Dict) -> JSHandle:
            pass

        def onExecutionContentCreated(event):
            nonlocal jsHandleFactory

            def jsHandleFactory(remoteObject):
                return JSHandle(executionContext, client, remoteObject)

            executionContext = ExecutionContext(client, event['context'], jsHandleFactory)
            self._executionContextCallback(executionContext)

        self._client.on('Runtime.executionContextCreated', onExecutionContentCreated)
        try:
            self._client.send('Runtime.enable', {})
        except Exception as e:
            try:
                debugError(logger, e)
            finally:
                e = None
                del e

        def onConsoleAPICalled(event):
            args = []
            for arg in event.get('args', []):
                args.append(jsHandleFactory(arg))

            consoleAPICalled(event['type'], args)

        self._client.on('Runtime.consoleAPICalled', onConsoleAPICalled)
        self._client.on('Runtime.exceptionThrown', lambda exception: exceptionThrown(exception['exceptionDetails']))

    def _executionContextCallback(self, value: ExecutionContext) -> None:
        self._executionContextPromise.set_result(value)

    @property
    def url(self) -> str:
        """Return URL."""
        return self._url

    async def executionContext(self) -> ExecutionContext:
        """Return ExecutionContext."""
        return await self._executionContextPromise

    async def evaluate(self, pageFunction: str, *args: Any) -> Any:
        """Evaluate ``pageFunction`` with ``args``.

        Shortcut for ``(await worker.executionContext).evaluate(pageFunction, *args)``.
        """
        return await ((await self._executionContextPromise).evaluate)(pageFunction, *args)

    async def evaluateHandle(self, pageFunction: str, *args: Any) -> JSHandle:
        """Evaluate ``pageFunction`` with ``args`` and return :class:`~pyppeteer.execution_context.JSHandle`.

        Shortcut for ``(await worker.executionContext).evaluateHandle(pageFunction, *args)``.
        """
        return await ((await self._executionContextPromise).evaluateHandle)(pageFunction, *args)
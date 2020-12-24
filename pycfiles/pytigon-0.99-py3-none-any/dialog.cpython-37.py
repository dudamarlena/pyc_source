# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/pyppeteer/pyppeteer/dialog.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 2264 bytes
"""Dialog module."""
from types import SimpleNamespace
from pyppeteer.connection import CDPSession

class Dialog(object):
    __doc__ = 'Dialog class.\n\n    Dialog objects are dispatched by page via the ``dialog`` event.\n\n    An example of using ``Dialog`` class:\n\n    .. code::\n\n        browser = await launch()\n        page = await browser.newPage()\n\n        async def close_dialog(dialog):\n            print(dialog.message)\n            await dialog.dismiss()\n            await browser.close()\n\n        page.on(\n            \'dialog\',\n            lambda dialog: asyncio.ensure_future(close_dialog(dialog))\n        )\n        await page.evaluate(\'() => alert("1")\')\n    '
    Type = SimpleNamespace(Alert='alert',
      BeforeUnload='beforeunload',
      Confirm='confirm',
      Prompt='prompt')

    def __init__(self, client: CDPSession, type: str, message: str, defaultValue: str='') -> None:
        self._client = client
        self._type = type
        self._message = message
        self._handled = False
        self._defaultValue = defaultValue

    @property
    def type(self) -> str:
        """Get dialog type.

        One of ``alert``, ``beforeunload``, ``confirm``, or ``prompt``.
        """
        return self._type

    @property
    def message(self) -> str:
        """Get dialog message."""
        return self._message

    @property
    def defaultValue(self) -> str:
        """If dialog is prompt, get default prompt value.

        If dialog is not prompt, return empty string (``''``).
        """
        return self._defaultValue

    async def accept(self, promptText: str='') -> None:
        """Accept the dialog.

        * ``promptText`` (str): A text to enter in prompt. If the dialog's type
          is not prompt, this does not cause any effect.
        """
        self._handled = True
        await self._client.send('Page.handleJavaScriptDialog', {'accept':True, 
         'promptText':promptText})

    async def dismiss(self) -> None:
        """Dismiss the dialog."""
        self._handled = True
        await self._client.send('Page.handleJavaScriptDialog', {'accept': False})
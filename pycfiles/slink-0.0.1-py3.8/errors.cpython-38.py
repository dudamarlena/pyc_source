# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slink/core/errors.py
# Compiled at: 2020-04-12 10:26:46
# Size of source mod 2**32: 755 bytes
from colorama import Fore, Style

class SLinkError(RuntimeError):
    _default_message = 'Unknown_error'
    _default_code = 'error'

    def __init__(self, code=None, message=None, *args, **kwargs):
        (super().__init__)(message, *args, **kwargs)
        self.code = code or self._default_code
        self.message = message or self._default_message

    def __str__(self):
        return f"[{Fore.RED + self.code + Style.RESET_ALL}] {self.message}"


class WrongResponse(SLinkError):
    _default_message = 'Server sent wrong response'


class NoResponse(SLinkError):
    _default_message = 'Server does not respond'


class Forbidden(WrongResponse):
    _default_message = 'Forbidden error. Please check your access token and limits'
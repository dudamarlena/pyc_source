# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slink/core/utils.py
# Compiled at: 2020-04-12 09:01:47
# Size of source mod 2**32: 574 bytes
import enum, click, requests.exceptions
from core.errors import SLinkError, NoResponse

class SERVICES(enum.Enum):
    BITLY = 'bitly'


class ErrorHandlingGroup(click.Group):

    def __call__(self, *args, **kwargs):
        try:
            return (self.main)(*args, **kwargs)
            except SLinkError as e:
            try:
                click.echo(str(e))
            finally:
                e = None
                del e


def reraise_requests(f):

    def deco(*args, **kwargs):
        try:
            return f(*args, **kwargs)
            except requests.exceptions.ConnectTimeout as e:
            try:
                raise NoResponse from e
            finally:
                e = None
                del e

    return deco
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/authentication.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1270 bytes
from ...errors import MatrixResponseError
from ...api import Method, Path
from .types import UserID
from .base import BaseClientAPI

class ClientAuthenticationMethods(BaseClientAPI):
    __doc__ = '\n    Methods in section 5 Authentication of the spec. These methods are used for setting and getting user\n    metadata and searching for users.\n\n    See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#client-authentication>`__\n    '

    async def whoami(self) -> UserID:
        """
        Get information about the current user.

        Returns:
            The user ID of the current user.
        """
        resp = await self.api.request(Method.GET, Path.account.whoami)
        try:
            return resp['user_id']
        except KeyError:
            raise MatrixResponseError('`user_id` not in response.')
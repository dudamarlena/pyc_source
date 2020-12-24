# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/filtering.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2162 bytes
from ...errors import MatrixResponseError
from ...api import Method, Path
from .base import BaseClientAPI
from .types import Filter, FilterID, Serializable

class FilteringMethods(BaseClientAPI):
    __doc__ = '\n    Methods in section 7 Filtering of the spec.\n\n    Filters can be created on the server and can be passed as as a parameter to APIs which return\n    events. These filters alter the data returned from those APIs. Not all APIs accept filters.\n\n    See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#filtering>`__\n    '

    async def get_filter(self, filter_id: FilterID) -> Filter:
        """
        Download a filter.

        See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#get-matrix-client-r0-user-userid-filter-filterid>`__

        Args:
            filter_id: The filter ID to download.

        Returns:
            The filter data.
        """
        content = await self.api.request(Method.GET, Path.user[self.mxid].filter[filter_id])
        return Filter.deserialize(content)

    async def create_filter(self, filter_params: Filter) -> FilterID:
        """
        Upload a new filter definition to the homeserver.

        See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#post-matrix-client-r0-user-userid-filter>`__

        Args:
            filter_params: The filter data.

        Returns:
            A filter ID that can be used in future requests to refer to the uploaded filter.
        """
        resp = await self.api.request(Method.POST, Path.user[self.mxid].filter, filter_params.serialize() if isinstance(filter_params, Serializable) else filter_params)
        try:
            return resp['filter_id']
        except KeyError:
            raise MatrixResponseError('`filter_id` not in response.')
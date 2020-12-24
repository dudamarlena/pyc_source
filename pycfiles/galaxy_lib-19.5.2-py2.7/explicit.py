# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/container_resolvers/explicit.py
# Compiled at: 2019-04-28 04:54:30
"""This module describes the :class:`ExplicitContainerResolver` ContainerResolver plugin."""
import logging
from ..container_resolvers import ContainerResolver
log = logging.getLogger(__name__)

class ExplicitContainerResolver(ContainerResolver):
    """Find explicit containers referenced in the tool description (e.g. tool XML file) if present."""
    resolver_type = 'explicit'

    def resolve(self, enabled_container_types, tool_info, **kwds):
        """Find a container explicitly mentioned in tool description.

        This ignores the tool requirements and assumes the tool author crafted
        a correct container.
        """
        for container_description in tool_info.container_descriptions:
            if self._container_type_enabled(container_description, enabled_container_types):
                return container_description

        return


class ExplicitSingularityContainerResolver(ExplicitContainerResolver):
    resolver_type = 'explicit_singularity'
    container_type = 'singularity'

    def resolve(self, enabled_container_types, tool_info, **kwds):
        """Find a container explicitly mentioned in tool description.

        This ignores the tool requirements and assumes the tool author crafted
        a correct container. We use singularity here to fetch docker containers,
        hence the container_description hack here.
        """
        for container_description in tool_info.container_descriptions:
            if container_description.type == 'docker':
                desc_dict = container_description.to_dict()
                desc_dict['type'] = self.container_type
                desc_dict['identifier'] = 'docker://%s' % container_description.identifier
                container_description = container_description.from_dict(desc_dict)
            if self._container_type_enabled(container_description, enabled_container_types):
                return container_description

        return


__all__ = ('ExplicitContainerResolver', 'ExplicitSingularityContainerResolver')
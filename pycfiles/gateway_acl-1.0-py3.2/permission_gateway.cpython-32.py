# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/gateway/permission_gateway.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 23, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that adds the Gateway objects based on ACL permissions.
"""
from acl.api.access import Access
from ally.container.support import setup
from ally.design.processor.attribute import defines, requires, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor, Handler
from collections import Iterable
from gateway.api.gateway import Gateway
import itertools, re
HEADER_FILTER_INPUT = 'Filter-Input'
PROPERTY_NAME = 'Property'

class Solicit(Context):
    """
    The solicit context.
    """
    gateways = defines(Iterable, doc='\n    @rtype: Iterable(Gateway)\n    The ACL gateways.\n    ')
    rootURI = optional(str)
    replacements = optional(dict)
    permissions = requires(Iterable)


class Permission(Context):
    """
    The permission context.
    """
    navigate = optional(str)
    access = requires(Access)
    filters = requires(dict)


@setup(Handler, name='registerPermissionGateway')
class RegisterPermissionGatewayHandler(HandlerProcessor):
    """
    Provides the handler that adds the Gateway objects based on ACL permissions.
    """

    def __init__(self):
        super().__init__(Permission=Permission)

    def process(self, chain, solicit: Solicit, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Adds the access permissions gateways.
        """
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        if not solicit.permissions:
            return
        else:
            if Solicit.rootURI in solicit:
                rootURI = solicit.rootURI
            else:
                rootURI = None
            if Solicit.replacements in solicit:
                replacements = solicit.replacements
            else:
                replacements = None
            gateways = self.iterateGateways(solicit.permissions, rootURI, replacements)
            if solicit.gateways is not None:
                solicit.gateways = itertools.chain(solicit.gateways, gateways)
            else:
                solicit.gateways = gateways
            return

    def iterateGateways(self, permissions, rootURI=None, replacements=None):
        """
        Iterate the gateways for permissions.
        """
        assert isinstance(permissions, Iterable), 'Invalid permissions %s' % permissions
        permissions = sorted(permissions, key=lambda perm: perm.access.Path)
        permissions.sort(key=lambda perm: perm.access.Priority)
        for perm in permissions:
            assert isinstance(perm, Permission), 'Invalid permission %s' % perm
            assert isinstance(perm.access, Access), 'Invalid permission access %s' % perm.access
            assert isinstance(perm.filters, dict), 'Invalid permission filters %s' % perm.filters
            assert isinstance(perm.access.Path, str), 'Invalid access path %s' % perm.access.Path
            pattern = '%s[\\/]?(?:\\.|$)' % '([^\\/]+)'.join(re.escape(pitem) for pitem in perm.access.Path.split('*'))
            if rootURI:
                assert isinstance(rootURI, str), 'Invalid root URI %s' % rootURI
                pattern = '%s\\/%s' % (re.escape(rootURI), pattern)
            gateway = Gateway()
            gateway.Pattern = '^%s' % pattern
            gateway.Methods = [perm.access.Method]
            filtersEntry = filtersProperty = None
            for pathsEntry, pathsProperty in perm.filters.values():
                assert isinstance(pathsEntry, dict), 'Invalid indexed path entries %s' % pathsEntry
                if filtersEntry is None:
                    filtersEntry = pathsEntry
                else:
                    if filtersEntry:
                        nfilters = {}
                        for position, paths in pathsEntry.items():
                            assert isinstance(paths, set), 'Invalid indexed paths %s' % paths
                            cpaths = filtersEntry.get(position)
                            if cpaths:
                                paths.update(cpaths)
                                nfilters[position] = paths
                                continue

                        filtersEntry = nfilters
                    if filtersProperty is None:
                        filtersProperty = pathsProperty
                    elif filtersProperty:
                        nfilters = {}
                        for name, paths in pathsProperty.items():
                            assert isinstance(paths, set), 'Invalid indexed paths %s' % paths
                            cpaths = filtersProperty.get(name)
                            if cpaths:
                                paths.update(cpaths)
                                nfilters[position] = paths
                                continue

                        filtersProperty = nfilters
                if not filtersEntry and not filtersProperty:
                    break

            if filtersEntry:
                for position in sorted(filtersEntry):
                    for path in sorted(filtersEntry[position]):
                        if gateway.Filters is None:
                            gateway.Filters = []
                        assert isinstance(path, str), 'Invalid path %s' % path
                        if replacements:
                            path = path % replacements
                        if rootURI:
                            path = '%s/%s' % (rootURI, path)
                        gateway.Filters.append('%s:%s' % (position, path))

            if filtersProperty:
                values = [
                 PROPERTY_NAME]
                for name in sorted(filtersProperty):
                    paths = sorted(filtersProperty[name])
                    if rootURI:
                        for k, path in enumerate(paths):
                            if replacements:
                                path = path % replacements
                            paths[k] = '%s/%s' % (rootURI, path)

                    values.append('%s=%s' % (name, '|'.join(paths)))

                if gateway.PutHeaders is None:
                    gateway.PutHeaders = {}
                gateway.PutHeaders[HEADER_FILTER_INPUT] = ';'.join(values)
            if Permission.navigate in perm and perm.navigate:
                if replacements:
                    path = perm.navigate % replacements
                else:
                    path = perm.navigate
                if rootURI:
                    path = '%s/%s' % (rootURI, path)
                gateway.Navigate = path
            yield gateway

        return
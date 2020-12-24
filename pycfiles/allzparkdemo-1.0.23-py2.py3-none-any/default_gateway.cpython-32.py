# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gateway/core/impl/processor/default_gateway.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 21, 2013\n\n@package: gateway\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that adds default Gateway objects.\n'
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from collections import Iterable
from gateway.api.gateway import Gateway
from itertools import chain

class Reply(Context):
    """
    The reply context.
    """
    gateways = defines(Iterable, doc='\n    @rtype: Iterable(Gateway)\n    The default gateways.\n    ')


@injected
@setup(Handler, name='registerDefaultGateways')
class RegisterDefaultGateways(HandlerProcessorProceed):
    """
    Provides the handler that populates default gateways.
    """
    default_gateways = []
    wire.config('default_gateways', doc="\n    The default gateways that are available for any unauthorized access. This is a list of dictionaries that are allowed\n    the following keys:\n        Pattern -   a string value:\n                    contains the regex that needs to match with the requested URI. The pattern needs to produce, if is the\n                    case, capturing groups that can be used by the Filters or Navigate.\n        Headers -   a list of strings:\n                    the headers to be filtered in order to validate the navigation. Even though this might look specific for\n                    http they actually can be used for any meta data that accompanies a request, it depends mostly on the\n                    gateway interpretation. The headers are provided as regexes that need to be matched. In case of headers\n                    that are paired as name and value the regex will receive the matching string as 'Name:Value', the name\n                    is not allowed to contain ':'. At least one header needs to match to consider the navigation valid.\n        Methods -   a list of strings:\n                    the list of allowed methods for the request, if no method is provided then all methods are considered\n                    valid. At least one method needs to match to consider the navigation valid.\n        Filters -   a list of strings:\n                    contains a list of URIs that need to be called in order to allow the gateway Navigate. The filters are\n                    allowed to have place holders of form '{1}' or '{2}' ... '{n}' where n is the number of groups obtained\n                    from the Pattern, the place holders will be replaced with their respective group value. All filters\n                    need to return a True value in order to allow the gateway Navigate.\n        Errors -    a list of integers:\n                    the list of errors codes that are considered to be handled by this Gateway entry, if no error is provided\n                    then it means the entry is not solving any error navigation. At least one error needs to match in order\n                    to consider the navigation valid.\n        Host -      a string value:\n                    the host where the request needs to be resolved, if not provided the request will be delegated to the\n                    default host.\n        Protocol -  a string value:\n                    the protocol to be used in the communication with the server that handles the request, if not provided\n                    the request will be delegated using the default protocol.\n        Navigate -  a string value:\n                    a pattern like string of forms like '*', 'resources/*' or 'redirect/Model/{1}'. The pattern is allowed to\n                    have place holders and also the '*' which stands for the actual called URI, also parameters are allowed\n                    for navigate URI, the parameters will override the actual parameters.\n        PutHeaders -The headers to be put on the forwarded requests. The values are provided as 'Name:Value', the name is\n                    not allowed to contain ':'.\n    ")

    def __init__(self):
        """
        Construct the default gateways register.
        """
        assert isinstance(self.default_gateways, list), 'Invalid default gateways %s' % self.default_gateways
        super().__init__()
        self._gateways = []
        for config in self.default_gateways:
            self._gateways.append(gatewayFrom(config))

    def process(self, reply: Reply, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Adds the default gateways.
        """
        assert isinstance(reply, Reply), 'Invalid reply %s' % reply
        if reply.gateways is not None:
            reply.gateways = chain(self._gateways, reply.gateways)
        else:
            reply.gateways = self._gateways
        return


def gatewayFrom(config):
    """
    Constructs a gateway from the provided configuration dictionary.
    
    @param config: dictionary{string, ...}
        The configurations dictionary to construct the gateway based on.
    @return: Gateway
        The constructed gateway.
    """
    assert isinstance(config, dict), 'Invalid gateway configuration %s' % config
    keys = set()
    gateway = Gateway()
    for key in ('Pattern', 'Headers', 'Methods', 'Filters', 'Errors', 'Host', 'Protocol',
                'Navigate'):
        value = config.get(key)
        if value is not None:
            if key == 'Pattern':
                assert isinstance(value, str), 'Invalid Pattern %s' % value
            else:
                if key == 'Headers':
                    assert isinstance(value, list), 'Invalid Headers %s' % value
                    for item in value:
                        if not isinstance(item, str):
                            raise AssertionError('Invalid Headers value %s' % item)

                else:
                    if key == 'Methods':
                        assert isinstance(value, list), 'Invalid Methods %s' % value
                        for item in value:
                            if not isinstance(item, str):
                                raise AssertionError('Invalid Methods value %s' % item)

                    else:
                        if key == 'Filters':
                            assert isinstance(value, list), 'Invalid Filters %s' % value
                            for item in value:
                                if not isinstance(item, str):
                                    raise AssertionError('Invalid Filters value %s' % item)

                        else:
                            if key == 'Errors':
                                assert isinstance(value, list), 'Invalid Errors %s' % value
                                for item in value:
                                    if not isinstance(item, int):
                                        raise AssertionError('Invalid Errors value %s' % item)

                            else:
                                if key == 'Host':
                                    assert isinstance(value, str), 'Invalid Host %s' % value
                                else:
                                    if key == 'Protocol':
                                        assert isinstance(value, str), 'Invalid Protocol %s' % value
                                    else:
                                        if key == 'Navigate':
                                            assert isinstance(value, str), 'Invalid Navigate %s' % value
                                        elif key == 'PutHeaders':
                                            assert isinstance(value, list), 'Invalid PutHeaders %s' % value
                                            for item in value:
                                                if not isinstance(item, str):
                                                    raise AssertionError('Invalid PutHeaders value %s' % item)

            setattr(gateway, key, value)
            if not keys.add(key):
                if not True:
                    raise AssertionError
                continue

    assert len(keys) == len(config), 'Invalid gateway configuration names: %s' % ', '.join(keys.difference(config))
    return gateway
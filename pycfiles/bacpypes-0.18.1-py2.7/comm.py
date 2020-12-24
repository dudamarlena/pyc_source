# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/comm.py
# Compiled at: 2018-08-02 15:42:10
"""
Communications Module
"""
import sys, struct
from copy import copy as _copy
from .errors import DecodingError, ConfigurationError
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging, btox
_debug = 0
_log = ModuleLogger(globals())
_short_mask = 65535
_long_mask = 4294967295
client_map = {}
server_map = {}
service_map = {}
element_map = {}

@bacpypes_debugging
class PCI(DebugContents):
    _debug_contents = ('pduUserData+', 'pduSource', 'pduDestination')

    def __init__(self, *args, **kwargs):
        if _debug:
            PCI._debug('__init__ %r %r', args, kwargs)
        my_kwargs = {}
        other_kwargs = {}
        for element in ('user_data', 'source', 'destination'):
            if element in kwargs:
                my_kwargs[element] = kwargs[element]

        for kw in kwargs:
            if kw not in my_kwargs:
                other_kwargs[kw] = kwargs[kw]

        if _debug:
            PCI._debug('    - my_kwargs: %r', my_kwargs)
        if _debug:
            PCI._debug('    - other_kwargs: %r', other_kwargs)
        super(PCI, self).__init__(*args, **other_kwargs)
        self.pduUserData = my_kwargs.get('user_data', None)
        self.pduSource = my_kwargs.get('source', None)
        self.pduDestination = my_kwargs.get('destination', None)
        return

    def update(self, pci):
        """Copy the PCI fields."""
        self.pduUserData = pci.pduUserData
        self.pduSource = pci.pduSource
        self.pduDestination = pci.pduDestination

    def pci_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PCI._debug('pci_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        for k, v in (('user_data', self.pduUserData), ('source', self.pduSource), ('destination', self.pduDestination)):
            if _debug:
                PCI._debug('    - %r: %r', k, v)
            if v is None:
                continue
            if hasattr(v, 'dict_contents'):
                v = v.dict_contents(as_class=as_class)
            use_dict.__setitem__(k, v)

        return use_dict

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PCI._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        return self.pci_contents(use_dict=use_dict, as_class=as_class)


@bacpypes_debugging
class PDUData(object):

    def __init__(self, data=None, *args, **kwargs):
        if _debug:
            PDUData._debug('__init__ %r %r %r', data, args, kwargs)
        super(PDUData, self).__init__(*args, **kwargs)
        if data is None:
            self.pduData = ''
        elif isinstance(data, str):
            self.pduData = data
        elif isinstance(data, PDUData) or isinstance(data, PDU):
            self.pduData = _copy(data.pduData)
        else:
            raise TypeError('string expected')
        return

    def get(self):
        if len(self.pduData) == 0:
            raise DecodingError('no more packet data')
        octet = ord(self.pduData[0])
        self.pduData = self.pduData[1:]
        return octet

    def get_data(self, dlen):
        if len(self.pduData) < dlen:
            raise DecodingError('no more packet data')
        data = self.pduData[:dlen]
        self.pduData = self.pduData[dlen:]
        return data

    def get_short(self):
        return struct.unpack('>H', self.get_data(2))[0]

    def get_long(self):
        return struct.unpack('>L', self.get_data(4))[0]

    def put(self, n):
        self.pduData += chr(n)

    def put_data(self, data):
        self.pduData += data

    def put_short(self, n):
        self.pduData += struct.pack('>H', n & _short_mask)

    def put_long(self, n):
        self.pduData += struct.pack('>L', n & _long_mask)

    def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
        if isinstance(self.pduData, str):
            if len(self.pduData) > 20:
                hexed = btox(self.pduData[:20], '.') + '...'
            else:
                hexed = btox(self.pduData, '.')
            file.write("%spduData = x'%s'\n" % ('    ' * indent, hexed))
        else:
            file.write('%spduData = %r\n' % ('    ' * indent, self.pduData))

    def pdudata_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PDUData._debug('pdudata_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        v = self.pduData
        if v is not None:
            if isinstance(v, str):
                v = btox(v)
            elif hasattr(v, 'dict_contents'):
                v = v.dict_contents(as_class=as_class)
            use_dict.__setitem__('data', v)
        return use_dict

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PDUData._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        return self.pdudata_contents(use_dict=use_dict, as_class=as_class)


@bacpypes_debugging
class PDU(PCI, PDUData):

    def __init__(self, data=None, **kwargs):
        if _debug:
            PDU._debug('__init__ %r %r', data, kwargs)
        user_data = kwargs.get('user_data', None)
        source = kwargs.get('source', None)
        destination = kwargs.get('destination', None)
        if isinstance(data, PDU):
            user_data = user_data or data.pduUserData
            source = source or data.pduSource
            destination = destination or data.pduDestination
        PCI.__init__(self, user_data=user_data, source=source, destination=destination)
        PDUData.__init__(self, data)
        return

    def __str__(self):
        return '<%s %s -> %s : %s>' % (self.__class__.__name__,
         self.pduSource,
         self.pduDestination,
         btox(self.pduData, '.'))

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PDU._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        self.pci_contents(use_dict=use_dict, as_class=as_class)
        self.pdudata_contents(use_dict=use_dict, as_class=as_class)
        return use_dict


@bacpypes_debugging
class Client(object):

    def __init__(self, cid=None):
        if _debug:
            Client._debug('__init__ cid=%r', cid)
        self.clientID = cid
        self.clientPeer = None
        if cid is not None:
            if cid in client_map:
                raise ConfigurationError(('already a client {!r}').format(cid))
            client_map[cid] = self
            if cid in server_map:
                server = server_map[cid]
                if server.serverPeer:
                    raise ConfigurationError(('server {!r} already bound').format(cid))
                bind(self, server)
        return

    def request(self, *args, **kwargs):
        if _debug:
            Client._debug('request %r %r', args, kwargs)
        if not self.clientPeer:
            raise ConfigurationError('unbound client')
        self.clientPeer.indication(*args, **kwargs)

    def confirmation(self, *args, **kwargs):
        raise NotImplementedError('confirmation must be overridden')


@bacpypes_debugging
class Server(object):

    def __init__(self, sid=None):
        if _debug:
            Server._debug('__init__ sid=%r', sid)
        self.serverID = sid
        self.serverPeer = None
        if sid is not None:
            if sid in server_map:
                raise RuntimeError(('already a server {!r}').format(sid))
            server_map[sid] = self
            if sid in client_map:
                client = client_map[sid]
                if client.clientPeer:
                    raise ConfigurationError(('client {!r} already bound').format(sid))
                bind(client, self)
        return

    def indication(self, *args, **kwargs):
        raise NotImplementedError('indication must be overridden')

    def response(self, *args, **kwargs):
        if _debug:
            Server._debug('response %r %r', args, kwargs)
        if not self.serverPeer:
            raise ConfigurationError('unbound server')
        self.serverPeer.confirmation(*args, **kwargs)


@bacpypes_debugging
class Debug(Client, Server):

    def __init__(self, label=None, cid=None, sid=None):
        if _debug:
            Debug._debug('__init__ label=%r cid=%r sid=%r', label, cid, sid)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        self.label = label

    def confirmation(self, *args, **kwargs):
        print ('Debug({!s}).confirmation').format(self.label)
        for i, arg in enumerate(args):
            print ('    - args[{:d}]: {!r}').format(i, arg)
            if hasattr(arg, 'debug_contents'):
                arg.debug_contents(2)

        for key, value in kwargs.items():
            print ('    - kwargs[{!r}]: {!r}').format(key, value)
            if hasattr(value, 'debug_contents'):
                value.debug_contents(2)

        if self.serverPeer:
            self.response(*args, **kwargs)

    def indication(self, *args, **kwargs):
        print ('Debug({!s}).indication').format(self.label)
        for i, arg in enumerate(args):
            print ('    - args[{:d}]: {!r}').format(i, arg)
            if hasattr(arg, 'debug_contents'):
                arg.debug_contents(2)

        for key, value in kwargs.items():
            print ('    - kwargs[{!r}]: {!r}').format(key, value)
            if hasattr(value, 'debug_contents'):
                value.debug_contents(2)

        if self.clientPeer:
            self.request(*args, **kwargs)


@bacpypes_debugging
class Echo(Client, Server):

    def __init__(self, cid=None, sid=None):
        if _debug:
            Echo._debug('__init__ cid=%r sid=%r', cid, sid)
        Client.__init__(self, cid)
        Server.__init__(self, sid)

    def confirmation(self, *args, **kwargs):
        if _debug:
            Echo._debug('confirmation %r %r', args, kwargs)
        self.request(*args, **kwargs)

    def indication(self, *args, **kwargs):
        if _debug:
            Echo._debug('indication %r %r', args, kwargs)
        self.response(*args, **kwargs)


@bacpypes_debugging
class Switch(Client, Server):
    """
    A Switch is a client and server that wraps around clients and/or servers
    and provides a way to switch between them without unbinding and rebinding
    the stack.
    """

    class TerminalWrapper(Client, Server):

        def __init__(self, switch, terminal):
            self.switch = switch
            self.terminal = terminal
            if isinstance(terminal, Server):
                bind(self, terminal)
            if isinstance(terminal, Client):
                bind(terminal, self)

        def indication(self, *args, **kwargs):
            self.switch.request(*args, **kwargs)

        def confirmation(self, *args, **kwargs):
            self.switch.response(*args, **kwargs)

    def __init__(self, **terminals):
        if _debug:
            Switch._debug('__init__ %r', terminals)
        Client.__init__(self)
        Server.__init__(self)
        self.terminals = {k:Switch.TerminalWrapper(self, v) for k, v in terminals.items()}
        self.current_terminal = None
        return

    def __getitem__(self, key):
        if key not in self.terminals:
            raise KeyError('%r not a terminal' % (key,))
        return self.terminals[key].terminal

    def __setitem__(self, key, term):
        if key in self.terminals:
            raise KeyError('%r already a terminal' % (key,))
        self.terminals[key] = Switch.TerminalWrapper(self, term)

    def __delitem__(self, key):
        if key not in self.terminals:
            raise KeyError('%r not a terminal' % (key,))
        term = self.terminals[key].terminal
        if term is self.current_terminal:
            terminal_deactivate = getattr(self.current_terminal, 'deactivate', None)
            if terminal_deactivate:
                terminal_deactivate()
            self.current_terminal = None
        del self.terminals[key]
        return

    def switch_terminal(self, key):
        if key not in self.terminals:
            raise KeyError('%r not a terminal' % (key,))
        if self.current_terminal:
            terminal_deactivate = getattr(self.current_terminal, 'deactivate', None)
            if terminal_deactivate:
                terminal_deactivate()
        if key is None:
            self.current_terminal = None
        else:
            self.current_terminal = self.terminals[key].terminal
            terminal_activate = getattr(self.current_terminal, 'activate', None)
            if terminal_activate:
                terminal_activate()
        return

    def indication(self, *args, **kwargs):
        """Downstream packet, send to current terminal."""
        if not self.current_terminal:
            raise RuntimeError('no active terminal')
        if not isinstance(self.current_terminal, Server):
            raise RuntimeError('current terminal not a server')
        self.current_terminal.indication(*args, **kwargs)

    def confirmation(self, *args, **kwargs):
        """Upstream packet, send to current terminal."""
        if not self.current_terminal:
            raise RuntimeError('no active terminal')
        if not isinstance(self.current_terminal, Client):
            raise RuntimeError('current terminal not a client')
        self.current_terminal.confirmation(*args, **kwargs)


@bacpypes_debugging
class ServiceAccessPoint(object):

    def __init__(self, sapID=None):
        if _debug:
            ServiceAccessPoint._debug('__init__(%s)', sapID)
        self.serviceID = sapID
        self.serviceElement = None
        if sapID is not None:
            if sapID in service_map:
                raise ConfigurationError(('already a service access point {!r}').format(sapID))
            service_map[sapID] = self
            if sapID in element_map:
                element = element_map[sapID]
                if element.elementService:
                    raise ConfigurationError(('application service element {!r} already bound').format(sapID))
                bind(element, self)
        return

    def sap_request(self, *args, **kwargs):
        if _debug:
            ServiceAccessPoint._debug('sap_request(%s) %r %r', self.serviceID, args, kwargs)
        if not self.serviceElement:
            raise ConfigurationError('unbound service access point')
        self.serviceElement.indication(*args, **kwargs)

    def sap_indication(self, *args, **kwargs):
        raise NotImplementedError('sap_indication must be overridden')

    def sap_response(self, *args, **kwargs):
        if _debug:
            ServiceAccessPoint._debug('sap_response(%s) %r %r', self.serviceID, args, kwargs)
        if not self.serviceElement:
            raise ConfigurationError('unbound service access point')
        self.serviceElement.confirmation(*args, **kwargs)

    def sap_confirmation(self, *args, **kwargs):
        raise NotImplementedError('sap_confirmation must be overridden')


@bacpypes_debugging
class ApplicationServiceElement(object):

    def __init__(self, aseID=None):
        if _debug:
            ApplicationServiceElement._debug('__init__(%s)', aseID)
        self.elementID = aseID
        self.elementService = None
        if aseID is not None:
            if aseID in element_map:
                raise ConfigurationError(('already an application service element {!r}').format(aseID))
            element_map[aseID] = self
            if aseID in service_map:
                service = service_map[aseID]
                if service.serviceElement:
                    raise ConfigurationError(('service access point {!r} already bound').format(aseID))
                bind(self, service)
        return

    def request(self, *args, **kwargs):
        if _debug:
            ApplicationServiceElement._debug('request(%s) %r %r', self.elementID, args, kwargs)
        if not self.elementService:
            raise ConfigurationError('unbound application service element')
        self.elementService.sap_indication(*args, **kwargs)

    def indication(self, *args, **kwargs):
        raise NotImplementedError('indication must be overridden')

    def response(self, *args, **kwargs):
        if _debug:
            ApplicationServiceElement._debug('response(%s) %r %r', self.elementID, args, kwargs)
        if not self.elementService:
            raise ConfigurationError('unbound application service element')
        self.elementService.sap_confirmation(*args, **kwargs)

    def confirmation(self, *args, **kwargs):
        raise NotImplementedError('confirmation must be overridden')


class NullServiceElement(ApplicationServiceElement):

    def indication(self, *args, **kwargs):
        pass

    def confirmation(self, *args, **kwargs):
        pass


class DebugServiceElement(ApplicationServiceElement):

    def indication(self, *args, **kwargs):
        print ('DebugServiceElement({!s}).indication').format(self.elementID)
        print ('    - args: {!r}').format(args)
        print ('    - kwargs: {!r}').format(kwargs)

    def confirmation(self, *args, **kwargs):
        print ('DebugServiceElement({!s}).confirmation').format(self.elementID)
        print ('    - args: {!r}').format(args)
        print ('    - kwargs: {!r}').format(kwargs)


@bacpypes_debugging
def bind(*args):
    """bind a list of clients and servers together, top down."""
    if _debug:
        bind._debug('bind %r', args)
    if not args:
        for cid, client in client_map.items():
            if client.clientPeer:
                continue
            if cid not in server_map:
                raise RuntimeError(('unmatched server {!r}').format(cid))
            server = server_map[cid]
            if server.serverPeer:
                raise RuntimeError(('server already bound %r').format(cid))
            bind(client, server)

        for sid, server in server_map.items():
            if server.serverPeer:
                continue
            if sid not in client_map:
                raise RuntimeError(('unmatched client {!r}').format(sid))
            else:
                raise RuntimeError(('mistery unbound server {!r}').format(sid))

        for eid, element in element_map.items():
            if element.elementService:
                continue
            if eid not in service_map:
                raise RuntimeError(('unmatched element {!r}').format(cid))
            service = service_map[eid]
            if server.serverPeer:
                raise RuntimeError(('service already bound {!r}').format(cid))
            bind(element, service)

        for sid, service in service_map.items():
            if service.serviceElement:
                continue
            if sid not in element_map:
                raise RuntimeError(('unmatched service {!r}').format(sid))
            else:
                raise RuntimeError(('mistery unbound service {!r}').format(sid))

    for i in xrange(len(args) - 1):
        client = args[i]
        if _debug:
            bind._debug('    - client: %r', client)
        server = args[(i + 1)]
        if _debug:
            bind._debug('    - server: %r', server)
        if isinstance(client, Client) and isinstance(server, Server):
            client.clientPeer = server
            server.serverPeer = client
        elif isinstance(client, ApplicationServiceElement) and isinstance(server, ServiceAccessPoint):
            client.elementService = server
            server.serviceElement = client
        else:
            raise TypeError('bind() requires a client and server')
        if _debug:
            bind._debug('    - bound')
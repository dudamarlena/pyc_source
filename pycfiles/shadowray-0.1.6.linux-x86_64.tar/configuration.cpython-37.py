# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/core/configuration.py
# Compiled at: 2019-03-24 13:21:40
# Size of source mod 2**32: 26777 bytes
import json

class BaseConfig:

    def __init__(self, obj, **kwargs):
        self._BaseConfig__obj = obj
        for key in kwargs:
            self._BaseConfig__obj[key] = kwargs[key]

    def __str__(self):
        return json.dumps(self._BaseConfig__obj)

    @property
    def json(self):
        return str(self)

    @property
    def json_obj(self):
        return self._BaseConfig__obj


class Configuration(BaseConfig):

    def __init__(self):
        self._Configuration__configuration = {'inbounds':[],  'outbounds':[]}
        super().__init__(self._Configuration__configuration)

    def set_log(self, log_obj):
        self._Configuration__configuration['log'] = log_obj.json_obj

    def set_api(self, api_obj):
        self._Configuration__configuration['api'] = api_obj.json_obj

    def add_inbound(self, inbound_obj):
        self._Configuration__configuration['inbounds'].append(inbound_obj.json_obj)

    def add_ontbound(self, outbound_obj):
        self._Configuration__configuration['outbounds'].append(outbound_obj.json_obj)

    class Log(BaseConfig):
        DEBUG = 'debug'
        INFO = 'info'
        WARNING = 'warning'
        ERROR = 'error'
        NONE = 'none'

        def __init__(self, access, error, level):
            self._Log__log = {'access':access, 
             'error':error, 
             'level':level}
            super().__init__(self._Log__log)

    class Inbound(BaseConfig):

        def __init__(self, port, listen, protocol, tag=None):
            self._Inbound__inbound = {'port':port, 
             'listen':listen, 
             'protocol':protocol, 
             'settings':{},  'streamSettings':{},  'sniffing':{'enabled':True, 
              'destOverride':[
               'http', 'tls']}}
            if tag is not None:
                self._Inbound__inbound['tag'] = tag
            super().__init__(self._Inbound__inbound)

        def set_settings(self, setting_boj):
            self._Inbound__inbound['settings'] = setting_boj.json_obj

        def set_tag(self, tag):
            self._Inbound__inbound['tag'] = tag

        def set_stream(self, stream_obj):
            self._Inbound__inbound['streamSettings'] = stream_obj.json_obj

        def set_sniffing(self, sniffing_obj):
            self._Inbound__inbound['sniffing'] = sniffing_obj.json_obj

        def set_allocate(self, allocate_obj):
            self._Inbound__inbound['allocate'] = allocate_obj.json_obj

        class Allocate:

            def __init__(self, strategy='always', refresh=5, concurrency=3):
                self._Allocate__allocate = {'strategy':strategy, 
                 'refresh':refresh, 
                 'concurrency':concurrency}

            def __str__(self):
                return json.dumps(self._Allocate__allocate)

            @property
            def json(self):
                return str(self)

            @property
            def json_obj(self):
                return self._Allocate__allocate

        class Sniffing:

            def __init__(self, enable, dest_override=None):
                if dest_override is None:
                    dest_override = [
                     'http', 'tls']
                self._Sniffing__sniffing = {'enabled':enable, 
                 'destOverride':dest_override}

            def add_dest_override(self, p):
                self._Sniffing__sniffing['destOverride'].append(p)

            def __str__(self):
                return json.dumps(self._Sniffing__sniffing)

            @property
            def json(self):
                return str(self)

            @property
            def json_obj(self):
                return self._Sniffing__sniffing

    class Outbound(BaseConfig):

        def __init__(self, protocol, tag=None, proxy_tag=None, send_through='0.0.0.0'):
            self._Outbound__outbound = {'sendThrough':send_through, 
             'protocol':protocol, 
             'settings':{},  'streamSettings':{}}
            if tag is not None:
                self._Outbound__outbound['tag'] = tag
            if proxy_tag is not None:
                self._Outbound__outbound['proxySettings'] = proxy_tag
            super().__init__(self._Outbound__outbound)

        def set_settings(self, setting_boj):
            self._Outbound__outbound['settings'] = setting_boj.json_obj

        def set_tag(self, tag):
            self._Outbound__outbound['tag'] = tag

        def set_stream(self, stream_obj):
            self._Outbound__outbound['streamSettings'] = stream_obj.json_obj

        def set_mux(self, mux_obj):
            self._Outbound__outbound['mux'] = mux_obj.json_obj

        class Mux(BaseConfig):

            def __init__(self, enable, concurrency=8):
                self._Mux__mux = {'enabled':enable, 
                 'concurrency':concurrency}
                super().__init__(self._Mux__mux)

    class Api(BaseConfig):

        def __init__(self, tag):
            self._Api__api = {'tag':tag, 
             'services':[]}
            super().__init__(self._Api__api)

        def add_service(self, service):
            self._Api__api['services'].append(service)

    class Dns(BaseConfig):

        def __init__(self, client_ip, tag):
            self._Dns__dns = {'hosts':{},  'servers':[],  'clientIp':client_ip, 
             'tag':tag}
            super().__init__(self._Dns__dns)

        def add_host(self, key, value):
            self._Dns__dns['host'][key] = value

        def add_server(self, server_obj):
            self._Dns__dns['servers'].append(server_obj.json_obj)

        class Server(BaseConfig):

            def __init__(self, addr, port):
                self._Server__server = {'address':addr, 
                 'port':port, 
                 'domains':[]}
                super().__init__(self._Server__server)

            def add_domain(self, domain):
                self._Server__server['domains'].append(domain)

    class Stats(BaseConfig):

        def __init__(self):
            self._Stats__stats = {}
            super().__init__(self._Stats__stats)

    class Routing(BaseConfig):

        def __init__(self, strategy):
            self._Routing__routing = {'domainStrategy':strategy, 
             'rules':[],  'balancers':[]}
            super().__init__(self._Routing__routing)

        def add_rule(self, rule_obj):
            self._Routing__routing['rules'].append(rule_obj.json_obj)

        def add_balancer(self, balancer_obj):
            self._Routing__routing['balancers'].append(balancer_obj.json_obj)

        class Rule(BaseConfig):

            def __init__(self, port, outbound_tag=None, balancer_tag=None, network=None, type='field'):
                self._Rule__rule = {'type':type, 
                 'domain':[],  'ip':[],  'port':port, 
                 'network':network, 
                 'source':[],  'user':[],  'inboundTag':[],  'protocol':[],  'outboundTag':outbound_tag, 
                 'balancerTag':balancer_tag}
                super().__init__(self._Rule__rule)

            def add_domain(self, domain):
                self._Rule__rule['domain'].append(domain)

            def add_ip(self, ip):
                self._Rule__rule['ip'].append(ip)

            def add_source(self, source):
                self._Rule__rule['source'].append(source)

            def add_user(self, user):
                self._Rule__rule['user'].append(user)

            def add_protocol(self, protocol):
                self._Rule__rule['protocol'].append(protocol)

            def add_inbound_tag(self, tag):
                self._Rule__rule['inboundTag'].append(tag)

        class Balancer(BaseConfig):

            def __init__(self, tag):
                self._Balancer__balancer = {'tag':tag, 
                 'selector':[]}
                super().__init__(self._Balancer__balancer)

            def add_selector(self, selector):
                self._Balancer__balancer['selector'].append(selector)

    class Policy(BaseConfig):

        def __init__(self):
            self._Policy__policy = {'levels':{},  'system':{}}
            super().__init__(self._Policy__policy)

        def add_level_policy(self, level, policy_obj):
            self._Policy__policy['levels'][str(level)] = policy_obj.json_obj

        def set_system_policy(self, policy_obj):
            self._Policy__policy['system'] = policy_obj.json_obj

        class LevelPolicy(BaseConfig):

            def __init__(self, stats_user_uplink, stats_user_downlink, handshake=4, conn_idle=300, uplink_only=2, downlink_only=5, buffer_size=None):
                self._LevelPolicy__level_policy = {'handshake':handshake, 
                 'connIdle':conn_idle, 
                 'uplinkOnly':uplink_only, 
                 'downlinkOnly':downlink_only, 
                 'statsUserUplink':stats_user_uplink, 
                 'statsUserDownlink':stats_user_downlink}
                if buffer_size is not None:
                    self._LevelPolicy__level_policy['bufferSize'] = buffer_size
                super().__init__(self._LevelPolicy__level_policy)

        class SystemPolicy(BaseConfig):

            def __init__(self, stats_inbound_uplink, stats_inbound_downlink):
                self._SystemPolicy__system_policy = {'statsInboundUplink':stats_inbound_uplink, 
                 'statsInboundDownlink':stats_inbound_downlink}
                super().__init__(self._SystemPolicy__system_policy)

    class Reverse(BaseConfig):

        def __init__(self):
            self._Reverse__reverse = {'bridges':[],  'portals':[]}
            super().__init__(self._Reverse__reverse)

        def add_bridge(self, bridge_obj):
            self._Reverse__reverse['bridges'].append(bridge_obj.json_obj)

        def add_portal(self, portal_obj):
            self._Reverse__reverse['portals'].append(portal_obj.json_obj)

        class Bridge(BaseConfig):

            def __init__(self, tag, domain):
                self._Bridge__bridge = {'tag':tag, 
                 'domain':domain}
                super().__init__(self._Bridge__bridge)

        class Portal(BaseConfig):

            def __init__(self, tag, domain):
                self._Portal__bridge = {'tag':tag, 
                 'domain':domain}
                super().__init__(self._Portal__bridge)

    class ProtocolSetting:

        class Inbound:

            class DokodemoDoor(BaseConfig):

                def __init__(self, port, network='tcp', timeout=300, **kwargs):
                    self._DokodemoDoor__dokodemo_door = {'port':port, 
                     'network':network, 
                     'timeout':timeout}
                    for key in kwargs:
                        self._DokodemoDoor__dokodemo_door[key] = kwargs[key]

                    super().__init__(self._DokodemoDoor__dokodemo_door)

                def set_address(self, addr):
                    self._DokodemoDoor__dokodemo_door['address'] = addr

                def set_follow_redirect(self, f):
                    self._DokodemoDoor__dokodemo_door['followRedirect'] = f

                def set_user_level(self, level):
                    self._DokodemoDoor__dokodemo_door['userLevel'] = level

            class Http(BaseConfig):

                def __init__(self, user_level, timeout=300, allow_transparent=False, **kwargs):
                    self._Http__http = {'timeout':timeout, 
                     'allowTransparent':allow_transparent, 
                     'userLevel':user_level, 
                     'account':[]}
                    for key in kwargs:
                        self._Http__http[key] = kwargs[key]

                    super().__init__(self._Http__http)

                def add_account(self, username, password):
                    self._Http__http['account'].append({'user':username, 
                     'pass':password})

            class Shadowsocks(BaseConfig):

                def __init__(self, method, password, level=0, network='tcp', **kwargs):
                    self._Shadowsocks__shadowsocks = {'method':method, 
                     'password':password, 
                     'level':level, 
                     'network':network}
                    for key in kwargs:
                        self._Shadowsocks__shadowsocks[key] = kwargs[key]

                    super().__init__(self._Shadowsocks__shadowsocks)

                def set_email(self, email):
                    self._Shadowsocks__shadowsocks['email'] = email

                def set_ota(self, f):
                    self._Shadowsocks__shadowsocks['ota'] = f

            class VMess(BaseConfig):

                def __init__(self, disable_insecure_encryption=False, **kwargs):
                    self._VMess__vmess = {'disableInsecureEncryption':disable_insecure_encryption, 
                     'clients':[]}
                    for key in kwargs:
                        self._VMess__vmess[key] = kwargs[key]

                    super().__init__(self._VMess__vmess)

                def set_detour(self, to):
                    self._VMess__vmess['detour'] = {'to': to}

                def set_default(self, level, aid):
                    self._VMess__vmess['default'] = {'level':level, 
                     'alterId':aid}

                def add_client(self, id, level, aid, email):
                    self._VMess__vmess['clients'].append({'id':id, 
                     'level':level, 
                     'alterId':aid, 
                     'email':email})

            class Socks(BaseConfig):

                def __init__(self, auth='noauth', udp=False, **kwargs):
                    self._Socks__socks = {'auth':auth, 
                     'udp':udp, 
                     'accounts':[]}
                    for key in kwargs:
                        self._Socks__socks[key] = kwargs[key]

                    super().__init__(self._Socks__socks)

                def set_ip(self, addr):
                    self._Socks__socks['ip'] = addr

                def set_user_level(self, level):
                    self._Socks__socks['userLevel'] = level

                def add_user(self, username, password):
                    self._Socks__socks['accounts'].append({'user':username, 
                     'pass':password})

        class MTProto(BaseConfig):

            def __init__(self, **kwargs):
                self._MTProto__mt_proto = {'users': []}
                for key in kwargs:
                    self._MTProto__mt_proto[key] = kwargs[key]

                super().__init__(self._MTProto__mt_proto)

            def add_user(self, email, level, secret):
                self._MTProto__mt_proto['users'].append({'email':email, 
                 'level':level, 
                 'secret':secret})

        class Outbound:

            class Blackhole(BaseConfig):

                def __init__(self, response_type):
                    self._Blackhole__blackhole = {'response': {'type': response_type}}
                    super().__init__(self._Blackhole__blackhole)

            class Dns(BaseConfig):

                def __init__(self, network, address, port):
                    self._Dns__dns = {'network':network, 
                     'address':address, 
                     'port':port}
                    super().__init__(self._Dns__dns)

            class Freedom(BaseConfig):

                def __init__(self, domain_strategy, redirect, user_level):
                    self._Freedom__freedom = {'domainStrategy':domain_strategy, 
                     'redirect':redirect, 
                     'userLevel':user_level}
                    super().__init__(self._Freedom__freedom)

            class ShadowSocks(BaseConfig):

                def __init__(self):
                    self._ShadowSocks__shadowsocks = {'servers': []}
                    super().__init__(self._ShadowSocks__shadowsocks)

                def add_server(self, address, port, method, password, level, ota=False, email=None):
                    self._ShadowSocks__shadowsocks['servers'].append({'email':email, 
                     'address':address, 
                     'port':port, 
                     'method':method, 
                     'password':password, 
                     'ota':ota, 
                     'level':level})

            class Socks(BaseConfig):

                def __init__(self):
                    self._Socks__socks = {'servers': []}
                    super().__init__(self._Socks__socks)

                def add_server(self, server_obj):
                    self._Socks__socks['servers'].append(server_obj.json_obj)

                class Server(BaseConfig):

                    def __init__(self, addr, port):
                        self._Server__server = {'address':addr, 
                         'port':port, 
                         'users':[]}
                        super().__init__(self._Server__server)

                    def add_user(self, username, password, level):
                        self._Server__server['users'].append({'user':username, 
                         'pass':password, 
                         'level':level})

            class VMess(BaseConfig):

                def __init__(self):
                    self._VMess__vmess = {'vnext': []}
                    super().__init__(self._VMess__vmess)

                def add_server(self, server_obj):
                    self._VMess__vmess['vnext'].append(server_obj.json_obj)

                class Server(BaseConfig):

                    def __init__(self, addr, port):
                        self._Server__server = {'address':addr, 
                         'port':port, 
                         'users':[]}
                        super().__init__(self._Server__server)

                    def add_user(self, id, aid, security, level):
                        self._Server__server['users'].append({'id':id, 
                         'alterId':aid, 
                         'security':security, 
                         'level':level})

    class StreamSetting(BaseConfig):
        STREAMSETTING = 'StreamSetting'
        TRANSPORT = 'Transport'

        def __init__(self, type, network='tcp', security='none', **kwargs):
            if type == Configuration.StreamSetting.STREAMSETTING:
                self._StreamSetting__stream_setiing = {'network':network,  'security':security, 
                 'tlsSettings':{},  'tcpSettings':{},  'kcpSettings':{},  'wsSettings':{},  'httpSettings':{},  'dsSettings':{},  'quicSettings':{},  'sockopt':{'mark':0, 
                  'tcpFastOpen':False, 
                  'tproxy':'off'}}
            else:
                if type == Configuration.StreamSetting.TRANSPORT:
                    self._StreamSetting__stream_setiing = {'tcpSettings':{},  'kcpSettings':{},  'wsSettings':{},  'httpSettings':{},  'dsSettings':{},  'quicSettings':{}}
            (super().__init__)((self._StreamSetting__stream_setiing), **kwargs)

        def set_tls(self, tls_obj):
            self._StreamSetting__stream_setiing['tlsSettings'] = tls_obj.json_obj

        def set_kcp(self, kcp_obj):
            self._StreamSetting__stream_setiing['kcpSettings'] = kcp_obj.json_obj

        def set_tcp(self, tcp_obj):
            self._StreamSetting__stream_setiing['tcpSettings'] = tcp_obj.json_obj

        def set_web_socket(self, ws_obj):
            self._StreamSetting__stream_setiing['wsSettings'] = ws_obj.json_obj

        def set_http(self, http_obj):
            self._StreamSetting__stream_setiing['httpSettings'] = http_obj.json_obj

        def set_domain_socket(self, ds_obj):
            self._StreamSetting__stream_setiing['dsSettings'] = ds_obj.json_obj

        def set_quic(self, quic_obj):
            self._StreamSetting__stream_setiing['quicSettings'] = quic_obj.json_obj

        def set_sockopt(self, sockopt_obj):
            self._StreamSetting__stream_setiing['sockopt'] = sockopt_obj.json_obj

        class TLS(BaseConfig):

            def __init__(self, alpn=None):
                if alpn is None:
                    alpn = [
                     'http/1.1']
                self._TLS__tls = {'alpn':alpn, 
                 'certificates':[]}
                super().__init__(self._TLS__tls)

            def add_alpn(self, alpn):
                self._TLS__tls['alpn'].append(alpn)

            def set_server_name(self, name):
                self._TLS__tls['serverName'] = name

            def set_allow_insecure(self, f):
                self._TLS__tls['allowInsecure'] = f

            def add_certificate(self, usage='encipherment', **kwargs):
                cer = {'usage': usage}
                for key in kwargs:
                    cer[key] = kwargs[key]

                self._TLS__tls['certificates'].append(cer)

        class TCP(BaseConfig):

            def __init__(self, masquerading=False, type=None, **kwargs):
                if masquerading is False:
                    self._TCP__tcp = {'type': 'none'}
                else:
                    self._TCP__tcp = {'type':type,  'request':{},  'response':{}}
                (super().__init__)((self._TCP__tcp), **kwargs)

            def set_request(self, request_obj):
                self._TCP__tcp['request'] = request_obj.json_obj

            def set_response(self, response_obj):
                self._TCP__tcp['response'] = response_obj.json_obj

            class HttpRequest(BaseConfig):

                def __init__(self, version='1.1', method='GET', path=None, headers=None, **kwargs):
                    self._HttpRequest__request = {'version':version, 
                     'method':method, 
                     'path':[],  'headers':{}}
                    if path is not None:
                        self._HttpRequest__request['path'].append(path)
                    if headers is not None:
                        self._HttpRequest__request['headers'] = headers
                    (super().__init__)((self._HttpRequest__request), **kwargs)

                def add_path(self, path):
                    self._HttpRequest__request['path'].append(path)

                def set_header(self, headers):
                    self._HttpRequest__request['headers'] = headers

            class HttpResponse(BaseConfig):

                def __init__(self, version='1.1', status='200', reason='OK', headers=None, **kwargs):
                    self._HttpResponse__response = {'version':version, 
                     'status':status, 
                     'reason':reason, 
                     'headers':{}}
                    if headers is not None:
                        self._HttpResponse__response['headers'] = headers
                    (super().__init__)((self._HttpResponse__response), **kwargs)

        class KCP(BaseConfig):

            def __init__(self, mtu=1350, tti=50, uplink_capacity=5, download_capacity=20, congestion=False, read_buffer_size=2, write_buffer_size=2, header_type='none'):
                self._KCP__kcp = {'mtu':mtu, 
                 'tti':tti, 
                 'uplinkCapacity':uplink_capacity, 
                 'downlinkCapacity':download_capacity, 
                 'congestion':congestion, 
                 'readBufferSize':read_buffer_size, 
                 'writeBufferSize':write_buffer_size, 
                 'header':{'type': header_type}}
                super().__init__(self._KCP__kcp)

        class WebSocket(BaseConfig):

            def __init__(self, path='/', headers=None):
                if headers is None:
                    headers = {}
                self._WebSocket__web_socket = {'path':path,  'headers':headers}
                super().__init__(self._WebSocket__web_socket)

            def add_header(self, key, value):
                self._WebSocket__web_socket['headers'][key] = value

        class Http(BaseConfig):

            def __init__(self, path='/'):
                self._Http__http = {'host':[],  'path':path}
                super().__init__(self._Http__http)

            def add_host(self, host):
                self._Http__http['host'].append(host)

        class DomainSocket(BaseConfig):

            def __init__(self, filename):
                self._DomainSocket__domain_socket = {'path': filename}
                super().__init__(self._DomainSocket__domain_socket)

        class Quic(BaseConfig):

            def __init__(self, security='none', key='', header_type=''):
                self._Quic__quic = {'security':security, 
                 'key':key, 
                 'header':{'type': header_type}}
                super().__init__(self._Quic__quic)

        class Sockopt(BaseConfig):

            def __init__(self, mark=0, tcp_fast_open=False, tproxy='off'):
                self._Sockopt__sockopt = {'mark':mark, 
                 'tcpFastOpen':tcp_fast_open, 
                 'tproxy':tproxy}
                super().__init__(self._Sockopt__sockopt)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../script/multicast.py
# Compiled at: 2020-05-05 08:44:18
# Size of source mod 2**32: 12353 bytes
import socket, signal, pyuv, json
from time import *
g_listenip = '0.0.0.0'
g_multicast_port = 30001
g_multicast_addr = '239.255.0.1'
JsonType = 0
ProtoType = 1
topicType = 0
serviceType = 1

class JsnCallBack(object):

    def __init__(self):
        topicName = ''
        jsnSub = None
        jsnCb = None


class MsgCallBack(object):

    def __init__(self):
        topicName = ''
        msgSub = None
        msgCb = None


class ServiceCall(object):

    def __init__(self):
        serviceName = ''
        servCall = ''
        callback = None
        params = {}


class Multicast(object):

    def __init__(self, multicast_addr, localip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        self._Multicast__m_localip = sock.getsockname()[0]
        self.loop = pyuv.Loop.default_loop()
        self._Multicast__m_multicast_addr = multicast_addr
        self._Multicast__m_recv_socket = pyuv.UDP(self.loop)
        self._Multicast__m_recv_socket.bind((g_listenip, g_multicast_port), pyuv.UV_UDP_REUSEADDR)
        self._Multicast__m_recv_socket.set_membership(multicast_addr, pyuv.UV_JOIN_GROUP)
        self._Multicast__m_recv_socket.set_broadcast(True)
        self._Multicast__m_recv_socket.start_recv(self.handlerRecv)
        self._Multicast__m_send_socket = pyuv.UDP(self.loop)
        self._Multicast__m_send_socket.bind((g_listenip, g_multicast_port), pyuv.UV_UDP_REUSEADDR)
        self._Multicast__m_localEndpoint = ''
        self._Multicast__m_localrpcEndpoint = ''
        self._Multicast__m_jsnCbMap = {}
        self._Multicast__m_msgCbMap = {}
        self._Multicast__m_serviceCallMap = {}
        self._Multicast__m_topicMap = {}
        self._Multicast__m_serviceMap = {}
        self._Multicast__m_signal_h = pyuv.Signal(self.loop)
        self._Multicast__m_signal_h.start(self.signal_handler, signal.SIGINT)

    def get_localip(self):
        return self._Multicast__m_localip

    def signal_handler(self, handle, signum):
        self._Multicast__m_signal_h.close()
        self._Multicast__m_recv_socket.close()
        self._Multicast__m_send_socket.close()

    def __del__(self):
        pass

    def setLocalEndpoint(self, pubsubEndpoing, rpcEndpoint):
        self._Multicast__m_localEndpoint = pubsubEndpoing
        self._Multicast__m_localrpcEndpoint = rpcEndpoint

    def dealDelayCallBack(self, topicName):
        jsoncall = self._Multicast__m_jsnCbMap.get(topicName)
        if jsoncall != None:
            jsncb = jsoncall.jsnCb
            jsoncall.jsnSub(topicName, jsncb)
            del self._Multicast__m_jsnCbMap[topicName]
        msgcall = self._Multicast__m_msgCbMap.get(topicName)
        if msgcall != None:
            msgcb = msgcall.msgCb
            msgcall.msgSub(topicName, msgcb)
            del self._Multicast__m_msgCbMap[topicName]

    def dealServiceDelayCall(self, serviceName):
        service_call = self._Multicast__m_serviceCallMap.get(serviceName)
        if service_call != None:
            params = service_call.params
            callback = service_call.callback
            service_call.servCall(serviceName, params, callback)
            del self._Multicast__m_serviceCallMap[serviceName]

    def updateMap(self, type, result):
        if type == topicType:
            print('update topic map')
            endpoints = self._Multicast__m_topicMap.get(result['topic'])
            endpoint = result['endpoint']
            if endpoints != None:
                if endpoint in endpoints:
                    return
                self._Multicast__m_topicMap[result['topic']].append(endpoint)
            else:
                ends = []
                ends.append(endpoint)
                self._Multicast__m_topicMap[result['topic']] = ends
        elif type == serviceType:
            print('update service map')
            endpoints = self._Multicast__m_serviceMap.get(result['service'])
            endpoint = result['endpoint']
            if endpoints != None:
                if endpoint in endpoints:
                    return
                self._Multicast__m_serviceMap[result['service']].append(endpoint)
            else:
                ends = []
                ends.append(endpoint)
                self._Multicast__m_serviceMap[result['service']] = ends

    def findLocalSupport(self, supportName, type):
        if type == topicType:
            self.sendRspToPeer(self._Multicast__m_topicMap, supportName, self._Multicast__m_localEndpoint, 'topic')
        elif type == serviceType:
            self.sendRspToPeer(self._Multicast__m_serviceMap, supportName, self._Multicast__m_localrpcEndpoint, 'service')

    def sendRspToPeer(self, map, supportName, endpoint, field):
        map.setdefault(supportName, None)
        endpoints = map[supportName]
        if endpoints != None:
            if endpoint in endpoints:
                json_dict = {'method': 'response', 
                 field: supportName, 
                 'endpoint': endpoint}
                json_str = json.dumps(json_dict)
                json_bytes = bytes(json_str, encoding='utf8')
                self._Multicast__m_recv_socket.send((self._Multicast__m_multicast_addr, g_multicast_port), json_bytes)

    def multicastTopic(self, topicName, endpoint):
        json_dict = {'method':'commonMulti',  'topic':topicName, 
         'endpoint':endpoint}
        json_str = json.dumps(json_dict)
        json_bytes = bytes(json_str, encoding='utf8')
        self._Multicast__m_send_socket.send((self._Multicast__m_multicast_addr, g_multicast_port), json_bytes)

    def sendRequest(self, supportName, filed):
        json_dict = {'method': 'request', 
         filed: supportName, 
         'endpoint': ''}
        json_str = json.dumps(json_dict)
        json_bytes = bytes(json_str, encoding='utf8')
        self._Multicast__m_send_socket.send((self._Multicast__m_multicast_addr, g_multicast_port), json_bytes)

    def multicastService(self, serviceName, endpoint):
        json_dict = {'method':'commonMulti', 
         'service':serviceName, 
         'endpoint':endpoint}
        json_str = json.dumps(json_dict)
        json_bytes = bytes(json_str, encoding='utf8')
        print('multicastService : ', json_str)
        self._Multicast__m_send_socket.send((self._Multicast__m_multicast_addr, g_multicast_port), json_bytes)

    def findTopic(self, topicName, endpoints=[]):
        res = True
        topic_endpoints = self._Multicast__m_topicMap.get(topicName)
        if topic_endpoints == None:
            res = False
            return res
        else:
            for endpoint in topic_endpoints:
                endpoints.append(endpoint)

            return res

    def findService(self, serviceName, endpoints):
        res = True
        service_endpoints = self._Multicast__m_serviceMap.get(serviceName)
        if service_endpoints == None:
            res = False
            return res
        else:
            for endpoint in service_endpoints:
                endpoints.append(endpoint)

            return res

    def pushTopic_JsonCallBack(self, JsnCallBack):
        self._Multicast__m_jsnCbMap[JsnCallBack.topicName] = JsnCallBack

    def pushTopic_MsgCallBack(self, MsgCallBack):
        self._Multicast__m_msgCbMap[MsgCallBack.topicName] = MsgCallBack

    def pushServiceCallBack(self, serviceCall):
        self._Multicast__m_serviceCallMap[serviceCall.serviceName] = serviceCall

    def run(self):
        self.loop.run()

    def handlerRecv(self, handle, ip_port, flags, data, error):
        if error is None:
            if data is not None:
                json_str = str(data, encoding='utf-8')
                result = json.loads(json_str)
                if 'endpoint' in result.keys():
                    method = result['method']
                    if 'topic' in result.keys():
                        if method == 'commonMulti':
                            self.updateMap(topicType, result)
                            self.dealDelayCallBack(result['topic'])
                        else:
                            if method == 'request':
                                self.findLocalSupport(result['topic'], topicType)
                            else:
                                if method == 'response':
                                    self.updateMap(topicType, result)
                                    self.dealDelayCallBack(result['topic'])
                    elif 'service' in result.keys():
                        if method == 'commonMulti':
                            self.updateMap(serviceType, result)
                            self.dealServiceDelayCall(result['service'])
                        else:
                            if method == 'request':
                                self.findLocalSupport(result['service'], serviceType)
                            else:
                                if method == 'response':
                                    self.updateMap(serviceType, result)
                                    self.dealServiceDelayCall(result['service'])
        else:
            print('error is ', error)
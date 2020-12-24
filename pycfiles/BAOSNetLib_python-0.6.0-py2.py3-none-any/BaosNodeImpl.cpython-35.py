# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../BaosNodeImpl.py
# Compiled at: 2020-03-11 08:33:05
# Size of source mod 2**32: 10766 bytes
import json, zmq, threading
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time
from multicast import *
from ZMQRPCServer import *
from ZMQRPCClient import *

class socketInfo(object):

    def __init__(self, socket, flag):
        self.socket = socket
        self.flag = flag


class AutoLock:

    def __init__(self, lock):
        self._lock = lock
        self._lock.acquire()

    def __del__(self):
        self._lock.release()


class BaosNodeImpl(object):
    m_instance = None
    m_poolSize = 8

    def __init__(self):
        self.m_mutex = []
        self.m_index = 0
        for i in range(BaosNodeImpl.m_poolSize):
            self.m_mutex.append(Lock())

        self.m_connManager = None
        self.m_pool = None
        self.m_servers = None
        self.m_workers = None
        self.m_context = None
        self.m_callback = {'sub': None}
        self.m_jsonHandlers = {}
        self.m_msgQueue = [i for i in range(BaosNodeImpl.m_poolSize)]
        self.m_connection = {}
        self.m_connectionDealWay = {}
        self.m_connectionJson = {}
        self.m_localIP = None
        self.m_localPort = None
        self.m_poller = zmq.Poller()
        self.m_socketInsVec = []

    def init(self, multiIP, localPort, point=None):
        self.m_connManager = Multicast(multiIP, self.m_localIP)
        self.m_localIP = self.m_connManager.get_localip()
        print('self.m_localIP is ', self.m_localIP)
        self.m_localPort = localPort
        self.m_topicEndpoint = 'tcp://' + self.m_localIP + ':' + self.m_localPort
        print('ZMQ PUB Binding to ', self.m_topicEndpoint)
        self.m_context = zmq.Context()
        self.m_pub = self.m_context.socket(zmq.PUB)
        self.m_pub.bind(self.m_topicEndpoint)
        self.m_serviceEndpoint = 'tcp://' + self.m_localIP + ':' + str(int(self.m_localPort) + 1)
        ZMQRPCServer.getInstance().initServer(self.m_serviceEndpoint, BaosNodeImpl.m_poolSize)
        self.m_rpcConnection = {}
        self.m_connManager.setLocalEndpoint(self.m_topicEndpoint, self.m_serviceEndpoint)
        self.m_pool = ThreadPoolExecutor(max_workers=BaosNodeImpl.m_poolSize)
        self.m_pool.submit(Multicast.run, self.m_connManager)
        self.m_pool.submit(self.dealpoller)

    @classmethod
    def getInstance(cls):
        if cls.m_instance == None:
            lock = Lock()
            lock.acquire()
            if cls.m_instance == None:
                cls.m_instance = BaosNodeImpl()
            lock.release()
        return cls.m_instance

    def createMessage(self, type_name):
        pass

    def runService(self):
        self.m_pool.submit(ZMQRPCServer.run, ZMQRPCServer.getInstance())

    def registerService(self, serviceName, f):
        self.m_connManager.multicastService(serviceName, 'tcp://' + str(self.m_localIP) + ':' + str(int(self.m_localPort) + 1))
        ZMQRPCServer.getInstance().registerCall(serviceName, f)

    def callService(self, serviceName, params=None, callback=None):
        endpoints = []
        result = {}
        if self.m_connManager.findService(serviceName, endpoints) == False:
            servicecall = ServiceCall()
            servicecall.params = params
            servicecall.callback = callback
            servicecall.servCall = self.callService
            servicecall.serviceName = serviceName
            self.m_connManager.pushServiceCallBack(servicecall)
            self.m_connManager.sendRequest(serviceName, 'service')
            return result
        for endpoint in endpoints:
            if endpoint in self.m_rpcConnection.keys():
                if callback == None:
                    result = self.m_rpcConnection[endpoint].call(serviceName, params)
                else:
                    self.m_rpcConnection[endpoint].async_call(serviceName, params, callback)
            else:
                self.m_rpcConnection[endpoint] = ZMQRPCClient()
                self.m_rpcConnection[endpoint].connect(endpoint)
                if callback == None:
                    result = self.m_rpcConnection[endpoint].call(serviceName, params)
                else:
                    self.m_rpcConnection[endpoint].async_call(serviceName, params, callback)
            return result

    def publishTopic(self, topic):
        print('get into publishTopic')
        print('topic is ', topic, '  m_topicEndpoint is ', self.m_topicEndpoint)
        self.m_connManager.multicastTopic(topic, self.m_topicEndpoint)

    def publish_json(self, topic, json_str):
        sendstr = topic + '-' + str(json_str)
        print('publish_json send sendstr', sendstr)
        self.m_pub.send_string(sendstr)

    def dealRecv(self, msg, flag, index):
        auto_lock = AutoLock(self.m_mutex[(self.m_index % BaosNodeImpl.m_poolSize)])
        content = msg.split('-')[1]
        topic = msg.split('-')[0]
        if flag == ProtoType:
            pass
        elif flag == JsonType:
            param = json.loads(content)
            handlers = self.m_jsonHandlers[topic]
            for handler in handlers:
                handler(param)

    def addSocket(self, socket, flag):
        self.m_poller.register(socket, zmq.POLLIN)
        self.m_socketInsVec.append(socketInfo(socket, flag))

    def dealpoller(self):
        while True:
            socks = self.m_poller.poll()
            for i in range(len(socks)):
                if socks[i][1] == zmq.POLLIN:
                    try:
                        auto_lock = AutoLock(self.m_mutex[(self.m_index % BaosNodeImpl.m_poolSize)])
                        self.m_msgQueue[self.m_index % BaosNodeImpl.m_poolSize] = self.m_socketInsVec[i].socket.recv_string()
                    except zmq.error as e:
                        print(e)
                        continue

                    self.m_pool.submit(self.dealRecv, self.m_msgQueue[(self.m_index % BaosNodeImpl.m_poolSize)], self.m_socketInsVec[i].flag, self.m_index)
                    self.m_index = self.m_index + 1
                    if self.m_index == BaosNodeImpl.m_poolSize:
                        self.m_index = 0

    def initNewSub(self, endpoint, topic, flag):
        self.m_connection[endpoint] = self.m_context.socket(zmq.SUB)
        print('initNewSub connect endpoint is ', endpoint)
        self.m_connection[endpoint].connect(endpoint)
        self.m_connection[endpoint].setsockopt_string(zmq.SUBSCRIBE, topic)
        self.addSocket(self.m_connection[endpoint], flag)
        if topic not in self.m_connectionDealWay.keys():
            vec = [0 for i in range(10)]
            self.m_connectionDealWay[endpoint] = vec

    def subscribeTopic_Json(self, topic, jsncb):
        endpoints = []
        endpoint = ''
        print('get into subscribeTopic_Json')
        if self.m_connManager.findTopic(topic, endpoints) == False:
            print('can not find topic')
            jsnCB = JsnCallBack()
            jsnCB.jsnCb = jsncb
            jsnCB.jsnSub = self.subscribeTopic_Json
            jsnCB.topicName = topic
            self.m_connManager.pushTopic_JsonCallBack(jsnCB)
            self.m_connManager.sendRequest(topic, 'topic')
            return
        print('subscribeTopic_Json find endpoints is ', endpoints)
        if self.m_jsonHandlers.get(topic) == None:
            jsoncb_list = []
            jsoncb_list.append(jsncb)
            self.m_jsonHandlers[topic] = jsoncb_list
        else:
            self.m_jsonHandlers[topic].append(jsncb)
        for endpoint in endpoints:
            if endpoint not in self.m_connectionJson.keys():
                self.initNewSub(endpoint, topic, JsonType)
            else:
                self.m_connectionJson[endpoint].setsockopt_string(zmq.SUBSCRIBE, topic)
                if self.m_connectionDealWay[endpoint][JsonType] == 0:
                    self.addSocket(self.m_connectionJson[endpoint], JsonType)
                    self.m_connectionDealWay[endpoint][JsonType] = 1

    def unSubscribeTopic(self, topic):
        endpoints = []
        self.m_connManager.findTopic(topic, endpoints)
        for endpoint in endpoints:
            if endpoint in self.m_connectionJson.keys():
                for i in range(len(self.m_jsonHandlers[topic])):
                    self.m_connectionJson[endpoint].setsockopt_string(zmq.UNSUBSCRIBE, topic)

                del self.m_jsonHandlers[topic]
                print('unsubscribe ', topic)
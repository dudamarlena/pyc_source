# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/msb_client/MsbClient.py
# Compiled at: 2018-08-16 06:14:45
# Size of source mod 2**32: 27924 bytes
"""
Copyright (c) 2017
Fraunhofer Institute for Manufacturing Engineering
and Automation (IPA)
Author: Daniel Stock
mailto: daniel DOT stock AT ipa DOT fraunhofer DOT com
See the file "LICENSE" for the full license governing this code.
"""
import websocket, threading, json, jsonschema, jsonpickle, ssl, time, uuid, os, logging
from msb_client.Event import *
from msb_client.Function import *
from random import randint

class MsbClient(websocket.WebSocketApp):

    def __init__(self, service_type=None, uuid=None, name=None, description=None, token=None):
        self.connected = False
        self.registered = False
        self.autoReconnect = True
        self.reconnecting = False
        self.userDisconnect = False
        self.reconnectInterval = 10
        self.keepAlive = False
        self.heartbeat_interval = 8
        self.sockJsFraming = True
        self.debug = False
        self.trace = False
        self.dataFormatValidation = True
        self.eventCache = []
        self.eventCacheEnabled = True
        self.eventCacheSize = 1000
        self.maxMessageSize = 100000000
        self.functions = {}
        self.events = {}
        self.configuration = {}
        self.configuration['parameters'] = {}
        self.msb_url = ''
        self._msb_url = ''
        self.ws = None
        self.hostnameVerification = False
        self.threadAsDaemonEnabled = False
        if (service_type or uuid or name or description or token) is not None:
            self.service_type = service_type
            self.uuid = uuid
            self.name = name
            self.description = description
            self.token = token
        else:
            self.readConfig()

    jsonpickle.set_encoder_options('json', sort_keys=False, indent=4)
    jsonpickle.set_preferred_backend('json')
    MSBMessageTypes = [
     'IO',
     'NIO',
     'IO_CONNECTED',
     'IO_REGISTERED',
     'IO_PUBLISHED',
     'NIO_ALREADY_CONNECTED',
     'NIO_REGISTRATION_ERROR',
     'NIO_UNEXPECTED_REGISTRATION_ERROR',
     'NIO_UNAUTHORIZED_CONNECTION',
     'NIO_EVENT_FORWARDING_ERROR',
     'NIO_UNEXPECTED_EVENT_FORWARDING_ERROR']

    def disableSockJsFraming(self, sockJsFraming):
        self.sockJsFraming = not sockJsFraming
        self.keepAlive = sockJsFraming

    def disableEventCache(self, disableEventCache):
        self.eventCacheEnabled = not disableEventCache

    def enableDataFormatValidation(self, dataFormatValidation):
        self.dataFormatValidation = dataFormatValidation

    def sendBuf(self):
        for idx, msg in enumerate(self.eventCache):
            try:
                if self.connected:
                    if self.registered:
                        logging.debug('SENDING (BUF): ' + msg)
                        if self.sockJsFraming:
                            _msg = self.objectToJson(msg).replace('\\n', '')
                            self.ws.send('["E ' + _msg[1:-1] + '"]')
                        else:
                            self.ws.send('E ' + msg)
                        self.eventCache.pop(idx)
            except:
                pass

    def on_message(self, message):
        if self.sockJsFraming:
            if self.debug:
                if message.startswith('h'):
                    logging.debug('♥')
            message = message[3:-2]
        else:
            if message in self.MSBMessageTypes:
                logging.info(message)
                if message == 'IO_CONNECTED':
                    if self.reconnecting:
                        self.reconnecting = False
                        if self.sockJsFraming:
                            _selfd = json.dumps(self.objectToJson(self.getSelfDescription())).replace('\\n', '')
                            self.ws.send('["R ' + _selfd[1:-1] + '"]')
                        else:
                            self.ws.send('R ' + self.objectToJson(self.getSelfDescription()))
                elif message == 'IO_REGISTERED':
                    self.registered = True
                    if self.eventCacheEnabled:
                        self.connected = True
                        self.sendBuf()
                else:
                    if message == 'NIO_ALREADY_CONNECTED':
                        if self.connected:
                            try:
                                ws.close()
                            except Exception:
                                pass

                    else:
                        if message == 'NIO_UNEXPECTED_REGISTRATION_ERROR':
                            if self.connected:
                                try:
                                    ws.close()
                                except Exception:
                                    pass

                        else:
                            if message == 'NIO_UNAUTHORIZED_CONNECTION' and self.connected:
                                try:
                                    ws.close()
                                except Exception:
                                    pass

                                if message.startswith('C'):
                                    jmsg = message.replace('\\"', '"')
                                    jmsg = json.loads(jmsg[2:])
                                    logging.info(str(jmsg))
                                    if jmsg['functionId'] not in self.functions:
                                        if jmsg['functionId'].startswith('/'):
                                            if not jmsg['functionId'].startswith('//'):
                                                jmsg['functionId'] = jmsg['functionId'][1:]
                                    if jmsg['functionId'] in self.functions:
                                        jmsg['functionParameters']['correlationId'] = jmsg['correlationId']
                                        self.functions[jmsg['functionId']].implementation(jmsg['functionParameters'])
                            else:
                                logging.warning('Function could not be found: ' + jmsg['functionId'])
            else:
                pass
            if message.startswith('K'):
                jmsg = message.replace('\\"', '"')
                jmsg = json.loads(jmsg[2:])
                logging.info(str(jmsg))
                logging.debug('CONFIGURATION: ' + str(jmsg))
                if jmsg['uuid'] == self.uuid:
                    for key in jmsg['params']:
                        if key in self.configuration['parameters']:
                            self.changeConfigParameter(key, jmsg['params'][key])

                    self.reRegister()

    def on_error(self, error):
        logging.error(error)

    def on_close(self):
        logging.debug('DISCONNECTED')
        self.connected = False
        self.registered = False
        if self.autoReconnect:
            if not self.userDisconnect:
                logging.info('### closed, waiting ' + str(self.reconnectInterval) + ' seconds before reconnect. ###')
                time.sleep(self.reconnectInterval)
                self.reconnecting = True
                logging.info('Start reconnecting to msb url: >' + self.msb_url + '<')
                self.connect(self.msb_url)

    def on_open(self):
        logging.debug('Socket open')
        self.connected = True

    def enableDebug(self, debug=False):
        if debug:
            logging.basicConfig(format='[%(asctime)s] %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.basicConfig(format='[%(asctime)s] %(message)s')
            logging.getLogger().setLevel(logging.INFO)
        self.debug = debug

    def enableTrace(self, trace=False):
        websocket.enableTrace(trace)

    def disableHostnameVerification(self, hostnameVerification=True):
        self.hostnameVerification = hostnameVerification

    def disableAutoReconnect(self, autoReconnect=False):
        self.autoReconnect = not autoReconnect

    def setReconnectInterval(self, interval=10000):
        self.reconnectInterval = interval / 1000

    def setEventCacheSize(self, eventCacheSize=True):
        self.eventCacheSize = eventCacheSize

    def enableThreadAsDaemon(self, threadAsDaemonEnabled=False):
        self.threadAsDaemonEnabled = threadAsDaemonEnabled

    def setKeepAlive(self, keepAlive=True, heartbeat_interval=8000):
        self.keepAlive = keepAlive
        if heartbeat_interval < 8000:
            self.heartbeat_interval = 8000
        else:
            self.heartbeat_interval = heartbeat_interval / 1000

    def _checkUrl(self, msb_url=None):
        server_id = str(randint(100, 999))
        session_id = str(uuid.uuid4()).replace('-', '')
        if msb_url is not None:
            self.msb_url = msb_url
        if 'http://' in self.msb_url:
            self.msb_url = self.msb_url.replace('http://', 'ws://')
        else:
            if 'https://' in self.msb_url:
                self.msb_url = self.msb_url.replace('https://', 'wss://')
            else:
                if not self.msb_url.startswith('ws://'):
                    if not self.msb_url.startswith('wss://'):
                        logging.error('WRONG MSB URL FORMAT: ' + str(self.msb_url))
                if self.sockJsFraming:
                    self._msb_url = self.msb_url + '/websocket/data/' + server_id + '/' + session_id + '/websocket'
                else:
                    self._msb_url = self.msb_url + '/websocket/data/websocket'

    def connect(self, msb_url=None):
        self.userDisconnect = False
        self._checkUrl(msb_url)
        ws = websocket.WebSocketApp((self._msb_url), on_message=(self.on_message),
          on_error=(self.on_error),
          on_close=(self.on_close))
        self.ws = ws
        ws.on_open = self.on_open

        def runf():
            try:
                if self.hostnameVerification:
                    if self.keepAlive:
                        ws.run_forever(ping_interval=(self.heartbeat_interval), ping_timeout=(self.heartbeat_interval - 5), sslopt={'cert_reqs':ssl.CERT_NONE, 
                         'check_hostname':False})
                    else:
                        ws.run_forever(sslopt={'cert_reqs':ssl.CERT_NONE,  'check_hostname':False})
                elif self.keepAlive:
                    ws.run_forever(ping_interval=(self.heartbeat_interval), ping_timeout=(self.heartbeat_interval - 3))
                else:
                    ws.run_forever()
            except:
                pass

        logging.info('Connecting to MSB @ ' + self.msb_url)
        wst = threading.Thread(target=runf)
        if self.threadAsDaemonEnabled:
            wst.setDaemon(True)
        wst.start()

    def disconnect(self):
        self.userDisconnect = True
        self.ws.close()

    def register(self):

        def _sendReg():
            if self.sockJsFraming:
                _selfd = json.dumps(self.objectToJson(self.getSelfDescription())).replace('\\n', '')
                _selfd = _selfd[1:-1]
                self.ws.send('["R ' + _selfd + '"]')
            else:
                self.ws.send('R ' + self.objectToJson(self.getSelfDescription()))

        def _set_interval(func, sec):

            def func_wrapper():
                if self.connected:
                    func()
                else:
                    _set_interval(func, sec)

            t = threading.Timer(sec, func_wrapper)
            t.start()
            return t

        _set_interval(_sendReg, 0.1)

    def addEvent--- This code section failed: ---

 L. 291         0  LOAD_FAST                'isArray'
              2_4  POP_JUMP_IF_FALSE   284  'to 284'

 L. 292         6  LOAD_GLOBAL              isinstance
                8  LOAD_FAST                'event_dataformat'
               10  LOAD_GLOBAL              ComplexDataFormat
               12  CALL_FUNCTION_2       2  '2 positional arguments'
               14  POP_JUMP_IF_FALSE   102  'to 102'

 L. 293        16  LOAD_STR                 'array'
               18  LOAD_FAST                'event_dataformat'
               20  LOAD_ATTR                dataFormat
               22  LOAD_STR                 'dataObject'
               24  BINARY_SUBSCR    
               26  LOAD_STR                 'type'
               28  STORE_SUBSCR     

 L. 294        30  BUILD_MAP_0           0 
               32  LOAD_FAST                'event_dataformat'
               34  LOAD_ATTR                dataFormat
               36  LOAD_STR                 'dataObject'
               38  BINARY_SUBSCR    
               40  LOAD_STR                 'items'
               42  STORE_SUBSCR     

 L. 295        44  BUILD_MAP_0           0 
               46  LOAD_FAST                'event_dataformat'
               48  LOAD_ATTR                dataFormat
               50  LOAD_STR                 'dataObject'
               52  BINARY_SUBSCR    
               54  LOAD_STR                 'items'
               56  BINARY_SUBSCR    
               58  LOAD_STR                 '$ref'
               60  STORE_SUBSCR     

 L. 296        62  LOAD_FAST                'event_dataformat'
               64  LOAD_ATTR                dataFormat
               66  LOAD_STR                 'dataObject'
               68  BINARY_SUBSCR    

 L. 297        70  LOAD_STR                 '$ref'
               72  BINARY_SUBSCR    
               74  LOAD_FAST                'event_dataformat'
               76  LOAD_ATTR                dataFormat
               78  LOAD_STR                 'dataObject'
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'items'
               84  BINARY_SUBSCR    
               86  LOAD_STR                 '$ref'
               88  STORE_SUBSCR     

 L. 298        90  LOAD_FAST                'event_dataformat'
               92  LOAD_ATTR                dataFormat
               94  LOAD_STR                 'dataObject'
               96  BINARY_SUBSCR    
               98  LOAD_STR                 '$ref'
              100  DELETE_SUBSCR    
            102_0  COME_FROM            14  '14'

 L. 299       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'event'
              106  LOAD_GLOBAL              Event
              108  CALL_FUNCTION_2       2  '2 positional arguments'
              110  POP_JUMP_IF_FALSE   186  'to 186'

 L. 300       112  LOAD_GLOBAL              vadilateEventDataFormat
              114  LOAD_FAST                'event'
              116  LOAD_ATTR                dataFormat
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  POP_JUMP_IF_FALSE   184  'to 184'

 L. 301       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                events
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  LOAD_CONST               1
              132  BINARY_ADD       
              134  LOAD_FAST                'event'
              136  STORE_ATTR               id

 L. 302       138  LOAD_FAST                'event'
              140  LOAD_ATTR                eventId
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                events
              146  COMPARE_OP               not-in
              148  POP_JUMP_IF_FALSE   164  'to 164'

 L. 303       150  LOAD_FAST                'event'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                events
              156  LOAD_FAST                'event'
              158  LOAD_ATTR                eventId
              160  STORE_SUBSCR     
              162  JUMP_FORWARD        184  'to 184'
            164_0  COME_FROM           148  '148'

 L. 305       164  LOAD_GLOBAL              logging
              166  LOAD_METHOD              error
              168  LOAD_GLOBAL              str
              170  LOAD_FAST                'event'
              172  LOAD_ATTR                eventId
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_STR                 ' already in events, change event id!'
              178  BINARY_ADD       
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          
            184_0  COME_FROM           162  '162'
            184_1  COME_FROM           120  '120'
              184  JUMP_FORWARD        710  'to 710'
            186_0  COME_FROM           110  '110'

 L. 307       186  LOAD_GLOBAL              Event
              188  LOAD_FAST                'event'
              190  LOAD_FAST                'event_name'
              192  LOAD_FAST                'event_description'
              194  LOAD_FAST                'event_dataformat'
              196  LOAD_FAST                'event_priority'
              198  LOAD_FAST                'isArray'
              200  CALL_FUNCTION_6       6  '6 positional arguments'
              202  STORE_FAST               '_event'

 L. 308       204  LOAD_GLOBAL              vadilateEventDataFormat
              206  LOAD_FAST                '_event'
              208  LOAD_ATTR                dataFormat
              210  CALL_FUNCTION_1       1  '1 positional argument'
          212_214  POP_JUMP_IF_FALSE   710  'to 710'

 L. 309       216  LOAD_GLOBAL              len
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                events
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  LOAD_CONST               1
              226  BINARY_ADD       
              228  LOAD_FAST                '_event'
              230  STORE_ATTR               id

 L. 310       232  LOAD_FAST                '_event'
              234  LOAD_ATTR                eventId
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                events
              240  COMPARE_OP               not-in
          242_244  POP_JUMP_IF_FALSE   260  'to 260'

 L. 311       246  LOAD_FAST                '_event'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                events
              252  LOAD_FAST                '_event'
              254  LOAD_ATTR                eventId
              256  STORE_SUBSCR     
              258  JUMP_FORWARD        710  'to 710'
            260_0  COME_FROM           242  '242'

 L. 313       260  LOAD_GLOBAL              logging
              262  LOAD_METHOD              error
              264  LOAD_GLOBAL              str
              266  LOAD_FAST                '_event'
              268  LOAD_ATTR                eventId
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  LOAD_STR                 ' already in events, change event id!'
              274  BINARY_ADD       
              276  CALL_METHOD_1         1  '1 positional argument'
              278  POP_TOP          
          280_282  JUMP_FORWARD        710  'to 710'
            284_0  COME_FROM             2  '2'

 L. 315       284  LOAD_GLOBAL              isinstance
              286  LOAD_FAST                'event'
              288  LOAD_GLOBAL              Event
              290  CALL_FUNCTION_2       2  '2 positional arguments'
          292_294  POP_JUMP_IF_FALSE   616  'to 616'

 L. 316       296  LOAD_GLOBAL              vadilateEventDataFormat
              298  LOAD_FAST                'event'
              300  LOAD_ATTR                dataFormat
              302  CALL_FUNCTION_1       1  '1 positional argument'
          304_306  POP_JUMP_IF_FALSE   710  'to 710'

 L. 317       308  LOAD_FAST                'event'
              310  LOAD_ATTR                isArray
          312_314  POP_JUMP_IF_FALSE   550  'to 550'

 L. 318       316  LOAD_STR                 '$ref'
              318  LOAD_FAST                'event'
              320  LOAD_ATTR                dataFormat
              322  LOAD_STR                 'dataObject'
              324  BINARY_SUBSCR    
              326  COMPARE_OP               in
          328_330  POP_JUMP_IF_FALSE   484  'to 484'

 L. 319       332  LOAD_STR                 'array'
              334  LOAD_FAST                'event'
              336  LOAD_ATTR                dataFormat
              338  LOAD_STR                 'dataObject'
              340  BINARY_SUBSCR    
              342  LOAD_STR                 'type'
              344  STORE_SUBSCR     

 L. 320       346  BUILD_MAP_0           0 
              348  LOAD_FAST                'event'
              350  LOAD_ATTR                dataFormat
              352  LOAD_STR                 'dataObject'
              354  BINARY_SUBSCR    
              356  LOAD_STR                 'items'
              358  STORE_SUBSCR     

 L. 321       360  BUILD_MAP_0           0 
              362  LOAD_FAST                'event'
              364  LOAD_ATTR                dataFormat
              366  LOAD_STR                 'dataObject'
              368  BINARY_SUBSCR    
              370  LOAD_STR                 'items'
              372  BINARY_SUBSCR    
              374  LOAD_STR                 '$ref'
              376  STORE_SUBSCR     

 L. 322       378  LOAD_FAST                'event'
              380  LOAD_ATTR                dataFormat
              382  LOAD_STR                 'dataObject'
              384  BINARY_SUBSCR    
              386  LOAD_STR                 '$ref'
              388  BINARY_SUBSCR    
              390  LOAD_FAST                'event'
              392  LOAD_ATTR                dataFormat
              394  LOAD_STR                 'dataObject'
              396  BINARY_SUBSCR    
              398  LOAD_STR                 'items'
              400  BINARY_SUBSCR    
              402  LOAD_STR                 '$ref'
              404  STORE_SUBSCR     

 L. 323       406  LOAD_FAST                'event'
              408  LOAD_ATTR                dataFormat
              410  LOAD_STR                 'dataObject'
              412  BINARY_SUBSCR    
              414  LOAD_STR                 '$ref'
              416  DELETE_SUBSCR    

 L. 324       418  LOAD_GLOBAL              len
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                events
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  LOAD_CONST               1
              428  BINARY_ADD       
              430  LOAD_FAST                'event'
              432  STORE_ATTR               id

 L. 325       434  LOAD_FAST                'event'
              436  LOAD_ATTR                eventId
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                events
              442  COMPARE_OP               not-in
          444_446  POP_JUMP_IF_FALSE   462  'to 462'

 L. 326       448  LOAD_FAST                'event'
              450  LOAD_FAST                'self'
              452  LOAD_ATTR                events
              454  LOAD_FAST                'event'
              456  LOAD_ATTR                eventId
              458  STORE_SUBSCR     
              460  JUMP_FORWARD        482  'to 482'
            462_0  COME_FROM           444  '444'

 L. 328       462  LOAD_GLOBAL              logging
              464  LOAD_METHOD              error
              466  LOAD_GLOBAL              str
              468  LOAD_FAST                'event'
              470  LOAD_ATTR                eventId
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  LOAD_STR                 ' already in events, change event id!'
              476  BINARY_ADD       
              478  CALL_METHOD_1         1  '1 positional argument'
              480  POP_TOP          
            482_0  COME_FROM           460  '460'
              482  JUMP_FORWARD        548  'to 548'
            484_0  COME_FROM           328  '328'

 L. 330       484  LOAD_GLOBAL              len
              486  LOAD_FAST                'self'
              488  LOAD_ATTR                events
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  LOAD_CONST               1
              494  BINARY_ADD       
              496  LOAD_FAST                'event'
              498  STORE_ATTR               id

 L. 331       500  LOAD_FAST                'event'
              502  LOAD_ATTR                eventId
              504  LOAD_FAST                'self'
              506  LOAD_ATTR                events
              508  COMPARE_OP               not-in
          510_512  POP_JUMP_IF_FALSE   528  'to 528'

 L. 332       514  LOAD_FAST                'event'
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                events
              520  LOAD_FAST                'event'
              522  LOAD_ATTR                eventId
              524  STORE_SUBSCR     
              526  JUMP_FORWARD        548  'to 548'
            528_0  COME_FROM           510  '510'

 L. 334       528  LOAD_GLOBAL              logging
              530  LOAD_METHOD              error
              532  LOAD_GLOBAL              str
              534  LOAD_FAST                'event'
              536  LOAD_ATTR                eventId
              538  CALL_FUNCTION_1       1  '1 positional argument'
              540  LOAD_STR                 ' already in events, change event id!'
              542  BINARY_ADD       
              544  CALL_METHOD_1         1  '1 positional argument'
              546  POP_TOP          
            548_0  COME_FROM           526  '526'
            548_1  COME_FROM           482  '482'
              548  JUMP_FORWARD        614  'to 614'
            550_0  COME_FROM           312  '312'

 L. 336       550  LOAD_GLOBAL              len
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                events
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  LOAD_CONST               1
              560  BINARY_ADD       
              562  LOAD_FAST                'event'
              564  STORE_ATTR               id

 L. 337       566  LOAD_FAST                'event'
              568  LOAD_ATTR                eventId
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                events
              574  COMPARE_OP               not-in
          576_578  POP_JUMP_IF_FALSE   594  'to 594'

 L. 338       580  LOAD_FAST                'event'
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                events
              586  LOAD_FAST                'event'
              588  LOAD_ATTR                eventId
              590  STORE_SUBSCR     
              592  JUMP_FORWARD        614  'to 614'
            594_0  COME_FROM           576  '576'

 L. 340       594  LOAD_GLOBAL              logging
              596  LOAD_METHOD              error
              598  LOAD_GLOBAL              str
              600  LOAD_FAST                'event'
              602  LOAD_ATTR                eventId
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  LOAD_STR                 ' already in events, change event id!'
              608  BINARY_ADD       
              610  CALL_METHOD_1         1  '1 positional argument'
            612_0  COME_FROM           184  '184'
              612  POP_TOP          
            614_0  COME_FROM           592  '592'
            614_1  COME_FROM           548  '548'
              614  JUMP_FORWARD        710  'to 710'
            616_0  COME_FROM           292  '292'

 L. 342       616  LOAD_GLOBAL              Event
              618  LOAD_FAST                'event'
              620  LOAD_FAST                'event_name'
              622  LOAD_FAST                'event_description'
              624  LOAD_FAST                'event_dataformat'
              626  LOAD_FAST                'event_priority'
              628  LOAD_FAST                'isArray'
              630  CALL_FUNCTION_6       6  '6 positional arguments'
              632  STORE_FAST               '_event'

 L. 343       634  LOAD_GLOBAL              vadilateEventDataFormat
              636  LOAD_FAST                '_event'
              638  LOAD_ATTR                dataFormat
              640  CALL_FUNCTION_1       1  '1 positional argument'
          642_644  POP_JUMP_IF_FALSE   710  'to 710'

 L. 344       646  LOAD_GLOBAL              len
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                events
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  LOAD_CONST               1
              656  BINARY_ADD       
              658  LOAD_FAST                '_event'
              660  STORE_ATTR               id

 L. 345       662  LOAD_FAST                '_event'
              664  LOAD_ATTR                eventId
              666  LOAD_FAST                'self'
              668  LOAD_ATTR                events
              670  COMPARE_OP               not-in
          672_674  POP_JUMP_IF_FALSE   690  'to 690'

 L. 346       676  LOAD_FAST                '_event'
              678  LOAD_FAST                'self'
              680  LOAD_ATTR                events
              682  LOAD_FAST                '_event'
              684  LOAD_ATTR                eventId
            686_0  COME_FROM           258  '258'
              686  STORE_SUBSCR     
              688  JUMP_FORWARD        710  'to 710'
            690_0  COME_FROM           672  '672'

 L. 348       690  LOAD_GLOBAL              logging
              692  LOAD_METHOD              error
              694  LOAD_GLOBAL              str
              696  LOAD_FAST                '_event'
              698  LOAD_ATTR                eventId
              700  CALL_FUNCTION_1       1  '1 positional argument'
              702  LOAD_STR                 ' already in events, change event id!'
              704  BINARY_ADD       
              706  CALL_METHOD_1         1  '1 positional argument'
              708  POP_TOP          
            710_0  COME_FROM           688  '688'
            710_1  COME_FROM           642  '642'
            710_2  COME_FROM           614  '614'
            710_3  COME_FROM           304  '304'
            710_4  COME_FROM           280  '280'
            710_5  COME_FROM           212  '212'

Parse error at or near `COME_FROM' instruction at offset 612_0

    def addFunction--- This code section failed: ---

 L. 351         0  LOAD_FAST                'isArray'
                2  POP_JUMP_IF_FALSE   248  'to 248'

 L. 352         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'function'
                8  LOAD_GLOBAL              Function
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  POP_JUMP_IF_FALSE   168  'to 168'

 L. 353        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'function_dataformat'
               18  LOAD_GLOBAL              ComplexDataFormat
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE   110  'to 110'

 L. 354        24  LOAD_STR                 'array'
               26  LOAD_FAST                'function_dataformat'
               28  LOAD_ATTR                dataFormat
               30  LOAD_STR                 'dataObject'
               32  BINARY_SUBSCR    
               34  LOAD_STR                 'type'
               36  STORE_SUBSCR     

 L. 355        38  BUILD_MAP_0           0 
               40  LOAD_FAST                'function_dataformat'
               42  LOAD_ATTR                dataFormat
               44  LOAD_STR                 'dataObject'
               46  BINARY_SUBSCR    
               48  LOAD_STR                 'items'
               50  STORE_SUBSCR     

 L. 356        52  BUILD_MAP_0           0 
               54  LOAD_FAST                'function_dataformat'
               56  LOAD_ATTR                dataFormat
               58  LOAD_STR                 'dataObject'
               60  BINARY_SUBSCR    
               62  LOAD_STR                 'items'
               64  BINARY_SUBSCR    
               66  LOAD_STR                 '$ref'
               68  STORE_SUBSCR     

 L. 358        70  LOAD_FAST                'function_dataformat'
               72  LOAD_ATTR                dataFormat
               74  LOAD_STR                 'dataObject'
               76  BINARY_SUBSCR    
               78  LOAD_STR                 '$ref'
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'function_dataformat'
               84  LOAD_ATTR                dataFormat
               86  LOAD_STR                 'dataObject'
               88  BINARY_SUBSCR    
               90  LOAD_STR                 'items'
               92  BINARY_SUBSCR    
               94  LOAD_STR                 '$ref'
               96  STORE_SUBSCR     

 L. 359        98  LOAD_FAST                'function_dataformat'
              100  LOAD_ATTR                dataFormat
              102  LOAD_STR                 'dataObject'
              104  BINARY_SUBSCR    
              106  LOAD_STR                 '$ref'
              108  DELETE_SUBSCR    
            110_0  COME_FROM            22  '22'

 L. 360       110  LOAD_GLOBAL              vadilateFunctionDataFormat
              112  LOAD_FAST                'function'
              114  LOAD_ATTR                dataFormat
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  POP_JUMP_IF_FALSE   244  'to 244'

 L. 361       120  LOAD_FAST                'function'
              122  LOAD_ATTR                functionId
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                functions
              128  COMPARE_OP               not-in
              130  POP_JUMP_IF_FALSE   146  'to 146'

 L. 362       132  LOAD_FAST                'function'
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                functions
              138  LOAD_FAST                'function'
              140  LOAD_ATTR                functionId
              142  STORE_SUBSCR     
              144  JUMP_ABSOLUTE       244  'to 244'
            146_0  COME_FROM           130  '130'

 L. 364       146  LOAD_GLOBAL              logging
              148  LOAD_METHOD              error
              150  LOAD_GLOBAL              str
              152  LOAD_FAST                'function'
              154  LOAD_ATTR                functionId
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  LOAD_STR                 ' already in functions, change event id!'
              160  BINARY_ADD       
              162  CALL_METHOD_1         1  '1 positional argument'
              164  POP_TOP          
              166  JUMP_FORWARD        612  'to 612'
            168_0  COME_FROM            12  '12'

 L. 367       168  LOAD_GLOBAL              Function
              170  LOAD_FAST                'function'
              172  LOAD_FAST                'function_name'
              174  LOAD_FAST                'function_description'
              176  LOAD_FAST                'function_dataformat'
              178  LOAD_FAST                'fnpointer'
              180  LOAD_FAST                'isArray'
              182  LOAD_FAST                'responseEvents'
              184  CALL_FUNCTION_7       7  '7 positional arguments'
              186  STORE_FAST               '_function'

 L. 368       188  LOAD_GLOBAL              vadilateFunctionDataFormat
              190  LOAD_FAST                '_function'
              192  LOAD_ATTR                dataFormat
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  POP_JUMP_IF_FALSE   244  'to 244'

 L. 369       198  LOAD_FAST                '_function'
              200  LOAD_ATTR                functionId
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                functions
              206  COMPARE_OP               not-in
              208  POP_JUMP_IF_FALSE   224  'to 224'

 L. 370       210  LOAD_FAST                '_function'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                functions
              216  LOAD_FAST                '_function'
              218  LOAD_ATTR                functionId
              220  STORE_SUBSCR     
              222  JUMP_FORWARD        612  'to 612'
            224_0  COME_FROM           208  '208'

 L. 372       224  LOAD_GLOBAL              logging
              226  LOAD_METHOD              error
              228  LOAD_GLOBAL              str
              230  LOAD_FAST                '_function'
              232  LOAD_ATTR                functionId
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  LOAD_STR                 ' already in functions, change event id!'
              238  BINARY_ADD       
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
            244_0  COME_FROM           196  '196'
            244_1  COME_FROM           118  '118'
          244_246  JUMP_FORWARD        612  'to 612'
            248_0  COME_FROM             2  '2'

 L. 374       248  LOAD_GLOBAL              isinstance
              250  LOAD_FAST                'function'
              252  LOAD_GLOBAL              Function
              254  CALL_FUNCTION_2       2  '2 positional arguments'
          256_258  POP_JUMP_IF_FALSE   532  'to 532'

 L. 375       260  LOAD_GLOBAL              vadilateFunctionDataFormat
              262  LOAD_FAST                'function'
              264  LOAD_ATTR                dataFormat
              266  CALL_FUNCTION_1       1  '1 positional argument'
          268_270  POP_JUMP_IF_FALSE   612  'to 612'

 L. 376       272  LOAD_FAST                'function'
              274  LOAD_ATTR                isArray
          276_278  POP_JUMP_IF_FALSE   482  'to 482'

 L. 377       280  LOAD_STR                 '$ref'
              282  LOAD_FAST                'function'
              284  LOAD_ATTR                dataFormat
              286  LOAD_STR                 'dataObject'
              288  BINARY_SUBSCR    
              290  COMPARE_OP               in
          292_294  POP_JUMP_IF_FALSE   432  'to 432'

 L. 378       296  LOAD_STR                 'array'
              298  LOAD_FAST                'function'
              300  LOAD_ATTR                dataFormat
              302  LOAD_STR                 'dataObject'
              304  BINARY_SUBSCR    
              306  LOAD_STR                 'type'
              308  STORE_SUBSCR     

 L. 379       310  BUILD_MAP_0           0 
              312  LOAD_FAST                'function'
              314  LOAD_ATTR                dataFormat
              316  LOAD_STR                 'dataObject'
              318  BINARY_SUBSCR    
              320  LOAD_STR                 'items'
              322  STORE_SUBSCR     

 L. 380       324  BUILD_MAP_0           0 
              326  LOAD_FAST                'function'
              328  LOAD_ATTR                dataFormat
              330  LOAD_STR                 'dataObject'
              332  BINARY_SUBSCR    
              334  LOAD_STR                 'items'
              336  BINARY_SUBSCR    
              338  LOAD_STR                 '$ref'
              340  STORE_SUBSCR     

 L. 382       342  LOAD_FAST                'function'
              344  LOAD_ATTR                dataFormat
              346  LOAD_STR                 'dataObject'
              348  BINARY_SUBSCR    
              350  LOAD_STR                 '$ref'
              352  BINARY_SUBSCR    
              354  LOAD_FAST                'function'
              356  LOAD_ATTR                dataFormat
              358  LOAD_STR                 'dataObject'
              360  BINARY_SUBSCR    
              362  LOAD_STR                 'items'
              364  BINARY_SUBSCR    
              366  LOAD_STR                 '$ref'
              368  STORE_SUBSCR     

 L. 383       370  LOAD_FAST                'function'
              372  LOAD_ATTR                dataFormat
              374  LOAD_STR                 'dataObject'
              376  BINARY_SUBSCR    
              378  LOAD_STR                 '$ref'
              380  DELETE_SUBSCR    

 L. 384       382  LOAD_FAST                'function'
              384  LOAD_ATTR                functionId
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                functions
              390  COMPARE_OP               not-in
          392_394  POP_JUMP_IF_FALSE   410  'to 410'

 L. 385       396  LOAD_FAST                'function'
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                functions
              402  LOAD_FAST                'function'
              404  LOAD_ATTR                functionId
              406  STORE_SUBSCR     
              408  JUMP_FORWARD        430  'to 430'
            410_0  COME_FROM           392  '392'

 L. 387       410  LOAD_GLOBAL              logging
              412  LOAD_METHOD              error
              414  LOAD_GLOBAL              str
              416  LOAD_FAST                'function'
              418  LOAD_ATTR                functionId
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  LOAD_STR                 ' already in functions, change event id!'
              424  BINARY_ADD       
              426  CALL_METHOD_1         1  '1 positional argument'
              428  POP_TOP          
            430_0  COME_FROM           408  '408'
              430  JUMP_FORWARD        480  'to 480'
            432_0  COME_FROM           292  '292'

 L. 389       432  LOAD_FAST                'function'
              434  LOAD_ATTR                functionId
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                functions
              440  COMPARE_OP               not-in
          442_444  POP_JUMP_IF_FALSE   460  'to 460'

 L. 390       446  LOAD_FAST                'function'
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                functions
              452  LOAD_FAST                'function'
              454  LOAD_ATTR                functionId
              456  STORE_SUBSCR     
              458  JUMP_FORWARD        480  'to 480'
            460_0  COME_FROM           442  '442'

 L. 392       460  LOAD_GLOBAL              logging
              462  LOAD_METHOD              error
              464  LOAD_GLOBAL              str
              466  LOAD_FAST                'function'
              468  LOAD_ATTR                functionId
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  LOAD_STR                 ' already in functions, change event id!'
              474  BINARY_ADD       
              476  CALL_METHOD_1         1  '1 positional argument'
              478  POP_TOP          
            480_0  COME_FROM           458  '458'
            480_1  COME_FROM           430  '430'
              480  JUMP_FORWARD        530  'to 530'
            482_0  COME_FROM           276  '276'

 L. 394       482  LOAD_FAST                'function'
              484  LOAD_ATTR                functionId
              486  LOAD_FAST                'self'
              488  LOAD_ATTR                functions
              490  COMPARE_OP               not-in
          492_494  POP_JUMP_IF_FALSE   510  'to 510'

 L. 395       496  LOAD_FAST                'function'
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                functions
              502  LOAD_FAST                'function'
              504  LOAD_ATTR                functionId
              506  STORE_SUBSCR     
              508  JUMP_FORWARD        530  'to 530'
            510_0  COME_FROM           492  '492'

 L. 397       510  LOAD_GLOBAL              logging
              512  LOAD_METHOD              error
              514  LOAD_GLOBAL              str
              516  LOAD_FAST                'function'
              518  LOAD_ATTR                functionId
              520  CALL_FUNCTION_1       1  '1 positional argument'
              522  LOAD_STR                 ' already in functions, change event id!'
              524  BINARY_ADD       
              526  CALL_METHOD_1         1  '1 positional argument'
              528  POP_TOP          
            530_0  COME_FROM           508  '508'
            530_1  COME_FROM           480  '480'
              530  JUMP_FORWARD        612  'to 612'
            532_0  COME_FROM           256  '256'
            532_1  COME_FROM           166  '166'

 L. 399       532  LOAD_GLOBAL              Function
              534  LOAD_FAST                'function'
              536  LOAD_FAST                'function_name'
              538  LOAD_FAST                'function_description'
              540  LOAD_FAST                'function_dataformat'
              542  LOAD_FAST                'fnpointer'
              544  LOAD_FAST                'isArray'
              546  LOAD_FAST                'responseEvents'
              548  CALL_FUNCTION_7       7  '7 positional arguments'
              550  STORE_FAST               '_function'

 L. 400       552  LOAD_GLOBAL              vadilateFunctionDataFormat
              554  LOAD_FAST                '_function'
              556  LOAD_ATTR                dataFormat
              558  CALL_FUNCTION_1       1  '1 positional argument'
          560_562  POP_JUMP_IF_FALSE   612  'to 612'

 L. 401       564  LOAD_FAST                '_function'
              566  LOAD_ATTR                functionId
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                functions
              572  COMPARE_OP               not-in
          574_576  POP_JUMP_IF_FALSE   592  'to 592'

 L. 402       578  LOAD_FAST                '_function'
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                functions
              584  LOAD_FAST                '_function'
              586  LOAD_ATTR                functionId
            588_0  COME_FROM           222  '222'
              588  STORE_SUBSCR     
              590  JUMP_FORWARD        612  'to 612'
            592_0  COME_FROM           574  '574'

 L. 404       592  LOAD_GLOBAL              logging
              594  LOAD_METHOD              error
              596  LOAD_GLOBAL              str
              598  LOAD_FAST                '_function'
              600  LOAD_ATTR                functionId
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  LOAD_STR                 ' already in functions, change event id!'
              606  BINARY_ADD       
              608  CALL_METHOD_1         1  '1 positional argument'
              610  POP_TOP          
            612_0  COME_FROM           590  '590'
            612_1  COME_FROM           560  '560'
            612_2  COME_FROM           530  '530'
            612_3  COME_FROM           268  '268'
            612_4  COME_FROM           244  '244'

Parse error at or near `COME_FROM' instruction at offset 588_0

    def setEventValue(self, eventId, eventValue):
        if eventId in self.events:
            self.events[eventId].dataObject = eventValue

    def publish(self, eventId, dataObject=None, priority=None, cached=False, postDate=None, correlationId=None):
        event = {}
        if dataObject is not None:
            self.events[eventId].dataObject = dataObject
            event['dataObject'] = self.events[eventId].dataObject
        if priority is not None:
            self.events[eventId].priority = priority
        event['eventId'] = eventId
        event['uuid'] = self.uuid
        if correlationId is not None:
            event['correlationId'] = correlationId
        event['priority'] = self.events[eventId].priority
        if postDate is None:
            event['postDate'] = datetime.datetime.now().isoformat()
        if self.dataFormatValidation:
            if dataObject is not None:
                if isinstance(self.events[eventId].df, ComplexDataFormat):
                    schema = {}
                    if '$ref' in self.events[eventId].dataFormat['dataObject']:
                        schema['$ref'] = {}
                        schema['$ref'] = self.events[eventId].dataFormat['dataObject']['$ref']
                        schema['type'] = 'object'
                    else:
                        schema['items'] = {}
                        schema['items']['$ref'] = self.events[eventId].dataFormat['dataObject']['items']['$ref']
                        schema['type'] = 'array'
                    schema['definitions'] = self.events[eventId].dataFormat
                    try:
                        jsonschema.validate((self.events[eventId].dataObject), schema, format_checker=(jsonschema.FormatChecker()))
                    except Exception as e:
                        try:
                            logging.error('Error validating event ' + eventId + '. Data object is of type ' + type(self.events[eventId].dataObject))
                            logging.error('Details: ' + e)
                            return
                        finally:
                            e = None
                            del e

        else:
            if not validateSimpleDataformat(eventId, self.events[eventId].df, self.events[eventId].dataObject, self.events[eventId].isArray):
                return
            msg = self.objectToJson(event)
        if self.connected and self.registered:
            try:
                if self.sockJsFraming:
                    _msg = self.objectToJson(msg).replace('\\n', '')
                    self.ws.send('["E ' + _msg[1:-1] + '"]')
                else:
                    self.ws.send('E ' + msg)
                logging.debug('SENDING: ' + msg)
            except Exception:
                logging.exception(self, 'Error, could not send message...')

        else:
            if self.eventCacheEnabled and cached:
                logging.debug('Not connected and/or registered, putting event in cache.')
                if len(self.eventCache) < self.eventCacheSize:
                    self.eventCache.append(msg)
                else:
                    self.eventCache.pop(0)
                    self.eventCache.append(msg)
            else:
                if cached:
                    self.eventCacheEnabled or logging.debug('Global cache disabled, message cache flag overridden and discarded.')
                else:
                    logging.debug('Caching disabled, message discarded.')

    def addConfigParameter(self, key, value, type):
        newParam = getDataType(type)
        newParam['type'] = newParam['type'].upper()
        if 'format' in newParam:
            newParam['format'] = newParam['format'].upper()
        newParam['value'] = value
        self.configuration['parameters'][key] = newParam

    def getConfigParameter(self, key):
        if key in self.configuration['parameters']:
            return self.configuration['parameters'][key]['value']
        return ''

    def changeConfigParameter(self, key, value):
        if key in self.configuration['parameters']:
            self.configuration['parameters'][key]['value'] = value

    def reRegister(self):
        logging.debug('Reregistering after configuration parameter change...')
        if self.sockJsFraming:
            _selfd = json.dumps(self.objectToJson(self.getSelfDescription())).replace('\\n', '')
            self.ws.send('["R ' + _selfd[1:-1] + '"]')
        else:
            self.ws.send('R ' + self.objectToJson(self.getSelfDescription()))

    def objectToJson(self, object):
        return jsonpickle.encode(object, unpicklable=False)

    def getSelfDescription(self):
        self_description = {}
        self_description['@class'] = self.service_type
        self_description['uuid'] = self.uuid
        self_description['name'] = self.name
        self_description['description'] = self.description
        self_description['token'] = self.token
        _ev = []
        e_props = ['@id', 'id', 'dataFormat', 'description', 'eventId', 'name']
        for event in self.events:
            current_e_props = []
            e = jsonpickle.decode(jsonpickle.encode((self.events[event]), unpicklable=False))
            for key in e.keys():
                if key == 'id':
                    e['@id'] = e['id']
                    del e[key]

            del e['priority']
            del e['df']
            if e['dataFormat'] is None:
                del e['dataFormat']
            del e['isArray']
            for key in e.keys():
                current_e_props.append(key)

            for key in current_e_props:
                if key not in e_props:
                    try:
                        del e[key]
                    except:
                        logging.exception(self, 'Key not found: ' + key)

            _ev.append(e)

        self_description['events'] = _ev
        _fu = []
        for function in self.functions:
            f = jsonpickle.decode(jsonpickle.encode((self.functions[function]), unpicklable=False))
            if f['responseEvents'] and len(f['responseEvents']) > 0:
                _re = []
                for idx, re in enumerate(f['responseEvents']):
                    _re.append(self.events[re].id)

                f['responseEvents'] = _re
            else:
                del f['responseEvents']
            del f['isArray']
            del f['implementation']
            if f['dataFormat'] is None:
                del f['dataFormat']
            _fu.append(f)

        self_description['functions'] = _fu
        self_description['configuration'] = self.configuration
        return self_description

    def readConfig(self):
        logging.info('Reading configuration from application.properties file')
        config = open('application.properties', 'r')
        for line in config:
            configparam = line.split('=')
            if configparam[0] == 'msb.type':
                self.service_type = configparam[1].rstrip()
            elif configparam[0] == 'msb.name':
                self.name = configparam[1].rstrip()
            elif configparam[0] == 'msb.uuid':
                self.uuid = configparam[1].rstrip()
            elif configparam[0] == 'msb.token':
                self.token = configparam[1].rstrip()
            elif configparam[0] == 'msb.url':
                self.msb_url = configparam[1].rstrip()
            elif configparam[0] == 'msb.description':
                self.description = configparam[1].rstrip()


def getConfigParamDataType(dt):
    try:
        return str(getDataType(dt)['type']).upper()
    except:
        logging.exception('Unknown dataType: ' + str(format))
        return 'UNKNOWN_DATATYPE'


def vadilateEventDataFormat(df):
    if df is None:
        return True
    schema_file = os.path.join(os.path.dirname(__file__), 'event_schema.json')
    schema = json.loads(open(schema_file).read())
    do = {'definitions': json.loads(jsonpickle.encode(df))}
    try:
        jsonschema.Draft4Validator(schema).validate(do)
    except Exception as e:
        try:
            logging.exception(e)
            return False
        finally:
            e = None
            del e

    return True


def vadilateFunctionDataFormat(df):
    if df is None:
        return True
    schema_file = os.path.join(os.path.dirname(__file__), 'function_schema.json')
    schema = json.loads(open(schema_file).read())
    do = {'definitions': json.loads(jsonpickle.encode(df))}
    try:
        jsonschema.Draft4Validator(schema).validate(do)
    except Exception as e:
        try:
            logging.exception(e)
            return False
        finally:
            e = None
            del e

    return True


def validateSimpleDataformat(eventId, df, val, isArray):
    if isArray:
        try:
            if all((type(item) == df for item in val)):
                return True
            logging.error('Error validating event ' + eventId + ': ' + "Value in list doesn't fit the required data format: " + str(val) + ' = ' + str(type(val)) + ', expected: ' + str(df))
            return False
        except:
            logging.error('Error validating event ' + eventId + '. DataObject (' + str(val) + ') is not an array as defined.')
            return False

    else:
        if type(val) == df:
            return True
    logging.error('Error validating event ' + eventId + ': ' + "Value doesn't fit the required data format: " + str(val) + ' = ' + str(type(val)) + ', expected: ' + str(df))
    return False
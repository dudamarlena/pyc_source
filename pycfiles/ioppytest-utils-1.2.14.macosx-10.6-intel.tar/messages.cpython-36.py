# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/messages.py
# Compiled at: 2018-12-04 09:53:59
# Size of source mod 2**32: 91053 bytes
"""

About the library:
-----------------

This module provides the API message formats used by ioppytest test framework.

The idea is to be able to have an
- organized and centralized way of dealing with the big amount of messages formats used in the platform;
- to be able to import (or just copy/paste) these messages for interacting with components on the event bus ,
- re-use this also for the interactinggration testing;
- to have version control the messages e.g. messages_testcase_start API v1 and API v2;
- to have a direct way of exporting this as doc.

Some conventions:
---------------------
- if event is a service request then the routing key (r_key) is someRpcExecutionEvent.request
- a reply to a service will be on topic/r_key : someRpcExecutionEvent.reply
- reply.correlation_id = request.correlation_id

Usage:
------
>>> m = MsgTestCaseSkip(testcase_id = 'some_testcase_id')
>>> m
MsgTestCaseSkip(_api_version = 1.2.14, description = Skip testcase, node = someNode, testcase_id = some_testcase_id, )
>>> m.routing_key
'testsuite.testcase.skip'
>>> m.message_id # doctest: +SKIP
'802012eb-24e3-45c4-9dcc-dc293c584f63'
>>> m.testcase_id
'some_testcase_id'

# also we can modify some of the fields (rewrite the default ones)
>>> m = MsgTestCaseSkip(testcase_id = 'TD_COAP_CORE_03')
>>> m
MsgTestCaseSkip(_api_version = 1.2.14, description = Skip testcase, node = someNode, testcase_id = TD_COAP_CORE_03, )
>>> m.testcase_id
'TD_COAP_CORE_03'

# and even export the message in json format (for example for sending the message though the amqp event bus)
>>> m.to_json()
'{"_api_version": "1.2.14", "description": "Skip testcase", "node": "someNode", "testcase_id": "TD_COAP_CORE_03"}'

# We can use the Message class to import json into Message objects:
>>> m=MsgTestSuiteStart()
>>> m.routing_key
'testsuite.start'
>>> m.to_json()
'{"_api_version": "1.2.14", "description": "Test suite START command"}'
>>> json_message = m.to_json()
>>> obj=Message.load(json_message,'testsuite.start', None )
>>> obj
MsgTestSuiteStart(_api_version = 1.2.14, description = Test suite START command, )
>>> type(obj) # doctest: +SKIP
<class 'messages.MsgTestSuiteStart'>

# We can use the library for generating error responses:
# the request:
>>> m = MsgSniffingStart()
>>>

# the error reply (note that we pass the message of the request to build the reply):
>>> err = MsgErrorReply(m)
>>> err
MsgErrorReply(_api_version = 1.2.14, error_code = None, error_message = None, ok = False, )

# properties of the message are auto-generated:
>>> m.reply_to
'sniffing.start.reply'
>>> err.routing_key
'sniffing.start.reply'
>>> m.correlation_id # doctest: +SKIP
'360b0f67-4455-43e3-a00f-eca91f2e84da'
>>> err.correlation_id # doctest: +SKIP
'360b0f67-4455-43e3-a00f-eca91f2e84da'

# we can get all the AMQP properties also as a dict:
>>> err.get_properties() # doctest: +SKIP
'{'timestamp': 1515172549, 'correlation_id': '16257581-06be-4088-a1f6-5672cc73d8f2', 'message_id': '1ec12c2b-33c7-44ad-97b8-5099c4d52e81', 'content_type': 'application/json'}'

"""
from collections import OrderedDict
import logging, time, json, uuid
logger = logging.getLogger(__name__)
API_VERSION = '1.2.14'

class NonCompliantMessageFormatError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Message(object):

    def __init__(self, **kwargs):
        global API_VERSION
        try:
            self._msg_data = {k:v for k, v in self._msg_data_template.items()}
        except AttributeError:
            self._msg_data = {}
            self._msg_data_template = {}

        self._properties = dict(content_type='application/json',
          message_id=(str(uuid.uuid4())),
          timestamp=(int(time.time())))
        try:
            if self.routing_key.endswith('.request'):
                self._properties['reply_to'] = self.routing_key.replace('.request', '.reply')
                self._properties['correlation_id'] = self._properties['message_id']
        except AttributeError:
            pass

        self._msg_data.update(kwargs)
        if '_api_version' not in self._msg_data:
            self._msg_data['_api_version'] = API_VERSION
        for key in self._msg_data:
            setattr(self, key, self._msg_data[key])

        for key in self._properties:
            setattr(self, key, self._properties[key])

    def to_dict(self):
        resp = {}
        for field in sorted(self._msg_data.keys()):
            resp[field] = getattr(self, field)

        return resp

    def to_odict(self):
        resp = {}
        for field in sorted(self._msg_data.keys()):
            resp[field] = getattr(self, field)

        return OrderedDict(sorted((resp.items()), key=(lambda t: t[0])))

    def to_json(self):
        return json.dumps(self.to_odict())

    def get_properties(self):
        resp = dict()
        for field in self._properties:
            resp[field] = getattr(self, field)

        return resp

    def __str__(self):
        s = ' - ' * 20 + '\n'
        s += 'Message routing key: %s' % self.routing_key
        s += '\n -  -  - \n'
        s += 'Message properties: %s' % json.dumps((self.get_properties()), indent=4)
        s += '\n -  -  - \n'
        s += 'Message body: %s' % json.dumps((self.to_odict()), indent=4)
        s += '\n' + ' - ' * 20
        return s

    def update_properties(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def load(cls, json_body, routing_key, properties=None):
        """
        Builds a python object representation of the AMQP message based on the ones defined by the event bus API.

        :param json_body: json description of message's body (amqp payload)
        :param routing_key: Maps to the right Message builder, passed argument cannot contain special char like * or #
        :param properties: Used for building more complete complex representation (e.g. for reply_to corre_id params)
        :return: The python Message object or subclass (e.g. MsgPacketSniffedRaw)

        about r_key matching mechanism:
            fromAgent.coap_client.packet.raw -> matches fromAgent.*.packet.raw -> returns MsgPacketSniffedRaw

        # We can use the Message class to build Message objects from json + rkey:
        >>> m=MsgSniffingGetCapture()
        >>> m.routing_key
        'sniffing.getcapture.request'
        >>> m.to_json()
        '{"_api_version": "1.2.14", "capture_id": "TD_COAP_CORE_01"}'
        >>> json_message = m.to_json()
        >>> json_message
        '{"_api_version": "1.2.14", "capture_id": "TD_COAP_CORE_01"}'
        >>> obj=Message.load(json_message,'testsuite.start', None )
        >>> type(obj) # doctest
        <class 'messages.MsgTestSuiteStart'>

        """
        global rk_pattern_to_message_type_map
        if not type(json_body) is str:
            raise AssertionError
        else:
            assert type(routing_key) is str
            props_dict = {}
            try:
                message_type = rk_pattern_to_message_type_map.get_message_type(routing_key)
            except KeyError as e:
                raise NonCompliantMessageFormatError('Routing key pattern not recogized for RKEY=%s' % routing_key)

        default_values_dict = message_type().to_dict()
        payload_dict = dict.fromkeys(default_values_dict.keys(), None)
        payload_dict.update(json.loads(json_body))
        built_message = message_type(**payload_dict)
        if properties is None:
            pass
        else:
            if type(properties) is dict:
                props_dict.update(properties)
            else:
                raise NotImplementedError('Incompatible properties input or not yet supported')
            if properties:
                (built_message.update_properties)(**props_dict)
            built_message.routing_key = routing_key
            return built_message

    @classmethod
    def load_from_pika(cls, method, props, body):
        """
        Builds a python object representation of the AMQP message based on the ones defined by the event bus API.
        Takes as arguments pika objects method, properties and body returned by channel.basic_consume method
        """
        props_dict = {'content_type':props.content_type, 
         'delivery_mode':props.delivery_mode, 
         'correlation_id':props.correlation_id, 
         'reply_to':props.reply_to, 
         'message_id':props.message_id, 
         'timestamp':props.timestamp, 
         'user_id':props.user_id, 
         'app_id':props.app_id}
        routing_key = method.routing_key
        json_body = body.decode('utf-8')
        return Message.load(json_body, routing_key, props_dict)

    @classmethod
    def from_json(cls, body):
        """
        :param body: json string or string encoded as utf-8
        :return:  Message object generated from the body
        :raises NonCompliantMessageFormatError: If the message cannot be build from the provided json
        """
        raise DeprecationWarning()

    @classmethod
    def from_dict(cls, message_dict):
        """
        :param body: dict
        :return:  Message object generated from the body
        :raises NonCompliantMessageFormatError: If the message cannot be build from the provided json
        """
        raise DeprecationWarning()

    def __repr__(self):
        ret = '%s(' % self.__class__.__name__
        for key, value in self.to_odict().items():
            ret += '%s = %s, ' % (key, value)

        ret += ')'
        return ret


class RoutingKeyToMessageMap:
    __doc__ = '\n    Special dict to map routing keys to messages of Message type.\n    Lookup is slow but it\'s due to the fact of using WILDCARDs (no hash mechanism can be used :/ )\n\n    example of use:\n        >>> r_map=RoutingKeyToMessageMap({\'fromAgent.*.packet.raw\':MsgPacketSniffedRaw })\n        >>> r_map\n        {\'fromAgent.*.packet.raw\': <class \'messages.MsgPacketSniffedRaw\'>}\n        >>> r_map.get_message_type(\'fromAgent.agent1.packet.raw\')\n        <class \'messages.MsgPacketSniffedRaw\'>\n        >>> r_map.get_message_type(\'blabla.agent1.packet.raw\') #IGNORE_EXCEPTION_DETAIL\n        Traceback (most recent call last):\n          File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/doctest.py", line 1320, in __run\n            compileflags, 1), test.globs)\n          File "<doctest __main__.RoutingKeyToMessageMap[3]>", line 1, in <module>\n            r_map.get_message_type(\'blabla.agent1.packet.raw\') #IGNORE_EXCEPTION_DETAIL\n          File "/Users/fsismondi/dev/f-interop-utils/messages.py", line 355, in get_message_type\n            "Routing Key pattern not found in mapping rkey patterns -> messages table, RKEY: %s" %routing_key)\n        KeyError: \'Routing Key pattern not found in mapping rkey patterns -> messages table, RKEY: blabla.agent1.packet.raw\'\n        >>>\n\n    '
    WILDCARDS = ('*', '#')
    TERM_SEPARATOR = '.'

    def __init__(self, rkey_to_message_dict):
        self.rkey_to_message_dict = rkey_to_message_dict

    def __repr__(self):
        return repr(self.rkey_to_message_dict)

    def get_message_type(self, routing_key):
        for key in self.rkey_to_message_dict.keys():
            if self.equals(key, routing_key):
                return self.rkey_to_message_dict[key]

        raise KeyError('Routing Key pattern not found in mapping rkey patterns -> messages table, RKEY: %s' % routing_key)

    @classmethod
    def equals(cls, r1, r2):

        def equal_terms(term_1, term_2):
            if term_1 == '*' or term_2 == '*':
                return True
            else:
                return term_1 == term_2

        complex_matching = False
        for wc in cls.WILDCARDS:
            if wc in r1 or wc in r2:
                complex_matching = True
                break

        if '#' in r1 or '#' in r2:
            raise NotImplementedError('Wildcard # still not supported in matching mechanism')
        if not complex_matching:
            return r1 == r2
        else:
            if len(r1.split(cls.TERM_SEPARATOR)) != len(r2.split(cls.TERM_SEPARATOR)):
                return False
            for term1, term2 in zip(r1.split(cls.TERM_SEPARATOR), r2.split(cls.TERM_SEPARATOR)):
                if not equal_terms(term1, term2):
                    return False
                    continue

            return True


class MsgReply(Message):
    __doc__ = '\n    Auxiliary class which creates replies messages with fields based on the request.\n    Routing key, corr_id are generated based on the request message\n    When not passing request_message as argument\n    '

    def __init__(self, request_message=None, **kwargs):
        if request_message:
            if hasattr(request_message, 'routing_key'):
                if request_message.routing_key.endswith('.request'):
                    self.routing_key = request_message.routing_key.replace('.request', '.reply')
                if not hasattr(self, '_msg_data_template'):
                    self._msg_data_template = {'ok': True}
                else:
                    if 'ok' not in self._msg_data_template:
                        self._msg_data_template.update({'ok': True})
                (super(MsgReply, self).__init__)(**kwargs)
                self._properties['correlation_id'] = request_message.correlation_id
                self.correlation_id = request_message.correlation_id
        else:
            (super(MsgReply, self).__init__)(**kwargs)
            logger.info('[messages] lazy message reply generated. Do not expect correlation between request and reply amqpproperties  %s' % repr(self)[:70])

    def correlate_to(self, request_message):
        """
        add to reply message the right correlation information to request
        """
        self._properties['correlation_id'] = request_message.correlation_id
        self.correlation_id = request_message.correlation_id


class MsgErrorReply(MsgReply):
    __doc__ = '\n    see section "F-Interop conventions" on top\n    '

    def __init__(self, request_message, **kwargs):
        assert request_message
        (super(MsgErrorReply, self).__init__)(request_message, **kwargs)

    _msg_data_template = {'ok':False, 
     'error_message':None, 
     'error_code':None}


class MsgOrchestratorVersionReq(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for returning current version of SO\n    '
    routing_key = 'orchestrator.version.request'
    _msg_data_template = {}


class MsgOrchestratorUsersList(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for returning user list of SO\n    '
    routing_key = 'orchestrator.users.list.request'
    _msg_data_template = {}


class MsgOrchestratorUserAdd(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for adding a user to SO\n    '
    routing_key = 'orchestrator.users.add.request'
    _msg_data_template = {}


class MsgOrchestratorUserDelete(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for deleting a user from SO\n    '
    routing_key = 'orchestrator.users.delete.request'
    _msg_data_template = {}


class MsgOrchestratorUserGet(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for getting a user from SO\n    '
    routing_key = 'orchestrator.users.get.request'
    _msg_data_template = {}


class MsgOrchestratorSessionsList(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for listing sessions from SO\n    '
    routing_key = 'orchestrator.sessions.list.request'
    _msg_data_template = {}


class MsgOrchestratorSessionsGet(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for getting a session from SO\n    '
    routing_key = 'orchestrator.sessions.get.request'
    _msg_data_template = {}


class MsgOrchestratorSessionsAdd(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for adding a session to SO\n    '
    routing_key = 'orchestrator.sessions.add.request'
    _msg_data_template = {}


class MsgOrchestratorSessionsDelete(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for deleting a session to SO\n    '
    routing_key = 'orchestrator.sessions.delete.request'
    _msg_data_template = {}


class MsgOrchestratorSessionsUpdate(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for updating a session from SO\n    '
    routing_key = 'orchestrator.sessions.update.request'
    _msg_data_template = {}


class MsgOrchestratorTestsGet(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for getting tests from SO\n    '
    routing_key = 'orchestrator.tests.get.request'
    _msg_data_template = {}


class MsgOrchestratorTestsGetContributorName(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> SO\n\n    Description: Message for getting tests from SO with contributor and name\n    '
    routing_key = 'orchestrator.tests.get_contributor_name.request'
    _msg_data_template = {}


class MsgUiReply(MsgReply):
    routing_key = 'ui.user.all.reply'
    _msg_data_template = {'fields': []}


class MsgUiDisplay(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message to display in user interface\n    '
    routing_key = 'ui.user.all.display'
    _msg_data_template = {'level':None, 
     'tags':{},  'fields':[
      {'type':'p', 
       'value':'Hello World!'}]}


class MsgUiRequest(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for requesting action or information to user\n    '
    routing_key = 'ui.user.all.request'
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'input_name', 
       'type':'text'}]}


class MsgUiRequestSessionConfiguration(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for requesting session information to UI\n    '
    routing_key = 'ui.core.session.get.request'
    _msg_data_template = {}


class MsgUiSessionConfigurationReply(MsgUiReply):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: UI -> TT\n\n    Description: Message for requesting session information to UI\n    '
    routing_key = 'ui.core.session.get.reply'
    _msg_data_template = {'amqp_url':'amqp://WX9D3L5A:5S68CRDC@mq.dev.f-interop.eu:443/277704a1-03c0-467c-b00d-c984976692d7', 
     'logs':[
      {'date':'2018-05-07T12:50:47.224000+00:00', 
       'message':'Session created locally', 
       'type':'info'}], 
     'resources':[{}],  'shared':True, 
     'slice_id':'urn:publicid:IDN+finterop:project1+slice+testing', 
     'start_date':'2018-05-07T12:50:48.128000+00:00', 
     'status':'open', 
     'testSuite':'http://orchestrator.dev.f-interop.eu:8181/tests/f-interop/dummy-tool-shared', 
     'testSuiteType':'interoperability', 
     'users':[
      'federico_sismondiojxu',
      'myslice',
      'federicosismondiparu']}


class MsgUiRequestQuestionRadio(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for radio request on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'some_info', 
       'type':'radio', 
       'label':'choice number 1', 
       'value':True},
      {'name':'some_info', 
       'type':'radio', 
       'label':'choice number 2', 
       'value':False}]}


class MsgUiRequestQuestionCheckbox(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for checkbox request on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'Choice1', 
       'label':'Choice1', 
       'type':'checkbox', 
       'value':0},
      {'name':'Choice2', 
       'label':'Choice2', 
       'type':'checkbox', 
       'value':1}]}


class MsgUiRequestQuestionSelect(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for select request on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'ideal_select', 
       'type':'select', 
       'options':[
        {'label':'choice 1', 
         'value':1},
        {'label':'choice 2', 
         'value':2},
        {'label':'choice 3', 
         'value':3}], 
       'value':1}]}


class MsgUiSendFileToDownload(MsgUiDisplay):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for file download on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'some_test_pcap_file.pcap', 
       'type':'data', 
       'value':None}]}


class MsgUiRequestUploadFile(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for file upload request on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'upload a file', 
       'type':'file'}]}


class MsgUiRequestTextInput(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for requesting a text input on UI\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'input_name', 
       'type':'text'}]}


class MsgUiRequestConfirmationButton(MsgUiRequest):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for requesting confirmation button\n    '
    _msg_data_template = {'tags':{},  'fields':[
      {'name':'test_button', 
       'type':'button', 
       'value':True}]}


class MsgUiDisplayMarkdownText(MsgUiDisplay):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for displaying Markdown text to user interface\n    '
    _msg_data_template = {'level':None, 
     'tags':{},  'fields':[
      {'type':'p', 
       'value':'Hello World!'}]}


class MsgUiDisplayIFrame(Message):
    __doc__ = '\n    Requirements: ...\n\n    Type: Event\n\n    Pub/Sub: TT -> UI\n\n    Description: Message for displaying iframing GUI and external server\n    '
    routing_key = 'ui.user.all.display'
    _msg_data_template = {'level':None, 
     'tags':{},  'fields':[
      {'type':'iframe', 
       'name':'my_iframe', 
       'value':'https://www.w3schools.com'}]}


class MsgAgentTunStart(Message):
    __doc__ = '\n    Requirements: Testing Tool MAY implement (if IP tun needed)\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Agent\n\n    Description: Message for triggering start IP tun interface in OS where the agent is running\n    '
    routing_key = 'toAgent.*.ip.tun.start'
    _msg_data_template = {'name':'agent_TT', 
     'ipv6_prefix':'bbbb', 
     'ipv6_host':':3', 
     'ipv6_no_forwarding':False, 
     'ipv4_host':None, 
     'ipv4_network':None, 
     'ipv4_netmask':None, 
     're_route_packets_if':None, 
     're_route_packets_prefix':None, 
     're_route_packets_host':None}


class MsgAgentTunStarted(Message):
    __doc__ = '\n    Requirements: Message for indicating that agent tun has been started\n\n    Type: Event\n\n    Pub/Sub: Agent -> Testing Tool\n\n    Description: TBD\n    '
    routing_key = 'fromAgent.*.ip.tun.started'
    _msg_data_template = {'name':'agent_TT', 
     'ipv6_prefix':'bbbb', 
     'ipv6_host':':3', 
     'ipv4_host':None, 
     'ipv4_network':None, 
     'ipv4_netmask':None, 
     'ipv6_no_forwarding':False, 
     're_route_packets_if':None, 
     're_route_packets_prefix':None, 
     're_route_packets_host':None}


class MsgAgentSerialStart(Message):
    __doc__ = '\n    Requirements: Testing Tool MAY implement (if serial interface is needed for the test)\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Agent\n\n    Description: Message for triggering start of serial interface , which communicates with probe 802.15.4\n    '
    routing_key = 'toAgent.*.802154.serial.start'
    _msg_data_template = {'name':None, 
     'port':None, 
     'boudrate':None}


class MsgAgentSerialStarted(Message):
    __doc__ = '\n    Requirements: TBD\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Agent\n\n    Description: Message for indicating that agent serial interface has been started\n    '
    routing_key = 'fromAgent.*.802154.serial.started'
    _msg_data_template = {'name':None, 
     'port':None, 
     'boudrate':None}


class MsgPacketInjectRaw(Message):
    __doc__ = '\n    Requirements: Message to be captured by the agent an push into the correct embedded interface (e.g. tun, serial, etc..)\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Agent\n\n    Description: TBD\n    '
    routing_key = 'toAgent.*.ip.tun.packet.raw'
    _msg_data_template = {'timestamp':1488586183.45, 
     'interface_name':'tun0', 
     'data':[
      96, 0, 0, 0, 0, 36, 0, 1, 254, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 255, 2, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 22, 58, 0, 5, 2, 0, 0, 1, 0, 143, 0, 112, 7, 0, 0, 0, 1, 4, 0, 0, 0, 255, 2, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]}


class MsgPacketSniffedRaw(Message):
    __doc__ = '\n    Description: Message captured by the agent in one of its embedded interfaces (e.g. tun, serial, etc..)\n\n    Type: Event\n\n    Pub/Sub: Agent -> Testing Tool\n\n    Description: TBD\n    '
    routing_key = 'fromAgent.*.ip.tun.packet.raw'
    _msg_data_template = {'timestamp':1488586183.45, 
     'interface_name':'tun0', 
     'data':[
      96, 0, 0, 0, 0, 36, 0, 1, 254, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 255, 2, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 22, 58, 0, 5, 2, 0, 0, 1, 0, 143, 0, 112, 7, 0, 0, 0, 1, 4, 0, 0, 0, 255, 2, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]}


class MsgTestingToolTerminate(Message):
    __doc__ = "\n    Requirements: TT SHOULD listen to event, and handle a gracefully termination of all it's processes\n\n    Type: Event\n\n    Pub/Sub: GUI, (or Orchestrator) -> Testing Tool\n\n    Description: Testing tool should stop all it's processes gracefully.\n    "
    routing_key = 'testingtool.terminate'
    _msg_data_template = {'description': 'Command TERMINATE testing tool execution'}


class MsgTestingToolReady(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event as soon as TT is up and listening on the event bus\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: Used to indicate to the GUI that testing is ready to start the test suite\n    '
    routing_key = 'testingtool.ready'
    _msg_data_template = {'description': 'Testing tool READY to start test suite.'}


class MsgTestingToolComponentReady(Message):
    __doc__ = "\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Event\n\n    Pub/Sub: Any Testing tool's component -> Test Coordinator\n\n    Description: Once a testing tool's component is ready, it should publish a compoennt ready message\n    "
    routing_key = 'testingtool.component.ready'
    _msg_data_template = {'component':'SomeComponent', 
     'description':'Component READY to start test suite.'}


class MsgSessionChat(Message):
    __doc__ = '\n    Requirements: GUI should implement\n\n    Type: Event\n\n    Pub/Sub: UI 1 (2) -> UI 2 (1)\n\n    Description: Generic descriptor of chat messages\n    '
    routing_key = 'chat'
    _msg_data_template = {'user_name':'Ringo', 
     'node':'unknown', 
     'description':"I've got blisters on my fingers!"}


class MsgSessionLog(Message):
    __doc__ = "\n    Requirements: Testing Tool SHOULD implement\n\n    Type: Event\n\n    Pub/Sub: Any Testing tool's component -> user/devs interfaces\n\n    Description: Generic descriptor of log messages\n    "
    routing_key = 'log.*.*'
    _msg_data_template = {'component':'misc', 
     'message':"I've got blisters on my fingers!"}


class MsgSessionConfiguration(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event, and configure accordingly\n\n    Type: Event\n\n    Pub/Sub: Orchestrator -> Testing Tool\n\n    Description: TT SHOULD listen to this message and configure the testsuite correspondingly\n    '
    routing_key = 'session.configuration'
    _msg_data_template = {'session_id':'666', 
     'configuration':{'testsuite.testcases': [
                              'someTestCaseId1',
                              'someTestCaseId2']}, 
     'testing_tools':'f-interop/someTestToolId', 
     'users':[
      'u1',
      'f-interop']}


class MsgTestingToolConfigured(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event once session.configuration message has been processed.\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Orchestrator, GUI\n\n    Description: The goal is to notify orchestrator and other components that the testing tool has been configured\n    '
    routing_key = 'testingtool.configured'
    _msg_data_template = {'description':'Testing tool CONFIGURED', 
     'session_id':None, 
     'testing_tools':'f-interop/interoperability-coap'}


class MsgSessionCreated(Message):
    __doc__ = '\n    Requirements: Session Orchestrator MUST publish message on common-services channel (on every session creation)\n\n    Type: Event\n\n    Pub/Sub: SO -> viz tools\n\n    Description: The goal is to notify viz tools about new sessions\n    '
    routing_key = 'orchestrator.session.created'
    _msg_data_template = {'description':'A new session has been created', 
     'session_id':None, 
     'testing_tools':None}


class MsgAutomatedIutTestPing(Message):
    __doc__ = "\n    Requirements: Automated IUTs SHOULD implement (other components should not subscribe to event)\n\n    Type: Event\n\n    Pub/Sub: Any Testing tool's component -> automated IUT\n\n    Description: tbd\n    "
    routing_key = 'testingtool.component.test.ping.request'
    _msg_data_template = {'description':'Automated IUT ping request', 
     'node':None, 
     'target_address':None}


class MsgAutomatedIutTestPingReply(MsgReply):
    __doc__ = "\n    Requirements: Automated IUTs SHOULD implement (other components should not subscribe to event)\n\n    Type: Event\n\n    Pub/Sub: automated IUT -> any Testing tool's component\n\n    Description: tbd\n    "
    routing_key = 'testingtool.component.test.ping.reply'
    _msg_data_template = {'description':'Automated IUT reply to executed ping request', 
     'node':None, 
     'target_address':None}


class MsgTestingToolComponentShutdown(Message):
    __doc__ = "\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Event\n\n    Pub/Sub: Any Testing tool's component -> Test Coordinator\n\n    Description: tbd\n    "
    routing_key = 'testingtool.component.shutdown'
    _msg_data_template = {'component':'SomeComponent', 
     'description':'Component SHUTDOWN. Bye!'}


class MsgTestSuiteStart(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event and start the test suite right after reception. MsgTestSuiteStarted\n\n    Type: Event\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description: tbd\n    '
    routing_key = 'testsuite.start'
    _msg_data_template = {'description': 'Test suite START command'}


class MsgTestSuiteStarted(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD publish to event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: tbd\n    '
    routing_key = 'testsuite.started'
    _msg_data_template = {'description': 'Test suite STARTED'}


class MsgTestSuiteFinish(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description: tbd\n    '
    routing_key = 'testsuite.finish'
    _msg_data_template = {'description': 'Test suite FINISH command'}


class MsgTestCaseReady(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description:\n        - Used to indicate to the GUI (or automated-iut) which is the next test case to be executed.\n        - This message is normally followed by a MsgTestCaseStart (from GUI-> Testing Tool)\n    '
    routing_key = 'testsuite.testcase.ready'
    _msg_data_template = {'description':'Test case ready to start', 
     'testcase_id':'TD_COAP_CORE_01', 
     'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_01', 
     'objective':'Perform GET transaction(CON mode)', 
     'state':None}


class MsgTestCaseStart(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description:\n        - Message used for indicating the testing tool to start the test case (the one previously selected)\n        - if testcase_id is Null then testing tool starts previously announced testcase in message\n        "testcoordination.testcase.ready",\n    '
    routing_key = 'testsuite.testcase.start'
    _msg_data_template = {'description':'Test case START command', 
     'testcase_id':None}


class MsgTestCaseStarted(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description:\n        - Message used for indicating that testcase has started\n    '
    routing_key = 'testsuite.testcase.started'
    _msg_data_template = {'description':'Test case STARTED', 
     'testcase_id':None}


class MsgTestCaseConfiguration(Message):
    __doc__ = '\n    Requirements: Testing Tool MAY publish event (if needed for executing the test case)\n    Type: Event\n    Pub/Sub: Testing Tool -> GUI & automated-iut\n    Description:\n        - Message used to indicate GUI and/or automated-iut which configuration to use.\n        - IMPORTANT: deprecate this message in favor of MsgConfigurationExecute and MsgConfigurationExecuted\n    '
    routing_key = 'testsuite.testcase.configuration'
    _msg_data_template = {'configuration_id':'COAP_CFG_01', 
     'node':'coap_server', 
     'testcase_id':None, 
     'testcase_ref':None, 
     'description':[
      'CoAP servers running service at [bbbb::2]:5683',
      'CoAP servers are requested to offer the following resources',
      [
       '/test', 'Default test resource', 'Should not exceed 64bytes'],
      [
       '/seg1/seg2/seg3', 'Long path ressource', 'Should not exceed 64bytes'],
      [
       '/query', 'Ressource accepting query parameters', 'Should not exceed 64bytes'],
      [
       '/separate',
       'Ressource which cannot be served immediately and which cannot be acknowledged in a piggy-backed way',
       'Should not exceed 64bytes'],
      [
       '/large', 'Large resource (>1024 bytes)', 'shall not exceed 2048bytes'],
      [
       '/large_update',
       'Large resource that can be updated using PUT method (>1024 bytes)',
       'shall not exceed 2048bytes'],
      [
       '/large_create',
       'Large resource that can be  created using POST method (>1024 bytes)',
       'shall not exceed 2048bytes'],
      [
       '/obs', 'Observable resource which changes every 5 seconds',
       'shall not exceed 2048bytes'],
      [
       '/.well-known/core', 'CoRE Link Format', 'may require usage of Block options']]}


class MsgConfigurationExecute(Message):
    __doc__ = '\n    Requirements: Testing Tool MAY publish event (if needed for executing the test case)\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI & automated-iut\n\n    Description:\n        - Message used to indicate GUI and/or automated-iut which configuration to use.\n    '
    routing_key = 'testsuite.testcase.configuration.execute'
    _msg_data_template = {'configuration_id':'COAP_CFG_01', 
     'node':'coap_server', 
     'testcase_id':None, 
     'testcase_ref':None, 
     'description':[
      'CoAP servers running service at [bbbb::2]:5683',
      'CoAP servers are requested to offer the following resources',
      [
       '/test', 'Default test resource', 'Should not exceed 64bytes'],
      [
       '/seg1/seg2/seg3', 'Long path ressource', 'Should not exceed 64bytes'],
      [
       '/query', 'Ressource accepting query parameters', 'Should not exceed 64bytes'],
      [
       '/separate',
       'Ressource which cannot be served immediately and which cannot be acknowledged in a piggy-backed way',
       'Should not exceed 64bytes'],
      [
       '/large', 'Large resource (>1024 bytes)', 'shall not exceed 2048bytes'],
      [
       '/large_update',
       'Large resource that can be updated using PUT method (>1024 bytes)',
       'shall not exceed 2048bytes'],
      [
       '/large_create',
       'Large resource that can be  created using POST method (>1024 bytes)',
       'shall not exceed 2048bytes'],
      [
       '/obs', 'Observable resource which changes every 5 seconds',
       'shall not exceed 2048bytes'],
      [
       '/.well-known/core', 'CoRE Link Format', 'may require usage of Block options']]}


class MsgConfigurationExecuted(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (automated-IUT) -> Testing Tool\n\n    Description:\n        - Message used for indicating that the IUT has been configured as requested\n        - pixit SHOULD be included in this message (pixit = Protocol Implementaiton eXtra Information for Testing)\n    '
    routing_key = 'testsuite.testcase.configuration.executed'
    _msg_data_template = {'description':'IUT has been configured', 
     'node':'coap_server', 
     'ipv6_address':None}


class MsgTestCaseStop(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI & automated-iut -> Testing Tool\n\n    Description:\n        - Message used for indicating the testing tool to stop the test case (the one running).\n    '
    routing_key = 'testsuite.testcase.stop'
    _msg_data_template = {'description': 'Event test case STOP'}


class MsgTestCaseRestart(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description: Restart the running test cases.\n    '
    routing_key = 'testsuite.testcase.restart'
    _msg_data_template = {'description': 'Test case RESTART command'}


class MsgStepStimuliExecute(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description:\n        - Used to indicate to the GUI (or automated-iut) which is the stimuli step to be executed by the user (or\n        automated-IUT).\n    '
    routing_key = 'testsuite.testcase.step.stimuli.execute'
    _msg_data_template = {'description':'Please execute TD_COAP_CORE_01_step_01', 
     'step_id':'TD_COAP_CORE_01_step_01', 
     'step_type':'stimuli', 
     'step_info':[
      'Client is requested to send a GET request with',
      'Type = 0(CON)',
      'Code = 1(GET)'], 
     'step_state':'executing', 
     'node':'coap_client', 
     'node_execution_mode':'user_assisted', 
     'testcase_id':None, 
     'testcase_ref':None, 
     'target_address':None}


class MsgStepStimuliExecuted(Message):
    __doc__ = "\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description:\n        - Used to indicate stimuli has been executed by user (and it's user-assisted iut) or by automated-iut\n    "
    routing_key = 'testsuite.testcase.step.stimuli.executed'
    _msg_data_template = {'description':'Step (stimuli) EXECUTED', 
     'node':'coap_client', 
     'node_execution_mode':'user_assisted'}


class MsgStepCheckExecute(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> Analysis\n\n    Description:\n        - Used to indicate to the GUI (or automated-iut) which is the stimuli step to be executed by the user (or\n        automated-IUT).\n    '
    routing_key = 'testsuite.testcase.step.check.execute'
    _msg_data_template = {'description':'Please execute TD_COAP_CORE_01_step_02', 
     'step_id':'TD_COAP_CORE_01_step_02', 
     'step_type':'check', 
     'step_info':[
      'The request sent by the client contains',
      'Type=0 and Code=1,Client-generated Message ID (➔ CMID)',
      'Client-generated Token (➔ CTOK)',
      'UTEST Uri-Path option test'], 
     'step_state':'executing', 
     'testcase_id':None, 
     'testcase_ref':None}


class MsgStepCheckExecuted(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement\n\n    Type: Event\n\n    Pub/Sub: test coordination -> test analysis\n\n    Description:\n        - In the context of IUT to IUT test execution, this message is used for indicating that the previously\n        executed\n        messages (stimuli message and its reply) CHECK or comply to what is described in the Test Description.\n        - Not used in CoAP testing Tool (analysis of traces is done post mortem)\n    '
    routing_key = 'testsuite.testcase.step.check.executed'
    _msg_data_template = {'partial_verdict':'pass', 
     'description':'TAT says: step complies (checks) with specification'}


class MsgStepVerifyExecute(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI (or automated-IUT)\n\n    Description:\n        - Used to indicate to the GUI (or automated-iut) which is the verify step to be executed by the user (or\n        automated-IUT).\n    '
    routing_key = 'testsuite.testcase.step.verify.execute'
    _msg_data_template = {'response_type':'bool', 
     'description':'Please execute TD_COAP_CORE_01_step_04', 
     'step_id':'TD_COAP_CORE_01_step_04', 
     'step_type':'verify', 
     'step_info':[
      'Client displays the received information'], 
     'node':'coap_client', 
     'node_execution_mode':'user_assisted', 
     'step_state':'executing', 
     'testcase_id':None, 
     'testcase_ref':None}


class MsgStepVerifyExecuted(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description:\n        - Message generated by user (GUI or automated-IUT) declaring if the IUT VERIFY verifies the expected behaviour.\n    '
    routing_key = 'testsuite.testcase.step.verify.executed'
    _msg_data_template = {'description':'Step (verify) EXECUTED', 
     'response_type':'bool', 
     'verify_response':True, 
     'node':'coap_client', 
     'node_execution_mode':'user_assisted'}


class MsgTestCaseFinished(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description:\n        - Used for indicating to subscribers that the test cases has finished.\n        - This message is followed by a verdict.\n    '
    routing_key = 'testsuite.testcase.finished'
    _msg_data_template = {'testcase_id':'TD_COAP_CORE_01', 
     'testcase_ref':None, 
     'description':'Testcase finished'}


class MsgTestCaseSkip(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description:\n        - Used for skipping a test cases event when was previusly selected to be executed.\n        - testcase_id (optional) : if not provided then current tc is skipped\n        - node (mandatory): node requesting to skip test case\n    '
    routing_key = 'testsuite.testcase.skip'
    _msg_data_template = {'description':'Skip testcase', 
     'testcase_id':None, 
     'node':'someNode'}


class MsgTestCaseSelect(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description: tbd\n\n    '
    routing_key = 'testsuite.testcase.select'
    _msg_data_template = {'testcase_id': 'TD_COAP_CORE_03'}


class MsgTestSuiteAbort(Message):
    __doc__ = '\n    Requirements: TT SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description: Event test suite ABORT\n    '
    routing_key = 'testsuite.abort'
    _msg_data_template = {'description': 'Test suite ABORT command'}


class MsgTestCaseAbort(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD listen to event\n\n    Type: Event\n\n    Pub/Sub: GUI (or automated-IUT)-> Testing Tool\n\n    Description: Event for current test case ABORT\n    '
    routing_key = 'testsuite.testcase.abort'
    _msg_data_template = {'description': 'Test case ABORT (current testcase) command'}


class MsgTestSuiteGetStatus(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description:\n        - Describes current state of the test suite.\n        - Format for the response not standardised.\n    '
    routing_key = 'testsuite.status.request'
    _msg_data_template = {}


class MsgTestSuiteGetStatusReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description:\n        - Describes current state of the test suite.\n        - Format for the response not standardised.\n    '
    routing_key = 'testsuite.status.reply'
    _msg_data_template = {'ok':True, 
     'started':True, 
     'testcase_id':'TD_COAP_CORE_01', 
     'testcase_state':'executing', 
     'step_id':'TD_COAP_CORE_01_step_01'}


class MsgTestSuiteGetTestCases(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: GUI -> Testing Tool\n\n    Description: TBD\n    '
    routing_key = 'testsuite.testcases.list.request'
    _msg_data_template = {}


class MsgTestSuiteGetTestCasesReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: TBD\n    '
    routing_key = 'testsuite.testcases.list.reply'
    _msg_data_template = {'ok':True, 
     'tc_list':[
      {'testcase_id':'TD_COAP_CORE_01', 
       'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_01', 
       'objective':'Perform GET transaction(CON mode)', 
       'state':None},
      {'testcase_id':'TD_COAP_CORE_02', 
       'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_02', 
       'objective':'Perform DELETE transaction (CON mode)', 
       'state':None},
      {'testcase_id':'TD_COAP_CORE_03', 
       'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_03', 
       'objective':'Perform PUT transaction (CON mode)', 
       'state':None}]}


class MsgTestCaseVerdict(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: Used to indicate to the GUI (or automated-iut) which is the final verdict of the testcase.\n    '
    routing_key = 'testsuite.testcase.verdict'
    _msg_data_template = {'verdict':'pass', 
     'description':'No interoperability error was detected,', 
     'partial_verdicts':[
      [
       'TD_COAP_CORE_01_step_02', None, 'CHECK postponed', ''],
      [
       'TD_COAP_CORE_01_step_03', None, 'CHECK postponed', ''],
      [
       'TD_COAP_CORE_01_step_04', 'pass',
       'VERIFY step: User informed that the information was displayed correclty on his/her IUT', ''],
      [
       'CHECK_1_post_mortem_analysis', 'pass',
       '<Frame   3: [bbbb::1 -> bbbb::2] CoAP [CON 43211] GET /test> Match: CoAP(type=0, code=1)'],
      [
       'CHECK_2_post_mortem_analysis', 'pass',
       "<Frame   4: [bbbb::2 -> bbbb::1] CoAP [ACK 43211] 2.05 Content > Match: CoAP(code=69, mid=0xa8cb, tok=b'', pl=Not(b''))"],
      [
       'CHECK_3_post_mortem_analysis', 'pass',
       '<Frame   4: [bbbb::2 -> bbbb::1] CoAP [ACK 43211] 2.05 Content > Match: CoAP(opt=Opt(CoAPOptionContentFormat()))']], 
     'testcase_id':'TD_COAP_CORE_01', 
     'testcase_ref':'http://f-interop.paris.inria.fr/tests/TD_COAP_CORE_01', 
     'objective':'Perform GET transaction(CON mode)', 
     'state':'finished'}


class MsgTestSuiteReport(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: Used to indicate to the GUI (or automated-iut) the final results of the test session.\n    '
    routing_key = 'testsuite.report'
    _msg_data_template = {'tc_results': [
                    {'testcase_id':'TD_COAP_CORE_01', 
                     'verdict':'pass', 
                     'description':'No interoperability error was detected,', 
                     'partial_verdicts':[
                      [
                       'TD_COAP_CORE_01_step_02', None, 'CHECK postponed', ''],
                      [
                       'TD_COAP_CORE_01_step_03', None, 'CHECK postponed', ''],
                      [
                       'TD_COAP_CORE_01_step_04', 'pass',
                       'VERIFY step: User informed that the information was displayed correclty on his/her IUT',
                       ''],
                      [
                       'CHECK_1_post_mortem_analysis', 'pass',
                       '<Frame   3: [bbbb::1 -> bbbb::2] CoAP [CON 43211] GET /test> Match: CoAP(type=0, code=1)'],
                      [
                       'CHECK_2_post_mortem_analysis', 'pass',
                       "<Frame   4: [bbbb::2 -> bbbb::1] CoAP [ACK 43211] 2.05 Content > Match: CoAP(code=69, mid=0xa8cb, tok=b'', pl=Not(b''))"],
                      [
                       'CHECK_3_post_mortem_analysis',
                       'pass',
                       '<Frame   4: [bbbb::2 -> bbbb::1] CoAP [ACK 43211] 2.05 Content > Match: CoAP(opt=Opt(CoAPOptionContentFormat()))']]},
                    {'testcase_id':'TD_COAP_CORE_02', 
                     'verdict':'pass', 
                     'description':'No interoperability error was detected,', 
                     'partial_verdicts':[
                      [
                       'TD_COAP_CORE_02_step_02', None, 'CHECK postponed', ''],
                      [
                       'TD_COAP_CORE_02_step_03', None, 'CHECK postponed', ''],
                      [
                       'TD_COAP_CORE_02_step_04', 'pass',
                       'VERIFY step: User informed that the information was displayed correclty on his/her IUT',
                       ''],
                      ['CHECK_1_post_mortem_analysis', 'pass',
                       '<Frame   3: [bbbb::1 -> bbbb::2] CoAP [CON 43213] DELETE /test> Match: CoAP(type=0, code=4)'],
                      [
                       'CHECK_2_post_mortem_analysis', 'pass',
                       "<Frame   4: [bbbb::2 -> bbbb::1] CoAP [ACK 43213] 2.02 Deleted > Match: CoAP(code=66, mid=0xa8cd, tok=b'')"]]}]}


class MsgSniffingStart(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> sniffing\n\n    Description: tbd\n    '
    routing_key = 'sniffing.start.request'
    _msg_data_template = {'capture_id':'TD_COAP_CORE_01', 
     'filter_if':'tun0', 
     'filter_proto':'udp'}


class MsgSniffingStartReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n    Type: Reply (service)\n    Pub/Sub: sniffing -> coordination\n    Description: tbd\n    '
    routing_key = 'sniffing.start.reply'
    _msg_data_template = {'ok': True}


class MsgSniffingStop(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> sniffing\n\n    Description: tbd\n    '
    routing_key = 'sniffing.stop.request'
    _msg_data_template = {}


class MsgSniffingStopReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: sniffing -> coordination\n\n    Description: tbd\n    '
    routing_key = 'sniffing.stop.reply'
    _msg_data_template = {'ok': True}


class MsgSniffingGetCapture(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> sniffing\n\n    Description: tbd\n    '
    routing_key = 'sniffing.getcapture.request'
    _msg_data_template = {'capture_id': 'TD_COAP_CORE_01'}


class MsgSniffingGetCaptureReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: sniffing -> coordination\n\n    Description: tbd\n    '
    routing_key = 'sniffing.getcapture.reply'
    _msg_data_template = {'ok':True, 
     'file_enc':'pcap_base64', 
     'filename':'TD_COAP_CORE_01.pcap', 
     'value':'1MOyoQIABAAAAAAAAAAAAMgAAAAAAAAA'}


class MsgSniffingGetCaptureLast(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> sniffing\n\n    Description: tbd\n    '
    routing_key = 'sniffing.getlastcapture.request'
    _msg_data_template = {}


class MsgSniffingGetCaptureLastReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: sniffing -> coordination\n\n    Description: tbd\n    '
    routing_key = 'sniffing.getlastcapture.reply'
    _msg_data_template = {'ok':True, 
     'file_enc':'pcap_base64', 
     'filename':'TD_COAP_CORE_01.pcap', 
     'value':'1MOyoQIABAAAAAAAAAAAAMgAAAAAAAAA'}


class MsgRoutingStartLossyLink(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: sniffing -> coordination\n\n    Description: tbd\n    '
    routing_key = 'routing.lossy.link.start'
    _msg_data_template = {'number_of_packets_to_drop': 1}


class MsgInteropTestCaseAnalyze(Message):
    __doc__ = "\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> analysis\n\n    Description:\n        - Method to launch an analysis from a pcap file or a token if the pcap file has already been provided.\n        - The method need a token or a pcap_file but doesn't allow someone to provide both.\n\n    "
    PCAP_empty_base64 = '1MOyoQIABAAAAAAAAAAAAMgAAAAAAAAA'
    PCAP_TC_COAP_01_base64 = '1MOyoQIABAAAAAAAAAAAAAAABAAAAAAAGfdPV8tZCAAtAAAALQAAAAIAAABFAAApcawAAEARAAB/AAABfwAAAdYxFjMAFf4oQgGqAWLatHRlc3TBAhn3T1fHrAgAXgAAAF4AAAACAAAARQAAWlLmAABAEQAAfwAAAX8AAAEWM9YxAEb+WWJFqgFi2sAhHpEC/1R5cGU6IDAgKENPTikKQ29kZTogMSAoR0VUKQpNSUQ6IDQzNTIxClRva2VuOiA2MmRh'
    routing_key = 'analysis.interop.testcase.analyze.request'
    _msg_data_template = {'protocol':'coap', 
     'testcase_id':'TD_COAP_CORE_01', 
     'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_01', 
     'file_enc':'pcap_base64', 
     'filename':'TD_COAP_CORE_01.pcap', 
     'value':PCAP_TC_COAP_01_base64}


class MsgInteropTestCaseAnalyzeReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: analysis -> coordination\n\n    Description:\n        - The recommended structure for the partial_verdicts field is a list of partial verdicts which complies to:\n           - each one of those elements of the list correspond to one CHECK or VERIFY steps of the test description\n            - first value of the list MUST be a "pass", "fail", "inconclusive" or eventually "error" partial verdict (\n            string)\n            - the second value MUST be a string with a description of partial verdict (intended for the user)\n            - more values elements MAY be added to the list\n\n    '
    routing_key = 'analysis.interop.testcase.analyze.reply'
    _msg_data_template = {'ok':True, 
     'verdict':'pass', 
     'analysis_type':'postmortem', 
     'description':'The test purpose has been verified without any fault detected', 
     'review_frames':[],  'token':'0lzzb_Bx30u8Gu-xkt1DFE1GmB4', 
     'partial_verdicts':[
      [
       'pass',
       '<Frame   1: [127.0.0.1 -> 127.0.0.1] CoAP [CON 43521] GET /test> Match: CoAP(type=0, code=1)'],
      [
       'pass',
       "<Frame   2: [127.0.0.1 -> 127.0.0.1] CoAP [ACK 43521] 2.05 Content > Match: CoAP(code=69, mid=0xaa01,                 tok=b'b\\xda', pl=Not(b''))"],
      [
       'pass',
       '<Frame   2: [127.0.0.1 -> 127.0.0.1] CoAP [ACK 43521] 2.05 Content >                 Match: CoAP(opt=Opt(CoAPOptionContentFormat()))']], 
     'testcase_id':'TD_COAP_CORE_01', 
     'testcase_ref':'http://doc.f-interop.eu/tests/TD_COAP_CORE_01'}


class MsgDissectionDissectCapture(Message):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Request (service)\n\n    Pub/Sub: coordination -> dissection, analysis -> dissection\n\n    Description: TBD\n    '
    PCAP_COAP_GET_OVER_TUN_INTERFACE_base64 = '1MOyoQIABAAAAAAAAAAAAMgAAABlAAAAqgl9WK8aBgA7AAAAOwAAAGADPxUAExFAu7sAAAAAAAAAAAAAAAAAAbu7AAAAAAAAAAAAAAAAAALXvBYzABNZUEABcGO0dGVzdMECqgl9WMcaBgCQAAAAkAAAAGAAAAAAaDr//oAAAAAAAAAAAAAAAAAAA7u7AAAAAAAAAAAAAAAAAAGJAAcTAAAAALu7AAAAAAAAAAAAAAAAAAK7uwAAAAAAAAAAAAAAAAACBAgAAAAAAABgAz8VABMRQLu7AAAAAAAAAAAAAAAAAAG7uwAAAAAAAAAAAAAAAAAC17wWMwATWVBAAXBjtHRlc6oJfVjSGgYAOwAAADsAAABgAz8VABMRP7u7AAAAAAAAAAAAAAAAAAG7uwAAAAAAAAAAAAAAAAAC17wWMwATWVBAAXBjtHRlc3TBAg=='
    routing_key = 'dissection.dissectcapture.request'
    _msg_data_template = {'file_enc':'pcap_base64', 
     'filename':'TD_COAP_CORE_01.pcap', 
     'value':PCAP_COAP_GET_OVER_TUN_INTERFACE_base64, 
     'protocol_selection':'coap'}


class MsgDissectionDissectCaptureReply(MsgReply):
    __doc__ = '\n    Requirements: Testing Tool SHOULD implement (other components should not subscribe to event)\n\n    Type: Reply (service)\n\n    Pub/Sub: Dissector -> Coordinator, Dissector -> Analyzer\n\n    Description: TBD\n    '
    routing_key = 'dissection.dissectcapture.reply'
    _frames_example = [
     {'_type':'frame', 
      'id':1, 
      'timestamp':1464858393.547275, 
      'error':None, 
      'protocol_stack':[
       {'_type':'protocol', 
        '_protocol':'NullLoopback', 
        'AddressFamily':'2', 
        'ProtocolFamily':'0'},
       {'_type':'protocol', 
        '_protocol':'IPv4', 
        'Version':'4', 
        'HeaderLength':'5', 
        'TypeOfService':'0x00', 
        'TotalLength':'41', 
        'Identification':'0x71ac', 
        'Reserved':'0', 
        'DontFragment':'0', 
        'MoreFragments':'0', 
        'FragmentOffset':'0', 
        'TimeToLive':'64', 
        'Protocol':'17', 
        'HeaderChecksum':'0x0000', 
        'SourceAddress':'127.0.0.1', 
        'DestinationAddress':'127.0.0.1', 
        'Options':"b''"}]}]
    _msg_data_template = {'ok':True, 
     'token':'0lzzb_Bx30u8Gu-xkt1DFE1GmB4', 
     'frames':_frames_example, 
     'frames_simple_text':None}


class MsgDissectionAutoDissect(Message):
    __doc__ = '\n    Requirements: TT SHOULD publish event\n\n    Type: Event\n\n    Pub/Sub: Testing Tool -> GUI\n\n    Description: Used to indicate to the GUI the dissection of the exchanged packets.\n        - GUI MUST display this info during execution:\n            - interop session\n            - conformance session\n            - performance ?\n            - privacy?\n\n    '
    routing_key = 'testsuite.dissection.autotriggered'
    _frames_example = MsgDissectionDissectCaptureReply._frames_example
    _msg_data_template = {'token':'0lzzb_Bx30u8Gu-xkt1DFE1GmB4', 
     'frames':_frames_example, 
     'frames_simple_text':None, 
     'testcase_id':None, 
     'testcase_ref':None}


class MsgPrivacyAnalyze(Message):
    __doc__ = "\n        Testing Tool's MUST-implement.\n        Analyze PCAP File for Privacy checks.\n    "
    routing_key = 'privacy.analyze.request'
    PCAP_COAP_GET_OVER_TUN_INTERFACE_base64 = 'Cg0NCpgAAABNPCsaAQAAAP//////////AwAuAE1hYyBPUyBYIDEwLjEyLjQsIGJ1aWxkIDE2RTE5NSAoRGFyd2luIDE2LjUuMCkAAAQAPQBEdW1wY2FwIChXaXJlc2hhcmspIDIuMi4wICh2Mi4yLjAtMC1nNTM2OGM1MCBmcm9tIG1hc3Rlci0yLjIpAAAAAAAAAJgAAAABAAAAXAAAAAAAAAAAAAQAAgAEAHR1bjAJAAEABgAAAAwALgBNYWMgT1MgWCAxMC4xMi40LCBidWlsZCAxNkUxOTUgKERhcndpbiAxNi41LjApAAAAAAAAXAAAAAUAAABsAAAAAAAAAIdOBQCsif6eAQAcAENvdW50ZXJzIHByb3ZpZGVkIGJ5IGR1bXBjYXACAAgAh04FAN2Zip4DAAgAh04FAKGJ/p4EAAgAAAAAAAAAAAAFAAgAAAAAAAAAAAAAAAAAbAAAAA=='
    _msg_data_template = {'value':PCAP_COAP_GET_OVER_TUN_INTERFACE_base64, 
     'file_enc':'pcap_base64', 
     'filename':'TD_PRIVACY_DEMO_01.pcap'}


class MsgPrivacyAnalyzeReply(MsgReply):
    __doc__ = "\n            Testing Tool's MUST-implement.\n            Response of Analyze request from GUI\n    "
    routing_key = 'privacy.analyze.reply'
    _privacy_empty_report = {'type':'Anomalies Report', 
     'protocols':[
      'coap'], 
     'conversation':[],  'status':'none', 
     'testing_tool':'Privacy Testing Tool', 
     'byte_exchanged':0, 
     'timestamp':1493798811.53124, 
     'is_final':True, 
     'packets':{},  'version':'0.0.1'}
    _msg_data_template = {'ok':True, 
     'verdict':_privacy_empty_report, 
     'testcase_id':None}


class MsgPrivacyGetConfiguration(Message):
    __doc__ = '\n           Read Privacy configuration.\n           GUI MUST display this info during setup\n    '
    routing_key = 'privacy.configuration.get.request'
    _msg_data_template = {}


class MsgPrivacyGetConfigurationReply(MsgReply):
    __doc__ = '\n           Read Privacy configuration.\n           GUI MUST display this info during setup\n    '
    routing_key = 'privacy.configuration.get.reply'
    _msg_data_template = {'configuration':{},  'ok':True}


class MsgPrivacySetConfiguration(Message):
    __doc__ = '\n        Write Privacy configuration.\n        GUI MUST display this info during setup\n    '
    routing_key = 'privacy.configuration.set.request'
    CFG_EXAMPLE = dict()
    _msg_data_template = {'configuration': CFG_EXAMPLE}


class MsgPrivacySetConfigurationReply(MsgReply):
    __doc__ = '\n        Write Privacy configuration.\n        GUI MUST display this info during setup\n    '
    routing_key = 'privacy.configuration.set.reply'
    _msg_data_template = {'ok': True}


class MsgPrivacyGetStatus(Message):
    __doc__ = "\n    Testing Tool's MUST-implement.\n    GUI -> Testing Tool\n    GUI MUST display this info during execution:\n     - privacy?\n\n    "
    routing_key = 'privacy.getstatus.request'
    _msg_data_template = {}


class MsgPrivacyGetStatusReply(MsgReply):
    __doc__ = "\n    Testing Tool's MUST-implement.\n    GUI -> Testing Tool\n    GUI MUST display this info during execution:\n     - privacy?\n\n    "
    REPORT_EXAMPLE = dict()
    routing_key = 'privacy.getstatus.reply'
    _msg_data_template = {'verdict':REPORT_EXAMPLE, 
     'status':None, 
     'ok':True}


class MsgPrivacyIssue(Message):
    __doc__ = "\n        Testing Tool's MUST-implement.\n        Testing tools -> GUI\n        GUI MUST display this info during execution:\n         - privacy\n\n        "
    routing_key = 'privacy.issue'
    _msg_data_template = {'verdict': json.dumps(MsgPrivacyAnalyzeReply._privacy_empty_report)}


class MsgPerformanceHeartbeat(Message):
    __doc__ = '\n    Requirements:   Timeline Controller MUST listen to event\n                    Performance submodules MUST emit event periodically\n    Type:           Event\n    Pub/Sub:    Performance Submodules -> Timeline Controller\n    Description:    The Timeline Controller verifies that all submodules are\n                    active and in the correct state\n    '
    routing_key = 'performance.heartbeat'
    _msg_data_template = {'mod_name':'unknown', 
     'status':'ready'}


class MsgPerformanceConfiguration(Message):
    __doc__ = '\n    Requirements: Timeline Controller MUST listen to event\n    Type: Event\n    Pub/Sub: Orchestrator -> Timeline Controller\n    Description: Carries the performance test configuration to the Timeline Controller\n    '
    routing_key = 'performance.configuration'
    _msg_data_template = {'configuration': {'static':{},  'initial':{},  'segments':[]}}


class MsgPerformanceSetValues(Message):
    __doc__ = '\n    Requirements:   Performance Submodules MUST listen to event\n    Type:           Event\n    Pub/Sub:    Timeline Controller -> Performance Submodules\n    Description:    During the test execution, the Timeline Controller will\n                    periodically emit this event to the performance submodules\n                    to update dynamic parameters\n    '
    routing_key = 'performance.setvalues'
    _msg_data_template = {'values': {}}


class MsgVizDashboardRequest(Message):
    __doc__ = '\n    Requirements:\n        - Visualization Tool MUST listen to this.\n        - Test Tools should send this message after the Visualization Tool has  confirmed the initialization\n\n    Type: Event\n    Pub/Sub: Testing Tool -> Visualization Tool\n    Description: Visualization Tool uses this message to configure the Dashboard based on the JSON config\n    '
    routing_key = 'viztool-grafana.set_dashboard.request'
    _msg_data_template = {'config': {}}


class MsgVizDashboardReply(MsgReply):
    __doc__ = '\n    Requirements:\n        - Visualization MUST send this after recieving MsgVizDashboardRequest\n        - Test Tool MUST listen to this\n    Type: Event\n    Pub/Sub: Visualization Tool -> Testing Tool\n    Description: This message contains the URL to access the internal Webserver that serves the Grafana Instance\n    '
    routing_key = 'viztool-grafana.set_dashboard.reply'
    _msg_data_template = {'ok': True}


class MsgVizWrite(Message):
    __doc__ = '\n    Requirements:\n        - Performance Testing Tool SHOULD emit this event periodically\n        - Visualization Tool MUST listen to this event\n    Type: Event\n    Pub/Sub: Performance Testing Tool -> Visualization\n    Description:\n        - During the test execution, the Performance Testing Tool MUST periodically emit this event carrying current performance statistics/measurements\n    '
    routing_key = 'viztool-grafana.write_data'
    _msg_data_template = {'measurement':'name', 
     'tags':{},  'time':0, 
     'fields':{'value': 0}}


class MsgVizInitRequest(Message):
    __doc__ = '\n    Requirements:   Implementing Test Tools should send this at start\n                    Visualization Tool MUST listen to this\n    Type:           Event\n    Pub/Sub:    Testing Tool -> Visualization Tool\n    Description:    Visualization Tool is waiting for this message\n                    to start init routines\n    '
    routing_key = 'viztool-grafana.init.request'
    _msg_data_template = {}


class MsgVizInitReply(MsgReply):
    __doc__ = '\n    Requirements:   Visualization MUST send this after recieving MsgVizInitRequest\n                    Test Tool MUST listen to this\n    Type:           Event\n    Pub/Sub:    Visualization Tool -> Testing Tool\n    Description:    This message contains the URL to access the internal Webserver\n                    that serves the Grafana Instance\n    '
    routing_key = 'viztool-grafana.init.reply'
    _msg_data_template = {'ok':True, 
     'url':'http://url-to-access-grafana:1234'}


class MsgReportSaveRequest(Message):
    routing_key = 'results_store.session.report.save.request'
    _msg_data_template = {'type':'final', 
     'data':{}}


class MsgReportSaveReply(MsgReply):
    routing_key = 'results_store.session.report.save.reply'
    _msg_data_template = {'ok': True}


class MsgInsertResultRequest(Message):
    routing_key = 'results_store.insert_result.request'
    _msg_data_template = {'resources':[],  'owners':[],  'session_id':'', 
     'testing_tool_id':'', 
     'timestamp':0, 
     'type':'', 
     'data':{}}


class MsgInsertResultReply(MsgReply):
    routing_key = 'results_store.insert_result.reply'
    _msg_data_template = {'ok': True}


class MsgGetResultRequest(Message):
    routing_key = 'results_store.get_result.request'
    _msg_data_template = {}


class MsgGetResultReply(MsgReply):
    routing_key = 'results_store.get_result.reply'
    _msg_data_template = {'ok':True, 
     'results':[]}


class MsgDeleteResultRequest(Message):
    routing_key = 'results_store.delete_result.request'
    _msg_data_template = {}


class MsgDeleteResultReply(MsgReply):
    routing_key = 'results_store.delete_result.reply'
    _msg_data_template = {'ok': True}


rk_pattern_to_message_type_map = RoutingKeyToMessageMap({'orchestrator.users.list.request':MsgOrchestratorUsersList, 
 'orchestrator.version.request':MsgOrchestratorVersionReq, 
 'orchestrator.users.add.request':MsgOrchestratorUserAdd, 
 'orchestrator.users.delete.request':MsgOrchestratorUserDelete, 
 'orchestrator.users.get.request':MsgOrchestratorUserGet, 
 'orchestrator.sessions.list.request':MsgOrchestratorSessionsList, 
 'orchestrator.sessions.get.request':MsgOrchestratorSessionsGet, 
 'orchestrator.sessions.add.request':MsgOrchestratorSessionsAdd, 
 'orchestrator.sessions.delete.request':MsgOrchestratorSessionsDelete, 
 'orchestrator.sessions.update.request':MsgOrchestratorSessionsUpdate, 
 'orchestrator.tests.get.request':MsgOrchestratorTestsGet, 
 'orchestrator.tests.get_contributor_name.request':MsgOrchestratorTestsGetContributorName, 
 'orchestrator.session.created':MsgSessionCreated, 
 'ui.core.session.get.request':MsgUiRequestSessionConfiguration, 
 'ui.core.session.get.reply':MsgUiSessionConfigurationReply, 
 'ui.user.*.display':MsgUiDisplay, 
 'ui.user.*.request':MsgUiRequest, 
 'ui.user.*.reply':MsgUiReply, 
 'log.*.*':MsgSessionLog, 
 'log':MsgSessionLog, 
 'chat':MsgSessionChat, 
 'fromAgent.*.ip.tun.packet.raw':MsgPacketSniffedRaw, 
 'fromAgent.*.802154.serial.packet.raw':MsgPacketSniffedRaw, 
 'toAgent.*.ip.tun.packet.raw':MsgPacketInjectRaw, 
 'toAgent.*.802154.serial.packet.raw':MsgPacketInjectRaw, 
 'toAgent.*.ip.tun.start':MsgAgentTunStart, 
 'fromAgent.*.ip.tun.started':MsgAgentTunStarted, 
 'toAgent.*.802154.serial.start':MsgAgentSerialStart, 
 'fromAgent.*.802154.serial.started':MsgAgentSerialStarted, 
 'testingtool.ready':MsgTestingToolReady, 
 'testingtool.configured':MsgTestingToolConfigured, 
 'testingtool.terminate':MsgTestingToolTerminate, 
 'testingtool.component.ready':MsgTestingToolComponentReady, 
 'testingtool.component.shutdown':MsgTestingToolComponentShutdown, 
 'testingtool.component.test.ping.request':MsgAutomatedIutTestPing, 
 'testingtool.component.test.ping.reply':MsgAutomatedIutTestPingReply, 
 'testsuite.start':MsgTestSuiteStart, 
 'testsuite.started':MsgTestSuiteStarted, 
 'testsuite.finish':MsgTestSuiteFinish, 
 'testsuite.testcase.ready':MsgTestCaseReady, 
 'testsuite.testcase.start':MsgTestCaseStart, 
 'testsuite.testcase.started':MsgTestCaseStarted, 
 'testsuite.testcase.step.stimuli.execute':MsgStepStimuliExecute, 
 'testsuite.testcase.step.stimuli.executed':MsgStepStimuliExecuted, 
 'testsuite.testcase.step.check.execute':MsgStepCheckExecute, 
 'testsuite.testcase.step.check.executed':MsgStepCheckExecuted, 
 'testsuite.testcase.step.verify.execute':MsgStepVerifyExecute, 
 'testsuite.testcase.step.verify.executed':MsgStepVerifyExecuted, 
 'testsuite.testcase.configuration':MsgTestCaseConfiguration, 
 'testsuite.testcase.configuration.execute':MsgConfigurationExecute, 
 'testsuite.testcase.configuration.executed':MsgConfigurationExecuted, 
 'testsuite.testcase.stop':MsgTestCaseStop, 
 'testsuite.testcase.restart':MsgTestCaseRestart, 
 'testsuite.testcase.skip':MsgTestCaseSkip, 
 'testsuite.testcase.select':MsgTestCaseSelect, 
 'testsuite.testcase.abort':MsgTestCaseAbort, 
 'testsuite.testcase.finished':MsgTestCaseFinished, 
 'testsuite.testcase.verdict':MsgTestCaseVerdict, 
 'testsuite.abort':MsgTestSuiteAbort, 
 'testsuite.report':MsgTestSuiteReport, 
 'testsuite.dissection.autotriggered':MsgDissectionAutoDissect, 
 'testsuite.status.request':MsgTestSuiteGetStatus, 
 'testsuite.status.reply':MsgTestSuiteGetStatusReply, 
 'testsuite.testcases.list.request':MsgTestSuiteGetTestCases, 
 'testsuite.testcases.list.reply':MsgTestSuiteGetTestCasesReply, 
 'session.configuration':MsgSessionConfiguration, 
 'sniffing.start.request':MsgSniffingStart, 
 'sniffing.start.reply':MsgSniffingStartReply, 
 'sniffing.stop.request':MsgSniffingStop, 
 'sniffing.stop.reply':MsgSniffingStopReply, 
 'sniffing.getcapture.request':MsgSniffingGetCapture, 
 'sniffing.getcapture.reply':MsgSniffingGetCaptureReply, 
 'sniffing.getlastcapture.request':MsgSniffingGetCaptureLast, 
 'sniffing.getlastcapture.reply':MsgSniffingGetCaptureLastReply, 
 'routing.lossy.link.start':MsgRoutingStartLossyLink, 
 'analysis.interop.testcase.analyze.request':MsgInteropTestCaseAnalyze, 
 'analysis.interop.testcase.analyze.reply':MsgInteropTestCaseAnalyzeReply, 
 'dissection.dissectcapture.request':MsgDissectionDissectCapture, 
 'dissection.dissectcapture.reply':MsgDissectionDissectCaptureReply, 
 'privacy.analyze.request':MsgPrivacyAnalyze, 
 'privacy.analyze.reply':MsgPrivacyAnalyzeReply, 
 'privacy.getstatus.request':MsgPrivacyGetStatus, 
 'privacy.getstatus.reply':MsgPrivacyGetStatusReply, 
 'privacy.issue':MsgPrivacyIssue, 
 'privacy.configuration.get.request':MsgPrivacyGetConfiguration, 
 'privacy.configuration.get.reply':MsgPrivacyGetConfigurationReply, 
 'privacy.configuration.set.request':MsgPrivacySetConfiguration, 
 'privacy.configuration.set.reply':MsgPrivacySetConfigurationReply, 
 'performance.heartbeat':MsgPerformanceHeartbeat, 
 'performance.configuration':MsgPerformanceConfiguration, 
 'performance.setvalues':MsgPerformanceSetValues, 
 'viztool-grafana.init.request':MsgVizInitRequest, 
 'viztool-grafana.init.reply':MsgVizInitReply, 
 'viztool-grafana.set_dashboard.request':MsgVizDashboardRequest, 
 'viztool-grafana.set_dashboard.reply':MsgVizDashboardReply, 
 'viztool-grafana.write_data':MsgVizWrite, 
 'results_store.session.report.save.request':MsgReportSaveRequest, 
 'results_store.session.report.save.reply':MsgReportSaveReply, 
 'results_store.insert_result.request':MsgInsertResultRequest, 
 'results_store.insert_result.reply':MsgInsertResultReply, 
 'results_store.get_result.request':MsgGetResultRequest, 
 'results_store.get_result.reply':MsgGetResultReply, 
 'results_store.delete_result.request':MsgDeleteResultRequest, 
 'results_store.delete_result.reply':MsgDeleteResultReply})
if __name__ == '__main__':
    import doctest
    doctest.testmod()
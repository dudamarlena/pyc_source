# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Communication.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 16072 bytes
__doc__ = '\nClusterShell inter-nodes communication module\n\nThis module contains the required material for nodes to communicate between each\nothers within the propagation tree. At the highest level, messages are instances\nof several classes. They can be converted into XML to be sent over SSH links\nthrough a Channel instance.\n\nIn the other side, XML is parsed and new message objects are instanciated.\n\nCommunication channels have been implemented as ClusterShell events handlers.\nWhenever a message chunk is read, the data is given to a SAX XML parser, that\nwill use it to create corresponding messages instances as a messages factory.\n\nAs soon as an instance is ready, it is then passed to a recv() method in the\nchannel. The recv() method of the Channel class is a stub, that requires to be\nimplemented in subclass to process incoming messages. So is the start() method\ntoo.\n\nSubclassing the Channel class allows implementing whatever logic you want on the\ntop of a communication channel.\n'
try:
    import _pickle as cPickle
except ImportError:
    import cPickle

import base64, binascii, logging, os, xml.sax
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax import SAXParseException
from collections import deque
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from ClusterShell import __version__
from ClusterShell.Event import EventHandler
ENCODING = 'utf-8'
DEFAULT_B64_LINE_LENGTH = 65536

class MessageProcessingError(Exception):
    """MessageProcessingError"""
    pass


class XMLReader(ContentHandler):
    """XMLReader"""

    def __init__(self):
        """XMLReader initializer"""
        ContentHandler.__init__(self)
        self.msg_queue = deque()
        self.version = None
        self._draft = None
        self._sections_map = None

    def startElement(self, name, attrs):
        """read a starting xml tag"""
        if name == 'channel':
            self.version = attrs.get('version')
            self.msg_queue.appendleft(StartMessage())
        else:
            if name == 'message':
                self._draft_new(attrs)
            else:
                raise MessageProcessingError('Invalid starting tag %s' % name)

    def endElement(self, name):
        """read an ending xml tag"""
        if name == 'message':
            self.msg_queue.appendleft(self._draft)
            self._draft = None
        elif name == 'channel':
            self.msg_queue.appendleft(EndMessage())

    def characters(self, content):
        """read content characters (always decoded string)"""
        if self._draft is not None:
            self._draft.data_update(content.encode(ENCODING))

    def msg_available(self):
        """return whether a message is available for delivery or not"""
        return len(self.msg_queue) > 0

    def pop_msg(self):
        """pop and return the oldest message queued"""
        if self.msg_available():
            return self.msg_queue.pop()

    def _draft_new(self, attributes):
        """start a new packet construction"""
        ctors_map = {ConfigurationMessage.ident: ConfigurationMessage, 
         ControlMessage.ident: ControlMessage, 
         ACKMessage.ident: ACKMessage, 
         ErrorMessage.ident: ErrorMessage, 
         StdOutMessage.ident: StdOutMessage, 
         StdErrMessage.ident: StdErrMessage, 
         RetcodeMessage.ident: RetcodeMessage, 
         TimeoutMessage.ident: TimeoutMessage}
        try:
            msg_type = attributes['type']
            ctor = ctors_map[msg_type]
        except KeyError:
            raise MessageProcessingError('Unknown message type')

        self._draft = ctor()
        self._draft.selfbuild(attributes)


class Channel(EventHandler):
    """Channel"""
    SNAME_WRITER = 'ch-writer'
    SNAME_READER = 'ch-reader'
    SNAME_ERROR = 'ch-error'

    def __init__(self, initiator=False):
        """
        """
        EventHandler.__init__(self)
        self.worker = None
        self.opened = False
        self.setup = False
        self.initiator = initiator
        self._xml_reader = XMLReader()
        self._parser = xml.sax.make_parser(['IncrementalParser'])
        self._parser.setContentHandler(self._xml_reader)
        self.logger = logging.getLogger(__name__)

    def _init(self):
        """start xml document for communication"""
        XMLGenerator((self.worker), encoding=ENCODING).startDocument()

    def _open(self):
        """open a new communication channel from src to dst"""
        xmlgen = XMLGenerator((self.worker), encoding=ENCODING)
        xmlgen.startElement('channel', {'version': __version__})

    def _close(self):
        """close an already opened channel"""
        send_endtag = self.opened
        if send_endtag:
            XMLGenerator((self.worker), encoding=ENCODING).endElement('channel')
        self.worker.abort()
        self.opened = self.setup = False

    def ev_start(self, worker):
        """connection established. Open higher level channel"""
        self.worker = worker
        self.start()

    def ev_read(self, worker, node, sname, msg):
        """channel has data to read"""
        if sname == self.SNAME_ERROR:
            if self.initiator:
                self.recv(StdErrMessage(node, msg))
            return
        try:
            self._parser.feed(msg + '\n')
        except SAXParseException as ex:
            self.logger.error('SAXParseException: %s: %s', ex.getMessage(), msg)
            if self.initiator:
                self.recv(StdErrMessage(node, ex.getMessage()))
            else:
                self.send(ErrorMessage('Parse error: %s' % ex.getMessage()))
            self._close()
            return
        except MessageProcessingError as ex:
            self.logger.error('MessageProcessingError: %s', ex)
            if self.initiator:
                self.recv(StdErrMessage(node, str(ex)))
            else:
                self.send(ErrorMessage(str(ex)))
            self._close()
            return

        while self._xml_reader.msg_available():
            msg = self._xml_reader.pop_msg()
            assert msg is not None
            self.recv(msg)

    def send(self, msg):
        """write an outgoing message as its XML representation"""
        self.worker.write((msg.xml() + '\n'), sname=(self.SNAME_WRITER))

    def start(self):
        """initialization logic"""
        raise NotImplementedError('Abstract method: subclasses must implement')

    def recv(self, msg):
        """callback: process incoming message"""
        raise NotImplementedError('Abstract method: subclasses must implement')


class Message(object):
    """Message"""
    _inst_counter = 0
    ident = 'GEN'
    has_payload = False

    def __init__(self):
        """
        """
        self.attr = {'type':str, 
         'msgid':int}
        self.type = self.__class__.ident
        self.msgid = Message._inst_counter
        self.data = None
        Message._inst_counter += 1

    def data_encode(self, inst):
        """serialize an instance and store the result"""
        encoded = base64.b64encode(cPickle.dumps(inst))
        line_length = int(os.environ.get('CLUSTERSHELL_GW_B64_LINE_LENGTH', DEFAULT_B64_LINE_LENGTH))
        self.data = '\n'.join(encoded[pos:pos + line_length] for pos in range(0, len(encoded), line_length))

    def data_decode(self):
        """deserialize a previously encoded instance and return it"""
        try:
            return cPickle.loads(base64.b64decode(self.data))
        except (EOFError, TypeError, cPickle.UnpicklingError, binascii.Error):
            raise MessageProcessingError('Message %s has an invalid payload' % self.ident)

    def data_update(self, raw):
        """append data to the instance (used for deserialization)"""
        if self.has_payload:
            if self.data is None:
                self.data = raw
            else:
                self.data += raw
        else:
            raise MessageProcessingError('Got unexpected payload for Message %s' % self.ident)

    def selfbuild(self, attributes):
        """self construction from a table of attributes"""
        for k, fmt in self.attr.items():
            try:
                setattr(self, k, fmt(attributes[k]))
            except KeyError:
                raise MessageProcessingError('Invalid "message" attributes: missing key "%s"' % k)

    def __str__(self):
        """printable representation"""
        elts = ['%s: %s' % (k, str(self.__dict__[k])) for k in self.attr.keys()]
        attributes = ', '.join(elts)
        return 'Message %s (%s)' % (self.type, attributes)

    def xml(self):
        """generate XML version of a configuration message"""
        out = BytesIO()
        generator = XMLGenerator(out, encoding=ENCODING)
        state = {}
        for k in self.attr:
            state[k] = str(getattr(self, k))

        generator.startElement('message', state)
        if self.data:
            generator.characters(self.data)
        generator.endElement('message')
        xml_msg = out.getvalue()
        out.close()
        return xml_msg


class ConfigurationMessage(Message):
    """ConfigurationMessage"""
    ident = 'CFG'
    has_payload = True

    def __init__(self, gateway=''):
        """initialize with gateway node name"""
        Message.__init__(self)
        self.attr.update({'gateway': str})
        self.gateway = gateway


class RoutedMessageBase(Message):
    """RoutedMessageBase"""

    def __init__(self, srcid):
        Message.__init__(self)
        self.attr.update({'srcid': int})
        self.srcid = srcid


class ControlMessage(RoutedMessageBase):
    """ControlMessage"""
    ident = 'CTL'
    has_payload = True

    def __init__(self, srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'action':str,  'target':str})
        self.action = ''
        self.target = ''


class ACKMessage(Message):
    """ACKMessage"""
    ident = 'ACK'

    def __init__(self, ackid=0):
        """
        """
        Message.__init__(self)
        self.attr.update({'ack': int})
        self.ack = ackid


class ErrorMessage(Message):
    """ErrorMessage"""
    ident = 'ERR'

    def __init__(self, err=''):
        """
        """
        Message.__init__(self)
        self.attr.update({'reason': str})
        self.reason = err


class StdOutMessage(RoutedMessageBase):
    """StdOutMessage"""
    ident = 'OUT'
    has_payload = True

    def __init__(self, nodes='', output=None, srcid=0):
        """
        Initialized either with empty payload (to be loaded, already encoded),
        or with payload provided (via output to encode here).
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'nodes': str})
        self.nodes = nodes
        self.data = None
        if output is not None:
            self.data_encode(output)


class StdErrMessage(StdOutMessage):
    """StdErrMessage"""
    ident = 'SER'


class RetcodeMessage(RoutedMessageBase):
    """RetcodeMessage"""
    ident = 'RET'

    def __init__(self, nodes='', retcode=0, srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'retcode':int,  'nodes':str})
        self.retcode = retcode
        self.nodes = nodes


class TimeoutMessage(RoutedMessageBase):
    """TimeoutMessage"""
    ident = 'TIM'

    def __init__(self, nodes='', srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'nodes': str})
        self.nodes = nodes


class StartMessage(Message):
    """StartMessage"""
    ident = 'CHA'


class EndMessage(Message):
    """EndMessage"""
    ident = 'END'
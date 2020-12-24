# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message_manager.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nmessage_manager.py\nImplements the MessageManager class which faciliates the sending and receiving\nof messages between a simulator through either the UDP or Capability message\npaths.\n\nContributors: http://svn.secondlife.com/svn/linden/projects/2008/pyogp/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright (c) 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License").\nYou may obtain a copy of the License at:\n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/LICENSE.txt\n$/LicenseInfo$\n'
from logging import getLogger
from pyogp.lib.base.message.udpdispatcher import UDPDispatcher
from pyogp.lib.base.message.message_handler import MessageHandler
from pyogp.lib.base.message.message_dot_xml import MessageDotXML
from pyogp.lib.base.event_queue import EventQueueClient
from pyogp.lib.base.settings import Settings
from eventlet import api
logger = getLogger('pyogp.lib.base.message_manager')

class MessageManager(object):
    """ 
    This object serves as a consolidation point for all messaging related
    functionality in the base/message directory.
    """
    __module__ = __name__

    def __init__(self, host, message_handler=None, capabilities={}, settings=None, start_monitors=False, message_template=None, message_xml=None):
        """ 
        Initialize the MessageManager, applying custom settings and dedicated 
        message_handler if needed 
        """
        logger.debug('Initializing the Message Manager ')
        self.host = host
        if settings != None:
            self.settings = settings
        else:
            self.settings = Settings()
        if message_handler != None:
            self.message_handler = message_handler
        elif self.settings.HANDLE_PACKETS:
            self.message_handler = MessageHandler()
        if not message_template:
            self.message_template = None
        elif isinstance(message_template, file):
            self.message_template = message_template
        else:
            log.warning('%s parameter is expected to be a filehandle, it is a %s.                         Using the embedded message_template.msg' % (message_template, type(message_template)))
            from pyogp.lib.base.data import msg_tmpl
            self.message_template = msg_tmpl
        if not message_xml:
            self.message_xml = MessageDotXML()
        elif isinstance(message_xml, file):
            self.message_xml = MessageDotXML(message_xml=message_xml.read())
        else:
            log.warning('%s parameter is expected to be a filehandle, it is a %s.                         Using the embedded message.xml' % (message_xml, type(message_xml)))
            self.message_xml = MessageDotXML()
        self._is_running = False
        self.capabilities = capabilities
        if self.capabilities.has_key('EventQueueGet'):
            self.event_queue = EventQueueClient(self.capabilities['EventQueueGet'], message_handler=self.message_handler, host=self.host)
        else:
            self.event_queue = None
        self.incoming_queue = []
        self.outgoing_queue = []
        self.udp_dispatcher = UDPDispatcher(settings=self.settings, message_handler=self.message_handler, message_template=self.message_template)
        if start_monitors:
            self.start_monitors()
        return

    def start_monitors(self):
        """ spawn queue monitoring coroutines """
        self._is_running = True
        logger.debug('Spawning region UDP connection')
        api.spawn(self._udp_dispatcher)
        if self.event_queue != None:
            logger.debug('Spawning region event queue connection')
            api.spawn(self.event_queue.start)
        return

    def stop_monitors(self):
        """ stops monitoring coroutines """
        self._is_running = False
        if self.event_queue._running:
            self.event_queue.stop()

    def monitor_outgoing_queue(self):
        """  """
        pass

    def enqueue_message(self, message, reliable=False, now=False):
        """ enqueues a Message() in the outgoing_queue """
        if now:
            self.outgoing_queue.insert(0, (message, reliable))
        else:
            self.outgoing_queue.append((message, reliable))

    def send_message(self):
        """  """
        pass

    def new_message(self, name):
        pass

    def _udp_dispatcher(self):
        """
        Sends and receives UDP messages.
        """
        logger.debug('Spawning region UDP connection')
        while self._is_running:
            api.sleep(0)
            (msg_buf, msg_size) = self.udp_dispatcher.udp_client.receive_packet(self.udp_dispatcher.socket)
            recv_packet = self.udp_dispatcher.receive_check(self.udp_dispatcher.udp_client.get_sender(), msg_buf, msg_size)
            if self.udp_dispatcher.has_unacked():
                self.udp_dispatcher.process_acks()
            while len(self.outgoing_queue) > 0:
                (packet, reliable) = self.outgoing_queue.pop(0)
                self.send_udp_message(packet, reliable)

        logger.debug('Stopped the UDP connection for %s' % self.host)

    def send_udp_message(self, packet, reliable=False):
        """
        Immediately sends an udp message to host
        """
        if reliable:
            return self.udp_dispatcher.send_reliable(packet, self.host, 0)
        else:
            return self.udp_dispatcher.send_message(packet, self.host)
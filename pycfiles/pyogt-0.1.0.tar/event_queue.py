# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/event_queue.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import traceback
from eventlet import api, util
util.wrap_socket_with_coroutine_socket()
from pyogp.lib.base.exc import RegionCapNotAvailable
from pyogp.lib.base.message.message_handler import MessageHandler
from pyogp.lib.base.message.message import Message, Block, Variable
from pyogp.lib.base.message.template_dict import TemplateDictionary
logger = getLogger('pyogp.lib.base.event_queue')

class EventQueueClient(object):
    """ handles an event queue of either an agent domain or a simulator 

    Initialize the event queue client class
    >>> client = EventQueueClient()

    The event queue client requires an event queue capability
    >>> from pyogp.lib.base.caps import Capability
    >>> cap = Capability('EventQueue', http://localhost:12345/cap)

    >>> event_queue = EventQueueClient(cap)
    >>> event_queue.start()

    Sample implementations: region.py
    Tests: tests/test_event_queue.py
    """
    __module__ = __name__

    def __init__(self, capability=None, settings=None, message_handler=None, host=None):
        """ set up the event queue attributes """
        if settings != None:
            self.settings = settings
        else:
            from pyogp.lib.base.settings import Settings
            self.settings = Settings()
        if message_handler != None:
            self.message_handler = message_handler
        else:
            self.message_handler = MessageHandler()
        self.host = host
        self.cap = capability
        self.type = 'typeNotSpecified'
        self._running = False
        self.stopped = False
        self.last_id = -1
        self.data = {}
        self.result = None
        self.template_dict = TemplateDictionary()
        self.current_template = None
        return

    def start(self):
        """ spawns a coroutine connecting to the event queue on the target """
        try:
            if self.cap.name == 'event_queue':
                if self.settings.LOG_COROUTINE_SPAWNS:
                    logger.info('Spawning a coroutine for event queue in the agent domain context.')
                self._processADEventQueue()
                return True
            elif self.cap.name == 'EventQueueGet':
                if self.settings.LOG_COROUTINE_SPAWNS:
                    logger.info('Spawning a coroutine for event queue in the simulator context for %s.' % self.host)
                self._processRegionEventQueue()
                return True
            else:
                logger.warning('Unable to start event queue polling due to %s' % 'unknown queue type')
                return False
        except Exception, error:
            logger.error('Problem starting event queue for %s with cap of %s, with an error of: %s' % (self.host, str(self.cap), error))
            return False

    def stop(self):
        """ trigger the event queue to stop communicating with the simulator """
        logger.info('Stopping event queue.')
        self.stopped = True

        def stop_monitor(self, interval, times):
            """ monitors the stopping of the event queue client connection """
            for i in range(0, times):
                api.sleep(interval)
                if self._running == False:
                    logger.info('Stopped event queue processing for %s', self.host)
                    return

            logger.warning('Failed to stop event queue for %s after %s seconds', self.host, str(interval * times))

        api.spawn(stop_monitor, self, self.settings.REGION_EVENT_QUEUE_POLL_INTERVAL, 10)

    def _processRegionEventQueue(self):
        if self.cap.name != 'EventQueueGet':
            raise RegionCapNotAvailable('EventQueueGet')
        else:
            self._running = True
            while not self.stopped:
                try:
                    api.sleep(self.settings.REGION_EVENT_QUEUE_POLL_INTERVAL)
                    self.data = {}
                    if self.last_id != -1:
                        self.data = {'ack': self.last_id}
                    if self.settings.ENABLE_EQ_LOGGING:
                        if self.settings.ENABLE_HOST_LOGGING:
                            host_string = ' to (%s)' % self.host
                        else:
                            host_string = ''
                        logger.debug('Posting to the event queue%s: %s' % (host_string, self.data))
                    try:
                        self.result = self.cap.POST(self.data)
                    except Exception, error:
                        if self.settings.ENABLE_HOST_LOGGING:
                            host_string = ' from (%s)' % self.host
                        else:
                            host_string = ''
                        logger.info('Received an error we ought not care about%s: %s' % (host_string, error))

                    if self.result != None:
                        self.last_id = self.result['id']
                    else:
                        self.last_id = -1
                    self._parse_result(self.result)
                except Exception, error:
                    logger.warning('Error in a post to the event queue. Error was: %s' % error)

            if self.last_id != -1:
                self.data = {'ack': self.last_id, 'done': True}
                self.cap.POST(self.data)
            self._running = False
            logger.debug('Stopped event queue processing for %s' % self.host)
        return

    def _processADEventQueue(self):
        """ connects to an agent domain's event queue """
        if self.cap.name != 'event_queue':
            raise RegionCapNotAvailable('event_queue')
        else:
            self._running = True
            while not self.stopped:
                api.sleep(self.settings.agentdomain_event_queue_interval)
                self.result = self.capabilities['event_queue'].POST(self.data)
                if self.result != None:
                    self.last_id = self.result['id']
                self._parse_result(self.result)

            self._running = False
        return

    def _parse_result(self, data):
        """ tries to parse the llsd response from an event queue request. 
        if successful, the event queue passes messages through the message_handler for evaluation"""
        try:
            if data != None:
                host_string = ' from (%s)' % self.host
                logger.debug('Event Queue result%s: %s' % (host_string, data))
                parsed_data = self._decode_eq_result(data)
                for packet in parsed_data:
                    self.message_handler.handle(packet)

        except Exception, error:
            traceback.print_exc()
            host_string = ' from (%s)' % self.host
            logger.warning('Error parsing even queue results%s. Error: %s. Data was: %s' % (host_string, error, data))

        return

    def _decode_eq_result(self, data=None):
        """ parse the event queue data, return a list of packets

        the building of packets borrows absurdly much from UDPDeserializer.__decode_data()
        """
        if data != None:
            messages = []
            if data.has_key('events'):
                for i in data:
                    if i == 'id':
                        pass
                    else:
                        for message in data[i]:
                            new_message = Message(message['message'])
                            new_message.event_queue_id = self.last_id
                            new_message.host = self.host
                            in_template = self.template_dict.get_template(message['message'])
                            if in_template:
                                for block_name in message['body']:
                                    for block_data in message['body'][block_name]:
                                        block = Block(block_name)
                                        new_message.add_block(block)
                                        for variable in block_data:
                                            var_data = Variable(variable, block_data[variable], -1)
                                            block.add_variable(var_data)

                            block = Block('Message_Data')
                            new_message.add_block(block)
                            for var in message['body']:
                                var_data = Variable(var, message['body'][var], -1)
                                block.add_variable(var_data)

                            messages.append(new_message)

            return messages
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evgen\writers.py
# Compiled at: 2017-04-23 03:24:59
from __future__ import print_function
from builtins import object
import abc
from evgen.formats import CSVEventFormat
import os, time
from future.utils import with_metaclass

class GenericWriter(with_metaclass(abc.ABCMeta, object)):

    def __init__(self, format=None):
        if format is None:
            format = CSVEventFormat()
        self.Format = format
        return

    @abc.abstractmethod
    def send(self, event):
        """Sends event to sink"""
        pass


class FileWriter(GenericWriter):

    def __init__(self, file_name, format=None, mode='a'):
        self.__output__ = open(file_name, mode)
        super(FileWriter, self).__init__(format=format)

    def send(self, event):
        v = self.Format.format(event)
        if v[(-1)] != '\n':
            v += '\n'
        v = v.encode('utf-8')
        self.__output__.write(v)


class EventHubWriter(GenericWriter):
    """
    EventHubWriter sends all the events to Microsoft Azure Event Hub Service.
    """

    def __init__(self, eh_name, connection_string, format=None):
        from azure.servicebus import ServiceBusService
        conn_dict = {i.split('=', 1)[0]:i.split('=', 1)[1] for i in connection_string.split(';')}
        ns_name = conn_dict['Endpoint'].replace('sb://', '').replace('.servicebus.windows.net/', '')
        self.__sbs__ = ServiceBusService(service_namespace=ns_name, shared_access_key_name=conn_dict['SharedAccessKeyName'], shared_access_key_value=conn_dict['SharedAccessKey'])
        self.__ehname__ = eh_name
        super(EventHubWriter, self).__init__(format=format)

    def send(self, event):
        event['TimeStamp'] = event['TimeStamp'].isoformat() + 'Z'
        try:
            self.__sbs__.send_event(self.__ehname__, self.Format.format(event))
        except:
            time.sleep(1)
            try:
                self.__sbs__.send_event(self.__ehname__, self.Format.format(event))
            except:
                raise IOError('Cannot send message to Event Hub service')


class RabbitMQWriter(GenericWriter):

    def __init__(self, connection_string, queue, format=None):
        import pika
        super(RabbitMQWriter, self).__init__(format=format)
        self.__conn__ = pika.BlockingConnection(pika.URLParameters(connection_string))
        self.__queue_name__ = queue
        self.__channel__ = self.__conn__.channel()
        self.__channel__.queue_declare(queue=self.__queue_name__)

    def send(self, event):
        formatted_event = self.Format.format(event)
        self.__channel__.basic_publish(exchange='', routing_key=self.__queue_name__, body=formatted_event)


class DirectoryWriter(GenericWriter):
    """
    DirectoryWriter creates separate file per session and stores them in predefined directory.
    """

    def __init__(self, directory_name, extension='.log', format=None, mode='a'):
        self.__directory__ = directory_name
        if directory_name not in os.listdir('.'):
            os.mkdir(self.__directory__)
        self.__mode__ = mode
        self.__sid__ = None
        self.__sink__ = None
        self.__extension__ = extension
        super(DirectoryWriter, self).__init__(format=format)
        return

    def send(self, event):
        if self.__sid__ != event['SessionId']:
            self.__sink__ = open(self.__directory__ + '/' + event['SessionId'] + self.__extension__, self.__mode__)
        v = self.Format.format(event)
        if v[(-1)] != '\n':
            v += '\n'
        self.__sink__.write(v)


class ConsoleWriter(GenericWriter):

    def send(self, event):
        print(self.Format.format(event))
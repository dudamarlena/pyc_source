# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmitry.kovalenko/MyOwnMess/my_own_messenger/my_own_client/client.py
# Compiled at: 2018-01-18 12:51:49
# Size of source mod 2**32: 4506 bytes
"""
Функции \u200bк\u200bлиента:\u200b
- сформировать \u200b\u200bpresence-сообщение;
- отправить \u200bс\u200bообщение \u200bс\u200bерверу;
- получить \u200b\u200bответ \u200bс\u200bервера;
- разобрать \u200bс\u200bообщение \u200bс\u200bервера;
- параметры \u200bк\u200bомандной \u200bс\u200bтроки \u200bс\u200bкрипта \u200bc\u200blient.py \u200b\u200b<addr> \u200b[\u200b<port>]:
- addr \u200b-\u200b \u200bi\u200bp-адрес \u200bс\u200bервера;
- port \u200b-\u200b \u200bt\u200bcp-порт \u200b\u200bна \u200bс\u200bервере, \u200b\u200bпо \u200bу\u200bмолчанию \u200b\u200b7777.
"""
from queue import Queue
import logging
from socket import socket, AF_INET, SOCK_STREAM
from my_own_jim.config import *
from my_own_jim.utils import send_message, get_message
import my_own_logs.client_log_config
from my_own_logs.decorators import Log
from my_own_jim.core import JimPresence, JimMessage, Jim, JimResponse, JimDelContact, JimAddContact, JimContactList, JimGetContacts
logger = logging.getLogger('client')
log = Log(logger)

class User:

    def __init__(self, login, addr, port):
        self.addr = addr
        self.port = port
        self.login = login
        self.request_queue = Queue()

    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.addr, self.port))
        presence = self.create_presence()
        send_message(self.sock, presence)
        response = get_message(self.sock)
        response = self.translate_response(response)
        return response

    def disconnect(self):
        self.sock.close()

    @log
    def create_presence(self):
        """
        Сформировать \u200b\u200bpresence-сообщение
        :return: Словарь сообщения
        """
        jim_presence = JimPresence(self.login)
        message = jim_presence.to_dict()
        return message

    @log
    def translate_response(self, response):
        """
        Разбор сообщения
        :param response: Словарь ответа от сервера
        :return: корректный словарь ответа
        """
        result = Jim.from_dict(response)
        return result.to_dict()

    def create_message(self, message_to, text):
        message = JimMessage(message_to, self.login, text)
        return message.to_dict()

    def get_contacts(self):
        jimmessage = JimGetContacts(self.login)
        send_message(self.sock, jimmessage.to_dict())
        response = self.request_queue.get()
        quantity = response.quantity
        message = self.request_queue.get()
        contacts = message.user_id
        return contacts

    def add_contact(self, username):
        message = JimAddContact(self.login, username)
        send_message(self.sock, message.to_dict())
        response = self.request_queue.get()
        return response

    def del_contact(self, username):
        message = JimDelContact(self.login, username)
        send_message(self.sock, message.to_dict())
        response = self.request_queue.get()
        return response

    def send_message(self, to, text):
        message = JimMessage(to, self.login, text)
        send_message(self.sock, message.to_dict())
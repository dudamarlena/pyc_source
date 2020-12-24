# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mqapi.py
# Compiled at: 2019-03-18 05:37:02
# Size of source mod 2**32: 5459 bytes
import sys
if sys.version > '3':
    PY3 = True
else:
    PY3 = False
import pika, pika.exceptions

class mqapi(object):

    def __init__(self, host, username, password, virtualhost='/', callback=None, port=5672):
        """
        RabbitMQ 消息队列出书画
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码
        :param virtualhost: virtualhost
        :param callback: 回调地址，发现消息这个可以不填
        :param port: 端口
        """
        self.user_pwd = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(host=host, credentials=(self.user_pwd), heartbeat=0, virtual_host=virtualhost)
        self.callback = callback

    def __enter__(self):
        pass

    def send_msg(self, queue_name, body, exchange=''):
        """
        消息发送
        :param queue_name: queue名称
        :param body: 参数
        :param exchange: exchange
        :return:
        """
        try:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except pika.exceptions.ConnectionClosed:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()

        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(exchange=exchange, routing_key=queue_name,
          body=body)
        self.s_conn.close()

    def receive_msg_import(self, routing, exchange, quence):
        try:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except pika.exceptions.ConnectionClosed:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except Exception as e:
            try:
                self.s_conn = pika.BlockingConnection(self.parameters)
                channel = self.s_conn.channel()
            finally:
                e = None
                del e

        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=routing)
        self.channel.queue_bind(exchange=exchange, queue=quence,
          routing_key=routing)
        self.channel.basic_consume((self._mqapi__callback), queue=routing, no_ack=False)
        try:
            self.channel.start_consuming()
        except:
            print(sys.exc_info())

        self.s_conn.close()

    def receive_msg(self, routings, exchange=''):
        """
        接收消息
        :param routings:
        :param exchange:
        :return:
        """
        try:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except pika.exceptions.ConnectionClosed:
            self.s_conn = pika.BlockingConnection(self.parameters)
            self.channel = self.s_conn.channel()
        except Exception as e:
            try:
                self.s_conn = pika.BlockingConnection(self.parameters)
                channel = self.s_conn.channel()
            finally:
                e = None
                del e

        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
        for routing in routings:
            self.channel.queue_declare(queue=routing)
            self.channel.queue_bind(exchange=exchange, queue=routing,
              routing_key=routing)
            self.channel.basic_consume((self._mqapi__callback), queue=routing, no_ack=False)

        try:
            self.channel.start_consuming()
        except:
            print(sys.exc_info())

        self.s_conn.close()

    def __callback(self, ch, method, properties, body):
        """
        回调处理
        :param ch:通道
        :param method:方法
        :param properties:
        :param body:
        :return:
        """
        try:
            if self.callback:
                self.callback(method.routing_key, body)
            ch.basic_ack(delivery_tag=(method.delivery_tag))
        except:
            print(sys.exc_info())

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit rabbit mq')
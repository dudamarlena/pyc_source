# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/oneiot_core/main.py
# Compiled at: 2020-04-30 20:03:54
# Size of source mod 2**32: 5458 bytes
import os, socketserver
from threading import Thread
import requests, env, webrepl_cli, websocket, json

class service(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        command = self.data.split('\n')
        result = ''
        print(command)
        if command[0] == 'connect_test':
            result = self.connect_test(command[1:])
        else:
            if command[0] == 'send_to_device':
                result = self.send_to_device(command[1:])
            else:
                if command[0] == 'reset':
                    result = self.reset(command[1:])
                else:
                    if command[0] == 'reset_webrepl':
                        result = self.reset_webrepl(command[1:])
                    else:
                        if command[0] == 'upload':
                            result = self.upload(command[1:])
                        else:
                            if command[0] == 'heartbeat':
                                result = self.heartbeat(command[1:])
        self.request.sendall(result)

    def reset(self, args):
        result = requests.get(f"http://{args[1]}/sys/reset")
        return b'true'

    def reset_webrepl(self, args):
        conn = websocket.WebSocket()
        conn.connect('ws://' + args[0] + ':8266')
        conn.send('secret\n')
        conn.send('import machine\r\n')
        conn.send('machine.reset()\r\n')
        conn.close()
        return b'true'

    def upload(self, args):
        id = args[0]
        ip = args[1]
        source = args[2]
        destination = args[3]
        try:
            requests.get(f"http://{args[1]}/sys/kill", timeout=1)
        except:
            pass

        try:
            webrepl_cli.main('secret', (ip + ':' + destination), 'put', src_file=source)
            return b'true'
        except Exception as e:
            try:
                return b'false'
            finally:
                e = None
                del e

    def connect_test(self, args):
        try:
            result = requests.get(f"http://{args[1]}/sys/test", timeout=1)
        except:
            return b'false'
            return result.content

    def send_to_device(self, args):
        result = requests.post(('http://' + args[1] + '/' + args[2]), data=(args[3]), timeout=3)
        return result.content

    def heartbeat(self, args):
        return b'OK'


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = 'localhost', int(env.var('ONEIOT_C_PORT', 1102))
    server = ThreadedTCPServer((HOST, PORT), service)
    try:
        server.serve_forever()
    except Exception as e:
        try:
            server.shutdown()
        finally:
            e = None
            del e
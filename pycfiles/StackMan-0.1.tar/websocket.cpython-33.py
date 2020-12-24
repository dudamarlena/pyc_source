# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/websocket.py
# Compiled at: 2013-12-13 01:34:17
# Size of source mod 2**32: 4781 bytes
import json, logging, tornado.websocket
from stackman.stack import Stack, load_item
from stackman.common import COMMON_ITEMS

class SocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    stacks = set()

    def allow_draft76(self):
        return True

    def open(self):
        logging.info('Client connected')
        SocketHandler.connections.add(self)

    def on_close(self):
        logging.info('Client disconnected')
        SocketHandler.connections.remove(self)

    @classmethod
    def send_message(cls, stack='', sender='', command='', payload=''):
        message = json.dumps({'stack': stack,  'sender': sender, 
         'command': command, 
         'payload': payload})
        logging.debug('SEND ' + message)
        for conn in cls.connections:
            try:
                conn.write_message(message)
            except:
                logging.error('Could not send message.', exc_info=True)

    def on_message(self, message):
        logging.info('RECV ' + message)
        try:
            message = json.loads(message)
            stack_id = message['stack']
            command = message['command'].lower()
            argument = message['arg']
            if stack_id:
                stack = SocketHandler.stack_by_id(stack_id)
        except ValueError as e:
            logging.warning(e, exc_info=True)
            return False

        try:
            if command == 'start':
                stack.start(argument)
            else:
                if command == 'stop':
                    stack.stop(argument)
                else:
                    if command == 'kill':
                        stack.kill(argument)
                    else:
                        if command == 'addstack':
                            SocketHandler.add_stack(Stack(argument), True)
                        else:
                            if command == 'removestack':
                                SocketHandler.remove_stack(stack, True)
                            else:
                                if command == 'additem':
                                    stack.add_item(argument)
                                else:
                                    if command == 'removeitem':
                                        stack.remove_item(argument)
                                    else:
                                        if command == 'moveup':
                                            stack.move_up(argument)
                                        else:
                                            if command == 'movedown':
                                                stack.move_down(argument)
                                            else:
                                                if command == 'save':
                                                    SocketHandler.save()
                                                else:
                                                    if command == 'reload':
                                                        SocketHandler.load_stacks()
                                                    else:
                                                        if command == 'list':
                                                            self.list_all()
                                                        else:
                                                            logging.warning('Unknown command: ' + command)
        except Exception as e:
            logging.error(e, exc_info=True)

    @classmethod
    def load_stacks(cls):
        for stack in cls.stacks:
            logging.info('Shutting down stack ' + stack[0] + ' for reload.')
            stack[1].stop()

        logging.info('Loading stacks from ' + cls.file)
        cls.stacks = set()
        stack_data = json.load(open(cls.file, 'r'))
        for stack in stack_data['stacks']:
            logging.info('Loading stack: ' + stack['name'])
            s = Stack(stack['name'], stack['id'])
            s.load_items(stack['items'])
            cls.add_stack(s, do_save=False)

        cls.list_all()

    @classmethod
    def save(cls):
        logging.warning('Saving stacks to ' + cls.file)
        out = {'stacks': []}
        for stack in cls.stacks:
            out['stacks'].append(stack[1].save)

        json.dump(out, open(cls.file, 'w'))

    @classmethod
    def stack_by_id(cls, stack_id):
        for stack in cls.stacks:
            if stack[0] == stack_id:
                return stack[1]

        raise Exception('Failed to find stack ' + stack_id)

    @classmethod
    def list_all(cls):
        stacks = dict()
        items = dict()
        for stack in cls.stacks:
            stacks[stack[0]] = stack[1].dump

        for item in COMMON_ITEMS:
            i = load_item(item)
            items[item] = i._dump_config

        cls.send_message(command='list', payload={'stacks': stacks,  'items': items})

    @classmethod
    def add_stack(cls, stack, send_update=False, do_save=True):
        if type(stack) == str:
            stack = Stack(stack)
        cls.stacks.add((stack.id, stack))
        stack.set_socket_handler(cls)
        if do_save:
            cls.save()
        if send_update:
            cls.send_message(stack=stack.id, command='addstack', payload=stack.dump)

    @classmethod
    def remove_stack(cls, stack, send_update=False):
        stack.stop()
        for item in stack.items:
            stack.remove_item(item._id)

        cls.stacks.remove((stack.id, stack))
        logging.info(cls.stacks)
        cls.save()
        if send_update:
            cls.list_all()
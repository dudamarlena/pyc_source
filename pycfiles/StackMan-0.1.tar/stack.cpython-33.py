# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/stack.py
# Compiled at: 2013-12-13 03:02:30
# Size of source mod 2**32: 11723 bytes
"""
StackMan
Stack Manager
Colton J. Provias - cj@coltonprovias.com
Created: December 8, 2013

Manages the stacks and stack objects
"""
import threading, subprocess, time, logging
from importlib import import_module
import uuid
from copy import deepcopy
from pprint import pprint
logging = logging.getLogger('tornado.general')

def load_item(path):
    parts = path.split('.')
    class_name = parts.pop()
    module_path = '.'.join(parts)
    module = import_module(module_path)
    return getattr(module, class_name)


class DummySocketHandler:
    __doc__ = "\n    A mock socket handler for standalone use and testing.  It does not work as\n    a socket, so don't get your hopes up.\n    "

    def send_message(self, stack, sender, command, payload):
        """ Send a message to logging.  Good luck getting it now! """
        logging.debug('Caught Message: ')
        logging.debug('- Stack: ' + stack)
        logging.debug('- Sender: ' + sender)
        logging.debug('- Command: ' + command)
        logging.debug('- Payload: ' + str(payload))

    def save(self):
        """ We aren't saving. """
        pass


class ASyncWatcher(threading.Thread):
    __doc__ = '\n    Watches our streams asyncrhonously.  It fires back to a callback when it\n    has found something interesting like things in stdout, stderr, or car keys.\n    Hint: It will never find one of those things.\n    '

    def __init__(self, process, stream, callback, terminated, stack_item):
        """ Constructor with Inheritence 101 """
        threading.Thread.__init__(self)
        self.process = process
        self.stream = stream
        self.callback = callback
        self.terminated = terminated
        self.stack_item = stack_item

    def run(self):
        """ Run the thread, watch everything, and report to the callback. """
        for line in iter(self.stream.readline, ''):
            if not line and self.process.poll() is not None:
                if self.process.poll() is not None:
                    self.terminated()
                return True
            if not line:
                time.sleep(0.1)
                continue
            self.callback(line.decode())

        return


class StackItemMeta(type):

    def __new__(cls, name, bases, ns):
        return super(StackItemMeta, cls).__new__(cls, name, bases, ns)

    @property
    def _dump_config(self):
        docs = self.__doc__.split('\n')
        output = {'name': {'label': 'Name',  'default': '',  'type': 'str'},  '_args': [
                   'name']}
        start_at = None
        current = None
        for line in docs:
            if line.strip() == 'Arguments:':
                start_at = docs.index(line) + 1
                break

        for line in docs[start_at:]:
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '*':
                name, ctype, label = line.split(' ', 3)[1:]
                current = name
                output[name] = {'type': ctype.strip('()'),  'label': label}
                output['_args'].append(name)
            if line[:8].lower() == 'default:':
                default = line[9:]
                ctype = output[current]['type']
                if ctype == 'bool':
                    default = default is 'True'
                elif ctype == 'int':
                    default = int(default)
                output[current]['default'] = default
                continue

        return output


class StackItem(metaclass=StackItemMeta):
    _socket_handler = DummySocketHandler()
    _is_ready = False
    _watcher_out = False
    _process = None
    _status = 'stopped'

    def __init__(self, **kwargs):
        self._id = str(uuid.uuid4())

    @property
    def _class(self):
        return self.__module__ + '.' + self.__class__.__name__

    @property
    def _config_vars(self):
        return list(self.__class__._dump_config.keys())

    @classmethod
    def _load(cls, item_data):
        new_item = cls()
        if 'id' in item_data:
            new_item._id = item_data['id']
        for arg, value in item_data['config'].items():
            setattr(new_item, arg, value)

        return new_item

    @property
    def _save(self):
        """ For saving to file. """
        arg_dict = dict()
        for arg in self._config_vars:
            if arg is '_args':
                continue
            arg_dict[arg] = getattr(self, arg)

        return {'config': arg_dict,  'class': self._class,  'id': self._id}

    @property
    def _dump(self):
        """ For dumping to browser. """
        out = dict()
        for arg in self._config_vars:
            if arg is '_args':
                continue
            out[arg] = getattr(self, arg)

        out['_id'] = self._id
        out['_class'] = self._class
        out['_command'] = self.command
        out['_status'] = self._status
        return out

    @property
    def _stack_name(self):
        return ':'.join([self._stack.name, self.name])

    @property
    def _is_running(self):
        return self._process is not None and self._process.poll() is None

    def _set_status(self, status):
        self._status = status
        self._socket_handler.send_message(stack=self._stack.id, sender=self._id, command='status', payload=status)
        logging.info(self._stack_name + ' ' + status)

    def _start(self):
        self._set_status('starting')
        self._process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self._watcher_out = ASyncWatcher(self._process, self._process.stdout, self._watch_for_ready, self._on_terminated, self)
        self._watcher_err = ASyncWatcher(self._process, self._process.stderr, self._watch_for_ready, self._on_terminated, self)
        self._watcher_out.start()
        self._watcher_err.start()

    def _stop(self):
        self._set_status('stopping')
        self._process.terminate()
        self._is_ready = False
        while True:
            if not self._is_running:
                break
            time.sleep(0.1)

    def _kill(self):
        self._set_status('killing')
        self._process.kill()
        self._is_ready = False
        while True:
            if not self._is_running:
                break
            time.sleep(0.1)

    def _watch_for_ready(self, line):
        self._on_stdout(line)
        if self.ready_text in line:
            self._set_status('ready')
            self._is_ready = True
            self._watcher_out.callback = self._on_stdout
            self._watcher_err.callback = self._on_stderr

    def _on_stdout(self, line):
        self._socket_handler.send_message(stack=self._stack.id, sender=self._id, command='stdout', payload=line)
        logging.debug(self._stack_name + ': ' + line)

    def _on_stderr(self, line):
        self._socket_handler.send_message(stack=self._stack.id, sender=self._id, command='stderr', payload=line)
        logging.error(self._stack_name + ': ' + line)

    def _on_terminated(self):
        self._set_status('stopped')


class Stack:
    __doc__ = '\n    A stack is like an onion.  Spending too much time with it will make you\n    cry.\n\n    Represents the stack and manages it.\n    '
    items = []
    socket_handler = DummySocketHandler()

    def __init__(self, name='default', stack_id=uuid.uuid4):
        self.name = name
        if stack_id == uuid.uuid4:
            stack_id = str(stack_id())
        self.id = stack_id

    @classmethod
    def set_socket_handler(cls, handler):
        cls.socket_handler = handler
        StackItem._socket_handler = handler

    def load_items(self, items):
        self.items = []
        for item in items:
            self.add_item(item)

    @property
    def save(self):
        out = dict()
        out['id'] = self.id
        out['name'] = self.name
        out['items'] = list()
        for i in self.items:
            out['items'].append(i._save)

        return out

    @property
    def dump(self):
        """ Called to dump to disk """
        out = dict()
        out['name'] = self.name
        out['id'] = self.id
        out['items'] = list()
        for i in self.items:
            out['items'].append(i._dump)

        return out

    def item_index_by_id(self, item_id):
        counter = 0
        for item in self.items:
            if item._id == item_id:
                return counter
            counter += 1

    def get_item_by_id(self, item_id):
        index = self.item_index_by_id(item_id)
        return self.items[index]

    def start(self, item_id=None):
        for item in self.items:
            if not item._is_running:
                item._start()
            while True:
                if item._is_running and item._is_ready:
                    break
                elif not item._is_running:
                    raise ValueError('Filed to start')
                else:
                    time.sleep(0.1)

            if item._id == item_id:
                break

    def stop(self, item_id=None):
        for item in reversed(self.items):
            if item._is_running:
                item._stop()
            else:
                item._set_status('stopped')
            if item._id == item_id:
                break

    def kill(self, item_id=None):
        for item in reversed(self.items):
            if item.is_running and item._id == item_id:
                item.kill()
                break
            elif item.is_running:
                item.stop()
            else:
                item._set_status('stopped')

    def add_item(self, item_data):
        item = load_item(item_data['class'])._load(item_data)
        item._stack = self
        self.items.append(item)
        self.socket_handler.save()
        self.socket_handler.send_message(stack=self.id, sender=item._id, command='additem', payload=item._dump)
        return item

    def remove_item(self, item_id):
        self.stop(item_id)
        i = self.item_index_by_id(item_id)
        self.items.pop(i)
        self.socket_handler.save()
        self.socket_handler.send_message(stack=self.id, sender=item_id, command='removeitem')

    def move_up(self, item_id):
        i = self.item_index_by_id(item_id)
        logging.info(item_id)
        if i < len(self.items) - 1:
            k = i + 1
            self.stop(item_id)
            self.items[i], self.items[k] = self.items[k], self.items[i]
            self.socket_handler.save()
            self.socket_handler.send_message(stack=self.id, sender=item_id, command='moveup')

    def move_down(self, item_id):
        i = self.item_index_by_id(item_id)
        if i > 0:
            k = i - 1
            self.stop(self.items[k]._id)
            self.items[i], self.items[k] = self.items[k], self.items[i]
            self.socket_handler.save()
            self.socket_handler.send_message(stack=self.id, sender=item_id, command='movedown')
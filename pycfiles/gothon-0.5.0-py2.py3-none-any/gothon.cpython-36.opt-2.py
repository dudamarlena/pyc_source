# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /gothon.py
# Compiled at: 2018-04-16 20:28:14
# Size of source mod 2**32: 6761 bytes
"""Gothon.

Gothon runs GO Code from Python using IPC RPC JSON (non-HTTP) & subprocess."""
import json, os, signal, socket, subprocess, sys
from glob import iglob
from itertools import count
from pathlib import Path
from shutil import which
from time import sleep
from uuid import uuid4
__version__ = '0.5.0'
__all__ = ('Gothon', 'GoImporter', 'PYTHON_MODULE_GO_TEMPLATE')
PYTHON_MODULE_GO_TEMPLATE = '\npackage main\n\nimport (\n    "log"\n    "net"\n    "net/rpc"\n    "net/rpc/jsonrpc"\n    "os"\n)\n\n// Define Functions here.\ntype Echo int\n\nfunc (h *Echo) Echo(arg *string, reply *string) error {\n    log.Println("received: ", *arg)\n    *reply = *arg\n    return nil\n}\n\nfunc main() {\n    // Register Functions on the RPC here.\n    hello := new(Echo)\n    rpc.Register(hello)\n\n    listener, errors := net.Listen("unix", os.Args[1])\n    defer listener.Close()\n\n    if errors != nil {\n        log.Fatal(errors)\n    }\n\n    log.Print("Listening for RPC-JSON connections: ", listener.Addr())\n\n    for {\n        log.Print("Waiting for RPC-JSON connections...")\n        conection, errors := listener.Accept()\n\n        if errors != nil {\n            log.Printf("Accept error: %s", conection)\n            continue\n        }\n\n        log.Printf("Connection started: %v", conection.RemoteAddr())\n        go jsonrpc.ServeConn(conection)\n    }\n}\n'

class RPCJSONClient(object):
    __doc__ = 'RPC JSON Client (non-HTTP).'
    __slots__ = ('socket_file', '_id', 'socket', '__repr__')

    def __init__(self, socket_file):
        self.socket_file = socket_file
        self._id = count()
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.socket_file)

    def call(self, name, *params):
        """RPC IPC Call to a Go function, return results or raise error."""
        mssg = {'id':next(self._id), 
         'params':tuple(params),  'method':name}
        data = bytes(json.dumps(mssg, separators=(',', ':')), 'utf-8')
        self.socket.sendall(data)
        print(f"Sent:     {data}")
        while True:
            try:
                json_response = json.loads(self.socket.recv(8192))
                if not json_response:
                    break
            except Exception:
                sleep(0.1)
            else:
                break

        response, _id = json_response.get, mssg.get('id')
        if response('id') != _id:
            raise Exception(f"Expected ID={_id},received ID={response('id')}.")
        else:
            if response('error') is not None:
                raise Exception(f"{self.__class__.__name__}: {response('error')}.")
        print(f"Received: {response('result')}")
        return response('result')

    def __exit__(self, *args, **kwargs):
        self.socket.close()


class Gothon(object):
    __doc__ = 'Gothon runs GO Code from Python using IPC RPC JSON.'
    __slots__ = ('go_file', 'startup_delay', 'go', 'rpc', 'proces', 'close', 'stop',
                 'kill', 'terminate', 'socket_file')

    def __init__(self, go_file: str=Path(__file__).parent / 'python_module.go', startup_delay: float=0.1):
        self.close = self.stop = self.kill = self.terminate = self.__exit__
        self.socket_file = f"/tmp/gothon-{uuid4().hex}.sock"
        self.startup_delay = float(startup_delay)
        self.go_file = Path(go_file)
        self.go = which('go')
        self.rpc, self.proces = (None, None)
        if self.go:
            if self.go_file.is_file():
                self._build()
        print(f"PID: {self.proces.pid}, Socket: {self.socket_file}")

    def _build(self):
        """Run Go code using 'go run' passing the Unix Socket as argument. """
        self.proces = subprocess.Popen(f"{self.go} run {self.go_file} {self.socket_file}",
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT),
          shell=True,
          preexec_fn=(os.setpgrp))

    def start(self) -> RPCJSONClient:
        """Start the RPC IPC Python Client side."""
        self.rpc = RPCJSONClient(self.socket_file)
        self.rpc.__doc__ = self.__doc__
        self.rpc.__repr__ = self.__repr__
        sleep(self.startup_delay)
        return self.rpc

    @staticmethod
    def clean():
        """Simple helper function to clean stale unused Unix Socket files."""
        for file2clean in iglob('/tmp/gothon-*.sock'):
            print(f"Deleted old stale unused Unix Socket file: {file2clean}")
            Path(file2clean).unlink()

    @staticmethod
    def template():
        """Helper function to print a Go code Template to start hacking into."""
        print(PYTHON_MODULE_GO_TEMPLATE)

    def __repr__(self):
        return f"<Gothon object {id(self)} from {self.go_file}>"

    def __exit__(self, *args, **kwargs):
        self.rpc.socket.close()
        self.proces.kill()
        os.killpg(os.getpgid(self.proces.pid), signal.SIGTERM)


class GoImporter(object):
    __doc__ = 'Custom Importer to just import Go *.go files as Python modules.'

    def __init__(self, *args, **kwargs):
        self.module_names = args
        self.go_path = None

    def find_module(self, fullname, path=None):
        if fullname in self.module_names:
            self.go_path = str(path)
            return self
        possible_module_paths = (
         Path(fullname + '.go'),
         Path('.') / f"{fullname}.go",
         Path(fullname).with_suffix('.go'),
         Path(fullname.split('.')[(-1)] + '.go'),
         Path(fullname.replace('.', os.sep)).with_suffix('.go'))
        if isinstance(path, str):
            if len(path):
                possible_module_paths += (
                 Path(path),
                 Path(path + '.go'),
                 Path('.') / f"{path}.go",
                 Path(path).with_suffix('.go'),
                 Path(path) / f"{fullname.split('.')[(-1)]}.go")
        for path2check in possible_module_paths:
            if path2check.is_file():
                if path2check.suffix == '.go':
                    self.go_path = str(path2check)
                    return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules.get(fullname)
        else:
            module = Gothon(go_file=(self.go_path))
            sys.modules[fullname] = module
            return module


def import_hook():
    """Enable importing *.go files."""
    go_importer = GoImporter()
    sys.path_hooks.insert(0, go_importer)
    sys.meta_path.insert(0, go_importer)
    return go_importer
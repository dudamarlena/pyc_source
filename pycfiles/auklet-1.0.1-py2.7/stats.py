# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auklet/stats.py
# Compiled at: 2018-10-16 12:42:27
from __future__ import absolute_import, division, unicode_literals
import msgpack, pprint, inspect
from uuid import uuid4
from time import time
from auklet.utils import get_agent_version
try:
    import psutil
except ImportError:
    psutil = None

__all__ = [b'MonitoringTree', b'Event', b'SystemMetrics', b'Function']

class Function(object):
    __slots__ = [
     b'samples', b'line_num', b'func_name', b'file_path',
     b'children', b'parent']

    def __init__(self, line_num, func_name, file_path=b'', parent=None, samples=1):
        self.line_num = line_num
        self.func_name = func_name
        self.parent = parent
        self.children = []
        self.file_path = file_path
        self.samples = samples

    def __str__(self):
        pp = pprint.PrettyPrinter()
        return pp.pformat(dict(self))

    def __iter__(self):
        yield (
         b'functionName', self.func_name)
        yield (b'nSamples', self.samples)
        yield (b'lineNumber', self.line_num)
        yield (b'filePath', self.file_path)
        yield (b'callees', [ dict(item) for item in self.children ])

    def has_child(self, test_child):
        for child in self.children:
            if test_child.func_name == child.func_name and test_child.file_path == child.file_path:
                return child

        return False


class Event(object):
    __slots__ = [
     b'trace', b'exc_type', b'line_num', b'abs_path']

    def __init__(self, exc_type, tb, tree, abs_path):
        self.exc_type = exc_type.__name__
        self.line_num = tb.tb_lineno
        self.abs_path = abs_path
        self._build_traceback(tb, tree)

    def __iter__(self):
        yield (
         b'stackTrace', self.trace)
        yield (b'excType', self.exc_type)

    def _convert_locals_to_string(self, local_vars):
        for key in local_vars:
            if type(local_vars[key]) != str and type(local_vars[key]) != int:
                local_vars[key] = str(local_vars[key])

        return local_vars

    def _build_traceback(self, trace, tree):
        tb = []
        while trace:
            frame = trace.tb_frame
            path = tree.get_filename(frame.f_code, frame)
            tb.append({b'functionName': frame.f_code.co_name, b'filePath': path, 
               b'lineNumber': frame.f_lineno, 
               b'locals': self._convert_locals_to_string(frame.f_locals)})
            trace = trace.tb_next

        self.trace = tb


class MonitoringTree(object):
    __slots__ = [
     b'commit_hash', b'public_ip', b'mac_hash',
     b'abs_path', b'root_func']
    cached_filenames = {}

    def __init__(self, mac_hash=None, release=None):
        from auklet.utils import get_device_ip, get_abs_path
        self.commit_hash = release
        self.public_ip = get_device_ip()
        self.abs_path = get_abs_path(b'.auklet/version')
        self.mac_hash = mac_hash
        self.root_func = None
        return

    def get_filename(self, code, frame):
        key = code.co_code
        file_name = self.cached_filenames.get(code.co_code, None)
        if file_name is None:
            try:
                file_name = inspect.getsourcefile(frame) or inspect.getfile(frame)
            except (TypeError, AttributeError):
                return

            self.cached_filenames[key] = file_name
        return file_name

    def _create_frame_func(self, frame, root=False, parent=None):
        if root:
            return Function(line_num=1, func_name=b'root', parent=None, file_path=b'', samples=1)
        else:
            file_path = self.get_filename(frame.f_code, frame)
            return Function(line_num=frame.f_code.co_firstlineno, func_name=frame.f_code.co_name, parent=parent, file_path=file_path)

    def _build_tree(self, new_stack):
        root_func = self._create_frame_func(None, True)
        parent_func = root_func
        for frame in reversed(new_stack):
            current_func = self._create_frame_func(frame, parent=parent_func)
            parent_func.children.append(current_func)
            parent_func = current_func

        return root_func

    def _update_sample_count(self, parent, new_parent):
        if not new_parent.children:
            return True
        new_child = new_parent.children[0]
        has_child = parent.has_child(new_child)
        if has_child:
            has_child.samples += 1
            return self._update_sample_count(has_child, new_child)
        parent.children.append(new_child)

    def update_hash(self, new_stack):
        new_tree_root = self._build_tree(new_stack)
        if self.root_func is None:
            self.root_func = new_tree_root
            return self.root_func
        else:
            self._update_sample_count(self.root_func, new_tree_root)
            return

    def clear_root(self):
        self.root_func = None
        return True

    def build_tree(self, client):
        if self.root_func is not None:
            return {b'application': client.app_id, 
               b'publicIP': self.public_ip, 
               b'id': str(uuid4()), 
               b'timestamp': int(round(time() * 1000)), 
               b'macAddressHash': self.mac_hash, 
               b'release': self.commit_hash, 
               b'agentVersion': get_agent_version(), 
               b'tree': dict(self.root_func), 
               b'device': client.broker_username, 
               b'absPath': client.abs_path, 
               b'version': client.version}
        else:
            return {}

    def build_msgpack_tree(self, client):
        return msgpack.packb(self.build_tree(client), use_bin_type=False)


class SystemMetrics(object):
    cpu_usage = 0.0
    mem_usage = 0.0
    inbound_network = 0
    outbound_network = 0
    prev_inbound = 0
    prev_outbound = 0

    def __init__(self):
        if psutil is not None:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            self.mem_usage = psutil.virtual_memory().percent
        return

    def __iter__(self):
        yield (
         b'cpuUsage', self.cpu_usage)
        yield (b'memoryUsage', self.mem_usage)
        yield (b'inboundNetwork', self.inbound_network)
        yield (b'outboundNetwork', self.outbound_network)
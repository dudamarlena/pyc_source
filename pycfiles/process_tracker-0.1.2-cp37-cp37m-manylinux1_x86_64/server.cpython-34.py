# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/process_tracing/sandbox/server.py
# Compiled at: 2017-01-18 08:39:39
# Size of source mod 2**32: 6203 bytes
import uuid, os, tempfile, errno, mmap, stat, struct, socket
from ptrace.cpu_info import CPU_WORD_SIZE
from threading import Thread
from cffi import FFI

class SharedMemoryManagementServer(Thread):
    """SharedMemoryManagementServer"""
    SOCKET_TIMEOUT = 10

    def __init__(self, shm_size=5242880):
        """
        Create a new shared memory server instance
        :param shm_size: Size of the shared memory area that should be created (in bytes)
        """
        super().__init__()
        self.shm_name = SharedMemoryManagementServer._get_unique_shared_memory_name()
        self.socket_path = SharedMemoryManagementServer._get_unique_socket_path()
        self._shm_lib = None
        self.stopped = False
        self.process_memory_map = {}
        self._shm_server_struct = struct.Struct('=256si')
        self._shm_client_struct = struct.Struct('@Pii')
        self.shm_size = shm_size
        self._shm_fd = self._open_shm(self.shm_name, self.shm_size)
        self.shared_memory = SharedMemoryManagementServer._open_shared_memory(self._shm_fd, self.shm_size)
        self.socket = SharedMemoryManagementServer._create_server_socket(self.socket_path)

    def stop(self):
        """
        Mark the server to halt on the next possible time
        As the socket has a fixed SOCKET_TIMEOUT it will take a maximum as SOCKET_TIMEOUT seconds before this
        method will return
        :return: None
        """
        self.stopped = True
        SharedMemoryManagementServer._close_server_socket(self.socket)
        self.socket = None
        self.join()

    def run(self):
        """
        Invoked when start is called by the Thread class
        This will start a new thread that runs the shared memory thread
        :return: None
        """
        while not self.stopped:
            try:
                client, port = self.socket.accept()
            except Exception as e:
                continue

            server_data = self._shm_server_struct.pack(self.shm_name.encode('ascii'), self.shm_size)
            client.send(server_data)
            client_data = client.recv(self._shm_client_struct.size)
            client_address, pid, _ = self._shm_client_struct.unpack(client_data)
            print('New client with PID {} connected and mapped the SHM to address: 0x{:08x}'.format(pid, client_address))
            client.close()
            self.process_memory_map[pid] = client_address

        SharedMemoryManagementServer._close_shared_memory(self.shared_memory)
        self._close_shm(self._shm_fd, self.shm_name)
        SharedMemoryManagementServer._close_server_socket(self.socket)

    def write_to_shared_memory(self, data, offset=0):
        """
        """
        position = self.shared_memory.tell()
        if (position + offset) % CPU_WORD_SIZE:
            padding = CPU_WORD_SIZE - (position + offset) % CPU_WORD_SIZE
            self.shared_memory.write('\x00' * padding)
            position = self.shared_memory.tell()
        self.shared_memory.write(data)
        if len(data) % CPU_WORD_SIZE:
            padding = CPU_WORD_SIZE - len(data) % CPU_WORD_SIZE
            self.shared_memory.write('\x00' * padding)
        return position

    def _get_shm_lib(self):
        if not self._shm_lib:
            ffi = FFI()
            ffi.cdef('int shm_open(const char *name, int oflag, int mode); int shm_unlink(const char *name);')
            self._shm_lib = ffi.dlopen('rt')
        if not self._shm_lib:
            raise OSError('SHM library could not be loaded. Is librt installed?')
        return self._shm_lib

    def _open_shm(self, name, size):
        """
        """
        shm_lib = self._get_shm_lib()
        fd = shm_lib.shm_open(name.encode('ascii'), os.O_CREAT | os.O_RDWR, stat.S_IRUSR | stat.S_IWUSR)
        if fd < 0:
            raise OSError('Failed to shm_open({}) with errno: {}', name, errno.errorcode)
        os.ftruncate(fd, size)
        return fd

    def _close_shm(self, fd, name):
        """
        """
        shm_lib = self._get_shm_lib()
        os.close(fd)
        result_code = shm_lib.shm_unlink(name.encode('ascii'))
        if result_code < 0:
            raise OSError('Failed to shm_unlink({}) with errno: {}', name, errno.errorcode)

    @staticmethod
    def _open_shared_memory(fd, size):
        """
        """
        mapped_memory = mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)
        if not mapped_memory:
            raise OSError('Failed to map the shared memory fd to memory.')
        mapped_memory.write('\x00' * size)
        mapped_memory.seek(0, os.SEEK_SET)
        return mapped_memory

    @staticmethod
    def _close_shared_memory(mapped_memory):
        """
        """
        mapped_memory.close()

    @staticmethod
    def _create_server_socket(path):
        """
        """
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        s.bind(path)
        s.listen(16)
        s.settimeout(SharedMemoryManagementServer.SOCKET_TIMEOUT)
        return s

    @staticmethod
    def _close_server_socket(s):
        """
        """
        if s:
            s.close()

    @staticmethod
    def _get_unique_socket_path():
        name = '{}.sock'.format(str(uuid.uuid4()))
        return os.path.join(tempfile.gettempdir(), name)

    @staticmethod
    def _get_unique_shared_memory_name():
        return str(uuid.uuid4())
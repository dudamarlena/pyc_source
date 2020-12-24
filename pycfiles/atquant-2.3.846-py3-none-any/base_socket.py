# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\socket_ctrl\base_socket.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 7881 bytes
import socket, struct, time, traceback
from atquant.data.const_data import Enum_Const
from atquant.utils.logger import write_syslog, write_userlog
OPEN = 1
CLOSE = 0

def atClearAllTCPIP():
    pass


class HandleSocket:

    def __init__(self, port, *args):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', port)
        self.BUF_SIZE = 104857600
        self.data = None
        self.temp_buf = bytearray(self.BUF_SIZE)
        self.recv_buf = memoryview(self.temp_buf)
        self.timeout = args[0] if args else 300
        self.client.settimeout(self.timeout)
        self.connect_to_at()
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576000)
        self.status = OPEN

    def connect_to_at(self):
        attempts = 0
        while attempts < 2:
            try:
                self.client.connect(self.server_address)
                self.status = OPEN
                break
            except (socket.timeout, socket.error) as e:
                attempts += 1
                if attempts == 2:
                    write_userlog('{}{!r} '.format(Enum_Const.FAIL_CONNECT_AT.value, e), level='error', console=Enum_Const.FAIL_CONNECT_AT.value)
                    exit(-1)

    def disconnect_from_at(self):
        try:
            if self.status != CLOSE:
                self.client.close()
                self.status = CLOSE
        except (socket.error, Exception) as e:
            write_syslog(traceback.format_exc(), level='error', console=str(e))

    def reconnect_to_at(self):
        self.disconnect_from_at()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(self.timeout)
        self.connect_to_at()
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576000)
        self.status = OPEN

    def send_data(self, data):
        self.client.sendall(data)
        write_syslog(data, level='info', trace_debug=True)

    def recv_data(self, recv_bytes=None, ignore_error=False, try_times=3):
        try:
            self.data = b''
            if isinstance(recv_bytes, (int, float)):
                recv_bytes = int(recv_bytes)
                self.data = b''
                if recv_bytes < 0:
                    return self.data
                try_counter = 0
                recv_len = 0
                while try_counter < try_times:
                    tmp_buf = self.client.recv(int(recv_bytes - recv_len))
                    try_counter += 1
                    if tmp_buf is not None:
                        self.data += tmp_buf
                    recv_len += len(tmp_buf)
                    if recv_len >= recv_bytes:
                        break
                    time.sleep(0.01)

                self.recv_buf[:len(self.data)] = self.data
                return self.data
            else:
                recv_len = self.client.recv_into(self.recv_buf, self.BUF_SIZE)
                self.data = self.recv_buf[:recv_len].tobytes()
                return self.data
        except (socket.error, Exception) as e:
            write_syslog(traceback.format_exc(), level='error', console=str(e))
            if ignore_error is False:
                raise Exception('received data from socket occoured an error') from e

    def recv_garbage_data(self, ignore_timeout=True):
        old_timeout = 300
        try:
            try:
                old_timeout = self.client.timeout
                self.client.settimeout(0.1)
                self.data = self.recv_data(ignore_error=True)
            except socket.error:
                pass

        finally:
            try:
                self.client.settimeout(old_timeout)
            except Exception:
                pass

        return self.data

    def recv_least_data(self, least_len, try_times=3):
        """
        从网络至少接收 least_len 字节的数据。
        注意接收数据的编码，不同编码，字节长度不一样。
        """
        recv_ = b''
        try_counter = 0
        while try_counter < try_times:
            data = self.recv_data(ignore_error=True)
            try_counter += 1
            if data is None:
                pass
            else:
                recv_ += data
                if len(recv_) >= least_len:
                    return recv_
                time.sleep(0.1)

    def recv_data_by_size2(self, body_size=-1):
        """
        接收指定大小的package，
        若从包头获取包体大小，格式为：数据类型(double 8字节)数据大小(double 8字节)数据
        :param packet_size: -1 表示从包头接收并解析待接收包的大小，否则，直接接收固定大小的包
        :return: 接收的二进制数据
        """
        PACK_HEAD_LEN = 16
        recv_len, pos = (0, 0)
        contain_head = True if body_size <= 0 else False
        if contain_head:
            head = self.recv_data(recv_bytes=PACK_HEAD_LEN, ignore_error=False)
            body_size, = struct.unpack('!d', head[8:16])
            recv_len += PACK_HEAD_LEN
        body = self.recv_data(recv_bytes=body_size, ignore_error=False)
        recv_len += int(body_size)
        if contain_head:
            self.temp_buf[0:PACK_HEAD_LEN] = head
            self.temp_buf[PACK_HEAD_LEN:recv_len] = body
        else:
            self.temp_buf[:recv_len] = body
        return self.temp_buf[0:recv_len]

    def recv_data_by_size(self):
        recv_len = 0
        head = self.recv_data(recv_bytes=8, ignore_error=False)
        body_size, = struct.unpack('!d', head[0:8])
        recv_len += 8
        body = self.recv_data(recv_bytes=body_size * 8, ignore_error=False)
        recv_len += int(body_size * 8)
        self.temp_buf[0:8] = head
        self.temp_buf[8:recv_len] = body
        return self.temp_buf[0:recv_len]

    def test_channel_available(self):
        if self.status != OPEN:
            self.connect_to_at()
        pid = int(round(time.time() * 1000) % 10000000)
        head = '<Matlabcmd pid="%d" cmd="%s" >' % (pid, 'ATraderEcho')
        end = '</Matlabcmd>'
        echo_cmd = head + end
        echo_cmd = echo_cmd.encode('utf-8')
        self.send_data(echo_cmd)
        self.recv_data()

    def send_xml_cmd(self, head_tail, *args):
        pid = int(round(time.time() * 1000) % 10000000)
        head = '<Matlabcmd pid="%d" %s>' % (pid, head_tail)
        end = '</Matlabcmd>'
        if len(args) > 0:
            middle = args[0]
            echo_cmd = head + middle + end
        else:
            echo_cmd = head + end
        echo_cmd = echo_cmd.encode('utf-8')
        self.send_data(echo_cmd)
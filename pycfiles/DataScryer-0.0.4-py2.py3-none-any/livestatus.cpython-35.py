# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\livestatus.py
# Compiled at: 2016-08-11 03:01:01
# Size of source mod 2**32: 3126 bytes
import re, socket, time
from datascryer.helper.python import python_3
BUFFER_SIZE = 1024

class Connector:

    def __init__(self, ip=None, soc=None):
        if ip is not None:
            self._Connector__address = ip
            self._Connector__socket_type = socket.AF_INET
        else:
            if soc is not None:
                self._Connector__address = soc
                self._Connector__socket_type = socket.AF_UNIX
            else:
                raise Exception('Neither IP nor socket was given!')
        self._Connector__socket = None
        self._Connector__perf_label_regex = re.compile('([^=]+)=(U|[\\d\\.\\-]+)([\\w\\/%]*);?([\\d\\.\\-:~@]+)?;?([\\d\\.\\-:~@]+)?;?([\\d\\.\\-]+)?;?([\\d\\.\\-]+)?;?\\s*')

    def _open_socket(self):
        self._Connector__socket = socket.socket(self._Connector__socket_type, socket.SOCK_STREAM)
        self._Connector__socket.connect(self._Connector__address)
        self._Connector__socket.settimeout(5)

    def _make_request(self, query):
        if not query.endswith('\n'):
            query += '\n'
        query += 'Localtime: %d\nOutputFormat: python\nResponseHeader: fixed16\n\n' % int(time.time())
        self._open_socket()
        if python_3():
            self._Connector__socket.send(bytes(query, encoding='UTF-8'))
        else:
            self._Connector__socket.send(query)
        self._Connector__socket.shutdown(socket.SHUT_WR)
        data = ''
        buffer = self._Connector__socket.recv(BUFFER_SIZE)
        while buffer:
            data += buffer.decode()
            buffer = self._Connector__socket.recv(BUFFER_SIZE)

        return_code = data[0:3]
        if return_code == '200':
            return eval(data[16:])
        raise Exception('Livestatus returned with ' + return_code)

    def get_hosts(self):
        response = self._make_request(query='GET hosts\nColumns: name check_command perf_data\n')
        result = {}
        for i in range(len(response)):
            lables = []
            for m in re.finditer(self._Connector__perf_label_regex, response[i][2]):
                lables.append(m.group(1))

            result[response[i][0]] = {'command': response[i][1].split('!')[0], 'perf_labels': lables}

        return result

    def get_services(self):
        response = self._make_request(query='GET services\nColumns: host_host_name display_name check_command perf_data\n')
        result = {}
        for i in range(len(response)):
            host_name = response[i][0]
            sevice_name = response[i][1]
            if host_name not in result:
                result[host_name] = {}
            lables = []
            for m in re.finditer(self._Connector__perf_label_regex, response[i][3]):
                lables.append(m.group(1))

            result[host_name][sevice_name] = {'command': response[i][2].split('!')[0], 'perf_labels': lables}

        return result

    def get_host_services(self, hostcheck_alias='hostcheck'):
        hosts = self.get_hosts()
        services = self.get_services()
        for h, v in hosts.items():
            if h not in services:
                services[h] = {}
            services[h][hostcheck_alias] = v

        return services
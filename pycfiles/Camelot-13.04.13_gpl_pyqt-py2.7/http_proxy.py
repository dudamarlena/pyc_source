# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/test/http_proxy.py
# Compiled at: 2013-04-11 17:47:52
import sys, base64
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QString
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtNetwork import QTcpSocket
from PyQt4.QtNetwork import QTcpServer
from PyQt4.QtNetwork import QHostAddress
from PyQt4.QtNetwork import QHttpRequestHeader
from PyQt4.QtNetwork import QNetworkProxy
from PyQt4.QtNetwork import QNetworkRequest
from PyQt4.QtNetwork import QNetworkAccessManager

class HTTPProxy(QObject):
    debug = True
    log = sys.stderr
    username = 'username'
    password = 'password'
    stopServing = pyqtSlot()

    def __init__(self, parent=None):
        super(HTTPProxy, self).__init__(parent)
        self.proxy_server = QTcpServer(self)
        self.proxy_server.listen(QHostAddress.Any, 8000)
        self.proxy_server.newConnection.connect(self.manage_request)
        if self.debug:
            self.log.write('Proxy server running on 0.0.0.0 port %s\n\n' % self.port())

    def port(self):
        return self.proxy_server.serverPort()

    def addr(self):
        return self.proxy_server.serverAddress().toString()

    def stopServing(self):
        if self.debug:
            self.log.write('Service is stopping...\n\n')
        self.proxy_server.close()
        if self.proxy_server.hasPendingConnections():
            socket = self.proxy_server.nextPendingConnection()
            while socket:
                socket.abort()
                socket = self.proxy_server.nextPendingConnection()

    def manage_request(self):
        proxy_server = self.sender()
        socket = proxy_server.nextPendingConnection()
        socket.readyRead.connect(self.process_request)
        socket.disconnected.connect(socket.deleteLater)

    def authorize_request(self, request_data):
        return True
        header = QHttpRequestHeader(QString(request_data))
        if self.debug:
            self.log.write(header.toString())
        auth = header.value('Proxy-Authorization')
        if not auth:
            return False
        challenge = base64.b64encode(self.username + ':' + self.password)
        return challenge == str(auth).split()[1]

    def process_request(self):
        socket = self.sender()
        request_data = socket.readAll()
        if not self.authorize_request(request_data):
            socket.write('HTTP/1.1 407 Proxy Authentication Required\r\n')
            if self.debug:
                self.log.write('407 Proxy Authentication Required\n\n')
            socket.write('Proxy-Authenticate: Basic realm="test"\r\n')
            socket.write('\r\n')
            socket.disconnectFromHost()
            return
        start = request_data.indexOf('Proxy-Authorization:')
        end = request_data.lastIndexOf('\r\n')
        request_data.remove(start, end)
        request_data.append('\r\n')
        pos = request_data.indexOf('\r\n')
        request_line = request_data.left(pos)
        request_data.remove(0, pos + 2)
        entries = request_line.split(' ')
        method = entries[0]
        address = entries[1]
        version = entries[2]
        port = '80'
        if address.count(':') > 1:
            protocol, host, port = address.split(':')
        else:
            protocol, host = address.split(':')
        print 'address', address
        url = QUrl.fromEncoded(address)
        if not url.isValid():
            if self.debug:
                self.log.write('Invalid URL: %s\n\n', url)
            socket.disconnectFromHost()
            return
        host = url.host()
        port = 80 if url.port() < 0 else url.port()
        req = url.encodedPath()
        if url.hasQuery():
            req.append('?').append(url.encodedQuery())
        request_line = method + ' ' + req + ' ' + version + '\r\n'
        request_data.prepend(request_line)
        if self.debug:
            self.log.write(method + ' ' + address + ' ' + version + '\n\n')
        key = host + ':' + QString.number(port)
        proxy_socket = socket.findChild(QTcpSocket, key)
        if proxy_socket:
            proxy_socket.setObjectName(key)
            proxy_socket.setProperty('url', url)
            proxy_socket.setProperty('request_data', request_data)
            proxy_socket.write(request_data)
        else:
            proxy_socket = QTcpSocket(socket)
            proxy_socket.setObjectName(key)
            proxy_socket.setProperty('url', url)
            proxy_socket.setProperty('request_data', request_data)
            proxy_socket.connected.connect(self.send_request)
            proxy_socket.readyRead.connect(self.transfer_data)
            proxy_socket.disconnected.connect(self.close_connection)
            proxy_socket.error.connect(self.close_connection)
            proxy_socket.connectToHost(host, port)

    def send_request(self):
        proxy_socket = self.sender()
        request_data = proxy_socket.property('request_data').toByteArray()
        proxy_socket.write(request_data)

    def transfer_data(self):
        proxy_socket = self.sender()
        socket = proxy_socket.parent()
        socket.write(proxy_socket.readAll())

    def close_connection(self):
        proxy_socket = self.sender()
        if proxy_socket:
            socket = proxy_socket.parent()
            if isinstance(socket, QTcpSocket) and socket:
                socket.disconnectFromHost()
            if proxy_socket.error() != QTcpSocket.RemoteHostClosedError:
                url = proxy_socket.property('url').toUrl()
                error_string = proxy_socket.errorString()
                if self.debug:
                    self.log.write('Error for %s %s\n\n' % (url, error_string))
            proxy_socket.deleteLater()


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    server = HTTPProxy()
    manager = QNetworkAccessManager()
    manager.finished.connect(server.stopServing)
    manager.finished.connect(app.quit)
    proxy = QNetworkProxy()
    proxy.setType(QNetworkProxy.HttpProxy)
    proxy.setHostName('127.0.0.1')
    proxy.setPort(server.port())
    proxy.setUser(server.username)
    proxy.setPassword(server.password)
    manager.setProxy(proxy)
    reply = manager.get(QNetworkRequest(QUrl('http://aws.amazon.com/')))
    sys.exit(app.exec_())
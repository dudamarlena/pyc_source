# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/upnpsoap.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import urllib3

class UpnpSoap:

    @staticmethod
    def extractSingleTag(self, data, tag):
        startTag = b'<%s' % tag
        endTag = b'</%s>' % tag
        try:
            tmp = data.split(startTag)[1]
            index = tmp.find(b'>')
            if index != -1:
                index += 1
                return tmp[index:].split(endTag)[0].strip()
        except:
            pass

        return

    @staticmethod
    def send(host_name, service_type, control_url, action_name, action_arguments):
        if b'://' in control_url:
            urls = control_url.split(b'/', 3)
            if len(urls) < 4:
                control_url = b'/'
            else:
                control_url = b'/' + urls[3]
        request = b'POST %s HTTP/1.1\r\n' % control_url
        if b':' in host_name:
            host_names = host_name.split(b':')
            host = host_names[0]
            try:
                port = int(host_names[1])
            except:
                print (
                 b'Invalid port specified for host connection:', host_name[1])
                return False

        else:
            host = host_name
            port = 80
        argList = b''
        for arg, (val, dt) in action_arguments.items():
            argList += b'<%s>%s</%s>' % (arg, val, arg)

        body = b'<?xml version="1.0"?>\n<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n<SOAP-ENV:Body>\n<m:%s xmlns:m="%s">\n%s\n</m:%s>\n</SOAP-ENV:Body>\n</SOAP-ENV:Envelope>\n' % (
         action_name, service_type, argList, action_name)
        headers = {b'Host': host_name, 
           b'Content-Length': len(body.encode(b'ascii')), 
           b'Content-Type': b'text/xml', 
           b'SOAPAction': b'"%s#%s"' % (service_type, action_name)}
        for head, value in headers.items():
            request += b'%s: %s\r\n' % (head, value)

        request += b'\r\n%s' % body
        soap_envelope_end = re.compile(b'<\\/.*:envelope>')
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host, port))
            sock.send(request.encode(b'ascii'))
            response = b''
            while True:
                data = sock.recv(8192)
                if not data:
                    break
                else:
                    response += data.decode(b'UTF-8')
                    if soap_envelope_end.search(response.lower()) is not None:
                        break

            sock.close()
            header, body = response.split(b'\r\n\r\n', 1)
            if not header.upper().startswith(b'HTTP/1.') and b' 200 ' in header.split(b'\r\n')[0]:
                print (
                 b'SOAP request failed with error code:', header.split(b'\r\n')[0].split(b' ', 1)[1])
                return False
            return body
        except Exception as e:
            print (
             b'UpnpSoap.send: Caught socket exception:', e)
            sock.close()
            return False
        except KeyboardInterrupt:
            sock.close()
            return False

        return

    @staticmethod
    def get(url):
        headers = {b'CONTENT-TYPE': b'text/xml; charset="utf-8"', 
           b'USER-AGENT': b'uPNP/1.0'}
        try:
            timeout = urllib3.util.timeout.Timeout(connect=2.0, read=7.0)
            http = urllib3.PoolManager(timeout=timeout)
            r = http.request(b'GET', url, headers=headers)
            return (r.status, r.data)
        except Exception as e:
            print b"Request for '%s' failed: %s" % (url, e)
            return (False, False)
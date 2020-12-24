# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ckip/__init__.py
# Compiled at: 2016-11-30 03:04:19
import re, select, socket, xml.etree.cElementTree as ET
DEFAULT_SERVER_ADDR = ('140.109.19.104', 1501)
_BUFSIZE = 8192

class CKIP(object):

    def __init__(self, username, password, server_addr=None):
        self._username = username
        self._password = password
        self._server_addr = server_addr or DEFAULT_SERVER_ADDR
        if username is None or password is None:
            raise RuntimeError('login credential must be set')
        return

    def Segment(self, text):
        """Segment text with CKIP API.

        Args:
            text: Chinese in utf-8 or unicode

        Return:
            a list of list of tuples, where each list item represents a
            sentence and each tuple having the format of (term, POS).
        """
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8')
        root = ET.Element('wordsegmentation', version='1.0')
        ET.SubElement(root, 'option', version='1.0')
        ET.SubElement(root, 'authentication', username=self._username, password=self._password)
        text_node = ET.SubElement(root, 'text')
        text_node.text = text
        request = ET.tostring(root, encoding='big5')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self._server_addr)
        s.send(request)
        response = s.recv(len(text) * 10 + _BUFSIZE)
        with open('test.txt', 'w') as (f):
            f.write(response)
        response = response.decode('big5').encode('utf8')
        root = ET.fromstring(response)
        status = root.find('./processstatus')
        if status.attrib['code'] == '3':
            raise RuntimeError(status.text)
        else:
            if status.attrib['code'] != '0':
                raise RuntimeError('unknown error: code %s: %s' % (
                 status.attrib['code'], status.text))
            result = []
            for sentence in root.findall('./result/sentence'):
                sen = []
                for pair in sentence.text.split('\u3000'):
                    if pair:
                        m = re.match('(.*)\\((.*)\\)', pair)
                        term, pos = m.groups()
                        sen.append((term, str(pos)))

                result.append(sen)

        return result
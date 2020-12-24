# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/resteve/virtualenv/nan38mifarma/python-seur/seur/api.py
# Compiled at: 2016-11-18 09:21:51
from xml.dom.minidom import parseString
import urllib2, socket, os, genshi, genshi.template
loader = genshi.template.TemplateLoader(os.path.join(os.path.dirname(__file__), 'template'), auto_reload=True)

class API(object):
    """
    Generic API to connect to seur
    """
    __slots__ = ('url', 'username', 'password', 'vat', 'franchise', 'seurid', 'ci',
                 'ccc', 'timeout', 'context')

    def __init__(self, username, password, vat, franchise, seurid, ci, ccc, timeout=None, context={}):
        """
        This is the Base API class which other APIs have to subclass. By
        default the inherited classes also get the properties of this
        class which will allow the use of the API with the `with` statement

        Example usage ::

            from seur.api import API

            with API(username, password, vat, franchise, seurid, ci, ccc) as seur_api:
                return seur_api.test_connection()

        :param username: API username of the Seur Web Services.
        :param password: API password of the Seur Web Services.
        :param vat: company vat
        :param franchise: franchise code
        :param seurid: identification description
        :param ci: franchise code
        :param ccc: identification description
        :param timeout: int number of seconds to lost connection
        """
        self.username = username
        self.password = password
        self.vat = vat
        self.franchise = franchise
        self.seurid = seurid
        self.ci = ci
        self.ccc = ccc
        self.timeout = timeout
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def connect(self, url, xml):
        """
        Connect to the Webservices and return XML data from seur

        :param url: url service.
        :param xml: XML data.
        
        Return XML object
        """
        headers = {}
        request = urllib2.Request(url, xml, headers)
        try:
            response = urllib2.urlopen(request, timeout=self.timeout)
            return response.read()
        except socket.timeout as err:
            return
        except socket.error as err:
            return

    def test_connection(self):
        """
        Test connection to Seur webservices
        Send XML to Seur and return error send data
        """
        tmpl = loader.load('test_connection.xml')
        vals = {'username': self.username, 
           'password': self.password, 
           'vat': self.vat, 
           'franchise': self.franchise, 
           'seurid': self.seurid}
        url = 'http://cit.seur.com/CIT-war/services/ImprimirECBWebService'
        xml = tmpl.generate(**vals).render()
        result = self.connect(url, xml)
        if not result:
            return 'timed out'
        dom = parseString(result)
        message = dom.getElementsByTagName('mensaje')
        if message:
            msg = message[0].firstChild.data
            if msg == 'ERROR':
                return 'Connection successfully'
            return msg
        return 'Not found message attribute from %s XML' % method
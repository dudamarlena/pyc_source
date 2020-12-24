# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\sms\core.py
# Compiled at: 2019-11-20 19:36:07
import urllib, urllib2, json, textwrap, time

class SMSMasivo(dict):
    """ Objeto para enviar sms. """

    def __init__(self, apikey, pruebas=False):
        self.apikey = apikey
        self.pruebas = pruebas

    def split_messages(self, message):
        """separa un mensaje largo en varios indicando el numero de mensaje en el mensaje. """
        mensajes_split = textwrap.wrap(message, 156)
        total = len(mensajes_split)
        messages = []
        for index, message in enumerate(mensajes_split):
            count = index + 1
            message += (' {0}/{1}').format(count, total)
            messages.append(message)

        return messages

    def send_unique(self, mensaje, telefono, numregion, voz):
        parametros_dic = {'apikey': self.apikey, 'mensaje': mensaje, 'numcelular': telefono, 'numregion': numregion}
        if self.pruebas:
            parametros_dic['sandbox'] = 1
        if voz:
            parametros_dic['voz'] = 1
        parametros = urllib.urlencode(parametros_dic)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
           'Accept-Encoding': 'none', 
           'Accept-Language': 'en-US,en;q=0.8', 
           'Connection': 'keep-alive'}
        request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.envio.sms.php', parametros, headers)
        opener = urllib2.build_opener()
        respuesta = opener.open(request_sms).read()
        print mensaje
        return json.loads(respuesta)

    def send(self, mensaje, telefono, numregion=52, voz=False):
        """
        enviar mensaje multiple si se pasa de 160 caracteres
        """
        if len(mensaje) > 160:
            messages = self.split_messages(mensaje)
            for message in messages:
                self.send_unique(message, telefono, numregion, voz)
                time.sleep(1)

        else:
            return self.send_unique(mensaje, telefono, numregion, voz)

    def multisend(self, mensaje, telefono, numregion=52):
        parametros_dic = {'apikey': self.apikey, 'mensaje': mensaje, 'numcelular': telefono, 'numregion': numregion}
        if self.pruebas:
            parametros_dic['sandbox'] = 1
        parametros = urllib.urlencode(parametros_dic)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
           'Accept-Encoding': 'none', 
           'Accept-Language': 'en-US,en;q=0.8', 
           'Connection': 'keep-alive'}
        request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.multienvio.sms.php', parametros, headers)
        opener = urllib2.build_opener()
        respuesta = opener.open(request_sms).read()
        return json.loads(respuesta)

    def credito(self):
        parametros = urllib.urlencode({'apikey': self.apikey})
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
           'Accept-Encoding': 'none', 
           'Accept-Language': 'en-US,en;q=0.8', 
           'Connection': 'keep-alive'}
        request_sms = urllib2.Request('https://app.smsmasivos.com.mx/components/api/api.credito.php', parametros, headers)
        opener = urllib2.build_opener()
        respuesta = opener.open(request_sms).read()
        return json.loads(respuesta)
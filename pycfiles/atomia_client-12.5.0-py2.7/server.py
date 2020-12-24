# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\atomia_client\pysimplesoap_atomia\server.py
# Compiled at: 2011-12-13 07:14:29
"""Simple SOAP Server implementation"""
__author__ = 'Mariano Reingart (reingart@gmail.com)'
__copyright__ = 'Copyright (C) 2010 Mariano Reingart'
__license__ = 'LGPL 3.0'
__version__ = '1.02c'
from simplexml import SimpleXMLElement, TYPE_MAP, DateTime, Date, Decimal
DEBUG = False

class SoapDispatcher(object):
    """Simple Dispatcher for SOAP Server"""

    def __init__(self, name, documentation='', action='', location='', namespace=None, prefix=False, soap_uri='http://schemas.xmlsoap.org/soap/envelope/', soap_ns='soap', **kwargs):
        self.methods = {}
        self.name = name
        self.documentation = documentation
        self.action = action
        self.location = location
        self.namespace = namespace
        self.prefix = prefix
        self.soap_ns = soap_ns
        self.soap_uri = soap_uri

    def register_function(self, name, fn, returns=None, args=None, doc=None):
        self.methods[name] = (fn, returns, args, doc or getattr(fn, '__doc__', ''))

    def dispatch(self, xml, action=None):
        """Receive and proccess SOAP call"""
        prefix = self.prefix
        ret = fault = None
        soap_ns, soap_uri = self.soap_ns, self.soap_uri
        soap_fault_code = 'VersionMismatch'
        try:
            request = SimpleXMLElement(xml, namespace=self.namespace)
            for k, v in request[:]:
                if v in ('http://schemas.xmlsoap.org/soap/envelope/', 'http://www.w3.org/2003/05/soap-env'):
                    soap_ns = request.attributes()[k].localName
                    soap_uri = request.attributes()[k].value

            soap_fault_code = 'Client'
            method = request('Body', ns=soap_uri).children()(0)
            if action:
                name = action[len(self.action) + 1:-1]
                prefix = self.prefix
            if not action or not name:
                name = method.get_local_name()
                prefix = method.get_prefix()
            if DEBUG:
                print 'dispatch method', name
            function, returns_types, args_types, doc = self.methods[name]
            if args_types:
                args = method.children().unmarshall(args_types)
            elif args_types is None:
                args = {'request': method}
            else:
                args = {}
            soap_fault_code = 'Server'
            ret = function(**args)
            if DEBUG:
                print ret
        except Exception as e:
            import sys
            etype, evalue, etb = sys.exc_info()
            if DEBUG:
                import traceback
                detail = ('').join(traceback.format_exception(etype, evalue, etb))
                detail += '\n\nXML REQUEST\n\n' + xml
            else:
                detail = None
            fault = {'faultcode': '%s.%s' % (soap_fault_code, etype.__name__), 'faultstring': unicode(evalue), 'detail': detail}

        if not prefix:
            xml = '<%(soap_ns)s:Envelope xmlns:%(soap_ns)s="%(soap_uri)s"/>'
        else:
            xml = '<%(soap_ns)s:Envelope xmlns:%(soap_ns)s="%(soap_uri)s"\n                       xmlns:%(prefix)s="%(namespace)s"/>'
        xml = xml % {'namespace': self.namespace, 'prefix': prefix, 'soap_ns': soap_ns, 
           'soap_uri': soap_uri}
        response = SimpleXMLElement(xml, namespace=self.namespace, prefix=prefix)
        response['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
        response['xmlns:xsd'] = 'http://www.w3.org/2001/XMLSchema'
        body = response.add_child('%s:Body' % soap_ns, ns=False)
        if fault:
            body.marshall('%s:Fault' % soap_ns, fault, ns=False)
        else:
            res = body.add_child('%sResponse' % name, ns=prefix)
            if not prefix:
                res['xmlns'] = self.namespace
            if returns_types:
                if not isinstance(ret, dict):
                    res.marshall(returns_types.keys()[0], ret)
                else:
                    for k, v in ret.items():
                        res.marshall(k, v)

            elif returns_types is None:
                res.import_node(ret)
        return response.as_xml()

    def list_methods(self):
        """Return a list of aregistered operations"""
        return [ (method, doc) for method, (function, returns, args, doc) in self.methods.items() ]

    def help(self, method=None):
        """Generate sample request and response messages"""
        function, returns, args, doc = self.methods[method]
        xml = '\n<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n<soap:Body><%(method)s xmlns="%(namespace)s"/></soap:Body>\n</soap:Envelope>' % {'method': method, 'namespace': self.namespace}
        request = SimpleXMLElement(xml, namespace=self.namespace, prefix=self.prefix)
        if args:
            items = args.items()
        else:
            if args is None:
                items = [
                 ('value', None)]
            else:
                items = []
            for k, v in items:
                request(method).marshall(k, v, add_comments=True, ns=False)

            xml = '\n<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n<soap:Body><%(method)sResponse xmlns="%(namespace)s"/></soap:Body>\n</soap:Envelope>' % {'method': method, 'namespace': self.namespace}
            response = SimpleXMLElement(xml, namespace=self.namespace, prefix=self.prefix)
            if returns:
                items = returns.items()
            elif args is None:
                items = [
                 ('value', None)]
            else:
                items = []
            for k, v in items:
                response('%sResponse' % method).marshall(k, v, add_comments=True, ns=False)

        return (
         request.as_xml(pretty=True), response.as_xml(pretty=True), doc)

    def wsdl(self):
        """Generate Web Service Description v1.1"""
        xml = '<?xml version="1.0"?>\n<wsdl:definitions name="%(name)s" \n          targetNamespace="%(namespace)s"\n          xmlns:tns="%(namespace)s"\n          xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"\n          xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"\n          xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n    <wsdl:documentation xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">%(documentation)s</wsdl:documentation>\n\n    <wsdl:types>\n       <xsd:schema targetNamespace="%(namespace)s"\n              elementFormDefault="qualified"\n              xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n       </xsd:schema>\n    </wsdl:types>\n\n</wsdl:definitions>\n' % {'namespace': self.namespace, 'name': self.name, 'documentation': self.documentation}
        wsdl = SimpleXMLElement(xml)
        for method, (function, returns, args, doc) in self.methods.items():

            def parse_element(name, values, array=False, complex=False):
                if not complex:
                    element = wsdl('wsdl:types')('xsd:schema').add_child('xsd:element')
                    complex = element.add_child('xsd:complexType')
                else:
                    complex = wsdl('wsdl:types')('xsd:schema').add_child('xsd:complexType')
                    element = complex
                element['name'] = name
                if values:
                    items = values
                elif values is None:
                    items = [
                     ('value', None)]
                else:
                    items = []
                if not array and items:
                    all = complex.add_child('xsd:all')
                else:
                    if items:
                        all = complex.add_child('xsd:sequence')
                    for k, v in items:
                        e = all.add_child('xsd:element')
                        e['name'] = k
                        if array:
                            e[:] = {'minOccurs': '0', 'maxOccurs': 'unbounded'}
                        if v in TYPE_MAP.keys():
                            t = 'xsd:%s' % TYPE_MAP[v]
                        elif v is None:
                            t = 'xsd:anyType'
                        elif isinstance(v, list):
                            n = 'ArrayOf%s%s' % (name, k)
                            l = []
                            for d in v:
                                l.extend(d.items())

                            parse_element(n, l, array=True, complex=True)
                            t = 'tns:%s' % n
                        elif isinstance(v, dict):
                            n = '%s%s' % (name, k)
                            parse_element(n, v.items(), complex=True)
                            t = 'tns:%s' % n
                        e.add_attribute('type', t)

                return

            parse_element('%s' % method, args and args.items())
            parse_element('%sResponse' % method, returns and returns.items())
            for m, e in (('Input', ''), ('Output', 'Response')):
                message = wsdl.add_child('wsdl:message')
                message['name'] = '%s%s' % (method, m)
                part = message.add_child('wsdl:part')
                part[:] = {'name': 'parameters', 'element': 'tns:%s%s' % (method, e)}

        portType = wsdl.add_child('wsdl:portType')
        portType['name'] = '%sPortType' % self.name
        for method, (function, returns, args, doc) in self.methods.items():
            op = portType.add_child('wsdl:operation')
            op['name'] = method
            if doc:
                op.add_child('wsdl:documentation', doc)
            input = op.add_child('wsdl:input')
            input['message'] = 'tns:%sInput' % method
            output = op.add_child('wsdl:output')
            output['message'] = 'tns:%sOutput' % method

        binding = wsdl.add_child('wsdl:binding')
        binding['name'] = '%sBinding' % self.name
        binding['type'] = 'tns:%sPortType' % self.name
        soapbinding = binding.add_child('soap:binding')
        soapbinding['style'] = 'document'
        soapbinding['transport'] = 'http://schemas.xmlsoap.org/soap/http'
        for method in self.methods.keys():
            op = binding.add_child('wsdl:operation')
            op['name'] = method
            soapop = op.add_child('soap:operation')
            soapop['soapAction'] = self.action + method
            soapop['style'] = 'document'
            input = op.add_child('wsdl:input')
            soapbody = input.add_child('soap:body')
            soapbody['use'] = 'literal'
            output = op.add_child('wsdl:output')
            soapbody = output.add_child('soap:body')
            soapbody['use'] = 'literal'

        service = wsdl.add_child('wsdl:service')
        service['name'] = '%sService' % self.name
        service.add_child('wsdl:documentation', text=self.documentation)
        port = service.add_child('wsdl:port')
        port['name'] = '%s' % self.name
        port['binding'] = 'tns:%sBinding' % self.name
        soapaddress = port.add_child('soap:address')
        soapaddress['location'] = self.location
        return wsdl.as_xml(pretty=True)


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class SOAPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """User viewable help information and wsdl"""
        args = self.path[1:].split('?')
        print 'serving', args
        if self.path != '/' and args[0] not in self.server.dispatcher.methods.keys():
            self.send_error(404, 'Method not found: %s' % args[0])
        else:
            if self.path == '/':
                response = self.server.dispatcher.wsdl()
            else:
                req, res, doc = self.server.dispatcher.help(args[0])
                if len(args) == 1 or args[1] == 'request':
                    response = req
                else:
                    response = res
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            self.wfile.write(response)

    def do_POST(self):
        """SOAP POST gateway"""
        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        request = self.rfile.read(int(self.headers.getheader('content-length')))
        response = self.server.dispatcher.dispatch(request)
        self.wfile.write(response)


if __name__ == '__main__':
    import sys
    dispatcher = SoapDispatcher(name='PySimpleSoapSample', location='http://localhost:8008/', action='http://localhost:8008/', namespace='http://example.com/pysimplesoapsamle/', prefix='ns0', documentation='Example soap service using PySimpleSoap', trace=True, ns=True)

    def adder(p, c, dt=None):
        """Add several values"""
        print c[0]['d'], c[1]['d'],
        import datetime
        dt = dt + datetime.timedelta(365)
        return {'ab': p['a'] + p['b'], 'dd': c[0]['d'] + c[1]['d'], 'dt': dt}


    def dummy(in0):
        """Just return input"""
        return in0


    def echo(request):
        """Copy request->response (generic, any type)"""
        return request.value


    dispatcher.register_function('Adder', adder, returns={'AddResult': {'ab': int, 'dd': str}}, args={'p': {'a': int, 'b': int}, 'dt': Date, 'c': [{'d': Decimal}]})
    dispatcher.register_function('Dummy', dummy, returns={'out0': str}, args={'in0': str})
    dispatcher.register_function('Echo', echo)
    if '--local' in sys.argv:
        wsdl = dispatcher.wsdl()
        print wsdl
        open('C:/test.wsdl', 'w').write(wsdl)
        xml = '<?xml version="1.0" encoding="UTF-8"?> \n    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n       <soap:Body>\n         <Adder xmlns="http://example.com/sample.wsdl">\n           <p><a>1</a><b>2</b></p><c><d>5000000.1</d><d>.2</d></c><dt>20100724</dt>\n        </Adder>\n       </soap:Body>\n    </soap:Envelope>'
        print dispatcher.dispatch(xml)
        xml = '\n<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pys="http://example.com/pysimplesoapsamle/">\n   <soapenv:Header/>\n   <soapenv:Body>\n      <pys:Adder>\n         <pys:p><pys:a>9</pys:a><pys:b>3</pys:b></pys:p>\n         <pys:dt>19690720<!--1969-07-20T21:28:00--></pys:dt>\n         <pys:c><pys:d>10.001</pys:d><pys:d>5.02</pys:d></pys:c>\n      </pys:Adder>\n   </soapenv:Body>\n</soapenv:Envelope>\n    '
        print dispatcher.dispatch(xml)
        xml = '<?xml version="1.0" encoding="UTF-8"?> \n    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"\n                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n                   xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n       <soap:Body>\n         <Echo xmlns="http://example.com/sample.wsdl">\n           <value xsi:type="xsd:string">Hello world</value>\n        </Echo>\n       </soap:Body>\n    </soap:Envelope>'
        print dispatcher.dispatch(xml)
        for method, doc in dispatcher.list_methods():
            request, response, doc = dispatcher.help(method)

    if '--serve' in sys.argv:
        print 'Starting server...'
        httpd = HTTPServer(('', 8008), SOAPHandler)
        httpd.dispatcher = dispatcher
        httpd.serve_forever()
    if '--consume' in sys.argv:
        from client import SoapClient
        client = SoapClient(location='http://localhost:8008/', action='http://localhost:8008/', namespace='http://example.com/sample.wsdl', soap_ns='soap', trace=True, ns=False)
        response = client.Adder(p={'a': 1, 'b': 2}, dt='20100724', c=[{'d': '1.20'}, {'d': '2.01'}])
        result = response.AddResult
        print int(result.ab)
        print str(result.dd)
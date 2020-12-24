# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgwebservices/tests/test_xml.py
# Compiled at: 2010-06-21 06:05:22
"""Tests for HTTP+XML services"""
import cStringIO as StringIO, cherrypy
from turbogears import testutil
import base64
try:
    from xml.etree import cElementTree as et
except ImportError:
    import cElementTree as et

from tgwebservices.tests.fixtures import *

def test_simple():
    cherrypy.root = MyService('http://foo.bar.baz')
    testutil.create_request('/times2?value=5')
    print cherrypy.response.headers['Content-Type']
    assert cherrypy.response.headers['Content-Type'] == 'text/xml; charset=utf-8'
    output = cherrypy.response.body[0]
    print output
    assert output == '<result>10</result>'


def test_xml_error():
    testutil.create_request('/times2?value=5&foo=1')
    output = cherrypy.response.body[0]
    print output
    assert output == "<result><faultcode>Client</faultcode><faultstring>foo is not a valid parameter (valid values are: ['value'])</faultstring></result>"


def test_complex_input():
    cherrypy.root = ComplexService('http://foo.bar.baz/')
    request = '<request>\n    <person><name>Fred</name><age>22</age></person>\n</request>'
    testutil.create_request('/tenyearsolder', rfile=StringIO.StringIO(request), method='POST', headers={'Content-Length': str(len(request)), 'Content-Type': 'text/xml; charset=utf-8'})
    print cherrypy.response.headers['Content-Type']
    assert cherrypy.response.headers['Content-Type'] == 'text/xml; charset=utf-8'
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><age>32</age><computed>Hello!</computed><name>Fred</name></result>'


def test_complex_input_on_get():
    cherrypy.root = ComplexService('http://foo.bar.baz/')
    request = '<request><person><name>Fred</name><age>22</age></person></request>'
    testutil.create_request('/tenyearsolder?tg_format=xml&_xml_request=%s' % request)
    print cherrypy.response.headers['Content-Type']
    assert cherrypy.response.headers['Content-Type'] == 'text/xml; charset=utf-8'
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><age>32</age><computed>Hello!</computed><name>Fred</name></result>'


def test_complex_params():
    cherrypy.root = ComplexService('http://foo.bar.baz/')
    person = '<person><name>Fred</name><age>22</age></person>\n'
    testutil.create_request('/tenyearsolder?tg_format=xml&person=%s' % person)
    print cherrypy.response.headers['Content-Type']
    assert cherrypy.response.headers['Content-Type'] == 'text/xml; charset=utf-8'
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><age>32</age><computed>Hello!</computed><name>Fred</name></result>'


def test_rwproperty():
    cherrypy.root = ComplexService('http://foo.bar.baz/')
    request = '<request>\n    <rwp><value>AValue</value></rwp>\n</request>'
    testutil.create_request('/getandsetrwprop', rfile=StringIO.StringIO(request), method='POST', headers={'Content-Length': str(len(request)), 'Content-Type': 'text/xml; charset=utf-8'})
    print cherrypy.response.headers['Content-Type']
    assert cherrypy.response.headers['Content-Type'] == 'text/xml; charset=utf-8'
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><value>AValue</value></result>'


def test_datetime():
    cherrypy.root = DateTimeService('http://foo.bar.baz/')
    request = '<request><d>2009-07-25</d><t>22:14:53.89654242</t></request>'
    testutil.create_request('/combine?tg_format=xml&_xml_request=%s' % request)
    output = cherrypy.response.body[0]
    print output
    assert output == '<result>2009-07-25T22:14:53.896542</result>'
    request = '<request><dt>2009-07-25T22:14:53.89654242</dt></request>'
    testutil.create_request('/split?tg_format=xml&_xml_request=%s' % request)
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><d>2009-07-25</d><t>22:14:53.896542</t></result>'


def test_binary():
    data = b'\xc2\xc3\xc4'
    cherrypy.root = BinaryService('http://foo.bar.baz/')
    request = '<request><data>%s</data></request>' % base64.encodestring(data)
    print request
    testutil.create_request('/reverse', rfile=StringIO.StringIO(request), method='POST', headers={'Content-Length': str(len(request)), 'Content-Type': 'text/xml; charset=utf-8'})
    output = cherrypy.response.body[0]
    print output
    r = et.fromstring(output)
    rdata = base64.decodestring(r.text)
    assert data == rdata[::-1]


def test_null():
    cherrypy.root = ComplexService('http://foo.bar.baz/')
    request = '<request><rwp><value nil="true"/></rwp></request>'
    testutil.create_request('/getandsetrwprop', rfile=StringIO.StringIO(request), method='POST', headers={'Content-Length': str(len(request)), 'Content-Type': 'text/xml; charset=utf-8', 
       'Accept': 'text/xml'})
    output = cherrypy.response.body[0]
    print output
    assert output == '<result><value nil="true"/></result>'
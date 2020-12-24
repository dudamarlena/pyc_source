# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_xmlparser.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import XMLParser
from insights.tests import context_wrap

class FakeXmlParserClass(XMLParser):

    def parse_dom(self):
        xmlns = 'http://people.example.com'
        keyword = '*{%s}%s' % (xmlns, 'neighbor[2]')
        tmo_dict = {}
        for n in self.dom.findall(keyword):
            tmo_dict = {n.get('name'): n.get('direction')}

        return tmo_dict

    @property
    def get_neighbors(self):
        return self.get_elements('./country/neighbor')


testdata = ('\n<?xml version="1.0"?>\n<data xmlns:fictional="http://characters.example.com"\n       xmlns="http://people.example.com">\n    <country name="Liechtenstein">\n        <rank updated="yes">2</rank>\n        <year>2008</year>\n        <gdppc>141100</gdppc>\n        <neighbor name="Austria" direction="E"/>\n        <neighbor name="Switzerland" direction="W"/>\n    </country>\n    <country name="Singapore">\n        <rank updated="yes">5</rank>\n        <year>2011</year>\n        <gdppc>59900</gdppc>\n        <neighbor name="Malaysia" direction="N"/>\n    </country>\n    <country name="Panama">\n        <rank>68</rank>\n        <year>2011</year>\n        <gdppc>13600</gdppc>\n        <neighbor name="Costa Rica" direction="W"/>\n    </country>\n</data>\n').strip()

def test_parse():
    ctx = context_wrap(testdata)
    xml = FakeXmlParserClass(ctx)
    assert xml.raw == testdata
    assert len(xml.get_neighbors) == 4
    assert xml.xmlns == 'http://people.example.com'
    assert 'Costa Rica' not in xml
    assert 'Switzerland' in xml
    assert xml.get('Switzerland', '') == 'W'
    assert len(xml.get_elements(".//year/..[@name='Singapore']")) == 1
    assert xml.get_elements(".//*[@name='Singapore']/year")[(-1)].text == '2011'
    assert xml.get_elements('.//neighbor[2]', xmlns='http://people.example.com')[0].get('name') == 'Switzerland'
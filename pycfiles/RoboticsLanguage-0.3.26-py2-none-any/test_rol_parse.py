# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Inputs/RoL/Tests/test_rol_parse.py
# Compiled at: 2019-09-09 15:48:17
import sys, copy, unittest, cloudpickle
from lxml import etree
from RoboticsLanguage.Inputs.RoL import Parse, Language as rol_language
from RoboticsLanguage.Transformers.Base import Language as base_language
from RoboticsLanguage.Base import Utilities, Initialise, CommandLine
with open('/tmp/parameters.pickle', 'rb') as (file):
    parameters = cloudpickle.load(file)

def removePositionAttributes(xml):
    for element in xml.xpath('//*[@p]'):
        element.attrib.pop('p')

    return xml


def check(self, text, result):
    global parameters
    code, __ = Parse.parse(text, parameters)
    self.assertEqual(etree.tostring(removePositionAttributes(code)), result)


class TestRolParse(unittest.TestCase):

    def test_Functional_Composition(self):
        text = "node(print('hello'))"
        result, __ = Parse.parse(text, parameters)
        self.assertEqual(etree.tostring(result), '<node p="20"><print p="19"><string p="18">hello</string></print></node>')
        check(self, "node(print('hello'),print('ok'))", '<node><print><string>hello</string></print><print><string>ok</string></print></node>')
        check(self, "node(print('hello',test:1))", '<node><print><string>hello</string><option name="test"><natural>1</natural></option></print></node>')

    def test_Types(self):
        check(self, 'node(123)', '<node><natural>123</natural></node>')
        check(self, 'node(1.23)', '<node><real>1.23</real></node>')
        check(self, 'node(1.23e10)', '<node><real>1.23e10</real></node>')
        check(self, 'node(1.23e-10)', '<node><real>1.23e-10</real></node>')
        check(self, 'node(.23)', '<node><real>.23</real></node>')
        check(self, 'node(.23e10)', '<node><real>.23e10</real></node>')
        check(self, 'node(.23e-10)', '<node><real>.23e-10</real></node>')
        check(self, 'node(true)', '<node><boolean>true</boolean></node>')
        check(self, 'node(false)', '<node><boolean>false</boolean></node>')
        check(self, "node('hello')", '<node><string>hello</string></node>')

    def test_Infix_Operators(self):
        check(self, 'node(1+2)', '<node><plus><natural>1</natural><natural>2</natural></plus></node>')
        check(self, 'node(1+2*3)', '<node><plus><natural>1</natural><times><natural>2</natural><natural>3</natural></times></plus></node>')
        check(self, 'node((1+2)*3)', '<node><times><plus><natural>1</natural><natural>2</natural></plus><natural>3</natural></times></node>')
        check(self, 'node(1 and 2 + 3 != 4 = 5 >= 6 * 7)', '<node><assign><and><natural>1</natural><notEqual><plus><natural>2</natural><natural>3</natural></plus><natural>4</natural></notEqual></and><largerEqual><natural>5</natural><times><natural>6</natural><natural>7</natural></times></largerEqual></assign></node>')
        check(self, 'node(1 ∧ 2 + 3 ≠ 4 = 5 ≥ 6 * 7)', '<node><assign><and><natural>1</natural><notEqual><plus><natural>2</natural><natural>3</natural></plus><natural>4</natural></notEqual></and><largerEqual><natural>5</natural><times><natural>6</natural><natural>7</natural></times></largerEqual></assign></node>')

    def test_Prefix_Operators(self):
        check(self, 'node(-a)', '<node><negative><variable name="a"/></negative></node>')

    def test_Bracket_Operators(self):
        check(self, 'node([1,{2,3}])', '<node><vector><natural>1</natural><set><natural>2</natural><natural>3</natural></set></vector></node>')

    def test_Custom_Operators(self):
        check(self, 'node(define f(x in Reals)->Reals:print(x+1))', '<node><function_definition name="f"><function_arguments><element><variable name="x"/><Reals/></element></function_arguments><function_returns><Reals/></function_returns><function_content><print><plus><variable name="x"/><natural>1</natural></plus></print></function_content></function_definition></node>')

    def test_Mini_Languages(self):
        check(self, 'node(RoLXML<{ <print><string>hello</string></print> }>)', '<node><print><string>hello</string></print></node>')


if __name__ == '__main__':
    unittest.main()
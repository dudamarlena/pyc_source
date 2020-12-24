# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/tests/test_variable_parser.py
# Compiled at: 2016-08-21 10:24:15
# Size of source mod 2**32: 2736 bytes
import sys
sys.path.append('/home/travis/build/bradwood/BPRC/bprc')
sys.path.append('/home/travis/build/bradwood/BPRC/bprc/tests')
print(sys.path)
import unittest, yaml
from ddt import ddt, data, file_data, unpack
from bprc.variables import Variables
from bprc.varprocessor import VarProcessor
from bprc.utils import *

@ddt
class SimpleTest(unittest.TestCase):

    def setUp(self):
        """Sets up the YAML data."""
        self.yamldata = '\n--- #sample recipe\nvariables:\n  name: brad\n  favourite_colour: red\n  age: 345\n  drinks_beer: true\n  floater: 343.55\n  numjoin: <%!age%>:<%!floater%>\n  multi-way-join: <%!age%>:<%!favourite_colour%> -- <%!age%>:<%!floater%>\n\n  age_and_colour: <%!age%>:<%!favourite_colour%>\n  lorumfile: <%f./examples/lorum.txt%>\n  testnull:\n'

    @unpack
    @data([
     'name', 'brad'], [
     'age', 345], [
     'age_and_colour', '345:red'], [
     'drinks_beer', True], [
     'floater', 343.55], [
     'testnull', None], [
     'numjoin', '345:343.55'], [
     'multi-way-join', '345:red -- 345:343.55'])
    def test_varprocessor_parse_values(self, varname, varval):
        """tests the php-like substitution logic in the recipe steps using various random checks for values"""
        datamap = yaml.load(self.yamldata)
        variables = Variables(datamap['variables'])
        varprocessor = VarProcessor(variables)
        variables[varname] = varprocessor.parse(variables[varname], variables)
        self.assertEquals(variables[varname], varval)

    @unpack
    @data([
     'lorumfile',
     "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\nThis is a new line\nAnd so is this.\n"])
    def test_varprocessor_fileparse_values(self, varname, varval):
        """tests the file substitution logic in the recipe steps using various random checks for values"""
        datamap = yaml.load(self.yamldata)
        variables = Variables(datamap['variables'])
        varprocessor = VarProcessor(variables)
        variables[varname] = varprocessor.fileparse(variables[varname], variables)
        self.assertEquals(variables[varname], varval)
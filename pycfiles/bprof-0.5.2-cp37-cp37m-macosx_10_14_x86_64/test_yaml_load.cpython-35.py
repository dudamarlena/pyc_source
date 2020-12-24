# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/tests/test_yaml_load.py
# Compiled at: 2016-08-21 10:24:23
# Size of source mod 2**32: 7234 bytes
import sys
sys.path.append('/home/travis/build/bradwood/BPRC/bprc')
sys.path.append('/home/travis/build/bradwood/BPRC/bprc/tests')
print(sys.path)
import unittest, yaml
from ddt import ddt, data, file_data, unpack
from bprc.recipe import Recipe, Request, Response, Options, QueryString, Headers, Body
from bprc.utils import *
from bprc._version import __version__

@ddt
class SimpleTest(unittest.TestCase):

    def setUp(self):
        """Sets up the YAML data."""
        with open('tests/yaml_load_test.yml', 'r') as (myfile):
            self.yamldata = myfile.read()
        with open('tests/yaml_no_recipe.yml', 'r') as (myfile):
            self.yamlnorecipe = myfile.read()
        with open('tests/yaml_no_URL.yml', 'r') as (myfile):
            self.yamlnoURL = myfile.read()
        with open('tests/yaml_no_steps.yml', 'r') as (myfile):
            self.yamlnosteps = myfile.read()

    def test_yaml_load(self):
        """tests the yaml loads and is able to instantiate a Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertIsInstance(r, Recipe)

    @unpack
    @data(['steps[0].request.headers["Authorisation"]', 'yadda-step one authorisation header brad'], [
     'steps[0].name', 'Create Kong API'], [
     'steps[0].response.body["id"]', 'this_is_a_param'], [
     'steps[2].options["request.body_format"]', 'json'], [
     'steps[2].options["request.retries"]', 3], [
     'steps[6].request.headers["someheader"]', 'SoMeVaL'], [
     'steps[6].request.headers["SomeHeader"]', 'SoMeVaL'], [
     'steps[6].request.headers["SoMeHeaDer2"]', 50], [
     'steps[6].request.headers["someheader2"]', 50], [
     'steps[6].request.headers["SOMEHEADER2"]', 50])
    def test_yaml_parse_values(self, path_suffix, val):
        """conducts misc value checks on the values passed in from the yaml on the Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertEquals(eval('r.' + path_suffix), val)

    @unpack
    @data(['steps[6].request.headers["someheader"]', 'someval'])
    def test_yaml_parse_values_not_equal(self, path_suffix, val):
        """conducts misc value checks on the values passed in from the yaml on the Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertNotEqual(eval('r.' + path_suffix), val)

    @data('r.steps[1].response.headers["Authorisation"]')
    def test_yaml_parse_nones(self, path_suffix):
        """conducts misc None checks on the values passed in from the yaml on the Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertIsNone(eval(path_suffix))

    @unpack
    @data(['steps[2].request.querystring["qsbool0"]'], [
     'steps[2].request.querystring["qsbool1"]'], [
     'steps[2].request.querystring["qsbool2"]'], [
     'steps[2].request.querystring["qsbool3"]'], [
     'steps[2].request.headers["headerbool0"]'], [
     'steps[2].request.headers["headerbool1"]'], [
     'steps[2].request.headers["headerbool2"]'], [
     'steps[2].request.headers["headerbool3"]'], [
     'steps[2].request.body["bodybool0"]'], [
     'steps[2].request.body["bodybool1"]'], [
     'steps[2].request.body["bodybool2"]'], [
     'steps[2].request.body["bodybool3"]'])
    def test_yaml_true(self, path_suffix):
        """conducts misc Boolean checks on the values passed in from the yaml on the Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertTrue(eval('r.' + path_suffix))

    @unpack
    @data(['steps[2].request.querystring["qsbool0"]', bool], [
     'steps[2].request.querystring["qsint"]', int], [
     'steps[2].request.querystring["qsstring"]', str], [
     'steps[2].request.querystring["qsfloat"]', float], [
     'steps[2].request.headers["headerbool0"]', bool], [
     'steps[2].request.headers["headerint"]', int], [
     'steps[2].request.headers["headerstring"]', str], [
     'steps[2].request.headers["headerfloat"]', float], [
     'steps[2].request.body["bodybool0"]', bool], [
     'steps[2].request.body["bodyint"]', int], [
     'steps[2].request.body["bodystring"]', str], [
     'steps[2].request.body["bodyfloat"]', float], [
     'steps[5].request', Request], [
     'steps[5].response', Response], [
     'steps[3].request', Request], [
     'steps[3].response', Response], [
     'steps[3].options', Options], [
     'steps[2].request.querystring', QueryString], [
     'steps[2].request.headers', Headers], [
     'steps[2].request.body', Body])
    def test_yaml_types(self, path_suffix, type):
        """conducts misc type checks on the values passed in from the yaml on the Recipe object"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertIsInstance(eval('r.' + path_suffix), type)

    def test_yaml_no_recipe(self):
        """conducts checks for a recipe key passed in the YAML"""
        datamap = yaml.safe_load(self.yamlnorecipe)
        self.assertRaises(KeyError, Recipe, datamap)

    def test_yaml_no_URL(self):
        """conducts checks for a URL key passed in the YAML"""
        datamap = yaml.safe_load(self.yamlnoURL)
        self.assertRaises(KeyError, Recipe, datamap)

    def test_yaml_no_steps(self):
        """conducts checks for a steps key passed in the YAML"""
        datamap = yaml.safe_load(self.yamlnosteps)
        self.assertRaises(TypeError, Recipe, datamap)

    @data('r.steps[3].request.headers', 'r.steps[3].request.querystring', 'r.steps[3].request.body', 'r.steps[3].options')
    def test_yaml_check_empty_elements_created(self, emtydata):
        """conducts checks for a steps key passed in the YAML"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertFalse(eval(emtydata))

    @unpack
    @data(['steps[3].httpmethod', 'GET'], [
     'steps[3].name', 'Step: 3'])
    def test_yaml_check_default_step_elements_created(self, path_suffix, val):
        """conducts checks for a steps key passed in the YAML"""
        datamap = yaml.safe_load(self.yamldata)
        r = Recipe(datamap)
        self.assertEquals(eval('r.' + path_suffix), val)


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\dave\Documents\Visual Studio 2013\Projects\clinPy\clinPy\define\define.py
# Compiled at: 2014-01-26 19:57:13
from pandas.io.excel import read_excel
import pandas
from jinja2 import Environment, FileSystemLoader
from lxml import etree
import datetime, os

def missInt(x):
    if not pandas.isnull(x):
        return int(x)
    else:
        return int(-1)


ROOTPATH = os.path.split(__file__)[0]
SCHEMAFILE = os.path.join(ROOTPATH, 'resource', 'define1-0-0.xsd')

class define(object):
    metaDataComponents = [
     'DEFINE_HEADER_METADATA',
     'TOC_METADATA',
     'VARIABLE_METADATA',
     'VALUELEVEL_METADATA',
     'COMPUTATION_METHOD',
     'CODELISTS']
    env = Environment(loader=FileSystemLoader(searchpath=os.path.join(ROOTPATH, 'template')))
    env.globals['merge'] = pandas.merge
    env.globals['pandas'] = pandas
    creationdate = datetime.date.today()
    creationdatetime = datetime.datetime.now()

    def __init__(self, *args, **kwargs):
        self.define = None
        self.schema = etree.XMLSchema(etree.parse(SCHEMAFILE))
        self.templatePath = None
        return

    def __str__(self):
        if self.define is not None:
            return etree.tostring(self.define.getroottree(), pretty_print=True, xml_declaration=True, encoding='utf-8')
        else:
            return

    def __readFromExcel(self, wkbk):
        for x in self.metaDataComponents:
            try:
                setattr(self, x, read_excel(wkbk, x, index_col=None, na_values=[
                 'NA']))
                self.readSuccess = 1
            except IOError as e:
                self.readSuccess = 0
                return

        self.VARIABLE_METADATA['VARNUM'] = [ missInt(x) for x in self.VARIABLE_METADATA['VARNUM'] ]
        self.VARIABLE_METADATA['SIGNIFICANTDIGITS'] = [ missInt(x) for x in self.VARIABLE_METADATA['SIGNIFICANTDIGITS'] ]
        self.VALUELEVEL_METADATA['SIGNIFICANTDIGITS'] = [ missInt(x) for x in self.VALUELEVEL_METADATA['SIGNIFICANTDIGITS'] ]
        return

    def __startDefine(self):
        if not self.readSuccess:
            print 'Must first read in meta data'
            return
        template = self.env.get_template('defineInit.html')
        self.define = template.render(this=self, int=int, globalVariables=[
         'StudyName', 'StudyDescription', 'ProtocolName'], crf='test.pdf')

    def __toXML(self):
        parser = etree.XMLParser(recover=True, encoding='unicode')
        self.define = etree.fromstring(self.define, parser)

    def fromExcel(self, wkbk):
        self.__readFromExcel(wkbk)
        self.__startDefine()
        self.__toXML()

    def loadFromFile(self, filename):
        self.define = etree.parse(filename)

    def validateXML(self):
        self.isXMLValid = self.schema.validate(self.define)

    def writeXML(self, filename):
        with open(filename, 'w') as (F):
            F.write(str(self))


if __name__ == '__main__':
    pass
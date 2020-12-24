# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_csv2xml.py
# Compiled at: 2011-07-15 11:51:54
"""
Created on 3.7.2011

@author: javl
"""
import unittest
from ttr.xml.csv2xml import string2xml, Csv2Xml
import csv, StringIO, xml.etree.cElementTree as ElementTree

class DialectSemicolon(csv.Dialect):
    """Describes properties of my CSV format"""
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE


class Test(unittest.TestCase):

    def setUp(self):
        self.csv_1_string = 'a;b;c\n1;2;3\n11;22;33\n111;222;333'
        self.csv_2_string = 'a,b,c\n1,2,3\n11,22,33\n111,222,333'
        self.buff_1 = StringIO.StringIO(self.csv_1_string)
        self.buff_2 = StringIO.StringIO(self.csv_2_string)

    def tearDown(self):
        pass

    def test_named_registered_dialect(self):
        """Testing how dialect_registration works. Not really testing my code.
        """
        dialect_name = 'ponaszimu'
        csv.register_dialect(dialect_name, delimiter='|', quoting=csv.QUOTE_NONE)
        csv.register_dialect(dialect_name, delimiter=';', quoting=csv.QUOTE_NONE)
        print csv.list_dialects()
        buff = StringIO.StringIO(self.csv_1_string)
        reader = csv.reader(buff, dialect=dialect_name)
        for line in reader:
            print line

    def test_dialect_class(self):
        """Testing dialect as instace of Dialect subclass.
        It is only test of cvs module, not of my own code.
        """
        buff = StringIO.StringIO(self.csv_1_string)
        reader = csv.reader(buff, dialect=DialectSemicolon)
        for line in reader:
            print line

    def test_string2xml(self):
        """testing function string2xml from my own code.
        """
        print string2xml(self.csv_2_string)

    def test_class_csv2xmlstring(self):
        """
        Test of my actual parser class.
        """
        csv_parser = Csv2Xml(self.buff_1, row_num_att='rownum', dialect=DialectSemicolon)
        res = csv_parser.as_string()
        print res

    def test_class_csv2xmlstring_excel_dialect(self):
        """
        Test of my actual parser class.
        """
        csv_parser = Csv2Xml(self.buff_2, row_num_att='rownum', dialect='excel')
        res = csv_parser.as_string()
        print res

    def test_class_csv2element(self):
        """
        Test of my actual parser class.
        """
        csv_parser = Csv2Xml(self.buff_1, row_num_att='rownum', dialect=DialectSemicolon)
        res = csv_parser.as_element()
        result_string = ElementTree.tostring(res, 'UTF-8')
        print result_string

    def test_iterator(self):
        """test use of iterator, returning Elements"""
        csv_parser = Csv2Xml(self.buff_1, row_num_att='rownum', dialect=DialectSemicolon)
        for row in csv_parser:
            print type(row)
            text = ElementTree.tostring(row, 'UTF-8')
            print text


if __name__ == '__main__':
    unittest.main()
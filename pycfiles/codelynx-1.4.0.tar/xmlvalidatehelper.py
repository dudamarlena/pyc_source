# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\XMLFunction\xmlvalidatehelper.py
# Compiled at: 2016-12-22 02:06:40
from lxml import etree
from lxml.etree import DocumentInvalid

def Validate_XSD(xml_filename, xsd_filename):
    xml_file = open(xml_filename)
    xsd_file = open(xsd_filename)
    xml_doc = etree.XML(xml_file.read())
    xsd_doc = etree.XML(xsd_file.read())
    xmlschema = etree.XMLSchema(xsd_doc)
    try:
        try:
            xmlschema.assertValid(xml_doc)
            return (
             True, '')
        except DocumentInvalid as e:
            return (
             False, e.message)

    finally:
        xml_file.close()
        xsd_file.close()


def main():
    xsd_path = 'C:\\Python27\\Lib\\site-packages\\CodeLibWrapper\\RobotFrameworkSample\\SampleData\\StockExchangeSecurity.xsd'
    xml_path = 'C:\\Python27\\Lib\\site-packages\\CodeLibWrapper\\RobotFrameworkSample\\SampleData\\new4.xml'
    result, error_message = Validate_XSD(xml_path, xsd_path)
    print result, error_message


if __name__ == '__main__':
    main()
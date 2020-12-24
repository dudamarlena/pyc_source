# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\XMLFunction\XmlUtils.py
# Compiled at: 2016-12-08 02:02:12
import lxml.etree as etree
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

def parse_xml_from_string(xml_content_string):
    u"""
    从String变量中装载XML 对象
    :param xml_content_string: XML内容
    :return: 返回XML Element
    """
    root = et.fromstring(xml_content_string)
    return root


def __remove_ns(tag):
    if tag.find('}') == -1:
        return tag
    else:
        return tag.split('}', 1)[1]


def __linearize(el, path):
    xpathlist = []
    if el.text is None:
        text = ''
    else:
        text = el.text.strip()
    if text == '':
        xpathlist.append(path)
    else:
        lines = text.splitlines()
        if len(lines) > 1:
            line_nb = 1
            for line in lines:
                xpathlist.append(path + '[line %d]=%s ' % (line_nb, line))
                line_nb += 1

        else:
            xpathlist.append(path + '=' + text)
        for name, val in el.items():
            xpathlist.append(path + '/@' + __remove_ns(name) + '=' + val)

        counters = {}
        for childEl in el:
            tag = __remove_ns(childEl.tag)
            if tag in counters:
                counters[tag] += 1
                numbered_tag = tag + '[' + str(counters[tag]) + ']'
            else:
                counters[tag] = 1
                numbered_tag = tag
            xpathlist.extend(__linearize(childEl, path + '/' + numbered_tag))

    return xpathlist


def __process(stream, prefix):
    tree = et.parse(stream)
    root = tree.getroot()
    return __linearize(root, prefix + '//' + __remove_ns(root.tag))


def parse_xpath_from_xml(file_path, output_to_console=True):
    u"""
    输出给定XML中的节点对应的XPath
    :param file_path: XML文件的Path
    :param output_to_console: 是否输出xpath结果到
    :return: 输出每个节点的xpath值
    """
    l_file = open(file_path)
    return_list = __process(l_file, '')
    if output_to_console:
        for xpath in return_list:
            print xpath

    return return_list


@staticmethod
def pretty_print_xml(xml_file_path):
    x = etree.parse(xml_file_path)
    print etree.tostring(x, pretty_print=True)


def validate_xml(schema_file, xml_file):
    xsd_doc = etree.parse(schema_file)
    xsd = etree.XMLSchema(xsd_doc)
    xml = etree.parse(xml_file)
    return xsd.validate(xml)


if __name__ == '__main__':
    print ''
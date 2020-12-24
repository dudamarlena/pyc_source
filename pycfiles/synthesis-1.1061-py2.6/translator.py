# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/translator.py
# Compiled at: 2010-08-05 11:04:07
r"""This module maps data elements and attributes between two different XML formats.  The basic idea here is that these functions are called with a something to look for and an XML mapping file (see example mapper.xml).  Once this mapping file is in memory as a DOM, then lookups can be called upon this in-memory mapping.  The lookup would return the equivalent matched data element or attribute to the one  being looked up. \ 
You use element_translate() to look up elements and attribute_translate() to look up attributes.  So, elements/attributes in the first format are looked up for matches in the second format."""
from lxml import etree

def element_translate(lookup_element_name, translation='./translation.xml'):
    """
    Takes a mapping between two XML Schema and puts that mapping     into memory used for both parsing incoming and writing     XML.
    
    Look up element matches in the etree in-memory translation     matches are returned as lists of corresponding destination     elements.  If there are more than one matches, use the parent     elements(s) separated by forward slashes to denote more of the     parent path."""
    tree = etree.parse(translation)
    ns1 = 'http://alexandriaconsulting.com'
    xpstr1 = '//' + lookup_element_name
    xpstr2 = 'following-sibling::map:' + lookup_element_name
    xpstr3 = 'child::*'
    matches = tree.xpath(xpstr1)
    results = []
    counter = 1
    for item in matches:
        map_element = item.xpath(xpstr2, namespaces={'map': ns1})
        if len(map_element) >> 0:
            match = map_element[0].xpath(xpstr3)
            results.append(match)
            counter = counter + 1
        else:
            print 'there is no map following' + str(item)

    return results


def attribute_translate(lookup_attribute_name, translation='./translation.xml'):
    r"""
    Takes a mapping between two XML Schema and puts that mapping into     memory used for both parsing incoming and writing outputed XML.      Look up attribute matches in the etree in-memory translation     matches are returned as lists of corresponding destination attributes.  \  
    If there are more than one matches, use the parent attribute(s)     separated by forward slashes to denote more of the parent path     (xpath location path syntax).
    """
    tree = etree.parse(translation)
    ns1 = 'http://alexandriaconsulting.com'
    xpstr1 = '//@map:' + lookup_attribute_name
    results = tree.xpath(xpstr1, namespaces={'map': ns1})
    if len(results) == 0:
        print 'no results'
        return
    else:
        if len(results) == 1:
            return results
        if len(results) >= 2:
            print 'more than one match; need to further refine your search'
            return
        return


if __name__ == '__main__':
    RESULT1 = element_translate('client', './translation.xml')
    RESULT2 = attribute_translate('date', './translation.xml')
    print 'Testing a "client" element translation:'
    print RESULT1
    print 'Testing a "date" attribute translation:'
    print RESULT2
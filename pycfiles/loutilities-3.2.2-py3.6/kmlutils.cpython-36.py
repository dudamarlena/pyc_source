# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\kmlutils.py
# Compiled at: 2019-11-27 06:58:53
# Size of source mod 2**32: 10705 bytes
"""
kmlutils - utilities for access to kml file
=============================================================

Provides methods to write KML files
"""
from xml.dom.minidom import getDOMImplementation as domimpl

class invalidChildattrs(Exception):
    pass


class kmldoc:
    __doc__ = '\n    Represents kml document\n    \n    :param name: name of high level document\n    :rtype: kmldoc instance\n    '

    def __init__(self, name):
        self.doc = domimpl().createDocument('http://www.opengis.net/kml/2.2', 'kml', None)
        self.kml = self.doc.documentElement
        self.kml.setAttribute('xmlns', 'http://www.opengis.net/kml/2.2')
        self.name = name
        ne = self.doc.createElement('name')
        ne.appendChild(self.doc.createTextNode(self.name))
        self.kml.appendChild(ne)
        self.dd = self.doc.createElement('Document')
        self.kml.appendChild(self.dd)

    def save(self, filename):
        """
        save document in the indicated filename
        
        :param filename: name of file to save kml output to
        """
        OUT = open(filename, 'w')
        self.doc.writexml(OUT, addindent='  ', newl='\n')

    def appendChildAttrs(self, element, attrs):
        """
        recursively append the attributes indicated by attrs to the element
        
        :param element: element to append children to
        :param attrs: ellist | attrtree
        
            * attrtree - dict with keywords for element's child attributes (may be nested)
            * ellist - list of elements to be appended, can have embedded attrtrees
            * Note: attrtree can contain embedded ellists or attrtrees
        """
        if isinstance(attrs, dict):
            for attr in attrs:
                atel = self.doc.createElement(attr)
                if isinstance(attrs[attr], dict):
                    self.appendChildAttrs(atel, attrs[attr])
                else:
                    if isinstance(attrs[attr], list):
                        for elattr in attrs[attr]:
                            if isinstance(elattr, dict):
                                self.appendChildAttrs(atel, elattr)
                            else:
                                atel.appendChild(elattr)

                    else:
                        atel.appendChild(self.doc.createTextNode(attrs[attr]))
                element.appendChild(atel)

        else:
            if isinstance(attrs, list):
                for elattr in attrs:
                    if isinstance(elattr, dict):
                        self.appendChildAttrs(element, elattr)
                    else:
                        element.appendChild(elattr)

            else:
                raise invalidChildattrs

    def namedel(self, name, attrs, childattrs):
        """
        return a named element with initial attributes
        
        :param name: tagname for the element
        :param attrs: dictionary with keywords for element's attributes
        :param childattrs: ellist | attrtree
        
            * attrtree - dict with keywords for element's child attributes (may be nested)
            * ellist - list of elements to be appended, can have embedded attrtrees
            * Note: attrtree can contain embedded ellists or attrtrees
        """
        element = self.doc.createElement(name)
        for attr in attrs:
            element.setAttribute(attr, attrs[attr])

        self.appendChildAttrs(element, childattrs)
        return element


class style:
    __doc__ = '\n    represents a style\n    \n    :param kml: kml instance\n    :param name: name of style\n    :param childattrs: dictionary with keywords for style attributes (may be nested)\n    '

    def __init__(self, kml, name, childattrs):
        self.kml = kml
        self.name = name
        self.childattrs = childattrs

    def el(self):
        """
        return kml element for this object
        """
        element = self.kml.doc.createElement('Style')
        element.setAttribute('id', self.name)
        self.kml.appendChildAttrs(element, self.childattrs)
        return element

    def elurl(self):
        element = self.kml.doc.createElement('styleUrl')
        element.appendChild(self.kml.doc.createTextNode('#{0}'.format(self.name)))
        return element


class coordinates:
    __doc__ = '\n    represents a list of coordinates\n    \n    :param kml: kml instance\n    :param clist: list of coordinates\n    '

    def __init__(self, kml, clist):
        self.kml = kml
        self.clist = clist

    def el(self):
        """
        return kml element for this object
        """
        element = self.kml.doc.createElement('coordinates')
        element.appendChild(self.kml.doc.createTextNode(' '.join([c.str() for c in self.clist])))
        return element


class coordinate:
    __doc__ = '\n    represents a coordinate\n    \n    :param lat: latitude (decimal degrees)\n    :param long: longitude (decimal degrees)\n    :param alt: altitude (meters) \n    '

    def __init__(self, lat, long, alt=None):
        self.lat = lat
        self.long = long
        self.alt = alt

    def str(self):
        """
        return kml string for this coordinate
        """
        if self.alt != None:
            return '{0},{1},{2}'.format(self.long, self.lat, self.alt)
        else:
            return '{0},{1}'.format(self.long, self.lat)


def main():
    kml = kmldoc('test doc')
    styred = style(kml, 'red-outline', {'LineStyle':{'color': 'ff0000ff'}, 
     'PolyStyle':{'fill': '0'}})
    styblue = style(kml, 'blue-outline', {'LineStyle':{'color': 'ffff0000'}, 
     'PolyStyle':{'fill': '0'}})
    stygreen = style(kml, 'green-outline', {'LineStyle':{'color': 'ff00ff00'}, 
     'PolyStyle':{'fill': '0'}})
    kml.dd.appendChild(styred.el())
    kml.dd.appendChild(styblue.el())
    kml.dd.appendChild(stygreen.el())
    cl = []
    for i in range(30):
        cl.append(coordinate(i, i + 1, i + 2))

    cs = coordinates(kml, cl)
    kml.dd.appendChild(cs.el())
    place = kml.namedel('Placemark', attrs={'id': 'poly'}, childattrs=[{'name': 'poly'}, stygreen.elurl(), {'Polygon': {'outerBoundaryIs': {'LinearRing': [cs.el()]}}}])
    kml.dd.appendChild(place)
    kml.save('kmlutilstest.kml')


if __name__ == '__main__':
    main()
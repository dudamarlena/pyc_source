# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/svgwrite/drawing.py
# Compiled at: 2012-08-15 03:48:07
"""
The *Drawing* object is the overall container for all SVG
elements. It provides the methods to store the drawing into a file or a
file-like object. If you want to use stylesheets, the reference links
to this stylesheets were also stored (`add_stylesheet`)
in the *Drawing* object.

set/get SVG attributes::

    element['attribute'] = value
    value = element['attribute']

The Drawing object also includes a defs section, add elements to the defs
section by::

    drawing.defs.add(element)

"""
from __future__ import unicode_literals
import io
from svgwrite.container import SVG, Defs
from svgwrite.elementfactory import ElementFactory

class Drawing(SVG, ElementFactory):
    """ This is the SVG drawing represented by the top level *svg* element.

    A drawing consists of any number of SVG elements contained within the drawing
    element, stored in the *elements* attribute.

    A drawing can range from an empty drawing (i.e., no content inside of the drawing),
    to a very simple drawing containing a single SVG element such as a *rect*,
    to a complex, deeply nested collection of container elements and graphics elements.
    """

    def __init__(self, filename=b'noname.svg', size=('100%', '100%'), **extra):
        """
        :param string filename: filesystem filename valid for :func:`open`
        :param 2-tuple size: width, height
        :param keywords extra: additional svg-attributes for the *SVG* object

        Important (and not SVG Attributes) **extra** parameters:

        :param string profile: ``'tiny | full'`` - define the SVG baseProfile
        :param bool debug: switch validation on/off

        """
        super(Drawing, self).__init__(size=size, **extra)
        self.filename = filename
        self._stylesheets = []

    def get_xml(self):
        """ Get the XML representation as `ElementTree` object.

        :return: XML `ElementTree` of this object and all its subelements

        """
        profile = self.profile
        version = self.get_version()
        self.attribs[b'xmlns'] = b'http://www.w3.org/2000/svg'
        self.attribs[b'xmlns:xlink'] = b'http://www.w3.org/1999/xlink'
        self.attribs[b'xmlns:ev'] = b'http://www.w3.org/2001/xml-events'
        self.attribs[b'baseProfile'] = profile
        self.attribs[b'version'] = version
        return super(Drawing, self).get_xml()

    def add_stylesheet(self, href, title, alternate=b'no', media=b'screen'):
        """ Add a stylesheet reference.

        :param string href: link to stylesheet <URI>
        :param string title: name of stylesheet
        :param string alternate: ``'yes'|'no'``
        :param string media: ``'all | aureal | braille | embossed | handheld | print | projection | screen | tty | tv'``

        """
        self._stylesheets.append((href, title, alternate, media))

    def write(self, fileobj):
        """ Write XML string to **fileobj**.

        :param fileobj: a *file-like* object

        Python 3.x - set encoding at the open command::

            open('filename', 'w', encoding='utf-8')
        """
        fileobj.write(b'<?xml version="1.0" encoding="utf-8" ?>\n')
        stylesheet_template = b'<?xml-stylesheet href="%s" type="text/css" title="%s" alternate="%s" media="%s"?>\n'
        for stylesheet in self._stylesheets:
            fileobj.write(stylesheet_template % stylesheet)

        fileobj.write(self.tostring())

    def save(self):
        """ Write the XML string to **filename**. """
        fileobj = io.open(self.filename, mode=b'w', encoding=b'utf-8')
        self.write(fileobj)
        fileobj.close()

    def saveas(self, filename):
        """ Write the XML string to **filename**.

        :param string filename: filesystem filename valid for :func:`open`
        """
        self.filename = filename
        self.save()
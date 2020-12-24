# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_rest_transformation.py
# Compiled at: 2011-01-03 17:15:11
"""
A test suite for transformation of REST resources.
"""
from StringIO import StringIO
from seishub.core.core import Component, implements
from seishub.core.packages.builtins import IResourceType, IPackage
from seishub.core.packages.installer import registerStylesheet
from seishub.core.processor import POST, PUT, DELETE, GET, Processor
from seishub.core.processor.resources import RESTFolder
from seishub.core.test import SeisHubEnvironmentTestCase
import os, unittest
XML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<sales>\n  <division id="North">\n    <revenue>10</revenue>\n    <growth>9</growth>\n    <bonus>7</bonus>\n  </division>\n  <division id="South">\n    <revenue>4</revenue>\n    <growth>3</growth>\n    <bonus>4</bonus>\n  </division>\n  <division id="West">\n    <revenue>6</revenue>\n    <growth>-1.5</growth>\n    <bonus>2</bonus>\n  </division>\n</sales>'
HTML_DOC = '<?xml version="1.0" encoding="utf-8"?>\n\n<html lang="en">\n  <head>\n    <title>Sales Results By Division</title>\n  </head>\n  <body>\n    <table border="1">\n      <tr>\n        <th>Division</th>\n        <th>Revenue</th>\n        <th>Growth</th>\n        <th>Bonus</th>\n      </tr>\n      <tr>\n        <td>\n          <em>North</em>\n        </td>\n        <td>10</td>\n        <td>9</td>\n        <td>7</td>\n      </tr>\n      <tr>\n        <td>\n          <em>West</em>\n        </td>\n        <td>6</td>\n        <td style="color:red">-1.5</td>\n        <td>2</td>\n      </tr>\n      <tr>\n        <td>\n          <em>South</em>\n        </td>\n        <td>4</td>\n        <td>3</td>\n        <td>4</td>\n      </tr>\n    </table>\n  </body>\n</html>\n'
TXT_DOC = 'Sales Results By Division\n\nNorth,10,9,7\nWest,6,-1.5,2\nSouth,4,3,4\n'
SVG_DOC = '<?xml version="1.0"?>\n<svg xmlns:svg="http://www.w3.org/Graphics/SVG/SVG-19990812.dtd" height="3in" width="3in">\n  <g style="stroke: #000000">\n    <line x1="0" x2="150" y1="150" y2="150"/>\n    <line x1="0" x2="0" y1="0" y2="150"/>\n    <text x="0" y="10">Revenue</text>\n    <text x="150" y="165">Division</text>\n    <rect height="100" width="20" x="10" y="50"/>\n    <text x="10" y="165">North</text>\n    <text x="10" y="45">10</text>\n    <rect height="40" width="20" x="50" y="110"/>\n    <text x="50" y="165">South</text>\n    <text x="50" y="105">4</text>\n    <rect height="60" width="20" x="90" y="90"/>\n    <text x="90" y="165">West</text>\n    <text x="90" y="85">6</text>\n  </g>\n</svg>\n'
XML_DOC_2 = '<?xml version="1.0" encoding="utf-8"?>\n\n<test>Sales Results By Division</test>'

class APackage(Component):
    """
    A test package.
    """
    implements(IPackage)
    package_id = 'transformation-test'


class AResourceType(Component):
    """
    A test resource type including various transformation style sheets.
    """
    implements(IResourceType)
    package_id = 'transformation-test'
    resourcetype_id = 'rt'
    registerStylesheet('data' + os.sep + 'transformation' + os.sep + 'xml2html.xslt', 'xml2html')
    registerStylesheet('data' + os.sep + 'transformation' + os.sep + 'xml2svg.xslt', 'xml2svg')
    registerStylesheet('data' + os.sep + 'transformation' + os.sep + 'html2txt.xslt', 'html2txt')
    registerStylesheet('data' + os.sep + 'transformation' + os.sep + 'html2xml.xslt', 'html2xml')


class RestTransformationTests(SeisHubEnvironmentTestCase):
    """
    A test suite for transformation of REST resources.
    """

    def setUp(self):
        self.env.enableComponent(APackage)
        self.env.enableComponent(AResourceType)
        self.env.tree = RESTFolder()
        self.path = os.path.dirname(__file__)

    def tearDown(self):
        for doc in self.env.registry.stylesheets.get('transformation-test'):
            self.env.registry.stylesheets.delete(document_id=doc.document_id)

        for rt in self.env.registry.getResourceTypeIds('transformation-test'):
            self.env.registry.db_deleteResourceType('transformation-test', rt)

        self.env.registry.db_deletePackage('transformation-test')

    def test_getFormatedResource(self):
        """
        Get resource in a certain format using a single style sheet.
        """
        proc = Processor(self.env)
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {'format': []}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC)
        proc.args = {'format': ['xml2html']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, HTML_DOC)
        proc.args = {'format': ['xml2svg']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, SVG_DOC)
        proc.args = {'format': ['XXX']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC)
        proc.run(DELETE, '/transformation-test/rt/test.xml')

    def test_getMultiFormatedResource(self):
        """
        Get resource in a certain format using multiple style sheets.
        """
        proc = Processor(self.env)
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {'format': ['xml2html', 'html2txt']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, TXT_DOC)
        proc.args = {'format': ['XXX', 'YYY', 'ZZZ']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC)
        proc.args = {'format': ['XXX', 'xml2html', 'YYY']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, HTML_DOC)
        proc.args = {'format': ['xml2html', 'html2txt', 'XXX']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, TXT_DOC)
        proc.args = {'format': ['xml2html', 'XXX', 'html2txt']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, TXT_DOC)
        proc.run(DELETE, '/transformation-test/rt/test.xml')

    def test_putFormatedResource(self):
        """
        Upload resource in a certain format using a single style sheets.
        """
        proc = Processor(self.env)
        proc.args = {'format': ['xml2html']}
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, HTML_DOC.strip())
        proc.args = {'format': ['html2txt']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, TXT_DOC)
        proc.run(DELETE, '/transformation-test/rt/test.xml')

    def test_putMultiFormatedResource(self):
        """
        Upload resource in a certain format using multiple style sheets.
        """
        proc = Processor(self.env)
        proc.args = {'format': ['xml2html', 'html2xml']}
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC_2)
        proc.args = {'format': ['xml2html', 'html2txt']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, 'Sales Results By Division\n\n')
        proc.run(DELETE, '/transformation-test/rt/test.xml')
        proc.args = {'format': ['xml2html', 'html2xml', 'XXX']}
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC_2)
        proc.run(DELETE, '/transformation-test/rt/test.xml')
        proc.args = {'format': ['xml2html', 'XXX', 'YYY']}
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, HTML_DOC.strip())
        proc.run(DELETE, '/transformation-test/rt/test.xml')

    def test_postMultiFormatedResource(self):
        """
        Update resource in a certain format using multiple style sheets.
        """
        proc = Processor(self.env)
        proc.run(POST, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {'format': ['xml2html', 'html2xml']}
        proc.run(PUT, '/transformation-test/rt/test.xml', StringIO(XML_DOC))
        proc.args = {}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, XML_DOC_2)
        proc.args = {'format': ['xml2html', 'html2txt']}
        res = proc.run(GET, '/transformation-test/rt/test.xml')
        data = res.render(proc)
        self.assertEquals(data, 'Sales Results By Division\n\n')
        proc.run(DELETE, '/transformation-test/rt/test.xml')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RestTransformationTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
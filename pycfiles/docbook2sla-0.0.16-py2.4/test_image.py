# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/test_image.py
# Compiled at: 2008-03-31 11:20:31
import os, sys, unittest, tempfile
from lxml import etree
from StringIO import StringIO
from docbook2sla import DocBook2Sla
dirname = os.path.dirname(__file__)

class ImagesTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        article = '<article>\n    <mediaobject id="uid001_image_1">\n        <imageobject>\n            <imagedata fileref="http://localhost:8080/test/example-article-1/internet-mail.png" />\n        </imageobject>\n        <caption>\n            <para>My Second Image</para>\n        </caption>\n    </mediaobject>\n</article>'
        scribus = os.path.join(os.path.dirname(__file__), 'data', 'scribus', 'clean134.sla')
        self.d2s = DocBook2Sla()
        outputfn = self.d2s.create(StringIO(article), scribus)
        output = open(outputfn, 'r').read()
        outputtree = etree.XML(output)
        self.output = output
        self.outputtree = outputtree

    def test_no_other_pageobjects(self):
        """ No other pageobjects are existent """
        count_pageobjects = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME!='uid001_image_1'])")
        self.assertEqual(count_pageobjects, 0.0)

    def test_pageobject_exists(self):
        """ Test if image pageobject exists """
        image1 = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME='uid001_image_1'])")
        self.assertEqual(image1, 1.0)

    def test_pageobject_attributes(self):
        """ Test attributes """
        ptype = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME='uid001_image_1' and @PTYPE='2'])")
        self.assertEqual(ptype, 1.0)
        embedded = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME='uid001_image_1' and @EMBEDDED='0'])")
        self.assertEqual(embedded, 1.0)
        irender = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME='uid001_image_1' and @IRENDER='0'])")
        self.assertEqual(irender, 1.0)
        pfile = self.outputtree.xpath("count(//PAGEOBJECT[@ANNAME='uid001_image_1' and @PFILE='http://localhost:8080/test/example-article-1/internet-mail.png'])")
        self.assertEqual(pfile, 1.0)


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ImagesTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    return suite


if __name__ == '__main__':
    test_suite()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Unicode.py
# Compiled at: 2019-09-22 10:12:27
from glob import glob
import os
from shutil import rmtree
import tempfile, unittest
from Cheetah.Compiler import Compiler
from Cheetah.Template import Template
from Cheetah import CheetahWrapper
from Cheetah.compat import PY2, unicode, load_module_from_file

class CommandLineTest(unittest.TestCase):

    def createAndCompile(self, source):
        fd, sourcefile = tempfile.mkstemp()
        os.close(fd)
        os.remove(sourcefile)
        sourcefile = sourcefile.replace('-', '_')
        if PY2:
            fd = open('%s.tmpl' % sourcefile, 'w')
        else:
            fd = open('%s.tmpl' % sourcefile, 'w', encoding='utf-8')
        fd.write(source)
        fd.close()
        wrap = CheetahWrapper.CheetahWrapper()
        wrap.main(['cheetah', 'compile',
         '--encoding=utf-8', '--settings=encoding="utf-8"',
         '--quiet', '--nobackup', sourcefile])
        module_name = os.path.split(sourcefile)[1]
        module = load_module_from_file(module_name, module_name, sourcefile + '.py')
        template = getattr(module, module_name)
        os.remove('%s.tmpl' % sourcefile)
        for sourcefile_py in glob('%s.py*' % sourcefile):
            os.remove(sourcefile_py)

        __pycache__ = os.path.join(os.path.dirname(sourcefile), '__pycache__')
        if os.path.exists(__pycache__):
            rmtree(__pycache__)
        return template


class JBQ_UTF8_Test1(unittest.TestCase):

    def runTest(self):
        t = Template.compile(source='Main file with |$v|\n\n        $other')
        otherT = Template.compile(source='Other template with |$v|')
        other = otherT()
        t.other = other
        t.v = 'Unicode String'
        t.other.v = 'Unicode String'
        assert unicode(t())


class JBQ_UTF8_Test2(unittest.TestCase):

    def runTest(self):
        t = Template.compile(source='Main file with |$v|\n\n        $other')
        otherT = Template.compile(source='Other template with |$v|')
        other = otherT()
        t.other = other
        t.v = 'Unicode String with eacute é'
        t.other.v = 'Unicode String'
        assert unicode(t())


class JBQ_UTF8_Test3(unittest.TestCase):

    def runTest(self):
        t = Template.compile(source='Main file with |$v|\n\n        $other')
        otherT = Template.compile(source='Other template with |$v|')
        other = otherT()
        t.other = other
        t.v = 'Unicode String with eacute é'
        t.other.v = 'Unicode String and an eacute é'
        assert unicode(t())


class JBQ_UTF8_Test4(unittest.TestCase):

    def runTest(self):
        t = Template.compile(source='#encoding utf-8\n        Main file with |$v| and eacute in the template é')
        t.v = 'Unicode String'
        assert unicode(t())


class JBQ_UTF8_Test5(unittest.TestCase):

    def runTest(self):
        t = Template.compile(source='#encoding utf-8\n        Main file with |$v| and eacute in the template é')
        t.v = 'Unicode String'
        assert unicode(t())


class JBQ_UTF8_Test6(unittest.TestCase):

    def runTest(self):
        source = '#encoding utf-8\n        #set $someUnicodeString = u"Bébé"\n        Main file with |$v| and eacute in the template é'
        t = Template.compile(source=source)
        t.v = 'Unicode String'
        assert unicode(t())


class JBQ_UTF8_Test7(CommandLineTest):

    def runTest(self):
        source = '#encoding utf-8\n        #set $someUnicodeString = u"Bébé"\n        Main file with |$v| and eacute in the template é'
        template = self.createAndCompile(source)
        template.v = 'Unicode String'
        assert unicode(template())


class JBQ_UTF8_Test8(CommandLineTest):

    def testStaticCompile(self):
        source = '#encoding utf-8\n#set $someUnicodeString = u"Bébé"\n$someUnicodeString'
        template = self.createAndCompile(source)()
        a = unicode(template)
        if PY2:
            a = a.encode('utf-8')
        self.assertEqual('Bébé', a)

    def testDynamicCompile(self):
        source = '#encoding utf-8\n#set $someUnicodeString = u"Bébé"\n$someUnicodeString'
        template = Template(source=source)
        a = unicode(template)
        if PY2:
            a = a.encode('utf-8')
        self.assertEqual('Bébé', a)


class EncodeUnicodeCompatTest(unittest.TestCase):
    """
        Taken initially from Red Hat's bugzilla #529332
        https://bugzilla.redhat.com/show_bug.cgi?id=529332
    """

    def runTest(self):
        t = Template('Foo ${var}', filter='EncodeUnicode')
        t.var = 'Text with some non-ascii characters: åäö'
        rc = t.respond()
        assert isinstance(rc, unicode), (
         'Template.respond() should return unicode', rc)
        rc = str(t)
        assert isinstance(rc, str), (
         'Template.__str__() should return a UTF-8 encoded string', rc)


class Unicode_in_SearchList_Test(CommandLineTest):

    def test_BasicASCII(self):
        source = 'This is $adjective'
        template = self.createAndCompile(source)
        assert template and issubclass(template, Template)
        template = template(searchList=[{'adjective': 'neat'}])
        assert template.respond()

    def test_Thai(self):
        source = 'This is $foo $adjective'
        template = self.createAndCompile(source)
        assert template and issubclass(template, Template)
        template = template(searchList=[
         {'foo': 'bar', 
            'adjective': 'ยินดีต้อนรับ'}])
        assert template.respond()

    def test_Thai_utf8(self):
        utf8 = 'ยินดีต้อนรับ'
        source = 'This is $adjective'
        template = self.createAndCompile(source)
        assert template and issubclass(template, Template)
        template = template(searchList=[{'adjective': utf8}])
        assert template.respond()


class InlineSpanishTest(unittest.TestCase):

    def setUp(self):
        super(InlineSpanishTest, self).setUp()
        self.template = '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n    <title>Pagina del vendedor</title>\n  </head>\n  <body>\n    $header\n    <h2>Bienvenido $nombre.</h2>\n    <br /><br /><br />\n    <center>\n      Usted tiene $numpedidos_noconf <a href="">pedidós</a> sin confirmar.\n      <br /><br />\n      Bodega tiene fecha para $numpedidos_bodega <a href="">pedidos</a>.\n    </center>\n  </body>\n</html>\n        '

    if PY2:

        def test_failure(self):
            """ Test a template lacking a proper #encoding tag """
            self.assertRaises(UnicodeDecodeError, Template, self.template, searchList=[
             {'header': '', 'nombre': '', 
                'numpedidos_bodega': '', 
                'numpedidos_noconf': ''}])

    def test_success(self):
        """ Test a template with a proper #encoding tag """
        template = '#encoding utf-8\n%s' % self.template
        template = Template(template, searchList=[
         {'header': '', 'nombre': '', 
            'numpedidos_bodega': '', 
            'numpedidos_noconf': ''}])
        self.assertTrue(unicode(template))


class CompilerTest(unittest.TestCase):

    def test_compiler_str(self):
        """ Test Compiler.__str__ """
        source = '#encoding utf-8\n#set $someUnicodeString = u"Bébé"\n$someUnicodeString'
        compiler = Compiler(source)
        self.assertIsInstance(str(compiler), str)
        self.assertEqual(compiler.getModuleEncoding(), 'utf-8')
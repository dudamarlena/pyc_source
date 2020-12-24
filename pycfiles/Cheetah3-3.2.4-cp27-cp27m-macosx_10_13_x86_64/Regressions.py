# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Regressions.py
# Compiled at: 2019-09-22 10:12:27
try:
    from cgi import escape as html_escape
except ImportError:
    from html import escape as html_escape

import unittest, Cheetah.NameMapper, Cheetah.Template
from Cheetah.compat import unicode

class GetAttrException(Exception):
    pass


class CustomGetAttrClass(object):

    def __getattr__(self, name):
        raise GetAttrException('FAIL, %s' % name)


class GetAttrTest(unittest.TestCase):
    """
        Test for an issue occurring when __getatttr__() raises an exception
        causing NameMapper to raise a NotFound exception
    """

    def test_ValidException(self):
        o = CustomGetAttrClass()
        try:
            print o.attr
        except GetAttrException:
            return
        except Exception as e:
            self.fail('Invalid exception raised: %s' % e)

        self.fail('Should have had an exception raised')

    def test_NotFoundException(self):
        template = '\n            #def raiseme()\n                $obj.attr\n            #end def'
        template = Cheetah.Template.Template.compile(template, compilerSettings={}, keepRefToGeneratedCode=True)
        template = template(searchList=[{'obj': CustomGetAttrClass()}])
        assert template, 'We should have a valid template object by now'
        self.assertRaises(GetAttrException, template.raiseme)


class InlineImportTest(unittest.TestCase):

    def test_FromFooImportThing(self):
        """
            Verify that a bug introduced in v2.1.0 where an inline:
                #from module import class
            would result in the following code being generated:
                import class
        """
        template = '\n            #def myfunction()\n                #if True\n                    #from os import path\n                    #return 17\n                    Hello!\n                #end if\n            #end def\n        '
        template = Cheetah.Template.Template.compile(template, compilerSettings={'useLegacyImportMode': False}, keepRefToGeneratedCode=True)
        template = template(searchList=[{}])
        assert template, 'We should have a valid template object by now'
        rc = template.myfunction()
        assert rc == 17, (template, "Didn't get a proper return value")

    def test_ImportFailModule(self):
        template = "\n            #try\n                #import invalidmodule\n            #except\n                #set invalidmodule = dict(FOO='BAR!')\n            #end try\n\n            $invalidmodule.FOO\n        "
        template = Cheetah.Template.Template.compile(template, compilerSettings={'useLegacyImportMode': False}, keepRefToGeneratedCode=True)
        template = template(searchList=[{}])
        assert template, 'We should have a valid template object by now'
        assert str(template), "We weren't able to properly generate the result from the template"

    def test_ProperImportOfBadModule(self):
        template = '\n            #from invalid import fail\n\n            This should totally $fail\n        '
        self.assertRaises(ImportError, Cheetah.Template.Template.compile, template, compilerSettings={'useLegacyImportMode': False}, keepRefToGeneratedCode=True)

    def test_AutoImporting(self):
        template = '\n            #extends FakeyTemplate\n\n            Boo!\n        '
        self.assertRaises(ImportError, Cheetah.Template.Template.compile, template)

    def test_StuffBeforeImport_Legacy(self):
        template = '\n###\n### I like comments before import\n###\n#extends Foo\nBar\n'
        self.assertRaises(ImportError, Cheetah.Template.Template.compile, template, compilerSettings={'useLegacyImportMode': True}, keepRefToGeneratedCode=True)


class Mantis_Issue_11_Regression_Test(unittest.TestCase):
    """
        Test case for bug outlined in Mantis issue #11:

        Output:
        Traceback (most recent call last):
          File "test.py", line 12, in <module>
            t.respond()
          File "DynamicallyCompiledCheetahTemplate.py", line 86, in respond
          File "/usr/lib64/python2.6/cgi.py", line 1035, in escape
            s = s.replace("&", "&") # Must be done first!
    """

    def test_FailingBehavior(self):
        template = Cheetah.Template.Template('$escape($request)', searchList=[{'escape': html_escape, 'request': 'foobar'}])
        assert template
        self.assertRaises(AttributeError, template.respond)

    def test_FailingBehaviorWithSetting(self):
        template = Cheetah.Template.Template('$escape($request)', searchList=[{'escape': html_escape, 'request': 'foobar'}], compilerSettings={'prioritizeSearchListOverSelf': True})
        assert template
        assert template.respond()


class Mantis_Issue_21_Regression_Test(unittest.TestCase):
    """
        Test case for bug outlined in issue #21

        Effectively @staticmethod and @classmethod
        decorated methods in templates don't
        properly define the _filter local, which breaks
        when using the NameMapper
    """

    def runTest(self):
        template = '\n            #@staticmethod\n            #def testMethod()\n                This is my $output\n            #end def\n        '
        template = Cheetah.Template.Template.compile(template)
        assert template
        assert template.testMethod(output='bug')


class Mantis_Issue_22_Regression_Test(unittest.TestCase):
    """
        Test case for bug outlined in issue #22

        When using @staticmethod and @classmethod
        in conjunction with the #filter directive
        the generated code for the #filter is reliant
        on the `self` local, breaking the function
    """

    def test_NoneFilter(self):
        return
        template = '\n            #@staticmethod\n            #def testMethod()\n                #filter None\n                    This is my $output\n                #end filter\n            #end def\n        '
        template = Cheetah.Template.Template.compile(template)
        assert template
        assert template.testMethod(output='bug')

    def test_DefinedFilter(self):
        return
        template = '\n            #@staticmethod\n            #def testMethod()\n                #filter Filter\n                    This is my $output\n                #end filter\n            #end def\n        '
        template = Cheetah.Template.Template.compile(template)
        assert template
        assert template.testMethod(output='bug')
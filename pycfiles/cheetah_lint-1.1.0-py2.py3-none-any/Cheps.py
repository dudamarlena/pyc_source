# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tests/Cheps.py
# Compiled at: 2019-09-22 10:12:27
import Cheetah, Cheetah.Parser, Cheetah.Template

class Chep_2_Conditionalized_Import_Behavior:

    def test_ModuleLevelImport(self):
        """ Verify module level (traditional) import behavior """
        pass

    def test_InlineImport(self):
        """ Verify (new) inline import behavior works """
        template = '\n            #def funky($s)\n                #try\n                    #import urllib\n                #except ImportError\n                    #pass\n                #end try\n                #return urllib.quote($s)\n            #end def\n        '
        try:
            template = Cheetah.Template.Template.compile(template)
        except Cheetah.Parser.ParseError as ex:
            self.fail('Failed to properly generate code %s' % ex)

        template = template()
        rc = template.funky('abc def')
        assert rc == 'abc+def'

    def test_LegacyMode(self):
        """ Verify disabling of CHEP #2 works """
        pass
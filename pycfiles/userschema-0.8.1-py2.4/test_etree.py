# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/userschema/tests/test_etree.py
# Compiled at: 2007-06-25 17:22:16
import unittest
try:
    from lxml.etree import XML
except ImportError:
    from elementtree.ElementTree import XML

try:
    from zope.datetime import parseDatetimetz
except ImportError:
    from zope.app.datetimeutils import parseDatetimetz

class FieldHandlerTests(unittest.TestCase):
    __module__ = __name__

    def test_TextHandler(self):
        from zope.schema import Text
        from userschema.etree import TextHandler
        node = XML('<Text name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                      </Text>')
        field = TextHandler(node)
        self.failUnless(isinstance(field, Text))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')

    def test_TextLineHandler(self):
        from zope.schema import TextLine
        from userschema.etree import TextLineHandler
        node = XML('<TextLine name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                        <min_length>5</min_length>\n                        <max_length>10</max_length>\n                      </TextLine>')
        field = TextLineHandler(node)
        self.failUnless(isinstance(field, TextLine))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')
        self.assertEqual(field.min_length, 5)
        self.assertEqual(field.max_length, 10)

    def test_PasswordHandler(self):
        from zope.schema import Password
        from userschema.etree import PasswordHandler
        node = XML('<Password name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                        <min_length>5</min_length>\n                        <max_length>10</max_length>\n                      </Password>')
        field = PasswordHandler(node)
        self.failUnless(isinstance(field, Password))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')
        self.assertEqual(field.min_length, 5)
        self.assertEqual(field.max_length, 10)

    def test_IntHandler(self):
        from zope.schema import Int
        from userschema.etree import IntHandler
        node = XML('<Int name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>6</default>\n                        <min>5</min>\n                        <max>10</max>\n                      </Int>')
        field = IntHandler(node)
        self.failUnless(isinstance(field, Int))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 6)
        self.assertEqual(field.min, 5)
        self.assertEqual(field.max, 10)

    def test_BoolHandler(self):
        from zope.schema import Bool
        from userschema.etree import BoolHandler
        node = XML('<Bool name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>True</default>\n                      </Bool>')
        field = BoolHandler(node)
        self.failUnless(isinstance(field, Bool))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, True)

    def test_SourceTextHandler(self):
        from zope.schema import SourceText
        from userschema.etree import SourceTextHandler
        node = XML('<SourceText name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Source text</default>\n                      </SourceText>')
        field = SourceTextHandler(node)
        self.failUnless(isinstance(field, SourceText))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Source text')

    def test_BytesHandler(self):
        from zope.schema import Bytes
        from userschema.etree import BytesHandler
        node = XML('<Bytes name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                      </Bytes>')
        field = BytesHandler(node)
        self.failUnless(isinstance(field, Bytes))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')

    def test_ASCIIHandler(self):
        from zope.schema import ASCII
        from userschema.etree import ASCIIHandler
        node = XML('<ASCII name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                      </ASCII>')
        field = ASCIIHandler(node)
        self.failUnless(isinstance(field, ASCII))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')

    def test_BytesLineHandler(self):
        from zope.schema import BytesLine
        from userschema.etree import BytesLineHandler
        node = XML('<BytesLine name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                        <min_length>5</min_length>\n                        <max_length>10</max_length>\n                      </BytesLine>')
        field = BytesLineHandler(node)
        self.failUnless(isinstance(field, BytesLine))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')
        self.assertEqual(field.min_length, 5)
        self.assertEqual(field.max_length, 10)

    def test_ASCIILineHandler(self):
        from zope.schema import ASCIILine
        from userschema.etree import ASCIILineHandler
        node = XML('<ASCIILine name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>Default</default>\n                        <min_length>5</min_length>\n                        <max_length>10</max_length>\n                      </ASCIILine>')
        field = ASCIILineHandler(node)
        self.failUnless(isinstance(field, ASCIILine))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 'Default')
        self.assertEqual(field.min_length, 5)
        self.assertEqual(field.max_length, 10)

    def test_FloatHandler(self):
        from zope.schema import Float
        from userschema.etree import FloatHandler
        node = XML('<Float name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>3.141926</default>\n                        <min>1.414</min>\n                        <max>7.1828</max>\n                      </Float>')
        field = FloatHandler(node)
        self.failUnless(isinstance(field, Float))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, 3.141926)
        self.assertEqual(field.min, 1.414)
        self.assertEqual(field.max, 7.1828)

    def test_DatetimeHandler(self):
        from zope.schema import Datetime
        from userschema.etree import DatetimeHandler
        DEFAULT = '2007-01-29T09:34:27Z'
        MIN = '2007-01-01T00:00:00Z'
        MAX = '2007-12-31T23:59:59Z'
        node = XML('<Datetime name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>%s</default>\n                        <min>%s</min>\n                        <max>%s</max>\n                      </Datetime>' % (DEFAULT, MIN, MAX))
        field = DatetimeHandler(node)
        self.failUnless(isinstance(field, Datetime))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, parseDatetimetz(DEFAULT))
        self.assertEqual(field.min, parseDatetimetz(MIN))
        self.assertEqual(field.max, parseDatetimetz(MAX))

    def test_DateHandler(self):
        from datetime import date
        from zope.schema import Date
        from userschema.etree import DateHandler
        DEFAULT = '2007-01-29'
        MIN = '2007-01-01'
        MAX = '2007-12-31'
        node = XML('<Date name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>%s</default>\n                        <min>%s</min>\n                        <max>%s</max>\n                      </Date>' % (DEFAULT, MIN, MAX))
        field = DateHandler(node)
        self.failUnless(isinstance(field, Date))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, parseDatetimetz(DEFAULT).date())
        self.assertEqual(field.min, parseDatetimetz(MIN).date())
        self.assertEqual(field.max, parseDatetimetz(MAX).date())

    def test_TimedeltaHandler(self):
        from datetime import timedelta
        from zope.schema import Timedelta
        from userschema.etree import TimedeltaHandler
        DEFAULT = timedelta(2, 3, 4)
        MIN = timedelta(1, 2, 3)
        MAX = timedelta(7, 8, 9)
        node = XML('<Timedelta name="test">\n                        <title>Title</title>\n                        <description>Description</description>\n                        <required>True</required>\n                        <readonly>False</readonly>\n                        <default>2:3:4</default>\n                        <min>1:2:3</min>\n                        <max>7:8:9</max>\n                      </Timedelta>')
        field = TimedeltaHandler(node)
        self.failUnless(isinstance(field, Timedelta))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, DEFAULT)
        self.assertEqual(field.min, MIN)
        self.assertEqual(field.max, MAX)

    def test_ChoiceHandler(self):
        from zope.schema import Choice
        from userschema.etree import ChoiceHandler
        DEFAULT = 'garlic'
        node = XML('<Choice name="test">\n            <title>Title</title>\n            <description>Description</description>\n            <required>True</required>\n            <readonly>False</readonly>\n            <default>garlic</default>\n            <option>basil</option>\n            <option>garlic</option>\n            <option>pepper</option>\n            <option>salt</option>\n            <option>oregano</option>\n            </Choice>')
        field = ChoiceHandler(node)
        self.failUnless(isinstance(field, Choice))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, DEFAULT)
        options = ['basil', 'garlic', 'pepper', 'salt', 'oregano']
        self.assertEqual([ term.value for term in field.vocabulary ], options)

    def test_ChoiceSetHandler(self):
        from userschema.schema import ChoiceSet
        from userschema.etree import ChoiceSetHandler
        from userschema.etree import SET_TYPE
        DEFAULT = SET_TYPE(['garlic'])
        node = XML('<ChoiceSet name="test">\n            <title>Title</title>\n            <description>Description</description>\n            <required>True</required>\n            <readonly>False</readonly>\n            <default>garlic</default>\n            <option>basil</option>\n            <option>garlic</option>\n            <option>pepper</option>\n            <option>salt</option>\n            <option>oregano</option>\n            </ChoiceSet>')
        field = ChoiceSetHandler(node)
        self.failUnless(isinstance(field, ChoiceSet))
        self.assertEqual(field.__name__, 'test')
        self.assertEqual(field.title, 'Title')
        self.assertEqual(field.description, 'Description')
        self.assertEqual(field.required, True)
        self.assertEqual(field.readonly, False)
        self.assertEqual(field.default, DEFAULT)
        options = ['basil', 'garlic', 'pepper', 'salt', 'oregano']
        self.assertEqual([ term.value for term in field.vocabulary ], options)

    def test_ChoiceSetHandlerNoDefault(self):
        from userschema.schema import ChoiceSet
        from userschema.etree import ChoiceSetHandler
        from userschema.etree import SET_TYPE
        DEFAULT = SET_TYPE(['garlic'])
        node = XML('<ChoiceSet name="test">\n            <title>Title</title>\n            <description>Description</description>\n            <required>True</required>\n            <readonly>False</readonly>\n            <option>basil</option>\n            <option>garlic</option>\n            <option>pepper</option>\n            <option>salt</option>\n            <option>oregano</option>\n            </ChoiceSet>')
        field = ChoiceSetHandler(node)
        self.assertEqual(field.default, None)
        return

    def test_ChoiceSetHandlerNonASCII(self):
        from userschema.schema import ChoiceSet
        from userschema.etree import ChoiceSetHandler
        node = XML('<ChoiceSet name="test">\n            <title>Title</title>\n            <description>Description</description>\n            <required>True</required>\n            <readonly>False</readonly>\n            <option>copyright sign (©)</option>\n            </ChoiceSet>')
        field = ChoiceSetHandler(node)
        tokens = [
         str(hash('copyright sign (©)'))]
        self.assertEqual([ term.token for term in field.vocabulary ], tokens)

    def test_IgnoreComments(self):
        from userschema.schema import ChoiceSet
        from userschema.etree import ChoiceSetHandler
        from userschema.etree import SET_TYPE
        DEFAULT = SET_TYPE(['garlic'])
        node = XML('<ChoiceSet name="test">\n            <title>Title</title>\n            <description>Description</description>\n            <required>True</required>\n            <readonly>False</readonly>\n            <default>garlic</default>\n            <!--comment-->\n            <!--comment-->\n            <!--comment-->\n            <option>basil</option>\n            <option>garlic</option>\n            <option>pepper</option>\n            <option>salt</option>\n            <option>oregano</option>\n            </ChoiceSet>')
        field = ChoiceSetHandler(node)


def test_suite():
    return unittest.TestSuite((unittest.makeSuite(FieldHandlerTests),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/django_common.py
# Compiled at: 2011-06-23 07:05:59
from common import Common
import re
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.template import Template, Context

class DjangoCommon(Common):
    """
    This class contains a number of custom assertions which
    extend the default Django assertions. Use this as the super
    class for you tests rather than django.test.TestCase
    """
    fixtures = []

    def setUp(self):
        """
        setUp is run before each test in the class. Use it for
        initilisation and creating mock objects to test
        """
        pass

    def tearDown(self):
        """
        tearDown is run after each test in the class. Use it for
        cleaning up data created during each test
        """
        pass

    def login_as_admin(self):
        """Create, then login as, an admin user"""
        try:
            User.objects.get(username='admin')
        except User.DoesNotExist:
            user = User.objects.create_user('admin', 'admin@example.com', 'password')
            user.is_staff = True
            user.is_superuser = True
            user.save()

        if not self.client.login(username='admin', password='password'):
            raise Exception('Login failed')

    template_tag_libraries = []

    def render(self, template, **kwargs):
        """Return the rendering of a given template including loading of template tags"""
        template = ('').join([ '{%% load %s %%}' % lib for lib in self.template_tag_libraries ]) + template
        return Template(template).render(Context(kwargs)).strip()

    def assert_response_contains(self, fragment, response):
        """Assert that a response object contains a given string"""
        self.assert_(fragment in response.content, "Response should contain `%s' but doesn't:\n%s" % (fragment, response.content))

    def assert_response_doesnt_contain(self, fragment, response):
        """Assert that a response object does not contain a given string"""
        self.assert_(fragment not in response.content, "Response should not contain `%s' but does:\n%s" % (fragment, response.content))

    def assert_render_matches(self, template, match_regexp, vars={}):
        """Assert than the output from rendering a given template with a given context matches a given regex"""
        r = re.compile(match_regexp)
        actual = Template(template).render(Context(vars))
        self.assert_(r.match(actual), 'Expected: %s\nGot: %s' % (
         match_regexp, actual))

    def assert_code(self, response, code):
        """Assert that a given response returns a given HTTP status code"""
        self.assertEqual(code, response.status_code, 'HTTP Response status code should be %d, and is %d' % (code, response.status_code))

    def assertNotContains(self, response, text, status_code=200):
        """
        Asserts that a response indicates that a page was retrieved
        successfully, (i.e., the HTTP status code was as expected), and that
        ``text`` doesn't occurs in the content of the response.
        """
        self.assertEqual(response.status_code, status_code, "Retrieving page: Response code was %d (expected %d)'" % (
         response.status_code, status_code))
        text = smart_str(text, response._charset)
        self.assertEqual(response.content.count(text), 0, "Response should not contain '%s'" % text)

    def assert_render(self, expected, template, **kwargs):
        """Asserts than a given template and context render a given fragment"""
        self.assert_equal(expected, self.render(template, **kwargs))

    def assert_render_matches(self, match_regexp, template, vars={}):
        r = re.compile(match_regexp)
        actual = Template(template).render(Context(vars))
        self.assert_(r.match(actual), 'Expected: %s\nGot: %s' % (
         match_regexp, actual))

    def assert_doesnt_render(self, expected, template, **kwargs):
        """Asserts than a given template and context don't render a given fragment"""
        self.assert_not_equal(expected, self.render(template, **kwargs))

    def assert_render_contains(self, expected, template, **kwargs):
        """Asserts than a given template and context rendering contains a given fragment"""
        self.assert_contains(expected, self.render(template, **kwargs))

    def assert_render_doesnt_contain(self, expected, template, **kwargs):
        """Asserts than a given template and context rendering does not contain a given fragment"""
        self.assert_doesnt_contain(expected, self.render(template, **kwargs))

    def assert_mail--- This code section failed: ---

 L. 125         0  LOAD_CONST               -1
                3  LOAD_CONST               ('mail',)
                6  IMPORT_NAME           0  'django.core'
                9  IMPORT_FROM           1  'mail'
               12  STORE_FAST            2  'mail'
               15  POP_TOP          

 L. 126        16  LOAD_GLOBAL           2  'len'
               19  LOAD_FAST             2  'mail'
               22  LOAD_ATTR             3  'outbox'
               25  CALL_FUNCTION_1       1  None
               28  STORE_FAST            3  'previous_mails'

 L. 127        31  LOAD_FAST             1  'funk'
               34  CALL_FUNCTION_0       0  None
               37  POP_TOP          

 L. 128        38  LOAD_FAST             2  'mail'
               41  LOAD_ATTR             3  'outbox'
               44  LOAD_FAST             3  'previous_mails'
               47  SLICE+1          
               48  STORE_FAST            4  'mails'

 L. 129        51  BUILD_LIST_0          0 
               54  LOAD_FAST             4  'mails'
               57  COMPARE_OP            3  !=
               60  POP_JUMP_IF_TRUE     72  'to 72'
               63  LOAD_ASSERT              AssertionError
               66  LOAD_CONST               'the called block produced no mails'
               69  RAISE_VARARGS_2       2  None

 L. 130        72  LOAD_GLOBAL           2  'len'
               75  LOAD_FAST             4  'mails'
               78  CALL_FUNCTION_1       1  None
               81  LOAD_CONST               1
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_FAST             4  'mails'
               93  LOAD_CONST               0
               96  BINARY_SUBSCR    
               97  RETURN_END_IF    
             98_0  COME_FROM            87  '87'

 L. 131        98  LOAD_FAST             4  'mails'
              101  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 101

    def assert_latest(self, query_set, lamb):
        pks = list(query_set.values_list('pk', flat=True).order_by('-pk'))
        high_water_mark = (pks + [0])[0]
        lamb()
        nu_records = list(query_set.filter(pk__gt=high_water_mark).order_by('pk'))
        if len(nu_records) == 1:
            return nu_records[0]
        if nu_records:
            return nu_records
        source = open(lamb.func_code.co_filename, 'r').readlines()[(lamb.func_code.co_firstlineno - 1)]
        source = source.replace('lambda:', '').strip()
        model_name = str(query_set.model)
        self.assertFalse(True, 'The called block, `' + source + '` should produce new ' + model_name + ' records')

    def deny_mail--- This code section failed: ---

 L. 156         0  LOAD_CONST               -1
                3  LOAD_CONST               ('mail',)
                6  IMPORT_NAME           0  'django.core'
                9  IMPORT_FROM           1  'mail'
               12  STORE_FAST            2  'mail'
               15  POP_TOP          

 L. 157        16  LOAD_GLOBAL           2  'len'
               19  LOAD_FAST             2  'mail'
               22  LOAD_ATTR             3  'outbox'
               25  CALL_FUNCTION_1       1  None
               28  STORE_FAST            3  'previous_mails'

 L. 158        31  LOAD_FAST             1  'funk'
               34  CALL_FUNCTION_0       0  None
               37  POP_TOP          

 L. 159        38  LOAD_FAST             2  'mail'
               41  LOAD_ATTR             3  'outbox'
               44  LOAD_FAST             3  'previous_mails'
               47  SLICE+1          
               48  STORE_FAST            4  'mails'

 L. 160        51  BUILD_LIST_0          0 
               54  LOAD_FAST             4  'mails'
               57  COMPARE_OP            2  ==
               60  POP_JUMP_IF_TRUE     72  'to 72'
               63  LOAD_ASSERT              AssertionError
               66  LOAD_CONST               'the called block should produce no mails'
               69  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 66

    def assert_model_changes(self, mod, item, frum, too, lamb):
        source = open(lamb.func_code.co_filename, 'r').readlines()[(lamb.func_code.co_firstlineno - 1)]
        source = source.replace('lambda:', '').strip()
        model = str(mod.__class__).replace("'>", '').split('.')[(-1)]
        should = '%s.%s should equal `%s` before your activation line, `%s`' % (
         model, item, frum, source)
        self.assertEqual(frum, mod.__dict__[item], should)
        lamb()
        mod = mod.__class__.objects.get(pk=mod.pk)
        should = '%s.%s should equal `%s` after your activation line, `%s`' % (
         model, item, too, source)
        self.assertEqual(too, mod.__dict__[item], should)
        return mod
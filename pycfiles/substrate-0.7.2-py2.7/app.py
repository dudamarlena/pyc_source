# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/local/substrate/lib/webtest/app.py
# Compiled at: 2012-09-09 20:09:24
"""
Routines for testing WSGI applications.

Most interesting is TestApp
"""
import random, warnings, mimetypes, cgi, os, re, fnmatch
from webtest.compat import urlparse
from webtest.compat import print_stderr
from webtest.compat import StringIO
from webtest.compat import BytesIO
from webtest.compat import SimpleCookie, CookieError
from webtest.compat import cookie_quote
from webtest.compat import urlencode
from webtest.compat import splittype
from webtest.compat import splithost
from webtest.compat import string_types
from webtest.compat import binary_type
from webtest.compat import text_type
from webtest.compat import to_string
from webtest.compat import to_bytes
from webtest.compat import join_bytes
from webtest.compat import OrderedDict
from webtest.compat import dumps
from webtest.compat import loads
from webtest.compat import PY3
from webob import Request, Response
if PY3:
    from webtest import lint3 as lint
else:
    from webtest import lint
__all__ = [
 'TestApp', 'TestRequest']

class NoDefault(object):
    pass


class AppError(Exception):

    def __init__(self, message, *args):
        message = to_string(message)
        str_args = ()
        for arg in args:
            if isinstance(arg, Response):
                body = arg.body
                if isinstance(body, binary_type):
                    if arg.charset:
                        arg = body.decode(arg.charset)
                    else:
                        arg = repr(body)
            elif isinstance(arg, binary_type):
                try:
                    arg = to_string(arg)
                except UnicodeDecodeError:
                    arg = repr(arg)

            str_args += (arg,)

        message = message % str_args
        Exception.__init__(self, message)


class TestResponse(Response):
    """
    Instances of this class are return by ``TestApp``
    """
    request = None
    _forms_indexed = None

    def forms__get(self):
        """
        Returns a dictionary of :class:`~webtest.Form` objects.  Indexes are
        both in order (from zero) and by form id (if the form is given an id).
        """
        if self._forms_indexed is None:
            self._parse_forms()
        return self._forms_indexed

    forms = property(forms__get, doc='\n                     A list of :class:`~webtest.Form`s found on the page\n                     ')

    def form__get(self):
        forms = self.forms
        if not forms:
            raise TypeError('You used response.form, but no forms exist')
        if 1 in forms:
            raise TypeError('You used response.form, but more than one form exists')
        return forms[0]

    form = property(form__get, doc='\n                    Returns a single :class:`~webtest.Form` instance; it is an\n                    error if there are multiple forms on the page.\n                    ')

    @property
    def testbody(self):
        if getattr(self, '_use_unicode', True) and self.charset:
            return self.unicode_body
        if PY3:
            return to_string(self.body)
        return self.body

    _tag_re = re.compile('<(/?)([:a-z0-9_\\-]*)(.*?)>', re.S | re.I)

    def _parse_forms--- This code section failed: ---

 L. 125         0  BUILD_MAP_0           0  None
                3  DUP_TOP          
                4  STORE_FAST            1  'forms'
                7  LOAD_FAST             0  'self'
               10  STORE_ATTR            0  '_forms_indexed'

 L. 126        13  BUILD_LIST_0          0 
               16  STORE_FAST            2  'form_texts'

 L. 127        19  LOAD_CONST               None
               22  STORE_FAST            3  'started'

 L. 128        25  SETUP_LOOP          196  'to 224'
               28  LOAD_FAST             0  'self'
               31  LOAD_ATTR             2  '_tag_re'
               34  LOAD_ATTR             3  'finditer'
               37  LOAD_FAST             0  'self'
               40  LOAD_ATTR             4  'testbody'
               43  CALL_FUNCTION_1       1  None
               46  GET_ITER         
               47  FOR_ITER            173  'to 223'
               50  STORE_FAST            4  'match'

 L. 129        53  LOAD_FAST             4  'match'
               56  LOAD_ATTR             5  'group'
               59  LOAD_CONST               1
               62  CALL_FUNCTION_1       1  None
               65  LOAD_CONST               '/'
               68  COMPARE_OP            2  ==
               71  STORE_FAST            5  'end'

 L. 130        74  LOAD_FAST             4  'match'
               77  LOAD_ATTR             5  'group'
               80  LOAD_CONST               2
               83  CALL_FUNCTION_1       1  None
               86  LOAD_ATTR             6  'lower'
               89  CALL_FUNCTION_0       0  None
               92  STORE_FAST            6  'tag'

 L. 131        95  LOAD_FAST             6  'tag'
               98  LOAD_CONST               'form'
              101  COMPARE_OP            3  !=
              104  POP_JUMP_IF_FALSE   113  'to 113'

 L. 132       107  CONTINUE             47  'to 47'
              110  JUMP_FORWARD          0  'to 113'
            113_0  COME_FROM           110  '110'

 L. 133       113  LOAD_FAST             5  'end'
              116  POP_JUMP_IF_FALSE   182  'to 182'

 L. 134       119  LOAD_FAST             3  'started'
              122  POP_JUMP_IF_TRUE    144  'to 144'
              125  LOAD_ASSERT              AssertionError

 L. 135       128  LOAD_CONST               '</form> unexpected at %s'
              131  LOAD_FAST             4  'match'
              134  LOAD_ATTR             8  'start'
              137  CALL_FUNCTION_0       0  None
              140  BINARY_MODULO    
              141  RAISE_VARARGS_2       2  None

 L. 136       144  LOAD_FAST             2  'form_texts'
              147  LOAD_ATTR             9  'append'
              150  LOAD_FAST             0  'self'
              153  LOAD_ATTR             4  'testbody'
              156  LOAD_FAST             3  'started'
              159  LOAD_FAST             4  'match'
              162  LOAD_ATTR            10  'end'
              165  CALL_FUNCTION_0       0  None
              168  SLICE+3          
              169  CALL_FUNCTION_1       1  None
              172  POP_TOP          

 L. 137       173  LOAD_CONST               None
              176  STORE_FAST            3  'started'
              179  JUMP_BACK            47  'to 47'

 L. 139       182  LOAD_FAST             3  'started'
              185  UNARY_NOT        
              186  POP_JUMP_IF_TRUE    208  'to 208'
              189  LOAD_ASSERT              AssertionError

 L. 140       192  LOAD_CONST               'Nested form tags at %s'
              195  LOAD_FAST             4  'match'
              198  LOAD_ATTR             8  'start'
              201  CALL_FUNCTION_0       0  None
              204  BINARY_MODULO    
              205  RAISE_VARARGS_2       2  None

 L. 141       208  LOAD_FAST             4  'match'
              211  LOAD_ATTR             8  'start'
              214  CALL_FUNCTION_0       0  None
              217  STORE_FAST            3  'started'
              220  JUMP_BACK            47  'to 47'
              223  POP_BLOCK        
            224_0  COME_FROM            25  '25'

 L. 142       224  LOAD_FAST             3  'started'
              227  UNARY_NOT        
              228  POP_JUMP_IF_TRUE    251  'to 251'
              231  LOAD_ASSERT              AssertionError

 L. 143       234  LOAD_CONST               'Danging form: %r'
              237  LOAD_FAST             0  'self'
              240  LOAD_ATTR             4  'testbody'
              243  LOAD_FAST             3  'started'
              246  SLICE+1          
              247  BINARY_MODULO    
              248  RAISE_VARARGS_2       2  None

 L. 144       251  SETUP_LOOP           76  'to 330'
              254  LOAD_GLOBAL          11  'enumerate'
              257  LOAD_FAST             2  'form_texts'
              260  CALL_FUNCTION_1       1  None
              263  GET_ITER         
              264  FOR_ITER             62  'to 329'
              267  UNPACK_SEQUENCE_2     2 
              270  STORE_FAST            7  'i'
              273  STORE_FAST            8  'text'

 L. 145       276  LOAD_GLOBAL          12  'Form'
              279  LOAD_FAST             0  'self'
              282  LOAD_FAST             8  'text'
              285  CALL_FUNCTION_2       2  None
              288  STORE_FAST            9  'form'

 L. 146       291  LOAD_FAST             9  'form'
              294  LOAD_FAST             1  'forms'
              297  LOAD_FAST             7  'i'
              300  STORE_SUBSCR     

 L. 147       301  LOAD_FAST             9  'form'
              304  LOAD_ATTR            13  'id'
              307  POP_JUMP_IF_FALSE   264  'to 264'

 L. 148       310  LOAD_FAST             9  'form'
              313  LOAD_FAST             1  'forms'
              316  LOAD_FAST             9  'form'
              319  LOAD_ATTR            13  'id'
              322  STORE_SUBSCR     
              323  JUMP_BACK           264  'to 264'
              326  JUMP_BACK           264  'to 264'
              329  POP_BLOCK        
            330_0  COME_FROM           251  '251'
              330  LOAD_CONST               None
              333  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 223

    def follow--- This code section failed: ---

 L. 156         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'status_int'
                6  LOAD_CONST               300
                9  COMPARE_OP            5  >=
               12  POP_JUMP_IF_FALSE    30  'to 30'
               15  LOAD_FAST             0  'self'
               18  LOAD_ATTR             0  'status_int'
               21  LOAD_CONST               400
               24  COMPARE_OP            0  <
             27_0  COME_FROM            12  '12'
               27  POP_JUMP_IF_TRUE     46  'to 46'
               30  LOAD_ASSERT              AssertionError

 L. 157        33  LOAD_CONST               'You can only follow redirect responses (not %s)'

 L. 158        36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             2  'status'
               42  BINARY_MODULO    
               43  RAISE_VARARGS_2       2  None

 L. 159        46  LOAD_FAST             0  'self'
               49  LOAD_ATTR             3  'headers'
               52  LOAD_CONST               'location'
               55  BINARY_SUBSCR    
               56  STORE_FAST            2  'location'

 L. 160        59  LOAD_GLOBAL           4  'splittype'
               62  LOAD_FAST             2  'location'
               65  CALL_FUNCTION_1       1  None
               68  UNPACK_SEQUENCE_2     2 
               71  STORE_FAST            3  'type'
               74  STORE_FAST            4  'rest'

 L. 161        77  LOAD_GLOBAL           5  'splithost'
               80  LOAD_FAST             4  'rest'
               83  CALL_FUNCTION_1       1  None
               86  UNPACK_SEQUENCE_2     2 
               89  STORE_FAST            5  'host'
               92  STORE_FAST            6  'path'

 L. 163        95  LOAD_FAST             0  'self'
               98  LOAD_ATTR             6  'test_app'
              101  LOAD_ATTR             7  'get'
              104  LOAD_FAST             2  'location'
              107  LOAD_FAST             1  'kw'
              110  CALL_FUNCTION_KW_1     1  None
              113  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 113

    def click(self, description=None, linkid=None, href=None, anchor=None, index=None, verbose=False, extra_environ=None):
        """
        Click the link as described.  Each of ``description``,
        ``linkid``, and ``url`` are *patterns*, meaning that they are
        either strings (regular expressions), compiled regular
        expressions (objects with a ``search`` method), or callables
        returning true or false.

        All the given patterns are ANDed together:

        * ``description`` is a pattern that matches the contents of the
          anchor (HTML and all -- everything between ``<a...>`` and
          ``</a>``)

        * ``linkid`` is a pattern that matches the ``id`` attribute of
          the anchor.  It will receive the empty string if no id is
          given.

        * ``href`` is a pattern that matches the ``href`` of the anchor;
          the literal content of that attribute, not the fully qualified
          attribute.

        * ``anchor`` is a pattern that matches the entire anchor, with
          its contents.

        If more than one link matches, then the ``index`` link is
        followed.  If ``index`` is not given and more than one link
        matches, or if no link matches, then ``IndexError`` will be
        raised.

        If you give ``verbose`` then messages will be printed about
        each link, and why it does or doesn't match.  If you use
        ``app.click(verbose=True)`` you'll see a list of all the
        links.

        You can use multiple criteria to essentially assert multiple
        aspects about the link, e.g., where the link's destination is.
        """
        __tracebackhide__ = True
        found_html, found_desc, found_attrs = self._find_element(tag='a', href_attr='href', href_extract=None, content=description, id=linkid, href_pattern=href, html_pattern=anchor, index=index, verbose=verbose)
        return self.goto(found_attrs['uri'], extra_environ=extra_environ)

    def clickbutton(self, description=None, buttonid=None, href=None, button=None, index=None, verbose=False):
        """
        Like ``.click()``, except looks for link-like buttons.
        This kind of button should look like
        ``<button onclick="...location.href='url'...">``.
        """
        __tracebackhide__ = True
        found_html, found_desc, found_attrs = self._find_element(tag='button', href_attr='onclick', href_extract=re.compile("location\\.href='(.*?)'"), content=description, id=buttonid, href_pattern=href, html_pattern=button, index=index, verbose=verbose)
        return self.goto(found_attrs['uri'])

    def _find_element(self, tag, href_attr, href_extract, content, id, href_pattern, html_pattern, index, verbose):
        content_pat = _make_pattern(content)
        id_pat = _make_pattern(id)
        href_pat = _make_pattern(href_pattern)
        html_pat = _make_pattern(html_pattern)
        body = self.testbody
        _tag_re = re.compile('<%s\\s+(.*?)>(.*?)</%s>' % (tag, tag), re.I + re.S)
        _script_re = re.compile('<script.*?>.*?</script>', re.I | re.S)
        bad_spans = []
        for match in _script_re.finditer(body):
            bad_spans.append((match.start(), match.end()))

        def printlog(s):
            if verbose:
                print s

        found_links = []
        total_links = 0
        for match in _tag_re.finditer(body):
            found_bad = False
            for bad_start, bad_end in bad_spans:
                if match.start() > bad_start and match.end() < bad_end:
                    found_bad = True
                    break

            if found_bad:
                continue
            el_html = match.group(0)
            el_attr = match.group(1)
            el_content = match.group(2)
            attrs = _parse_attrs(el_attr)
            if verbose:
                printlog('Element: %r' % el_html)
            if not attrs.get(href_attr):
                printlog('  Skipped: no %s attribute' % href_attr)
                continue
            el_href = attrs[href_attr]
            if href_extract:
                m = href_extract.search(el_href)
                if not m:
                    printlog("  Skipped: doesn't match extract pattern")
                    continue
                el_href = m.group(1)
            attrs['uri'] = el_href
            if el_href.startswith('#'):
                printlog('  Skipped: only internal fragment href')
                continue
            if el_href.startswith('javascript:'):
                printlog('  Skipped: cannot follow javascript:')
                continue
            total_links += 1
            if content_pat and not content_pat(el_content):
                printlog("  Skipped: doesn't match description")
                continue
            if id_pat and not id_pat(attrs.get('id', '')):
                printlog("  Skipped: doesn't match id")
                continue
            if href_pat and not href_pat(el_href):
                printlog("  Skipped: doesn't match href")
                continue
            if html_pat and not html_pat(el_html):
                printlog("  Skipped: doesn't match html")
                continue
            printlog('  Accepted')
            found_links.append((el_html, el_content, attrs))

        if not found_links:
            raise IndexError('No matching elements found (from %s possible)' % total_links)
        if index is None:
            if len(found_links) > 1:
                raise IndexError('Multiple links match: %s' % (', ').join([ repr(anc) for anc, d, attr in found_links ]))
            found_link = found_links[0]
        else:
            try:
                found_link = found_links[index]
            except IndexError:
                raise IndexError('Only %s (out of %s) links match; index %s out of range' % (
                 len(found_links), total_links, index))

        return found_link

    def goto--- This code section failed: ---

 L. 334         0  LOAD_GLOBAL           0  'urlparse'
                3  LOAD_ATTR             1  'urlsplit'
                6  LOAD_FAST             1  'href'
                9  CALL_FUNCTION_1       1  None
               12  UNPACK_SEQUENCE_5     5 
               15  STORE_FAST            4  'scheme'
               18  STORE_FAST            5  'host'
               21  STORE_FAST            6  'path'
               24  STORE_FAST            7  'query'
               27  STORE_FAST            8  'fragment'

 L. 336        30  LOAD_CONST               ''
               33  DUP_TOP          
               34  STORE_FAST            4  'scheme'
               37  DUP_TOP          
               38  STORE_FAST            5  'host'
               41  STORE_FAST            8  'fragment'

 L. 337        44  LOAD_GLOBAL           0  'urlparse'
               47  LOAD_ATTR             2  'urlunsplit'
               50  LOAD_FAST             4  'scheme'
               53  LOAD_FAST             5  'host'
               56  LOAD_FAST             6  'path'
               59  LOAD_FAST             7  'query'
               62  LOAD_FAST             8  'fragment'
               65  BUILD_TUPLE_5         5 
               68  CALL_FUNCTION_1       1  None
               71  STORE_FAST            1  'href'

 L. 338        74  LOAD_GLOBAL           0  'urlparse'
               77  LOAD_ATTR             3  'urljoin'
               80  LOAD_DEREF            0  'self'
               83  LOAD_ATTR             4  'request'
               86  LOAD_ATTR             5  'url'
               89  LOAD_FAST             1  'href'
               92  CALL_FUNCTION_2       2  None
               95  STORE_FAST            1  'href'

 L. 339        98  LOAD_FAST             2  'method'
              101  LOAD_ATTR             6  'lower'
              104  CALL_FUNCTION_0       0  None
              107  STORE_FAST            2  'method'

 L. 340       110  LOAD_FAST             2  'method'
              113  LOAD_CONST               ('get', 'post')
              116  COMPARE_OP            6  in
              119  POP_JUMP_IF_TRUE    135  'to 135'
              122  LOAD_ASSERT              AssertionError

 L. 341       125  LOAD_CONST               'Only "get" or "post" are allowed for method (you gave %r)'

 L. 342       128  LOAD_FAST             2  'method'
              131  BINARY_MODULO    
              132  RAISE_VARARGS_2       2  None

 L. 345       135  LOAD_GLOBAL           8  'PY3'
              138  UNARY_NOT        
              139  POP_JUMP_IF_FALSE   345  'to 345'
              142  LOAD_GLOBAL           9  'getattr'
              145  LOAD_DEREF            0  'self'
              148  LOAD_CONST               '_use_unicode'
              151  LOAD_GLOBAL          10  'False'
              154  CALL_FUNCTION_3       3  None
            157_0  COME_FROM           139  '139'
              157  POP_JUMP_IF_FALSE   345  'to 345'

 L. 346       160  LOAD_CLOSURE          0  'self'
              166  LOAD_CODE                <code_object to_str>
              169  MAKE_CLOSURE_0        0  None
              172  STORE_FAST            9  'to_str'

 L. 351       175  LOAD_FAST             9  'to_str'
              178  LOAD_FAST             1  'href'
              181  CALL_FUNCTION_1       1  None
              184  STORE_FAST            1  'href'

 L. 353       187  LOAD_CONST               'params'
              190  LOAD_FAST             3  'args'
              193  COMPARE_OP            6  in
              196  POP_JUMP_IF_FALSE   250  'to 250'

 L. 354       199  BUILD_LIST_0          0 

 L. 355       202  LOAD_FAST             3  'args'
              205  LOAD_CONST               'params'
              208  BINARY_SUBSCR    
              209  GET_ITER         
              210  FOR_ITER             27  'to 240'
              213  STORE_FAST           10  'p'
              216  LOAD_GLOBAL          11  'tuple'
              219  LOAD_GLOBAL          12  'map'
              222  LOAD_FAST             9  'to_str'
              225  LOAD_FAST            10  'p'
              228  CALL_FUNCTION_2       2  None
              231  CALL_FUNCTION_1       1  None
              234  LIST_APPEND           2  None
              237  JUMP_BACK           210  'to 210'
              240  LOAD_FAST             3  'args'
              243  LOAD_CONST               'params'
              246  STORE_SUBSCR     
              247  JUMP_FORWARD          0  'to 250'
            250_0  COME_FROM           247  '247'

 L. 357       250  LOAD_CONST               'upload_files'
              253  LOAD_FAST             3  'args'
              256  COMPARE_OP            6  in
              259  POP_JUMP_IF_FALSE   307  'to 307'

 L. 358       262  BUILD_LIST_0          0 

 L. 359       265  LOAD_FAST             3  'args'
              268  LOAD_CONST               'upload_files'
              271  BINARY_SUBSCR    
              272  GET_ITER         
              273  FOR_ITER             21  'to 297'
              276  STORE_FAST           11  'f'
              279  LOAD_GLOBAL          12  'map'
              282  LOAD_FAST             9  'to_str'
              285  LOAD_FAST            11  'f'
              288  CALL_FUNCTION_2       2  None
              291  LIST_APPEND           2  None
              294  JUMP_BACK           273  'to 273'
              297  LOAD_FAST             3  'args'
              300  LOAD_CONST               'upload_files'
              303  STORE_SUBSCR     
              304  JUMP_FORWARD          0  'to 307'
            307_0  COME_FROM           304  '304'

 L. 361       307  LOAD_CONST               'content_type'
              310  LOAD_FAST             3  'args'
              313  COMPARE_OP            6  in
              316  POP_JUMP_IF_FALSE   345  'to 345'

 L. 362       319  LOAD_FAST             9  'to_str'
              322  LOAD_FAST             3  'args'
              325  LOAD_CONST               'content_type'
              328  BINARY_SUBSCR    
              329  CALL_FUNCTION_1       1  None
              332  LOAD_FAST             3  'args'
              335  LOAD_CONST               'content_type'
              338  STORE_SUBSCR     
              339  JUMP_ABSOLUTE       345  'to 345'
              342  JUMP_FORWARD          0  'to 345'
            345_0  COME_FROM           342  '342'

 L. 364       345  LOAD_FAST             2  'method'
              348  LOAD_CONST               'get'
              351  COMPARE_OP            2  ==
              354  POP_JUMP_IF_FALSE   372  'to 372'

 L. 365       357  LOAD_DEREF            0  'self'
              360  LOAD_ATTR            13  'test_app'
              363  LOAD_ATTR            14  'get'
              366  STORE_FAST            2  'method'
              369  JUMP_FORWARD         12  'to 384'

 L. 367       372  LOAD_DEREF            0  'self'
              375  LOAD_ATTR            13  'test_app'
              378  LOAD_ATTR            15  'post'
              381  STORE_FAST            2  'method'
            384_0  COME_FROM           369  '369'

 L. 368       384  LOAD_FAST             2  'method'
              387  LOAD_FAST             1  'href'
              390  LOAD_FAST             3  'args'
              393  CALL_FUNCTION_KW_1     1  None
              396  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 396

    _normal_body_regex = re.compile(to_bytes('[ \\n\\r\\t]+'))
    _normal_body = None

    def normal_body__get(self):
        if self._normal_body is None:
            self._normal_body = self._normal_body_regex.sub(to_bytes(' '), self.body)
        return self._normal_body

    normal_body = property(normal_body__get, doc=('\n                           Return the whitespace-normalized body\n                           ').strip())

    def unicode_normal_body__get(self):
        if not self.charset:
            raise AttributeError('You cannot access Response.unicode_normal_body unless charset is set')
        return self.normal_body.decode(self.charset)

    unicode_normal_body = property(unicode_normal_body__get, doc=('\n        Return the whitespace-normalized body, as unicode\n        ').strip())

    def __contains__(self, s):
        """
        A response 'contains' a string if it is present in the body
        of the response.  Whitespace is normalized when searching
        for a string.
        """
        if not isinstance(s, string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                s = str(s)
        if isinstance(s, text_type) and not self.charset:
            s = to_bytes(s)
        if isinstance(s, text_type):
            body = self.unicode_body
            normal_body = self.unicode_normal_body
        else:
            body = self.body
            normal_body = self.normal_body
        return s in body or s in normal_body

    def mustcontain(self, *strings, **kw):
        """
        Assert that the response contains all of the strings passed
        in as arguments.

        Equivalent to::

            assert string in res
        """
        if 'no' in kw:
            no = kw['no']
            del kw['no']
            if isinstance(no, string_types):
                no = [
                 no]
        else:
            no = []
        if kw:
            raise TypeError("The only keyword argument allowed is 'no'")
        for s in strings:
            if s not in self:
                print_stderr('Actual response (no %r):' % s)
                print_stderr(str(self))
                raise IndexError('Body does not contain string %r' % s)

        for no_s in no:
            if no_s in self:
                print_stderr('Actual response (has %r)' % no_s)
                print_stderr(str(self))
                raise IndexError('Body contains bad string %r' % no_s)

    def __str__(self):
        simple_body = ('\n').join([ l for l in self.testbody.splitlines() if l.strip()
                                  ])
        headers = [ (self._normalize_header_name(n), v) for n, v in self.headerlist if n.lower() != 'content-length'
                  ]
        headers.sort()
        output = 'Response: %s\n%s\n%s' % (
         to_string(self.status),
         ('\n').join([ '%s: %s' % (n, v) for n, v in headers ]),
         simple_body)
        if not PY3 and isinstance(output, text_type):
            output = output.encode(self.charset or 'utf-8', 'replace')
        return output

    def _normalize_header_name(self, name):
        name = name.replace('-', ' ').title().replace(' ', '-')
        return name

    def __repr__(self):
        if self.content_type:
            ct = ' %s' % self.content_type
        else:
            ct = ''
        if self.body:
            br = repr(self.body)
            if len(br) > 18:
                br = br[:10] + '...' + br[-5:]
                br += '/%s' % len(self.body)
            body = ' body=%s' % br
        else:
            body = ' no body'
        if self.location:
            location = ' location: %s' % self.location
        else:
            location = ''
        return '<' + to_string(self.status) + ct + location + body + '>'

    def html(self):
        """
        Returns the response as a `BeautifulSoup
        <http://www.crummy.com/software/BeautifulSoup/documentation.html>`_
        object.

        Only works with HTML responses; other content-types raise
        AttributeError.
        """
        if 'html' not in self.content_type:
            raise AttributeError('Not an HTML response body (content-type: %s)' % self.content_type)
        try:
            from BeautifulSoup import BeautifulSoup
        except ImportError:
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                raise ImportError('You must have BeautifulSoup installed to use response.html')

        soup = BeautifulSoup(self.testbody)
        return soup

    html = property(html, doc=html.__doc__)

    def xml(self):
        """
        Returns the response as an `ElementTree
        <http://python.org/doc/current/lib/module-xml.etree.ElementTree.html>`_
        object.

        Only works with XML responses; other content-types raise
        AttributeError
        """
        if 'xml' not in self.content_type:
            raise AttributeError('Not an XML response body (content-type: %s)' % self.content_type)
        try:
            from xml.etree import ElementTree
        except ImportError:
            try:
                import ElementTree
            except ImportError:
                try:
                    from elementtree import ElementTree
                except ImportError:
                    raise ImportError('You must have ElementTree installed (or use Python 2.5) to use response.xml')

        return ElementTree.XML(self.body)

    xml = property(xml, doc=xml.__doc__)

    def lxml(self):
        """
        Returns the response as an `lxml object
        <http://codespeak.net/lxml/>`_.  You must have lxml installed
        to use this.

        If this is an HTML response and you have lxml 2.x installed,
        then an ``lxml.html.HTML`` object will be returned; if you
        have an earlier version of lxml then a ``lxml.HTML`` object
        will be returned.
        """
        if 'html' not in self.content_type and 'xml' not in self.content_type:
            raise AttributeError('Not an XML or HTML response body (content-type: %s)' % self.content_type)
        try:
            from lxml import etree
        except ImportError:
            raise ImportError('You must have lxml installed to use response.lxml')

        try:
            from lxml.html import fromstring
        except ImportError:
            fromstring = etree.HTML

        if self.content_type == 'text/html':
            return fromstring(self.testbody, base_url=self.request.url)
        else:
            return etree.XML(self.testbody, base_url=self.request.url)

    lxml = property(lxml, doc=lxml.__doc__)

    def json(self):
        """
        Return the response as a JSON response.  You must have `simplejson
        <http://goo.gl/B9g6s>`_ installed to use this, or be using a Python
        version with the json module.

        The content type must be application/json to use this.
        """
        if self.content_type != 'application/json':
            raise AttributeError('Not a JSON response body (content-type: %s)' % self.content_type)
        if loads is None:
            raise ImportError('You must have simplejson installed to use response.json')
        return loads(self.testbody)

    json = property(json, doc=json.__doc__)

    def pyquery(self):
        """
        Returns the response as a `PyQuery <http://pyquery.org/>`_ object.

        Only works with HTML and XML responses; other content-types raise
        AttributeError.
        """
        if 'html' not in self.content_type and 'xml' not in self.content_type:
            raise AttributeError('Not an HTML or XML response body (content-type: %s)' % self.content_type)
        try:
            from pyquery import PyQuery
        except ImportError:
            raise ImportError('You must have PyQuery installed to use response.pyquery')

        d = PyQuery(self.testbody)
        return d

    pyquery = property(pyquery, doc=pyquery.__doc__)

    def showbrowser(self):
        """
        Show this response in a browser window (for debugging purposes,
        when it's hard to read the HTML).
        """
        import webbrowser, tempfile
        f = tempfile.NamedTemporaryFile(prefix='webtest-page', suffix='.html')
        name = f.name
        f.close()
        f = open(name, 'w')
        f.write(to_string(self.body))
        f.close()
        if name[0] != '/':
            url = 'file:///' + name
        else:
            url = 'file://' + name
        webbrowser.open_new(url)


class TestRequest(Request):
    disabled = True
    ResponseClass = TestResponse


class TestApp(object):
    """
    Wraps a WSGI application in a more convenient interface for
    testing.

    ``app`` may be an application, or a Paste Deploy app
    URI, like ``'config:filename.ini#test'``.

    ``extra_environ`` is a dictionary of values that should go
    into the environment for each request.  These can provide a
    communication channel with the application.

    ``relative_to`` is a directory, and filenames used for file
    uploads are calculated relative to this.  Also ``config:``
    URIs that aren't absolute.
    """
    disabled = True
    RequestClass = TestRequest

    def __init__(self, app, extra_environ=None, relative_to=None, use_unicode=True):
        if isinstance(app, string_types):
            from paste.deploy import loadapp
            app = loadapp(app, relative_to=relative_to)
        self.app = app
        self.relative_to = relative_to
        if extra_environ is None:
            extra_environ = {}
        self.extra_environ = extra_environ
        self.use_unicode = use_unicode
        self.reset()
        return

    def reset(self):
        """
        Resets the state of the application; currently just clears
        saved cookies.
        """
        self.cookies = {}

    def _make_environ(self, extra_environ=None):
        environ = self.extra_environ.copy()
        environ['paste.throw_errors'] = True
        if extra_environ:
            environ.update(extra_environ)
        return environ

    def _remove_fragment(self, url):
        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        return urlparse.urlunsplit((scheme, netloc, path, query, ''))

    def get(self, url, params=None, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Get the given url (well, actually a path like
        ``'/page.html'``).

        ``params``:
            A query string, or a dictionary that will be encoded
            into a query string.  You may also include a query
            string on the ``url``.

        ``headers``:
            A dictionary of extra headers to send.

        ``extra_environ``:
            A dictionary of environmental variables that should
            be added to the request.

        ``status``:
            The integer status code you expect (if not 200 or 3xx).
            If you expect a 404 response, for instance, you must give
            ``status=404`` or it will be an error.  You can also give
            a wildcard, like ``'3*'`` or ``'*'``.

        ``expect_errors``:
            If this is not true, then if anything is written to
            ``wsgi.errors`` it will be an error.  If it is true, then
            non-200/3xx responses are also okay.

        Returns a :class:`webtest.TestResponse` object.
        """
        environ = self._make_environ(extra_environ)
        __tracebackhide__ = True
        url = str(url)
        url = self._remove_fragment(url)
        if params:
            if not isinstance(params, string_types):
                params = urlencode(params, doseq=True)
            if '?' in url:
                url += '&'
            else:
                url += '?'
            url += params
        if '?' in url:
            url, environ['QUERY_STRING'] = url.split('?', 1)
        else:
            environ['QUERY_STRING'] = ''
        req = self.RequestClass.blank(url, environ)
        if headers:
            req.headers.update(headers)
        return self.do_request(req, status=status, expect_errors=expect_errors)

    def _gen_request(self, method, url, params='', headers=None, extra_environ=None, status=None, upload_files=None, expect_errors=False, content_type=None):
        """
        Do a generic request.
        """
        environ = self._make_environ(extra_environ)
        inline_uploads = []
        if isinstance(params, dict) or hasattr(params, 'items'):
            params = list(params.items())
        if isinstance(params, (list, tuple)):
            inline_uploads = [ v for k, v in params if isinstance(v, (File, Upload)) ]
        if len(inline_uploads) > 0:
            content_type, params = self.encode_multipart(params, upload_files or ())
            environ['CONTENT_TYPE'] = content_type
        else:
            params = encode_params(params, content_type)
            if upload_files or content_type and to_string(content_type).startswith('multipart'):
                params = cgi.parse_qsl(params, keep_blank_values=True)
                content_type, params = self.encode_multipart(params, upload_files or ())
                environ['CONTENT_TYPE'] = content_type
            elif params:
                environ.setdefault('CONTENT_TYPE', 'application/x-www-form-urlencoded')
        if '?' in url:
            url, environ['QUERY_STRING'] = url.split('?', 1)
        else:
            environ['QUERY_STRING'] = ''
        if content_type is not None:
            environ['CONTENT_TYPE'] = content_type
        environ['CONTENT_LENGTH'] = str(len(params))
        environ['REQUEST_METHOD'] = method
        environ['wsgi.input'] = BytesIO(to_bytes(params))
        url = self._remove_fragment(url)
        req = self.RequestClass.blank(url, environ)
        if headers:
            req.headers.update(headers)
        return self.do_request(req, status=status, expect_errors=expect_errors)

    def post(self, url, params='', headers=None, extra_environ=None, status=None, upload_files=None, expect_errors=False, content_type=None):
        """
        Do a POST request.  Very like the ``.get()`` method.
        ``params`` are put in the body of the request.

        ``upload_files`` is for file uploads.  It should be a list of
        ``[(fieldname, filename, file_content)]``.  You can also use
        just ``[(fieldname, filename)]`` and the file content will be
        read from disk.

        For post requests params could be a collections.OrderedDict with
        Upload fields included in order:

            app.post('/myurl', collections.OrderedDict([
                ('textfield1', 'value1'),
                ('uploadfield', webapp.Upload('filename.txt', 'contents'),
                ('textfield2', 'value2')])))

        Returns a ``webob.Response`` object.
        """
        return self._gen_request('POST', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=upload_files, expect_errors=expect_errors, content_type=content_type)

    def post_json(self, url, params=NoDefault, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Do a POST request.  Very like the ``.get()`` method.
        ``params`` are dumps to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a ``webob.Response`` object.
        """
        content_type = 'application/json'
        if params is not NoDefault:
            params = dumps(params)
        return self._gen_request('POST', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors, content_type=content_type)

    def put(self, url, params='', headers=None, extra_environ=None, status=None, upload_files=None, expect_errors=False, content_type=None):
        """
        Do a PUT request.  Very like the ``.post()`` method.
        ``params`` are put in the body of the request, if params is a
        tuple, dictionary, list, or iterator it will be urlencoded and
        placed in the body as with a POST, if it is string it will not
        be encoded, but placed in the body directly.

        Returns a ``webob.Response`` object.
        """
        return self._gen_request('PUT', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=upload_files, expect_errors=expect_errors, content_type=content_type)

    def put_json(self, url, params=NoDefault, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Do a PUT request.  Very like the ``.post()`` method.
        ``params`` are dumps to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a ``webob.Response`` object.
        """
        content_type = 'application/json'
        if params is not NoDefault:
            params = dumps(params)
        return self._gen_request('PUT', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors, content_type=content_type)

    def delete(self, url, params='', headers=None, extra_environ=None, status=None, expect_errors=False, content_type=None):
        """
        Do a DELETE request.  Very like the ``.get()`` method.

        Returns a ``webob.Response`` object.
        """
        if params:
            warnings.warn('You are not supposed to send a body in a DELETE request. Most web servers will ignore it', lint.WSGIWarning)
        return self._gen_request('DELETE', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors, content_type=content_type)

    def delete_json(self, url, params=NoDefault, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Do a DELETE request.  Very like the ``.get()`` method.
        Content-Type is set to ``application/json``.

        Returns a ``webob.Response`` object.
        """
        if params:
            warnings.warn('You are not supposed to send a body in a DELETE request. Most web servers will ignore it', lint.WSGIWarning)
        content_type = 'application/json'
        if params is not NoDefault:
            params = dumps(params)
        return self._gen_request('DELETE', url, params=params, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors, content_type=content_type)

    def options(self, url, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Do a OPTIONS request.  Very like the ``.get()`` method.

        Returns a ``webob.Response`` object.
        """
        return self._gen_request('OPTIONS', url, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors)

    def head(self, url, headers=None, extra_environ=None, status=None, expect_errors=False):
        """
        Do a HEAD request.  Very like the ``.get()`` method.

        Returns a ``webob.Response`` object.
        """
        return self._gen_request('HEAD', url, headers=headers, extra_environ=extra_environ, status=status, upload_files=None, expect_errors=expect_errors)

    def encode_multipart(self, params, files):
        """
        Encodes a set of parameters (typically a name/value list) and
        a set of files (a list of (name, filename, file_body)) into a
        typical POST body, returning the (content_type, body).
        """
        boundary = '----------a_BoUnDaRy%s$' % random.random()
        lines = []

        def _append_value(key, value):
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.append('')
            lines.append(value)

        def _append_file(file_info):
            key, filename, value = self._get_file_info(file_info)
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (
             key, filename))
            fcontent = mimetypes.guess_type(filename)[0]
            lines.append('Content-Type: %s' % (fcontent or 'application/octet-stream'))
            lines.append('')
            lines.append(value)

        for key, value in params:
            if isinstance(value, File):
                if value.value:
                    _append_file([key] + list(value.value))
            elif isinstance(value, Upload):
                file_info = [
                 key, value.filename]
                if value.file_content is not None:
                    file_info.append(value.file_content)
                _append_file(file_info)
            else:
                _append_value(key, value)

        for file_info in files:
            _append_file(file_info)

        lines.append('--' + boundary + '--')
        lines.append('')
        body = join_bytes('\r\n', lines)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return (content_type, body)

    def _get_file_info(self, file_info):
        if len(file_info) == 2:
            filename = file_info[1]
            if self.relative_to:
                filename = os.path.join(self.relative_to, filename)
            f = open(filename, 'rb')
            content = f.read()
            if PY3 and isinstance(content, text_type):
                content = content.encode(f.encoding)
            f.close()
            return (
             file_info[0], filename, content)
        if len(file_info) == 3:
            content = file_info[2]
            if not isinstance(content, binary_type):
                raise ValueError('File content must be %s not %s' % (
                 binary_type, type(content)))
            return file_info
        raise ValueError('upload_files need to be a list of tuples of (fieldname, filename, filecontent) or (fieldname, filename); you gave: %r' % repr(file_info)[:100])

    def request(self, url_or_req, status=None, expect_errors=False, **req_params):
        """
        Creates and executes a request.  You may either pass in an
        instantiated :class:`TestRequest` object, or you may pass in a
        URL and keyword arguments to be passed to
        :meth:`TestRequest.blank`.

        You can use this to run a request without the intermediary
        functioning of :meth:`TestApp.get` etc.  For instance, to
        test a WebDAV method::

            resp = app.request('/new-col', method='MKCOL')

        Note that the request won't have a body unless you specify it,
        like::

            resp = app.request('/test.txt', method='PUT', body='test')

        You can use ``POST={args}`` to set the request body to the
        serialized arguments, and simultaneously set the request
        method to ``POST``
        """
        if isinstance(url_or_req, string_types):
            req = self.RequestClass.blank(url_or_req, **req_params)
        else:
            req = url_or_req.copy()
            for name, value in req_params.items():
                setattr(req, name, value)

            if req.content_length == -1:
                req.content_length = len(req.body)
            req.environ['paste.throw_errors'] = True
            for name, value in self.extra_environ.items():
                req.environ.setdefault(name, value)

        return self.do_request(req, status=status, expect_errors=expect_errors)

    def do_request(self, req, status, expect_errors):
        """
        Executes the given request (``req``), with the expected
        ``status``.  Generally ``.get()`` and ``.post()`` are used
        instead.

        To use this::

            resp = app.do_request(webtest.TestRequest.blank(
                'url', ...args...))

        Note you can pass any keyword arguments to
        ``TestRequest.blank()``, which will be set on the request.
        These can be arguments like ``content_type``, ``accept``, etc.
        """
        __tracebackhide__ = True
        errors = StringIO()
        req.environ['wsgi.errors'] = errors
        script_name = req.environ.get('SCRIPT_NAME', '')
        if script_name and req.path_info.startswith(script_name):
            req.path_info = req.path_info[len(script_name):]
        cookies = self.cookies or {}
        cookies = list(cookies.items())
        if 'Cookie' in req.headers:
            req_cookies = [ i.strip() for i in req.headers['Cookie'].split(';') ]
            req_cookies = [ i.split('=') for i in req_cookies ]
            cookies.extend(req_cookies)
        if cookies:
            cookie_header = ('').join([ '%s=%s; ' % (name, cookie_quote(value)) for name, value in cookies
                                      ])
            req.environ['HTTP_COOKIE'] = cookie_header
        req.environ['paste.testing'] = True
        req.environ['paste.testing_variables'] = {}
        app = lint.middleware(self.app)
        res = req.get_response(app, catch_exc_info=True)
        res._use_unicode = self.use_unicode
        res.request = req
        res.app = app
        res.test_app = self
        try:
            res.body
        except TypeError:
            pass

        res.errors = errors.getvalue()
        for name, value in req.environ['paste.testing_variables'].items():
            if hasattr(res, name):
                raise ValueError('paste.testing_variables contains the variable %r, but the response object already has an attribute by that name' % name)
            setattr(res, name, value)

        if not expect_errors:
            self._check_status(status, res)
            self._check_errors(res)
        res.cookies_set = {}
        for header in res.headers.getall('set-cookie'):
            try:
                c = SimpleCookie(header)
            except CookieError:
                raise CookieError('Could not parse cookie header %r' % (header,))

            for key, morsel in c.items():
                self.cookies[key] = morsel.value
                res.cookies_set[key] = morsel.value

        return res

    def _check_status(self, status, res):
        __tracebackhide__ = True
        if status == '*':
            return
        else:
            res_status = to_string(res.status)
            if isinstance(status, string_types) and '*' in status:
                if re.match(fnmatch.translate(status), res_status, re.I):
                    return
            if isinstance(status, (list, tuple)):
                if res.status_int not in status:
                    raise AppError('Bad response: %s (not one of %s for %s)\n%s', res_status, (', ').join(map(str, status)), res.request.url, res)
                return
            if status is None:
                if res.status_int >= 200 and res.status_int < 400:
                    return
                raise AppError('Bad response: %s (not 200 OK or 3xx redirect for %s)\n%s', res_status, res.request.url, res)
            if status != res.status_int:
                raise AppError('Bad response: %s (not %s)', res_status, status)
            return

    def _check_errors(self, res):
        errors = res.errors
        if errors:
            raise AppError('Application had errors logged:\n%s', errors)


_attr_re = re.compile('([^= \\n\\r\\t]+)[ \\n\\r\\t]*(?:=[ \\n\\r\\t]*(?:"([^"]*)"|\\\'([^\\\']*)\\\'|([^"\\\'][^ \\n\\r\\t>]*)))?', re.S)

def _parse_attrs(text):
    attrs = {}
    for match in _attr_re.finditer(text):
        attr_name = match.group(1).lower()
        attr_body = match.group(2) or match.group(3)
        attr_body = html_unquote(attr_body or '')
        attrs[str(attr_name)] = attr_body

    return attrs


class Upload(object):

    def __init__(self, filename, file_content=None):
        self.filename = filename
        self.file_content = file_content


class Field(object):
    """
    Field object.
    """
    classes = {}
    settable = True

    def __init__(self, form, tag, name, pos, value=None, id=None, **attrs):
        self.form = form
        self.tag = tag
        self.name = name
        self.pos = pos
        self._value = value
        self.id = id
        self.attrs = attrs

    def value__set(self, value):
        if not self.settable:
            raise AttributeError('You cannot set the value of the <%s> field %r' % (
             self.tag, self.name))
        self._value = value

    def force_value(self, value):
        """
        Like setting a value, except forces it even for, say, hidden
        fields.
        """
        self._value = value

    def value__get(self):
        return self._value

    value = property(value__get, value__set)

    def __repr__(self):
        value = '<%s name="%s"' % (self.__class__.__name__, self.name)
        if self.id:
            value += ' id="%s"' % self.id
        return value + '>'


class NoValue(object):
    pass


class Select(Field):
    """
    Field representing ``<select>``
    """

    def __init__(self, *args, **attrs):
        super(Select, self).__init__(*args, **attrs)
        self.options = []
        self.selectedIndex = None
        self._forced_value = NoValue
        return

    def force_value(self, value):
        self._forced_value = value

    def value__set(self, value):
        if self._forced_value is not NoValue:
            self._forced_value = NoValue
        for i, (option, checked) in enumerate(self.options):
            if option == _stringify(value):
                self.selectedIndex = i
                break
        else:
            raise ValueError('Option %r not found (from %s)' % (
             value, (', ').join([ repr(o) for o, c in self.options ])))

    def value__get(self):
        if self._forced_value is not NoValue:
            return self._forced_value
        else:
            if self.selectedIndex is not None:
                return self.options[self.selectedIndex][0]
            for option, checked in self.options:
                if checked:
                    return option
            else:
                if self.options:
                    return self.options[0][0]
                else:
                    return

            return

    value = property(value__get, value__set)


Field.classes['select'] = Select

class MultipleSelect(Field):
    """
    Field representing ``<select multiple="multiple">``
    """

    def __init__(self, *args, **attrs):
        super(MultipleSelect, self).__init__(*args, **attrs)
        self.options = []
        self.selectedIndices = []
        self._forced_values = []

    def force_value(self, values):
        self._forced_values = values
        self.selectedIndices = []

    def value__set(self, values):
        str_values = [ _stringify(value) for value in values ]
        self.selectedIndices = []
        for i, (option, checked) in enumerate(self.options):
            if option in str_values:
                self.selectedIndices.append(i)
                str_values.remove(option)

        if str_values:
            raise ValueError('Option(s) %r not found (from %s)' % (
             (', ').join(str_values),
             (', ').join([ repr(o) for o, c in self.options ])))

    def value__get(self):
        selected_values = []
        if self.selectedIndices:
            selected_values = [ self.options[i][0] for i in self.selectedIndices ]
        elif not self._forced_values:
            selected_values = []
            for option, checked in self.options:
                if checked:
                    selected_values.append(option)

        if self._forced_values:
            selected_values += self._forced_values
        if self.options and not selected_values:
            selected_values = None
        return selected_values

    value = property(value__get, value__set)


Field.classes['multiple_select'] = MultipleSelect

class Radio(Select):
    """
    Field representing ``<input type="radio">``
    """

    def value__get(self):
        if self._forced_value is not NoValue:
            self._forced_value = NoValue
        if self.selectedIndex is not None:
            return self.options[self.selectedIndex][0]
        else:
            for option, checked in self.options:
                if checked:
                    return option
            else:
                return

            return

    value = property(value__get, Select.value__set)


Field.classes['radio'] = Radio

class Checkbox(Field):
    """
    Field representing ``<input type="checkbox">``
    """

    def __init__(self, *args, **attrs):
        super(Checkbox, self).__init__(*args, **attrs)
        self.checked = 'checked' in attrs

    def value__set(self, value):
        self.checked = not not value

    def value__get(self):
        if self.checked:
            if self._value is None:
                return 'on'
            else:
                return self._value

        else:
            return
        return

    value = property(value__get, value__set)


Field.classes['checkbox'] = Checkbox

class Text(Field):
    """
    Field representing ``<input type="text">``
    """

    def value__get(self):
        if self._value is None:
            return ''
        else:
            return self._value
            return

    value = property(value__get, Field.value__set)


Field.classes['text'] = Text

class File(Field):
    """
    Field representing ``<input type="file">``
    """

    def value__get(self):
        if self._value is None:
            return ''
        else:
            return self._value
            return

    value = property(value__get, Field.value__set)


Field.classes['file'] = File

class Textarea(Text):
    """
    Field representing ``<textarea>``
    """
    pass


Field.classes['textarea'] = Textarea

class Hidden(Text):
    """
    Field representing ``<input type="hidden">``
    """
    pass


Field.classes['hidden'] = Hidden

class Submit(Field):
    """
    Field representing ``<input type="submit">`` and ``<button>``
    """
    settable = False

    def value__get(self):
        return

    value = property(value__get)

    def value_if_submitted(self):
        return self._value


Field.classes['submit'] = Submit
Field.classes['button'] = Submit
Field.classes['image'] = Submit

class Form(object):
    """
    This object represents a form that has been found in a page.
    This has a couple useful attributes:

    ``text``:
        the full HTML of the form.

    ``action``:
        the relative URI of the action.

    ``method``:
        the method (e.g., ``'GET'``).

    ``id``:
        the id, or None if not given.

    ``fields``:
        a dictionary of fields, each value is a list of fields by
        that name.  ``<input type="radio">`` and ``<select>`` are
        both represented as single fields with multiple options.
    """
    _tag_re = re.compile('<(/?)([a-z0-9_\\-]*)([^>]*?)>', re.I)
    _label_re = re.compile('<label\\s+(?:[^>]*)for=(?:"|\')([a-z0-9_\\-]+)(?:"|\')(?:[^>]*)>', re.I)
    FieldClass = Field

    def __init__(self, response, text):
        self.response = response
        self.text = text
        self._parse_fields()
        self._parse_action()

    def _parse_fields--- This code section failed: ---

 L.1510         0  LOAD_CONST               None
                3  STORE_FAST            1  'in_select'

 L.1511         6  LOAD_CONST               None
                9  STORE_FAST            2  'in_textarea'

 L.1512        12  LOAD_GLOBAL           1  'OrderedDict'
               15  CALL_FUNCTION_0       0  None
               18  STORE_FAST            3  'fields'

 L.1513        21  SETUP_LOOP          879  'to 903'
               24  LOAD_FAST             0  'self'
               27  LOAD_ATTR             2  '_tag_re'
               30  LOAD_ATTR             3  'finditer'
               33  LOAD_FAST             0  'self'
               36  LOAD_ATTR             4  'text'
               39  CALL_FUNCTION_1       1  None
               42  GET_ITER         
               43  FOR_ITER            856  'to 902'
               46  STORE_FAST            4  'match'

 L.1514        49  LOAD_FAST             4  'match'
               52  LOAD_ATTR             5  'group'
               55  LOAD_CONST               1
               58  CALL_FUNCTION_1       1  None
               61  LOAD_CONST               '/'
               64  COMPARE_OP            2  ==
               67  STORE_FAST            5  'end'

 L.1515        70  LOAD_FAST             4  'match'
               73  LOAD_ATTR             5  'group'
               76  LOAD_CONST               2
               79  CALL_FUNCTION_1       1  None
               82  LOAD_ATTR             6  'lower'
               85  CALL_FUNCTION_0       0  None
               88  STORE_FAST            6  'tag'

 L.1516        91  LOAD_FAST             6  'tag'

 L.1517        94  LOAD_CONST               ('input', 'select', 'option', 'textarea', 'button')
               97  COMPARE_OP            7  not-in
              100  POP_JUMP_IF_FALSE   109  'to 109'

 L.1518       103  CONTINUE             43  'to 43'
              106  JUMP_FORWARD          0  'to 109'
            109_0  COME_FROM           106  '106'

 L.1519       109  LOAD_FAST             6  'tag'
              112  LOAD_CONST               'select'
              115  COMPARE_OP            2  ==
              118  POP_JUMP_IF_FALSE   167  'to 167'
              121  LOAD_FAST             5  'end'
            124_0  COME_FROM           118  '118'
              124  POP_JUMP_IF_FALSE   167  'to 167'

 L.1520       127  LOAD_FAST             1  'in_select'
              130  POP_JUMP_IF_TRUE    155  'to 155'
              133  LOAD_ASSERT              AssertionError

 L.1521       136  LOAD_CONST               '%r without starting select'
              139  LOAD_FAST             4  'match'
              142  LOAD_ATTR             5  'group'
              145  LOAD_CONST               0
              148  CALL_FUNCTION_1       1  None
              151  BINARY_MODULO    
              152  RAISE_VARARGS_2       2  None

 L.1522       155  LOAD_CONST               None
              158  STORE_FAST            1  'in_select'

 L.1523       161  CONTINUE             43  'to 43'
              164  JUMP_FORWARD          0  'to 167'
            167_0  COME_FROM           164  '164'

 L.1524       167  LOAD_FAST             6  'tag'
              170  LOAD_CONST               'textarea'
              173  COMPARE_OP            2  ==
              176  POP_JUMP_IF_FALSE   261  'to 261'
              179  LOAD_FAST             5  'end'
            182_0  COME_FROM           176  '176'
              182  POP_JUMP_IF_FALSE   261  'to 261'

 L.1525       185  LOAD_FAST             2  'in_textarea'
              188  POP_JUMP_IF_TRUE    210  'to 210'
              191  LOAD_ASSERT              AssertionError

 L.1526       194  LOAD_CONST               '</textarea> with no <textarea> at %s'
              197  LOAD_FAST             4  'match'
              200  LOAD_ATTR             8  'start'
              203  CALL_FUNCTION_0       0  None
              206  BINARY_MODULO    
              207  RAISE_VARARGS_2       2  None

 L.1527       210  LOAD_GLOBAL           9  'html_unquote'

 L.1528       213  LOAD_FAST             0  'self'
              216  LOAD_ATTR             4  'text'
              219  LOAD_FAST             2  'in_textarea'
              222  LOAD_CONST               1
              225  BINARY_SUBSCR    
              226  LOAD_FAST             4  'match'
              229  LOAD_ATTR             8  'start'
              232  CALL_FUNCTION_0       0  None
              235  SLICE+3          
              236  CALL_FUNCTION_1       1  None
              239  LOAD_FAST             2  'in_textarea'
              242  LOAD_CONST               0
              245  BINARY_SUBSCR    
              246  STORE_ATTR           10  'value'

 L.1529       249  LOAD_CONST               None
              252  STORE_FAST            2  'in_textarea'

 L.1530       255  CONTINUE             43  'to 43'
              258  JUMP_FORWARD          0  'to 261'
            261_0  COME_FROM           258  '258'

 L.1531       261  LOAD_FAST             5  'end'
              264  POP_JUMP_IF_FALSE   273  'to 273'

 L.1532       267  CONTINUE             43  'to 43'
              270  JUMP_FORWARD          0  'to 273'
            273_0  COME_FROM           270  '270'

 L.1533       273  LOAD_GLOBAL          11  '_parse_attrs'
              276  LOAD_FAST             4  'match'
              279  LOAD_ATTR             5  'group'
              282  LOAD_CONST               3
              285  CALL_FUNCTION_1       1  None
              288  CALL_FUNCTION_1       1  None
              291  STORE_FAST            7  'attrs'

 L.1534       294  LOAD_CONST               'name'
              297  LOAD_FAST             7  'attrs'
              300  COMPARE_OP            6  in
              303  POP_JUMP_IF_FALSE   324  'to 324'

 L.1535       306  LOAD_FAST             7  'attrs'
              309  LOAD_ATTR            12  'pop'
              312  LOAD_CONST               'name'
              315  CALL_FUNCTION_1       1  None
              318  STORE_FAST            8  'name'
              321  JUMP_FORWARD          6  'to 330'

 L.1537       324  LOAD_CONST               None
              327  STORE_FAST            8  'name'
            330_0  COME_FROM           321  '321'

 L.1538       330  LOAD_FAST             6  'tag'
              333  LOAD_CONST               'option'
              336  COMPARE_OP            2  ==
              339  POP_JUMP_IF_FALSE   385  'to 385'

 L.1539       342  LOAD_FAST             1  'in_select'
              345  LOAD_ATTR            13  'options'
              348  LOAD_ATTR            14  'append'
              351  LOAD_FAST             7  'attrs'
              354  LOAD_ATTR            15  'get'
              357  LOAD_CONST               'value'
              360  CALL_FUNCTION_1       1  None

 L.1540       363  LOAD_CONST               'selected'
              366  LOAD_FAST             7  'attrs'
              369  COMPARE_OP            6  in
              372  BUILD_TUPLE_2         2 
              375  CALL_FUNCTION_1       1  None
              378  POP_TOP          

 L.1541       379  CONTINUE             43  'to 43'
              382  JUMP_FORWARD          0  'to 385'
            385_0  COME_FROM           382  '382'

 L.1542       385  LOAD_FAST             6  'tag'
              388  LOAD_CONST               'input'
              391  COMPARE_OP            2  ==
              394  POP_JUMP_IF_FALSE   591  'to 591'
              397  LOAD_FAST             7  'attrs'
              400  LOAD_ATTR            15  'get'
              403  LOAD_CONST               'type'
              406  CALL_FUNCTION_1       1  None
              409  LOAD_CONST               'radio'
              412  COMPARE_OP            2  ==
            415_0  COME_FROM           394  '394'
              415  POP_JUMP_IF_FALSE   591  'to 591'

 L.1543       418  LOAD_FAST             3  'fields'
              421  LOAD_ATTR            15  'get'
              424  LOAD_FAST             8  'name'
              427  CALL_FUNCTION_1       1  None
              430  STORE_FAST            9  'field'

 L.1544       433  LOAD_FAST             9  'field'
              436  POP_JUMP_IF_TRUE    507  'to 507'

 L.1545       439  LOAD_FAST             0  'self'
              442  LOAD_ATTR            16  'FieldClass'
              445  LOAD_ATTR            17  'classes'
              448  LOAD_CONST               'radio'
              451  BINARY_SUBSCR    

 L.1546       452  LOAD_FAST             0  'self'
              455  LOAD_FAST             6  'tag'
              458  LOAD_FAST             8  'name'
              461  LOAD_FAST             4  'match'
              464  LOAD_ATTR             8  'start'
              467  CALL_FUNCTION_0       0  None
              470  LOAD_FAST             7  'attrs'
              473  CALL_FUNCTION_KW_4     4  None
              476  STORE_FAST            9  'field'

 L.1547       479  LOAD_FAST             3  'fields'
              482  LOAD_ATTR            18  'setdefault'
              485  LOAD_FAST             8  'name'
              488  BUILD_LIST_0          0 
              491  CALL_FUNCTION_2       2  None
              494  LOAD_ATTR            14  'append'
              497  LOAD_FAST             9  'field'
              500  CALL_FUNCTION_1       1  None
              503  POP_TOP          
              504  JUMP_FORWARD         41  'to 548'

 L.1549       507  LOAD_FAST             9  'field'
              510  LOAD_CONST               0
              513  BINARY_SUBSCR    
              514  STORE_FAST            9  'field'

 L.1550       517  LOAD_GLOBAL          19  'isinstance'
              520  LOAD_FAST             9  'field'
              523  LOAD_FAST             0  'self'
              526  LOAD_ATTR            16  'FieldClass'
              529  LOAD_ATTR            17  'classes'
              532  LOAD_CONST               'radio'
              535  BINARY_SUBSCR    
              536  CALL_FUNCTION_2       2  None
              539  POP_JUMP_IF_TRUE    548  'to 548'
              542  LOAD_ASSERT              AssertionError
              545  RAISE_VARARGS_1       1  None
            548_0  COME_FROM           504  '504'

 L.1551       548  LOAD_FAST             9  'field'
              551  LOAD_ATTR            13  'options'
              554  LOAD_ATTR            14  'append'
              557  LOAD_FAST             7  'attrs'
              560  LOAD_ATTR            15  'get'
              563  LOAD_CONST               'value'
              566  CALL_FUNCTION_1       1  None

 L.1552       569  LOAD_CONST               'checked'
              572  LOAD_FAST             7  'attrs'
              575  COMPARE_OP            6  in
              578  BUILD_TUPLE_2         2 
              581  CALL_FUNCTION_1       1  None
              584  POP_TOP          

 L.1553       585  CONTINUE             43  'to 43'
              588  JUMP_FORWARD          0  'to 591'
            591_0  COME_FROM           588  '588'

 L.1554       591  LOAD_FAST             6  'tag'
              594  STORE_FAST           10  'tag_type'

 L.1555       597  LOAD_FAST             6  'tag'
              600  LOAD_CONST               'input'
              603  COMPARE_OP            2  ==
              606  POP_JUMP_IF_FALSE   636  'to 636'

 L.1556       609  LOAD_FAST             7  'attrs'
              612  LOAD_ATTR            15  'get'
              615  LOAD_CONST               'type'
              618  LOAD_CONST               'text'
              621  CALL_FUNCTION_2       2  None
              624  LOAD_ATTR             6  'lower'
              627  CALL_FUNCTION_0       0  None
              630  STORE_FAST           10  'tag_type'
              633  JUMP_FORWARD          0  'to 636'
            636_0  COME_FROM           633  '633'

 L.1557       636  LOAD_FAST            10  'tag_type'
              639  LOAD_CONST               'select'
              642  COMPARE_OP            2  ==
              645  POP_JUMP_IF_FALSE   693  'to 693'
              648  LOAD_FAST             7  'attrs'
              651  LOAD_ATTR            15  'get'
              654  LOAD_CONST               'multiple'
              657  CALL_FUNCTION_1       1  None
            660_0  COME_FROM           645  '645'
              660  POP_JUMP_IF_FALSE   693  'to 693'

 L.1558       663  LOAD_FAST             0  'self'
              666  LOAD_ATTR            16  'FieldClass'
              669  LOAD_ATTR            17  'classes'
              672  LOAD_ATTR            15  'get'
              675  LOAD_CONST               'multiple_select'

 L.1559       678  LOAD_FAST             0  'self'
              681  LOAD_ATTR            16  'FieldClass'
              684  CALL_FUNCTION_2       2  None
              687  STORE_FAST           11  'FieldClass'
              690  JUMP_FORWARD         27  'to 720'

 L.1561       693  LOAD_FAST             0  'self'
              696  LOAD_ATTR            16  'FieldClass'
              699  LOAD_ATTR            17  'classes'
              702  LOAD_ATTR            15  'get'
              705  LOAD_FAST            10  'tag_type'

 L.1562       708  LOAD_FAST             0  'self'
              711  LOAD_ATTR            16  'FieldClass'
              714  CALL_FUNCTION_2       2  None
              717  STORE_FAST           11  'FieldClass'
            720_0  COME_FROM           690  '690'

 L.1563       720  LOAD_FAST            11  'FieldClass'
              723  LOAD_FAST             0  'self'
              726  LOAD_FAST             6  'tag'
              729  LOAD_FAST             8  'name'
              732  LOAD_FAST             4  'match'
              735  LOAD_ATTR             8  'start'
              738  CALL_FUNCTION_0       0  None
              741  LOAD_FAST             7  'attrs'
              744  CALL_FUNCTION_KW_4     4  None
              747  STORE_FAST            9  'field'

 L.1564       750  LOAD_FAST             6  'tag'
              753  LOAD_CONST               'textarea'
              756  COMPARE_OP            2  ==
              759  POP_JUMP_IF_FALSE   818  'to 818'

 L.1565       762  LOAD_FAST             2  'in_textarea'
              765  UNARY_NOT        
              766  POP_JUMP_IF_TRUE    797  'to 797'
              769  LOAD_ASSERT              AssertionError

 L.1566       772  LOAD_CONST               'Nested textareas: %r and %r'

 L.1567       775  LOAD_FAST             2  'in_textarea'
              778  LOAD_FAST             4  'match'
              781  LOAD_ATTR             5  'group'
              784  LOAD_CONST               0
              787  CALL_FUNCTION_1       1  None
              790  BUILD_TUPLE_2         2 
              793  BINARY_MODULO    
              794  RAISE_VARARGS_2       2  None

 L.1568       797  LOAD_FAST             9  'field'
              800  LOAD_FAST             4  'match'
              803  LOAD_ATTR            20  'end'
              806  CALL_FUNCTION_0       0  None
              809  BUILD_TUPLE_2         2 
              812  STORE_FAST            2  'in_textarea'
              815  JUMP_FORWARD         56  'to 874'

 L.1569       818  LOAD_FAST             6  'tag'
              821  LOAD_CONST               'select'
              824  COMPARE_OP            2  ==
              827  POP_JUMP_IF_FALSE   874  'to 874'

 L.1570       830  LOAD_FAST             1  'in_select'
              833  UNARY_NOT        
              834  POP_JUMP_IF_TRUE    865  'to 865'
              837  LOAD_ASSERT              AssertionError

 L.1571       840  LOAD_CONST               'Nested selects: %r and %r'

 L.1572       843  LOAD_FAST             1  'in_select'
              846  LOAD_FAST             4  'match'
              849  LOAD_ATTR             5  'group'
              852  LOAD_CONST               0
              855  CALL_FUNCTION_1       1  None
              858  BUILD_TUPLE_2         2 
              861  BINARY_MODULO    
              862  RAISE_VARARGS_2       2  None

 L.1573       865  LOAD_FAST             9  'field'
              868  STORE_FAST            1  'in_select'
              871  JUMP_FORWARD          0  'to 874'
            874_0  COME_FROM           871  '871'
            874_1  COME_FROM           815  '815'

 L.1574       874  LOAD_FAST             3  'fields'
              877  LOAD_ATTR            18  'setdefault'
              880  LOAD_FAST             8  'name'
              883  BUILD_LIST_0          0 
              886  CALL_FUNCTION_2       2  None
              889  LOAD_ATTR            14  'append'
              892  LOAD_FAST             9  'field'
              895  CALL_FUNCTION_1       1  None
              898  POP_TOP          
              899  JUMP_BACK            43  'to 43'
              902  POP_BLOCK        
            903_0  COME_FROM            21  '21'

 L.1575       903  LOAD_FAST             3  'fields'
              906  LOAD_FAST             0  'self'
              909  STORE_ATTR           21  'fields'
              912  LOAD_CONST               None
              915  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 902

    def _parse_action--- This code section failed: ---

 L.1578         0  LOAD_CONST               None
                3  LOAD_FAST             0  'self'
                6  STORE_ATTR            1  'action'

 L.1579         9  SETUP_LOOP          216  'to 228'
               12  LOAD_FAST             0  'self'
               15  LOAD_ATTR             2  '_tag_re'
               18  LOAD_ATTR             3  'finditer'
               21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             4  'text'
               27  CALL_FUNCTION_1       1  None
               30  GET_ITER         
               31  FOR_ITER            178  'to 212'
               34  STORE_FAST            1  'match'

 L.1580        37  LOAD_FAST             1  'match'
               40  LOAD_ATTR             5  'group'
               43  LOAD_CONST               1
               46  CALL_FUNCTION_1       1  None
               49  LOAD_CONST               '/'
               52  COMPARE_OP            2  ==
               55  STORE_FAST            2  'end'

 L.1581        58  LOAD_FAST             1  'match'
               61  LOAD_ATTR             5  'group'
               64  LOAD_CONST               2
               67  CALL_FUNCTION_1       1  None
               70  LOAD_ATTR             6  'lower'
               73  CALL_FUNCTION_0       0  None
               76  STORE_FAST            3  'tag'

 L.1582        79  LOAD_FAST             3  'tag'
               82  LOAD_CONST               'form'
               85  COMPARE_OP            3  !=
               88  POP_JUMP_IF_FALSE    97  'to 97'

 L.1583        91  CONTINUE             31  'to 31'
               94  JUMP_FORWARD          0  'to 97'
             97_0  COME_FROM            94  '94'

 L.1584        97  LOAD_FAST             2  'end'
              100  POP_JUMP_IF_FALSE   107  'to 107'

 L.1585       103  BREAK_LOOP       
              104  JUMP_FORWARD          0  'to 107'
            107_0  COME_FROM           104  '104'

 L.1586       107  LOAD_GLOBAL           7  '_parse_attrs'
              110  LOAD_FAST             1  'match'
              113  LOAD_ATTR             5  'group'
              116  LOAD_CONST               3
              119  CALL_FUNCTION_1       1  None
              122  CALL_FUNCTION_1       1  None
              125  STORE_FAST            4  'attrs'

 L.1587       128  LOAD_FAST             4  'attrs'
              131  LOAD_ATTR             8  'get'
              134  LOAD_CONST               'action'
              137  LOAD_CONST               ''
              140  CALL_FUNCTION_2       2  None
              143  LOAD_FAST             0  'self'
              146  STORE_ATTR            1  'action'

 L.1588       149  LOAD_FAST             4  'attrs'
              152  LOAD_ATTR             8  'get'
              155  LOAD_CONST               'method'
              158  LOAD_CONST               'GET'
              161  CALL_FUNCTION_2       2  None
              164  LOAD_FAST             0  'self'
              167  STORE_ATTR            9  'method'

 L.1589       170  LOAD_FAST             4  'attrs'
              173  LOAD_ATTR             8  'get'
              176  LOAD_CONST               'id'
              179  CALL_FUNCTION_1       1  None
              182  LOAD_FAST             0  'self'
              185  STORE_ATTR           10  'id'

 L.1590       188  LOAD_FAST             4  'attrs'
              191  LOAD_ATTR             8  'get'
              194  LOAD_CONST               'enctype'

 L.1591       197  LOAD_CONST               'application/x-www-form-urlencoded'
              200  CALL_FUNCTION_2       2  None
              203  LOAD_FAST             0  'self'
              206  STORE_ATTR           11  'enctype'
              209  JUMP_BACK            31  'to 31'
              212  POP_BLOCK        

 L.1593       213  LOAD_CONST               0
              216  POP_JUMP_IF_TRUE    228  'to 228'
              219  LOAD_ASSERT              AssertionError
              222  LOAD_CONST               'No </form> tag found'
              225  RAISE_VARARGS_2       2  None
            228_0  COME_FROM             9  '9'

 L.1594       228  LOAD_FAST             0  'self'
              231  LOAD_ATTR             1  'action'
              234  LOAD_CONST               None
              237  COMPARE_OP            9  is-not
              240  POP_JUMP_IF_TRUE    252  'to 252'
              243  LOAD_ASSERT              AssertionError

 L.1595       246  LOAD_CONST               'No <form> tag found'
              249  RAISE_VARARGS_2       2  None
              252  LOAD_CONST               None
              255  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 228_0

    def __setitem__--- This code section failed: ---

 L.1610         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'fields'
                6  LOAD_ATTR             1  'get'
                9  LOAD_FAST             1  'name'
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST            3  'fields'

 L.1611        18  LOAD_FAST             3  'fields'
               21  LOAD_CONST               None
               24  COMPARE_OP            9  is-not
               27  POP_JUMP_IF_TRUE     76  'to 76'
               30  LOAD_ASSERT              AssertionError

 L.1612        33  LOAD_CONST               'No field by the name %r found (fields: %s)'

 L.1613        36  LOAD_FAST             1  'name'
               39  LOAD_CONST               ', '
               42  LOAD_ATTR             4  'join'
               45  LOAD_GLOBAL           5  'map'
               48  LOAD_GLOBAL           6  'repr'
               51  LOAD_FAST             0  'self'
               54  LOAD_ATTR             0  'fields'
               57  LOAD_ATTR             7  'keys'
               60  CALL_FUNCTION_0       0  None
               63  CALL_FUNCTION_2       2  None
               66  CALL_FUNCTION_1       1  None
               69  BUILD_TUPLE_2         2 
               72  BINARY_MODULO    
               73  RAISE_VARARGS_2       2  None

 L.1614        76  LOAD_GLOBAL           8  'len'
               79  LOAD_FAST             3  'fields'
               82  CALL_FUNCTION_1       1  None
               85  LOAD_CONST               1
               88  COMPARE_OP            2  ==
               91  POP_JUMP_IF_TRUE    131  'to 131'
               94  LOAD_ASSERT              AssertionError

 L.1615        97  LOAD_CONST               'Multiple fields match %r: %s'

 L.1616       100  LOAD_FAST             1  'name'
              103  LOAD_CONST               ', '
              106  LOAD_ATTR             4  'join'
              109  LOAD_GLOBAL           5  'map'
              112  LOAD_GLOBAL           6  'repr'
              115  LOAD_FAST             3  'fields'
              118  CALL_FUNCTION_2       2  None
              121  CALL_FUNCTION_1       1  None
              124  BUILD_TUPLE_2         2 
              127  BINARY_MODULO    
              128  RAISE_VARARGS_2       2  None

 L.1617       131  LOAD_FAST             2  'value'
              134  LOAD_FAST             3  'fields'
              137  LOAD_CONST               0
              140  BINARY_SUBSCR    
              141  STORE_ATTR            9  'value'
              144  LOAD_CONST               None
              147  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 144

    def __getitem__--- This code section failed: ---

 L.1623         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'fields'
                6  LOAD_ATTR             1  'get'
                9  LOAD_FAST             1  'name'
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST            2  'fields'

 L.1624        18  LOAD_FAST             2  'fields'
               21  LOAD_CONST               None
               24  COMPARE_OP            9  is-not
               27  POP_JUMP_IF_TRUE     43  'to 43'
               30  LOAD_ASSERT              AssertionError

 L.1625        33  LOAD_CONST               'No field by the name %r found'
               36  LOAD_FAST             1  'name'
               39  BINARY_MODULO    
               40  RAISE_VARARGS_2       2  None

 L.1626        43  LOAD_GLOBAL           4  'len'
               46  LOAD_FAST             2  'fields'
               49  CALL_FUNCTION_1       1  None
               52  LOAD_CONST               1
               55  COMPARE_OP            2  ==
               58  POP_JUMP_IF_TRUE     98  'to 98'
               61  LOAD_ASSERT              AssertionError

 L.1627        64  LOAD_CONST               'Multiple fields match %r: %s'

 L.1628        67  LOAD_FAST             1  'name'
               70  LOAD_CONST               ', '
               73  LOAD_ATTR             5  'join'
               76  LOAD_GLOBAL           6  'map'
               79  LOAD_GLOBAL           7  'repr'
               82  LOAD_FAST             2  'fields'
               85  CALL_FUNCTION_2       2  None
               88  CALL_FUNCTION_1       1  None
               91  BUILD_TUPLE_2         2 
               94  BINARY_MODULO    
               95  RAISE_VARARGS_2       2  None

 L.1629        98  LOAD_FAST             2  'fields'
              101  LOAD_CONST               0
              104  BINARY_SUBSCR    
              105  RETURN_VALUE     

Parse error at or near `BINARY_SUBSCR' instruction at offset 104

    def lint(self):
        """Check that the html is valid:

        - each field must have an id
        - each field must have a label
        """
        labels = self._label_re.findall(self.text)
        for name, fields in self.fields.items():
            for field in fields:
                if not isinstance(field, (Submit, Hidden)):
                    if not field.id:
                        raise AttributeError('%r as no id attribute' % field)
                    elif field.id not in labels:
                        raise AttributeError('%r as no associated label' % field)

    def set--- This code section failed: ---

 L.1652         0  LOAD_FAST             3  'index'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_FALSE    25  'to 25'

 L.1653        12  LOAD_FAST             2  'value'
               15  LOAD_FAST             0  'self'
               18  LOAD_FAST             1  'name'
               21  STORE_SUBSCR     
               22  JUMP_FORWARD         62  'to 87'

 L.1655        25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  'fields'
               31  LOAD_ATTR             2  'get'
               34  LOAD_FAST             1  'name'
               37  CALL_FUNCTION_1       1  None
               40  STORE_FAST            4  'fields'

 L.1656        43  LOAD_FAST             4  'fields'
               46  LOAD_CONST               None
               49  COMPARE_OP            9  is-not
               52  POP_JUMP_IF_TRUE     68  'to 68'
               55  LOAD_ASSERT              AssertionError

 L.1657        58  LOAD_CONST               'No fields found matching %r'
               61  LOAD_FAST             1  'name'
               64  BINARY_MODULO    
               65  RAISE_VARARGS_2       2  None

 L.1658        68  LOAD_FAST             4  'fields'
               71  LOAD_FAST             3  'index'
               74  BINARY_SUBSCR    
               75  STORE_FAST            5  'field'

 L.1659        78  LOAD_FAST             2  'value'
               81  LOAD_FAST             5  'field'
               84  STORE_ATTR            4  'value'
             87_0  COME_FROM            22  '22'
               87  LOAD_CONST               None
               90  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 87_0

    def get--- This code section failed: ---

 L.1666         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'fields'
                6  LOAD_ATTR             1  'get'
                9  LOAD_FAST             1  'name'
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST            4  'fields'

 L.1667        18  LOAD_FAST             4  'fields'
               21  LOAD_CONST               None
               24  COMPARE_OP            8  is
               27  POP_JUMP_IF_FALSE    46  'to 46'
               30  LOAD_FAST             3  'default'
               33  LOAD_GLOBAL           3  'NoDefault'
               36  COMPARE_OP            9  is-not
             39_0  COME_FROM            27  '27'
               39  POP_JUMP_IF_FALSE    46  'to 46'

 L.1668        42  LOAD_FAST             3  'default'
               45  RETURN_END_IF    
             46_0  COME_FROM            39  '39'

 L.1669        46  LOAD_FAST             2  'index'
               49  LOAD_CONST               None
               52  COMPARE_OP            8  is
               55  POP_JUMP_IF_FALSE    66  'to 66'

 L.1670        58  LOAD_FAST             0  'self'
               61  LOAD_FAST             1  'name'
               64  BINARY_SUBSCR    
               65  RETURN_END_IF    
             66_0  COME_FROM            55  '55'

 L.1672        66  LOAD_FAST             0  'self'
               69  LOAD_ATTR             0  'fields'
               72  LOAD_ATTR             1  'get'
               75  LOAD_FAST             1  'name'
               78  CALL_FUNCTION_1       1  None
               81  STORE_FAST            4  'fields'

 L.1673        84  LOAD_FAST             4  'fields'
               87  LOAD_CONST               None
               90  COMPARE_OP            9  is-not
               93  POP_JUMP_IF_TRUE    109  'to 109'
               96  LOAD_ASSERT              AssertionError

 L.1674        99  LOAD_CONST               'No fields found matching %r'
              102  LOAD_FAST             1  'name'
              105  BINARY_MODULO    
              106  RAISE_VARARGS_2       2  None

 L.1675       109  LOAD_FAST             4  'fields'
              112  LOAD_FAST             2  'index'
              115  BINARY_SUBSCR    
              116  STORE_FAST            5  'field'

 L.1676       119  LOAD_FAST             5  'field'
              122  RETURN_VALUE     
              123  LOAD_CONST               None
              126  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 123

    def select(self, name, value, index=None):
        """
        Like ``.set()``, except also confirms the target is a
        ``<select>``.
        """
        field = self.get(name, index=index)
        assert isinstance(field, Select)
        field.value = value

    def submit(self, name=None, index=None, **args):
        """
        Submits the form.  If ``name`` is given, then also select that
        button (using ``index`` to disambiguate)``.

        Any extra keyword arguments are passed to the ``.get()`` or
        ``.post()`` method.

        Returns a :class:`webtest.TestResponse` object.
        """
        fields = self.submit_fields(name, index=index)
        if self.method.upper() != 'GET':
            args.setdefault('content_type', self.enctype)
        return self.response.goto(self.action, method=self.method, params=fields, **args)

    def upload_fields(self):
        """
        Return a list of file field tuples of the form:
            (field name, file name)
        or
            (field name, file name, file contents).
        """
        uploads = []
        for name, fields in self.fields.items():
            for field in fields:
                if isinstance(field, File) and field.value:
                    uploads.append([name] + list(field.value))

        return uploads

    def submit_fields(self, name=None, index=None):
        """
        Return a list of ``[(name, value), ...]`` for the current
        state of the form.
        """
        submit = []
        if name is not None:
            field = self.get(name, index=index)
            submit.append((field.name, field.value_if_submitted()))
        for name, fields in self.fields.items():
            if name is None:
                continue
            for field in fields:
                value = field.value
                if value is None:
                    continue
                if isinstance(field, File):
                    submit.append((name, field))
                    continue
                if isinstance(value, list):
                    for item in value:
                        submit.append((name, item))

                else:
                    submit.append((name, value))

        return submit

    def __repr__(self):
        value = '<Form'
        if self.id:
            value += ' id=%r' % str(self.id)
        return value + ' />'


def _stringify(value):
    if isinstance(value, text_type):
        return value
    return str(value)


def _popget(d, key, default=None):
    """
    Pop the key if found (else return default)
    """
    if key in d:
        return d.pop(key)
    return default


def _space_prefix(pref, full, sep=None, indent=None, include_sep=True):
    """
    Anything shared by pref and full will be replaced with spaces
    in full, and full returned.
    """
    if sep is None:
        sep = os.path.sep
    pref = pref.split(sep)
    full = full.split(sep)
    padding = []
    while pref and full and pref[0] == full[0]:
        if indent is None:
            padding.append(' ' * (len(full[0]) + len(sep)))
        else:
            padding.append(' ' * indent)
        full.pop(0)
        pref.pop(0)

    if padding:
        if include_sep:
            return ('').join(padding) + sep + sep.join(full)
        else:
            return ('').join(padding) + sep.join(full)

    else:
        return sep.join(full)
    return


def _make_pattern--- This code section failed: ---

 L.1799         0  LOAD_FAST             0  'pat'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_FALSE    16  'to 16'

 L.1800        12  LOAD_CONST               None
               15  RETURN_END_IF    
             16_0  COME_FROM             9  '9'

 L.1801        16  LOAD_GLOBAL           1  'isinstance'
               19  LOAD_FAST             0  'pat'
               22  LOAD_GLOBAL           2  'string_types'
               25  CALL_FUNCTION_2       2  None
               28  POP_JUMP_IF_FALSE    49  'to 49'

 L.1802        31  LOAD_GLOBAL           3  're'
               34  LOAD_ATTR             4  'compile'
               37  LOAD_FAST             0  'pat'
               40  CALL_FUNCTION_1       1  None
               43  STORE_FAST            0  'pat'
               46  JUMP_FORWARD          0  'to 49'
             49_0  COME_FROM            46  '46'

 L.1803        49  LOAD_GLOBAL           5  'hasattr'
               52  LOAD_FAST             0  'pat'
               55  LOAD_CONST               'search'
               58  CALL_FUNCTION_2       2  None
               61  POP_JUMP_IF_FALSE    71  'to 71'

 L.1804        64  LOAD_FAST             0  'pat'
               67  LOAD_ATTR             6  'search'
               70  RETURN_END_IF    
             71_0  COME_FROM            61  '61'

 L.1805        71  LOAD_GLOBAL           5  'hasattr'
               74  LOAD_FAST             0  'pat'
               77  LOAD_CONST               '__call__'
               80  CALL_FUNCTION_2       2  None
               83  POP_JUMP_IF_FALSE    90  'to 90'

 L.1806        86  LOAD_FAST             0  'pat'
               89  RETURN_END_IF    
             90_0  COME_FROM            83  '83'

 L.1807        90  LOAD_CONST               0
               93  POP_JUMP_IF_TRUE    109  'to 109'
               96  LOAD_ASSERT              AssertionError

 L.1808        99  LOAD_CONST               'Cannot make callable pattern object out of %r'
              102  LOAD_FAST             0  'pat'
              105  BINARY_MODULO    
              106  RAISE_VARARGS_2       2  None
              109  LOAD_CONST               None
              112  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 109


def html_unquote(v):
    """
    Unquote (some) entities in HTML.  (incomplete)
    """
    for ent, repl in [('&nbsp;', ' '), ('&gt;', '>'),
     ('&lt;', '<'), ('&quot;', '"'),
     ('&amp;', '&')]:
        v = v.replace(ent, repl)

    return v


def encode_params(params, content_type):
    if params is NoDefault:
        return ''
    if isinstance(params, dict) or hasattr(params, 'items'):
        params = list(params.items())
    if isinstance(params, (list, tuple)):
        if content_type:
            content_type = content_type.lower()
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[1]
                charset = charset.strip('; ').lower()
                encoded_params = []
                for k, v in params:
                    if isinstance(v, text_type):
                        v = v.encode(charset)
                    encoded_params.append((k, v))

                params = encoded_params
        params = urlencode(params, doseq=True)
    return params
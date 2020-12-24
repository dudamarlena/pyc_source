# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Dropbox\vk\django-trusted-html\trustedhtml\tests.py
# Compiled at: 2014-05-19 04:07:47
import unittest
from trustedhtml.classes import *
from trustedhtml import rules
from trustedhtml import signals

class TestClasses(unittest.TestCase):

    def setUp(self):
        pass

    def test_rule(self):
        rule = Rule()

        class Test(object):
            pass

        test = Test()
        self.assertEqual(rule.validate(test), test)

    def test_string(self):
        string = String()
        self.assertRaises(EmptyException, string.validate, '')
        self.assertEqual(string.validate('qwe'), 'qwe')
        self.assertEqual(string.validate('  qw e '), 'qw e')

    def test_list(self):
        rule = List(values=['a', 'aB'], strip=True)
        self.assertRaises(IncorrectException, rule.validate, 'ac')
        self.assertEqual(rule.validate('  a '), 'a')
        self.assertEqual(rule.validate('  Ab '), 'aB')

    def test_list_case(self):
        rule = List(values=['a', 'aB'], return_defined=False, case_sensitive=True)
        self.assertRaises(IncorrectException, rule.validate, 'ac')
        self.assertEqual(rule.validate('  a '), 'a')
        self.assertRaises(IncorrectException, rule.validate, '  Ab ')

    def test_regexp_regexp(self):
        rule = RegExp(regexp='@*([-+]?\\d{1,7})@*$')
        self.assertRaises(IncorrectException, rule.validate, '-')
        self.assertRaises(IncorrectException, rule.validate, '@@@-')
        self.assertEqual(rule.validate('  @@@-12@ '), '-12')

    def test_regexp_expand(self):
        rule = RegExp(regexp='([-+]?\\d*),(?P<a>\\d*)$', expand='\\g<a>;\\1')
        self.assertEqual(rule.validate('-12,34'), '34;-12')
        self.assertRaises(IncorrectException, rule.validate, '-12,34a')

    def test_or(self):
        rule = Or(rules=[
         List(values=['a', 'aB']),
         RegExp(regexp='([-+]?\\d{1,7})$')])
        self.assertRaises(EmptyException, rule.validate, '')
        self.assertRaises(IncorrectException, rule.validate, '-')
        self.assertEqual(rule.validate('  -12 '), '-12')
        self.assertEqual(rule.validate('  Ab '), 'aB')

    def test_or_empty(self):
        rule = Or(rules=[
         List(values=['a', 'aB']),
         RegExp(regexp='([-+]?\\d{1,7})$')])
        self.assertRaises(EmptyException, rule.validate, '')
        self.assertRaises(IncorrectException, rule.validate, '-')
        self.assertEqual(rule.validate('  -12 '), '-12')
        self.assertEqual(rule.validate('  Ab '), 'aB')

    def test_and(self):
        rule = And(rules=[
         RegExp(regexp='!*(\\w{2})$'),
         List(values=['a', 'aB', 'Cd'])])
        self.assertRaises(EmptyException, rule.validate, '')
        self.assertRaises(IncorrectException, rule.validate, '-')
        self.assertRaises(IncorrectException, rule.validate, 'a')
        self.assertEqual(rule.validate('  Ab '), 'aB')
        self.assertRaises(IncorrectException, rule.validate, 'ef')
        self.assertEqual(rule.validate('  !!cD '), 'Cd')

    def test_style(self):
        text_decoration = List(values=['underline', 'line-through'])
        simple_margin_top = RegExp(regexp='(\\w+)$')
        rule = Style(rules={'text-decoration': text_decoration, 
           'margin-top': simple_margin_top})
        self.assertEqual(rule.validate('text-decoration: line-through; foo: line-through;text-decoration: bar; text-decoration: underline;margin-ttop: 1; margin-tOP: 3;'), 'text-decoration: underline; margin-top: 3;')

    def tearDown(self):
        pass


class TestUri(unittest.TestCase):

    def setUp(self):
        pass

    def test_a(self):
        rule = Uri()
        self.assertRaises(IncorrectException, rule.validate, 'script:alert("hack")')
        self.assertEqual(rule.validate('http://foreign.com/img.jpg'), 'http://foreign.com/img.jpg')
        self.assertEqual(rule.validate('http://local.com/img.jpg'), 'http://local.com/img.jpg')
        self.assertEqual(rule.validate('ftp://local.com/img.jpg'), 'ftp://local.com/img.jpg')
        self.assertEqual(rule.validate('http://local-mirror.com/img.jpg'), 'http://local-mirror.com/img.jpg')
        self.assertEqual(rule.validate('/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('img.jpg'), 'img.jpg')

    def test_a_local(self):
        rule = Uri(cut_sites=['local.com', 'local-mirror.com'])
        self.assertRaises(IncorrectException, rule.validate, 'script:alert("hack")')
        self.assertEqual(rule.validate('http://foreign.com/img.jpg'), 'http://foreign.com/img.jpg')
        self.assertEqual(rule.validate('http://local.com/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('ftp://local.com/img.jpg'), 'ftp://local.com/img.jpg')
        self.assertEqual(rule.validate('http://local-mirror.com/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('img.jpg'), 'img.jpg')

    def test_img(self):
        rule = Uri(allow_sites=['local.com', 'local-mirror.com'])
        self.assertRaises(IncorrectException, rule.validate, 'script:alert("hack")')
        self.assertRaises(IncorrectException, rule.validate, 'http://foreign.com/img.jpg')
        self.assertEqual(rule.validate('http://local.com/img.jpg'), 'http://local.com/img.jpg')
        self.assertEqual(rule.validate('ftp://local.com/img.jpg'), 'ftp://local.com/img.jpg')
        self.assertEqual(rule.validate('http://local-mirror.com/img.jpg'), 'http://local-mirror.com/img.jpg')
        self.assertEqual(rule.validate('/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('img.jpg'), 'img.jpg')

    def test_img_local(self):
        rule = Uri(allow_sites=False, cut_sites=['local.com', 'local-mirror.com'])
        self.assertRaises(IncorrectException, rule.validate, 'script:alert("hack")')
        self.assertRaises(IncorrectException, rule.validate, 'http://foreign.com/img.jpg')
        self.assertRaises(IncorrectException, rule.validate, 'ftp://local.com/img.jpg')
        self.assertEqual(rule.validate('http://local.com/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('http://local-mirror.com/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('/img.jpg'), '/img.jpg')
        self.assertEqual(rule.validate('img.jpg'), 'img.jpg')

    def test_ext(self):
        rule = Uri(allow_sites=['local.com', 'local-mirror.com'], cut_sites=['local.com', 'local-mirror.com'])
        self.assertEqual(rule.validate('http://local.com?qw'), '?qw')
        self.assertEqual(rule.validate('http://local.com'), '/')
        self.assertEqual(rule.validate('http://local.com?'), '/?')
        self.assertEqual(rule.validate('http://local.com#'), '/#')
        self.assertEqual(rule.validate('?qw'), '?qw')
        self.assertEqual(rule.validate('/'), '/')
        self.assertEqual(rule.validate('?'), '?')
        self.assertEqual(rule.validate('#'), '#')
        self.assertRaises(EmptyException, rule.validate, '')

    def test_verify(self):
        rule = Uri(verify_sites=True, local_sites=['local.com'])
        self.assertEqual(rule.validate('http://example.com'), 'http://example.com')
        self.assertEqual(rule.validate('http://local.com/doesnotexists.html'), 'http://local.com/doesnotexists.html')
        self.assertRaises(IncorrectException, rule.validate, 'http://does.not.exist.example.com')
        self.assertEqual(rule.validate('/doesnotexists.html'), '/doesnotexists.html')

    def test_local(self):
        rule = Uri(verify_sites=True, verify_local=True, local_sites=['local.com'])
        self.assertEqual(rule.validate('http://example.com'), 'http://example.com')
        self.assertRaises(IncorrectException, rule.validate, 'http://local.com/doesnotexists.html')
        self.assertRaises(IncorrectException, rule.validate, 'http://does.not.exist.example.com')
        self.assertRaises(IncorrectException, rule.validate, '/doesnotexists.html')
        self.assertEqual(rule.validate('http://local.com/response'), 'http://local.com/response')
        self.assertEqual(rule.validate('http://local.com/redirect_response'), 'http://local.com/redirect_response')
        self.assertRaises(IncorrectException, rule.validate, 'http://local.com/redirect_notfound')
        self.assertEqual(rule.validate('http://local.com/request_true_response'), 'http://local.com/request_true_response')
        self.assertEqual(rule.validate('http://local.com/request_false_response'), 'http://local.com/request_false_response')
        self.assertEqual(rule.validate('/response'), '/response')
        self.assertEqual(rule.validate('/response#'), '/response#')
        self.assertEqual(rule.validate('/response#anchor'), '/response#anchor')
        self.assertEqual(rule.validate('/response?'), '/response?')
        self.assertEqual(rule.validate('/response?query'), '/response?query')
        self.assertRaises(IncorrectException, rule.validate, '/')
        self.assertRaises(IncorrectException, rule.validate, 'response')
        self.assertEqual(rule.validate('#'), '#')
        self.assertEqual(rule.validate('#anchor'), '#anchor')
        self.assertRaises(IncorrectException, rule.validate, '?')
        self.assertRaises(IncorrectException, rule.validate, '?query')
        self.assertRaises(EmptyException, rule.validate, '')

    def test_settings(self):
        link_sites = settings.TRUSTEDHTML_LINK_SITES
        image_sites = settings.TRUSTEDHTML_IMAGE_SITES
        object_sites = settings.TRUSTEDHTML_OBJECT_SITES
        cut_sites = settings.TRUSTEDHTML_CUT_SITES
        rule = Uri()
        self.assertEqual(rule.validate('http://link.com'), 'http://link.com')
        self.assertEqual(rule.validate('http://image.com'), 'http://image.com')
        self.assertEqual(rule.validate('http://object.com'), 'http://object.com')
        self.assertEqual(rule.validate('http://cut.com'), 'http://cut.com')
        settings.TRUSTEDHTML_LINK_SITES = [
         'link.com']
        settings.TRUSTEDHTML_IMAGE_SITES = ['image.com']
        settings.TRUSTEDHTML_OBJECT_SITES = ['object.com']
        settings.TRUSTEDHTML_CUT_SITES = ['cut.com']
        rule = Uri(type=Uri.LINK)
        self.assertEqual(rule.validate('http://link.com'), 'http://link.com')
        self.assertRaises(IncorrectException, rule.validate, 'http://image.com')
        self.assertRaises(IncorrectException, rule.validate, 'http://object.com')
        self.assertEqual(rule.validate('http://cut.com'), '/')
        rule = Uri(type=Uri.IMAGE)
        self.assertRaises(IncorrectException, rule.validate, 'http://link.com')
        self.assertEqual(rule.validate('http://image.com'), 'http://image.com')
        self.assertRaises(IncorrectException, rule.validate, 'http://object.com')
        self.assertEqual(rule.validate('http://cut.com'), '/')
        rule = Uri(type=Uri.OBJECT)
        self.assertRaises(IncorrectException, rule.validate, 'http://link.com')
        self.assertRaises(IncorrectException, rule.validate, 'http://image.com')
        self.assertEqual(rule.validate('http://object.com'), 'http://object.com')
        self.assertEqual(rule.validate('http://cut.com'), '/')
        settings.TRUSTEDHTML_LINK_SITES = link_sites
        settings.TRUSTEDHTML_IMAGE_SITES = image_sites
        settings.TRUSTEDHTML_OBJECT_SITES = object_sites
        settings.TRUSTEDHTML_CUT_SITES = cut_sites


class TestCss(unittest.TestCase):

    def setUp(self):
        pass

    def test_re(self):
        self.assertEqual(re.match('%(escape)s$' % rules.css.grammar.grammar, '\\\x07'), None)
        self.assertNotEqual(re.match('%(escape)s$' % rules.css.grammar.grammar, '\\я'), None)
        self.assertEqual(re.match('%(string1)s$' % rules.css.grammar.grammar, '"img".jpg"'), None)
        self.assertNotEqual(re.match('%(string1)s$' % rules.css.grammar.grammar, '"img\\".jpg"'), None)
        return

    def test_number(self):
        self.assertRaises(IncorrectException, rules.css.syndata.number.validate, 'a')
        self.assertRaises(IncorrectException, rules.css.syndata.number.validate, '1.')
        self.assertEqual(rules.css.syndata.number.validate('  12.3 '), '12.3')

    def test_length(self):
        self.assertRaises(IncorrectException, rules.css.syndata.length.validate, '-')
        self.assertRaises(IncorrectException, rules.css.syndata.length.validate, '-12pxs')
        self.assertRaises(IncorrectException, rules.css.syndata.length.validate, '-12')
        self.assertEqual(rules.css.syndata.length.validate('  -12.3px '), '-12.3px')
        self.assertEqual(rules.css.syndata.length.validate('  0 '), '0')

    def test_color(self):
        self.assertEqual(rules.css.syndata.color.validate('  WinDow '), 'window')
        self.assertEqual(rules.css.syndata.color.validate('Red'), 'red')
        self.assertEqual(rules.css.syndata.color.validate('rgb( 1,  34%,5)'), 'rgb(1,34%,5)')
        self.assertEqual(rules.css.syndata.color.validate('rgba( 1,  34%,5  , 1 )'), 'rgba(1,34%,5,1)')
        self.assertEqual(rules.css.syndata.color.validate('rgb( 1,  34%,-5)'), 'rgb(1,34%,-5)')
        self.assertRaises(IncorrectException, rules.css.syndata.color.validate, 'rgb( 1,  34%,5a)')
        self.assertRaises(IncorrectException, rules.css.syndata.color.validate, 'rgb( 1,  34%,5)-')
        self.assertRaises(IncorrectException, rules.css.syndata.color.validate, 'rgb( 1,  34%,0.5)')
        self.assertEqual(rules.css.syndata.color.validate('#fff'), '#fff')
        self.assertEqual(rules.css.syndata.color.validate('#aaafff'), '#aaafff')
        self.assertRaises(IncorrectException, rules.css.syndata.color.validate, '#aazfff')

    def test_uri(self):
        self.assertEqual(rules.css.syndata.uri.validate('url( img.jpg  )'), 'url(img.jpg)')
        self.assertEqual(rules.css.syndata.uri.validate('url( http://ya.ru/img.jpg   )'), 'url(http://ya.ru/img.jpg)')
        self.assertEqual(rules.css.syndata.uri.validate('url( http://ya.ru/imяg.jpg  )'), 'url(http://ya.ru/imяg.jpg)')
        self.assertEqual(rules.css.syndata.uri.validate('url( http://ya.ru/img.jpg \t   )'), 'url(http://ya.ru/img.jpg)')
        self.assertRaises(IncorrectException, rules.css.syndata.uri.validate, 'url( script:alert(1)  )')
        self.assertEqual(rules.css.syndata.uri.validate('url( "http://ya.ru/img\' .jpg"  )'), 'url("http://ya.ru/img\' .jpg")')
        self.assertEqual(rules.css.syndata.uri.validate('url( \'http://ya.ru/img" .jpg\'  )'), 'url(\'http://ya.ru/img" .jpg\')')
        self.assertEqual(rules.css.syndata.uri.validate("url( 'http://ya.ru/img\\' .jpg'  )"), "url('http://ya.ru/img\\' .jpg')")

    def test_border(self):
        self.assertEqual(rules.css.box.border.validate(' 2px  Solid Black'), '2px solid black')
        self.assertEqual(rules.css.box.border.validate(' 2px  Black'), '2px black')
        self.assertEqual(rules.css.box.border.validate(' 2px  Solid Black'), '2px solid black')
        self.assertEqual(rules.css.box.border.validate(' 2px  Solid'), '2px solid')
        self.assertEqual(rules.css.box.border.validate(' Solid Black'), 'solid black')
        self.assertEqual(rules.css.box.border.validate(' Solid'), 'solid')
        self.assertEqual(rules.css.box.border.validate(' Black'), 'black')
        self.assertEqual(rules.css.box.border.validate(' 2px'), '2px')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px  Solid BBlack')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px  SSolid Black')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2pxx  Solid Black')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px  Black  Solid')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' Solid Black 2px')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px Solid Black 2px')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px 2px Solid Black')
        self.assertRaises(IncorrectException, rules.css.box.border.validate, ' 2px Solid Black Black')
        self.assertRaises(EmptyException, rules.css.box.border.validate, '')

    def test_background_position(self):
        self.assertEqual(rules.css.colors.background_position.validate(' lEft  toP '), 'left top')
        self.assertRaises(IncorrectException, rules.css.colors.background_position.validate, ' toP  lEft ')
        self.assertEqual(rules.css.colors.background_position.validate(' lEft  12pX '), 'left 12pX')
        self.assertRaises(IncorrectException, rules.css.colors.background_position.validate, ' lEft 12 px ')
        self.assertRaises(IncorrectException, rules.css.colors.background_position.validate, ' lEft 12pxs ')
        self.assertRaises(IncorrectException, rules.css.colors.background_position.validate, ' toP 12pX ')
        self.assertEqual(rules.css.colors.background_position.validate(' 34em  toP '), '34em top')
        self.assertRaises(IncorrectException, rules.css.colors.background_position.validate, ' 34em lEft ')
        self.assertEqual(rules.css.colors.background_position.validate(' 34em  12px '), '34em 12px')
        self.assertEqual(rules.css.colors.background_position.validate(' 34em  '), '34em')
        self.assertEqual(rules.css.colors.background_position.validate(' lEft  '), 'left')
        self.assertEqual(rules.css.colors.background_position.validate(' toP  '), 'top')
        self.assertRaises(EmptyException, rules.css.colors.background_position.validate, '')

    def test_background(self):
        self.assertEqual(rules.css.colors.background.validate(' rEd repEat   sCroll'), 'red repeat scroll')
        self.assertEqual(rules.css.colors.background.validate(' rgb(10%,100,255) rEpeat sCroll lEft'), 'rgb(10%,100,255) repeat scroll left')
        self.assertEqual(rules.css.colors.background.validate('#FFFFFF none repeat scroll 0'), '#FFFFFF none repeat scroll 0')
        self.assertEqual(rules.css.colors.background.validate('#FFFFFF none repeat scroll 0 0'), '#FFFFFF none repeat scroll 0 0')

    def test_full(self):
        self.assertEqual(rules.css.full.validate('color:black;font-family:sans-serif;'), 'color: black; font-family: sans-serif;')
        self.assertEqual(rules.css.full.validate('background:#FDFEFF url(/media/img/header.gif) repeat-x scroll center;height:auto; margin:0; padding:2; ppading: 2px; width:auto;'), 'background: #FDFEFF url(/media/img/header.gif) repeat-x scroll center; height: auto; margin: 0; width: auto;')

    def test_custom(self):
        lst = rules.css.custom.disabled + rules.css.custom.for_table + rules.css.custom.for_image + rules.css.custom.allowed
        append = []
        remove = [ name for name in rules.css.values.values.iterkeys() ]
        for item in lst:
            self.assertFalse(item in append)
            append.append(item)
            self.assertTrue(item in remove)
            remove.remove(item)

        self.assertFalse(remove)

    def tearDown(self):
        pass


class TestHtml(unittest.TestCase):

    def setUp(self):
        pass

    def test_values(self):
        self.assertEqual(rules.html.values.values['type'].validate('text/html'), 'text/html')
        self.assertEqual(rules.html.values.values['type'].validate('application/x-shockwave-Flash'), 'application/x-shockwave-Flash')
        self.assertRaises(IncorrectException, rules.html.values.values['type'].validate, 'application/x-shockwave-FFlash')

    def test_custom(self):
        remove = [ name for name in rules.html.attributes.attributes.iterkeys() ]
        for item in rules.html.contents.contents.iterkeys():
            self.assertTrue(item in remove)
            remove.remove(item)

        self.assertFalse(remove)
        remove = [ name for name in rules.html.attributes.attributes.iterkeys() ]
        for item in rules.html.elements.elements.iterkeys():
            self.assertTrue(item in remove)
            remove.remove(item)

        self.assertFalse(remove)
        lst = rules.html.custom.docement_elements + rules.html.custom.frame_elements + rules.html.custom.form_elements + rules.html.custom.remove_elements + rules.html.custom.remove_elements_with_content + rules.html.custom.pretty_elements + rules.html.custom.rare_elements
        append = []
        remove = [ name for name in rules.html.attributes.attributes.iterkeys() ]
        for item in lst:
            self.assertFalse(item in append, repr(item))
            append.append(item)
            self.assertTrue(item in remove, repr(item))
            remove.remove(item)

        self.assertFalse(remove)

    def test_full(self):
        self.assertEqual(rules.html.full.validate('<p>test</p>'), '<p>test</p>')
        self.assertEqual(rules.html.full.validate('<p foo="bar">test</p>'), '<p>test</p>')
        self.assertEqual(rules.html.full.validate('<p>te<foo></foo>st</p>'), '<p>test</p>')
        self.assertEqual(rules.html.full.validate('<p>t<foo>es</foo>t</p>'), '<p>test</p>')
        self.assertEqual(rules.html.full.validate('<p>t<foo>e<bar>s</bar></foo>t</p>'), '<p>test</p>')
        self.assertEqual(rules.html.full.validate('<p>   t   <span>   e   </span>   <span>   s   </span>   t   </p>'), '<p> t <span> e </span> <span> s </span> t </p>')
        self.assertEqual(rules.html.full.validate('<p>   te   <span></span>   <span>   s   </span>   t   </p>'), '<p> te <span> s </span> t </p>')
        self.assertEqual(rules.html.full.validate('<p> te<span> </span> <span> </span> st </p>'), '<p> te st </p>')
        self.assertEqual(rules.html.full.validate(' te<span> </span> <span> </span> st '), '<p>te st</p>')
        self.assertEqual(rules.html.pretty.validate('<tr><td></td><td>a</td><td><span> </span> <span> </span> </td></tr>'), '<p><tr><td>&nbsp;</td><td>a</td><td>&nbsp;</td></tr></p>')
        self.assertEqual(rules.html.full.validate('<img />'), '')
        self.assertEqual(rules.html.full.validate('<img src="img.png" />'), '<p><img src="img.png" alt="" /></p>')
        self.assertEqual(rules.html.full.validate('<img style="float: left; border: 2px solid black; margin-top: 3px; margin-bottom: 3px; margin-left: 4px; margin-right: 4px;" src="/media/img/warning.png" alt="qwe" width="64" height="64" />'), '<p><img style="float: left; border: 2px solid black; margin-top: 3px; margin-bottom: 3px; margin-left: 4px; margin-right: 4px;" src="/media/img/warning.png" alt="qwe" width="64" height="64" /></p>')
        self.assertEqual(rules.html.full.validate(tinymce_in), tinymce_full)
        self.assertEqual(rules.html.full.validate('<a href="/search?text=ask&amp;page=2">HTML</a>'), '<p><a href="/search?text=ask&amp;page=2">HTML</a></p>')
        self.assertEqual(rules.html.full.validate('<p> </p><p>&nbsp;</p><p> </p><p>   &nbsp;   &nbsp; a&nbsp;&nbsp;  &nbsp; </p><p> </p>'), '<p>\xa0a\xa0</p>')
        self.assertEqual(rules.html.full.validate('<iframe width="425" height="349" src="http://www.youtube.com/embed/oFYhDogAzdM" frameborder="0" allowfullscreen></iframe>'), '<p><iframe width="425" height="349" src="http://www.youtube.com/embed/oFYhDogAzdM" frameborder="0"></iframe></p>')

    def test_pretty(self):
        self.assertEqual(rules.html.pretty.validate('a<dl><dd>b</dd></dl>c'), '<p>abc</p>')
        self.assertEqual(rules.html.pretty.validate('<form><p>t<select><option>e</option></select></p><p>s</p><select><option>t</option></select></form><p>.</p>'), '<p>te</p><p>s</p><p>t</p><p>.</p>')
        self.assertEqual(rules.html.pretty.validate(tinymce_in), tinymce_pretty)
        self.assertEqual(rules.html.pretty.validate('<p>a<noindex>b</noindex>c</p>'), '<p>a<noindex>b</noindex>c</p>')
        self.assertEqual(rules.html.pretty.validate('<iframe width="425" height="349" src="http://www.youtube.com/embed/oFYhDogAzdM" frameborder="0" allowfullscreen></iframe>'), '<p><iframe width="425" height="349" src="http://www.youtube.com/embed/oFYhDogAzdM"></iframe></p>')
        self.assertEqual(rules.html.pretty.validate('<iframe width="425" height="349" src="http://www.youtu.be.com/embed/oFYhDogAzdM" frameborder="0" allowfullscreen></iframe>'), '<p><iframe width="425" height="349"></iframe></p>')

    def test_hack(self):
        self.assertEqual(rules.html.full.validate('<SCRIPT>alert("XSS")</SCRIPT>'), '')
        self.assertEqual(rules.html.full.validate('<i\x00mg src="1.jpg">'), '<p><img src="1.jpg" alt="" /></p>')
        self.assertEqual(rules.html.full.validate('&#x26x26&#38#38+&#x26;x26;&#38;#38;'), '<p>&amp;x26&amp;#38+&amp;x26;&amp;#38;</p>')
        self.assertEqual(rules.html.full.validate("<IMG SRC='&#106&#0000097asdasd'>"), '<p><img src="jaasdasd" alt="" /></p>')
        self.assertEqual(rules.html.full.validate('<IMG SRC="javascript:alert(\'XSS\');">'), '')
        self.assertEqual(rules.html.full.validate("<IMG SRC=JaVaScRiPt:alert('XSS')>"), '')
        self.assertEqual(rules.html.full.validate('<IMG """><SCRIPT>alert("XSS")</SCRIPT>">'), '<p>&quot;&gt;</p>')
        self.assertEqual(rules.html.full.validate('<img src=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>'), '')
        self.assertEqual(rules.html.full.validate('<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>'), '')
        self.assertEqual(rules.html.full.validate('<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'), '')
        self.assertEqual(rules.html.full.validate('<img src=&#0000106&#x61&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>'), '<p><img src="javascriptalert(\'XSS\')" alt="" /></p>')
        self.assertEqual(rules.html.full.validate('<A href="&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29">a</A>'), '<p><a>a</a></p>')
        self.assertEqual(rules.html.full.validate('<A href=%6A%61%76%61%73%63%72%69%70%74%3A%61%6C%65%72%74%28%27%58%53%53%27%29>a</A>'), '<p><a href="%6A%61%76%61%73%63%72%69%70%74%3A%61%6C%65%72%74%28%27%58%53%53%27%29">a</a></p>')
        self.assertEqual(rules.html.full.validate('<IMG SRC="jav   ascript:alert(\'XSS\');">'), '')
        self.assertEqual(rules.html.full.validate('<SCRIPT/XSS SRC="http://ha.ckers.org/xss.js"></SCRIPT>'), '<p>/ha.ckers.org/xss.js&quot;&gt;</p>')
        self.assertEqual(rules.html.full.validate('<SCRIPT SRC=http://ha.ckers.org/xss.js?<B></SCRIPT>'), '')
        self.assertEqual(rules.html.full.validate('<SCRIPT SRC=//ha.ckers.org/.j></SCRIPT>'), '')
        self.assertEqual(rules.html.full.validate('<IMG SRC="javascript:alert(\'XSS\')" <IMG SRC="1.jpg">'), '<p><img src="1.jpg" alt="" /></p>')
        self.assertEqual(rules.html.full.validate("<BODY ONLOAD=alert('XSS')>BODY</BODY>"), '<p><body>BODY</body></p>')
        self.assertEqual(rules.html.full.validate('<IMG SRC=\'vbscript:msgbox("XSS")\'>'), '')
        self.assertEqual(rules.html.full.validate('<img style="xss:expr/*XSS*/ession(alert(\'XSS\'))">'), '')
        self.assertEqual(rules.html.full.validate("<!--[if gte IE 4]><SCRIPT>alert('XSS');</SCRIPT><![endif]-->"), '')
        self.assertEqual(rules.html.full.validate('<A HREF="h\ntt\x00p://6&#9;6.000146.0x7.147/">XSS</A>'), '<p><a>XSS</a></p>')
        self.assertEqual(rules.html.full.validate('<IMG STYLE="exp/*<A STYLE=\'no\\xss:noxss("*//*");xss:&#101;x&#x2F;*XSS*//*/*/pression(alert("XSS"))\'>a</a>'), '<p><a>a</a></p>')
        self.assertEqual(rules.html.full.validate('<A HREF="http://%77%77%77%2E%67%6F%6F%67%6C%65%2E%63%6F%6D">XSS</A>'), '<p><a href="http://%77%77%77%2e%67%6f%6f%67%6c%65%2e%63%6f%6d">XSS</a></p>')
        self.assertEqual(rules.html.full.validate('<DIV STYLE="background-image: url(&#1;javascript:alert(\'XSS\'))">div</div>'), '<div>div</div>')
        self.assertEqual(rules.html.full.validate('<DIV STYLE="background:#fff url(\\0031.jpg);">NOXSS</div>'), '<div style="background: #fff url(\\0031.jpg);">NOXSS</div>')
        self.assertEqual(rules.html.full.validate('<DIV STYLE="background-image:url(javascript\\3aalert(1))">XSS</DIV>'), '<div>XSS</div>')
        self.assertEqual(rules.html.full.validate('<DIV STYLE="background-image:\\0075\\0072\\006C\\0028\'\\006a\\0061\\0076\\0061\\0073\\0063\\0072\\0069\\0070\\0074\\003a\\0061\\006c\\0065\\0072\\0074\\0028\'\\0058\'\\0029\'\\0029">XSS</DIV>'), '<div>XSS</div>')
        self.assertEqual(rules.html.full.validate("<IMG SRC='%399.jpg'>"), '<p><img src="%399.jpg" alt="" /></p>')
        self.assertEqual(rules.html.full.validate('<DIV STYLE="background-image:url(\'\\x3c\\x3C\\u003c\\u003C\')>div</div>'), '<div>div</div>')
        self.assertEqual(rules.html.full.validate('<DIV sstyle=foobar"tstyle="foobar"ystyle="foobar"lstyle="foobar"estyle="foobar"=-moz-binding:url(http://h4k.in/mozxss.xml#xss)>foobar#xss)" a=">asd"</DIV>'), '<div>foobar#xss)&quot; a=&quot;&gt;asd&quot;</div>')
        self.assertEqual(rules.html.full.validate("<IMG SRC='vbscript:Execute(MsgBox(chr(88)&chr(83)&chr(83)))'>"), '')
        self.assertEqual(rules.html.full.validate("<A HREF='res://c:\\\\program%20files\\\\adobe\\\\acrobat%207.0\\\\acrobat\\\\acrobat.dll/#2/#210'>asd</A>"), '<p><a>asd</a></p>')
        self.assertEqual(rules.html.full.validate('<A onclick=eval/**/(/ale/.source%2b/rt/.source%2b/(7)/.source);>asd</A>'), '<p><a>asd</a></p>')
        self.assertEqual(rules.html.full.validate("<!--adasda<IMG SRC='1.jpg'> ->1w<!- adasda IMG SRC='1.jpg'>2w-->3w->4w>"), '<p>3w-&gt;4w&gt;</p>')
        self.assertEqual(rules.html.full.validate('TEXT<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/transitional.dtd"><html>foo<!bar</html>text'), '<p>TEXT<html>foo&lt;!bar&lt;/html&gt;text</html></p>')

    def tearDown(self):
        pass


class TestSignals(unittest.TestCase):

    def setUp(self):

        def done(sender, **kwargs):
            pass

        def exception(sender, **kwargs):
            pass

        signals.rule_done.connect(done)
        signals.rule_exception.connect(exception)

    def test_signals(self):
        pass

    def tearDown(self):
        pass


def get_html(html, type='Transitional'):
    return '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 %s//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-%s.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>For w3c</title>\n<meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n<meta http-equiv="Content-Language" content="en" />\n</head>\n<body>\n%s\n</body>\n</html>\n' % (type, type.lower(), html)


tinymce_in = '\n<p>q<strong>w</strong>e<em>r</em>t<span style="text-decoration: underline;">y</span>u<span style="text-decoration: line-through;">i</span>o<span style="text-decoration: line-through;"><span style="text-decoration: underline;"><em><strong>p</strong></em></span></span>[]a<sub>s</sub>d<sup>f</sup>g&amp;hjkl;\'</p>\n<p><a name="ANC"></a>a</p>\n<ul>\n<li>b\n<ul>\n<li>A</li>\n<li>B</li>\n<li>C</li>\n</ul>\n</li>\n<li>c</li>\n<li>d</li>\n</ul>\n<ol>\n<li>1<ol>\n<li>!</li>\n<li>@</li>\n<li>#</li>\n</ol></li>\n<li>2</li>\n<li>3</li>\n</ol><address>H</address>\n<pre>\nJ\nJJJJ\nJJ\n</pre>\n<h1>1</h1>\n<h2>2</h2>\n<h3>3</h3>\n<h4>4</h4>\n<h5>5</h5>\n<h6>6</h6>\n<p><a href="http://ya.ru">Z</a>X<a href="/news" target="_blank">C</a>V<a href="#ANC">B</a>NM<img title="sb" src="/media/img/search.jpg" alt="Search button" width="30" height="30" />&lt;</p>\n<p><img id="I1" style="border: 1px solid black; margin: 2px 3px; float: right;" src="/media/img/logo.png" alt="" width="94" height="94" /></p>\n<p>&nbsp;</p>\n<p>&nbsp;</p>\n<p>&nbsp;</p>\n<p>And</p>\n<p>&nbsp;</p>\n<p>&nbsp;</p>\n<p>this:</p>\n<p>&nbsp;</p>\n<p>\n<object width="100" height="100" data="http://www.youtube.com/watch?v=rAy8JbMitog" type="application/x-shockwave-flash">\n<param name="src" value="http://www.youtube.com/watch?v=rAy8JbMitog" />\n</object>\n</p>\n<p>Options:</p>\n<p>\n<object width="425" height="350" data="http://www.youtube.com/v/rAy8JbMitog" type="application/x-shockwave-flash">\n<param name="loop" value="false" />\n<param name="src" value="http://www.youtube.com/v/rAy8JbMitog" />\n<param name="align" value="right" />\n<param name="bgcolor" value="#a1f074" />\n<param name="vspace" value="10" />\n<param name="hspace" value="30" />\n</object>\n</p>\n<p>&nbsp;</p>\n<p>&amp;&euro;&delta;&nbsp;&Theta;</p>\n<blockquote>\n<p>asdas</p>\n</blockquote>\n<p><del>b</del><ins>c</ins>d<del>e</del>f</p>\n<table border="0">\n<tbody>\n<tr>\n<td>qq</td>\n<td colspan="2">\n<p>wwweeee</p>\n</td>\n</tr>\n<tr>\n<td>aaaa</td>\n<td>ss</td>\n<td>ddd</td>\n</tr>\n</tbody>\n</table>\n<table style="border-color: #37c5c7; border-width: 2px; height: 200px; background-color: #bacbb8; width: 100%;" border="2" cellspacing="3" cellpadding="2" frame="hsides" rules="rows">\n<caption></caption>\n<tbody>\n<tr style="background-image: url(/media/img/content-corner.gif);" align="right">\n<td>ad</td>\n<td>qw</td>\n<td>\n<table style="height: 100px;" width="40" frame="lhs" rules="cols" align="left" summary="asd" hack=\'on\'>\n<caption></caption> \n<tbody>\n<tr>\n<td>dd</td>\n<td>fd</td>\n</tr>\n<tr>\n<td>fdf</td>\n<td>fd</td>\n</tr>\n</tbody>\n</table>\n</td>\n</tr>\n<tr>\n<td></td>\n<td style="background-color: #a2a1c4;" colspan="2" rowspan="2" align="center" valign="top">big</td>\n</tr>\n<tr>\n<td style="background-color: #c2a1a4; text-decoration:underline;border-left: 2px solid red">zx</td>\n</tr>\n</tbody>\n</table>\n<p>&lt;img src="javascript:alert(1);"&gt;</p>\ntext\n<p>русский<br />end</p>\n'
tinymce_full = '<p>q<strong>w</strong>e<em>r</em>t<span style="text-decoration: underline;">y</span>u<span style="text-decoration: line-through;">i</span>o<span style="text-decoration: line-through;"><span style="text-decoration: underline;"><em><strong>p</strong></em></span></span>[]a<sub>s</sub>d<sup>f</sup>g&amp;hjkl;&apos;</p><p><a name="ANC"></a>a</p><ul> <li>b <ul> <li>A</li> <li>B</li> <li>C</li> </ul> </li> <li>c</li> <li>d</li> </ul><ol> <li>1<ol> <li>!</li> <li>@</li> <li>#</li> </ol></li> <li>2</li> <li>3</li> </ol><address>H</address><pre> J JJJJ JJ </pre><h1>1</h1><h2>2</h2><h3>3</h3><h4>4</h4><h5>5</h5><h6>6</h6><p><a href="http://ya.ru">Z</a>X<a href="/news" target="_blank">C</a>V<a href="#ANC">B</a>NM<img title="sb" src="/media/img/search.jpg" alt="Search button" width="30" height="30" />&lt;</p><p><img id="I1" style="border: 1px solid black; margin: 2px 3px; float: right;" src="/media/img/logo.png" alt="" width="94" height="94" /></p><p>And</p><p>this:</p><p> <object width="100" height="100" data="http://www.youtube.com/watch?v=rAy8JbMitog" type="application/x-shockwave-flash"> <param name="src" value="http://www.youtube.com/watch?v=rAy8JbMitog" /> </object> </p><p>Options:</p><p> <object width="425" height="350" data="http://www.youtube.com/v/rAy8JbMitog" type="application/x-shockwave-flash"> <param name="loop" value="false" /> <param name="src" value="http://www.youtube.com/v/rAy8JbMitog" /> <param name="align" value="right" /> <param name="bgcolor" value="#a1f074" /> <param name="vspace" value="10" /> <param name="hspace" value="30" /> </object> </p><p>&amp;€δ\xa0Θ</p><blockquote> <p>asdas</p> </blockquote><p><del>b</del><ins>c</ins>d<del>e</del>f</p><table border="0"> <tbody> <tr> <td>qq</td> <td colspan="2"> <p>wwweeee</p> </td> </tr> <tr> <td>aaaa</td> <td>ss</td> <td>ddd</td> </tr> </tbody> </table><table style="border-color: #37c5c7; border-width: 2px; height: 200px; background-color: #bacbb8; width: 100%;" border="2" cellspacing="3" cellpadding="2" frame="hsides" rules="rows"> <caption></caption> <tbody> <tr style="background-image: url(/media/img/content-corner.gif);" align="right"> <td>ad</td> <td>qw</td> <td> <table style="height: 100px;" width="40" frame="lhs" rules="cols" align="left" summary="asd"> <caption></caption> <tbody> <tr> <td>dd</td> <td>fd</td> </tr> <tr> <td>fdf</td> <td>fd</td> </tr> </tbody> </table> </td> </tr> <tr> <td>&nbsp;</td> <td style="background-color: #a2a1c4;" colspan="2" rowspan="2" align="center" valign="top">big</td> </tr> <tr> <td style="background-color: #c2a1a4; text-decoration: underline; border-left: 2px solid red;">zx</td> </tr> </tbody> </table><p>&lt;img src=&quot;javascript:alert(1);&quot;&gt;</p><p> text </p><p>русский<br />end</p>'
tinymce_pretty = '<p>q<strong>w</strong>e<em>r</em>t<span style="text-decoration: underline;">y</span>u<span style="text-decoration: line-through;">i</span>o<span style="text-decoration: line-through;"><span style="text-decoration: underline;"><em><strong>p</strong></em></span></span>[]a<sub>s</sub>d<sup>f</sup>g&amp;hjkl;&apos;</p><p><a name="ANC"></a>a</p><ul> <li>b <ul> <li>A</li> <li>B</li> <li>C</li> </ul> </li> <li>c</li> <li>d</li> </ul><ol> <li>1<ol> <li>!</li> <li>@</li> <li>#</li> </ol></li> <li>2</li> <li>3</li> </ol><address>H</address><pre> J JJJJ JJ </pre><h1>1</h1><h2>2</h2><h3>3</h3><h4>4</h4><h5>5</h5><h6>6</h6><p><a href="http://ya.ru">Z</a>X<a href="/news" target="_blank">C</a>V<a href="#ANC">B</a>NM<img title="sb" src="/media/img/search.jpg" alt="Search button" width="30" height="30" />&lt;</p><p><img style="float: right;" src="/media/img/logo.png" alt="" width="94" height="94" /></p><p>And</p><p>this:</p><p> <object width="100" height="100" data="http://www.youtube.com/watch?v=rAy8JbMitog" type="application/x-shockwave-flash"> <param name="src" value="http://www.youtube.com/watch?v=rAy8JbMitog" /> </object> </p><p>Options:</p><p> <object width="425" height="350" data="http://www.youtube.com/v/rAy8JbMitog" type="application/x-shockwave-flash"> <param name="loop" value="false" /> <param name="src" value="http://www.youtube.com/v/rAy8JbMitog" /> <param name="align" value="right" /> <param name="bgcolor" value="#a1f074" /> <param name="vspace" value="10" /> <param name="hspace" value="30" /> </object> </p><p>&amp;€δ\xa0Θ</p><blockquote> <p>asdas</p> </blockquote><p><del>b</del><ins>c</ins>d<del>e</del>f</p><table> <tbody> <tr> <td>qq</td> <td colspan="2"> <p>wwweeee</p> </td> </tr> <tr> <td>aaaa</td> <td>ss</td> <td>ddd</td> </tr> </tbody> </table><table> <caption></caption> <tbody> <tr align="right"> <td>ad</td> <td>qw</td> <td> <table summary="asd"> <caption></caption> <tbody> <tr> <td>dd</td> <td>fd</td> </tr> <tr> <td>fdf</td> <td>fd</td> </tr> </tbody> </table> </td> </tr> <tr> <td>&nbsp;</td> <td colspan="2" rowspan="2" align="center" valign="top">big</td> </tr> <tr> <td style="text-decoration: underline;">zx</td> </tr> </tbody> </table><p>&lt;img src=&quot;javascript:alert(1);&quot;&gt;</p><p> text </p><p>русский<br />end</p>'
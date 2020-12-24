# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/tests/test_strtools.py
# Compiled at: 2013-11-12 16:15:32
import pdb, sys, unittest, re, bs4
from PyQt4 import QtGui
try:
    from .. import textools
    from ..extra import richtext, researched_richtext
    from .. import dectools
except ValueError:
    for n in xrange(2):
        try:
            import textools
            from extra import richtext, researched_richtext
            import dectools
            break
        except ImportError:
            import sys
            sys.path.insert(1, '..')

    else:
        raise ImportError

DEBUG = True

def text_setUp(self):
    text1 = "talking about expecting the Spanish Inquisition in the text below: \nChapman: I didn't expect a kind of Spanish Inquisition. \n(JARRING CHORD - the cardinals burst in) \nXiminez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) \n"
    text1_proper_formatted = "<*m0>[[{talking {about }<g[1]>expect{ing }<g[2]>{the }<g[3]>Spanish Inquisition{ }<g[4]>}<g[0]>]]in the text below: \nChapman: <*m1>[[{I {didn't }<g[1]>expect{ a kind of }<g[2]>Spanish Inquisition{.}<g[4]>}<g[0]>]] \n(JARRING CHORD - the cardinals burst in) \nXiminez: <*m2>[[{{NOBODY }<g[1]>expect{s }<g[2]>{the }<g[3]>Spanish Inquisition{!}<g[4]>}<g[0]>]] Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) \n"
    text1_proper_replaced = "<*m0>[[{talking {about }<g[1]>expect{ing }<g[2]>{the }<g[3]>Spanish Inquisition{ }<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]]in the text below: \nChapman: <*m1>[[{I {didn't }<g[1]>expect{ a kind of }<g[2]>Spanish Inquisition{.}<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]] \n(JARRING CHORD - the cardinals burst in) \nXiminez: <*m2>[[{{NOBODY }<g[1]>expect{s }<g[2]>{the }<g[3]>Spanish Inquisition{!}<g[4]>}<g[0]>]]==>[[What is this, the Spanish Inquisition?]] Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry... are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) \n"
    regexp1 = "([a-zA-Z']+\\s)+?expect(.*?)(the )*Spanish " + 'Inquisition(!|.)'
    replace1 = 'What is this, the Spanish Inquisition?'
    text2 = "Researching my re search is really easy with this handy new tool! \nIt shows me my matches and group number, I think it is great that they're seen in this new light! \n"
    text2_proper_formatted = "<*m0>[[{{R}<g[2]>esearching}<g[0, 1]>]] my <*m1>[[{{r}<g[2]>e search}<g[0, 1]>]] <*m2>[[{is}<g[0, 3]>]] really easy with <*m3>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]] handy new tool! \nIt shows me my matches and group number, I think it <*m4>[[{is}<g[0, 3]>]] great that they'<*m5>[[{{r}<g[2]>e seen}<g[0, 1]>]] in <*m6>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]] new light! \n"
    text2_proper_replaced = "<*m0>[[{{R}<g[2]>esearching}<g[0, 1]>]]==>[[New Research!]] my <*m1>[[{{r}<g[2]>e search}<g[0, 1]>]]==>[[New Research!]] <*m2>[[{is}<g[0, 3]>]]==>[[New Research!]] really easy with <*m3>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]]==>[[New Research!]] handy new tool! \nIt shows me my matches and group number, I think it <*m4>[[{is}<g[0, 3]>]]==>[[New Research!]] great that they'<*m5>[[{{r}<g[2]>e seen}<g[0, 1]>]]==>[[New Research!]] in <*m6>[[{{{t}<g[5]>h}<g[4]>is}<g[0, 3]>]]==>[[New Research!]] new light! \n"
    regexp2 = '((R|r)e ?se\\w*)|(((T|t)h)?is)'
    replace2 = 'New Research!'
    self.text_list = (
     text1, text2)
    self.regexp_list = (regexp1, regexp2)
    self.replace_list = (replace1, replace2)
    self.proper_formatted = (text1_proper_formatted, text2_proper_formatted)
    self.proper_replaced = (text1_proper_replaced, text2_proper_replaced)
    self.all_list = tuple(zip(self.text_list, self.regexp_list, self.replace_list, self.proper_formatted, self.proper_replaced))


def get_researched_str_recursive(data_list):
    outlist = []
    for regpart in data_list:
        if type(regpart) == str:
            outlist.append(regpart)
        else:
            outlist.append(get_researched_str_recursive(regpart.data_list))

    return ('').join(outlist)


class regPartTest(unittest.TestCase):

    def setUp(self):
        text_setUp(self)
        app = QtGui.QApplication(sys.argv)
        self.TextEdit = QtGui.QTextEdit()
        self.TextEdit.setText(self.text_list[0])

    def test_re_search(self):
        for stuff in self.all_list:
            text, regexp, replace, prop_formatted, prop_replaced = stuff
            del stuff
            regcmp = re.compile(regexp)
            researched = textools.re_search(regexp, text)
            r_formatted = textools.format_re_search(researched)
            r_text = textools.get_str_researched(researched)
            self.assertEqual(r_text, text, 'Simple text not equal')
            self.assertEqual(r_formatted, prop_formatted, 'Formatted')
            r_text = get_researched_str_recursive(researched)
            self.assertEqual(r_text, text, 'Recursive text not equal')
            researched_replace = textools.re_search_replace(researched, replace, preview=True)
            std_replaced = regcmp.sub(replace, text)
            r_replaced = textools.get_str_researched(researched_replace)
            r_formatted_replaced = textools.format_re_search(researched_replace)
            self.assertEqual(r_formatted_replaced, prop_replaced)
            self.assertEqual(r_replaced, std_replaced, 'Replaced text not equal')

    @dectools.debug(DEBUG)
    def test_richtext(self):
        """Test the richtext position finder. This also simultaniously tests
        to make sure that most of the richtext and researched_richtext
        modules are working properly"""
        for stuff in self.all_list:
            text, regexp, replace, prop_formatted, prop_replaced = stuff
            del stuff
            researched = textools.re_search(regexp, text)
            researched_html_list = researched_richtext.re_search_format_html(researched)
            str_html = richtext.get_str_formated_html(researched_html_list)
            ignore = set(n[0] for n in richtext.html_replace_str_list)
            deformated_html_list = richtext.deformat_html(str_html, keepif=richtext.KEEPIF['black-bold'])
            str_deformated = richtext.get_str_formated_html(deformated_html_list)
            for check_list, check_str in ((researched_html_list, str_html),
             (
              deformated_html_list, str_deformated)):
                num_ignores = 0
                for n in xrange(0, len(check_str)):
                    new_n = n - num_ignores
                    if text[new_n] in ignore:
                        num_ignores += 1
                        continue
                    out_text_pos, out_vis_pos, out_html_pos = richtext.get_position(check_list, true_position=new_n)
                    self.assertEqual(text[n], check_str[out_html_pos], ('Position {0} not equal:\nTEXT[n:n+10] == {1}\n\nHTML[pos:pos+50]== {2}').format(n, text[n:n + 10], check_str[out_html_pos:out_html_pos + 50]))

            qtpos = self.Tab_text.get_text_cursor_pos()
            print 'Got pos', qtpos
            raw_html = self.Tab_text.getHtml()
            deformated = richtext.deformat_html(raw_html, (
             richtext.KEEPIF['black-bold'],
             richtext.KEEPIF['red-underlined-bold']))
            deformated_str = richtext.get_str_formated_true(deformated)
            true_pos = richtext.get_position(deformated, visible_position=qtpos)[0]
            print 'true pos', true_pos
            del qtpos
            del deformated
            del raw_html
            researched = textools.re_search(str(self.Ledit_regexp.text()), deformated_str)
            if researched == None:
                print 'No Match'
                self._disable_signals = False
                return
            if self.Tab_text.Radio_match.isChecked():
                print 'doing match'
                html_list = rsearch_rtext.re_search_format_html(researched)
            else:
                print 'doing replace'
                replaced = textools.re_search_replace(researched, str(self.Ledit_replace.text()), preview=True)
                html_list = rsearch_rtext.re_search_format_html(replaced)
            raw_html = richtext.get_str_formated_html(html_list)
            self.Tab_text.setHtml(raw_html)
            visible_pos = richtext.get_position(html_list, text_position=true_pos)[1]
            print 'new visible pos', visible_pos
            self.Tab_text.set_text_cursor_pos(visible_pos)

        return


if __name__ == '__main__':
    unittest.main()
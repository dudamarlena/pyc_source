# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/htmllist/htmllist_break.py
# Compiled at: 2010-10-16 07:02:00
"""
This module define HtmlListBreak which makes sure every HTML section has some
text in it. It is also calculating the average number of words that in the HTML
list. The counting is done BEFORE rendering the list text.
"""
from htmllist_base import HtmlList, InvalidListException

class HtmlListBreak(HtmlList):
    """ """

    def handle_sub_html(self, lst, next):
        """ Add validation that a sub HTML section has some text in it. """
        if not self._bhp.validate_list(lst, next):
            raise InvalidListException()
        return HtmlList.handle_sub_html(self, lst, next)

    def _find_last_element(self, elm):
        """ keep reference to the last element """
        if elm not in self._elm_set:
            self._elm_set.add(elm)
            self.last_elm = elm

    def avrg_words_in_section(self):
        """ Return the approximate average number of words in a sub HTML section.
                I use a method that returns None as an argument to the traverse_list
                function, to find the last element of the section.
                """
        self._elm_set = set()
        html_lst = self.break_cls.get_text_list(self.pattern_cls.indices_lst)
        total = count = 0
        for (lst, next) in html_lst:
            count += 1
            self.break_cls.traverse_list(lst, self._find_last_element, self._find_last_element, stop_elm=next)
            total += self.break_cls.words_between_elements(lst[0], self.last_elm)

        if count == 0:
            return 0
        return float(total) / count


if __name__ == '__main__':
    pass
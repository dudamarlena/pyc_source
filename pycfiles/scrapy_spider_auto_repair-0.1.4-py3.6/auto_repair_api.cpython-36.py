# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spider_auto_repair\auto_repair_api.py
# Compiled at: 2018-08-13 06:01:22
# Size of source mod 2**32: 2880 bytes
from .auto_repair_code import Page
from .auto_repair_code import auto_repair

def auto_repair_lst(old_page_path, new_page_path, lst_extracted_old_subtrees, rules=None):
    """
        This function is used to repair the incorrect
        data extracted by the broken spider from the new
        page. lst_extracted_old_subtree(passed as an
        argument) is the correct data extracted by the
        unbroken spider from the old page. This data must
        be a list of subtrees in the HTML code of the old
        page. This function repairs the spider to return
        the list of rules, called rules, and it also returns
        the correct data, called lst_repaired_subtrees.
        If rules or the rules are passed to this function,
        then, it uses the rules to find the correct data
        to be extracted from old_page, otherwise, it first
        generates the rules and then, corrects the spider
        and outputs rules(called rules, so that they can be
        used directly on pages having similar layout) as well
        as the lst_repaired_subtrees. See example below.
        Parameters:
            1. old_page_path(type = string)
            2. new_page_path(type = string)
            3. lst_extracted_old_subtree(type = list of lxml.etree._Element objects)
            4. rules(type = list)
        Example:
            >>> old_page_path = 'Examples/Autorepair_Old_Page.html'
            >>> new_page_path = 'Examples/Autorepair_New_Page.html'
            >>> old_page = Page(old_page_path, 'html')
            >>> new_page = Page(new_page_path, 'html')
            >>> lst_extracted_old_subtrees = [old_page.tree.getroot()[0][1][0][0]]
            >>> lst_rules, lst_repaired_subtrees = auto_repair_lst(old_page_path, new_page_path, lst_extracted_old_subtrees)
            >>> lst_rules
            [[([0, 0], [0, 0, 0]), ([0, 1], [0, 0, 1])]]
            >>> len(lst_repaired_subtrees)
            1
            >>> tostring(lst_repaired_subtrees[0])
            b'<div>
                    <div>
                        <p>Username</p>
            <p>email</p>
        <p>Captcha1</p>
                        <p>Captcha2</p>
                    </div>
                </div>
            '
            >>> 
    """
    new_page = Page(new_page_path, 'html')
    old_page = Page(old_page_path, 'html')
    lst_rules = []
    lst_repaired_subtrees = []
    if rules is None:
        rules = [
         None] * len(lst_extracted_old_subtrees)
    idx = 0
    for extracted_old_subtree in lst_extracted_old_subtrees:
        final_rules, repaired_subtree = auto_repair(old_page, new_page, extracted_old_subtree, rules=(rules[idx]))
        lst_rules.append(final_rules)
        lst_repaired_subtrees.append(repaired_subtree)
        idx += 1

    return (
     lst_rules, lst_repaired_subtrees)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/ast_funcs.py
# Compiled at: 2020-04-18 08:04:46
# Size of source mod 2**32: 2562 bytes


def get_assign_name(element):
    """
    Get name assignment associated with the element. The element might be the
    value or the target or something but we just want to identify the closest
    Assign ancestor and get its Name.

    If Assign appears more than once in the ancestral chain e.g.
    body-Assign-spam-eggs-Assign-targets-Name then we get a list like this:
    [body-Assign, body-Assign-spam-eggs-Assign] and we want the closest one to
    the element i.e. assign_els[-1]

    Ordered set of nodes, from parent to ancestor?
    https://stackoverflow.com/a/15645846
    """
    assign_els = element.xpath('ancestor::Assign')
    assign_el = assign_els[(-1)]
    name = assign_el.xpath('targets/Name')[0].get('id')
    return name


def get_xml_element_first_line_no(element):
    element_line_nos = element.xpath('./ancestor-or-self::*[@lineno][1]/@lineno')
    if element_line_nos:
        first_line_no = int(element_line_nos[0])
    else:
        first_line_no = None
    return first_line_no


def _get_last_line_no(element, *, first_line_no):
    last_line_no = None
    ancestor = element
    while True:
        next_siblings = ancestor.xpath('./following-sibling::*')
        for sibling in next_siblings:
            sibling_line_nos = sibling.xpath('./ancestor-or-self::*[@lineno][1]/@lineno')
            if len(sibling_line_nos):
                last_line_no = max(int(sibling_line_nos[0]) - 1, first_line_no)
                break

        ancestor_ancestors = ancestor.xpath('./..')
        if len(ancestor_ancestors):
            ancestor = ancestor_ancestors[0]
        else:
            break

    return last_line_no


def get_xml_element_line_no_range(element):
    element_line_nos = element.xpath('./ancestor-or-self::*[@lineno][1]/@lineno')
    if element_line_nos:
        first_line_no = int(element_line_nos[0])
        last_line_no = _get_last_line_no(element, first_line_no=first_line_no)
    else:
        first_line_no, last_line_no = (None, None)
    return (
     first_line_no, last_line_no)
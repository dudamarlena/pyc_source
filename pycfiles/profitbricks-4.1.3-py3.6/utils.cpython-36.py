# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/profitbricks/utils.py
# Compiled at: 2018-07-12 06:04:26
# Size of source mod 2**32: 3517 bytes
import re

def ask(question, options, default):
    """
    Ask the user a question with a list of allowed answers (like yes or no).

    The user is presented with a question and asked to select an answer from
    the given options list. The default will be returned if the user enters
    nothing. The user is asked to repeat his answer if his answer does not
    match any of the allowed anwsers.

    :param    question: Question to present to the user (without question mark)
    :type     question: ``str``

    :param    options: List of allowed anwsers
    :type     options: ``list``

    :param    default: Default answer (if the user enters no text)
    :type     default: ``str``

    """
    assert default in options
    question += ' ({})? '.format('/'.join((o.upper() if o == default else o) for o in options))
    selected = None
    while selected not in options:
        selected = input(question).strip().lower()
        if selected == '':
            selected = default
        elif selected not in options:
            question = "Please type '{}'{comma} or '{}': ".format(("', '".join(options[:-1])),
              (options[(-1)]), comma=(',' if len(options) > 2 else ''))

    return selected


def find_item_by_name(list_, namegetter, name):
    """
    Find a item a given list by a matching name.

    The search for the name is done in this relaxing way:

    - exact name match
    - case-insentive name match
    - attribute starts with the name
    - attribute starts with the name (case insensitive)
    - name appears in the attribute
    - name appears in the attribute (case insensitive)

    :param    list_: A list of elements
    :type     list_: ``list``

    :param    namegetter: Function that returns the name for a given
                          element in the list
    :type     namegetter: ``function``

    :param    name: Name to search for
    :type     name: ``str``

    """
    matching_items = [i for i in list_ if namegetter(i) == name]
    if len(matching_items) == 0:
        prog = re.compile(re.escape(name) + '$', re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if len(matching_items) == 0:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if len(matching_items) == 0:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if len(matching_items) == 0:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    if len(matching_items) == 0:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    return matching_items
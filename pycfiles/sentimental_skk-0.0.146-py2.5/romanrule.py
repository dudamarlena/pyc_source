# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/romanrule.py
# Compiled at: 2014-03-11 11:41:30
import kanadb, rule, logging
SKK_ROMAN_VALUE = 65540
SKK_ROMAN_NEXT = 65541
SKK_ROMAN_PREV = 65542
SKK_ROMAN_BUFFER = 65543

def _maketree(rule, onbin, txu, nn):
    """ makes try-tree """
    tree = {}
    for (key, value) in rule.items():
        buf = ''
        context = tree
        for c in key:
            code = ord(c)
            if code not in context:
                context[code] = {SKK_ROMAN_PREV: context}
            context = context[code]
            buf += chr(code)
            context[SKK_ROMAN_BUFFER] = buf

        context[SKK_ROMAN_VALUE] = value
        first = key[0]
        if first in onbin:
            key = first + key
            value = txu + value
            buf = ''
            context = tree
            for c in key:
                code = ord(c)
                if code not in context:
                    context[code] = {SKK_ROMAN_PREV: context}
                context = context[code]
                if buf == chr(code):
                    buf = txu
                buf += chr(code)
                context[SKK_ROMAN_BUFFER] = buf

            context[SKK_ROMAN_VALUE] = value

    for (key, value) in tree.items():
        context = tree
        if key == 110:
            for c in onbin:
                code = ord(c)
                value[code] = {SKK_ROMAN_VALUE: nn, SKK_ROMAN_NEXT: tree[code]}

    tree[SKK_ROMAN_BUFFER] = ''
    tree[SKK_ROMAN_PREV] = tree
    return tree


def _make_rules(rule):
    hira_rule = rule
    kata_rule = {}
    for (key, value) in hira_rule.items():
        kata_rule[key] = kanadb.to_kata(value)

    return (
     hira_rule, kata_rule)


def compile(method='builtin_normal'):
    r""" make hiragana/katakana input state trie-tree
    >>> hira_tree, kata_tree = compile('builtin_normal')
    >>> hira_tree[ord('k')][ord('y')][ord('a')][SKK_ROMAN_VALUE]
    u'\u304d\u3083'
    >>> hira_tree[ord('t')][ord('t')][ord('a')][SKK_ROMAN_VALUE]
    u'\u3063\u305f'
    >>> kata_tree[ord('k')][ord('y')][ord('a')][SKK_ROMAN_VALUE]
    u'\u30ad\u30e3'
    >>> hira_tree, kata_tree = compile('builtin_azik')
    >>> hira_tree[ord('k')][ord('y')][ord('a')][SKK_ROMAN_VALUE]
    u'\u304d\u3083'
    >>> kata_tree[ord('k')][ord('y')][ord('a')][SKK_ROMAN_VALUE]
    u'\u30ad\u30e3'
    >>> hira_tree, kata_tree = compile('builtin_act')
    >>> hira_tree[ord('c')][ord('g')][ord('a')][SKK_ROMAN_VALUE]
    u'\u304d\u3083'
    >>> kata_tree[ord('c')][ord('g')][ord('a')][SKK_ROMAN_VALUE]
    u'\u30ad\u30e3'
    """
    logging.info('compile roman rule: %s' % method)
    (_base_name, base_ruledict) = rule.get('builtin_base')
    (name, ruledict) = rule.get(method)
    ruledict.update(base_ruledict)
    (hira_rule, kata_rule) = _make_rules(ruledict)
    if method == 'builtin_normal':
        onbin = 'bcdfghjkmprstvwxz'
    else:
        onbin = 'w'
    _hira_tree = _maketree(hira_rule, onbin, 'っ', 'ん')
    _kata_tree = _maketree(kata_rule, onbin, 'ッ', 'ン')
    return (
     _hira_tree, _kata_tree)


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()
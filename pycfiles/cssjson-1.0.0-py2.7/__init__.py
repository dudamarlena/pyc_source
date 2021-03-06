# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cssjson/__init__.py
# Compiled at: 2019-04-03 20:10:23
import cssutils
from pprint import pprint
import json

def toJSON(text, path=False, url=False):
    dct = {'rules': {}}
    if path:
        sheet = cssutils.parseFile(text)
    else:
        if url:
            sheet = cssutils.parseUrl(text)
        else:
            sheet = cssutils.parseString(text)
        for rule in sheet:
            try:
                selector = rule.selectorText
                styles = rule.style.cssText.split(';\n')
                properties = {}
                for s in styles:
                    _s = s.split(':')
                    if len(_s) != 1:
                        prop_name = _s[0]
                        prop_attr = _s[1]
                        if len(_s) > 2:
                            prop_attr = (':').join(_s[1:])
                        properties[prop_name] = prop_attr.strip()

                dct['rules'][selector] = {'attr': properties}
            except Exception as E:
                try:
                    media = rule.media.mediaText
                    mrules = rule.cssRules
                    dct['rules']['@media ' + media] = {'rules': {}}
                    for mrule in mrules:
                        selector = mrule.selectorText
                        styles = mrule.style.cssText.split(';\n')
                        properties = {}
                        for s in styles:
                            _s = s.split(':')
                            prop_name = _s[0]
                            prop_attr = _s[1]
                            if len(_s) > 2:
                                prop_attr = (':').join(_s[1:])
                            properties[prop_name] = prop_attr.strip()

                        dct['rules'][('@media ' + media)]['rules'].update({selector: {'attr': properties}})

                except:
                    pass

    return dct


def toCSS(css):
    if not isinstance(css, dict):
        raise TypeError('Invalid type error. Provide a dict/json serialized css')
    css_result = ''
    css_block = '{} {}\n{}{}\n'
    for rule, attrs in css['rules'].items():
        attrs_result = ''
        if attrs.get('attr', None):
            for prop, attr in attrs['attr'].items():
                attrs_block = '{}:{};\n'
                attrs_result += attrs_block.format(prop, attr.encode('ascii', 'ignore'))

            css_result += css_block.format(rule, '{', attrs_result, '}')
        elif attrs.get('rules', None):
            media_result = ''
            media_block = '{} {}\n{}{}\n'
            for mrule, mattrs in attrs['rules'].items():
                mattrs_result = ''
                for prop, attr in mattrs['attr'].items():
                    attrs_block = '{}:{};\n'
                    mattrs_result += attrs_block.format(prop, attr.encode('ascii', 'ignore'))

                media_result += css_block.format(mrule, '{', mattrs_result, '}')

            media_block.format(rule, '{', media_result, '}')
            css_result += media_block

    return css_result
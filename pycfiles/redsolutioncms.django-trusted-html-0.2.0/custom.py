# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\html\custom.py
# Compiled at: 2014-04-29 06:05:21
"""
Attributes for Index of Attributes
http://www.w3.org/TR/REC-html40/index/attributes.html
"""
from trustedhtml.utils import get_dict
from trustedhtml.classes import Element
from trustedhtml.rules import css
from trustedhtml.rules.html.elements import elements
from trustedhtml.rules.html.attributes import attributes
docement_elements = [
 'body',
 'head',
 'html',
 'link',
 'meta',
 'title']
frame_elements = [
 'frame',
 'frameset',
 'noframes']
form_elements = [
 'button',
 'fieldset',
 'form',
 'input',
 'label',
 'legend',
 'optgroup',
 'option',
 'select',
 'textarea']
remove_elements = [
 'base',
 'basefont',
 'center',
 'dir',
 'font',
 'isindex',
 'menu',
 'noscript',
 's',
 'strike',
 'style',
 'u']
remove_elements_with_content = [
 'applet',
 'script']
pretty_elements = [
 'a',
 'address',
 'blockquote',
 'br',
 'caption',
 'del',
 'div',
 'em',
 'h1',
 'h2',
 'h3',
 'h4',
 'h5',
 'h6',
 'hr',
 'ins',
 'img',
 'li',
 'object',
 'iframe',
 'ol',
 'p',
 'pre',
 'q',
 'param',
 'small',
 'span',
 'strong',
 'sub',
 'sup',
 'table',
 'tbody',
 'td',
 'th',
 'tr',
 'ul',
 'noindex']
rare_elements = [
 'abbr',
 'acronym',
 'area',
 'b',
 'bdo',
 'big',
 'cite',
 'code',
 'col',
 'colgroup',
 'dd',
 'dfn',
 'dl',
 'dt',
 'i',
 'kbd',
 'map',
 'samp',
 'tfoot',
 'thead',
 'tt',
 'var']
remove_attributes_for_all = [
 'accesskey',
 'id',
 'class',
 'compact',
 'bgcolor',
 'frameborder',
 'hspace',
 'onblur',
 'onchange',
 'onclick',
 'ondblclick',
 'onfocus',
 'onkeydown',
 'onkeypress',
 'onkeyup',
 'onload',
 'onmousedown',
 'onmousemove',
 'onmouseout',
 'onmouseover',
 'onmouseup',
 'onreset',
 'onselect',
 'onsubmit',
 'onunload',
 'nowrap',
 'vspace']
remove_attributes_for_element = {}
remove_attributes_for_element['body'] = [
 'align',
 'alink',
 'background',
 'link',
 'text',
 'vlink']
remove_attributes_for_element['col'] = [
 'width']
remove_attributes_for_element['colgroup'] = [
 'width']
remove_attributes_for_element['div'] = [
 'align']
remove_attributes_for_element['h1'] = [
 'align']
remove_attributes_for_element['h2'] = [
 'align']
remove_attributes_for_element['h3'] = [
 'align']
remove_attributes_for_element['h4'] = [
 'align']
remove_attributes_for_element['h5'] = [
 'align']
remove_attributes_for_element['h6'] = [
 'align']
remove_attributes_for_element['html'] = [
 'version']
remove_attributes_for_element['hr'] = [
 'align',
 'noshade',
 'size',
 'width']
remove_attributes_for_element['img'] = [
 'align',
 'border']
remove_attributes_for_element['input'] = [
 'align',
 'src']
remove_attributes_for_element['legend'] = [
 'align']
remove_attributes_for_element['li'] = [
 'type',
 'value']
remove_attributes_for_element['object'] = [
 'align',
 'border']
remove_attributes_for_element['ol'] = [
 'start',
 'type']
remove_attributes_for_element['p'] = [
 'align']
remove_attributes_for_element['pre'] = [
 'width']
remove_attributes_for_element['table'] = [
 'align',
 'border',
 'cellpadding',
 'cellspacing',
 'frame',
 'rules',
 'width']
remove_attributes_for_element['td'] = [
 'height',
 'width']
remove_attributes_for_element['th'] = [
 'height',
 'width']
remove_attributes_for_element['ul'] = [
 'type']
replace_attributes_for_all = {'style': css.common}
replace_attributes_for_element = {}
replace_attributes_for_element['img'] = {'style': css.images}
replace_attributes_for_element['caption'] = {'style': css.tables}
replace_attributes_for_element['thead'] = {'style': css.tables}
replace_attributes_for_element['tfoot'] = {'style': css.tables}
replace_attributes_for_element['tbody'] = {'style': css.tables}
replace_attributes_for_element['tr'] = {'style': css.tables}
replace_attributes_for_element['td'] = {'style': css.tables}
replace_attributes_for_element['th'] = {'style': css.tables}

def get_elements(leave):
    result = {}
    for name, value in get_dict(source=elements, leave=leave).iteritems():
        remove = remove_attributes_for_all + remove_attributes_for_element.get(name, [])
        replace = {}
        replace.update(replace_attributes_for_all)
        replace.update(replace_attributes_for_element.get(name, {}))
        rules = get_dict(attributes[name], remove=remove, append=replace)
        element = Element(rules=rules, empty_element=value.empty_element, default=value.default, optional_start=value.optional_start, optional_end=value.optional_end, contents=value.contents, save_content=value.save_content)
        result[name] = element

    for name in remove_elements_with_content:
        element = Element(remove_element=True, save_content=False)
        result[name] = element

    return result


pretty = get_elements(pretty_elements)
normal = get_elements(pretty_elements + rare_elements)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\html\values.py
# Compiled at: 2014-04-29 06:05:21
"""
Values for Index of Attributes
http://www.w3.org/TR/REC-html40/index/attributes.html

Attributes for different elements can have different validation mechanism.
In such case we will use different names:
name of attribute followed immediately by an '~' character followed immediately
by [a-z] character.

Attributes for different elements can have same validation mechanism,
but separated in specification because of meaning.
In such case we will assign same values to the same attributes.
We do it to parse descriptions and generate ``map.py``.
"""
from trustedhtml.classes import RegExp, Sequence
from trustedhtml.rules.html.types import name, name_required, idrefs, idrefs_comma, number, number_required, positive_number, text, text_required, text_default, uri, uri_required, uri_image, uri_object, uri_image_required, uris, color, pixels, length, multi_length, multi_lengths, length_required, coords, content_type, content_types, content_type_required, language_code, charset, charsets, character, datetime, link_types, media_descs, style_sheet, frame_target, script
values = {}
values['abbr'] = text
values['accept-charset'] = charsets
values['accept'] = content_types
values['accesskey'] = character
values['action'] = uri_required
values['align~c'] = RegExp(regexp='(top|bottom|left|right)$')
values['align~i'] = RegExp(regexp='(top|middle|bottom|left|right)$')
values['align~l'] = RegExp(regexp='(top|bottom|left|right)$')
values['align~t'] = RegExp(regexp='(left|center|right)$')
values['align~h'] = RegExp(regexp='(left|center|right)$')
values['align~d'] = RegExp(regexp='(left|center|right|justify)$')
values['align'] = RegExp(regexp='(left|center|right|justify|char)$')
values['alink'] = color
values['alt'] = text
values['alt~r'] = text_required
values['alt~i'] = text_default
values['alt'] = text
values['archive~a'] = Sequence(rule=uri_object, regexp='\\s*,\\s*', join_string=',')
values['archive'] = Sequence(rule=uri_object, regexp='\\s+', join_string=' ')
values['axis'] = idrefs_comma
values['background'] = uri_image
values['bgcolor'] = color
values['bgcolor'] = color
values['bgcolor'] = color
values['bgcolor'] = color
values['border'] = pixels
values['border'] = pixels
values['cellpadding'] = length
values['cellspacing'] = length
values['char'] = character
values['charoff'] = length
values['charset'] = charset
values['checked'] = RegExp(regexp='(checked)$')
values['cite'] = uri
values['cite'] = uri
values['class'] = idrefs
values['classid'] = uri_object
values['clear'] = RegExp(regexp='(left|all|right|none)$')
values['code'] = text
values['codebase'] = uri_object
values['codebase'] = uri_object
values['codetype'] = content_type
values['color'] = color
values['cols'] = multi_lengths
values['cols'] = number_required
values['colspan'] = number
values['compact'] = RegExp(regexp='(compact)$')
values['content'] = text_required
values['coords'] = coords
values['coords'] = coords
values['data'] = uri_object
values['datetime'] = datetime
values['declare'] = RegExp(regexp='(declare)$')
values['defer'] = RegExp(regexp='(defer)$')
values['dir'] = RegExp(regexp='(ltr|rtl)$')
values['dir~r'] = RegExp(regexp='(ltr|rtl)$', element_exception=True)
values['disabled'] = RegExp(regexp='(disabled)$')
values['enctype'] = content_type
values['face'] = idrefs_comma
values['for'] = name
values['frame'] = RegExp(regexp='(void|above|below|hsides|lhs|rhs|vsides|box|border)$')
values['frameborder'] = RegExp(regexp='(1|0)$')
values['headers'] = idrefs
values['height'] = length
values['height'] = length
values['height'] = length
values['height~r'] = length_required
values['href'] = uri
values['href~r'] = uri_required
values['href'] = uri
values['hreflang'] = language_code
values['hspace'] = pixels
values['http-equiv'] = name
values['id'] = name
values['ismap'] = RegExp(regexp='(ismap)$')
values['label'] = text
values['label~r'] = text_required
values['lang'] = language_code
values['language'] = text
values['link'] = color
values['longdesc'] = uri
values['longdesc'] = uri
values['marginheight'] = pixels
values['marginwidth'] = pixels
values['maxlength'] = number
values['media'] = media_descs
values['media'] = media_descs
values['method'] = RegExp(regexp='(GET|POST)$')
values['multiple'] = RegExp(regexp='(multiple)$')
values['name'] = name
values['name'] = name
values['name'] = name
values['name'] = name
values['name'] = name
values['name'] = name
values['name'] = name
values['name~r'] = name_required
values['name'] = name
values['name~r'] = name_required
values['name~r'] = name_required
values['name'] = name
values['nohref'] = RegExp(regexp='(nohref)$')
values['noresize'] = RegExp(regexp='(noresize)$')
values['noshade'] = RegExp(regexp='(noshade)$')
values['nowrap'] = RegExp(regexp='(nowrap)$')
values['object'] = name
values['onblur'] = script
values['onchange'] = script
values['onclick'] = script
values['ondblclick'] = script
values['onfocus'] = script
values['onkeydown'] = script
values['onkeypress'] = script
values['onkeyup'] = script
values['onload'] = script
values['onload'] = script
values['onmousedown'] = script
values['onmousemove'] = script
values['onmouseout'] = script
values['onmouseover'] = script
values['onmouseup'] = script
values['onreset'] = script
values['onselect'] = script
values['onsubmit'] = script
values['onunload'] = script
values['onunload'] = script
values['profile'] = uris
values['prompt'] = text
values['readonly'] = RegExp(regexp='(readonly)$')
values['readonly'] = RegExp(regexp='(readonly)$')
values['rel'] = link_types
values['rev'] = link_types
values['rows'] = multi_lengths
values['rows'] = number_required
values['rowspan'] = number
values['rules'] = RegExp(regexp='(none|groups|rows|cols|all)$')
values['scheme'] = text
values['scope'] = RegExp(regexp='(row|col|rowgroup|colgroup)$')
values['scrolling'] = RegExp(regexp='(yes|no|auto)$')
values['selected'] = RegExp(regexp='(selected)$')
values['shape'] = RegExp(regexp='(default|rect|circle|poly)$')
values['shape'] = RegExp(regexp='(default|rect|circle|poly)$')
values['size~h'] = pixels
values['size~f'] = RegExp(regexp='([-+]?[1-7])$')
values['size'] = number
values['size~b'] = RegExp(regexp='([-+]?[1-7])$', element_exception=True)
values['size'] = number
values['span'] = positive_number
values['span'] = positive_number
values['src'] = uri
values['src~i'] = uri_image
values['src~f'] = uri_object
values['src~r'] = uri_image_required
values['standby'] = text
values['start'] = number
values['style'] = style_sheet
values['summary'] = text
values['tabindex'] = number
values['target'] = frame_target
values['text'] = color
values['title'] = text
values['type'] = content_type
values['type'] = content_type
values['type'] = content_type
values['type~r'] = content_type_required
values['type~r'] = content_type_required
values['type~i'] = RegExp(regexp='(text|password|checkbox|radio|submit|reset|file|hidden|image|button)$')
values['type~l'] = RegExp(regexp='(1|a|A|i|I|disc|square|circle)$')
values['type~o'] = RegExp(regexp='(1|a|A|i|I)$')
values['type~u'] = RegExp(regexp='(disc|square|circle)$')
values['type~b'] = RegExp(regexp='(button|submit|reset)$')
values['usemap'] = uri
values['valign'] = RegExp(regexp='(top|middle|bottom|baseline)$')
values['value'] = text
values['value'] = text
values['value'] = text
values['value'] = text
values['value~l'] = number
values['valuetype'] = RegExp(regexp='(data|ref|object)$')
values['version'] = uri
values['vlink'] = color
values['vspace'] = pixels
values['width'] = length
values['width'] = length
values['width'] = length
values['width'] = length
values['width'] = length
values['width~r'] = length_required
values['width~c'] = multi_length
values['width~c'] = multi_length
values['width~p'] = number
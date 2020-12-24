# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Dropbox\vk\django-trusted-html\trustedhtml\rules\html\grammar.py
# Compiled at: 2014-04-29 06:05:21
"""
The grammar of HTML 4.0 based on
http://www.w3.org/TR/REC-html40/types.html
"""
grammar = {}
grammar['h'] = '([0-9a-f])' % grammar
grammar['w'] = '([ \\t\\r\\n\\f]*)' % grammar
grammar['name'] = '([a-z][-_:.a-z0-9]*)' % grammar
grammar['number'] = '([0-9]+)' % grammar
grammar['positive-number'] = '([1-9][0-9]*)' % grammar
grammar['percentage'] = '(%(number)s%%)' % grammar
grammar['length'] = '(%(number)s|%(percentage)s)' % grammar
grammar['multi-length'] = '(%(number)s|%(percentage)s|%(number)s\\*|\\*)' % grammar
grammar['color'] = '(#%(h)s{6}|black|green|silver|lime|gray|olive|white|yellow|maroon|navy|red|blue|purple|teal|fuchsia|aqua)' % grammar
grammar['content-type'] = '(text/html|image/(jpeg|png|gif)|audio/mpeg|video/mpeg|application/(x\\-www\\-form\\-urlencoded|x\\-shockwave\\-flash)|multipart/form\\-data)' % grammar
grammar['language-code'] = '([a-z]{1-8}(-[a-z]{1-8})*)' % grammar
grammar['charset'] = '((?!utf-7$)([-+:.a-z0-9]+))' % grammar
grammar['datetime'] = '([0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9](Z|([-+][0-2][0-9]:[0-5][0-9])))' % grammar
grammar['link-types'] = '(%(name)s(%(w)s%(name)s))' % grammar
grammar['media-desc'] = '([-a-z0-9]+)' % grammar
grammar['frame-target'] = '(_blank|_self|_parent|_top|[a-z]+)'
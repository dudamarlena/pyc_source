# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/roles_plain.py
# Compiled at: 2008-02-24 09:47:59
"""Additional roles for reference documentation.
"""
import re
from docutils import nodes, utils
from docutils.parsers.rst import roles
innernodetypes = {'ref': nodes.emphasis, 'term': nodes.emphasis, 'token': nodes.strong}
ws_re = re.compile('\\s+')
_litvar_re = re.compile('{([^}]+)}')

def deprecated_xfileref_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    if text[0:1] == '!':
        text = text[1:]
        return ([innernodetypes.get(typ, nodes.literal)(rawtext, text, classes=['xref'])], [])
    pnode = addnodes.pending_xref(rawtext)
    pnode['reftype'] = typ
    if text[0:1] == '.' and typ in ('data', 'exc', 'func', 'class', 'const', 'attr',
                                    'meth'):
        text = text[1:]
        pnode['refspecific'] = True
    pnode['reftarget'] = ws_re.sub(typ == 'term' and ' ' or '', text)
    pnode += innernodetypes.get(typ, nodes.literal)(rawtext, text, classes=['xref'])
    return (
     [
      pnode], [])


def emph_literal_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    retnodes = []
    pos = 0
    for m in _litvar_re.finditer(text):
        if m.start() > pos:
            txt = text[pos:m.start()]
            retnodes.append(nodes.literal(txt, txt))
        retnodes.append(nodes.emphasis('', '', nodes.literal(m.group(1), m.group(1))))
        pos = m.end()

    if pos < len(text):
        node = nodes.literal(text[pos:], text[pos:])
        node['classes'] += ['role', 'role-' + str(typ)]
        retnodes.append(node)
    return (
     retnodes, [])


specific_docroles = {'data': emph_literal_role, 'exc': emph_literal_role, 'func': emph_literal_role, 'class': emph_literal_role, 'const': emph_literal_role, 'attr': emph_literal_role, 'meth': emph_literal_role, 'cfunc': emph_literal_role, 'cdata': emph_literal_role, 'ctype': emph_literal_role, 'cmacro': emph_literal_role, 'mod': emph_literal_role, 'keyword': emph_literal_role, 'ref': emph_literal_role, 'token': emph_literal_role, 'term': emph_literal_role, 'file': emph_literal_role, 'samp': emph_literal_role}
for (rolename, func) in specific_docroles.iteritems():
    roles.register_canonical_role(rolename, func)
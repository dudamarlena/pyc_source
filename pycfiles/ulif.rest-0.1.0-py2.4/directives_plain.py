# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/directives_plain.py
# Compiled at: 2008-02-24 09:47:59
"""
Additional directives for reference documentation.
"""
from os import path
import re
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.directives import admonitions
py_sig_re = re.compile('^([\\w.]*\\.)?        # class names\n                           (\\w+)  \\s*          # thing name\n                           (?: \\((.*)\\) )? $   # optionally arguments\n                        ', re.VERBOSE)
py_paramlist_re = re.compile('([\\[\\],])')

def parse_py_signature(signode, sig, desctype):
    """
    Transform a python signature into RST nodes.

    Return (fully qualified name of the thing, classname if any).
    """
    m = py_sig_re.match(sig)
    if m is None:
        raise ValueError
    (classname, name, arglist) = m.groups()
    fullname = classname and classname + name or name
    if classname is not None:
        signode += nodes.strong(classname, classname)
    signode += nodes.strong(name, name)
    if not arglist:
        if desctype in ('function', 'method'):
            signode += nodes.inline('()', '()')
        return (
         fullname, classname)
    signode += nodes.inline()
    paramlist = py_paramlist_re.split(arglist)
    if len(paramlist):
        signode += nodes.inline('(', '(')
    stack = [
     signode[(-1)]]
    for token in paramlist:
        if token == '[':
            opt = nodes.inline('[', '[')
            stack[(-1)] += opt
            stack.append(opt)
        elif token == ']':
            stack[(-1)] += nodes.inline(token, token)
            try:
                stack.pop()
            except IndexError:
                raise ValueError

        elif not token or token == ',' or token.isspace():
            if token:
                if token == ',':
                    stack[(-1)] += nodes.inline(', ', ', ')
                else:
                    stack[(-1)] += nodes.inline(token, token)
        else:
            token = token.strip()
            paramnode = nodes.emphasis(token, token)
            stack[(-1)] += paramnode

    if len(stack) != 1:
        raise ValueError
    if len(paramlist):
        signode += nodes.inline(')', ')')
    return (
     fullname, classname)


from docutils import nodes

def toctree_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    try:
        settings = state.document.settings
        filename = settings._source
        dirname = path.dirname(filename)
    except AttributeError:
        dirname = '.'

    subnode = nodes.comment()
    includefiles = filter(None, content)
    includefiles = map(lambda x: path.normpath(path.join(dirname, x)), includefiles)
    subnode['includefiles'] = includefiles
    subnode['maxdepth'] = options.get('maxdepth', -1)
    return [subnode]


toctree_directive.content = 1
toctree_directive.options = {'maxdepth': int}
directives.register_directive('toctree', toctree_directive)

def desc_directive(desctype, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    node = nodes.admonition()
    node['classes'] += ['desc-' + str(desctype)]
    signatures = map(lambda s: s.strip(), arguments[0].split('\n'))
    node['desctype'] = desctype
    names = []
    for (i, sig) in enumerate(signatures):
        sig = sig.strip()
        signode = nodes.inline(sig, '')
        signode['first'] = False
        node.append(signode)
        try:
            if desctype in ('function', 'data', 'class', 'exception', 'method', 'attribute'):
                (name, clsname) = parse_py_signature(signode, sig, desctype)
        except ValueError, err:
            signode.clear()
            signode += nodes.inline(sig, sig)
            continue

    subnode = nodes.container()
    state.nested_parse(content, content_offset, subnode)
    node.append(subnode)
    return [node]


desc_directive.content = 1
desc_directive.arguments = (1, 0, 1)
desc_directive.options = {'noindex': directives.flag}
desctypes = [
 'function', 'data', 'class', 'method', 'attribute', 'exception', 'cmdoption', 'envvar', 'describe']
for name in desctypes:
    directives.register_directive(name, desc_directive)

def seealso_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """A directive to indicate, that other things are of interest as
    well.
    """
    options['class'] = [
     str(name)]
    rv = admonitions.make_admonition(nodes.admonition, name, ['See also:'], options, content, lineno, content_offset, block_text, state, state_machine)
    return rv


seealso_directive.content = 1
seealso_directive.arguments = (0, 0, 0)
directives.register_directive('seealso', seealso_directive)

def version_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """A directive to indicate version related modifications.
    """
    node = nodes.admonition()
    node['type'] = name
    node['version'] = arguments[0]
    if name == 'versionchanged':
        text = 'Changed in version %s: ' % node['version']
    elif name == 'versionadded':
        text = 'Added in version %s: ' % node['version']
    elif name == 'deprecated':
        text = 'Deprecated from version %s: ' % node['version']
    else:
        text = '%s %s: ' % (name, arguments[0])
    arguments[0] = text
    options['class'] = [
     str(name)]
    rv = admonitions.make_admonition(nodes.admonition, name, arguments, options, content, lineno, content_offset, block_text, state, state_machine)
    return rv


version_directive.arguments = (1, 1, 1)
version_directive.content = 1
directives.register_directive('deprecated', version_directive)
directives.register_directive('versionadded', version_directive)
directives.register_directive('versionchanged', version_directive)
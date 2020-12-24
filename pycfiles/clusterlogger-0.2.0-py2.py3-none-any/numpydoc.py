# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ajoly/git/clusterlib/doc/sphinxext/numpy_ext/numpydoc.py
# Compiled at: 2014-11-27 05:24:09
__doc__ = b"\n========\nnumpydoc\n========\n\nSphinx extension that handles docstrings in the Numpy standard format. [1]\n\nIt will:\n\n- Convert Parameters etc. sections to field lists.\n- Convert See Also section to a See also entry.\n- Renumber references.\n- Extract the signature from the docstring, if it can't be determined\n  otherwise.\n\n.. [1] http://projects.scipy.org/numpy/wiki/CodingStyleGuidelines#docstring-standard\n\n"
from __future__ import unicode_literals
import sys, os, re, pydoc
from .docscrape_sphinx import get_doc_object
from .docscrape_sphinx import SphinxDocString
import inspect

def mangle_docstrings(app, what, name, obj, options, lines, reference_offset=[
 0]):
    global get_doc_object
    cfg = dict(use_plots=app.config.numpydoc_use_plots, show_class_members=app.config.numpydoc_show_class_members)
    if what == b'module':
        title_re = re.compile(b'^\\s*[#*=]{4,}\\n[a-z0-9 -]+\\n[#*=]{4,}\\s*', re.I | re.S)
        lines[:] = title_re.sub(b'', (b'\n').join(lines)).split(b'\n')
    else:
        doc = get_doc_object(obj, what, (b'\n').join(lines), config=cfg)
        if sys.version_info[0] < 3:
            lines[:] = unicode(doc).splitlines()
        else:
            lines[:] = str(doc).splitlines()
        if app.config.numpydoc_edit_link and hasattr(obj, b'__name__') and obj.__name__:
            if hasattr(obj, b'__module__'):
                v = dict(full_name=b'%s.%s' % (obj.__module__, obj.__name__))
            else:
                v = dict(full_name=obj.__name__)
            lines += [b'', b'.. htmlonly::', b'']
            lines += [ b'    %s' % x for x in (app.config.numpydoc_edit_link % v).split(b'\n')
                     ]
        references = []
        for line in lines:
            line = line.strip()
            m = re.match(b'^.. \\[([a-z0-9_.-])\\]', line, re.I)
            if m:
                references.append(m.group(1))

    references.sort(key=lambda x: -len(x))
    if references:
        for i, line in enumerate(lines):
            for r in references:
                if re.match(b'^\\d+$', r):
                    new_r = b'R%d' % (reference_offset[0] + int(r))
                else:
                    new_r = b'%s%d' % (r, reference_offset[0])
                lines[i] = lines[i].replace(b'[%s]_' % r, b'[%s]_' % new_r)
                lines[i] = lines[i].replace(b'.. [%s]' % r, b'.. [%s]' % new_r)

    reference_offset[0] += len(references)


def mangle_signature(app, what, name, obj, options, sig, retann):
    if inspect.isclass(obj) and (not hasattr(obj, b'__init__') or b'initializes x; see ' in pydoc.getdoc(obj.__init__)):
        return ('', '')
    if not (callable(obj) or hasattr(obj, b'__argspec_is_invalid_')):
        return
    if not hasattr(obj, b'__doc__'):
        return
    doc = SphinxDocString(pydoc.getdoc(obj))
    if doc[b'Signature']:
        sig = re.sub(b'^[^(]*', b'', doc[b'Signature'])
        return (
         sig, b'')


def setup(app, get_doc_object_=get_doc_object):
    global get_doc_object
    get_doc_object = get_doc_object_
    if sys.version_info[0] < 3:
        app.connect(b'autodoc-process-docstring', mangle_docstrings)
        app.connect(b'autodoc-process-signature', mangle_signature)
    else:
        app.connect(b'autodoc-process-docstring', mangle_docstrings)
        app.connect(b'autodoc-process-signature', mangle_signature)
    app.add_config_value(b'numpydoc_edit_link', None, False)
    app.add_config_value(b'numpydoc_use_plots', None, False)
    app.add_config_value(b'numpydoc_show_class_members', True, True)
    app.add_domain(NumpyPythonDomain)
    app.add_domain(NumpyCDomain)
    return


try:
    import sphinx
except ImportError:
    CDomain = PythonDomain = object
else:
    from sphinx.domains.c import CDomain
    from sphinx.domains.python import PythonDomain

class ManglingDomainBase(object):
    directive_mangling_map = {}

    def __init__(self, *a, **kw):
        super(ManglingDomainBase, self).__init__(*a, **kw)
        self.wrap_mangling_directives()

    def wrap_mangling_directives(self):
        for name, objtype in self.directive_mangling_map.items():
            self.directives[name] = wrap_mangling_directive(self.directives[name], objtype)


class NumpyPythonDomain(ManglingDomainBase, PythonDomain):
    name = b'np'
    directive_mangling_map = {b'function': b'function', 
       b'class': b'class', 
       b'exception': b'class', 
       b'method': b'function', 
       b'classmethod': b'function', 
       b'staticmethod': b'function', 
       b'attribute': b'attribute'}


class NumpyCDomain(ManglingDomainBase, CDomain):
    name = b'np-c'
    directive_mangling_map = {b'function': b'function', 
       b'member': b'attribute', 
       b'macro': b'function', 
       b'type': b'class', 
       b'var': b'object'}


def wrap_mangling_directive(base_directive, objtype):

    class directive(base_directive):

        def run(self):
            env = self.state.document.settings.env
            name = None
            if self.arguments:
                m = re.match(b'^(.*\\s+)?(.*?)(\\(.*)?', self.arguments[0])
                name = m.group(2).strip()
            if not name:
                name = self.arguments[0]
            lines = list(self.content)
            mangle_docstrings(env.app, objtype, name, None, None, lines)
            from docutils.statemachine import ViewList
            self.content = ViewList(lines, self.content.parent)
            return base_directive.run(self)

    return directive
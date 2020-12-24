# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christian/Dropbox/workspace/masai/doc/sphinxext/fortran_domain.py
# Compiled at: 2012-11-24 14:59:46
"""
A fortran domain for sphinx

"""
import re
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.compat import Directive
from sphinx.util.docfields import Field, GroupedField, TypedField, DocFieldTransformer, _is_single_paragraph

def convert_arithm(node, expr, modname=None, nodefmt=nodes.Text):
    """Format an arithmetic expression for a node"""
    ops = re.findall('(\\W+)', expr)
    nums = re.split('\\W+', expr)
    if len(nums) != len(ops):
        ops.append('')
    for num, op in zip(nums, ops):
        if num:
            if num[0].isalpha():
                refnode = addnodes.pending_xref('', refdomain='f', reftype='var', reftarget=num, modname=modname)
                refnode += nodefmt(num, num)
                node += refnode
            else:
                node += nodefmt(num, num)
        if op:
            node += nodefmt(op, op)


def parse_shape(shape):
    if not shape:
        return
    if not shape.startswith('('):
        shape = '(' + shape
    if not shape.endswith(')'):
        shape += ')'
    return shape


def add_shape(node, shape, modname=None, nodefmt=nodes.Text):
    """Format a shape expression for a node"""
    dims = re.split('\\s*,\\s*', shape.strip('( )'))
    node += nodefmt(' (', ' (')
    convert_arithm(node, shape.strip('( )'), modname=modname, nodefmt=nodefmt)
    node += nodefmt(')', ')')


re_name_shape = re.compile('(\\w+)(\\(.+\\))?')
re_fieldname_match = re.compile('(?P<type>\\b\\w+\\b)?\\s*(?P<name>\\b\\w+\\b)\\s*(?P<shape>\\(.*\\))?\\s*(?P<sattrs>\\[.+\\])?').match

class FortranField(Field):

    def make_xref(self, rolename, domain, target, innernode=nodes.emphasis, modname=None, typename=None):
        if not rolename:
            return innernode(target, target)
        refnode = addnodes.pending_xref('', refdomain=domain, refexplicit=False, reftype=rolename, reftarget=target, modname=modname, typename=typename)
        refnode += innernode(target, target)
        return refnode


class FortranCallField(FortranField):
    is_grouped = True

    def __init__(self, name, names=(), label=None, rolename=None):
        Field.__init__(self, name, names, label, True, rolename)

    def make_field(self, types, domain, items, **kwargs):
        fieldname = nodes.field_name('', self.label)
        par = nodes.paragraph()
        for i, item in enumerate(items):
            if i:
                par += nodes.Text(' ')
            par += item[1]

        fieldbody = nodes.field_body('', par)
        return nodes.field('', fieldname, fieldbody)


class FortranCompleteField(FortranField, GroupedField):
    """
    A doc field that is grouped and has type information for the arguments.  It
    always has an argument.  The argument can be linked using the given
    *rolename*, the type using the given *typerolename*.

    Two uses are possible: either parameter and type description are given
    separately, using a field from *names* and one from *typenames*,
    respectively, or both are given using a field from *names*, see the example.

    Example::

       :param foo: description of parameter foo
       :type foo:  SomeClass

       -- or --

       :param SomeClass foo: description of parameter foo
    """
    is_typed = 2

    def __init__(self, name, names=(), typenames=(), label=None, rolename=None, typerolename=None, shapenames=None, attrnames=None, prefix=None, strong=True, can_collapse=False):
        GroupedField.__init__(self, name, names, label, rolename, can_collapse)
        self.typenames = typenames
        self.typerolename = typerolename
        self.shapenames = shapenames
        self.attrnames = attrnames
        self.prefix = prefix
        if strong:
            self.namefmt = nodes.strong
        else:
            self.namefmt = addnodes.desc_name

    def make_field(self, types, domain, items, shapes=None, attrs=None, modname=None, typename=None):

        def handle_item(fieldarg, content):
            par = nodes.paragraph()
            if self.prefix:
                par += self.namefmt(self.prefix, self.prefix)
            par += self.make_xref(self.rolename, domain, fieldarg, self.namefmt, modname=modname, typename=typename)
            fieldtype = types.pop(fieldarg, None)
            fieldshape = shapes and shapes.pop(fieldarg, None)
            fieldattrs = attrs and attrs.pop(fieldarg, None)
            if fieldshape:
                shape = parse_shape(fieldshape[0].astext())
                add_shape(par, shape, modname=modname)
            if fieldtype or fieldattrs:
                par += nodes.emphasis(' [', ' [')
            if fieldtype:
                if len(fieldtype) == 1 and isinstance(fieldtype[0], nodes.Text):
                    thistypename = fieldtype[0].astext()
                    par += self.make_xref(self.typerolename, domain, thistypename, modname=modname, typename=typename)
                else:
                    par += fieldtype
            if fieldattrs:
                if fieldtype:
                    par += nodes.emphasis(',', ',')
                par += fieldattrs
            if fieldtype or fieldattrs:
                par += nodes.emphasis(']', ']')
            if content:
                par += nodes.Text(' :: ')
                par += content
            return par

        if len(items) == 1 and self.can_collapse:
            fieldarg, content = items[0]
            bodynode = handle_item(fieldarg, content)
        else:
            bodynode = self.list_type()
            for fieldarg, content in items:
                bodynode += nodes.list_item('', handle_item(fieldarg, content))

        label = self.label or ''
        fieldname = nodes.field_name('', label)
        fieldbody = nodes.field_body('', bodynode)
        return nodes.field('', fieldname, fieldbody)


class FortranDocFieldTransformer(DocFieldTransformer):
    """
    Transforms field lists in "doc field" syntax into better-looking
    equivalents, using the field type definitions given on a domain.
    """

    def __init__(self, directive, modname=None, typename=None):
        self.domain = directive.domain
        if '_doc_field_type_map' not in directive.__class__.__dict__:
            directive.__class__._doc_field_type_map = self.preprocess_fieldtypes(directive.__class__.doc_field_types)
        self.typemap = directive._doc_field_type_map
        self.modname = modname
        self.typename = typename

    def preprocess_fieldtypes(self, types):
        typemap = {}
        for fieldtype in types:
            for name in fieldtype.names:
                typemap[name] = (
                 fieldtype, False)

            if fieldtype.is_typed:
                for name in fieldtype.typenames:
                    typemap[name] = (
                     fieldtype, 'types')

                for name in fieldtype.shapenames:
                    typemap[name] = (
                     fieldtype, 'shapes')

                for name in fieldtype.attrnames:
                    typemap[name] = (
                     fieldtype, 'attrs')

        return typemap

    def scan_fieldarg(self, fieldname):
        """Extract type, name, shape and attributes from a field name.
        
        :Some possible syntaxes:
        
            - ``p name``
            - ``p type name(shape) [attr1,attr2]``
            - ``p type name``
            - ``p name [attr1, attr2]``
            
        :Returns: ``name, shape, type, list of attributes``.
            if no shape is specified, it is set to ``None``,
        """
        m = re_fieldname_match(fieldname.strip())
        if not m:
            raise ValueError('Wrong field (%s). It must have at least one parameter name and one argument' % fieldname)
        ftype, name, shape, attrs = m.groups()
        attrs = attrs and attrs[1:-1]
        return (
         name, shape, ftype, attrs)

    def transform(self, node):
        """Transform a single field list *node*."""
        typemap = self.typemap
        fmodname = self.modname
        ftypename = self.typename
        entries = []
        groupindices = {}
        types = {}
        shapes = {}
        attrs = {}
        for field in node:
            fieldname, fieldbody = field
            try:
                fieldtype, fieldarg = fieldname.astext().split(None, 1)
            except ValueError:
                fieldtype, fieldarg = fieldname.astext(), ''

            typedesc, is_typefield = typemap.get(fieldtype, (None, None))
            if typedesc is None:
                new_fieldname = fieldtype.capitalize() + ' ' + fieldarg
                fieldname[0] = nodes.Text(new_fieldname)
                entries.append(field)
                continue
            typename = typedesc.name
            if _is_single_paragraph(fieldbody):
                content = fieldbody.children[0].children
            else:
                content = fieldbody.children
            if is_typefield:
                content = filter(lambda n: isinstance(n, nodes.Inline) or isinstance(n, nodes.Text), content)
                if content:
                    eval(is_typefield).setdefault(typename, {})[fieldarg] = content
                continue
            if typedesc.is_typed == 2:
                argname, argshape, argtype, argattrs = self.scan_fieldarg(fieldarg)
                if argtype:
                    types.setdefault(typename, {})[argname] = [nodes.Text(argtype)]
                if argshape:
                    shapes.setdefault(typename, {})[argname] = [nodes.Text(argshape)]
                if argattrs:
                    attrs.setdefault(typename, {})[argname] = [nodes.emphasis(argattrs, argattrs)]
                fieldarg = argname
            elif typedesc.is_typed:
                try:
                    argtype, argname = fieldarg.split(None, 1)
                except ValueError:
                    pass
                else:
                    types.setdefault(typename, {})[argname] = [nodes.Text(argtype)]
                    fieldarg = argname

            if typedesc.is_grouped:
                if typename in groupindices:
                    group = entries[groupindices[typename]]
                else:
                    groupindices[typename] = len(entries)
                    group = [typedesc, []]
                    entries.append(group)
                group[1].append(typedesc.make_entry(fieldarg, content))
            else:
                entries.append([typedesc,
                 typedesc.make_entry(fieldarg, content)])

        new_list = nodes.field_list()
        for entry in entries:
            if isinstance(entry, nodes.field):
                new_list += entry
            else:
                fieldtype, content = entry
                fieldtypes = types.get(fieldtype.name, {})
                fieldshapes = shapes.get(fieldtype.name, {})
                fieldattrs = attrs.get(fieldtype.name, {})
                new_list += fieldtype.make_field(fieldtypes, self.domain, content, shapes=fieldshapes, attrs=fieldattrs, modname=fmodname, typename=ftypename)

        node.replace_self(new_list)
        return


f_sep = '/'
f_sig_re = re.compile('^ (\\w+(?:[^%%%(f_sep)s]%(f_sep)s\\w+))? \\s*          # type\n          (\\b(?:subroutine|function))?  \\s*             # objtype\n          (\\b\\w+%(f_sep)s)?              # module name\n          (\\b\\w+%%)?              # type name\n          (\\b\\w+)  \\s*             # thing name\n          (?: \\((.*)\\))?           # optional: arguments\n           $                   # and nothing more\n          ' % dict(f_sep=f_sep), re.VERBOSE + re.I)
wsplit_re = re.compile('(\\W+)')
f_type_re = re.compile('^([\\w]+).*$')
f_paramlist_re = re.compile('([\\[\\],])')

def _pseudo_parse_arglist(signode, arglist):
    """"Parse" a list of arguments separated by commas.

    Arguments can have "optional" annotations given by enclosing them in
    brackets.  Currently, this will split at any comma, even if it's inside a
    string literal (e.g. default argument value).
    """
    paramlist = addnodes.desc_parameterlist()
    stack = [paramlist]
    try:
        for argument in arglist.split(','):
            argument = argument.strip()
            ends_open = ends_close = 0
            while argument.startswith('['):
                stack.append(addnodes.desc_optional())
                stack[(-2)] += stack[(-1)]
                argument = argument[1:].strip()

            while argument.startswith(']'):
                stack.pop()
                argument = argument[1:].strip()

            while argument.endswith(']'):
                ends_close += 1
                argument = argument[:-1].strip()

            while argument.endswith('['):
                ends_open += 1
                argument = argument[:-1].strip()

            if argument:
                stack[(-1)] += addnodes.desc_parameter(argument, argument)
            while ends_open:
                stack.append(addnodes.desc_optional())
                stack[(-2)] += stack[(-1)]
                ends_open -= 1

            while ends_close:
                stack.pop()
                ends_close -= 1

        if len(stack) != 1:
            raise IndexError
    except IndexError:
        signode += addnodes.desc_parameterlist()
        signode[(-1)] += addnodes.desc_parameter(arglist, arglist)
    else:
        signode += paramlist


class FortranObject(ObjectDescription):
    """
    Description of a general Fortran object.
    """
    option_spec = {'noindex': directives.flag, 
       'module': directives.unchanged, 
       'type': directives.unchanged, 
       'shape': parse_shape, 
       'attrs': directives.unchanged}
    doc_field_types = [
     FortranCompleteField('parameter', label=l_('Parameters'), names=('p', 'param', 'parameter',
                                                                 'a', 'arg', 'argument'), typerolename='type', typenames=('paramtype',
                                                                                                                          'type',
                                                                                                                          'ptype'), shapenames=('shape',
                                                                                                                                                'pshape'), attrnames=('attrs',
                                                                                                                                                                      'pattrs',
                                                                                                                                                                      'attr'), can_collapse=True),
     FortranCompleteField('optional', label=l_('Options'), names=('o', 'optional', 'opt',
                                                             'keyword', 'option'), typerolename='type', typenames=('optparamtype',
                                                                                                                   'otype'), shapenames=('oshape', ), attrnames=('oattrs',
                                                                                                                                                                 'oattr'), can_collapse=True),
     FortranCompleteField('typefield', label=l_('Type fields'), names=('f', 'field', 'typef',
                                                                  'typefield'), typerolename='type', typenames=('fieldtype',
                                                                                                                'ftype'), shapenames=('fshape', ), attrnames=('fattrs',
                                                                                                                                                              'fattr'), prefix='% ', strong=False, can_collapse=False),
     FortranCompleteField('return', label=l_('Return'), names=('r', 'return', 'returns'), typerolename='type', typenames=('returntype',
                                                                                                                     'rtype'), shapenames=('rshape', ), attrnames=('rattrs',
                                                                                                                                                                   'rattr'), can_collapse=True),
     FortranCallField('calledfrom', label=l_('Called from'), names=('calledfrom', 'from')),
     FortranCallField('callto', label=l_('Call to'), names=('callto', 'to'))]
    stopwords = set(('float', 'integer', 'character', 'double', 'long'))
    _parens = ''

    def get_signature_prefix(self, sig):
        """
        May return a prefix to put before the object name in the signature.
        """
        return ''

    def needs_arglist(self):
        """
        May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """
        Transform a Fortran signature into RST nodes.
        Returns (fully qualified name of the thing, classname if any).

        If inside a class, the current class name is handled intelligently:
        * it is stripped from the displayed name if present
        * it is added to the full name (return value) if not present
        """
        m = f_sig_re.match(sig)
        if m is None:
            raise ValueError
        ftype, objtype, modname, typename, name, arglist = m.groups()
        if not typename:
            typename = ''
        modname = modname and modname[:-1] or self.options.get('module', self.env.temp_data.get('f:module'))
        if typename:
            name = typename[:-1]
        attrs = self.options.get('attrs')
        shape = parse_shape(self.options.get('shape'))
        ftype = ftype or self.options.get('type')
        if self.objtype == 'typefield' and not typename:
            raise ValueError
        if self.objtype == 'program':
            fullname = name
        else:
            fullname = (modname or '_') + f_sep + name
        signode['module'] = modname
        signode['type'] = typename
        signode['fullname'] = fullname
        sig_prefix = self.get_signature_prefix(sig)
        if objtype or sig_prefix:
            objtype = objtype or sig_prefix
            signode += addnodes.desc_annotation(objtype + ' ', objtype + ' ')
        if self.env.config.add_module_names and modname and self.objtype != 'typefield':
            nodetext = modname + f_sep
            signode += addnodes.desc_addname(nodetext, nodetext)
        signode += addnodes.desc_name(name, name)
        if self.needs_arglist():
            if arglist:
                _pseudo_parse_arglist(signode, arglist)
            elif self.needs_arglist():
                signode += addnodes.desc_parameterlist()
        elif arglist and not shape:
            shape = arglist
        self.add_shape_and_attrs(signode, modname, ftype, shape, attrs)
        return (
         fullname, ftype)

    def add_shape_and_attrs(self, signode, modname, ftype, shape, attrs):
        if shape:
            add_shape(signode, shape, modname=modname)
        if ftype or attrs:
            signode += nodes.emphasis(' [', ' [')
        if ftype:
            refnode = addnodes.pending_xref('', refdomain='f', reftype='type', reftarget=ftype, modname=modname)
            refnode += nodes.emphasis(ftype, ftype)
            signode += refnode
        if attrs:
            if ftype:
                signode += nodes.emphasis(',', ',')
            for iatt, att in enumerate(re.split('\\s*,\\s*', attrs)):
                if iatt:
                    signode += nodes.emphasis(',', ',')
                if att.startswith('parameter'):
                    value = att.split('=')[1]
                    signode += nodes.emphasis('parameter=', 'parameter=')
                    convert_arithm(signode, value, modname=modname)
                else:
                    signode += nodes.emphasis(att, att)

        if ftype or attrs:
            signode += nodes.emphasis(']', ']')

    def add_target_and_index(self, name, sig, signode):
        modname = signode.get('module', self.env.temp_data.get('f:module'))
        fullname = 'f' + f_sep + name[0]
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['f']['objects']
            if fullname in objects:
                self.env.warn(self.env.docname, 'duplicate object description of %s, ' % fullname + 'other instance in ' + self.env.doc2path(objects[fullname][0]), self.lineno)
            objects[fullname] = (
             self.env.docname, self.objtype)
        indextext = self.get_index_text(modname, fullname)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
             fullname, fullname))

    def before_content(self):
        self.typename_set = False

    def after_content(self):
        if self.typename_set:
            self.env.temp_data['f:type'] = None
        return

    def get_index_text(self, modname, name):
        add_modules = self.env.config.add_module_names
        if name.startswith('f' + f_sep):
            name = name[2:]
        mn = modname or '_'
        sobj = ''
        if name.startswith(mn + f_sep):
            name = name[len(mn) + 1:]
        if self.objtype == 'type':
            sobj = _('fortran type')
        if self.objtype == 'typefield':
            sobj = _('fortran type field')
        elif self.objtype == 'variable':
            sobj = _('fortran variable')
        elif self.objtype == 'subroutine':
            sobj = _('fortran subroutine')
        elif self.objtype == 'function':
            sobj = _('fortran function')
        elif self.objtype == 'module':
            sobj = _('fortran module')
            modname = ''
        elif self.objtype == 'program':
            sobj = _('fortran program')
            modname = ''
        sinmodule = _(' in module %s') % modname if modname and add_modules else ''
        return '%s%s (%s%s)' % (name, self._parens, sobj, sinmodule)


class FortranSpecial():

    def get_signature_prefix(self, sig):
        """
        May return a prefix to put before the object name in the signature.
        """
        return self.objtype + ' '


class WithFortranDocFieldTransformer():

    def run(self):
        """Same as :meth:`sphinx.directives.ObjectDescription` 
        but using :class:`FortranDocFieldTransformer`"""
        if ':' in self.name:
            self.domain, self.objtype = self.name.split(':', 1)
        else:
            self.domain, self.objtype = '', self.name
        self.env = self.state.document.settings.env
        self.indexnode = addnodes.index(entries=[])
        node = addnodes.desc()
        node.document = self.state.document
        node['domain'] = self.domain
        node['objtype'] = node['desctype'] = self.objtype
        node['noindex'] = noindex = 'noindex' in self.options
        self.names = []
        signatures = self.get_signatures()
        for i, sig in enumerate(signatures):
            signode = addnodes.desc_signature(sig, '')
            signode['first'] = False
            node.append(signode)
            try:
                name = self.handle_signature(sig, signode)
            except ValueError:
                signode.clear()
                signode += addnodes.desc_name(sig, sig)
                continue

            if not noindex and name not in self.names:
                self.names.append(name)
                self.add_target_and_index(name, sig, signode)

        modname = signode.get('module')
        typename = signode.get('type')
        contentnode = addnodes.desc_content()
        node.append(contentnode)
        if self.names:
            self.env.temp_data['object'] = self.names[0]
        self.before_content()
        self.state.nested_parse(self.content, self.content_offset, contentnode)
        FortranDocFieldTransformer(self, modname=modname, typename=typename).transform_all(contentnode)
        self.env.temp_data['object'] = None
        self.after_content()
        return [self.indexnode, node]


class FortranType(FortranSpecial, WithFortranDocFieldTransformer, FortranObject):

    def before_content(self):
        FortranObject.before_content(self)
        if self.names:
            self.env.temp_data['f:type'] = self.names[0][0].split(f_sep)[(-1)]
            self.typename_set = True


class FortranTypeField(FortranObject):

    def before_content(self):
        FortranObject.before_content(self)
        lastname = self.names and self.names[(-1)][1]
        if lastname and not self.env.temp_data.get('f:type'):
            self.env.temp_data['f:type'] = lastname.split(f_sep)[(-1)]
            self.typename_set = True


class FortranProgram(FortranSpecial, WithFortranDocFieldTransformer, FortranObject):
    pass


class FortranWithSig(FortranSpecial, WithFortranDocFieldTransformer, FortranObject):
    """
    Description of a function of subroutine
    """
    _parens = '()'

    def needs_arglist(self):
        return True

    def get_signature_prefix(self, sig):
        """
        May return a prefix to put before the object name in the signature.
        """
        return self.objtype + ' '


class FortranField(Directive):
    """
    Directive to describe a change/addition/deprecation in a specific version.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'type': directives.unchanged, 
       'shape': parse_shape, 
       'attrs': directives.unchanged}

    def run(self):
        from docutils import nodes
        node = nodes.paragraph()
        node += addnodes.desc_name(self.arguments[0], self.arguments[0])
        shape = self.options.get('shape')
        if shape:
            add_shape(node, shape)
        type = self.options.get('type')
        attrs = self.options.get('attrs')
        if type or attrs:
            node += nodes.Text(' :: ', ' :: ')
            if type:
                node += nodes.emphasis('', type)
            if attr:
                node += nodes.literal('', '[' + attr + ']')
        if self.content:
            node += nodes.Text(': ', ': ')
            argnodes, msgs = self.state.inline_text((' ').join(self.content), self.lineno)
            node += argnodes
            node += msgs
        ret = [
         node]
        return ret


class FortranModule(Directive):
    """
    Directive to mark description of a new module.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'platform': lambda x: x, 
       'synopsis': lambda x: x, 
       'noindex': directives.flag, 
       'deprecated': directives.flag}

    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        noindex = 'noindex' in self.options
        env.temp_data['f:module'] = modname
        env.domaindata['f']['modules'][modname] = (
         env.docname, self.options.get('synopsis', ''),
         self.options.get('platform', ''), 'deprecated' in self.options)
        env.domaindata['f']['objects']['f' + f_sep + modname] = (env.docname, 'module')
        targetnode = nodes.target('', '', ids=['f' + f_sep + modname], ismod=True)
        self.state.document.note_explicit_target(targetnode)
        ret = [targetnode]
        if 'platform' in self.options:
            platform = self.options['platform']
            node = nodes.paragraph()
            node += nodes.emphasis('', _('Platforms: '))
            node += nodes.Text(platform, platform)
            ret.append(node)
        if not noindex:
            indextext = _('%s (module)') % modname
            inode = addnodes.index(entries=[
             ('single', indextext,
              'f' + f_sep + modname, modname)])
            ret.append(inode)
        return ret


class FortranCurrentModule(Directive):
    """
    This directive is just to tell Sphinx that we're documenting
    stuff in module foo, but links to module foo won't lead here.
    """
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {}

    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments and (self.arguments[0] or self.arguments[0].strip()) or None
        if modname:
            env.temp_data['f:module'] = None
        else:
            env.temp_data['f:module'] = modname
        return []


class FortranXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['f:module'] = env.temp_data.get('f:module')
        refnode['f:type'] = env.temp_data.get('f:type')
        if not has_explicit_title:
            title = title.lstrip('.')
            target = target.lstrip('~')
            if title[0:1] == '~':
                title = title[1:].split(f_sep)[(-1)]
        if target.startswith(f_sep):
            target = target[1:]
            refnode['refspecific'] = True
        return (
         title, target)


class FortranModuleIndex(Index):
    """
    Index subclass to provide the Fortran module index.
    """
    name = 'modindex'
    localname = l_('Fortran Module Index')
    shortname = l_('fortran modules')

    def generate(self, docnames=None):
        content = {}
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        modules = sorted(self.domain.data['modules'].iteritems(), key=lambda x: x[0].lower())
        prev_modname = ''
        num_toplevels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue
            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ''

            if not modname:
                modname, stripped = stripped, ''
            entries = content.setdefault(modname[0].lower(), [])
            package = modname.split(f_sep)[0]
            if package != modname:
                if prev_modname == package:
                    entries[(-1)][1] = 1
                elif not prev_modname.startswith(package):
                    entries.append([stripped + package, 1, '', '', '', '', ''])
                subtype = 2
            else:
                num_toplevels += 1
                subtype = 0
            qualifier = deprecated and _('Deprecated') or ''
            entries.append([stripped + modname, subtype, docname,
             'f' + f_sep + stripped + modname, platforms,
             qualifier, synopsis or ''])
            prev_modname = modname

        collapse = len(modules) - num_toplevels < num_toplevels
        content = sorted(content.iteritems())
        return (
         content, collapse)


class FortranDomain(Domain):
    """Fortran language domain."""
    name = 'f'
    label = 'Fortran'
    object_types = {'program': ObjType(l_('program'), 'prog'), 
       'type': ObjType(l_('type'), 'type'), 
       'variable': ObjType(l_('variable'), 'var'), 
       'function': ObjType(l_('function'), 'func'), 
       'subroutine': ObjType(l_('subroutine'), 'func', 'subr'), 
       'module': ObjType(l_('module'), 'mod')}
    directives = {'program': FortranProgram, 
       'type': FortranType, 
       'variable': FortranObject, 
       'function': FortranWithSig, 
       'subroutine': FortranWithSig, 
       'module': FortranModule, 
       'currentmodule': FortranCurrentModule}
    roles = {'prog': FortranXRefRole(), 
       'type': FortranXRefRole(), 
       'var': FortranXRefRole(), 
       'func': FortranXRefRole(fix_parens=True), 
       'subr': FortranXRefRole(fix_parens=True), 
       'mod': FortranXRefRole()}
    initial_data = {'objects': {}, 'modules': {}}
    indices = [
     FortranModuleIndex]

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]

        for modname, (fn, _, _, _) in self.data['modules'].items():
            if fn == docname:
                del self.data['modules'][modname]

    def find_obj(self, env, modname, name, role, searchorder=0):
        """
        Find a Fortran object for "name", perhaps using the given module and/or
        typename.
        
        :Params:
        
            - **searchorder**, optional: Start using relative search
        """
        if name.endswith('()'):
            name = name[:-2]
        if not name:
            return (None, None)
        else:
            if f_sep in name:
                modname, name = name.split(f_sep)
            if '%' in name:
                name, tmp = name.split('%')
            objects = self.data['objects']
            newname = None
            matches = []
            objtypes = self.objtypes_for_role(role)
            if searchorder == 1:
                if role in ('mod', 'prog'):
                    if 'f' + f_sep + name not in objects:
                        return []
                    newname = 'f' + f_sep + name
                elif modname and 'f' + f_sep + modname + f_sep + name in objects and objects[('f' + f_sep + modname + f_sep + name)][1] in objtypes:
                    newname = 'f' + f_sep + modname + f_sep + name
                elif 'f' + f_sep + '_' + f_sep + name in objects and objects[('f' + f_sep + '_' + f_sep + name)][1] in objtypes:
                    newname = 'f' + f_sep + '_' + f_sep + name
                elif 'f' + f_sep + name in objects and objects[('f' + f_sep + name)][1] in objtypes:
                    newname = 'f' + f_sep + name
                elif name in objects and objects[name][1] in objtypes:
                    newname = name
            elif 'f' + f_sep + name in objects:
                newname = 'f' + f_sep + name
            else:
                if role in ('mod', 'prog'):
                    return []
                if 'f' + f_sep + '_' + f_sep + name in objects:
                    newname = 'f' + f_sep + '_' + f_sep + name
                elif modname and 'f' + f_sep + modname + f_sep + name in objects:
                    newname = 'f' + f_sep + modname + f_sep + name
            if newname is None:
                matches = [ (oname, objects[oname]) for oname in objects if oname.endswith(f_sep + name) and objects[oname][1] in objtypes
                          ]
            else:
                matches.append((newname, objects[newname]))
            return matches

    def resolve_xref(self, env, fromdocname, builder, type, target, node, contnode):
        modname = node.get('f:module', node.get('modname'))
        typename = node.get('f:type', node.get('typename'))
        searchorder = node.hasattr('refspecific') and 1 or 0
        matches = self.find_obj(env, modname, target, type, searchorder)
        if not matches:
            return
        else:
            if len(matches) > 1:
                env.warn(fromdocname, 'more than one target found for cross-reference %r: %s' % (
                 target,
                 (', ').join(match[0] for match in matches)), node.line)
            name, obj = matches[0]
            if obj[1] == 'module':
                docname, synopsis, platform, deprecated = self.data['modules'][name[1 + len(f_sep):]]
                assert docname == obj[0]
                title = name
                if synopsis:
                    title += ': ' + synopsis
                if deprecated:
                    title += _(' (deprecated)')
                return make_refnode(builder, fromdocname, docname, name, contnode, title)
            return make_refnode(builder, fromdocname, obj[0], name, contnode, name)
            return

    def get_objects(self):
        for modname, info in self.data['modules'].iteritems():
            yield (modname, modname, 'module', info[0], 'module-' + modname, 0)

        for refname, (docname, type) in self.data['objects'].iteritems():
            yield (
             refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(FortranDomain)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/processor/dependencies.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 5944 bytes
"""
The dependencies module determines which descriptions depend on which other
descriptions.
"""
from ..descriptions import *
from ..ctypedescs import *
from ..messages import *

def find_dependencies(data, opts):
    """Visit each description in `data` and figure out which other descriptions
it depends on, putting the results in desc.requirements. Also find errors in
ctypedecls or expressions attached to the description and transfer them to the
description."""
    struct_names = {}
    enum_names = {}
    typedef_names = {}
    ident_names = {}
    for name in opts.other_known_names:
        typedef_names[name] = None
        ident_names[name] = None
        if not name.startswith('struct_'):
            if name.startswith('enum_'):
                variety = name.split('_')[0]
                tag = '_'.join(name.split('_')[1:])
                struct_names[(variety, tag)] = None
            if name.startswith('enum_'):
                enum_names[name] = None

    def depend(desc, nametable, name):
        """Try to add `name` as a requirement for `desc`, looking `name` up in
`nametable`. Returns True if found."""
        if name in nametable:
            requirement = nametable[name]
            if requirement:
                desc.add_requirements([requirement])
            return True
        return False

    def co_depend(desc, nametable, name):
        """
        Try to add `name` as a requirement for `desc`, looking `name` up in
        `nametable`.  Also try to add desc as a requirement for `name`.

        Returns Description of `name` if found.
        """
        requirement = nametable.get(name, None)
        if requirement is None:
            return
        desc.add_requirements([requirement])
        requirement.add_requirements([desc])
        return requirement

    def find_dependencies_for(desc, kind):
        if kind == 'constant':
            roots = [
             desc.value]
        else:
            if kind == 'struct':
                roots = []
            else:
                if kind == 'struct-body':
                    roots = [
                     desc.ctype]
                else:
                    if kind == 'enum':
                        roots = []
                    else:
                        if kind == 'typedef':
                            roots = [
                             desc.ctype]
                        else:
                            if kind == 'function':
                                roots = desc.argtypes + [desc.restype]
                            else:
                                if kind == 'variable':
                                    roots = [
                                     desc.ctype]
                                else:
                                    if kind == 'macro':
                                        if desc.expr:
                                            roots = [
                                             desc.expr]
                                        else:
                                            roots = []
                                    elif kind == 'undef':
                                        roots = [
                                         desc.macro]
        cstructs, cenums, ctypedefs, errors, identifiers = ([], [], [], [], [])
        for root in roots:
            s, e, t, errs, i = visit_type_and_collect_info(root)
            cstructs.extend(s)
            cenums.extend(e)
            ctypedefs.extend(t)
            errors.extend(errs)
            identifiers.extend(i)

        unresolvables = []
        for cstruct in cstructs:
            if kind == 'struct' and desc.variety == cstruct.variety:
                if desc.tag == cstruct.tag:
                    continue
                depend(desc, struct_names, (cstruct.variety, cstruct.tag)) or unresolvables.append('%s "%s"' % (cstruct.variety, cstruct.tag))

        for cenum in cenums:
            if kind == 'enum':
                if desc.tag == cenum.tag:
                    continue
                depend(desc, enum_names, cenum.tag) or unresolvables.append('enum "%s"' % cenum.tag)

        for ctypedef in ctypedefs:
            if not depend(desc, typedef_names, ctypedef):
                unresolvables.append('typedef "%s"' % ctypedef)

        for ident in identifiers:
            if isinstance(desc, MacroDescription) and desc.params and ident in desc.params:
                continue
            elif opts.include_undefs and isinstance(desc, UndefDescription):
                macro_desc = None
                if ident == desc.macro.name:
                    macro_desc = co_depend(desc, ident_names, ident)
                macro_desc is None or isinstance(macro_desc, MacroDescription) or unresolvables.append('identifier "%s"' % ident)
            else:
                depend(desc, ident_names, ident) or unresolvables.append('identifier "%s"' % ident)

        for u in unresolvables:
            errors.append(('%s depends on an unknown %s.' % (desc.casual_name(), u), None))

        for err, cls in errors:
            err += ' %s will not be output' % desc.casual_name()
            desc.error(err, cls=cls)

    def add_to_lookup_table(desc, kind):
        if kind == 'struct':
            if (
             desc.variety, desc.tag) not in struct_names:
                struct_names[(desc.variety, desc.tag)] = desc
        else:
            if kind == 'enum':
                if desc.tag not in enum_names:
                    enum_names[desc.tag] = desc
            if kind == 'typedef':
                if desc.name not in typedef_names:
                    typedef_names[desc.name] = desc
            if kind in ('function', 'constant', 'variable', 'macro') and desc.name not in ident_names:
                ident_names[desc.name] = desc

    for kind, desc in data.output_order:
        add_to_lookup_table(desc, kind)
        if kind != 'macro':
            find_dependencies_for(desc, kind)

    for kind, desc in data.output_order:
        if kind == 'macro':
            find_dependencies_for(desc, kind)
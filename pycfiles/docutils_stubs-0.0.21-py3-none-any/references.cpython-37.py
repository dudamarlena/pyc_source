# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/transforms/references.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 36576 bytes
"""
Transforms for resolving references.
"""
__docformat__ = 'reStructuredText'
import sys, re
from docutils import nodes, utils
from docutils.transforms import TransformError, Transform

class PropagateTargets(Transform):
    __doc__ = '\n    Propagate empty internal targets to the next element.\n\n    Given the following nodes::\n\n        <target ids="internal1" names="internal1">\n        <target anonymous="1" ids="id1">\n        <target ids="internal2" names="internal2">\n        <paragraph>\n            This is a test.\n\n    PropagateTargets propagates the ids and names of the internal\n    targets preceding the paragraph to the paragraph itself::\n\n        <target refid="internal1">\n        <target anonymous="1" refid="id1">\n        <target refid="internal2">\n        <paragraph ids="internal2 id1 internal1" names="internal2 internal1">\n            This is a test.\n    '
    default_priority = 260

    def apply(self):
        for target in self.document.traverse(nodes.target):
            if isinstance(target.parent, nodes.TextElement) or target.hasattr('refid') or target.hasattr('refuri') or target.hasattr('refname'):
                continue
            assert len(target) == 0, 'error: block-level target has children'
            next_node = target.next_node(ascend=True)
            if next_node is not None and not isinstance(next_node, nodes.Invisible):
                if isinstance(next_node, nodes.Targetable):
                    if isinstance(next_node, nodes.target):
                        next_node['ids'].extend(target['ids'])
                        next_node['names'].extend(target['names'])
                        if not hasattr(next_node, 'expect_referenced_by_name'):
                            next_node.expect_referenced_by_name = {}
                    if not hasattr(next_node, 'expect_referenced_by_id'):
                        next_node.expect_referenced_by_id = {}
                for id in target['ids']:
                    self.document.ids[id] = next_node
                    next_node.expect_referenced_by_id[id] = target

                for name in target['names']:
                    next_node.expect_referenced_by_name[name] = target

                next_node.expect_referenced_by_name.update(getattr(target, 'expect_referenced_by_name', {}))
                next_node.expect_referenced_by_id.update(getattr(target, 'expect_referenced_by_id', {}))
                target['refid'] = target['ids'][0]
                target['ids'] = []
                target['names'] = []
                self.document.note_refid(target)


class AnonymousHyperlinks(Transform):
    __doc__ = '\n    Link anonymous references to targets.  Given::\n\n        <paragraph>\n            <reference anonymous="1">\n                internal\n            <reference anonymous="1">\n                external\n        <target anonymous="1" ids="id1">\n        <target anonymous="1" ids="id2" refuri="http://external">\n\n    Corresponding references are linked via "refid" or resolved via "refuri"::\n\n        <paragraph>\n            <reference anonymous="1" refid="id1">\n                text\n            <reference anonymous="1" refuri="http://external">\n                external\n        <target anonymous="1" ids="id1">\n        <target anonymous="1" ids="id2" refuri="http://external">\n    '
    default_priority = 440

    def apply(self):
        anonymous_refs = []
        anonymous_targets = []
        for node in self.document.traverse(nodes.reference):
            if node.get('anonymous'):
                anonymous_refs.append(node)

        for node in self.document.traverse(nodes.target):
            if node.get('anonymous'):
                anonymous_targets.append(node)

        if len(anonymous_refs) != len(anonymous_targets):
            msg = self.document.reporter.error('Anonymous hyperlink mismatch: %s references but %s targets.\nSee "backrefs" attribute for IDs.' % (
             len(anonymous_refs), len(anonymous_targets)))
            msgid = self.document.set_id(msg)
            for ref in anonymous_refs:
                prb = nodes.problematic((ref.rawsource),
                  (ref.rawsource), refid=msgid)
                prbid = self.document.set_id(prb)
                msg.add_backref(prbid)
                ref.replace_self(prb)

            return
        for ref, target in zip(anonymous_refs, anonymous_targets):
            target.referenced = 1
            while True:
                if target.hasattr('refuri'):
                    ref['refuri'] = target['refuri']
                    ref.resolved = 1
                    break
                else:
                    if not target['ids']:
                        target = self.document.ids[target['refid']]
                        continue
                    ref['refid'] = target['ids'][0]
                    self.document.note_refid(ref)
                    break


class IndirectHyperlinks(Transform):
    __doc__ = '\n    a) Indirect external references::\n\n           <paragraph>\n               <reference refname="indirect external">\n                   indirect external\n           <target id="id1" name="direct external"\n               refuri="http://indirect">\n           <target id="id2" name="indirect external"\n               refname="direct external">\n\n       The "refuri" attribute is migrated back to all indirect targets\n       from the final direct target (i.e. a target not referring to\n       another indirect target)::\n\n           <paragraph>\n               <reference refname="indirect external">\n                   indirect external\n           <target id="id1" name="direct external"\n               refuri="http://indirect">\n           <target id="id2" name="indirect external"\n               refuri="http://indirect">\n\n       Once the attribute is migrated, the preexisting "refname" attribute\n       is dropped.\n\n    b) Indirect internal references::\n\n           <target id="id1" name="final target">\n           <paragraph>\n               <reference refname="indirect internal">\n                   indirect internal\n           <target id="id2" name="indirect internal 2"\n               refname="final target">\n           <target id="id3" name="indirect internal"\n               refname="indirect internal 2">\n\n       Targets which indirectly refer to an internal target become one-hop\n       indirect (their "refid" attributes are directly set to the internal\n       target\'s "id"). References which indirectly refer to an internal\n       target become direct internal references::\n\n           <target id="id1" name="final target">\n           <paragraph>\n               <reference refid="id1">\n                   indirect internal\n           <target id="id2" name="indirect internal 2" refid="id1">\n           <target id="id3" name="indirect internal" refid="id1">\n    '
    default_priority = 460

    def apply(self):
        for target in self.document.indirect_targets:
            if not target.resolved:
                self.resolve_indirect_target(target)
            self.resolve_indirect_references(target)

    def resolve_indirect_target(self, target):
        refname = target.get('refname')
        if refname is None:
            reftarget_id = target['refid']
        else:
            reftarget_id = self.document.nameids.get(refname)
            if not reftarget_id:
                for resolver_function in self.document.transformer.unknown_reference_resolvers:
                    if resolver_function(target):
                        break
                else:
                    self.nonexistent_indirect_target(target)

                return
            else:
                reftarget = self.document.ids[reftarget_id]
                reftarget.note_referenced_by(id=reftarget_id)
                if isinstance(reftarget, nodes.target):
                    if not reftarget.resolved:
                        if reftarget.hasattr('refname'):
                            if hasattr(target, 'multiply_indirect'):
                                self.circular_indirect_reference(target)
                                return
                            target.multiply_indirect = 1
                            self.resolve_indirect_target(reftarget)
                            del target.multiply_indirect
                elif reftarget.hasattr('refuri'):
                    target['refuri'] = reftarget['refuri']
                    if 'refid' in target:
                        del target['refid']
                else:
                    if reftarget.hasattr('refid'):
                        target['refid'] = reftarget['refid']
                        self.document.note_refid(target)
                    else:
                        if reftarget['ids']:
                            target['refid'] = reftarget_id
                            self.document.note_refid(target)
                        else:
                            self.nonexistent_indirect_target(target)
                            return
            if refname is not None:
                del target['refname']
            target.resolved = 1

    def nonexistent_indirect_target(self, target):
        if target['refname'] in self.document.nameids:
            self.indirect_target_error(target, 'which is a duplicate, and cannot be used as a unique reference')
        else:
            self.indirect_target_error(target, 'which does not exist')

    def circular_indirect_reference(self, target):
        self.indirect_target_error(target, 'forming a circular reference')

    def indirect_target_error(self, target, explanation):
        naming = ''
        reflist = []
        if target['names']:
            naming = '"%s" ' % target['names'][0]
        for name in target['names']:
            reflist.extend(self.document.refnames.get(name, []))

        for id in target['ids']:
            reflist.extend(self.document.refids.get(id, []))

        if target['ids']:
            naming += '(id="%s")' % target['ids'][0]
        msg = self.document.reporter.error(('Indirect hyperlink target %s refers to target "%s", %s.' % (
         naming, target['refname'], explanation)),
          base_node=target)
        msgid = self.document.set_id(msg)
        for ref in utils.uniq(reflist):
            prb = nodes.problematic((ref.rawsource),
              (ref.rawsource), refid=msgid)
            prbid = self.document.set_id(prb)
            msg.add_backref(prbid)
            ref.replace_self(prb)

        target.resolved = 1

    def resolve_indirect_references(self, target):
        if target.hasattr('refid'):
            attname = 'refid'
            call_method = self.document.note_refid
        else:
            if target.hasattr('refuri'):
                attname = 'refuri'
                call_method = None
            else:
                return
        attval = target[attname]
        for name in target['names']:
            reflist = self.document.refnames.get(name, [])
            if reflist:
                target.note_referenced_by(name=name)
            for ref in reflist:
                if ref.resolved:
                    continue
                del ref['refname']
                ref[attname] = attval
                if call_method:
                    call_method(ref)
                ref.resolved = 1
                if isinstance(ref, nodes.target):
                    self.resolve_indirect_references(ref)

        for id in target['ids']:
            reflist = self.document.refids.get(id, [])
            if reflist:
                target.note_referenced_by(id=id)
            for ref in reflist:
                if ref.resolved:
                    continue
                del ref['refid']
                ref[attname] = attval
                if call_method:
                    call_method(ref)
                ref.resolved = 1
                if isinstance(ref, nodes.target):
                    self.resolve_indirect_references(ref)


class ExternalTargets(Transform):
    __doc__ = '\n    Given::\n\n        <paragraph>\n            <reference refname="direct external">\n                direct external\n        <target id="id1" name="direct external" refuri="http://direct">\n\n    The "refname" attribute is replaced by the direct "refuri" attribute::\n\n        <paragraph>\n            <reference refuri="http://direct">\n                direct external\n        <target id="id1" name="direct external" refuri="http://direct">\n    '
    default_priority = 640

    def apply(self):
        for target in self.document.traverse(nodes.target):
            if target.hasattr('refuri'):
                refuri = target['refuri']
                for name in target['names']:
                    reflist = self.document.refnames.get(name, [])
                    if reflist:
                        target.note_referenced_by(name=name)
                    for ref in reflist:
                        if ref.resolved:
                            continue
                        del ref['refname']
                        ref['refuri'] = refuri
                        ref.resolved = 1


class InternalTargets(Transform):
    default_priority = 660

    def apply(self):
        for target in self.document.traverse(nodes.target):
            if not target.hasattr('refuri'):
                target.hasattr('refid') or self.resolve_reference_ids(target)

    def resolve_reference_ids(self, target):
        """
        Given::

            <paragraph>
                <reference refname="direct internal">
                    direct internal
            <target id="id1" name="direct internal">

        The "refname" attribute is replaced by "refid" linking to the target's
        "id"::

            <paragraph>
                <reference refid="id1">
                    direct internal
            <target id="id1" name="direct internal">
        """
        for name in target['names']:
            refid = self.document.nameids.get(name)
            reflist = self.document.refnames.get(name, [])
            if reflist:
                target.note_referenced_by(name=name)
            for ref in reflist:
                if ref.resolved:
                    continue
                if refid:
                    del ref['refname']
                    ref['refid'] = refid
                ref.resolved = 1


class Footnotes(Transform):
    __doc__ = '\n    Assign numbers to autonumbered footnotes, and resolve links to footnotes,\n    citations, and their references.\n\n    Given the following ``document`` as input::\n\n        <document>\n            <paragraph>\n                A labeled autonumbered footnote referece:\n                <footnote_reference auto="1" id="id1" refname="footnote">\n            <paragraph>\n                An unlabeled autonumbered footnote referece:\n                <footnote_reference auto="1" id="id2">\n            <footnote auto="1" id="id3">\n                <paragraph>\n                    Unlabeled autonumbered footnote.\n            <footnote auto="1" id="footnote" name="footnote">\n                <paragraph>\n                    Labeled autonumbered footnote.\n\n    Auto-numbered footnotes have attribute ``auto="1"`` and no label.\n    Auto-numbered footnote_references have no reference text (they\'re\n    empty elements). When resolving the numbering, a ``label`` element\n    is added to the beginning of the ``footnote``, and reference text\n    to the ``footnote_reference``.\n\n    The transformed result will be::\n\n        <document>\n            <paragraph>\n                A labeled autonumbered footnote referece:\n                <footnote_reference auto="1" id="id1" refid="footnote">\n                    2\n            <paragraph>\n                An unlabeled autonumbered footnote referece:\n                <footnote_reference auto="1" id="id2" refid="id3">\n                    1\n            <footnote auto="1" id="id3" backrefs="id2">\n                <label>\n                    1\n                <paragraph>\n                    Unlabeled autonumbered footnote.\n            <footnote auto="1" id="footnote" name="footnote" backrefs="id1">\n                <label>\n                    2\n                <paragraph>\n                    Labeled autonumbered footnote.\n\n    Note that the footnotes are not in the same order as the references.\n\n    The labels and reference text are added to the auto-numbered ``footnote``\n    and ``footnote_reference`` elements.  Footnote elements are backlinked to\n    their references via "refids" attributes.  References are assigned "id"\n    and "refid" attributes.\n\n    After adding labels and reference text, the "auto" attributes can be\n    ignored.\n    '
    default_priority = 620
    autofootnote_labels = None
    symbols = [
     '*',
     '†',
     '‡',
     '§',
     '¶',
     '#',
     '♠',
     '♥',
     '♦',
     '♣']

    def apply(self):
        self.autofootnote_labels = []
        startnum = self.document.autofootnote_start
        self.document.autofootnote_start = self.number_footnotes(startnum)
        self.number_footnote_references(startnum)
        self.symbolize_footnotes()
        self.resolve_footnotes_and_citations()

    def number_footnotes(self, startnum):
        """
        Assign numbers to autonumbered footnotes.

        For labeled autonumbered footnotes, copy the number over to
        corresponding footnote references.
        """
        for footnote in self.document.autofootnotes:
            while 1:
                label = str(startnum)
                startnum += 1
                if label not in self.document.nameids:
                    break

            footnote.insert(0, nodes.label('', label))
            for name in footnote['names']:
                for ref in self.document.footnote_refs.get(name, []):
                    ref += nodes.Text(label)
                    ref.delattr('refname')
                    assert len(footnote['ids']) == len(ref['ids']) == 1
                    ref['refid'] = footnote['ids'][0]
                    footnote.add_backref(ref['ids'][0])
                    self.document.note_refid(ref)
                    ref.resolved = 1

            if not footnote['names']:
                footnote['dupnames'] or footnote['names'].append(label)
                self.document.note_explicit_target(footnote, footnote)
                self.autofootnote_labels.append(label)

        return startnum

    def number_footnote_references(self, startnum):
        """Assign numbers to autonumbered footnote references."""
        i = 0
        for ref in self.document.autofootnote_refs:
            if not ref.resolved:
                if ref.hasattr('refid'):
                    continue
                try:
                    label = self.autofootnote_labels[i]
                except IndexError:
                    msg = self.document.reporter.error(('Too many autonumbered footnote references: only %s corresponding footnotes available.' % len(self.autofootnote_labels)),
                      base_node=ref)
                    msgid = self.document.set_id(msg)
                    for ref in self.document.autofootnote_refs[i:]:
                        if not ref.resolved:
                            if ref.hasattr('refname'):
                                continue
                            prb = nodes.problematic((ref.rawsource),
                              (ref.rawsource), refid=msgid)
                            prbid = self.document.set_id(prb)
                            msg.add_backref(prbid)
                            ref.replace_self(prb)

                    break

                ref += nodes.Text(label)
                id = self.document.nameids[label]
                footnote = self.document.ids[id]
                ref['refid'] = id
                self.document.note_refid(ref)
                assert len(ref['ids']) == 1
                footnote.add_backref(ref['ids'][0])
                ref.resolved = 1
                i += 1

    def symbolize_footnotes(self):
        """Add symbols indexes to "[*]"-style footnotes and references."""
        labels = []
        for footnote in self.document.symbol_footnotes:
            reps, index = divmod(self.document.symbol_footnote_start, len(self.symbols))
            labeltext = self.symbols[index] * (reps + 1)
            labels.append(labeltext)
            footnote.insert(0, nodes.label('', labeltext))
            self.document.symbol_footnote_start += 1
            self.document.set_id(footnote)

        i = 0
        for ref in self.document.symbol_footnote_refs:
            try:
                ref += nodes.Text(labels[i])
            except IndexError:
                msg = self.document.reporter.error(('Too many symbol footnote references: only %s corresponding footnotes available.' % len(labels)),
                  base_node=ref)
                msgid = self.document.set_id(msg)
                for ref in self.document.symbol_footnote_refs[i:]:
                    if not ref.resolved:
                        if ref.hasattr('refid'):
                            continue
                        prb = nodes.problematic((ref.rawsource),
                          (ref.rawsource), refid=msgid)
                        prbid = self.document.set_id(prb)
                        msg.add_backref(prbid)
                        ref.replace_self(prb)

                break

            footnote = self.document.symbol_footnotes[i]
            assert len(footnote['ids']) == 1
            ref['refid'] = footnote['ids'][0]
            self.document.note_refid(ref)
            footnote.add_backref(ref['ids'][0])
            i += 1

    def resolve_footnotes_and_citations(self):
        """
        Link manually-labeled footnotes and citations to/from their
        references.
        """
        for footnote in self.document.footnotes:
            for label in footnote['names']:
                if label in self.document.footnote_refs:
                    reflist = self.document.footnote_refs[label]
                    self.resolve_references(footnote, reflist)

        for citation in self.document.citations:
            for label in citation['names']:
                if label in self.document.citation_refs:
                    reflist = self.document.citation_refs[label]
                    self.resolve_references(citation, reflist)

    def resolve_references(self, note, reflist):
        assert len(note['ids']) == 1
        id = note['ids'][0]
        for ref in reflist:
            if ref.resolved:
                continue
            ref.delattr('refname')
            ref['refid'] = id
            assert len(ref['ids']) == 1
            note.add_backref(ref['ids'][0])
            ref.resolved = 1

        note.resolved = 1


class CircularSubstitutionDefinitionError(Exception):
    pass


class Substitutions(Transform):
    __doc__ = '\n    Given the following ``document`` as input::\n\n        <document>\n            <paragraph>\n                The\n                <substitution_reference refname="biohazard">\n                    biohazard\n                 symbol is deservedly scary-looking.\n            <substitution_definition name="biohazard">\n                <image alt="biohazard" uri="biohazard.png">\n\n    The ``substitution_reference`` will simply be replaced by the\n    contents of the corresponding ``substitution_definition``.\n\n    The transformed result will be::\n\n        <document>\n            <paragraph>\n                The\n                <image alt="biohazard" uri="biohazard.png">\n                 symbol is deservedly scary-looking.\n            <substitution_definition name="biohazard">\n                <image alt="biohazard" uri="biohazard.png">\n    '
    default_priority = 220

    def apply(self):
        defs = self.document.substitution_defs
        normed = self.document.substitution_names
        subreflist = self.document.traverse(nodes.substitution_reference)
        nested = {}
        for ref in subreflist:
            refname = ref['refname']
            key = None
            if refname in defs:
                key = refname
            else:
                normed_name = refname.lower()
                if normed_name in normed:
                    key = normed[normed_name]
                else:
                    if key is None:
                        msg = self.document.reporter.error(('Undefined substitution referenced: "%s".' % refname),
                          base_node=ref)
                        msgid = self.document.set_id(msg)
                        prb = nodes.problematic((ref.rawsource),
                          (ref.rawsource), refid=msgid)
                        prbid = self.document.set_id(prb)
                        msg.add_backref(prbid)
                        ref.replace_self(prb)
                subdef = defs[key]
                parent = ref.parent
                index = parent.index(ref)
                if 'ltrim' in subdef.attributes or 'trim' in subdef.attributes:
                    if index > 0:
                        if isinstance(parent[(index - 1)], nodes.Text):
                            parent.replace(parent[(index - 1)], parent[(index - 1)].rstrip())
            if not 'rtrim' in subdef.attributes:
                if 'trim' in subdef.attributes:
                    if len(parent) > index + 1:
                        if isinstance(parent[(index + 1)], nodes.Text):
                            parent.replace(parent[(index + 1)], parent[(index + 1)].lstrip())
                subdef_copy = subdef.deepcopy()
                try:
                    for nested_ref in subdef_copy.traverse(nodes.substitution_reference):
                        nested_name = normed[nested_ref['refname'].lower()]
                        if nested_name in nested.setdefault(nested_name, []):
                            raise CircularSubstitutionDefinitionError
                        else:
                            nested[nested_name].append(key)
                            nested_ref['ref-origin'] = ref
                            subreflist.append(nested_ref)

                except CircularSubstitutionDefinitionError:
                    parent = ref.parent
                    if isinstance(parent, nodes.substitution_definition):
                        msg = self.document.reporter.error('Circular substitution definition detected:',
                          (nodes.literal_block(parent.rawsource, parent.rawsource)),
                          line=(parent.line),
                          base_node=parent)
                        parent.replace_self(msg)
                    else:
                        ref_origin = ref
                        while ref_origin.hasattr('ref-origin'):
                            ref_origin = ref_origin['ref-origin']

                        msg = self.document.reporter.error(('Circular substitution definition referenced: "%s".' % refname),
                          base_node=ref_origin)
                        msgid = self.document.set_id(msg)
                        prb = nodes.problematic((ref.rawsource),
                          (ref.rawsource), refid=msgid)
                        prbid = self.document.set_id(prb)
                        msg.add_backref(prbid)
                        ref.replace_self(prb)
                else:
                    ref.replace_self(subdef_copy.children)
                    for node in subdef_copy.children:
                        if isinstance(node, nodes.Referential) and 'refname' in node:
                            self.document.note_refname(node)


class TargetNotes(Transform):
    __doc__ = '\n    Creates a footnote for each external target in the text, and corresponding\n    footnote references after each reference.\n    '
    default_priority = 540

    def __init__(self, document, startnode):
        Transform.__init__(self, document, startnode=startnode)
        self.classes = startnode.details.get('class', [])

    def apply(self):
        notes = {}
        nodelist = []
        for target in self.document.traverse(nodes.target):
            if not target.hasattr('refuri'):
                continue
            names = target['names']
            refs = []
            for name in names:
                refs.extend(self.document.refnames.get(name, []))

            if not refs:
                continue
            footnote = self.make_target_footnote(target['refuri'], refs, notes)
            if target['refuri'] not in notes:
                notes[target['refuri']] = footnote
                nodelist.append(footnote)

        for ref in self.document.traverse(nodes.reference):
            if not ref.get('anonymous'):
                continue
            if ref.hasattr('refuri'):
                footnote = self.make_target_footnote(ref['refuri'], [ref], notes)
                if ref['refuri'] not in notes:
                    notes[ref['refuri']] = footnote
                    nodelist.append(footnote)

        self.startnode.replace_self(nodelist)

    def make_target_footnote(self, refuri, refs, notes):
        if refuri in notes:
            footnote = notes[refuri]
            assert len(footnote['names']) == 1
            footnote_name = footnote['names'][0]
        else:
            footnote = nodes.footnote()
            footnote_id = self.document.set_id(footnote)
            footnote_name = 'TARGET_NOTE: ' + footnote_id
            footnote['auto'] = 1
            footnote['names'] = [footnote_name]
            footnote_paragraph = nodes.paragraph()
            footnote_paragraph += nodes.reference('', refuri, refuri=refuri)
            footnote += footnote_paragraph
            self.document.note_autofootnote(footnote)
            self.document.note_explicit_target(footnote, footnote)
        for ref in refs:
            if isinstance(ref, nodes.target):
                continue
            else:
                refnode = nodes.footnote_reference(refname=footnote_name, auto=1)
                refnode['classes'] += self.classes
                self.document.note_autofootnote_ref(refnode)
                self.document.note_footnote_ref(refnode)
                index = ref.parent.index(ref) + 1
                reflist = [refnode]
                if (utils.get_trim_footnote_ref_space(self.document.settings) or self).classes:
                    reflist.insert(0, nodes.inline(text=' ', Classes=(self.classes)))
                else:
                    reflist.insert(0, nodes.Text(' '))
            ref.parent.insert(index, reflist)

        return footnote


class DanglingReferences(Transform):
    __doc__ = '\n    Check for dangling references (incl. footnote & citation) and for\n    unreferenced targets.\n    '
    default_priority = 850

    def apply(self):
        visitor = DanglingReferencesVisitor(self.document, self.document.transformer.unknown_reference_resolvers)
        self.document.walk(visitor)
        for target in self.document.traverse(nodes.target):
            if not target.referenced:
                if target.get('anonymous'):
                    continue
                elif target['names']:
                    naming = target['names'][0]
                else:
                    if target['ids']:
                        naming = target['ids'][0]
                    else:
                        naming = target['refid']
                self.document.reporter.info(('Hyperlink target "%s" is not referenced.' % naming),
                  base_node=target)


class DanglingReferencesVisitor(nodes.SparseNodeVisitor):

    def __init__(self, document, unknown_reference_resolvers):
        nodes.SparseNodeVisitor.__init__(self, document)
        self.document = document
        self.unknown_reference_resolvers = unknown_reference_resolvers

    def unknown_visit(self, node):
        pass

    def visit_reference(self, node):
        if not node.resolved:
            if not node.hasattr('refname'):
                return
            refname = node['refname']
            id = self.document.nameids.get(refname)
            if id is None:
                for resolver_function in self.unknown_reference_resolvers:
                    if resolver_function(node):
                        break
                else:
                    if refname in self.document.nameids:
                        msg = self.document.reporter.error(('Duplicate target name, cannot be used as a unique reference: "%s".' % node['refname']),
                          base_node=node)
                    else:
                        msg = self.document.reporter.error(('Unknown target name: "%s".' % node['refname']),
                          base_node=node)
                    msgid = self.document.set_id(msg)
                    prb = nodes.problematic((node.rawsource),
                      (node.rawsource), refid=msgid)
                    try:
                        prbid = node['ids'][0]
                    except IndexError:
                        prbid = self.document.set_id(prb)

                    msg.add_backref(prbid)
                    node.replace_self(prb)
        else:
            del node['refname']
            node['refid'] = id
            self.document.ids[id].note_referenced_by(id=id)
            node.resolved = 1

    visit_footnote_reference = visit_citation_reference = visit_reference
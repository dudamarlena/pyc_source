# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/schema/viewer.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 35697 bytes
"""
web2ldap.app.schema.viewer -  Display LDAPv3 schema

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0
from ldap0.schema.subentry import SCHEMA_ATTRS, SCHEMA_CLASS_MAPPING, SCHEMA_ATTR_MAPPING
from ldap0.schema.models import LDAPSyntax, AttributeType, ObjectClass, MatchingRule, MatchingRuleUse, DITContentRule, DITStructureRule, NameForm, OBJECTCLASS_KIND_STR
from web2ldap.web import escape_html
import web2ldap.app.gui, web2ldap.app.schema.syntaxes
OBSOLETE_TEMPL = {False:'%s', 
 True:'<s>%s</s>'}
SCHEMA_VIEWER_USAGE = '\n<p>Hints:</p>\n<ul>\n  <li>You can search for schema elements by OID or name.</li>\n  <li>Wildcard search with * is supported.</li>\n  <li>For browsing choose from context menu on the right</li>\n</ul>\n'

def schema_link_text(se, charset):
    names = [escape_html(name) for name in se.__dict__.get('names', ())]
    obsolete = se.__dict__.get('obsolete', False)
    if len(names) == 1:
        res = names[0]
    else:
        if len(names) > 1:
            res = '%s (alias %s)' % (names[0], ', '.join(names[1:]))
        else:
            if isinstance(se, LDAPSyntax) and se.desc is not None:
                res = escape_html(se.desc)
            else:
                res = escape_html(se.oid)
    return OBSOLETE_TEMPL[obsolete] % res


def schema_anchor(app, se_nameoroid, se_class, name_template='%s', link_text=None):
    """
    Return a pretty HTML-formatted string describing a schema element
    referenced by name or OID
    """
    se = app.schema.get_obj(se_class, se_nameoroid, None)
    if se is None:
        return name_template % app.form.utf2display(se_nameoroid)
    anchor = app.anchor('oid', link_text or schema_link_text(se, app.form.accept_charset), [
     (
      'dn', app.dn),
     (
      'oid', se.oid),
     (
      'oid_class', ldap0.schema.SCHEMA_ATTR_MAPPING[se_class])])
    if link_text is None:
        return name_template % anchor
    return '%s\n%s' % (
     name_template % app.form.utf2display(se_nameoroid),
     anchor)


def schema_anchors(app, se_names, se_class):
    link_texts = []
    for se_nameoroid in se_names:
        se = app.schema.get_obj(se_class, se_nameoroid, default=None)
        if se:
            ltxt = schema_link_text(se, app.form.accept_charset)
            try:
                schema_id = se.oid
            except AttributeError:
                schema_id = se.ruleid
            else:
                anchor = app.anchor('oid', ltxt, [
                 (
                  'dn', app.dn),
                 (
                  'oid', schema_id),
                 (
                  'oid_class', SCHEMA_ATTR_MAPPING[se_class])])
                link_texts.append((ltxt, anchor))
        else:
            link_texts.append((se_nameoroid, se_nameoroid))
    else:
        link_texts.sort(key=(lambda x: x[0].lower()))
        return [i[1] for i in link_texts]


def schema_tree_html(app, schema, se_class, se_tree, se_oid, level):
    """HTML output for browser"""
    app.outf.write('<dl>')
    se_obj = schema.get_obj(se_class, se_oid)
    if se_obj is not None:
        display_id = (se_obj.names or (se_oid,))[0]
        app.outf.write('<dt>%s</dt>' % (
         schema_anchor(app, display_id, se_class),))
    elif se_tree[se_oid]:
        app.outf.write('<dd>')
        for sub_se_oid in se_tree[se_oid]:
            schema_tree_html(app, schema, se_class, se_tree, sub_se_oid, level + 1)
        else:
            app.outf.write('</dd>')

    else:
        app.outf.write('<dd></dd>')
    app.outf.write('</dl>')


def schema_context_menu(app):
    """Build context menu with schema-related items"""
    context_menu_list = []
    sub_schema_dn = None
    try:
        sub_schema_dn = app.ls.l.search_subschemasubentry_s(app.dn)
    except ldap0.LDAPError:
        pass
    else:
        if sub_schema_dn is not None:
            form_param_list = [('dn', sub_schema_dn),
             ('filterstr', '(objectClass=subschema)')]
            for schema_attr in SCHEMA_ATTRS + ['objectClass', 'cn']:
                form_param_list.append(('read_attr', schema_attr))
            else:
                context_menu_list.append(app.anchor('read',
                  'Subschema Subentry', form_param_list,
                  title='Directly read the subschema subentry'))

        if app.schema:
            se_class_attrs = [SCHEMA_ATTR_MAPPING[se_class] for se_class in app.schema.sed.keys() if app.schema.sed[se_class]]
            se_class_attrs.sort(key=(str.lower))
            for se_class_attr in se_class_attrs:
                context_menu_list.append(app.anchor('oid',
                  se_class_attr, [
                 (
                  'dn', app.dn), ('oid_class', se_class_attr)],
                  title=('Browse all %s' % se_class_attr)))

        else:
            return context_menu_list


class DisplaySchemaElement:
    type_desc = 'Abstract Schema Element'
    detail_attrs = ()

    def __init__(self, app, se):
        self._app = app
        self.s = app.schema
        self.se = se
        try:
            schema_id = self.se.oid
        except AttributeError:
            schema_id = self.se.ruleid
        else:
            self.sei = app.schema.get_inheritedobj(self.se.__class__, schema_id, [])

    def disp_details(self):
        for text, class_attr, se_class in self.detail_attrs:
            class_attr_value = self.sei.__dict__.get(class_attr, None)
            if class_attr_value is None:
                pass
            else:
                if isinstance(class_attr_value, (tuple, list)):
                    class_attr_value_list = list(class_attr_value)
                    class_attr_value_list.sort(key=(str.lower))
                else:
                    class_attr_value_list = [
                     class_attr_value]
                if se_class is None:
                    value_output = ', '.join([self._app.form.utf2display(v, sp_entity=' ', lf_entity='<br>') for v in class_attr_value_list])
                else:
                    value_output = ', '.join(schema_anchors(self._app, class_attr_value_list, se_class))
                self._app.outf.write('<dt>%s</dt>\n<dd>\n%s\n</dd>\n' % (text, value_output))

    def display(self):
        ms_ad_schema_link = ''
        if 'schemaNamingContext' in self._app.ls.rootDSE:
            try:
                result = self._app.ls.l.search_s((self._app.ls.rootDSE['schemaNamingContext'][0].decode(self._app.ls.charset)),
                  (ldap0.SCOPE_SUBTREE),
                  ('(|(&(objectClass=attributeSchema)(attributeID=%s))(&(objectClass=classSchema)(governsID=%s)))' % (
                 self.se.oid,
                 self.se.oid)),
                  attrlist=[
                 'cn'])
            except ldap0.LDAPError:
                pass
            else:
                if result:
                    ad_schema_dn, ad_schema_entry = result[0].dn_s, result[0].entry_s
                    ms_ad_schema_link = '<dt>Schema Definition Entry (MS AD)</dt>\n<dd>\n%s\n</dd>\n' % self._app.anchor('read', ad_schema_entry['cn'][0], [
                     (
                      'dn', ad_schema_dn)])
        obsolete = self.se.__dict__.get('obsolete', 0)
        web2ldap.app.gui.top_section((self._app),
          ('%s %s (%s)' % (
         self.type_desc,
         ', '.join(self.se.__dict__.get('names', ())),
         self.se.oid)),
          (web2ldap.app.gui.main_menu(self._app)),
          context_menu_list=(schema_context_menu(self._app)))
        self._app.outf.write('\n            %s\n            <h1>%s <em>%s</em> (%s)</h1>\n            Try to look it up:\n            <a id="alvestrand_oid" href="%s/urlredirect/%s?http://www.alvestrand.no/objectid/%s.html">[Alvestrand]</a>\n            <a id="oid-info_oid" href="%s/urlredirect/%s?http://www.oid-info.com/get/%s">[oid-info.com]</a>\n            <dl>\n            <dt>Schema element string:</dt>\n            <dd><code>%s</code></dd>\n            %s\n            </dl>\n            ' % (
         oid_input_form(self._app, ''),
         self.type_desc,
         OBSOLETE_TEMPL[obsolete] % (
          ', '.join(self.se.__dict__.get('names', ())),),
         self.se.oid,
         self._app.form.script_name, self._app.sid, self.se.oid,
         self._app.form.script_name, self._app.sid, self.se.oid,
         self._app.form.utf2display(str(self.se)),
         ms_ad_schema_link))
        self.disp_details()
        web2ldap.app.gui.footer(self._app)


class DisplayObjectClass(DisplaySchemaElement):
    type_desc = 'Object class'
    detail_attrs = (
     ('Description', 'desc', None),
     (
      'Derived from', 'sup', ObjectClass))

    def __init__(self, app, se):
        DisplaySchemaElement.__init__(self, app, se)
        self.sei = app.schema.get_inheritedobj(self.se.__class__, self.se.oid, ['kind'])

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        must, may = self.s.attribute_types([self.se.oid], raise_keyerror=False)
        self._app.outf.write('<dt>Kind of object class:</dt><dd>\n%s&nbsp;</dd>\n' % OBJECTCLASS_KIND_STR[self.sei.kind])
        self._app.outf.write('<dt>All required attributes:</dt><dd>\n%s&nbsp;</dd>\n' % ', '.join(schema_anchors(self._app, must.keys(), AttributeType)))
        self._app.outf.write('<dt>All allowed attributes:</dt><dd>\n%s&nbsp;</dd>\n' % ', '.join(schema_anchors(self._app, may.keys(), AttributeType)))
        content_rule = self.s.get_obj(DITContentRule, self.se.oid)
        if content_rule:
            self._app.outf.write('<dt>Governed by DIT content rule:</dt><dd>\n%s&nbsp;</dd>\n' % schema_anchor(self._app, content_rule.oid, DITContentRule))
            self._app.outf.write('<dt>Applicable auxiliary object classes:</dt><dd>\n%s&nbsp;</dd>\n' % ', '.join(schema_anchors(self._app, content_rule.aux, ObjectClass)))
        dcr_list = []
        structural_oc_list = []
        for _, content_rule in self.s.sed[DITContentRule].items():
            for aux_class_name in content_rule.aux:
                aux_class_oid = self.s.get_oid(ObjectClass, aux_class_name)
                if aux_class_oid == self.se.oid:
                    dcr_list.append(content_rule.oid)
                    structural_oc_list.append(content_rule.oid)

        else:
            if dcr_list:
                self._app.outf.write('<dt>Referring DIT content rules:</dt><dd>\n%s&nbsp;</dd>\n' % ', '.join(schema_anchors(self._app, dcr_list, DITContentRule)))
            if structural_oc_list:
                self._app.outf.write('<dt>Allowed with structural object classes:</dt><dd>\n%s&nbsp;</dd>\n' % ', '.join(schema_anchors(self._app, structural_oc_list, ObjectClass)))
            oc_ref_list = []

        for nf_oid, name_form_se in self.s.sed[NameForm].items():
            name_form_oc = name_form_se.oc.lower()
            se_names = set([o.lower() for o in self.sei.names])
            if name_form_se.oc == self.sei.oid or name_form_oc in se_names:
                pass
            oc_ref_list.append(nf_oid)
        else:
            if oc_ref_list:
                self._app.outf.write('<dt>Applicable name forms:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, oc_ref_list, NameForm)))
            self._app.outf.write('<dt>Object class tree:</dt>\n')
            self._app.outf.write('<dd>\n')

        try:
            oc_tree = self.s.tree(ObjectClass)
        except KeyError as e:
            try:
                self._app.outf.write('<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % self._app.form.utf2display(str(e)))
            finally:
                e = None
                del e

        else:
            if self.se.oid in oc_tree:
                if oc_tree[self.se.oid]:
                    schema_tree_html(self._app, self.s, ObjectClass, oc_tree, self.se.oid, 0)
            self._app.outf.write('&nbsp;</dd>\n')
            self._app.outf.write('<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % self._app.anchor('searchform',
              ('(objectClass=%s)' % self._app.form.utf2display(str((self.se.names or [self.se.oid])[0]))),
              [
             (
              'dn', self._app.dn),
             ('searchform_mode', 'adv'),
             ('search_attr', 'objectClass'),
             (
              'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
             (
              'search_string', str((self.se.names or [self.se.oid])[0]))],
              title='Search entries by object class'))


class DisplayAttributeType(DisplaySchemaElement):
    type_desc = 'Attribute type'
    detail_attrs = (
     ('Description', 'desc', None),
     (
      'Syntax', 'syntax', LDAPSyntax),
     (
      'Derived from', 'sup', AttributeType),
     (
      'Equality matching rule', 'equality', MatchingRule),
     (
      'Sub-string matching rule', 'substr', MatchingRule),
     (
      'Ordering matching rule', 'ordering', MatchingRule))

    def __init__(self, app, se):
        DisplaySchemaElement.__init__(self, app, se)
        try:
            self.sei = app.schema.get_inheritedobj(self.se.__class__, self.se.oid, ('syntax',
                                                                                    'equality',
                                                                                    'substr',
                                                                                    'ordering'))
        except KeyError:
            self.sei = app.schema.get_obj(self.se.__class__, self.se.oid)

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        at_oid = self.se.oid
        syntax_oid = self.sei.syntax
        self._app.outf.write('<dt>Usage:</dt>\n<dd>\n%s\n</dd>\n' % {0:'userApplications', 
         1:'directoryOperation', 
         2:'distributedOperation', 
         3:'dSAOperation'}[self.se.usage])
        if syntax_oid is not None:
            mr_use_se = self.s.get_obj(MatchingRuleUse, syntax_oid)
            applies_dict = {}
            for mr_oid, mr_use_se in self.s.sed[MatchingRuleUse].items():
                applies_dict[mr_oid] = {}
                mr_use_se = self.s.get_obj(MatchingRuleUse, mr_oid)
                for a in mr_use_se.applies:
                    applies_dict[mr_oid][self.s.get_oid(AttributeType, a)] = None
                else:
                    mr_applicable_for = [mr_oid for mr_oid in self.s.sed[MatchingRule].keys() if mr_oid in applies_dict if at_oid in applies_dict[mr_oid]]
                    if mr_applicable_for:
                        self._app.outf.write('<dt>Applicable matching rules:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, mr_applicable_for, MatchingRule)))

        attr_type_ref_list = []
        for oc_oid, object_class_se in self.s.sed[ObjectClass].items():
            object_class_se = self.s.get_obj(ObjectClass, oc_oid)

        for dcr_at in object_class_se.must + object_class_se.may:
            if not dcr_at == at_oid:
                if dcr_at in self.sei.names:
                    pass
                attr_type_ref_list.append(oc_oid)
        else:
            if attr_type_ref_list:
                self._app.outf.write('<dt>Directly referencing object classes:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)))
            all_object_classes = self.s.sed[ObjectClass].keys()
            attr_type_ref_list = []
            for oc_oid in all_object_classes:
                must, may = self.s.attribute_types([oc_oid], raise_keyerror=False)
                if at_oid in must or at_oid in may:
                    pass
                attr_type_ref_list.append(oc_oid)
            else:
                if attr_type_ref_list:
                    self._app.outf.write('<dt>Usable in these object classes:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)))
                attr_type_ref_list = []
                for dcr_oid, dit_content_rule_se in self.s.sed[DITContentRule].items():
                    dit_content_rule_se = self.s.get_obj(DITContentRule, dcr_oid)

        for dcr_at in dit_content_rule_se.must + dit_content_rule_se.may + dit_content_rule_se.nots:
            if not dcr_at == at_oid:
                if dcr_at in self.sei.names:
                    pass
                attr_type_ref_list.append(dcr_oid)
        else:
            if attr_type_ref_list:
                self._app.outf.write('<dt>Referencing DIT content rules:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, attr_type_ref_list, DITContentRule)))
            attr_type_ref_list = []
            for nf_oid, name_form_se in self.s.sed[NameForm].items():
                name_form_se = self.s.get_obj(NameForm, nf_oid)

            for nf_at in name_form_se.must + name_form_se.may:
                if not nf_at == at_oid:
                    if nf_at in self.sei.names:
                        pass
                    attr_type_ref_list.append(nf_oid)
            else:
                if attr_type_ref_list:
                    self._app.outf.write('<dt>Referencing name forms:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, attr_type_ref_list, NameForm)))
                self._app.outf.write('<dt>Attribute type tree:</dt>\n<dd>\n')
                try:
                    at_tree = self.s.tree(AttributeType)
                except KeyError as e:
                    try:
                        self._app.outf.write('<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % self._app.form.utf2display(str(e)))
                    finally:
                        e = None
                        del e

                else:
                    if at_oid in at_tree:
                        if at_tree[at_oid]:
                            schema_tree_html(self._app, self.s, AttributeType, at_tree, at_oid, 0)
                    self._app.outf.write('</dd>\n<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % self._app.anchor('searchform',
                      ('(%s=*)' % self._app.form.utf2display(str((self.se.names or [self.se.oid])[0]))),
                      [
                     (
                      'dn', self._app.dn),
                     ('searchform_mode', 'adv'),
                     (
                      'search_attr', str((self.se.names or [self.se.oid])[0])),
                     (
                      'search_option', web2ldap.app.searchform.SEARCH_OPT_ATTR_EXISTS),
                     ('search_string', '')],
                      title='Search entries by attribute presence'))
                    self._app.outf.write('\n          <dt>Associated plugin class(es):</dt>\n          <dd>\n            <table>\n              <tr><th>Structural<br>object class</th><th>Plugin class</th>')
                for structural_oc in web2ldap.app.schema.syntaxes.syntax_registry.at2syntax[at_oid].keys() or [None]:
                    syntax_class = web2ldap.app.schema.syntaxes.syntax_registry.get_syntax(self.s, at_oid, structural_oc)
                    if structural_oc:
                        oc_text = schema_anchor(self._app, structural_oc, ObjectClass)
                    else:
                        oc_text = '-any-'
                    self._app.outf.write('<tr><td>%s</td><td>%s.%s</td></th>\n' % (
                     oc_text,
                     self._app.form.utf2display(str(syntax_class.__module__)),
                     self._app.form.utf2display(str(syntax_class.__name__))))
                else:
                    self._app.outf.write('</table>\n</dd>\n')


class DisplayLDAPSyntax(DisplaySchemaElement):
    type_desc = 'LDAP Syntax'
    detail_attrs = (('Description', 'desc', None), )

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        syntax_using_at_list = [at_oid for at_oid in self.s.sed[AttributeType].keys() if self.s.get_syntax(at_oid) == self.se.oid]
        if syntax_using_at_list:
            self._app.outf.write('<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, syntax_using_at_list, AttributeType)))
        syntax_ref_mr_list = [mr_oid for mr_oid in self.s.listall(MatchingRule, [('syntax', self.se.oid)])]
        if syntax_ref_mr_list:
            self._app.outf.write('<dt>Referencing matching rules:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, syntax_ref_mr_list, MatchingRule)))
        try:
            x_subst = self.se.x_subst
        except AttributeError:
            pass
        else:
            if x_subst:
                self._app.outf.write('<dt>Substituted by:</dt>\n<dd>\n%s\n</dd>\n' % schema_anchor(self._app, x_subst, LDAPSyntax))
            self._app.outf.write('<dt>Associated syntax class</dt>\n<dd>\n%s\n</dd>\n' % '.'.join((syntax_class.__module__, syntax_class.__name__)))


class DisplayMatchingRule(DisplaySchemaElement):
    type_desc = 'Matching Rule'
    detail_attrs = (
     ('Description', 'desc', None),
     (
      'LDAP syntax', 'syntax', LDAPSyntax))

    def disp_details--- This code section failed: ---

 L. 608         0  LOAD_GLOBAL              DisplaySchemaElement
                2  LOAD_METHOD              disp_details
                4  LOAD_FAST                'self'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 609        10  LOAD_FAST                'self'
               12  LOAD_ATTR                s
               14  LOAD_METHOD              get_obj
               16  LOAD_GLOBAL              MatchingRuleUse
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                se
               22  LOAD_ATTR                oid
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'mr_use_se'

 L. 610        28  LOAD_FAST                'mr_use_se'
               30  POP_JUMP_IF_FALSE   134  'to 134'

 L. 611        32  BUILD_MAP_0           0 
               34  STORE_DEREF              'applies_dict'

 L. 612        36  LOAD_FAST                'mr_use_se'
               38  LOAD_ATTR                applies
               40  GET_ITER         
               42  FOR_ITER             66  'to 66'
               44  STORE_FAST               'a'

 L. 613        46  LOAD_CONST               None
               48  LOAD_DEREF               'applies_dict'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                s
               54  LOAD_METHOD              get_oid
               56  LOAD_GLOBAL              AttributeType
               58  LOAD_FAST                'a'
               60  CALL_METHOD_2         2  ''
               62  STORE_SUBSCR     
               64  JUMP_BACK            42  'to 42'

 L. 615        66  LOAD_CLOSURE             'applies_dict'
               68  BUILD_TUPLE_1         1 
               70  LOAD_LISTCOMP            '<code_object <listcomp>>'
               72  LOAD_STR                 'DisplayMatchingRule.disp_details.<locals>.<listcomp>'
               74  MAKE_FUNCTION_8          'closure'

 L. 617        76  LOAD_FAST                'self'
               78  LOAD_ATTR                s
               80  LOAD_ATTR                sed
               82  LOAD_GLOBAL              AttributeType
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              keys
               88  CALL_METHOD_0         0  ''

 L. 615        90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'mr_applicable_for'

 L. 620        96  LOAD_FAST                'mr_applicable_for'
               98  POP_JUMP_IF_FALSE   134  'to 134'

 L. 621       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _app
              104  LOAD_ATTR                outf
              106  LOAD_METHOD              write
              108  LOAD_STR                 '<dt>Applicable for attribute types per matching rule use:</dt>\n<dd>\n%s\n</dd>\n'

 L. 622       110  LOAD_STR                 ', '
              112  LOAD_METHOD              join
              114  LOAD_GLOBAL              schema_anchors
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _app
              120  LOAD_FAST                'mr_applicable_for'
              122  LOAD_GLOBAL              AttributeType
              124  CALL_FUNCTION_3       3  ''
              126  CALL_METHOD_1         1  ''

 L. 621       128  BINARY_MODULO    
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
            134_0  COME_FROM            98  '98'
            134_1  COME_FROM            30  '30'

 L. 624       134  BUILD_LIST_0          0 
              136  STORE_FAST               'mr_used_by'

 L. 625       138  LOAD_FAST                'self'
              140  LOAD_ATTR                s
              142  LOAD_ATTR                sed
              144  LOAD_GLOBAL              AttributeType
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              keys
              150  CALL_METHOD_0         0  ''
              152  GET_ITER         
            154_0  COME_FROM           296  '296'
            154_1  COME_FROM           202  '202'
              154  FOR_ITER            312  'to 312'
              156  STORE_FAST               'at_oid'

 L. 626       158  SETUP_FINALLY       180  'to 180'

 L. 627       160  LOAD_FAST                'self'
              162  LOAD_ATTR                s
              164  LOAD_METHOD              get_inheritedobj
              166  LOAD_GLOBAL              AttributeType
              168  LOAD_FAST                'at_oid'
              170  LOAD_CONST               ('equality', 'substr', 'ordering')
              172  CALL_METHOD_3         3  ''
              174  STORE_FAST               'at_se'
              176  POP_BLOCK        
              178  JUMP_FORWARD        200  'to 200'
            180_0  COME_FROM_FINALLY   158  '158'

 L. 628       180  DUP_TOP          
              182  LOAD_GLOBAL              KeyError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   198  'to 198'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 629       194  POP_EXCEPT       
              196  JUMP_BACK           154  'to 154'
            198_0  COME_FROM           186  '186'
              198  END_FINALLY      
            200_0  COME_FROM           178  '178'

 L. 631       200  LOAD_FAST                'at_se'
              202  POP_JUMP_IF_FALSE   154  'to 154'

 L. 632       204  LOAD_FAST                'at_se'
              206  LOAD_ATTR                equality
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                se
              212  LOAD_ATTR                names
              214  COMPARE_OP               in

 L. 631   216_218  POP_JUMP_IF_TRUE    298  'to 298'

 L. 632       220  LOAD_FAST                'at_se'
              222  LOAD_ATTR                substr
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                se
              228  LOAD_ATTR                names
              230  COMPARE_OP               in

 L. 631   232_234  POP_JUMP_IF_TRUE    298  'to 298'

 L. 632       236  LOAD_FAST                'at_se'
              238  LOAD_ATTR                ordering
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                se
              244  LOAD_ATTR                names
              246  COMPARE_OP               in

 L. 631   248_250  POP_JUMP_IF_TRUE    298  'to 298'

 L. 633       252  LOAD_FAST                'at_se'
              254  LOAD_ATTR                equality
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                se
              260  LOAD_ATTR                oid
              262  COMPARE_OP               ==

 L. 631   264_266  POP_JUMP_IF_TRUE    298  'to 298'

 L. 633       268  LOAD_FAST                'at_se'
              270  LOAD_ATTR                substr
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                se
              276  LOAD_ATTR                oid
              278  COMPARE_OP               ==

 L. 631   280_282  POP_JUMP_IF_TRUE    298  'to 298'

 L. 633       284  LOAD_FAST                'at_se'
              286  LOAD_ATTR                ordering
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                se
              292  LOAD_ATTR                oid
              294  COMPARE_OP               ==

 L. 631       296  POP_JUMP_IF_FALSE   154  'to 154'
            298_0  COME_FROM           280  '280'
            298_1  COME_FROM           264  '264'
            298_2  COME_FROM           248  '248'
            298_3  COME_FROM           232  '232'
            298_4  COME_FROM           216  '216'

 L. 635       298  LOAD_FAST                'mr_used_by'
              300  LOAD_METHOD              append
              302  LOAD_FAST                'at_se'
              304  LOAD_ATTR                oid
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_BACK           154  'to 154'

 L. 636       312  LOAD_FAST                'mr_used_by'
          314_316  POP_JUMP_IF_FALSE   352  'to 352'

 L. 637       318  LOAD_FAST                'self'
              320  LOAD_ATTR                _app
              322  LOAD_ATTR                outf
              324  LOAD_METHOD              write
              326  LOAD_STR                 '<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n'

 L. 638       328  LOAD_STR                 ', '
              330  LOAD_METHOD              join
              332  LOAD_GLOBAL              schema_anchors
              334  LOAD_FAST                'self'
              336  LOAD_ATTR                _app
              338  LOAD_FAST                'mr_used_by'
              340  LOAD_GLOBAL              AttributeType
              342  CALL_FUNCTION_3       3  ''
              344  CALL_METHOD_1         1  ''

 L. 637       346  BINARY_MODULO    
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          
            352_0  COME_FROM           314  '314'

Parse error at or near `LOAD_FAST' instruction at offset 312


class DisplayMatchingRuleUse(DisplaySchemaElement):
    type_desc = 'Matching Rule Use'
    detail_attrs = (
     ('Names', 'names', None),
     (
      'Matching Rule', 'oid', MatchingRule),
     (
      'Applies to', 'applies', AttributeType))


class DisplayDITContentRule(DisplaySchemaElement):
    type_desc = 'DIT content rule'
    detail_attrs = (
     ('Names', 'names', None),
     (
      'Governs structural object class', 'oid', ObjectClass),
     (
      'Auxiliary classes', 'aux', ObjectClass),
     (
      'Must have', 'must', AttributeType),
     (
      'May have', 'may', AttributeType),
     (
      'Must not have', 'nots', AttributeType))


class DisplayDITStructureRule(DisplaySchemaElement):
    type_desc = 'DIT structure rule'
    detail_attrs = (
     ('Description', 'desc', None),
     (
      'Associated name form', 'form', NameForm),
     (
      'Superior structure rules', 'sup', DITStructureRule))

    def display(self):
        web2ldap.app.gui.top_section((self._app),
          ('%s %s (%s)' % (
         self.type_desc,
         ', '.join(self.se.__dict__.get('names', ())),
         self.se.ruleid)),
          (web2ldap.app.gui.main_menu(self._app)),
          context_menu_list=(schema_context_menu(self._app)))
        self._app.outf.write('\n            %s\n            <h1>%s <em>%s</em> (%s)</h1>\n            <dl>\n            <dt>Schema element string:</dt>\n            <dd><code>%s</code></dd>\n            </dl>\n            ' % (
         oid_input_form(self._app, ''),
         self.type_desc,
         ', '.join(self.se.__dict__.get('names', ())),
         self.se.ruleid,
         self._app.form.utf2display(str(self.se).decode(self._app.ls.charset))))
        self.disp_details()
        web2ldap.app.gui.footer(self._app)

    def disp_details(self):
        """
        Display subordinate DIT structure rule(s)
        """
        DisplaySchemaElement.disp_details(self)
        ditsr_rules_ref_list = []
        for ditsr_id, ditsr_se in self.s.sed[DITStructureRule].items():
            if self.sei.ruleid in ditsr_se.sup:
                ditsr_rules_ref_list.append(ditsr_id)
        else:
            if ditsr_rules_ref_list:
                self._app.outf.write('<dt>Subordinate DIT structure rules:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, ditsr_rules_ref_list, DITStructureRule)))


class DisplayNameForm(DisplaySchemaElement):
    type_desc = 'Name form'
    detail_attrs = (
     ('Description', 'desc', None),
     (
      'Structural object class this rule applies to', 'oc', ObjectClass),
     (
      'Mandantory naming attributes', 'must', AttributeType),
     (
      'Allowed naming attributes', 'may', AttributeType))

    def disp_details(self):
        """
        Display referencing DIT structure rule(s)
        """
        DisplaySchemaElement.disp_details(self)
        ditsr_rules_ref_list = []
        for ditsr_id, ditsr_se in self.s.sed[DITStructureRule].items():
            if ditsr_se.form == self.sei.oid or ditsr_se.form in self.sei.names:
                ditsr_rules_ref_list.append(ditsr_id)
        else:
            if ditsr_rules_ref_list:
                self._app.outf.write('<dt>Referencing DIT structure rule:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, ditsr_rules_ref_list, DITStructureRule)))


SCHEMA_VIEWER_CLASS = {ObjectClass: DisplayObjectClass, 
 AttributeType: DisplayAttributeType, 
 LDAPSyntax: DisplayLDAPSyntax, 
 MatchingRule: DisplayMatchingRule, 
 MatchingRuleUse: DisplayMatchingRuleUse, 
 DITContentRule: DisplayDITContentRule, 
 DITStructureRule: DisplayDITStructureRule, 
 NameForm: DisplayNameForm}

def oid_input_form(app, oid=None):
    oid_input_field_html = web2ldap.app.form.OIDInput('oid',
      'OID or descriptive name of schema element',
      default=oid).input_html(oid)
    oid_class_select_html = app.form.field['oid_class'].input_html('')
    return app.form_html('oid',
      'Search', 'GET', [
     (
      'dn', app.dn)],
      extrastr=('\n'.join((oid_input_field_html, oid_class_select_html))))


def display_schema_elements(app, se_classes, se_list):
    se_list = se_list or []
    se_classes = tuple(filter(None, se_classes or []) or SCHEMA_CLASS_MAPPING.values())
    web2ldap.app.gui.top_section(app,
      'Schema elements',
      (web2ldap.app.gui.main_menu(app)),
      context_menu_list=(schema_context_menu(app)))
    if app.schema is None:
        raise web2ldap.app.core.ErrorExit('No sub schema available!')
    oid_dict = {}
    if se_list:
        for schema_class in se_classes:
            oid_dict[schema_class] = []
        else:
            for se in se_list:
                try:
                    se_id = se.oid
                except AttributeError:
                    se_id = se.ruleid
                else:
                    try:
                        oid_dict[se.__class__].append(se_id)
                    except KeyError:
                        oid_dict[se.__class__] = [
                         se_id]

    else:
        for schema_class in se_classes:
            oid_dict[schema_class] = app.schema.sed[schema_class].keys()
        else:
            app.outf.write(oid_input_form(app, ''))
            if oid_dict:
                for schema_class in oid_dict.keys():
                    schema_elements = oid_dict[schema_class]
                    if not schema_elements:
                        pass
                    else:
                        app.outf.write('<h2>%s</h2>\n<p>found %d</p>\n%s\n' % (
                         SCHEMA_VIEWER_CLASS[schema_class].type_desc,
                         len(schema_elements),
                         ',\n '.join(schema_anchors(app, schema_elements, schema_class))))

            else:
                app.outf.write(SCHEMA_VIEWER_USAGE)
            web2ldap.app.gui.footer(app)


def w2l_schema_viewer--- This code section failed: ---

 L. 823         0  LOAD_CODE                <code_object contains_oid>
                2  LOAD_STR                 'w2l_schema_viewer.<locals>.contains_oid'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'contains_oid'

 L. 826         8  LOAD_CODE                <code_object startswith_oid>
               10  LOAD_STR                 'w2l_schema_viewer.<locals>.startswith_oid'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'startswith_oid'

 L. 829        16  LOAD_CODE                <code_object endswith_oid>
               18  LOAD_STR                 'w2l_schema_viewer.<locals>.endswith_oid'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'endswith_oid'

 L. 833        24  LOAD_FAST                'app'
               26  LOAD_ATTR                form
               28  LOAD_METHOD              getInputValue
               30  LOAD_STR                 'oid'
               32  LOAD_CONST               None
               34  BUILD_LIST_1          1 
               36  CALL_METHOD_2         2  ''
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  STORE_FAST               'oid'

 L. 834        44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               46  LOAD_STR                 'w2l_schema_viewer.<locals>.<listcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 836        50  LOAD_FAST                'app'
               52  LOAD_ATTR                form
               54  LOAD_METHOD              getInputValue
               56  LOAD_STR                 'oid_class'
               58  BUILD_LIST_0          0 
               60  CALL_METHOD_2         2  ''

 L. 834        62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'se_classes'

 L. 840        68  LOAD_FAST                'oid'
               70  POP_JUMP_IF_TRUE     88  'to 88'

 L. 842        72  LOAD_GLOBAL              display_schema_elements
               74  LOAD_FAST                'app'
               76  LOAD_FAST                'se_classes'
               78  LOAD_CONST               None
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          

 L. 843        84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            70  '70'

 L. 846        88  LOAD_FAST                'oid'
               90  LOAD_METHOD              strip
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'oid'

 L. 847        96  LOAD_FAST                'oid'
               98  LOAD_METHOD              lower
              100  CALL_METHOD_0         0  ''
              102  LOAD_METHOD              endswith
              104  LOAD_STR                 ';binary'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 848       110  LOAD_FAST                'oid'
              112  LOAD_CONST               None
              114  LOAD_CONST               -7
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'oid'
            122_0  COME_FROM           108  '108'

 L. 851       122  LOAD_FAST                'oid'
              124  LOAD_METHOD              startswith
              126  LOAD_STR                 '*'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_FALSE   164  'to 164'
              132  LOAD_FAST                'oid'
              134  LOAD_METHOD              endswith
              136  LOAD_STR                 '*'
              138  CALL_METHOD_1         1  ''
              140  POP_JUMP_IF_FALSE   164  'to 164'

 L. 852       142  LOAD_FAST                'oid'
              144  LOAD_CONST               1
              146  LOAD_CONST               -1
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  LOAD_METHOD              lower
              154  CALL_METHOD_0         0  ''
              156  STORE_FAST               'oid_mv'

 L. 853       158  LOAD_FAST                'contains_oid'
              160  STORE_FAST               'cmp_method'
              162  JUMP_FORWARD        232  'to 232'
            164_0  COME_FROM           140  '140'
            164_1  COME_FROM           130  '130'

 L. 854       164  LOAD_FAST                'oid'
              166  LOAD_METHOD              startswith
              168  LOAD_STR                 '*'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   196  'to 196'

 L. 855       174  LOAD_FAST                'oid'
              176  LOAD_CONST               1
              178  LOAD_CONST               None
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  LOAD_METHOD              lower
              186  CALL_METHOD_0         0  ''
              188  STORE_FAST               'oid_mv'

 L. 856       190  LOAD_FAST                'endswith_oid'
              192  STORE_FAST               'cmp_method'
              194  JUMP_FORWARD        232  'to 232'
            196_0  COME_FROM           172  '172'

 L. 857       196  LOAD_FAST                'oid'
              198  LOAD_METHOD              endswith
              200  LOAD_STR                 '*'
              202  CALL_METHOD_1         1  ''
              204  POP_JUMP_IF_FALSE   228  'to 228'

 L. 858       206  LOAD_FAST                'oid'
              208  LOAD_CONST               None
              210  LOAD_CONST               -1
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_METHOD              lower
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'oid_mv'

 L. 859       222  LOAD_FAST                'startswith_oid'
              224  STORE_FAST               'cmp_method'
              226  JUMP_FORWARD        232  'to 232'
            228_0  COME_FROM           204  '204'

 L. 861       228  LOAD_CONST               None
              230  STORE_FAST               'cmp_method'
            232_0  COME_FROM           226  '226'
            232_1  COME_FROM           194  '194'
            232_2  COME_FROM           162  '162'

 L. 863       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'se_classes'
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_CONST               1
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   304  'to 304'
              246  LOAD_FAST                'cmp_method'
              248  LOAD_CONST               None
              250  COMPARE_OP               is
          252_254  POP_JUMP_IF_FALSE   304  'to 304'

 L. 865       256  BUILD_LIST_0          0 
              258  STORE_FAST               'se_list'

 L. 866       260  LOAD_FAST                'app'
              262  LOAD_ATTR                schema
              264  LOAD_METHOD              get_obj
              266  LOAD_FAST                'se_classes'
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  LOAD_FAST                'oid'
              274  LOAD_CONST               None
              276  CALL_METHOD_3         3  ''
              278  STORE_FAST               'se_obj'

 L. 867       280  LOAD_FAST                'se_obj'
              282  LOAD_CONST               None
              284  COMPARE_OP               is-not
          286_288  POP_JUMP_IF_FALSE   582  'to 582'

 L. 868       290  LOAD_FAST                'se_list'
              292  LOAD_METHOD              append
              294  LOAD_FAST                'se_obj'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
          300_302  JUMP_FORWARD        582  'to 582'
            304_0  COME_FROM           252  '252'
            304_1  COME_FROM           242  '242'

 L. 871       304  BUILD_LIST_0          0 
              306  STORE_FAST               'se_list'

 L. 872       308  LOAD_FAST                'cmp_method'
              310  LOAD_CONST               None
              312  COMPARE_OP               is
          314_316  POP_JUMP_IF_FALSE   378  'to 378'

 L. 874       318  LOAD_FAST                'se_classes'
          320_322  JUMP_IF_TRUE_OR_POP   330  'to 330'
              324  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              326  LOAD_METHOD              keys
              328  CALL_METHOD_0         0  ''
            330_0  COME_FROM           320  '320'
              330  GET_ITER         
            332_0  COME_FROM           358  '358'
              332  FOR_ITER            376  'to 376'
              334  STORE_FAST               'schema_element_type'

 L. 875       336  LOAD_FAST                'app'
              338  LOAD_ATTR                schema
              340  LOAD_METHOD              get_obj
              342  LOAD_FAST                'schema_element_type'
              344  LOAD_FAST                'oid'
              346  LOAD_CONST               None
              348  CALL_METHOD_3         3  ''
              350  STORE_FAST               'se'

 L. 876       352  LOAD_FAST                'se'
              354  LOAD_CONST               None
              356  COMPARE_OP               is-not
          358_360  POP_JUMP_IF_FALSE   332  'to 332'

 L. 877       362  LOAD_FAST                'se_list'
              364  LOAD_METHOD              append
              366  LOAD_FAST                'se'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
          372_374  JUMP_BACK           332  'to 332'
              376  JUMP_FORWARD        582  'to 582'
            378_0  COME_FROM           314  '314'

 L. 880       378  LOAD_FAST                'se_classes'
          380_382  JUMP_IF_TRUE_OR_POP   390  'to 390'
              384  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              386  LOAD_METHOD              keys
              388  CALL_METHOD_0         0  ''
            390_0  COME_FROM           380  '380'
              390  GET_ITER         
              392  FOR_ITER            582  'to 582'
              394  STORE_FAST               'schema_element_type'

 L. 881       396  LOAD_FAST                'app'
              398  LOAD_ATTR                schema
              400  LOAD_ATTR                sed
              402  LOAD_FAST                'schema_element_type'
              404  BINARY_SUBSCR    
              406  LOAD_METHOD              values
              408  CALL_METHOD_0         0  ''
              410  GET_ITER         
              412  FOR_ITER            578  'to 578'
              414  STORE_FAST               'se'

 L. 882       416  SETUP_FINALLY       428  'to 428'

 L. 883       418  LOAD_FAST                'se'
              420  LOAD_ATTR                oid
              422  STORE_FAST               'se_id'
              424  POP_BLOCK        
              426  JUMP_FORWARD        456  'to 456'
            428_0  COME_FROM_FINALLY   416  '416'

 L. 884       428  DUP_TOP          
              430  LOAD_GLOBAL              AttributeError
              432  COMPARE_OP               exception-match
          434_436  POP_JUMP_IF_FALSE   454  'to 454'
              438  POP_TOP          
              440  POP_TOP          
              442  POP_TOP          

 L. 885       444  LOAD_FAST                'se'
              446  LOAD_ATTR                ruleid
              448  STORE_FAST               'se_id'
              450  POP_EXCEPT       
              452  JUMP_FORWARD        456  'to 456'
            454_0  COME_FROM           434  '434'
              454  END_FINALLY      
            456_0  COME_FROM           452  '452'
            456_1  COME_FROM           426  '426'

 L. 886       456  LOAD_FAST                'cmp_method'
              458  LOAD_FAST                'se_id'
              460  LOAD_METHOD              lower
              462  CALL_METHOD_0         0  ''
              464  LOAD_FAST                'oid_mv'
              466  CALL_FUNCTION_2       2  ''
          468_470  POP_JUMP_IF_FALSE   484  'to 484'

 L. 888       472  LOAD_FAST                'se_list'
              474  LOAD_METHOD              append
              476  LOAD_FAST                'se'
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          
              482  JUMP_BACK           412  'to 412'
            484_0  COME_FROM           468  '468'

 L. 891       484  SETUP_FINALLY       496  'to 496'

 L. 892       486  LOAD_FAST                'se'
              488  LOAD_ATTR                names
              490  STORE_FAST               'se_names'
              492  POP_BLOCK        
              494  JUMP_FORWARD        524  'to 524'
            496_0  COME_FROM_FINALLY   484  '484'

 L. 893       496  DUP_TOP          
              498  LOAD_GLOBAL              AttributeError
              500  COMPARE_OP               exception-match
          502_504  POP_JUMP_IF_FALSE   522  'to 522'
              506  POP_TOP          
              508  POP_TOP          
              510  POP_TOP          

 L. 894       512  POP_EXCEPT       
          514_516  JUMP_BACK           412  'to 412'
              518  POP_EXCEPT       
              520  JUMP_FORWARD        524  'to 524'
            522_0  COME_FROM           502  '502'
              522  END_FINALLY      
            524_0  COME_FROM           520  '520'
            524_1  COME_FROM           494  '494'

 L. 895       524  LOAD_FAST                'se_names'
          526_528  JUMP_IF_TRUE_OR_POP   532  'to 532'
              530  BUILD_LIST_0          0 
            532_0  COME_FROM           526  '526'
              532  GET_ITER         
            534_0  COME_FROM           550  '550'
              534  FOR_ITER            574  'to 574'
              536  STORE_FAST               'se_name'

 L. 896       538  LOAD_FAST                'cmp_method'
              540  LOAD_FAST                'se_name'
              542  LOAD_METHOD              lower
              544  CALL_METHOD_0         0  ''
              546  LOAD_FAST                'oid_mv'
              548  CALL_FUNCTION_2       2  ''
          550_552  POP_JUMP_IF_FALSE   534  'to 534'

 L. 897       554  LOAD_FAST                'se_list'
              556  LOAD_METHOD              append
              558  LOAD_FAST                'se'
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          

 L. 898       564  POP_TOP          
          566_568  CONTINUE            412  'to 412'
          570_572  JUMP_BACK           534  'to 534'
          574_576  JUMP_BACK           412  'to 412'
          578_580  JUMP_BACK           392  'to 392'
            582_0  COME_FROM           376  '376'
            582_1  COME_FROM           300  '300'
            582_2  COME_FROM           286  '286'

 L. 900       582  LOAD_FAST                'se_list'
          584_586  POP_JUMP_IF_TRUE    636  'to 636'

 L. 902       588  LOAD_FAST                'app'
              590  LOAD_ATTR                simple_message

 L. 903       592  LOAD_STR                 ''

 L. 904       594  LOAD_STR                 '<h1>Schema elements</h1><p class="ErrorMessage">Name or OID not found in schema!</p><p>%s</p>'

 L. 905       596  LOAD_GLOBAL              oid_input_form
              598  LOAD_FAST                'app'
              600  LOAD_FAST                'oid'
              602  CALL_FUNCTION_2       2  ''

 L. 904       604  BINARY_MODULO    

 L. 907       606  LOAD_STR                 'Message'

 L. 908       608  LOAD_GLOBAL              web2ldap
              610  LOAD_ATTR                app
              612  LOAD_ATTR                gui
              614  LOAD_METHOD              main_menu
              616  LOAD_FAST                'app'
              618  CALL_METHOD_1         1  ''

 L. 909       620  LOAD_GLOBAL              schema_context_menu
              622  LOAD_FAST                'app'
              624  CALL_FUNCTION_1       1  ''

 L. 902       626  LOAD_CONST               ('title', 'message', 'main_div_id', 'main_menu_list', 'context_menu_list')
              628  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              630  POP_TOP          

 L. 911       632  LOAD_CONST               None
              634  RETURN_VALUE     
            636_0  COME_FROM           584  '584'

 L. 912       636  LOAD_GLOBAL              len
              638  LOAD_FAST                'se_list'
              640  CALL_FUNCTION_1       1  ''
              642  LOAD_CONST               1
              644  COMPARE_OP               >
          646_648  POP_JUMP_IF_FALSE   666  'to 666'

 L. 914       650  LOAD_GLOBAL              display_schema_elements
              652  LOAD_FAST                'app'
              654  LOAD_CONST               None
              656  LOAD_FAST                'se_list'
              658  CALL_FUNCTION_3       3  ''
              660  POP_TOP          

 L. 915       662  LOAD_CONST               None
              664  RETURN_VALUE     
            666_0  COME_FROM           646  '646'

 L. 918       666  LOAD_FAST                'se_list'
              668  LOAD_CONST               0
              670  BINARY_SUBSCR    
              672  STORE_FAST               'se_obj'

 L. 919       674  LOAD_FAST                'se_obj'
              676  LOAD_ATTR                __class__
              678  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              680  COMPARE_OP               not-in
          682_684  POP_JUMP_IF_FALSE   700  'to 700'

 L. 920       686  LOAD_GLOBAL              web2ldap
              688  LOAD_ATTR                app
              690  LOAD_ATTR                core
              692  LOAD_METHOD              ErrorExit
              694  LOAD_STR                 'No viewer for this type of schema element!'
              696  CALL_METHOD_1         1  ''
              698  RAISE_VARARGS_1       1  'exception instance'
            700_0  COME_FROM           682  '682'

 L. 921       700  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              702  LOAD_FAST                'se_obj'
              704  LOAD_ATTR                __class__
              706  BINARY_SUBSCR    
              708  LOAD_FAST                'app'
              710  LOAD_FAST                'se_obj'
              712  CALL_FUNCTION_2       2  ''
              714  STORE_FAST               'schema_viewer'

 L. 922       716  LOAD_FAST                'schema_viewer'
              718  LOAD_METHOD              display
              720  CALL_METHOD_0         0  ''
              722  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 518
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/schema/viewer.py
# Compiled at: 2020-05-04 07:49:38
# Size of source mod 2**32: 36952 bytes
"""
web2ldap.app.schema.viewer -  Display LDAPv3 schema

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0
from ldap0.schema.subentry import SCHEMA_ATTRS, SCHEMA_ATTR_MAPPING, SCHEMA_CLASS_MAPPING
from ldap0.schema.models import LDAPSyntax, AttributeType, ObjectClass, MatchingRule, MatchingRuleUse, DITContentRule, DITStructureRule, NameForm, OBJECTCLASS_KIND_STR
from web2ldap.web import escape_html
import web2ldap.app.gui, web2ldap.app.schema.syntaxes
OBSOLETE_TEMPL = {False:'%s', 
 True:'<s>%s</s>'}
SCHEMA_VIEWER_USAGE = '\n<p>Hints:</p>\n<ul>\n  <li>You can search for schema elements by OID or name.</li>\n  <li>Wildcard search with * is supported.</li>\n  <li>For browsing choose from context menu on the right</li>\n</ul>\n'
SCHEMA_ELEMENT_HEAD_TMPL = '\n%s\n<h1>%s <em>%s</em> (%s)</h1>\nTry to look it up:\n<a id="alvestrand_oid" href="%s/urlredirect/%s?https://www.alvestrand.no/objectid/%s.html">[Alvestrand]</a>\n<a id="oid-info_oid" href="%s/urlredirect/%s?http://www.oid-info.com/get/%s">[oid-info.com]</a>\n<dl>\n<dt>Schema element string:</dt>\n<dd><code>%s</code></dd>\n%s\n</dl>\n'

def schema_link_text(se_obj):
    names = [escape_html(name) for name in getattr(se_obj, 'names', ())]
    obsolete = getattr(se_obj, 'obsolete', False)
    if len(names) == 1:
        res = names[0]
    else:
        if len(names) > 1:
            res = '{name} (alias {other_names})'.format(name=(names[0]),
              other_names=(', '.join(names[1:])))
        else:
            if isinstance(se_obj, LDAPSyntax) and se_obj.desc is not None:
                res = escape_html(se_obj.desc)
            else:
                res = escape_html(se_obj.oid)
    return OBSOLETE_TEMPL[obsolete] % res


def schema_anchor(app, se_nameoroid, se_class, name_template='{name}\n{anchor}', link_text=None):
    """
    Return a pretty HTML-formatted string describing a schema element
    referenced by name or OID
    """
    try:
        se_obj = app.schema.get_obj(se_class, se_nameoroid, None, raise_keyerror=True)
    except KeyError:
        anchor = ''
    else:
        anchor = app.anchor('oid', link_text or schema_link_text(se_obj), [
         (
          'dn', app.dn),
         (
          'oid', se_obj.oid),
         (
          'oid_class', SCHEMA_ATTR_MAPPING[se_class])])
    return name_template.format(name=(app.form.utf2display(se_nameoroid)),
      anchor=anchor)


def schema_anchors--- This code section failed: ---

 L. 119         0  BUILD_LIST_0          0 
                2  STORE_FAST               'link_texts'

 L. 120         4  LOAD_FAST                'se_names'
                6  GET_ITER         
                8  FOR_ITER            176  'to 176'
               10  STORE_FAST               'se_nameoroid'

 L. 121        12  SETUP_FINALLY        38  'to 38'

 L. 122        14  LOAD_FAST                'app'
               16  LOAD_ATTR                schema
               18  LOAD_ATTR                get_obj
               20  LOAD_FAST                'se_class'
               22  LOAD_FAST                'se_nameoroid'
               24  LOAD_CONST               None
               26  LOAD_CONST               True
               28  LOAD_CONST               ('default', 'raise_keyerror')
               30  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               32  STORE_FAST               'se_obj'
               34  POP_BLOCK        
               36  JUMP_FORWARD         76  'to 76'
             38_0  COME_FROM_FINALLY    12  '12'

 L. 123        38  DUP_TOP          
               40  LOAD_GLOBAL              KeyError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    74  'to 74'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 124        52  LOAD_FAST                'link_texts'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'se_nameoroid'
               58  LOAD_FAST                'se_nameoroid'
               60  BUILD_TUPLE_2         2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 125        66  POP_EXCEPT       
               68  JUMP_BACK             8  'to 8'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            44  '44'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            36  '36'

 L. 126        76  LOAD_GLOBAL              schema_link_text
               78  LOAD_FAST                'se_obj'
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'ltxt'

 L. 127        84  SETUP_FINALLY        96  'to 96'

 L. 128        86  LOAD_FAST                'se_obj'
               88  LOAD_ATTR                oid
               90  STORE_FAST               'schema_id'
               92  POP_BLOCK        
               94  JUMP_FORWARD        122  'to 122'
             96_0  COME_FROM_FINALLY    84  '84'

 L. 129        96  DUP_TOP          
               98  LOAD_GLOBAL              AttributeError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   120  'to 120'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 130       110  LOAD_FAST                'se_obj'
              112  LOAD_ATTR                ruleid
              114  STORE_FAST               'schema_id'
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM           102  '102'
              120  END_FINALLY      
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            94  '94'

 L. 131       122  LOAD_FAST                'app'
              124  LOAD_METHOD              anchor

 L. 132       126  LOAD_STR                 'oid'

 L. 132       128  LOAD_FAST                'ltxt'

 L. 134       130  LOAD_STR                 'dn'
              132  LOAD_FAST                'app'
              134  LOAD_ATTR                dn
              136  BUILD_TUPLE_2         2 

 L. 135       138  LOAD_STR                 'oid'
              140  LOAD_FAST                'schema_id'
              142  BUILD_TUPLE_2         2 

 L. 136       144  LOAD_STR                 'oid_class'
              146  LOAD_GLOBAL              SCHEMA_ATTR_MAPPING
              148  LOAD_FAST                'se_class'
              150  BINARY_SUBSCR    
              152  BUILD_TUPLE_2         2 

 L. 133       154  BUILD_LIST_3          3 

 L. 131       156  CALL_METHOD_3         3  ''
              158  STORE_FAST               'anchor'

 L. 139       160  LOAD_FAST                'link_texts'
              162  LOAD_METHOD              append
              164  LOAD_FAST                'ltxt'
              166  LOAD_FAST                'anchor'
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_BACK             8  'to 8'

 L. 140       176  LOAD_FAST                'link_texts'
              178  LOAD_ATTR                sort
              180  LOAD_LAMBDA              '<code_object <lambda>>'
              182  LOAD_STR                 'schema_anchors.<locals>.<lambda>'
              184  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              186  LOAD_CONST               ('key',)
              188  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              190  POP_TOP          

 L. 141       192  LOAD_LISTCOMP            '<code_object <listcomp>>'
              194  LOAD_STR                 'schema_anchors.<locals>.<listcomp>'
              196  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              198  LOAD_FAST                'link_texts'
              200  GET_ITER         
              202  CALL_FUNCTION_1       1  ''
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 70


def schema_tree_html(app, schema, se_class, se_tree, se_oid, level):
    """HTML output for browser"""
    app.outf.write('<dl>')
    se_obj = schema.get_obj(se_class, se_oid)
    if se_obj is not None:
        display_id = (se_obj.names or (se_oid,))[0]
        app.outf.write(schema_anchor(app, display_id, se_class, name_template='<dt>{anchor}</dt>'))
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
                  title=('Browse all %s' % (se_class_attr,))))

        else:
            return context_menu_list


class DisplaySchemaElement:
    type_desc = 'Abstract Schema Element'
    detail_attrs = ()

    def __init__(self, app, se_obj):
        self._app = app
        self._schema = app.schema
        self._se = se_obj
        try:
            schema_id = self._se.oid
        except AttributeError:
            schema_id = self._se.ruleid
        else:
            self._sei = app.schema.get_inheritedobj(self._se.__class__, schema_id, [])

    def disp_details(self):
        for text, class_attr, se_class in self.detail_attrs:
            class_attr_value = getattr(self._sei, class_attr, None)
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
                 self._se.oid,
                 self._se.oid)),
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
        obsolete = getattr(self._se, 'obsolete', 0)
        web2ldap.app.gui.top_section((self._app),
          ('%s %s (%s)' % (
         self.type_desc,
         ', '.join(getattr(self._se, 'names', ())),
         self._se.oid)),
          (web2ldap.app.gui.main_menu(self._app)),
          context_menu_list=(schema_context_menu(self._app)))
        self._app.outf.write(SCHEMA_ELEMENT_HEAD_TMPL % (
         oid_input_form(self._app, ''),
         self.type_desc,
         OBSOLETE_TEMPL[obsolete] % (
          ', '.join(getattr(self._se, 'names', ())),),
         self._se.oid,
         self._app.form.script_name, self._app.sid, self._se.oid,
         self._app.form.script_name, self._app.sid, self._se.oid,
         self._app.form.utf2display(str(self._se)),
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
        self._sei = app.schema.get_inheritedobj(self._se.__class__, self._se.oid, ['kind'])

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        must, may = self._schema.attribute_types([self._se.oid], raise_keyerror=False)
        self._app.outf.write('<dt>Kind of object class:</dt><dd>\n%s&nbsp;</dd>\n' % (
         OBJECTCLASS_KIND_STR[self._sei.kind],))
        self._app.outf.write('<dt>All required attributes:</dt><dd>\n%s&nbsp;</dd>\n' % (
         ', '.join(schema_anchors(self._app, must.keys(), AttributeType)),))
        self._app.outf.write('<dt>All allowed attributes:</dt><dd>\n%s&nbsp;</dd>\n' % (
         ', '.join(schema_anchors(self._app, may.keys(), AttributeType)),))
        content_rule = self._schema.get_obj(DITContentRule, self._se.oid)
        if content_rule:
            self._app.outf.write('<dt>Governed by DIT content rule:</dt><dd>\n%s&nbsp;</dd>\n' % (
             schema_anchor(self._app, content_rule.oid, DITContentRule),))
            self._app.outf.write('<dt>Applicable auxiliary object classes:</dt><dd>\n%s&nbsp;</dd>\n' % (
             ', '.join(schema_anchors(self._app, content_rule.aux, ObjectClass)),))
        dcr_list = []
        structural_oc_list = []
        for _, content_rule in self._schema.sed[DITContentRule].items():
            for aux_class_name in content_rule.aux:
                aux_class_oid = self._schema.get_oid(ObjectClass, aux_class_name)
                if aux_class_oid == self._se.oid:
                    dcr_list.append(content_rule.oid)
                    structural_oc_list.append(content_rule.oid)

        else:
            if dcr_list:
                self._app.outf.write('<dt>Referring DIT content rules:</dt><dd>\n%s&nbsp;</dd>\n' % (
                 ', '.join(schema_anchors(self._app, dcr_list, DITContentRule)),))
            if structural_oc_list:
                self._app.outf.write('<dt>Allowed with structural object classes:</dt><dd>\n%s&nbsp;</dd>\n' % (
                 ', '.join(schema_anchors(self._app, structural_oc_list, ObjectClass)),))
            oc_ref_list = []

        for nf_oid, name_form_se in self._schema.sed[NameForm].items():
            name_form_oc = name_form_se.oc.lower()
            se_names = {o.lower() for o in self._sei.names}
            if name_form_se.oc == self._sei.oid or name_form_oc in se_names:
                pass
            oc_ref_list.append(nf_oid)
        else:
            if oc_ref_list:
                self._app.outf.write('<dt>Applicable name forms:</dt>\n<dd>\n%s\n</dd>\n' % (
                 ', '.join(schema_anchors(self._app, oc_ref_list, NameForm)),))
            self._app.outf.write('<dt>Object class tree:</dt>\n')
            self._app.outf.write('<dd>\n')

        try:
            oc_tree = self._schema.tree(ObjectClass)
        except KeyError as err:
            try:
                self._app.outf.write('<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % (
                 self._app.form.utf2display(err),))
            finally:
                err = None
                del err

        else:
            if self._se.oid in oc_tree:
                if oc_tree[self._se.oid]:
                    schema_tree_html(self._app, self._schema, ObjectClass, oc_tree, self._se.oid, 0)
            self._app.outf.write('&nbsp;</dd>\n')
            self._app.outf.write('<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % (
             self._app.anchor('searchform',
               ('(objectClass=%s)' % (
              self._app.form.utf2display((self._se.names or [self._se.oid])[0]),)),
               [
              (
               'dn', self._app.dn),
              ('searchform_mode', 'adv'),
              ('search_attr', 'objectClass'),
              (
               'search_option', web2ldap.app.searchform.SEARCH_OPT_IS_EQUAL),
              (
               'search_string', (self._se.names or [self._se.oid])[0])],
               title='Search entries by object class'),))


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
            self._sei = app.schema.get_inheritedobj(self._se.__class__, self._se.oid, ('syntax',
                                                                                       'equality',
                                                                                       'substr',
                                                                                       'ordering'))
        except KeyError:
            self._sei = app.schema.get_obj(self._se.__class__, self._se.oid)

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        at_oid = self._se.oid
        syntax_oid = self._sei.syntax
        self._app.outf.write('<dt>Usage:</dt>\n<dd>\n%s\n</dd>\n' % (
         {0:'userApplications', 
          1:'directoryOperation', 
          2:'distributedOperation', 
          3:'dSAOperation'}[self._se.usage],))
        if syntax_oid is not None:
            mr_use_se = self._schema.get_obj(MatchingRuleUse, syntax_oid)
            applies_dict = {}
            for mr_oid, mr_use_se in self._schema.sed[MatchingRuleUse].items():
                applies_dict[mr_oid] = {}
                mr_use_se = self._schema.get_obj(MatchingRuleUse, mr_oid)
                for at_nameoroid in mr_use_se.applies:
                    applies_dict[mr_oid][self._schema.get_oid(AttributeType, at_nameoroid)] = None
                else:
                    mr_applicable_for = [mr_oid for mr_oid in self._schema.sed[MatchingRule].keys() if mr_oid in applies_dict if at_oid in applies_dict[mr_oid]]
                    if mr_applicable_for:
                        self._app.outf.write('<dt>Applicable matching rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                         ', '.join(schema_anchors(self._app, mr_applicable_for, MatchingRule)),))

        attr_type_ref_list = []
        for oc_oid, object_class_se in self._schema.sed[ObjectClass].items():
            object_class_se = self._schema.get_obj(ObjectClass, oc_oid)

        for dcr_at in object_class_se.must + object_class_se.may:
            if not dcr_at == at_oid:
                if dcr_at in self._sei.names:
                    pass
                attr_type_ref_list.append(oc_oid)
        else:
            if attr_type_ref_list:
                self._app.outf.write('<dt>Directly referencing object classes:</dt>\n<dd>\n%s\n</dd>\n' % (
                 ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)),))
            all_object_classes = self._schema.sed[ObjectClass].keys()
            attr_type_ref_list = []
            for oc_oid in all_object_classes:
                must, may = self._schema.attribute_types([oc_oid], raise_keyerror=False)
                if at_oid in must or at_oid in may:
                    pass
                attr_type_ref_list.append(oc_oid)
            else:
                if attr_type_ref_list:
                    self._app.outf.write('<dt>Usable in these object classes:</dt>\n<dd>\n%s\n</dd>\n' % (
                     ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)),))
                attr_type_ref_list = []
                for dcr_oid, dit_content_rule_se in self._schema.sed[DITContentRule].items():
                    dit_content_rule_se = self._schema.get_obj(DITContentRule, dcr_oid)

        for dcr_at in dit_content_rule_se.must + dit_content_rule_se.may + dit_content_rule_se.nots:
            if not dcr_at == at_oid:
                if dcr_at in self._sei.names:
                    pass
                attr_type_ref_list.append(dcr_oid)
        else:
            if attr_type_ref_list:
                self._app.outf.write('<dt>Referencing DIT content rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                 ', '.join(schema_anchors(self._app, attr_type_ref_list, DITContentRule)),))
            attr_type_ref_list = []
            for nf_oid, name_form_se in self._schema.sed[NameForm].items():
                name_form_se = self._schema.get_obj(NameForm, nf_oid)

            for nf_at in name_form_se.must + name_form_se.may:
                if not nf_at == at_oid:
                    if nf_at in self._sei.names:
                        pass
                    attr_type_ref_list.append(nf_oid)
            else:
                if attr_type_ref_list:
                    self._app.outf.write('<dt>Referencing name forms:</dt>\n<dd>\n%s\n</dd>\n' % (
                     ', '.join(schema_anchors(self._app, attr_type_ref_list, NameForm)),))
                self._app.outf.write('<dt>Attribute type tree:</dt>\n<dd>\n')
                try:
                    at_tree = self._schema.tree(AttributeType)
                except KeyError as err:
                    try:
                        self._app.outf.write('<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % (
                         self._app.form.utf2display(err),))
                    finally:
                        err = None
                        del err

                else:
                    if at_oid in at_tree:
                        if at_tree[at_oid]:
                            schema_tree_html(self._app, self._schema, AttributeType, at_tree, at_oid, 0)
                    self._app.outf.write('</dd>\n<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % (
                     self._app.anchor('searchform',
                       ('(%s=*)' % (
                      self._app.form.utf2display((self._se.names or [self._se.oid])[0]),)),
                       [
                      (
                       'dn', self._app.dn),
                      ('searchform_mode', 'adv'),
                      (
                       'search_attr', (self._se.names or [self._se.oid])[0]),
                      (
                       'search_option', web2ldap.app.searchform.SEARCH_OPT_ATTR_EXISTS),
                      ('search_string', '')],
                       title='Search entries by attribute presence'),))
                    self._app.outf.write('\n          <dt>Associated plugin class(es):</dt>\n          <dd>\n            <table>\n              <tr><th>Structural<br>object class</th><th>Plugin class</th>')
                for structural_oc in web2ldap.app.schema.syntaxes.syntax_registry.at2syntax[at_oid].keys() or [None]:
                    syntax_class = web2ldap.app.schema.syntaxes.syntax_registry.get_syntax(self._schema, at_oid, structural_oc)
                    if structural_oc:
                        oc_text = schema_anchor(self._app, structural_oc, ObjectClass)
                    else:
                        oc_text = '-any-'
                    self._app.outf.write('<tr><td>%s</td><td>%s.%s</td></th>\n' % (
                     oc_text,
                     self._app.form.utf2display(syntax_class.__module__),
                     self._app.form.utf2display(syntax_class.__name__)))
                else:
                    self._app.outf.write('</table>\n</dd>\n')


class DisplayLDAPSyntax(DisplaySchemaElement):
    type_desc = 'LDAP Syntax'
    detail_attrs = (('Description', 'desc', None), )

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        syntax_using_at_list = [at_oid for at_oid in self._schema.sed[AttributeType].keys() if self._schema.get_syntax(at_oid) == self._se.oid]
        if syntax_using_at_list:
            self._app.outf.write('<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, syntax_using_at_list, AttributeType)))
        syntax_ref_mr_list = self._schema.listall(MatchingRule, [('syntax', self._se.oid)])
        if syntax_ref_mr_list:
            self._app.outf.write('<dt>Referencing matching rules:</dt>\n<dd>\n%s\n</dd>\n' % ', '.join(schema_anchors(self._app, syntax_ref_mr_list, MatchingRule)))
        try:
            x_subst = self._se.x_subst
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

 L. 647         0  LOAD_GLOBAL              DisplaySchemaElement
                2  LOAD_METHOD              disp_details
                4  LOAD_FAST                'self'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 648        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _schema
               14  LOAD_METHOD              get_obj
               16  LOAD_GLOBAL              MatchingRuleUse
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _se
               22  LOAD_ATTR                oid
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'mr_use_se'

 L. 649        28  LOAD_FAST                'mr_use_se'
               30  POP_JUMP_IF_FALSE   136  'to 136'

 L. 650        32  BUILD_MAP_0           0 
               34  STORE_DEREF              'applies_dict'

 L. 651        36  LOAD_FAST                'mr_use_se'
               38  LOAD_ATTR                applies
               40  GET_ITER         
               42  FOR_ITER             66  'to 66'
               44  STORE_FAST               'at_nameoroid'

 L. 652        46  LOAD_CONST               None
               48  LOAD_DEREF               'applies_dict'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _schema
               54  LOAD_METHOD              get_oid
               56  LOAD_GLOBAL              AttributeType
               58  LOAD_FAST                'at_nameoroid'
               60  CALL_METHOD_2         2  ''
               62  STORE_SUBSCR     
               64  JUMP_BACK            42  'to 42'

 L. 654        66  LOAD_CLOSURE             'applies_dict'
               68  BUILD_TUPLE_1         1 
               70  LOAD_LISTCOMP            '<code_object <listcomp>>'
               72  LOAD_STR                 'DisplayMatchingRule.disp_details.<locals>.<listcomp>'
               74  MAKE_FUNCTION_8          'closure'

 L. 656        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _schema
               80  LOAD_ATTR                sed
               82  LOAD_GLOBAL              AttributeType
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              keys
               88  CALL_METHOD_0         0  ''

 L. 654        90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'mr_applicable_for'

 L. 659        96  LOAD_FAST                'mr_applicable_for'
               98  POP_JUMP_IF_FALSE   136  'to 136'

 L. 660       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _app
              104  LOAD_ATTR                outf
              106  LOAD_METHOD              write

 L. 662       108  LOAD_STR                 '<dt>Applicable for attribute types per matching rule use:</dt>\n<dd>\n%s\n</dd>\n'

 L. 665       110  LOAD_STR                 ', '
              112  LOAD_METHOD              join
              114  LOAD_GLOBAL              schema_anchors
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _app
              120  LOAD_FAST                'mr_applicable_for'
              122  LOAD_GLOBAL              AttributeType
              124  CALL_FUNCTION_3       3  ''
              126  CALL_METHOD_1         1  ''

 L. 664       128  BUILD_TUPLE_1         1 

 L. 661       130  BINARY_MODULO    

 L. 660       132  CALL_METHOD_1         1  ''
              134  POP_TOP          
            136_0  COME_FROM            98  '98'
            136_1  COME_FROM            30  '30'

 L. 668       136  BUILD_LIST_0          0 
              138  STORE_FAST               'mr_used_by'

 L. 669       140  LOAD_GLOBAL              set
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _se
              146  LOAD_ATTR                names
              148  CALL_FUNCTION_1       1  ''
              150  STORE_FAST               'mr_names'

 L. 670       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _schema
              156  LOAD_ATTR                sed
              158  LOAD_GLOBAL              AttributeType
              160  BINARY_SUBSCR    
              162  GET_ITER         
            164_0  COME_FROM           286  '286'
              164  FOR_ITER            302  'to 302'
              166  STORE_FAST               'at_oid'

 L. 671       168  SETUP_FINALLY       190  'to 190'

 L. 672       170  LOAD_FAST                'self'
              172  LOAD_ATTR                _schema
              174  LOAD_METHOD              get_inheritedobj

 L. 673       176  LOAD_GLOBAL              AttributeType

 L. 674       178  LOAD_FAST                'at_oid'

 L. 675       180  LOAD_CONST               ('equality', 'substr', 'ordering')

 L. 672       182  CALL_METHOD_3         3  ''
              184  STORE_FAST               'at_se'
              186  POP_BLOCK        
              188  JUMP_FORWARD        214  'to 214'
            190_0  COME_FROM_FINALLY   168  '168'

 L. 677       190  DUP_TOP          
              192  LOAD_GLOBAL              KeyError
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   212  'to 212'
              198  POP_TOP          
              200  POP_TOP          
              202  POP_TOP          

 L. 678       204  POP_EXCEPT       
              206  JUMP_BACK           164  'to 164'
              208  POP_EXCEPT       
              210  JUMP_FORWARD        214  'to 214'
            212_0  COME_FROM           196  '196'
              212  END_FINALLY      
            214_0  COME_FROM           210  '210'
            214_1  COME_FROM           188  '188'

 L. 679       214  LOAD_FAST                'at_se'
              216  LOAD_CONST               None
              218  COMPARE_OP               is
              220  POP_JUMP_IF_FALSE   224  'to 224'

 L. 680       222  JUMP_BACK           164  'to 164'
            224_0  COME_FROM           220  '220'

 L. 681       224  LOAD_FAST                'at_se'
              226  LOAD_ATTR                equality
              228  LOAD_FAST                'at_se'
              230  LOAD_ATTR                substr
              232  LOAD_FAST                'at_se'
              234  LOAD_ATTR                ordering
              236  BUILD_SET_3           3 
              238  STORE_FAST               'at_mr_set'

 L. 683       240  LOAD_FAST                'at_se'
              242  LOAD_ATTR                equality
              244  LOAD_FAST                'mr_names'
              246  COMPARE_OP               in

 L. 682   248_250  POP_JUMP_IF_TRUE    288  'to 288'

 L. 684       252  LOAD_FAST                'at_se'
              254  LOAD_ATTR                substr
              256  LOAD_FAST                'mr_names'
              258  COMPARE_OP               in

 L. 682   260_262  POP_JUMP_IF_TRUE    288  'to 288'

 L. 685       264  LOAD_FAST                'at_se'
              266  LOAD_ATTR                ordering
              268  LOAD_FAST                'mr_names'
              270  COMPARE_OP               in

 L. 682   272_274  POP_JUMP_IF_TRUE    288  'to 288'

 L. 686       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _se
              280  LOAD_ATTR                oid
              282  LOAD_FAST                'at_mr_set'
              284  COMPARE_OP               in

 L. 682       286  POP_JUMP_IF_FALSE   164  'to 164'
            288_0  COME_FROM           272  '272'
            288_1  COME_FROM           260  '260'
            288_2  COME_FROM           248  '248'

 L. 688       288  LOAD_FAST                'mr_used_by'
              290  LOAD_METHOD              append
              292  LOAD_FAST                'at_se'
              294  LOAD_ATTR                oid
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_BACK           164  'to 164'

 L. 689       302  LOAD_FAST                'mr_used_by'
          304_306  POP_JUMP_IF_FALSE   342  'to 342'

 L. 690       308  LOAD_FAST                'self'
              310  LOAD_ATTR                _app
              312  LOAD_ATTR                outf
              314  LOAD_METHOD              write
              316  LOAD_STR                 '<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n'

 L. 691       318  LOAD_STR                 ', '
              320  LOAD_METHOD              join
              322  LOAD_GLOBAL              schema_anchors
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                _app
              328  LOAD_FAST                'mr_used_by'
              330  LOAD_GLOBAL              AttributeType
              332  CALL_FUNCTION_3       3  ''
              334  CALL_METHOD_1         1  ''

 L. 690       336  BINARY_MODULO    
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          
            342_0  COME_FROM           304  '304'

Parse error at or near `POP_EXCEPT' instruction at offset 208


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
         ', '.join(getattr(self._se, 'names', ())),
         self._se.ruleid)),
          (web2ldap.app.gui.main_menu(self._app)),
          context_menu_list=(schema_context_menu(self._app)))
        self._app.outf.write('\n            %s\n            <h1>%s <em>%s</em> (%s)</h1>\n            <dl>\n            <dt>Schema element string:</dt>\n            <dd><code>%s</code></dd>\n            </dl>\n            ' % (
         oid_input_form(self._app, ''),
         self.type_desc,
         ', '.join(getattr(self._se, 'names', ())),
         self._se.ruleid,
         self._app.form.utf2display(str(self._se))))
        self.disp_details()
        web2ldap.app.gui.footer(self._app)

    def disp_details(self):
        """
        Display subordinate DIT structure rule(s)
        """
        DisplaySchemaElement.disp_details(self)
        ditsr_rules_ref_list = []
        for ditsr_id, ditsr_se in self._schema.sed[DITStructureRule].items():
            if self._sei.ruleid in ditsr_se.sup:
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
        for ditsr_id, ditsr_se in self._schema.sed[DITStructureRule].items():
            if ditsr_se.form == self._sei.oid or ditsr_se.form in self._sei.names:
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
            for se_obj in se_list:
                try:
                    se_id = se_obj.oid
                except AttributeError:
                    se_id = se_obj.ruleid
                else:
                    try:
                        oid_dict[se_obj.__class__].append(se_id)
                    except KeyError:
                        oid_dict[se_obj.__class__] = [
                         se_id]

    else:
        for schema_class in se_classes:
            oid_dict[schema_class] = app.schema.sed[schema_class].keys()
        else:
            app.outf.write(oid_input_form(app, ''))
            if oid_dict:
                for schema_class in oid_dict:
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

 L. 876         0  LOAD_CODE                <code_object contains_oid>
                2  LOAD_STR                 'w2l_schema_viewer.<locals>.contains_oid'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'contains_oid'

 L. 879         8  LOAD_CODE                <code_object startswith_oid>
               10  LOAD_STR                 'w2l_schema_viewer.<locals>.startswith_oid'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'startswith_oid'

 L. 882        16  LOAD_CODE                <code_object endswith_oid>
               18  LOAD_STR                 'w2l_schema_viewer.<locals>.endswith_oid'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'endswith_oid'

 L. 886        24  LOAD_FAST                'app'
               26  LOAD_ATTR                form
               28  LOAD_METHOD              getInputValue
               30  LOAD_STR                 'oid'
               32  LOAD_CONST               None
               34  BUILD_LIST_1          1 
               36  CALL_METHOD_2         2  ''
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  STORE_FAST               'oid'

 L. 887        44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               46  LOAD_STR                 'w2l_schema_viewer.<locals>.<listcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 889        50  LOAD_FAST                'app'
               52  LOAD_ATTR                form
               54  LOAD_METHOD              getInputValue
               56  LOAD_STR                 'oid_class'
               58  BUILD_LIST_0          0 
               60  CALL_METHOD_2         2  ''

 L. 887        62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'se_classes'

 L. 893        68  LOAD_FAST                'oid'
               70  POP_JUMP_IF_TRUE     88  'to 88'

 L. 895        72  LOAD_GLOBAL              display_schema_elements
               74  LOAD_FAST                'app'
               76  LOAD_FAST                'se_classes'
               78  LOAD_CONST               None
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          

 L. 896        84  LOAD_CONST               None
               86  RETURN_VALUE     
             88_0  COME_FROM            70  '70'

 L. 899        88  LOAD_FAST                'oid'
               90  LOAD_METHOD              strip
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'oid'

 L. 900        96  LOAD_FAST                'oid'
               98  LOAD_METHOD              lower
              100  CALL_METHOD_0         0  ''
              102  LOAD_METHOD              endswith
              104  LOAD_STR                 ';binary'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   122  'to 122'

 L. 901       110  LOAD_FAST                'oid'
              112  LOAD_CONST               None
              114  LOAD_CONST               -7
              116  BUILD_SLICE_2         2 
              118  BINARY_SUBSCR    
              120  STORE_FAST               'oid'
            122_0  COME_FROM           108  '108'

 L. 904       122  LOAD_FAST                'oid'
              124  LOAD_METHOD              startswith
              126  LOAD_STR                 '*'
              128  CALL_METHOD_1         1  ''
              130  POP_JUMP_IF_FALSE   164  'to 164'
              132  LOAD_FAST                'oid'
              134  LOAD_METHOD              endswith
              136  LOAD_STR                 '*'
              138  CALL_METHOD_1         1  ''
              140  POP_JUMP_IF_FALSE   164  'to 164'

 L. 905       142  LOAD_FAST                'oid'
              144  LOAD_CONST               1
              146  LOAD_CONST               -1
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  LOAD_METHOD              lower
              154  CALL_METHOD_0         0  ''
              156  STORE_FAST               'oid_mv'

 L. 906       158  LOAD_FAST                'contains_oid'
              160  STORE_FAST               'cmp_method'
              162  JUMP_FORWARD        232  'to 232'
            164_0  COME_FROM           140  '140'
            164_1  COME_FROM           130  '130'

 L. 907       164  LOAD_FAST                'oid'
              166  LOAD_METHOD              startswith
              168  LOAD_STR                 '*'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   196  'to 196'

 L. 908       174  LOAD_FAST                'oid'
              176  LOAD_CONST               1
              178  LOAD_CONST               None
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  LOAD_METHOD              lower
              186  CALL_METHOD_0         0  ''
              188  STORE_FAST               'oid_mv'

 L. 909       190  LOAD_FAST                'endswith_oid'
              192  STORE_FAST               'cmp_method'
              194  JUMP_FORWARD        232  'to 232'
            196_0  COME_FROM           172  '172'

 L. 910       196  LOAD_FAST                'oid'
              198  LOAD_METHOD              endswith
              200  LOAD_STR                 '*'
              202  CALL_METHOD_1         1  ''
              204  POP_JUMP_IF_FALSE   228  'to 228'

 L. 911       206  LOAD_FAST                'oid'
              208  LOAD_CONST               None
              210  LOAD_CONST               -1
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_METHOD              lower
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'oid_mv'

 L. 912       222  LOAD_FAST                'startswith_oid'
              224  STORE_FAST               'cmp_method'
              226  JUMP_FORWARD        232  'to 232'
            228_0  COME_FROM           204  '204'

 L. 914       228  LOAD_CONST               None
              230  STORE_FAST               'cmp_method'
            232_0  COME_FROM           226  '226'
            232_1  COME_FROM           194  '194'
            232_2  COME_FROM           162  '162'

 L. 916       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'se_classes'
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_CONST               1
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   304  'to 304'
              246  LOAD_FAST                'cmp_method'
              248  LOAD_CONST               None
              250  COMPARE_OP               is
          252_254  POP_JUMP_IF_FALSE   304  'to 304'

 L. 918       256  BUILD_LIST_0          0 
              258  STORE_FAST               'se_list'

 L. 919       260  LOAD_FAST                'app'
              262  LOAD_ATTR                schema
              264  LOAD_METHOD              get_obj
              266  LOAD_FAST                'se_classes'
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  LOAD_FAST                'oid'
              274  LOAD_CONST               None
              276  CALL_METHOD_3         3  ''
              278  STORE_FAST               'se_obj'

 L. 920       280  LOAD_FAST                'se_obj'
              282  LOAD_CONST               None
              284  COMPARE_OP               is-not
          286_288  POP_JUMP_IF_FALSE   604  'to 604'

 L. 921       290  LOAD_FAST                'se_list'
              292  LOAD_METHOD              append
              294  LOAD_FAST                'se_obj'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
          300_302  JUMP_FORWARD        604  'to 604'
            304_0  COME_FROM           252  '252'
            304_1  COME_FROM           242  '242'

 L. 924       304  BUILD_LIST_0          0 
              306  STORE_FAST               'se_list'

 L. 925       308  LOAD_FAST                'cmp_method'
              310  LOAD_CONST               None
              312  COMPARE_OP               is
          314_316  POP_JUMP_IF_FALSE   400  'to 400'

 L. 927       318  LOAD_FAST                'se_classes'
          320_322  JUMP_IF_TRUE_OR_POP   330  'to 330'
              324  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              326  LOAD_METHOD              keys
              328  CALL_METHOD_0         0  ''
            330_0  COME_FROM           320  '320'
              330  GET_ITER         
              332  FOR_ITER            398  'to 398'
              334  STORE_FAST               'schema_element_type'

 L. 928       336  SETUP_FINALLY       362  'to 362'

 L. 929       338  LOAD_FAST                'app'
              340  LOAD_ATTR                schema
              342  LOAD_ATTR                get_obj
              344  LOAD_FAST                'schema_element_type'
              346  LOAD_FAST                'oid'
              348  LOAD_CONST               None
              350  LOAD_CONST               True
              352  LOAD_CONST               ('raise_keyerror',)
              354  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              356  STORE_FAST               'se_obj'
              358  POP_BLOCK        
              360  JUMP_FORWARD        384  'to 384'
            362_0  COME_FROM_FINALLY   336  '336'

 L. 930       362  DUP_TOP          
              364  LOAD_GLOBAL              KeyError
              366  COMPARE_OP               exception-match
          368_370  POP_JUMP_IF_FALSE   382  'to 382'
              372  POP_TOP          
              374  POP_TOP          
              376  POP_TOP          

 L. 931       378  POP_EXCEPT       
              380  JUMP_BACK           332  'to 332'
            382_0  COME_FROM           368  '368'
              382  END_FINALLY      
            384_0  COME_FROM           360  '360'

 L. 933       384  LOAD_FAST                'se_list'
              386  LOAD_METHOD              append
              388  LOAD_FAST                'se_obj'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
          394_396  JUMP_BACK           332  'to 332'
              398  JUMP_FORWARD        604  'to 604'
            400_0  COME_FROM           314  '314'

 L. 936       400  LOAD_FAST                'se_classes'
          402_404  JUMP_IF_TRUE_OR_POP   412  'to 412'
              406  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              408  LOAD_METHOD              keys
              410  CALL_METHOD_0         0  ''
            412_0  COME_FROM           402  '402'
              412  GET_ITER         
              414  FOR_ITER            604  'to 604'
              416  STORE_FAST               'schema_element_type'

 L. 937       418  LOAD_FAST                'app'
              420  LOAD_ATTR                schema
              422  LOAD_ATTR                sed
              424  LOAD_FAST                'schema_element_type'
              426  BINARY_SUBSCR    
              428  LOAD_METHOD              values
              430  CALL_METHOD_0         0  ''
              432  GET_ITER         
              434  FOR_ITER            600  'to 600'
              436  STORE_FAST               'se_obj'

 L. 938       438  SETUP_FINALLY       450  'to 450'

 L. 939       440  LOAD_FAST                'se_obj'
              442  LOAD_ATTR                oid
              444  STORE_FAST               'se_id'
              446  POP_BLOCK        
              448  JUMP_FORWARD        478  'to 478'
            450_0  COME_FROM_FINALLY   438  '438'

 L. 940       450  DUP_TOP          
              452  LOAD_GLOBAL              AttributeError
              454  COMPARE_OP               exception-match
          456_458  POP_JUMP_IF_FALSE   476  'to 476'
              460  POP_TOP          
              462  POP_TOP          
              464  POP_TOP          

 L. 941       466  LOAD_FAST                'se_obj'
              468  LOAD_ATTR                ruleid
              470  STORE_FAST               'se_id'
              472  POP_EXCEPT       
              474  JUMP_FORWARD        478  'to 478'
            476_0  COME_FROM           456  '456'
              476  END_FINALLY      
            478_0  COME_FROM           474  '474'
            478_1  COME_FROM           448  '448'

 L. 942       478  LOAD_FAST                'cmp_method'
              480  LOAD_FAST                'se_id'
              482  LOAD_METHOD              lower
              484  CALL_METHOD_0         0  ''
              486  LOAD_FAST                'oid_mv'
              488  CALL_FUNCTION_2       2  ''
          490_492  POP_JUMP_IF_FALSE   506  'to 506'

 L. 944       494  LOAD_FAST                'se_list'
              496  LOAD_METHOD              append
              498  LOAD_FAST                'se_obj'
              500  CALL_METHOD_1         1  ''
              502  POP_TOP          
              504  JUMP_BACK           434  'to 434'
            506_0  COME_FROM           490  '490'

 L. 947       506  SETUP_FINALLY       518  'to 518'

 L. 948       508  LOAD_FAST                'se_obj'
              510  LOAD_ATTR                names
              512  STORE_FAST               'se_names'
              514  POP_BLOCK        
              516  JUMP_FORWARD        546  'to 546'
            518_0  COME_FROM_FINALLY   506  '506'

 L. 949       518  DUP_TOP          
              520  LOAD_GLOBAL              AttributeError
              522  COMPARE_OP               exception-match
          524_526  POP_JUMP_IF_FALSE   544  'to 544'
              528  POP_TOP          
              530  POP_TOP          
              532  POP_TOP          

 L. 950       534  POP_EXCEPT       
          536_538  JUMP_BACK           434  'to 434'
              540  POP_EXCEPT       
              542  JUMP_FORWARD        546  'to 546'
            544_0  COME_FROM           524  '524'
              544  END_FINALLY      
            546_0  COME_FROM           542  '542'
            546_1  COME_FROM           516  '516'

 L. 951       546  LOAD_FAST                'se_names'
          548_550  JUMP_IF_TRUE_OR_POP   554  'to 554'
              552  BUILD_LIST_0          0 
            554_0  COME_FROM           548  '548'
              554  GET_ITER         
            556_0  COME_FROM           572  '572'
              556  FOR_ITER            596  'to 596'
              558  STORE_FAST               'se_name'

 L. 952       560  LOAD_FAST                'cmp_method'
              562  LOAD_FAST                'se_name'
              564  LOAD_METHOD              lower
              566  CALL_METHOD_0         0  ''
              568  LOAD_FAST                'oid_mv'
              570  CALL_FUNCTION_2       2  ''
          572_574  POP_JUMP_IF_FALSE   556  'to 556'

 L. 953       576  LOAD_FAST                'se_list'
              578  LOAD_METHOD              append
              580  LOAD_FAST                'se_obj'
              582  CALL_METHOD_1         1  ''
              584  POP_TOP          

 L. 954       586  POP_TOP          
          588_590  CONTINUE            434  'to 434'
          592_594  JUMP_BACK           556  'to 556'
          596_598  JUMP_BACK           434  'to 434'
          600_602  JUMP_BACK           414  'to 414'
            604_0  COME_FROM           398  '398'
            604_1  COME_FROM           300  '300'
            604_2  COME_FROM           286  '286'

 L. 956       604  LOAD_FAST                'se_list'
          606_608  POP_JUMP_IF_TRUE    660  'to 660'

 L. 958       610  LOAD_FAST                'app'
              612  LOAD_ATTR                simple_message

 L. 959       614  LOAD_STR                 ''

 L. 961       616  LOAD_STR                 '<h1>Schema elements</h1><p class="ErrorMessage">Name or OID not found in schema!</p><p>%s</p>'

 L. 964       618  LOAD_GLOBAL              oid_input_form
              620  LOAD_FAST                'app'
              622  LOAD_FAST                'oid'
              624  CALL_FUNCTION_2       2  ''

 L. 963       626  BUILD_TUPLE_1         1 

 L. 960       628  BINARY_MODULO    

 L. 966       630  LOAD_STR                 'Message'

 L. 967       632  LOAD_GLOBAL              web2ldap
              634  LOAD_ATTR                app
              636  LOAD_ATTR                gui
              638  LOAD_METHOD              main_menu
              640  LOAD_FAST                'app'
              642  CALL_METHOD_1         1  ''

 L. 968       644  LOAD_GLOBAL              schema_context_menu
              646  LOAD_FAST                'app'
              648  CALL_FUNCTION_1       1  ''

 L. 958       650  LOAD_CONST               ('title', 'message', 'main_div_id', 'main_menu_list', 'context_menu_list')
              652  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              654  POP_TOP          

 L. 970       656  LOAD_CONST               None
              658  RETURN_VALUE     
            660_0  COME_FROM           606  '606'

 L. 971       660  LOAD_GLOBAL              len
              662  LOAD_FAST                'se_list'
              664  CALL_FUNCTION_1       1  ''
              666  LOAD_CONST               1
              668  COMPARE_OP               >
          670_672  POP_JUMP_IF_FALSE   690  'to 690'

 L. 973       674  LOAD_GLOBAL              display_schema_elements
              676  LOAD_FAST                'app'
              678  LOAD_CONST               None
              680  LOAD_FAST                'se_list'
              682  CALL_FUNCTION_3       3  ''
              684  POP_TOP          

 L. 974       686  LOAD_CONST               None
              688  RETURN_VALUE     
            690_0  COME_FROM           670  '670'

 L. 977       690  LOAD_FAST                'se_list'
              692  LOAD_CONST               0
              694  BINARY_SUBSCR    
              696  STORE_FAST               'se_obj'

 L. 978       698  LOAD_FAST                'se_obj'
              700  LOAD_ATTR                __class__
              702  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              704  COMPARE_OP               not-in
          706_708  POP_JUMP_IF_FALSE   724  'to 724'

 L. 979       710  LOAD_GLOBAL              web2ldap
              712  LOAD_ATTR                app
              714  LOAD_ATTR                core
              716  LOAD_METHOD              ErrorExit
              718  LOAD_STR                 'No viewer for this type of schema element!'
              720  CALL_METHOD_1         1  ''
              722  RAISE_VARARGS_1       1  'exception instance'
            724_0  COME_FROM           706  '706'

 L. 980       724  LOAD_GLOBAL              SCHEMA_VIEWER_CLASS
              726  LOAD_FAST                'se_obj'
              728  LOAD_ATTR                __class__
              730  BINARY_SUBSCR    
              732  LOAD_FAST                'app'
              734  LOAD_FAST                'se_obj'
              736  CALL_FUNCTION_2       2  ''
              738  STORE_FAST               'schema_viewer'

 L. 981       740  LOAD_FAST                'schema_viewer'
              742  LOAD_METHOD              display
              744  CALL_METHOD_0         0  ''
              746  POP_TOP          

Parse error at or near `POP_EXCEPT' instruction at offset 540
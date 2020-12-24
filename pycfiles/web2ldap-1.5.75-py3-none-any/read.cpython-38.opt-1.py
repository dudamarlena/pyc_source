# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/read.py
# Compiled at: 2020-05-04 07:51:24
# Size of source mod 2**32: 23322 bytes
"""
web2ldap.app.read: Read single entry and output as HTML or vCard

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
from collections import UserDict
import ldap0.schema
from ldap0.cidict import CIDict
from ldap0.schema.models import SchemaElementOIDSet, AttributeType
from ldap0.schema.subentry import SubSchema
from ldap0.base import encode_entry_dict
from ldap0.dn import DNObj
import web2ldap.web.forms, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.gui, web2ldap.app.schema
from web2ldap.app.schema.syntaxes import syntax_registry
from web2ldap.msbase import GrabKeys
from web2ldap.app.schema.viewer import schema_anchor

class VCardEntry(UserDict):

    def __init__(self, app, entry, out_charset='utf-8'):
        self._app = app
        self._entry = entry
        self._out_charset = out_charset

    def __contains__(self, nameoroid):
        return self._entry.__contains__(nameoroid)

    def __getitem__(self, nameoroid):
        if web2ldap.app.schema.no_humanreadable_attr(self._app.schema, nameoroid):
            raise KeyError('Not human-readable attribute %r not usable in vCard' % (nameoroid,))
        value = self._entry.__getitem__(nameoroid)[0]
        return value.decode(self._app.ls.charset)


def get_vcard_template(app, object_classes):
    template_dict = CIDict(app.cfg_param('vcard_template', {}))
    current_oc_set = {s.lower().decode('ascii') for s in object_classes}
    template_oc = list(current_oc_set.intersection(template_dict.data.keys()))
    if not template_oc:
        return
    return web2ldap.app.gui.GetVariantFilename(template_dict[template_oc[0]], app.form.accept_language)


def generate_vcard(template_str, vcard_entry):
    res = []
    for line in template_str.decode('utf-8').split('\n'):
        try:
            res_line = line % vcard_entry
        except KeyError:
            pass
        else:
            res.append(res_line.strip())
    else:
        return '\r\n'.join(res)


class DisplayEntry(UserDict):

    def __init__(self, app, dn, schema, entry, sep_attr, commandbutton):
        if not isinstance(dn, str):
            raise AssertionError(TypeError("Argument 'dn' must be str, was %r" % dn))
        elif not isinstance(schema, SubSchema):
            raise AssertionError(TypeError('Expected schema to be instance of SubSchema, was %r' % schema))
        else:
            self._app = app
            self.schema = schema
            self._set_dn(dn)
            if isinstance(entry, dict):
                self.entry = ldap0.schema.models.Entry(schema, dn, entry)
            else:
                if isinstance(entry, ldap0.schema.models.Entry):
                    self.entry = entry
                else:
                    raise TypeError('Invalid type of argument entry, was %s.%s %r' % (
                     entry.__class__.__module__,
                     entry.__class__.__name__,
                     entry))
        self.soc = self.entry.get_structural_oc()
        self.invalid_attrs = set()
        self.sep_attr = sep_attr
        self.commandbutton = commandbutton

    def __getitem__(self, nameoroid):
        try:
            values = self.entry.__getitem__(nameoroid)
        except KeyError:
            return ''
        else:
            result = []
            syntax_se = syntax_registry.get_syntax(self.entry._s, nameoroid, self.soc)
            for i, value in enumerate(values):
                attr_instance = syntax_se(self._app, self.dn, self.entry._s, nameoroid, value, self.entry)
                try:
                    attr_value_html = attr_instance.display(valueindex=i,
                      commandbutton=(self.commandbutton))
                except UnicodeError:
                    attr_instance = web2ldap.app.schema.syntaxes.OctetString(self._app, self.dn, self.schema, nameoroid, value, self.entry)
                    attr_value_html = attr_instance.display(valueindex=i,
                      commandbutton=True)
                else:
                    try:
                        attr_instance.validate(value)
                    except web2ldap.app.schema.syntaxes.LDAPSyntaxValueError:
                        attr_value_html = '<s>%s</s>' % attr_value_html
                        self.invalid_attrs.add(nameoroid)
                    else:
                        result.append(attr_value_html)
            else:
                if self.sep_attr is not None:
                    value_sep = getattr(attr_instance, self.sep_attr)
                    return value_sep.join(result)
                return result

    def _get_rdn_dict(self, dn):
        assert isinstance(dn, str), TypeError("Argument 'dn' must be str, was %r" % dn)
        entry_rdn_dict = ldap0.schema.models.Entry(self.schema, dn, encode_entry_dict(DNObj.from_str(dn).rdn_attrs()))
        for attr_type, attr_values in list(entry_rdn_dict.items()):
            del entry_rdn_dict[attr_type]
            d = ldap0.cidict.CIDict()
            for attr_value in attr_values:
                assert isinstance(attr_value, bytes), TypeError("Var 'attr_value' must be bytes, was %r" % attr_value)
                d[attr_value] = None
            else:
                entry_rdn_dict[attr_type] = d

        else:
            return entry_rdn_dict

    def _set_dn(self, dn):
        self.dn = dn
        self.rdn_dict = self._get_rdn_dict(dn)

    def get_html_templates(self, cnf_key):
        read_template_dict = CIDict(self._app.cfg_param(cnf_key, {}))
        all_object_class_oid_set = self.entry.object_class_oid_set()
        object_class_oid_set = SchemaElementOIDSet(self.entry._s, ldap0.schema.models.ObjectClass, [])
        structural_oc = self.entry.get_structural_oc()
        if structural_oc:
            object_class_oid_set.add(structural_oc)
        for oc in all_object_class_oid_set:
            oc_obj = self.entry._s.get_obj(ldap0.schema.models.ObjectClass, oc)
            if oc_obj is None or oc_obj.kind != 0:
                object_class_oid_set.add(oc)
            template_oc = object_class_oid_set.intersection(read_template_dict.data.keys())
            return (template_oc.names, read_template_dict)

    def template_output--- This code section failed: ---

 L. 188         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              get_html_templates
                4  LOAD_FAST                'cnf_key'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'template_oc'
               12  STORE_FAST               'read_template_dict'

 L. 190        14  LOAD_GLOBAL              web2ldap
               16  LOAD_ATTR                app
               18  LOAD_ATTR                schema
               20  LOAD_METHOD              object_class_categories

 L. 191        22  LOAD_DEREF               'self'
               24  LOAD_ATTR                entry
               26  LOAD_ATTR                _s

 L. 192        28  LOAD_FAST                'template_oc'

 L. 190        30  CALL_METHOD_2         2  ''
               32  UNPACK_SEQUENCE_3     3 
               34  STORE_FAST               'structural_oc'
               36  STORE_FAST               'abstract_oc'
               38  STORE_FAST               'auxiliary_oc'

 L. 195        40  LOAD_GLOBAL              set
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'used_templates'

 L. 196        46  LOAD_GLOBAL              set
               48  CALL_FUNCTION_0       0  ''
               50  STORE_FAST               'displayed_attrs'

 L. 197        52  LOAD_CONST               None
               54  STORE_FAST               'error_msg'

 L. 198        56  LOAD_FAST                'structural_oc'
               58  LOAD_FAST                'abstract_oc'
               60  LOAD_FAST                'auxiliary_oc'
               62  BUILD_TUPLE_3         3 
               64  GET_ITER         
               66  FOR_ITER            314  'to 314'
               68  STORE_FAST               'oc_set'

 L. 199        70  LOAD_FAST                'oc_set'
               72  GET_ITER         
             74_0  COME_FROM           280  '280'
               74  FOR_ITER            312  'to 312'
               76  STORE_FAST               'oc'

 L. 200        78  SETUP_FINALLY        92  'to 92'

 L. 201        80  LOAD_FAST                'read_template_dict'
               82  LOAD_FAST                'oc'
               84  BINARY_SUBSCR    
               86  STORE_FAST               'read_template_filename'
               88  POP_BLOCK        
               90  JUMP_FORWARD        120  'to 120'
             92_0  COME_FROM_FINALLY    78  '78'

 L. 202        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   118  'to 118'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 203       106  LOAD_STR                 'Template file not found'
              108  STORE_FAST               'error_msg'

 L. 204       110  POP_EXCEPT       
              112  JUMP_BACK            74  'to 74'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            98  '98'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'
            120_1  COME_FROM            90  '90'

 L. 205       120  LOAD_GLOBAL              web2ldap
              122  LOAD_ATTR                app
              124  LOAD_ATTR                gui
              126  LOAD_METHOD              GetVariantFilename

 L. 206       128  LOAD_FAST                'read_template_filename'

 L. 207       130  LOAD_DEREF               'self'
              132  LOAD_ATTR                _app
              134  LOAD_ATTR                form
              136  LOAD_ATTR                accept_language

 L. 205       138  CALL_METHOD_2         2  ''
              140  STORE_FAST               'read_template_filename'

 L. 209       142  LOAD_FAST                'read_template_filename'
              144  LOAD_FAST                'used_templates'
              146  COMPARE_OP               in
              148  POP_JUMP_IF_FALSE   152  'to 152'

 L. 211       150  JUMP_BACK            74  'to 74'
            152_0  COME_FROM           148  '148'

 L. 212       152  LOAD_FAST                'used_templates'
              154  LOAD_METHOD              add
              156  LOAD_FAST                'read_template_filename'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 213       162  LOAD_FAST                'read_template_filename'
              164  POP_JUMP_IF_TRUE    172  'to 172'

 L. 214       166  LOAD_STR                 'Empty template filename'
              168  STORE_FAST               'error_msg'

 L. 215       170  JUMP_BACK            74  'to 74'
            172_0  COME_FROM           164  '164'

 L. 216       172  SETUP_FINALLY       214  'to 214'

 L. 217       174  LOAD_GLOBAL              open
              176  LOAD_FAST                'read_template_filename'
              178  LOAD_STR                 'rb'
              180  CALL_FUNCTION_2       2  ''
              182  SETUP_WITH          204  'to 204'
              184  STORE_FAST               'template_file'

 L. 218       186  LOAD_FAST                'template_file'
              188  LOAD_METHOD              read
              190  CALL_METHOD_0         0  ''
              192  LOAD_METHOD              decode
              194  LOAD_STR                 'utf-8'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'template_str'
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM_WITH      182  '182'
              204  WITH_CLEANUP_START
              206  WITH_CLEANUP_FINISH
              208  END_FINALLY      
              210  POP_BLOCK        
              212  JUMP_FORWARD        242  'to 242'
            214_0  COME_FROM_FINALLY   172  '172'

 L. 219       214  DUP_TOP          
              216  LOAD_GLOBAL              IOError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   240  'to 240'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 220       228  LOAD_STR                 'I/O error reading template file'
              230  STORE_FAST               'error_msg'

 L. 221       232  POP_EXCEPT       
              234  JUMP_BACK            74  'to 74'
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           220  '220'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           212  '212'

 L. 222       242  LOAD_CLOSURE             'self'
              244  BUILD_TUPLE_1         1 
              246  LOAD_SETCOMP             '<code_object <setcomp>>'
              248  LOAD_STR                 'DisplayEntry.template_output.<locals>.<setcomp>'
              250  MAKE_FUNCTION_8          'closure'

 L. 224       252  LOAD_GLOBAL              GrabKeys
              254  LOAD_FAST                'template_str'
              256  CALL_FUNCTION_1       1  ''
              258  CALL_FUNCTION_0       0  ''

 L. 222       260  GET_ITER         
              262  CALL_FUNCTION_1       1  ''
              264  STORE_FAST               'template_attr_oid_set'

 L. 226       266  LOAD_FAST                'display_duplicate_attrs'
          268_270  POP_JUMP_IF_TRUE    282  'to 282'
              272  LOAD_FAST                'displayed_attrs'
              274  LOAD_METHOD              intersection
              276  LOAD_FAST                'template_attr_oid_set'
              278  CALL_METHOD_1         1  ''
              280  POP_JUMP_IF_TRUE     74  'to 74'
            282_0  COME_FROM           268  '268'

 L. 227       282  LOAD_DEREF               'self'
              284  LOAD_ATTR                _app
              286  LOAD_ATTR                outf
              288  LOAD_METHOD              write
              290  LOAD_FAST                'template_str'
              292  LOAD_DEREF               'self'
              294  BINARY_MODULO    
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          

 L. 228       300  LOAD_FAST                'displayed_attrs'
              302  LOAD_METHOD              update
              304  LOAD_FAST                'template_attr_oid_set'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_BACK            74  'to 74'
              312  JUMP_BACK            66  'to 66'

 L. 229       314  LOAD_FAST                'error_msg'
          316_318  POP_JUMP_IF_FALSE   342  'to 342'

 L. 230       320  LOAD_DEREF               'self'
              322  LOAD_ATTR                _app
              324  LOAD_ATTR                outf
              326  LOAD_METHOD              write

 L. 231       328  LOAD_STR                 '<p class="ErrorMessage">%s! (object class <var>%r</var>)</p>'

 L. 232       330  LOAD_FAST                'error_msg'

 L. 233       332  LOAD_FAST                'oc'

 L. 231       334  BUILD_TUPLE_2         2 
              336  BINARY_MODULO    

 L. 230       338  CALL_METHOD_1         1  ''
              340  POP_TOP          
            342_0  COME_FROM           316  '316'

 L. 236       342  LOAD_FAST                'displayed_attrs'
              344  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 114


def display_attribute_table(app, entry, attrs, comment):
    """
    Send a table of attributes to outf
    """
    show_attrs = [a for a in attrs if a in entry.entry]
    if not show_attrs:
        return
    show_attrs.sort(key=(str.lower))
    read_expandattr_set = {at.strip().lower() for at in app.form.getInputValue('read_expandattr', []) if at if at}
    if '*' in read_expandattr_set:
        read_tablemaxcount_dict = {}
    else:
        read_tablemaxcount_dict = ldap0.cidict.CIDict(app.cfg_param('read_tablemaxcount', {}))
        for at in read_expandattr_set:
            try:
                del read_tablemaxcount_dict[at]
            except KeyError:
                pass

        else:
            app.outf.write('<h2>%s</h2>\n<table class="ReadAttrTable">' % comment)
            entry.sep = None
            for attr_type_name in show_attrs:
                attr_type_anchor_id = 'readattr_%s' % app.form.utf2display(attr_type_name)
                attr_type_str = schema_anchor(app,
                  attr_type_name,
                  (ldap0.schema.models.AttributeType),
                  name_template='<var>{name}</var>\n{anchor}',
                  link_text='&raquo;')
                attr_value_disp_list = entry[attr_type_name] or [
                 '<strong>&lt;Empty attribute value list!&gt;</strong>']
                attr_value_count = len(attr_value_disp_list)
                dt_list = [
                 '<span id="%s">%s</span>\n' % (attr_type_anchor_id, attr_type_str)]
                read_tablemaxcount = min(read_tablemaxcount_dict.get(attr_type_name, attr_value_count), attr_value_count)
                if attr_value_count > 1:
                    if attr_value_count > read_tablemaxcount:
                        dt_list.append(app.anchor('read',
                          ('(%d of %d values)' % (read_tablemaxcount, attr_value_count)),
                          app.form.allInputFields(fields=[
                         (
                          'read_expandattr', attr_type_name)]),
                          anchor_id=attr_type_anchor_id))
                    else:
                        dt_list.append('(%d values)' % attr_value_count)
                if web2ldap.app.schema.no_humanreadable_attr(app.schema, attr_type_name):
                    if not web2ldap.app.schema.no_userapp_attr(app.schema, attr_type_name):
                        dt_list.append(app.anchor('delete', 'Delete', [
                         (
                          'dn', app.dn), ('delete_attr', attr_type_name)]))
                    dt_list.append(app.anchor('read', 'Save to disk', [
                     (
                      'dn', app.dn),
                     (
                      'read_attr', attr_type_name),
                     ('read_attrmimetype', 'application/octet-stream'),
                     ('read_attrindex', '0')]))
                dt_str = '<br>'.join(dt_list)
                app.outf.write('<tr class="ReadAttrTableRow"><td class="ReadAttrType" rowspan="%d">\n%s\n</td>\n<td class="ReadAttrValue">%s</td></tr>' % (
                 read_tablemaxcount,
                 dt_str,
                 attr_value_disp_list[0]))
                if read_tablemaxcount >= 2:
                    for i in range(1, read_tablemaxcount):
                        app.outf.write('<tr class="ReadAttrTableRow">\n<td class="ReadAttrValue">%s</td></tr>\n' % (
                         attr_value_disp_list[i],))
                    else:
                        app.outf.write('</table>\n')


def w2l_read(app):
    read_output = app.form.getInputValue('read_output', ['template'])[0]
    filterstr = app.form.getInputValue('filterstr', ['(objectClass=*)'])[0]
    read_nocache = int(app.form.getInputValue('read_nocache', ['0'])[0] or '0')
    wanted_attr_set = SchemaElementOIDSet(app.schema, ldap0.schema.models.AttributeType, app.form.getInputValue('read_attr', app.ldap_url.attrs or []))
    wanted_attrs = wanted_attr_set.names
    search_attrs = app.form.getInputValue('search_attrs', [''])[0]
    if search_attrs:
        wanted_attrs.extend([a.strip() for a in search_attrs.split(',')])
    elif (wanted_attrs or app.ls).supportsAllOpAttr:
        wanted_attrs = [
         '*', '+']
    else:
        wanted_attrs = []
    search_result = app.ls.l.read_s((app.dn),
      attrlist=wanted_attrs,
      filterstr=filterstr,
      cache_ttl=(None if read_nocache else -1.0))
    if not search_result:
        raise web2ldap.app.core.ErrorExit('Empty search result.')
    entry = ldap0.schema.models.Entry(app.schema, app.dn, search_result.entry_as)
    requested_attrs = SchemaElementOIDSet(app.schema, AttributeType, app.cfg_param('requested_attrs', []))
    if not wanted_attrs:
        if requested_attrs:
            try:
                search_result = app.ls.l.read_s((app.dn),
                  filterstr=filterstr,
                  attrlist=(requested_attrs.names),
                  cache_ttl=(None if read_nocache else -1.0))
            except (
             ldap0.NO_SUCH_ATTRIBUTE,
             ldap0.INSUFFICIENT_ACCESS):
                pass

            if search_result:
                entry.update(search_result.entry_as)
    display_entry = DisplayEntry(app, app.dn, app.schema, entry, 'readSep', 1)
    if wanted_attrs:
        if len(wanted_attrs) == 1:
            if wanted_attrs[0] not in {b'*', b'+'}:
                attr_type = wanted_attrs[0]
                if attr_type not in entry:
                    if attr_type + ';binary' in entry:
                        attr_type = attr_type + ';binary'
                    else:
                        raise web2ldap.app.core.ErrorExit('Attribute <em>%s</em> not in entry.' % app.form.utf2display(attr_type))
                read_attrindex = int(app.form.getInputValue('read_attrindex', ['0'])[0])
                syntax_se = syntax_registry.get_syntax(app.schema, attr_type, entry.get_structural_oc())
                attr_instance = syntax_se(app, app.dn, app.schema, attr_type, None, entry)
                web2ldap.app.gui.Header(app,
                  (app.form.getInputValue('read_attrmimetype', [
                 attr_instance.mimeType])[0]),
                  (app.form.accept_charset),
                  more_headers=[
                 (
                  'Content-Disposition',
                  'inline; filename=web2ldap-export.%s' % (attr_instance.fileExt,))])
                app.outf.write_bytes(entry[attr_type][read_attrindex])
                return
            if read_output in {'table', 'template'}:
                web2ldap.app.gui.top_section(app,
                  '',
                  (web2ldap.app.gui.main_menu(app)),
                  context_menu_list=web2ldap.app.gui.ContextMenuSingleEntry(app,
                  vcard_link=(get_vcard_template(app, entry.get('objectClass', [])) is not None),
                  dds_link=(b'dynamicObject' in entry.get('objectClass', [])),
                  entry_uuid=(entry['entryUUID'][0].decode(app.ls.charset) if 'entryUUID' in entry else None)))
                export_field = web2ldap.app.form.ExportFormatSelect()
                export_field.charset = app.form.accept_charset
                app.outf.write('%s\n' % (
                 app.form_html('search',
                   'Export', 'GET', [
                  (
                   'dn', app.dn),
                  ('scope', '0'),
                  ('filterstr', '(objectClass=*)'),
                  ('search_resnumber', '0'),
                  (
                   'search_attrs', ','.join(map(str, wanted_attrs or [])))],
                   extrastr=('\n'.join((
                  export_field.input_html(),
                  'Incl. op. attrs.:',
                  web2ldap.app.form.InclOpAttrsCheckbox().input_html()))),
                   target='web2ldapexport'),))
                displayed_attrs = set()
                if read_output == 'template':
                    displayed_attrs.update(display_entry.template_output('read_template'))
                h1_display_name = displayed_attrs or app.dn or 'Root DSE'
            else:
                h1_display_name = entry.get('displayName', entry.get('cn', [b'']))[0].decode(app.ls.charset) or str(app.dn_obj.slice(0, 1))
        else:
            app.outf.write('<h1>{0}</h1>\n<p class="EntryDN">{1}</p>\n'.format(app.form.utf2display(h1_display_name), display_entry['entryDN']))
        required_attrs_dict, allowed_attrs_dict = entry.attribute_types(raise_keyerror=0)
        required_attrs = []
        allowed_attrs = []
        collective_attrs = []
        nomatching_attrs = []
        for a in entry.keys():
            at_se = app.schema.get_obj(ldap0.schema.models.AttributeType, a, None)
            if at_se is None:
                nomatching_attrs.append(a)
            else:
                at_oid = at_se.oid
                if at_oid in displayed_attrs:
                    pass
                elif at_oid in required_attrs_dict:
                    required_attrs.append(a)
                elif at_oid in allowed_attrs_dict:
                    allowed_attrs.append(a)
                elif at_se.collective:
                    collective_attrs.append(a)
                else:
                    nomatching_attrs.append(a)
        else:
            display_entry.sep_attr = None
            display_attribute_table(app, display_entry, required_attrs, 'Required Attributes')
            display_attribute_table(app, display_entry, allowed_attrs, 'Allowed Attributes')
            display_attribute_table(app, display_entry, collective_attrs, 'Collective Attributes')
            display_attribute_table(app, display_entry, nomatching_attrs, 'Various Attributes')
            display_entry.sep_attr = 'readSep'
            app.outf.write('%s\n%s\n%s<p>\n%s\n\n            <input type=submit value="Request"> attributes:\n            <input name="search_attrs" value="%s" size="40" maxlength="255">\n            </p></form>\n            ' % (
             app.begin_form('read', 'GET'),
             app.form.hiddenFieldHTML('read_nocache', '1', ''),
             app.form.hiddenFieldHTML('dn', app.dn, ''),
             app.form.hiddenFieldHTML('read_output', read_output, ''),
             ','.join([app.form.utf2display(at, sp_entity='  ') for at in wanted_attrs or {False:[
               '*'], 
              True:['*', '+']}[app.ls.supportsAllOpAttr]])))
            web2ldap.app.gui.footer(app)

    else:
        pass
    if read_output == 'vcard':
        vcard_template_filename = get_vcard_template(app, entry.get('objectClass', []))
        if not vcard_template_filename:
            raise web2ldap.app.core.ErrorExit('No vCard template file found for object class(es) of this entry.')
        try:
            template_str = open(vcard_template_filename, 'rb').read()
        except IOError:
            raise web2ldap.app.core.ErrorExit('I/O error during reading vCard template file!')
        else:
            vcard_filename = 'web2ldap-vcard'
            for vcard_name_attr in ('displayName', 'cn', 'o'):
                try:
                    vcard_filename = entry[vcard_name_attr][0].decode(app.ls.charset)
                except (KeyError, IndexError):
                    pass
                else:
                    break
            else:
                entry['dn'] = [
                 app.ldap_dn]
                display_entry = VCardEntry(app, entry)
                web2ldap.app.gui.Header(app,
                  'text/x-vcard',
                  (app.form.accept_charset),
                  more_headers=[
                 (
                  'Content-Disposition',
                  'inline; filename={0}.vcf'.format(vcard_filename))])
                app.outf.write(generate_vcard(template_str, display_entry))
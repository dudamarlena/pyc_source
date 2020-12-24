# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/addmodifyform.py
# Compiled at: 2020-03-20 20:49:32
# Size of source mod 2**32: 53429 bytes
"""
web2ldap.app.addmodifyform: input form for adding and modifying an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
from io import BytesIO
import ldap0, ldap0.ldif, ldap0.schema
from ldap0.dn import DNObj
from ldap0.base import decode_list
from ldap0.schema.models import AttributeType, ObjectClass, DITStructureRule, DITContentRule
import web2ldapcnf, web2ldap.web
from web2ldap.web import escape_html
import web2ldap.ldapsession, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.form, web2ldap.app.gui, web2ldap.app.read, web2ldap.app.schema
from web2ldap.app.schema.viewer import schema_anchors
from web2ldap.app.schema.syntaxes import syntax_registry
from web2ldap.msbase import GrabKeys
from web2ldap.app.schema.syntaxes import LDAPSyntaxValueError
from web2ldap.app.schema.viewer import schema_anchor
H1_MSG = {'add':'Add new entry', 
 'modify':'Modify entry'}
INPUT_FORM_BEGIN_TMPL = '\n\n  <h1>{text_heading}</h1>\n\n  {text_msg}\n\n  {text_supentry}\n\n  {form_begin}\n\n  {field_dn}\n  {field_currentformtype}\n\n  <p>\n\n    <input\n      type="submit"\n      value="Save"\n    >\n\n    Change input form:\n\n    <button\n      type="submit"\n      name="in_ft"\n      value="Template"\n      title="Switch to HTML template input form"\n    >\n      Template\n    </button>\n\n    <button\n      type="submit"\n      name="in_ft"\n      value="Table"\n      title="Switch to attribute table input form"\n    >\n      Table\n    </button>\n\n    <button\n      type="submit"\n      name="in_ft"\n      value="LDIF"\n      title="Switch to multi-line LDIF input form"\n    >\n      LDIF\n    </button>\n\n    Change&nbsp;Object&nbsp;\n    <button\n      type="submit"\n      name="in_ft"\n      title="Switch to object class select form"\n      value="OC">\n      Classes\n    </button>\n\n  </p>\n'
INPUT_FORM_LDIF_TMPL = '\n<fieldset>\n  <legend>Raw LDIF data</legend>\n  <textarea name="in_ldif" rows="50" cols="80" wrap="off">{value_ldif}</textarea>\n  <p>\n    Notes:\n  </p>\n  <ul>\n    <li>Lines containing "dn:" will be ignored</li>\n    <li>Only the first entry (until first empty line) will be accepted</li>\n    <li>Maximum length is set to {value_ldifmaxbytes} bytes</li>\n    <li>Allowed URL schemes: {text_ldifurlschemes}</li>\n  </ul>\n</fieldset>\n'

def get_entry_input(app):
    in_attrtype_list = app.form.getInputValue('in_at', [])
    in_value_list = app.form.getInputValue('in_av', [])
    if not len(in_attrtype_list) == len(in_value_list):
        raise web2ldap.app.core.ErrorExit('Different count of attribute types and values input.')
    entry = ldap0.schema.models.Entry(app.schema, app.dn, {})
    for i, attr_type in enumerate(in_attrtype_list):
        attr_value = in_value_list[i]
        if isinstance(attr_value, str):
            attr_value = app.ls.uc_encode(attr_value)[0]
        try:
            entry[attr_type].append(attr_value)
        except KeyError:
            entry[attr_type] = [
             attr_value]

    else:
        oc_attr_instance = syntax_registry.get_at(app,
          (app.dn), (app.schema), 'objectClass',
          None, entry=entry)
        entry['objectClass'] = [oc_attr_instance.sanitize(oc) for oc in entry.get('objectClass', [])]
        for attr_type, in_values in entry.items():
            if attr_type == '2.5.4.0':
                pass
            else:
                attr_values = []
                for in_value in in_values:
                    attr_instance = syntax_registry.get_at(app,
                      (app.dn), (app.schema), attr_type,
                      None, entry=entry)
                    assert isinstance(in_value, bytes), TypeError('Expected in_value to be bytes, got %r' % (in_value,))
                    attr_value = attr_instance.sanitize(in_value)
                    assert isinstance(attr_value, bytes), TypeError('Expected %s.sanitize(%r) to return bytes, got %r' % (
                     attr_instance.__class__.__name__,
                     in_value,
                     attr_value))
                    attr_values.append(attr_value)
                else:
                    entry[attr_type] = attr_values

    try:
        in_ldif = app.form.field['in_ldif'].getLDIFRecords()
    except ValueError as e:
        try:
            raise web2ldap.app.core.ErrorExit('LDIF parsing error: %s' % app.form.utf2display(str(e)))
        finally:
            e = None
            del e

    else:
        if in_ldif:
            entry.update(in_ldif[0][1])
        iteration_count = 7
        entry_changed = True
        if entry_changed and iteration_count:
            iteration_count -= 1
            entry_changed = False
            for attr_type, attr_values in entry.items():
                attr_instance = syntax_registry.get_at(app,
                  (app.dn), (app.schema), attr_type,
                  None, entry=entry)
                new_values = attr_instance.transmute(attr_values)
                if attr_values:
                    assert isinstance(attr_values[0], bytes), TypeError('Expected %s.transmute(%r) to return list of bytes, got %r' % (
                     attr_instance.__class__.__name__,
                     attr_values,
                     new_values))
                entry_changed = entry_changed or new_values != attr_values
                entry[attr_type] = new_values
            else:
                invalid_attrs = {}
                for attr_type, attr_values in list(entry.items()):
                    attr_values = entry[attr_type]

            if not attr_values:
                del entry[attr_type]
        else:
            attr_instance = syntax_registry.get_at(app,
              (app.dn), (app.schema), attr_type,
              None, entry=entry)
            for attr_index, attr_value in enumerate(attr_values):
                if attr_value:
                    try:
                        attr_instance.validate(attr_value)
                    except LDAPSyntaxValueError:
                        try:
                            invalid_attrs[attr_type].append(attr_index)
                        except KeyError:
                            invalid_attrs[attr_type] = [
                             attr_index]

            else:
                return (
                 entry, invalid_attrs)


class InputFormEntry(web2ldap.app.read.DisplayEntry):

    def __init__(self, app, dn, schema, entry, writeable_attr_oids, existing_object_classes=None, invalid_attrs=None):
        assert isinstance(dn, str), TypeError("Argument 'dn' must be str, was %r" % dn)
        web2ldap.app.read.DisplayEntry.__init__(self, app, dn, schema, entry, 'fieldSep', False)
        self.existing_object_classes = existing_object_classes
        self.writeable_attr_oids = writeable_attr_oids
        self.invalid_attrs = invalid_attrs or {}
        new_object_classes = set(list(self.entry.object_class_oid_set())) - set([self.entry._s.get_oid(ObjectClass, oc_name) for oc_name in existing_object_classes or []])
        new_attribute_types = self.entry._s.attribute_types(new_object_classes,
          raise_keyerror=0,
          ignore_dit_content_rule=(self._app.ls.relax_rules))
        old_attribute_types = self.entry._s.attribute_types((existing_object_classes or []),
          raise_keyerror=0,
          ignore_dit_content_rule=(self._app.ls.relax_rules))
        self.new_attribute_types_oids = set()
        self.new_attribute_types_oids.update(new_attribute_types[0].keys())
        self.new_attribute_types_oids.update(new_attribute_types[1].keys())
        for at_oid in list(old_attribute_types[0].keys()) + list(old_attribute_types[1].keys()):
            try:
                self.new_attribute_types_oids.remove(at_oid)
            except KeyError:
                pass

    def _reset_input_counters(self):
        self.attr_counter = 0
        self.row_counter = 0

    def __getitem__--- This code section failed: ---

 L. 298         0  LOAD_FAST                'self'
                2  LOAD_ATTR                entry
                4  LOAD_METHOD              name2key
                6  LOAD_FAST                'nameoroid'
                8  CALL_METHOD_1         1  ''
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'oid'

 L. 299        16  LOAD_FAST                'self'
               18  LOAD_ATTR                entry
               20  LOAD_ATTR                _s
               22  LOAD_METHOD              get_obj
               24  LOAD_GLOBAL              AttributeType
               26  LOAD_FAST                'nameoroid'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'nameoroid_se'

 L. 300        32  LOAD_GLOBAL              web2ldap
               34  LOAD_ATTR                app
               36  LOAD_ATTR                schema
               38  LOAD_ATTR                syntaxes
               40  LOAD_ATTR                syntax_registry
               42  LOAD_METHOD              get_syntax

 L. 301        44  LOAD_FAST                'self'
               46  LOAD_ATTR                entry
               48  LOAD_ATTR                _s

 L. 302        50  LOAD_FAST                'nameoroid'

 L. 303        52  LOAD_FAST                'self'
               54  LOAD_ATTR                soc

 L. 300        56  CALL_METHOD_3         3  ''
               58  STORE_FAST               'syntax_class'

 L. 305        60  SETUP_FINALLY        78  'to 78'

 L. 306        62  LOAD_FAST                'self'
               64  LOAD_ATTR                entry
               66  LOAD_METHOD              __getitem__
               68  LOAD_FAST                'nameoroid'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'attr_values'
               74  POP_BLOCK        
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM_FINALLY    60  '60'

 L. 307        78  DUP_TOP          
               80  LOAD_GLOBAL              KeyError
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   100  'to 100'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 308        92  BUILD_LIST_0          0 
               94  STORE_FAST               'attr_values'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            84  '84'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            76  '76'

 L. 310       102  LOAD_FAST                'attr_values'
              104  JUMP_IF_TRUE_OR_POP   110  'to 110'
              106  LOAD_CONST               None
              108  BUILD_LIST_1          1 
            110_0  COME_FROM           104  '104'
              110  STORE_FAST               'attr_values'

 L. 312       112  BUILD_LIST_0          0 
              114  STORE_FAST               'result'

 L. 315       116  LOAD_FAST                'syntax_class'
              118  LOAD_ATTR                editable
              120  POP_JUMP_IF_TRUE    128  'to 128'

 L. 316       122  LOAD_CONST               b''
              124  BUILD_LIST_1          1 
              126  STORE_FAST               'attr_values'
            128_0  COME_FROM           120  '120'

 L. 318       128  LOAD_FAST                'syntax_class'

 L. 319       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _app

 L. 319       134  LOAD_FAST                'self'
              136  LOAD_ATTR                dn

 L. 319       138  LOAD_FAST                'self'
              140  LOAD_ATTR                entry
              142  LOAD_ATTR                _s

 L. 319       144  LOAD_FAST                'nameoroid'

 L. 319       146  LOAD_CONST               None

 L. 319       148  LOAD_FAST                'self'
              150  LOAD_ATTR                entry

 L. 318       152  CALL_FUNCTION_6       6  ''
              154  STORE_FAST               'attr_inst'

 L. 321       156  LOAD_GLOBAL              set
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                invalid_attrs
              162  LOAD_METHOD              get
              164  LOAD_FAST                'nameoroid'
              166  BUILD_LIST_0          0 
              168  CALL_METHOD_2         2  ''
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'invalid_attr_indexes'

 L. 323       174  LOAD_GLOBAL              enumerate
              176  LOAD_FAST                'attr_values'
              178  CALL_FUNCTION_1       1  ''
              180  GET_ITER         
          182_184  FOR_ITER            884  'to 884'
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'attr_index'
              190  STORE_FAST               'attr_value'

 L. 325       192  LOAD_FAST                'syntax_class'

 L. 326       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _app

 L. 326       198  LOAD_FAST                'self'
              200  LOAD_ATTR                dn

 L. 326       202  LOAD_FAST                'self'
              204  LOAD_ATTR                entry
              206  LOAD_ATTR                _s

 L. 326       208  LOAD_FAST                'nameoroid'

 L. 326       210  LOAD_FAST                'attr_value'

 L. 326       212  LOAD_FAST                'self'
              214  LOAD_ATTR                entry

 L. 325       216  CALL_FUNCTION_6       6  ''
              218  STORE_FAST               'attr_inst'

 L. 328       220  LOAD_FAST                'attr_index'
              222  LOAD_FAST                'invalid_attr_indexes'
              224  COMPARE_OP               in
              226  STORE_FAST               'highlight_invalid'

 L. 332       228  LOAD_FAST                'oid'
              230  LOAD_STR                 '2.5.4.0'
              232  COMPARE_OP               ==

 L. 330   234_236  POP_JUMP_IF_TRUE    360  'to 360'

 L. 335       238  LOAD_FAST                'oid'
              240  LOAD_STR                 '2.5.21.9'
              242  COMPARE_OP               ==

 L. 330   244_246  POP_JUMP_IF_TRUE    360  'to 360'

 L. 338       248  LOAD_FAST                'self'
              250  LOAD_ATTR                writeable_attr_oids
              252  LOAD_CONST               None
              254  COMPARE_OP               is-not

 L. 330   256_258  POP_JUMP_IF_FALSE   284  'to 284'

 L. 339       260  LOAD_FAST                'oid'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                writeable_attr_oids
              266  COMPARE_OP               not-in

 L. 330   268_270  POP_JUMP_IF_FALSE   284  'to 284'

 L. 340       272  LOAD_FAST                'oid'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                new_attribute_types_oids
              278  COMPARE_OP               not-in

 L. 330   280_282  POP_JUMP_IF_TRUE    360  'to 360'
            284_0  COME_FROM           268  '268'
            284_1  COME_FROM           256  '256'

 L. 343       284  LOAD_FAST                'self'
              286  LOAD_ATTR                existing_object_classes

 L. 330   288_290  POP_JUMP_IF_FALSE   326  'to 326'

 L. 344       292  LOAD_FAST                'attr_value'

 L. 330   294_296  POP_JUMP_IF_FALSE   326  'to 326'

 L. 345       298  LOAD_FAST                'nameoroid'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                rdn_dict
              304  COMPARE_OP               in

 L. 330   306_308  POP_JUMP_IF_FALSE   326  'to 326'

 L. 346       310  LOAD_FAST                'attr_value'
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                rdn_dict
              316  LOAD_FAST                'nameoroid'
              318  BINARY_SUBSCR    
              320  COMPARE_OP               in

 L. 330   322_324  POP_JUMP_IF_TRUE    360  'to 360'
            326_0  COME_FROM           306  '306'
            326_1  COME_FROM           294  '294'
            326_2  COME_FROM           288  '288'

 L. 349       326  LOAD_FAST                'self'
              328  LOAD_ATTR                _app
              330  LOAD_ATTR                ls
              332  LOAD_ATTR                relax_rules

 L. 330   334_336  POP_JUMP_IF_TRUE    518  'to 518'

 L. 350       338  LOAD_GLOBAL              web2ldap
              340  LOAD_ATTR                app
              342  LOAD_ATTR                schema
              344  LOAD_METHOD              no_userapp_attr
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                entry
              350  LOAD_ATTR                _s
              352  LOAD_FAST                'oid'
              354  CALL_METHOD_2         2  ''

 L. 330   356_358  POP_JUMP_IF_FALSE   518  'to 518'
            360_0  COME_FROM           322  '322'
            360_1  COME_FROM           280  '280'
            360_2  COME_FROM           244  '244'
            360_3  COME_FROM           234  '234'

 L. 352       360  LOAD_FAST                'result'
              362  LOAD_METHOD              append
              364  LOAD_STR                 '\n'
              366  LOAD_METHOD              join

 L. 353       368  LOAD_STR                 '<span class="InvalidInput">'
              370  LOAD_FAST                'highlight_invalid'
              372  BINARY_MULTIPLY  

 L. 354       374  LOAD_FAST                'self'
              376  LOAD_ATTR                _app
              378  LOAD_ATTR                form
              380  LOAD_METHOD              hiddenFieldHTML
              382  LOAD_STR                 'in_at'
              384  LOAD_FAST                'nameoroid'
              386  LOAD_STR                 ''
              388  CALL_METHOD_3         3  ''

 L. 355       390  LOAD_GLOBAL              web2ldap
              392  LOAD_ATTR                app
              394  LOAD_ATTR                gui
              396  LOAD_ATTR                HIDDEN_FIELD
              398  LOAD_STR                 'in_avi'
              400  LOAD_GLOBAL              str
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                attr_counter
              406  CALL_FUNCTION_1       1  ''
              408  LOAD_STR                 ''
              410  BUILD_TUPLE_3         3 
              412  BINARY_MODULO    

 L. 356       414  LOAD_GLOBAL              web2ldap
              416  LOAD_ATTR                app
              418  LOAD_ATTR                gui
              420  LOAD_ATTR                HIDDEN_FIELD

 L. 357       422  LOAD_STR                 'in_av'

 L. 358       424  LOAD_FAST                'self'
              426  LOAD_ATTR                _app
              428  LOAD_ATTR                form
              430  LOAD_ATTR                utf2display
              432  LOAD_FAST                'attr_inst'
              434  LOAD_METHOD              formValue
              436  CALL_METHOD_0         0  ''
              438  LOAD_STR                 '  '
              440  LOAD_CONST               ('sp_entity',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 359       444  LOAD_FAST                'self'
              446  LOAD_ATTR                _app
              448  LOAD_ATTR                form
              450  LOAD_ATTR                utf2display
              452  LOAD_FAST                'attr_inst'
              454  LOAD_METHOD              formValue
              456  CALL_METHOD_0         0  ''
              458  LOAD_STR                 '&nbsp;&nbsp;'
              460  LOAD_CONST               ('sp_entity',)
              462  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 356       464  BUILD_TUPLE_3         3 
              466  BINARY_MODULO    

 L. 361       468  LOAD_FAST                'attr_inst'
              470  LOAD_METHOD              valueButton
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                _app
              476  LOAD_ATTR                command
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                row_counter
              482  LOAD_STR                 '+'
              484  CALL_METHOD_3         3  ''

 L. 362       486  LOAD_STR                 '</span>'
              488  LOAD_FAST                'highlight_invalid'
              490  BINARY_MULTIPLY  

 L. 352       492  BUILD_TUPLE_6         6 
              494  CALL_METHOD_1         1  ''
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          

 L. 364       500  LOAD_FAST                'self'
              502  DUP_TOP          
              504  LOAD_ATTR                row_counter
              506  LOAD_CONST               1
              508  INPLACE_ADD      
              510  ROT_TWO          
              512  STORE_ATTR               row_counter
          514_516  JUMP_FORWARD        868  'to 868'
            518_0  COME_FROM           356  '356'
            518_1  COME_FROM           334  '334'

 L. 367       518  LOAD_STR                 ''
              520  STORE_FAST               'attr_title'

 L. 368       522  BUILD_LIST_0          0 
              524  STORE_FAST               'attr_type_tags'

 L. 369       526  LOAD_GLOBAL              str
              528  LOAD_FAST                'nameoroid'
              530  CALL_FUNCTION_1       1  ''
              532  LOAD_METHOD              split
              534  LOAD_STR                 ';'
              536  CALL_METHOD_1         1  ''
              538  LOAD_CONST               0
              540  BINARY_SUBSCR    
              542  STORE_FAST               'attr_type_name'

 L. 370       544  LOAD_FAST                'nameoroid_se'
          546_548  POP_JUMP_IF_FALSE   670  'to 670'

 L. 371       550  LOAD_FAST                'nameoroid_se'
              552  LOAD_ATTR                names
          554_556  JUMP_IF_TRUE_OR_POP   564  'to 564'
              558  LOAD_FAST                'nameoroid_se'
              560  LOAD_ATTR                oid
              562  BUILD_LIST_1          1 
            564_0  COME_FROM           554  '554'
              564  LOAD_CONST               0
              566  BINARY_SUBSCR    
              568  STORE_FAST               'attr_type_name'

 L. 372       570  SETUP_FINALLY       588  'to 588'

 L. 373       572  LOAD_FAST                'nameoroid_se'
              574  LOAD_ATTR                desc
          576_578  JUMP_IF_TRUE_OR_POP   582  'to 582'
              580  LOAD_STR                 ''
            582_0  COME_FROM           576  '576'
              582  STORE_FAST               'attr_title'
              584  POP_BLOCK        
              586  JUMP_FORWARD        614  'to 614'
            588_0  COME_FROM_FINALLY   570  '570'

 L. 374       588  DUP_TOP          
              590  LOAD_GLOBAL              UnicodeError
              592  COMPARE_OP               exception-match
          594_596  POP_JUMP_IF_FALSE   612  'to 612'
              598  POP_TOP          
              600  POP_TOP          
              602  POP_TOP          

 L. 376       604  LOAD_STR                 ''
              606  STORE_FAST               'attr_title'
              608  POP_EXCEPT       
              610  JUMP_FORWARD        614  'to 614'
            612_0  COME_FROM           594  '594'
              612  END_FINALLY      
            614_0  COME_FROM           610  '610'
            614_1  COME_FROM           586  '586'

 L. 379       614  LOAD_FAST                'nameoroid'
              616  LOAD_METHOD              endswith
              618  LOAD_STR                 ';binary'
              620  CALL_METHOD_1         1  ''

 L. 378   622_624  POP_JUMP_IF_TRUE    660  'to 660'

 L. 380       626  LOAD_FAST                'oid'
              628  LOAD_GLOBAL              web2ldap
              630  LOAD_ATTR                app
              632  LOAD_ATTR                schema
              634  LOAD_ATTR                NEEDS_BINARY_TAG
              636  COMPARE_OP               in

 L. 378   638_640  POP_JUMP_IF_TRUE    660  'to 660'

 L. 381       642  LOAD_FAST                'nameoroid_se'
              644  LOAD_ATTR                syntax
              646  LOAD_GLOBAL              web2ldap
              648  LOAD_ATTR                app
              650  LOAD_ATTR                schema
              652  LOAD_ATTR                NEEDS_BINARY_TAG
              654  COMPARE_OP               in

 L. 378   656_658  POP_JUMP_IF_FALSE   670  'to 670'
            660_0  COME_FROM           638  '638'
            660_1  COME_FROM           622  '622'

 L. 383       660  LOAD_FAST                'attr_type_tags'
              662  LOAD_METHOD              append
              664  LOAD_STR                 'binary'
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          
            670_0  COME_FROM           656  '656'
            670_1  COME_FROM           546  '546'

 L. 384       670  LOAD_FAST                'attr_inst'
              672  LOAD_METHOD              formFields
              674  CALL_METHOD_0         0  ''
              676  STORE_FAST               'input_fields'

 L. 385       678  LOAD_FAST                'input_fields'
              680  GET_ITER         
              682  FOR_ITER            868  'to 868'
              684  STORE_FAST               'input_field'

 L. 386       686  LOAD_STR                 'in_av'
              688  LOAD_FAST                'input_field'
              690  STORE_ATTR               name

 L. 387       692  LOAD_FAST                'self'
              694  LOAD_ATTR                _app
              696  LOAD_ATTR                form
              698  LOAD_ATTR                accept_charset
              700  LOAD_FAST                'input_field'
              702  STORE_ATTR               charset

 L. 388       704  LOAD_FAST                'result'
              706  LOAD_METHOD              append
              708  LOAD_STR                 '\n'
              710  LOAD_METHOD              join

 L. 389       712  LOAD_STR                 '<span class="InvalidInput">'
              714  LOAD_FAST                'highlight_invalid'
              716  BINARY_MULTIPLY  

 L. 390       718  LOAD_GLOBAL              web2ldap
              720  LOAD_ATTR                app
              722  LOAD_ATTR                gui
              724  LOAD_ATTR                HIDDEN_FIELD

 L. 391       726  LOAD_STR                 'in_at'

 L. 392       728  LOAD_STR                 ';'
              730  LOAD_METHOD              join
              732  LOAD_FAST                'attr_type_name'
              734  BUILD_LIST_1          1 
              736  LOAD_FAST                'attr_type_tags'
              738  BINARY_ADD       
              740  CALL_METHOD_1         1  ''

 L. 393       742  LOAD_STR                 ''

 L. 390       744  BUILD_TUPLE_3         3 
              746  BINARY_MODULO    

 L. 396       748  LOAD_GLOBAL              web2ldap
              750  LOAD_ATTR                app
              752  LOAD_ATTR                gui
              754  LOAD_ATTR                HIDDEN_FIELD
              756  LOAD_STR                 'in_avi'
              758  LOAD_GLOBAL              str
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                attr_counter
              764  CALL_FUNCTION_1       1  ''
              766  LOAD_STR                 ''
              768  BUILD_TUPLE_3         3 
              770  BINARY_MODULO    

 L. 397       772  LOAD_FAST                'input_field'
              774  LOAD_ATTR                input_html

 L. 398       776  LOAD_STR                 '_'
              778  LOAD_METHOD              join

 L. 399       780  LOAD_STR                 'inputattr'

 L. 399       782  LOAD_FAST                'attr_type_name'

 L. 399       784  LOAD_GLOBAL              str
              786  LOAD_FAST                'attr_index'
              788  CALL_FUNCTION_1       1  ''

 L. 398       790  BUILD_TUPLE_3         3 
              792  CALL_METHOD_1         1  ''

 L. 401       794  LOAD_FAST                'attr_title'

 L. 397       796  LOAD_CONST               ('id_value', 'title')
              798  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 403       800  LOAD_FAST                'attr_inst'
              802  LOAD_METHOD              valueButton
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                _app
              808  LOAD_ATTR                command
              810  LOAD_FAST                'self'
              812  LOAD_ATTR                row_counter
              814  LOAD_STR                 '+'
              816  CALL_METHOD_3         3  ''

 L. 404       818  LOAD_FAST                'attr_inst'
              820  LOAD_METHOD              valueButton
              822  LOAD_FAST                'self'
              824  LOAD_ATTR                _app
              826  LOAD_ATTR                command
              828  LOAD_FAST                'self'
              830  LOAD_ATTR                row_counter
              832  LOAD_STR                 '-'
              834  CALL_METHOD_3         3  ''

 L. 405       836  LOAD_STR                 '</span>'
              838  LOAD_FAST                'highlight_invalid'
              840  BINARY_MULTIPLY  

 L. 388       842  BUILD_LIST_7          7 
              844  CALL_METHOD_1         1  ''
              846  CALL_METHOD_1         1  ''
              848  POP_TOP          

 L. 407       850  LOAD_FAST                'self'
              852  DUP_TOP          
              854  LOAD_ATTR                row_counter
              856  LOAD_CONST               1
              858  INPLACE_ADD      
              860  ROT_TWO          
              862  STORE_ATTR               row_counter
          864_866  JUMP_BACK           682  'to 682'
            868_0  COME_FROM           514  '514'

 L. 409       868  LOAD_FAST                'self'
              870  DUP_TOP          
              872  LOAD_ATTR                attr_counter
              874  LOAD_CONST               1
              876  INPLACE_ADD      
              878  ROT_TWO          
              880  STORE_ATTR               attr_counter
              882  JUMP_BACK           182  'to 182'

 L. 411       884  LOAD_STR                 '<a class="hide" id="in_a_%s"></a>%s'

 L. 412       886  LOAD_FAST                'self'
              888  LOAD_ATTR                _app
              890  LOAD_ATTR                form
              892  LOAD_METHOD              utf2display
              894  LOAD_FAST                'nameoroid'
              896  CALL_METHOD_1         1  ''

 L. 413       898  LOAD_STR                 '\n<br>\n'
              900  LOAD_METHOD              join
              902  LOAD_FAST                'result'
              904  CALL_METHOD_1         1  ''

 L. 411       906  BUILD_TUPLE_2         2 
              908  BINARY_MODULO    
              910  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 514_516

    def attribute_types(self):
        attr_type_filter = [
         (
          'no_user_mod', [0]),
         (
          'collective', [0])]
        if not self._app.ls.relax_rules:
            attr_type_filter.append(('obsolete', [0]))
        object_class_oids = self.entry.object_class_oid_set()
        try:
            object_class_oids.remove('1.3.6.1.4.1.1466.101.120.111')
        except KeyError:
            pass
        else:
            try:
                object_class_oids.remove('extensibleObject')
            except KeyError:
                pass
            else:
                required_attrs_dict, allowed_attrs_dict = self.entry._s.attribute_types((list(object_class_oids)),
                  attr_type_filter=attr_type_filter,
                  raise_keyerror=0,
                  ignore_dit_content_rule=(self._app.ls.relax_rules))
                if '2.5.4.0' not in required_attrs_dict:
                    if '2.5.4.0' not in allowed_attrs_dict:
                        required_attrs_dict['2.5.4.0'] = self.entry._s.get_obj(ObjectClass, '2.5.4.0')
                return (
                 required_attrs_dict, allowed_attrs_dict)

    def fieldset_table(self, attr_types_dict, fieldset_title):
        self._app.outf.write('<fieldset title="%s">\n            <legend>%s</legend>\n            <table summary="%s">\n            ' % (
         fieldset_title, fieldset_title, fieldset_title))
        seen_attr_type_oids = ldap0.cidict.CIDict()
        attr_type_names = ldap0.cidict.CIDict()
        for a in self.entry.keys():
            at_oid = self.entry.name2key(a)[0]
            if at_oid in attr_types_dict:
                seen_attr_type_oids[at_oid] = None
                attr_type_names[a] = None
            for at_oid, at_se in attr_types_dict.items():
                if at_se and at_oid not in seen_attr_type_oids:
                    if not web2ldap.app.schema.no_userapp_attr(self.entry._s, at_oid):
                        attr_type_names[(at_se.names or (at_se.oid,))[0]] = None
                    attr_types = list(attr_type_names.keys())
                    attr_types.sort(key=(str.lower))

        for attr_type in attr_types:
            attr_type_name = schema_anchor((self._app), attr_type, AttributeType, link_text='&raquo')
            attr_value_field_html = self[attr_type]
            self._app.outf.write('<tr>\n<td class="InputAttrType">\n%s\n</td>\n<td>\n%s\n</td>\n</tr>\n' % (
             attr_type_name,
             attr_value_field_html))
        else:
            self._app.outf.write('</table>\n</fieldset>\n')

    def table_input(self, attrs_dict_list):
        self._reset_input_counters()
        for attr_dict, fieldset_title in attrs_dict_list:
            if attr_dict:
                self.fieldset_table(attr_dict, fieldset_title)

    def template_output(self, cnf_key, display_duplicate_attrs=True):
        self._reset_input_counters()
        displayed_attrs = web2ldap.app.read.DisplayEntry.template_output(self,
          cnf_key, display_duplicate_attrs=display_duplicate_attrs)
        for attr_type, attr_values in self.entry.items():
            at_oid = self.entry.name2key(attr_type)[0]
            syntax_class = syntax_registry.get_syntax(self.entry._s, attr_type, self.soc)
            if syntax_class.editable and not web2ldap.app.schema.no_userapp_attr(self.entry._s, attr_type):
                if at_oid not in displayed_attrs:
                    for attr_value in attr_values:
                        attr_inst = syntax_classself._appself.dnself.entry._sattr_typeattr_valueself.entry
                        self._app.outf.write(self._app.form.hiddenFieldHTML('in_at', attr_type, ''))
                        self._app.outf.write(web2ldap.app.gui.HIDDEN_FIELD % ('in_avi', str(self.attr_counter), ''))
                        try:
                            attr_value_html = self._app.form.utf2display((attr_inst.formValue()), sp_entity='  ')
                        except UnicodeDecodeError:
                            attr_value_html = ''
                        else:
                            self._app.outf.write(web2ldap.app.gui.HIDDEN_FIELD % (
                             'in_av', attr_value_html, ''))
                            self.attr_counter += 1

            return displayed_attrs

    def ldif_input(self):
        f = BytesIO()
        ldif_writer = ldap0.ldif.LDIFWriter(f)
        ldap_entry = {}
        for attr_type in self.entry.keys():
            attr_values = self.entry.__getitem__(attr_type)
            if not web2ldap.app.schema.no_userapp_attr(self.entry._s, attr_type):
                ldap_entry[attr_type.encode('ascii')] = [attr_value for attr_value in attr_values if attr_value]
            ldif_writer.unparse(self.dn.encode(self._app.ls.charset), ldap_entry)
            self._app.outf.write(INPUT_FORM_LDIF_TMPL.format(value_ldif=self._app.form.utf2display((f.getvalue().decode('utf-8')),
              sp_entity='  ',
              lf_entity='\n'),
              value_ldifmaxbytes=(web2ldapcnf.ldif_maxbytes),
              text_ldifurlschemes=(', '.join(web2ldapcnf.ldif_url_schemes))))


def SupentryDisplayString(app, parent_dn, supentry_display_tmpl=None):
    supentry_display_tmpl = supentry_display_tmpl or '\n        <p title="Superior entry information">\n          <strong>Superior entry:</strong><br>\n          %s\n        </p>\n        '
    assert isinstance(parent_dn, str), TypeError("Argument 'parent_dn' must be str, was %r" % parent_dn)
    if parent_dn is None:
        return ''
    supentry_display_strings = []
    inputform_supentrytemplate = app.cfg_param('inputform_supentrytemplate', {})
    if inputform_supentrytemplate:
        inputform_supentrytemplate_attrtypes = set(['objectClass'])
        for oc in inputform_supentrytemplate.keys():
            inputform_supentrytemplate_attrtypes.update(GrabKeys(inputform_supentrytemplate[oc]).keys)
        else:
            try:
                parent_search_result = app.ls.l.read_s(parent_dn,
                  attrlist=inputform_supentrytemplate_attrtypes)
            except (
             ldap0.NO_SUCH_OBJECT,
             ldap0.INSUFFICIENT_ACCESS,
             ldap0.REFERRAL):
                pass

            if parent_search_result is not None:
                parent_entry = web2ldap.app.read.DisplayEntry(app, parent_dn, app.schema, parent_search_result.entry_as, 'readSep', 0)
                for oc in parent_search_result.entry_s.get('objectClass', []):
                    try:
                        inputform_supentrytemplate[oc]
                    except KeyError:
                        pass
                    else:
                        supentry_display_strings.append(inputform_supentrytemplate[oc] % parent_entry)

    if supentry_display_strings:
        return supentry_display_tmpl % '\n'.join(supentry_display_strings)
    return app.form.utf2display(parent_dn)


def ObjectClassForm(app, existing_object_classes, structural_object_class):
    """Form for choosing object class(es)"""

    def get_possible_soc(app, parent_dn):
        """
        This function tries to determine the possible structural object classes
        and returns it as a list of object class NAMEs
        """
        all_structural_oc = None
        dit_structure_rule_html = ''
        if app.schema.sed[DITStructureRule]:
            dit_structure_ruleid = app.ls.get_governing_structure_rule(parent_dn, app.schema)
            if dit_structure_ruleid is not None:
                subord_structural_ruleids, subord_structural_oc = app.schema.get_subord_structural_oc_names(dit_structure_ruleid)
                if subord_structural_oc:
                    all_structural_oc = subord_structural_oc
                    dit_structure_rule_html = 'DIT structure rules:<br>%s' % '<br>'.join(schema_anchors(app, subord_structural_ruleids, DITStructureRule))
        else:
            if '1.2.840.113556.1.4.912' in app.schema.sed[AttributeType]:
                if not app.ls.is_openldap:
                    try:
                        parent = app.ls.l.read_s(parent_dn,
                          attrlist=[
                         'allowedChildClasses', 'allowedChildClassesEffective'])
                    except (
                     ldap0.NO_SUCH_OBJECT,
                     ldap0.INSUFFICIENT_ACCESS,
                     ldap0.REFERRAL):
                        pass

                    if parent:
                        try:
                            allowed_child_classes = parent.entry_s['allowedChildClasses']
                        except KeyError:
                            dit_structure_rule_html = ''
                        else:
                            allowed_child_classes_kind_dict = {0:[],  1:[],  2:[]}
                            for av in allowed_child_classes:
                                at_se = app.schema.get_obj(ObjectClass, av)
                                if at_se is not None:
                                    allowed_child_classes_kind_dict[at_se.kind].append(av)
                                all_structural_oc = allowed_child_classes_kind_dict[0]
                                dit_structure_rule_html = 'Governed by <var>allowedChildClasses</var>.'

            return (
             all_structural_oc, dit_structure_rule_html)

    def ExpertOCFields(app, parent_dn):
        all_structural_oc, all_abstract_oc, all_auxiliary_oc = web2ldap.app.schema.object_class_categories(app.schema, all_oc)
        dit_structure_rule_html = ''
        restricted_structural_oc, dit_structure_rule_html = get_possible_soc(app, parent_dn)
        all_structural_oc = restricted_structural_oc or all_structural_oc
        existing_misc_oc = set(existing_object_classes)
        for a in existing_structural_oc + existing_abstract_oc + existing_auxiliary_oc:
            existing_misc_oc.discard(a)
        else:
            existing_misc_oc = list(existing_misc_oc)
            dit_content_rule_html = ''
            if existing_object_classes:
                if structural_object_class:
                    soc_oid = app.schema.name2oid[ObjectClass].get(structural_object_class, structural_object_class)
                    dit_content_rule = app.schema.get_obj(DITContentRule, soc_oid, None)
                    if dit_content_rule is not None:
                        if dit_content_rule.obsolete:
                            dit_content_rule_status_text = 'Ignored obsolete'
                        else:
                            if app.ls.relax_rules:
                                dit_content_rule_status_text = 'Ignored'
                            else:
                                dit_content_rule_status_text = 'Governed by'
                                all_auxiliary_oc_oids = set([app.schema.get_oid(ObjectClass, nameoroid) for nameoroid in dit_content_rule.aux])
                                all_auxiliary_oc = [oc for oc in all_auxiliary_oc if app.schema.get_oid(ObjectClass, oc) in all_auxiliary_oc_oids]
                        dit_content_rule_html = '%s<br>DIT content rule:<br>%s' % (
                         dit_content_rule_status_text,
                         schema_anchor(app,
                           (dit_content_rule.names[0]),
                           DITContentRule,
                           link_text='&raquo'))
            else:
                abstract_select_field = web2ldap.app.form.ObjectClassSelect(name='in_oc',
                  text='Abstract object class(es)',
                  options=all_abstract_oc,
                  default=existing_abstract_oc,
                  size=20)
                structural_select_field = web2ldap.app.form.ObjectClassSelect(name='in_oc',
                  text='Structural object class(es)',
                  options=all_structural_oc,
                  default=existing_structural_oc,
                  size=20)
                auxiliary_select_field = web2ldap.app.form.ObjectClassSelect(name='in_oc',
                  text='Auxiliary object class(es)',
                  options=all_auxiliary_oc,
                  default=existing_auxiliary_oc,
                  size=20)
                misc_select_field = web2ldap.app.form.ObjectClassSelect(name='in_oc',
                  text='Misc. object class(es)',
                  options=[],
                  default=existing_misc_oc,
                  size=20)
                if existing_misc_oc:
                    misc_select_field_th = '<th><label for="add_misc_oc">Misc.<label></th>'
                    misc_select_field_td = '<td>%s</td>' % misc_select_field.input_html(id_value='add_misc_oc')
                else:
                    misc_select_field_th = ''
                misc_select_field_td = ''
            input_currentformtype = app.form.getInputValue('in_oft', ['Template'])[0]
            add_structural_oc_html = structural_select_field.input_html(id_value='add_structural_oc',
              title='Structural object classes to be added')
            add_auxiliary_oc_html = auxiliary_select_field.input_html(id_value='add_auxiliary_oc',
              title='Auxiliary object classes to be added')
            add_abstract_oc_html = abstract_select_field.input_html(id_value='add_abstract_oc',
              title='Abstract object classes to be added')
            add_template_field_html = '\n          <p>\n            <label for="input_formtype">Form type:</label> %s\n            <input type="submit" value="Next &gt;&gt;">\n          </p>\n          <table>\n            <tr>\n              <th><label for="add_structural_oc">Structural</label></th>\n              <th><label for="add_auxiliary_oc">Auxiliary</label></th>\n              <th><label for="add_abstract_oc">Abstract</label></th>\n              %s\n            </tr>\n            <tr>\n              <td><label for="add_structural_oc">%s</label></td>\n              <td><label for="add_auxiliary_oc">%s</label></td>\n              <td><label for="add_abstract_oc">%s</label></td>\n              %s\n            </tr>\n            <tr>\n              <td>%s</td>\n              <td>%s</td>\n              <td>&nbsp;</td>\n            </tr>\n          </table>\n        %s\n        ' % (
             app.form.field['in_ft'].input_html(default=input_currentformtype),
             misc_select_field_th,
             add_structural_oc_html,
             add_auxiliary_oc_html,
             add_abstract_oc_html,
             misc_select_field_td,
             dit_structure_rule_html,
             dit_content_rule_html,
             app.form.hiddenInputHTML(ignoreFieldNames=('dn', 'add_clonedn', 'in_ocf', 'in_oft',
                                           'in_ft', 'in_wrtattroids')))
            Msg = {'add':'Choose object class(es) for new entry.', 
             'modify':'You may change the object class(es) for the entry.'}[app.command]
            Msg = '<p class="WarningMessage">%s</p>' % Msg
            return (Msg, add_template_field_html)

    def LDIFTemplateField--- This code section failed: ---

 L. 812         0  LOAD_GLOBAL              web2ldap
                2  LOAD_ATTR                app
                4  LOAD_ATTR                schema
                6  LOAD_METHOD              object_class_categories
                8  LOAD_FAST                'app'
               10  LOAD_ATTR                schema
               12  LOAD_DEREF               'all_oc'
               14  CALL_METHOD_2         2  ''
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'all_structural_oc'
               20  STORE_FAST               'all_abstract_oc'
               22  STORE_FAST               'all_auxiliary_oc'

 L. 813        24  LOAD_GLOBAL              list
               26  LOAD_FAST                'app'
               28  LOAD_METHOD              cfg_param
               30  LOAD_STR                 'addform_entry_templates'
               32  BUILD_MAP_0           0 
               34  CALL_METHOD_2         2  ''
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  ''
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'addform_entry_templates_keys'

 L. 814        44  LOAD_FAST                'app'
               46  LOAD_METHOD              cfg_param
               48  LOAD_STR                 'addform_parent_attrs'
               50  BUILD_LIST_0          0 
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'addform_parent_attrs'

 L. 815        56  LOAD_FAST                'addform_entry_templates_keys'
               58  LOAD_METHOD              sort
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          

 L. 816        64  BUILD_MAP_0           0 
               66  STORE_FAST               'add_tmpl_dict'

 L. 817        68  LOAD_FAST                'addform_entry_templates_keys'
               70  GET_ITER         
             72_0  COME_FROM           404  '404'
             72_1  COME_FROM           396  '396'
            72_74  FOR_ITER            460  'to 460'
               76  STORE_FAST               'template_name'

 L. 818        78  LOAD_GLOBAL              ReadLDIFTemplate
               80  LOAD_FAST                'app'
               82  LOAD_FAST                'template_name'
               84  CALL_FUNCTION_2       2  ''
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'ldif_dn'
               90  STORE_FAST               'ldif_entry'

 L. 819        92  LOAD_GLOBAL              str
               94  LOAD_GLOBAL              DNObj
               96  LOAD_METHOD              from_str
               98  LOAD_FAST                'ldif_dn'
              100  LOAD_METHOD              decode
              102  LOAD_FAST                'app'
              104  LOAD_ATTR                ls
              106  LOAD_ATTR                charset
              108  CALL_METHOD_1         1  ''
              110  CALL_METHOD_1         1  ''
              112  LOAD_METHOD              parent
              114  CALL_METHOD_0         0  ''
              116  CALL_FUNCTION_1       1  ''
              118  JUMP_IF_TRUE_OR_POP   122  'to 122'
              120  LOAD_FAST                'parent_dn'
            122_0  COME_FROM           118  '118'
              122  STORE_FAST               'tmpl_parent_dn'

 L. 821       124  LOAD_FAST                'addform_parent_attrs'
              126  POP_JUMP_IF_FALSE   240  'to 240'

 L. 822       128  SETUP_FINALLY       152  'to 152'

 L. 823       130  LOAD_FAST                'app'
              132  LOAD_ATTR                ls
              134  LOAD_ATTR                l
              136  LOAD_ATTR                read_s

 L. 824       138  LOAD_FAST                'tmpl_parent_dn'

 L. 825       140  LOAD_FAST                'addform_parent_attrs'

 L. 823       142  LOAD_CONST               ('attrlist',)
              144  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              146  STORE_FAST               'parent_result'
              148  POP_BLOCK        
              150  JUMP_FORWARD        184  'to 184'
            152_0  COME_FROM_FINALLY   128  '128'

 L. 827       152  DUP_TOP          
              154  LOAD_GLOBAL              ldap0
              156  LOAD_ATTR                NO_SUCH_OBJECT
              158  LOAD_GLOBAL              ldap0
              160  LOAD_ATTR                INSUFFICIENT_ACCESS
              162  BUILD_TUPLE_2         2 
              164  COMPARE_OP               exception-match
              166  POP_JUMP_IF_FALSE   182  'to 182'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L. 828       174  POP_EXCEPT       
              176  JUMP_BACK            72  'to 72'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           166  '166'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           150  '150'

 L. 829       184  LOAD_FAST                'parent_result'
              186  POP_JUMP_IF_TRUE    190  'to 190'

 L. 830       188  JUMP_BACK            72  'to 72'
            190_0  COME_FROM           186  '186'

 L. 831       190  LOAD_GLOBAL              ldap0
              192  LOAD_ATTR                schema
              194  LOAD_ATTR                models
              196  LOAD_METHOD              Entry

 L. 832       198  LOAD_FAST                'app'
              200  LOAD_ATTR                schema

 L. 833       202  LOAD_FAST                'tmpl_parent_dn'

 L. 834       204  LOAD_FAST                'parent_result'
              206  LOAD_ATTR                entry_as

 L. 831       208  CALL_METHOD_3         3  ''
              210  STORE_DEREF              'parent_entry'

 L. 836       212  LOAD_GLOBAL              set
              214  LOAD_CLOSURE             'parent_entry'
              216  BUILD_TUPLE_1         1 
              218  LOAD_LISTCOMP            '<code_object <listcomp>>'
              220  LOAD_STR                 'ObjectClassForm.<locals>.LDIFTemplateField.<locals>.<listcomp>'
              222  MAKE_FUNCTION_8          'closure'

 L. 838       224  LOAD_FAST                'addform_parent_attrs'

 L. 836       226  GET_ITER         
              228  CALL_FUNCTION_1       1  ''
              230  CALL_FUNCTION_1       1  ''
              232  STORE_FAST               'missing_parent_attrs'

 L. 841       234  LOAD_FAST                'missing_parent_attrs'
              236  POP_JUMP_IF_FALSE   240  'to 240'

 L. 842       238  JUMP_BACK            72  'to 72'
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           126  '126'

 L. 843       240  LOAD_DEREF               'get_possible_soc'
              242  LOAD_FAST                'app'
              244  LOAD_FAST                'tmpl_parent_dn'
              246  CALL_FUNCTION_2       2  ''
              248  UNPACK_SEQUENCE_2     2 
              250  STORE_FAST               'restricted_structural_oc'
              252  STORE_FAST               'dit_structure_rule_html'

 L. 844       254  LOAD_FAST                'app'
              256  LOAD_ATTR                schema
              258  LOAD_ATTR                sed
              260  LOAD_GLOBAL              DITStructureRule
              262  BINARY_SUBSCR    
          264_266  POP_JUMP_IF_FALSE   318  'to 318'

 L. 845       268  LOAD_FAST                'app'
              270  LOAD_ATTR                ls
              272  LOAD_METHOD              get_governing_structure_rule
              274  LOAD_FAST                'tmpl_parent_dn'
              276  LOAD_FAST                'app'
              278  LOAD_ATTR                schema
              280  CALL_METHOD_2         2  ''
              282  STORE_FAST               'parent_gov_structure_rule'

 L. 846       284  LOAD_FAST                'parent_gov_structure_rule'
              286  LOAD_CONST               None
              288  COMPARE_OP               is
          290_292  POP_JUMP_IF_FALSE   306  'to 306'

 L. 847       294  LOAD_FAST                'restricted_structural_oc'
          296_298  JUMP_IF_TRUE_OR_POP   302  'to 302'
              300  LOAD_FAST                'all_structural_oc'
            302_0  COME_FROM           296  '296'
              302  STORE_FAST               'restricted_structural_oc'
              304  JUMP_FORWARD        316  'to 316'
            306_0  COME_FROM           290  '290'

 L. 849       306  LOAD_FAST                'restricted_structural_oc'
          308_310  JUMP_IF_TRUE_OR_POP   314  'to 314'
              312  BUILD_LIST_0          0 
            314_0  COME_FROM           308  '308'
              314  STORE_FAST               'restricted_structural_oc'
            316_0  COME_FROM           304  '304'
              316  JUMP_FORWARD        322  'to 322'
            318_0  COME_FROM           264  '264'

 L. 851       318  LOAD_FAST                'all_structural_oc'
              320  STORE_FAST               'restricted_structural_oc'
            322_0  COME_FROM           316  '316'

 L. 852       322  LOAD_GLOBAL              ldap0
              324  LOAD_ATTR                schema
              326  LOAD_ATTR                models
              328  LOAD_METHOD              SchemaElementOIDSet

 L. 853       330  LOAD_FAST                'app'
              332  LOAD_ATTR                schema

 L. 854       334  LOAD_GLOBAL              ObjectClass

 L. 855       336  LOAD_FAST                'restricted_structural_oc'

 L. 852       338  CALL_METHOD_3         3  ''
              340  STORE_FAST               'restricted_structural_oc_set'

 L. 857       342  LOAD_GLOBAL              ldap0
              344  LOAD_ATTR                schema
              346  LOAD_ATTR                models
              348  LOAD_METHOD              Entry

 L. 858       350  LOAD_FAST                'app'
              352  LOAD_ATTR                schema

 L. 859       354  LOAD_FAST                'ldif_dn'
              356  LOAD_METHOD              decode
              358  LOAD_FAST                'app'
              360  LOAD_ATTR                ls
              362  LOAD_ATTR                charset
              364  CALL_METHOD_1         1  ''

 L. 860       366  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              368  LOAD_STR                 'ObjectClassForm.<locals>.LDIFTemplateField.<locals>.<dictcomp>'
              370  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              372  LOAD_FAST                'ldif_entry'
              374  LOAD_METHOD              items
              376  CALL_METHOD_0         0  ''
              378  GET_ITER         
              380  CALL_FUNCTION_1       1  ''

 L. 857       382  CALL_METHOD_3         3  ''
              384  STORE_FAST               'entry'

 L. 862       386  LOAD_FAST                'entry'
              388  LOAD_METHOD              get_structural_oc
              390  CALL_METHOD_0         0  ''
              392  STORE_FAST               'soc'

 L. 863       394  LOAD_FAST                'soc'
              396  POP_JUMP_IF_FALSE    72  'to 72'
              398  LOAD_FAST                'soc'
              400  LOAD_FAST                'restricted_structural_oc_set'
              402  COMPARE_OP               in
              404  POP_JUMP_IF_FALSE    72  'to 72'

 L. 864       406  SETUP_FINALLY       426  'to 426'

 L. 865       408  LOAD_FAST                'add_tmpl_dict'
              410  LOAD_FAST                'tmpl_parent_dn'
              412  BINARY_SUBSCR    
              414  LOAD_METHOD              append
              416  LOAD_FAST                'template_name'
              418  CALL_METHOD_1         1  ''
              420  POP_TOP          
              422  POP_BLOCK        
              424  JUMP_BACK            72  'to 72'
            426_0  COME_FROM_FINALLY   406  '406'

 L. 866       426  DUP_TOP          
              428  LOAD_GLOBAL              KeyError
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   456  'to 456'
              436  POP_TOP          
              438  POP_TOP          
              440  POP_TOP          

 L. 867       442  LOAD_FAST                'template_name'
              444  BUILD_LIST_1          1 
              446  LOAD_FAST                'add_tmpl_dict'
              448  LOAD_FAST                'tmpl_parent_dn'
              450  STORE_SUBSCR     
              452  POP_EXCEPT       
              454  JUMP_BACK            72  'to 72'
            456_0  COME_FROM           432  '432'
              456  END_FINALLY      
              458  JUMP_BACK            72  'to 72'

 L. 868       460  LOAD_FAST                'add_tmpl_dict'
          462_464  POP_JUMP_IF_TRUE    500  'to 500'

 L. 870       466  LOAD_STR                 '<p class="ErrorMessage">No usable LDIF templates here. Wrong %s?</p>'

 L. 871       468  LOAD_FAST                'app'
              470  LOAD_ATTR                anchor

 L. 872       472  LOAD_STR                 'dit'

 L. 872       474  LOAD_STR                 'sub-tree'

 L. 873       476  LOAD_STR                 'dn'
              478  LOAD_FAST                'app'
              480  LOAD_ATTR                dn
              482  BUILD_TUPLE_2         2 
              484  BUILD_LIST_1          1 

 L. 874       486  LOAD_STR                 'browse directory tree'

 L. 871       488  LOAD_CONST               ('title',)
              490  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 870       492  BINARY_MODULO    

 L. 877       494  LOAD_STR                 ''

 L. 869       496  BUILD_TUPLE_2         2 
              498  RETURN_VALUE     
            500_0  COME_FROM           462  '462'

 L. 879       500  LOAD_STR                 '<dl>'
              502  BUILD_LIST_1          1 
              504  STORE_FAST               'add_template_html_list'

 L. 880       506  LOAD_GLOBAL              sorted
              508  LOAD_FAST                'add_tmpl_dict'
              510  LOAD_METHOD              keys
              512  CALL_METHOD_0         0  ''
              514  CALL_FUNCTION_1       1  ''
              516  GET_ITER         
              518  FOR_ITER            646  'to 646'
              520  STORE_FAST               'pdn'

 L. 881       522  LOAD_FAST                'add_template_html_list'
              524  LOAD_METHOD              append
              526  LOAD_STR                 '<dt>%s<dt>'

 L. 882       528  LOAD_GLOBAL              SupentryDisplayString
              530  LOAD_FAST                'app'
              532  LOAD_FAST                'pdn'
              534  LOAD_STR                 '%s'
              536  LOAD_CONST               ('supentry_display_tmpl',)
              538  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 881       540  BUILD_TUPLE_1         1 
              542  BINARY_MODULO    
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          

 L. 884       548  LOAD_FAST                'add_template_html_list'
              550  LOAD_METHOD              append
              552  LOAD_STR                 '<dd><ul>'
              554  CALL_METHOD_1         1  ''
              556  POP_TOP          

 L. 885       558  LOAD_FAST                'add_tmpl_dict'
              560  LOAD_FAST                'pdn'
              562  BINARY_SUBSCR    
              564  GET_ITER         
              566  FOR_ITER            632  'to 632'
              568  STORE_FAST               'tmpl_name'

 L. 886       570  LOAD_FAST                'add_template_html_list'
              572  LOAD_METHOD              append

 L. 887       574  LOAD_STR                 '<li>%s</li>'

 L. 888       576  LOAD_FAST                'app'
              578  LOAD_ATTR                anchor

 L. 889       580  LOAD_STR                 'add'

 L. 889       582  LOAD_FAST                'app'
              584  LOAD_ATTR                form
              586  LOAD_METHOD              utf2display
              588  LOAD_FAST                'tmpl_name'
              590  CALL_METHOD_1         1  ''

 L. 891       592  LOAD_STR                 'dn'
              594  LOAD_FAST                'pdn'
              596  BUILD_TUPLE_2         2 

 L. 892       598  LOAD_STR                 'add_template'
              600  LOAD_FAST                'tmpl_name'
              602  BUILD_TUPLE_2         2 

 L. 893       604  LOAD_CONST               ('in_ft', 'Template')

 L. 890       606  BUILD_LIST_3          3 

 L. 895       608  LOAD_STR                 'Add entry beneath %s\nbased on template "%s"'
              610  LOAD_FAST                'pdn'
              612  LOAD_FAST                'tmpl_name'
              614  BUILD_TUPLE_2         2 
              616  BINARY_MODULO    

 L. 888       618  LOAD_CONST               ('title',)
              620  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 887       622  BINARY_MODULO    

 L. 886       624  CALL_METHOD_1         1  ''
              626  POP_TOP          
          628_630  JUMP_BACK           566  'to 566'

 L. 899       632  LOAD_FAST                'add_template_html_list'
              634  LOAD_METHOD              append
              636  LOAD_STR                 '</ul></dd>'
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          
          642_644  JUMP_BACK           518  'to 518'

 L. 900       646  LOAD_FAST                'add_template_html_list'
              648  LOAD_METHOD              append
              650  LOAD_STR                 '</dl>'
              652  CALL_METHOD_1         1  ''
              654  POP_TOP          

 L. 901       656  LOAD_STR                 '\n'
              658  LOAD_METHOD              join
              660  LOAD_FAST                'add_template_html_list'
              662  CALL_METHOD_1         1  ''
              664  STORE_FAST               'add_template_field_html'

 L. 902       666  LOAD_STR                 '<p class="WarningMessage">Choose a LDIF template and base DN for new entry</p>'
              668  STORE_FAST               'Msg'

 L. 903       670  LOAD_FAST                'Msg'
              672  LOAD_FAST                'add_template_field_html'
              674  BUILD_TUPLE_2         2 
              676  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 178

    in_ocf = app.form.getInputValue('in_ocf', ['tmpl'])[0]
    command_hidden_fields = [
     (
      'dn', app.dn)]
    existing_structural_oc, existing_abstract_oc, existing_auxiliary_oc = web2ldap.app.schema.object_class_categories(app.schema, existing_object_classes)
    all_oc = [(app.schema.get_obj(ObjectClass, oid).names or (oid,))[0] for oid in app.schema.listall(ObjectClass)]
    if app.command == 'add':
        parent_dn = app.dn
    else:
        if app.command == 'modify':
            parent_dn = app.parent_dn
        elif app.command == 'add' and in_ocf == 'tmpl':
            Msg, add_template_field_html = LDIFTemplateField(app, parent_dn)
        else:
            Msg, add_template_field_html = ExpertOCFields(app, parent_dn)
        context_menu_list = []
        if app.command == 'add':
            context_menu_list.extend([
             app.anchor('add', 'Templates', [('dn', app.dn), ('in_ocf', 'tmpl')]),
             app.anchor('add', 'Expert', [('dn', app.dn), ('in_ocf', 'exp')])])
        web2ldap.app.gui.top_section(app,
          (H1_MSG[app.command]),
          (web2ldap.app.gui.main_menu(app)),
          context_menu_list=context_menu_list,
          main_div_id='Input')
        app.outf.write('<h1>%s</h1>\n%s\n</form>' % (
         H1_MSG[app.command],
         '\n'.join((
          app.begin_form(app.command, 'POST'),
          ''.join([app.form.hiddenFieldHTML(param_name, param_value, '') for param_name, param_value in command_hidden_fields]),
          Msg,
          add_template_field_html))))
        web2ldap.app.gui.footer(app)


def ReadLDIFTemplate(app, template_name):
    addform_entry_templates = app.cfg_param('addform_entry_templates', {})
    template_name_html = escape_html(template_name)
    if template_name not in addform_entry_templates:
        raise web2ldap.app.core.ErrorExit('LDIF template key &quot;%s&quot; not known.' % template_name_html)
    ldif_file_name = addform_entry_templates[template_name]
    try:
        ldif_file = None
        try:
            ldif_file = open(ldif_file_name, 'rb')
        except IOError:
            raise web2ldap.app.core.ErrorExit('I/O error opening LDIF template for &quot;%s&quot;.' % template_name_html)
        else:
            try:
                dn, entry = list(ldap0.ldif.LDIFParser(ldif_file,
                  ignored_attr_types=[], process_url_schemes=(web2ldapcnf.ldif_url_schemes)).parse(max_entries=1))[0]
            except (IOError, ValueError):
                raise web2ldap.app.core.ErrorExit('Value error reading/parsing LDIF template for &quot;%s&quot;.' % template_name_html)
            except Exception:
                raise web2ldap.app.core.ErrorExit('Other error reading/parsing LDIF template for &quot;%s&quot;.' % template_name_html)

    finally:
        if ldif_file is not None:
            ldif_file.close()

    return (
     dn, entry)


def AttributeTypeDict(app, param_name, param_default):
    """
    Build a list of attributes assumed in configuration to be constant while editing entry
    """
    attrs = ldap0.cidict.CIDict()
    for attr_type in app.cfg_param(param_name, param_default):
        attrs[attr_type] = attr_type
    else:
        return attrs


def ConfiguredConstantAttributes(app):
    """
    Build a list of attributes assumed in configuration to be constant while editing entry
    """
    return AttributeTypeDict(app, 'modify_constant_attrs', [
     'createTimestamp', 'modifyTimestamp', 'creatorsName', 'modifiersName'])


def AssertionFilter--- This code section failed: ---

 L.1014         0  BUILD_LIST_0          0 
                2  STORE_FAST               'assertion_filter_list'

 L.1015         4  LOAD_GLOBAL              ConfiguredConstantAttributes
                6  LOAD_DEREF               'app'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_METHOD              values
               12  CALL_METHOD_0         0  ''
               14  GET_ITER         
               16  FOR_ITER             86  'to 86'
               18  STORE_DEREF              'attr_type'

 L.1016        20  SETUP_FINALLY        34  'to 34'

 L.1017        22  LOAD_FAST                'entry'
               24  LOAD_DEREF               'attr_type'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'attr_values'
               30  POP_BLOCK        
               32  JUMP_FORWARD         58  'to 58'
             34_0  COME_FROM_FINALLY    20  '20'

 L.1018        34  DUP_TOP          
               36  LOAD_GLOBAL              KeyError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    56  'to 56'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.1019        48  POP_EXCEPT       
               50  JUMP_BACK            16  'to 16'
               52  POP_EXCEPT       
               54  JUMP_BACK            16  'to 16'
             56_0  COME_FROM            40  '40'
               56  END_FINALLY      
             58_0  COME_FROM            32  '32'

 L.1021        58  LOAD_FAST                'assertion_filter_list'
               60  LOAD_METHOD              extend
               62  LOAD_CLOSURE             'app'
               64  LOAD_CLOSURE             'attr_type'
               66  BUILD_TUPLE_2         2 
               68  LOAD_LISTCOMP            '<code_object <listcomp>>'
               70  LOAD_STR                 'AssertionFilter.<locals>.<listcomp>'
               72  MAKE_FUNCTION_8          'closure'

 L.1028        74  LOAD_FAST                'attr_values'

 L.1021        76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            16  'to 16'

 L.1031        86  LOAD_FAST                'assertion_filter_list'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L.1032        90  LOAD_STR                 '(&%s)'
               92  LOAD_STR                 ''
               94  LOAD_METHOD              join
               96  LOAD_FAST                'assertion_filter_list'
               98  CALL_METHOD_1         1  ''
              100  BINARY_MODULO    
              102  STORE_FAST               'assertion_filter'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            88  '88'

 L.1034       106  LOAD_STR                 '(objectClass=*)'
              108  STORE_FAST               'assertion_filter'
            110_0  COME_FROM           104  '104'

 L.1035       110  LOAD_FAST                'assertion_filter'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 52


def nomatching_attrs(sub_schema, entry, allowed_attrs_dict, required_attrs_dict):
    """
    Determine attributes which does not appear in the schema but
    do exist in the entry
    """
    nomatching_attrs_dict = ldap0.cidict.CIDict()
    for at_name in entry.entry.keys():
        try:
            at_oid = sub_schema.name2oid[AttributeType][at_name]
        except KeyError:
            nomatching_attrs_dict[at_name] = None
        else:
            if not at_oid in allowed_attrs_dict:
                if not at_oid in required_attrs_dict:
                    if not at_name.lower() == 'objectclass':
                        nomatching_attrs_dict[at_oid] = sub_schema.get_obj(AttributeType, at_oid)
            return nomatching_attrs_dict


WRITEABLE_ATTRS_NONE = None
WRITEABLE_ATTRS_SLAPO_ALLOWED = 1
WRITEABLE_ATTRS_GET_EFFECTIVE_RIGHTS = 2

def read_old_entry(app, dn, sub_schema, assertion_filter, read_attrs=None):
    """
    Retrieve all editable attribute types an entry
    """
    server_ctrls = []
    if not read_attrs:
        read_attrs = ldap0.cidict.CIDict({'*': '*'})
        read_attrs.update(ConfiguredConstantAttributes(app))
        read_attrs.update(AttributeTypeDict(app, 'requested_attrs', []))
    elif '1.2.840.113556.1.4.914' in sub_schema.sed[AttributeType]:
        read_attrs['allowedAttributesEffective'] = 'allowedAttributesEffective'
        write_attrs_method = WRITEABLE_ATTRS_SLAPO_ALLOWED
    else:
        write_attrs_method = WRITEABLE_ATTRS_NONE
    assert write_attrs_method in {WRITEABLE_ATTRS_NONE, WRITEABLE_ATTRS_SLAPO_ALLOWED, WRITEABLE_ATTRS_GET_EFFECTIVE_RIGHTS}, ValueError('Invalid value for write_attrs_method')
    if app.ls.manage_dsa_it:
        read_attrs['ref'] = 'ref'
    ldap_res = app.ls.l.read_s(dn,
      attrlist=(read_attrs.values()),
      filterstr=(assertion_filter or '(objectClass=*)'),
      cache_ttl=(-1.0),
      req_ctrls=(server_ctrls or None))
    if ldap_res is None:
        raise ldap0.NO_SUCH_OBJECT('Empty search result.')
    entry = ldap0.schema.models.Entry(sub_schema, ldap_res.dn_s, ldap_res.entry_as)
    if write_attrs_method == WRITEABLE_ATTRS_NONE:
        writeable_attr_oids = None
    else:
        if write_attrs_method == WRITEABLE_ATTRS_SLAPO_ALLOWED:
            try:
                writeable_attr_oids = ldap0.schema.models.SchemaElementOIDSet(sub_schema, AttributeType, [av.decode('ascii') for av in ldap_res.entry_as.get('allowedAttributesEffective', [])])
            except KeyError:
                writeable_attr_oids = set([])
            else:
                if 'allowedAttributesEffective' in entry:
                    del entry['allowedAttributesEffective']
        else:
            if write_attrs_method == WRITEABLE_ATTRS_GET_EFFECTIVE_RIGHTS:
                acl_rights_attribute_level = [(
                 a, v) for a, v in entry.data.items() if a[0] == '1.3.6.1.4.1.42.2.27.9.1.39' if a[1] == 'attributelevel']
                if acl_rights_attribute_level:
                    writeable_attr_oids = set([])
                    for a, v in acl_rights_attribute_level:
                        try:
                            dummy1, dummy2, attr_type = a
                        except ValueError:
                            pass
                        else:
                            if v[0].lower().find(',write:1,') >= 0:
                                writeable_attr_oids.add(sub_schema.get_oid(AttributeType, a[2]).decode('ascii'))
                            del entry[';'.join((dummy1, dummy2, attr_type))]

            return (
             entry, writeable_attr_oids)


def w2l_addform(app, add_rdn, add_basedn, entry, msg='', invalid_attrs=None):
    if msg:
        msg = '<p class="ErrorMessage">%s</p>' % msg
    else:
        input_formtype = app.form.getInputValue('in_ft', app.form.getInputValue('in_oft', ['OC']))[0]
        if 'in_oc' in app.form.input_field_names:
            entry['objectClass'] = [oc.encode('ascii') for oc in app.form.field['in_oc'].value]
        if not input_formtype == 'OC':
            if not entry:
                ObjectClassForm(app, decode_list(entry.get('objectClass', []), 'ascii'), None)
                return None
            input_form_entry = InputFormEntry(app, (app.dn), (app.schema), entry, None, invalid_attrs=invalid_attrs)
            required_attrs_dict, allowed_attrs_dict = input_form_entry.attribute_types()
            nomatching_attrs_dict = nomatching_attrs(app.schema, input_form_entry, allowed_attrs_dict, required_attrs_dict)
            rdn_options = input_form_entry.entry.get_rdn_templates()
            supentry_display_string = SupentryDisplayString(app, add_basedn)
            if rdn_options and len(rdn_options) > 0:
                rdn_input_field = web2ldap.web.forms.Select('add_rdn', 'RDN variants', 1, options=rdn_options)
        else:
            rdn_input_field = app.form.field['add_rdn']
    if add_rdn:
        rdn_input_field.set_default(add_rdn)
    else:
        rdn_candidate_attr_nameoroids = [(required_attrs_dict[at_oid].names or (at_oid,))[0] for at_oid in required_attrs_dict.keys() if at_oid != '2.5.4.0' if not web2ldap.app.schema.no_humanreadable_attr(app.schema, at_oid)]
        if len(rdn_candidate_attr_nameoroids) == 1:
            rdn_input_field.set_default(rdn_candidate_attr_nameoroids[0] + '=')
        if app.ls.relax_rules:
            msg = ''.join((
             msg,
             '<p class="WarningMessage">Relax Rules Control enabled! Be sure you know what you are doing!</p>'))
    if input_formtype == 'Template':
        template_oc, read_template_dict = input_form_entry.get_html_templates('input_template')
        msg = template_oc or ''.join((
         msg,
         '<p class="WarningMessage">No templates defined for chosen object classes.</p>'))
        input_formtype = 'Table'
    else:
        if app.ls.relax_rules:
            msg = ''.join((
             msg,
             '<p class="WarningMessage">Forced to table input because Relax Rules Control is enabled.</p>'))
            input_formtype = 'Table'
        web2ldap.app.gui.top_section(app,
          (H1_MSG[app.command]),
          (web2ldap.app.gui.main_menu(app)),
          context_menu_list=[])
        app.outf.write(INPUT_FORM_BEGIN_TMPL.format(text_heading=(H1_MSG[app.command]),
          text_msg=msg,
          text_supentry=supentry_display_string,
          form_begin=app.begin_form((app.command), 'POST', enctype='multipart/form-data'),
          field_dn=(app.form.hiddenFieldHTML('dn', app.dn, '')),
          field_currentformtype=(app.form.hiddenFieldHTML('in_oft', str(input_formtype), ''))))
        app.outf.write('%s\n<p>RDN: %s</p>\n%s' % (
         app.form.hiddenFieldHTML('add_basedn', add_basedn, ''),
         rdn_input_field.input_html(),
         app.form.hiddenFieldHTML('in_ocf', 'exp', '')))
    if input_formtype == 'Template':
        input_form_entry.template_output('input_template',
          display_duplicate_attrs=False)
    else:
        if input_formtype == 'Table':
            input_form_entry.table_input((
             (
              required_attrs_dict, 'Required attributes'),
             (
              allowed_attrs_dict, 'Allowed attributes'),
             (
              nomatching_attrs_dict, 'Other attributes')))
        else:
            if input_formtype == 'LDIF':
                input_form_entry.ldif_input()
            app.outf.write('</form>')
            web2ldap.app.gui.footer(app)


def w2l_modifyform(app, entry, msg='', invalid_attrs=None):
    if msg:
        msg = '<p class="ErrorMessage">%s</p>' % msg
    else:
        input_formtype = app.form.getInputValue('in_ft', app.form.getInputValue('in_oft', ['Template']))[0]
        if 'in_oc' in app.form.input_field_names:
            entry['objectClass'] = [oc.encode('ascii') for oc in app.form.field['in_oc'].value]
        else:
            old_entry, read_writeable_attr_oids = read_old_entry(app, app.dn, app.schema, None)
            if not entry:
                entry = old_entry
            else:
                in_wrtattroids = app.form.getInputValue('in_wrtattroids', [])
                if in_wrtattroids == ['nonePseudoValue;x-web2ldap-None']:
                    writeable_attr_oids = None
                else:
                    if in_wrtattroids:
                        writeable_attr_oids = set([a.encode(app.ls.charset) for a in in_wrtattroids])
                    else:
                        writeable_attr_oids = read_writeable_attr_oids
        if input_formtype == 'OC':
            ObjectClassForm(app, decode_list(entry['objectClass'], 'ascii'), entry.get_structural_oc())
            return
            existing_object_classes = decode_list((entry['objectClass'][:]), encoding='ascii')
            input_form_entry = InputFormEntry(app,
              (app.dn), (app.schema), entry,
              writeable_attr_oids, existing_object_classes, invalid_attrs=invalid_attrs)
            required_attrs_dict, allowed_attrs_dict = input_form_entry.attribute_types()
            nomatching_attrs_dict = nomatching_attrs(app.schema, input_form_entry, allowed_attrs_dict, required_attrs_dict)
            supentry_display_string = SupentryDisplayString(app, app.parent_dn)
            if writeable_attr_oids is None:
                in_wrtattroids_values = app.form.hiddenFieldHTML('in_wrtattroids', 'nonePseudoValue;x-web2ldap-None', '')
        else:
            in_wrtattroids_values = ''.join([app.form.hiddenFieldHTML('in_wrtattroids', at_name, '') for at_name in writeable_attr_oids or []])
    if app.ls.relax_rules:
        msg = ''.join((
         msg,
         '<p class="WarningMessage">Relax Rules Control enabled! Be sure you know what you are doing!</p>'))
    if input_formtype == 'Template':
        template_oc, _ = input_form_entry.get_html_templates('input_template')
        msg = template_oc or ''.join((
         msg,
         '<p class="WarningMessage">No templates defined for chosen object classes.</p>'))
        input_formtype = 'Table'
    else:
        if app.ls.relax_rules:
            msg = ''.join((
             msg,
             '<p class="WarningMessage">Forced to table input because Relax Rules Control is enabled.</p>'))
            input_formtype = 'Table'
        web2ldap.app.gui.top_section(app,
          (H1_MSG[app.command]),
          (web2ldap.app.gui.main_menu(app)),
          context_menu_list=[])
        app.outf.write(INPUT_FORM_BEGIN_TMPL.format(text_heading=(H1_MSG[app.command]),
          text_msg=msg,
          text_supentry=supentry_display_string,
          form_begin=app.begin_form((app.command), 'POST', enctype='multipart/form-data'),
          field_dn=(app.form.hiddenFieldHTML('dn', app.dn, '')),
          field_currentformtype=(app.form.hiddenFieldHTML('in_oft', input_formtype, ''))))
        app.outf.write('\n'.join((
         app.form.hiddenFieldHTML('in_assertion', AssertionFilter(app, entry), ''),
         '\n'.join([app.form.hiddenFieldHTML('in_oldattrtypes', at_name, '') for at_name in app.form.getInputValue('in_oldattrtypes', entry.keys())]),
         in_wrtattroids_values)))
    if input_formtype == 'Template':
        input_form_entry.template_output('input_template',
          display_duplicate_attrs=False)
    else:
        if input_formtype == 'Table':
            input_form_entry.table_input((
             (
              required_attrs_dict, 'Required attributes'),
             (
              allowed_attrs_dict, 'Allowed attributes'),
             (
              nomatching_attrs_dict, 'Other attributes')))
        else:
            if input_formtype == 'LDIF':
                input_form_entry.ldif_input()
            app.outf.write('</form>')
            web2ldap.app.gui.footer(app)
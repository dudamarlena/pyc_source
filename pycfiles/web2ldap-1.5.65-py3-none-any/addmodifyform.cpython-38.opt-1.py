# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/addmodifyform.py
# Compiled at: 2020-04-23 17:13:02
# Size of source mod 2**32: 53403 bytes
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

    def __init__--- This code section failed: ---

 L. 259         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'dn'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'
               10  LOAD_ASSERT              AssertionError
               12  LOAD_GLOBAL              TypeError
               14  LOAD_STR                 "Argument 'dn' must be str, was %r"
               16  LOAD_FAST                'dn'
               18  BINARY_MODULO    
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 260        26  LOAD_GLOBAL              web2ldap
               28  LOAD_ATTR                app
               30  LOAD_ATTR                read
               32  LOAD_ATTR                DisplayEntry
               34  LOAD_METHOD              __init__

 L. 261        36  LOAD_DEREF               'self'

 L. 261        38  LOAD_FAST                'app'

 L. 261        40  LOAD_FAST                'dn'

 L. 261        42  LOAD_FAST                'schema'

 L. 261        44  LOAD_FAST                'entry'

 L. 261        46  LOAD_STR                 'fieldSep'

 L. 261        48  LOAD_CONST               False

 L. 260        50  CALL_METHOD_7         7  ''
               52  POP_TOP          

 L. 263        54  LOAD_FAST                'existing_object_classes'
               56  LOAD_DEREF               'self'
               58  STORE_ATTR               existing_object_classes

 L. 264        60  LOAD_FAST                'writeable_attr_oids'
               62  LOAD_DEREF               'self'
               64  STORE_ATTR               writeable_attr_oids

 L. 265        66  LOAD_FAST                'invalid_attrs'
               68  JUMP_IF_TRUE_OR_POP    72  'to 72'
               70  BUILD_MAP_0           0 
             72_0  COME_FROM            68  '68'
               72  LOAD_DEREF               'self'
               74  STORE_ATTR               invalid_attrs

 L. 266        76  LOAD_GLOBAL              set
               78  LOAD_DEREF               'self'
               80  LOAD_ATTR                entry
               82  LOAD_METHOD              object_class_oid_set
               84  CALL_METHOD_0         0  ''
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CLOSURE             'self'
               90  BUILD_TUPLE_1         1 
               92  LOAD_SETCOMP             '<code_object <setcomp>>'
               94  LOAD_STR                 'InputFormEntry.__init__.<locals>.<setcomp>'
               96  MAKE_FUNCTION_8          'closure'

 L. 268        98  LOAD_FAST                'existing_object_classes'
              100  JUMP_IF_TRUE_OR_POP   104  'to 104'
              102  BUILD_LIST_0          0 
            104_0  COME_FROM           100  '100'

 L. 266       104  GET_ITER         
              106  CALL_FUNCTION_1       1  ''
              108  BINARY_SUBTRACT  
              110  STORE_FAST               'new_object_classes'

 L. 270       112  LOAD_DEREF               'self'
              114  LOAD_ATTR                entry
              116  LOAD_ATTR                _s
              118  LOAD_ATTR                attribute_types

 L. 271       120  LOAD_FAST                'new_object_classes'

 L. 272       122  LOAD_CONST               0

 L. 273       124  LOAD_DEREF               'self'
              126  LOAD_ATTR                _app
              128  LOAD_ATTR                ls
              130  LOAD_ATTR                relax_rules

 L. 270       132  LOAD_CONST               ('raise_keyerror', 'ignore_dit_content_rule')
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  STORE_FAST               'new_attribute_types'

 L. 275       138  LOAD_DEREF               'self'
              140  LOAD_ATTR                entry
              142  LOAD_ATTR                _s
              144  LOAD_ATTR                attribute_types

 L. 276       146  LOAD_FAST                'existing_object_classes'
              148  JUMP_IF_TRUE_OR_POP   152  'to 152'
              150  BUILD_LIST_0          0 
            152_0  COME_FROM           148  '148'

 L. 277       152  LOAD_CONST               0

 L. 278       154  LOAD_DEREF               'self'
              156  LOAD_ATTR                _app
              158  LOAD_ATTR                ls
              160  LOAD_ATTR                relax_rules

 L. 275       162  LOAD_CONST               ('raise_keyerror', 'ignore_dit_content_rule')
              164  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              166  STORE_FAST               'old_attribute_types'

 L. 280       168  LOAD_GLOBAL              set
              170  CALL_FUNCTION_0       0  ''
              172  LOAD_DEREF               'self'
              174  STORE_ATTR               new_attribute_types_oids

 L. 281       176  LOAD_DEREF               'self'
              178  LOAD_ATTR                new_attribute_types_oids
              180  LOAD_METHOD              update
              182  LOAD_FAST                'new_attribute_types'
              184  LOAD_CONST               0
              186  BINARY_SUBSCR    
              188  LOAD_METHOD              keys
              190  CALL_METHOD_0         0  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 282       196  LOAD_DEREF               'self'
              198  LOAD_ATTR                new_attribute_types_oids
              200  LOAD_METHOD              update
              202  LOAD_FAST                'new_attribute_types'
              204  LOAD_CONST               1
              206  BINARY_SUBSCR    
              208  LOAD_METHOD              keys
              210  CALL_METHOD_0         0  ''
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 283       216  LOAD_GLOBAL              list
              218  LOAD_FAST                'old_attribute_types'
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_METHOD              keys
              226  CALL_METHOD_0         0  ''
              228  CALL_FUNCTION_1       1  ''
              230  LOAD_GLOBAL              list
              232  LOAD_FAST                'old_attribute_types'
              234  LOAD_CONST               1
              236  BINARY_SUBSCR    
              238  LOAD_METHOD              keys
              240  CALL_METHOD_0         0  ''
              242  CALL_FUNCTION_1       1  ''
              244  BINARY_ADD       
              246  GET_ITER         
              248  FOR_ITER            294  'to 294'
              250  STORE_FAST               'at_oid'

 L. 284       252  SETUP_FINALLY       270  'to 270'

 L. 285       254  LOAD_DEREF               'self'
              256  LOAD_ATTR                new_attribute_types_oids
              258  LOAD_METHOD              remove
              260  LOAD_FAST                'at_oid'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
              266  POP_BLOCK        
              268  JUMP_BACK           248  'to 248'
            270_0  COME_FROM_FINALLY   252  '252'

 L. 286       270  DUP_TOP          
              272  LOAD_GLOBAL              KeyError
              274  COMPARE_OP               exception-match
          276_278  POP_JUMP_IF_FALSE   290  'to 290'
              280  POP_TOP          
              282  POP_TOP          
              284  POP_TOP          

 L. 287       286  POP_EXCEPT       
              288  JUMP_BACK           248  'to 248'
            290_0  COME_FROM           276  '276'
              290  END_FINALLY      
              292  JUMP_BACK           248  'to 248'

Parse error at or near `LOAD_SETCOMP' instruction at offset 92

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
        f = BytesIO
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

    def ExpertOCFields--- This code section failed: ---

 L. 665         0  LOAD_GLOBAL              web2ldap
                2  LOAD_ATTR                app
                4  LOAD_ATTR                schema
                6  LOAD_METHOD              object_class_categories
                8  LOAD_DEREF               'app'
               10  LOAD_ATTR                schema
               12  LOAD_DEREF               'all_oc'
               14  CALL_METHOD_2         2  ''
               16  UNPACK_SEQUENCE_3     3 
               18  STORE_FAST               'all_structural_oc'
               20  STORE_FAST               'all_abstract_oc'
               22  STORE_FAST               'all_auxiliary_oc'

 L. 666        24  LOAD_STR                 ''
               26  STORE_FAST               'dit_structure_rule_html'

 L. 668        28  LOAD_DEREF               'get_possible_soc'
               30  LOAD_DEREF               'app'
               32  LOAD_FAST                'parent_dn'
               34  CALL_FUNCTION_2       2  ''
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'restricted_structural_oc'
               40  STORE_FAST               'dit_structure_rule_html'

 L. 669        42  LOAD_FAST                'restricted_structural_oc'
               44  JUMP_IF_TRUE_OR_POP    48  'to 48'
               46  LOAD_FAST                'all_structural_oc'
             48_0  COME_FROM            44  '44'
               48  STORE_FAST               'all_structural_oc'

 L. 671        50  LOAD_GLOBAL              set
               52  LOAD_DEREF               'existing_object_classes'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'existing_misc_oc'

 L. 672        58  LOAD_DEREF               'existing_structural_oc'
               60  LOAD_DEREF               'existing_abstract_oc'
               62  BINARY_ADD       
               64  LOAD_DEREF               'existing_auxiliary_oc'
               66  BINARY_ADD       
               68  GET_ITER         
               70  FOR_ITER             86  'to 86'
               72  STORE_FAST               'a'

 L. 673        74  LOAD_FAST                'existing_misc_oc'
               76  LOAD_METHOD              discard
               78  LOAD_FAST                'a'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            70  'to 70'

 L. 674        86  LOAD_GLOBAL              list
               88  LOAD_FAST                'existing_misc_oc'
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'existing_misc_oc'

 L. 676        94  LOAD_STR                 ''
               96  STORE_FAST               'dit_content_rule_html'

 L. 678        98  LOAD_DEREF               'existing_object_classes'
              100  POP_JUMP_IF_FALSE   250  'to 250'
              102  LOAD_DEREF               'structural_object_class'
              104  POP_JUMP_IF_FALSE   250  'to 250'

 L. 680       106  LOAD_DEREF               'app'
              108  LOAD_ATTR                schema
              110  LOAD_ATTR                name2oid
              112  LOAD_GLOBAL              ObjectClass
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              get
              118  LOAD_DEREF               'structural_object_class'
              120  LOAD_DEREF               'structural_object_class'
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'soc_oid'

 L. 681       126  LOAD_DEREF               'app'
              128  LOAD_ATTR                schema
              130  LOAD_METHOD              get_obj
              132  LOAD_GLOBAL              DITContentRule
              134  LOAD_FAST                'soc_oid'
              136  LOAD_CONST               None
              138  CALL_METHOD_3         3  ''
              140  STORE_FAST               'dit_content_rule'

 L. 682       142  LOAD_FAST                'dit_content_rule'
              144  LOAD_CONST               None
              146  COMPARE_OP               is-not
              148  POP_JUMP_IF_FALSE   250  'to 250'

 L. 683       150  LOAD_FAST                'dit_content_rule'
              152  LOAD_ATTR                obsolete
              154  POP_JUMP_IF_FALSE   162  'to 162'

 L. 684       156  LOAD_STR                 'Ignored obsolete'
              158  STORE_FAST               'dit_content_rule_status_text'
              160  JUMP_FORWARD        220  'to 220'
            162_0  COME_FROM           154  '154'

 L. 685       162  LOAD_DEREF               'app'
              164  LOAD_ATTR                ls
              166  LOAD_ATTR                relax_rules
              168  POP_JUMP_IF_FALSE   176  'to 176'

 L. 686       170  LOAD_STR                 'Ignored'
              172  STORE_FAST               'dit_content_rule_status_text'
              174  JUMP_FORWARD        220  'to 220'
            176_0  COME_FROM           168  '168'

 L. 688       176  LOAD_STR                 'Governed by'
              178  STORE_FAST               'dit_content_rule_status_text'

 L. 689       180  LOAD_CLOSURE             'app'
              182  BUILD_TUPLE_1         1 
              184  LOAD_SETCOMP             '<code_object <setcomp>>'
              186  LOAD_STR                 'ObjectClassForm.<locals>.ExpertOCFields.<locals>.<setcomp>'
              188  MAKE_FUNCTION_8          'closure'

 L. 691       190  LOAD_FAST                'dit_content_rule'
              192  LOAD_ATTR                aux

 L. 689       194  GET_ITER         
              196  CALL_FUNCTION_1       1  ''
              198  STORE_DEREF              'all_auxiliary_oc_oids'

 L. 693       200  LOAD_CLOSURE             'all_auxiliary_oc_oids'
              202  LOAD_CLOSURE             'app'
              204  BUILD_TUPLE_2         2 
              206  LOAD_LISTCOMP            '<code_object <listcomp>>'
              208  LOAD_STR                 'ObjectClassForm.<locals>.ExpertOCFields.<locals>.<listcomp>'
              210  MAKE_FUNCTION_8          'closure'

 L. 695       212  LOAD_FAST                'all_auxiliary_oc'

 L. 693       214  GET_ITER         
              216  CALL_FUNCTION_1       1  ''
              218  STORE_FAST               'all_auxiliary_oc'
            220_0  COME_FROM           174  '174'
            220_1  COME_FROM           160  '160'

 L. 698       220  LOAD_STR                 '%s<br>DIT content rule:<br>%s'

 L. 699       222  LOAD_FAST                'dit_content_rule_status_text'

 L. 700       224  LOAD_GLOBAL              schema_anchor

 L. 701       226  LOAD_DEREF               'app'

 L. 702       228  LOAD_FAST                'dit_content_rule'
              230  LOAD_ATTR                names
              232  LOAD_CONST               0
              234  BINARY_SUBSCR    

 L. 703       236  LOAD_GLOBAL              DITContentRule

 L. 704       238  LOAD_STR                 '&raquo'

 L. 700       240  LOAD_CONST               ('link_text',)
              242  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 698       244  BUILD_TUPLE_2         2 
              246  BINARY_MODULO    
              248  STORE_FAST               'dit_content_rule_html'
            250_0  COME_FROM           148  '148'
            250_1  COME_FROM           104  '104'
            250_2  COME_FROM           100  '100'

 L. 708       250  LOAD_GLOBAL              web2ldap
              252  LOAD_ATTR                app
              254  LOAD_ATTR                form
              256  LOAD_ATTR                ObjectClassSelect

 L. 709       258  LOAD_STR                 'in_oc'

 L. 710       260  LOAD_STR                 'Abstract object class(es)'

 L. 711       262  LOAD_FAST                'all_abstract_oc'

 L. 712       264  LOAD_DEREF               'existing_abstract_oc'

 L. 713       266  LOAD_CONST               20

 L. 708       268  LOAD_CONST               ('name', 'text', 'options', 'default', 'size')
              270  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              272  STORE_FAST               'abstract_select_field'

 L. 715       274  LOAD_GLOBAL              web2ldap
              276  LOAD_ATTR                app
              278  LOAD_ATTR                form
              280  LOAD_ATTR                ObjectClassSelect

 L. 716       282  LOAD_STR                 'in_oc'

 L. 717       284  LOAD_STR                 'Structural object class(es)'

 L. 718       286  LOAD_FAST                'all_structural_oc'

 L. 719       288  LOAD_DEREF               'existing_structural_oc'

 L. 720       290  LOAD_CONST               20

 L. 715       292  LOAD_CONST               ('name', 'text', 'options', 'default', 'size')
              294  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              296  STORE_FAST               'structural_select_field'

 L. 722       298  LOAD_GLOBAL              web2ldap
              300  LOAD_ATTR                app
              302  LOAD_ATTR                form
              304  LOAD_ATTR                ObjectClassSelect

 L. 723       306  LOAD_STR                 'in_oc'

 L. 724       308  LOAD_STR                 'Auxiliary object class(es)'

 L. 725       310  LOAD_FAST                'all_auxiliary_oc'

 L. 726       312  LOAD_DEREF               'existing_auxiliary_oc'

 L. 727       314  LOAD_CONST               20

 L. 722       316  LOAD_CONST               ('name', 'text', 'options', 'default', 'size')
              318  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              320  STORE_FAST               'auxiliary_select_field'

 L. 729       322  LOAD_GLOBAL              web2ldap
              324  LOAD_ATTR                app
              326  LOAD_ATTR                form
              328  LOAD_ATTR                ObjectClassSelect

 L. 730       330  LOAD_STR                 'in_oc'

 L. 731       332  LOAD_STR                 'Misc. object class(es)'

 L. 732       334  BUILD_LIST_0          0 

 L. 733       336  LOAD_FAST                'existing_misc_oc'

 L. 734       338  LOAD_CONST               20

 L. 729       340  LOAD_CONST               ('name', 'text', 'options', 'default', 'size')
              342  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              344  STORE_FAST               'misc_select_field'

 L. 736       346  LOAD_FAST                'existing_misc_oc'
          348_350  POP_JUMP_IF_FALSE   374  'to 374'

 L. 737       352  LOAD_STR                 '<th><label for="add_misc_oc">Misc.<label></th>'
              354  STORE_FAST               'misc_select_field_th'

 L. 738       356  LOAD_STR                 '<td>%s</td>'
              358  LOAD_FAST                'misc_select_field'
              360  LOAD_ATTR                input_html
              362  LOAD_STR                 'add_misc_oc'
              364  LOAD_CONST               ('id_value',)
              366  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              368  BINARY_MODULO    
              370  STORE_FAST               'misc_select_field_td'
              372  JUMP_FORWARD        382  'to 382'
            374_0  COME_FROM           348  '348'

 L. 740       374  LOAD_STR                 ''
              376  STORE_FAST               'misc_select_field_th'

 L. 741       378  LOAD_STR                 ''
              380  STORE_FAST               'misc_select_field_td'
            382_0  COME_FROM           372  '372'

 L. 743       382  LOAD_DEREF               'app'
              384  LOAD_ATTR                form
              386  LOAD_METHOD              getInputValue
              388  LOAD_STR                 'in_oft'
              390  LOAD_STR                 'Template'
              392  BUILD_LIST_1          1 
              394  CALL_METHOD_2         2  ''
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  STORE_FAST               'input_currentformtype'

 L. 745       402  LOAD_FAST                'structural_select_field'
              404  LOAD_ATTR                input_html

 L. 746       406  LOAD_STR                 'add_structural_oc'

 L. 747       408  LOAD_STR                 'Structural object classes to be added'

 L. 745       410  LOAD_CONST               ('id_value', 'title')
              412  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              414  STORE_FAST               'add_structural_oc_html'

 L. 749       416  LOAD_FAST                'auxiliary_select_field'
              418  LOAD_ATTR                input_html

 L. 750       420  LOAD_STR                 'add_auxiliary_oc'

 L. 751       422  LOAD_STR                 'Auxiliary object classes to be added'

 L. 749       424  LOAD_CONST               ('id_value', 'title')
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  STORE_FAST               'add_auxiliary_oc_html'

 L. 753       430  LOAD_FAST                'abstract_select_field'
              432  LOAD_ATTR                input_html

 L. 754       434  LOAD_STR                 'add_abstract_oc'

 L. 755       436  LOAD_STR                 'Abstract object classes to be added'

 L. 753       438  LOAD_CONST               ('id_value', 'title')
              440  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              442  STORE_FAST               'add_abstract_oc_html'

 L. 757       444  LOAD_STR                 '\n          <p>\n            <label for="input_formtype">Form type:</label> %s\n            <input type="submit" value="Next &gt;&gt;">\n          </p>\n          <table>\n            <tr>\n              <th><label for="add_structural_oc">Structural</label></th>\n              <th><label for="add_auxiliary_oc">Auxiliary</label></th>\n              <th><label for="add_abstract_oc">Abstract</label></th>\n              %s\n            </tr>\n            <tr>\n              <td><label for="add_structural_oc">%s</label></td>\n              <td><label for="add_auxiliary_oc">%s</label></td>\n              <td><label for="add_abstract_oc">%s</label></td>\n              %s\n            </tr>\n            <tr>\n              <td>%s</td>\n              <td>%s</td>\n              <td>&nbsp;</td>\n            </tr>\n          </table>\n        %s\n        '

 L. 783       446  LOAD_DEREF               'app'
              448  LOAD_ATTR                form
              450  LOAD_ATTR                field
              452  LOAD_STR                 'in_ft'
              454  BINARY_SUBSCR    
              456  LOAD_ATTR                input_html
              458  LOAD_FAST                'input_currentformtype'
              460  LOAD_CONST               ('default',)
              462  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 784       464  LOAD_FAST                'misc_select_field_th'

 L. 785       466  LOAD_FAST                'add_structural_oc_html'

 L. 786       468  LOAD_FAST                'add_auxiliary_oc_html'

 L. 787       470  LOAD_FAST                'add_abstract_oc_html'

 L. 788       472  LOAD_FAST                'misc_select_field_td'

 L. 789       474  LOAD_FAST                'dit_structure_rule_html'

 L. 790       476  LOAD_FAST                'dit_content_rule_html'

 L. 791       478  LOAD_DEREF               'app'
              480  LOAD_ATTR                form
              482  LOAD_ATTR                hiddenInputHTML

 L. 792       484  LOAD_CONST               ('dn', 'add_clonedn', 'in_ocf', 'in_oft', 'in_ft', 'in_wrtattroids')

 L. 791       486  LOAD_CONST               ('ignoreFieldNames',)
              488  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 782       490  BUILD_TUPLE_9         9 

 L. 757       492  BINARY_MODULO    
              494  STORE_FAST               'add_template_field_html'

 L. 803       496  LOAD_STR                 'Choose object class(es) for new entry.'

 L. 804       498  LOAD_STR                 'You may change the object class(es) for the entry.'

 L. 802       500  LOAD_CONST               ('add', 'modify')
              502  BUILD_CONST_KEY_MAP_2     2 

 L. 805       504  LOAD_DEREF               'app'
              506  LOAD_ATTR                command

 L. 802       508  BINARY_SUBSCR    
              510  STORE_FAST               'Msg'

 L. 806       512  LOAD_STR                 '<p class="WarningMessage">%s</p>'
              514  LOAD_FAST                'Msg'
              516  BINARY_MODULO    
              518  STORE_FAST               'Msg'

 L. 807       520  LOAD_FAST                'Msg'
              522  LOAD_FAST                'add_template_field_html'
              524  BUILD_TUPLE_2         2 
              526  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 184

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
             72_0  COME_FROM           400  '400'
             72_1  COME_FROM           392  '392'
            72_74  FOR_ITER            456  'to 456'
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
              126  POP_JUMP_IF_FALSE   236  'to 236'

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

 L. 836       212  LOAD_CLOSURE             'parent_entry'
              214  BUILD_TUPLE_1         1 
              216  LOAD_SETCOMP             '<code_object <setcomp>>'
              218  LOAD_STR                 'ObjectClassForm.<locals>.LDIFTemplateField.<locals>.<setcomp>'
              220  MAKE_FUNCTION_8          'closure'

 L. 838       222  LOAD_FAST                'addform_parent_attrs'

 L. 836       224  GET_ITER         
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'missing_parent_attrs'

 L. 841       230  LOAD_FAST                'missing_parent_attrs'
              232  POP_JUMP_IF_FALSE   236  'to 236'

 L. 842       234  JUMP_BACK            72  'to 72'
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           126  '126'

 L. 843       236  LOAD_DEREF               'get_possible_soc'
              238  LOAD_FAST                'app'
              240  LOAD_FAST                'tmpl_parent_dn'
              242  CALL_FUNCTION_2       2  ''
              244  UNPACK_SEQUENCE_2     2 
              246  STORE_FAST               'restricted_structural_oc'
              248  STORE_FAST               'dit_structure_rule_html'

 L. 844       250  LOAD_FAST                'app'
              252  LOAD_ATTR                schema
              254  LOAD_ATTR                sed
              256  LOAD_GLOBAL              DITStructureRule
              258  BINARY_SUBSCR    
          260_262  POP_JUMP_IF_FALSE   314  'to 314'

 L. 845       264  LOAD_FAST                'app'
              266  LOAD_ATTR                ls
              268  LOAD_METHOD              get_governing_structure_rule
              270  LOAD_FAST                'tmpl_parent_dn'
              272  LOAD_FAST                'app'
              274  LOAD_ATTR                schema
              276  CALL_METHOD_2         2  ''
              278  STORE_FAST               'parent_gov_structure_rule'

 L. 846       280  LOAD_FAST                'parent_gov_structure_rule'
              282  LOAD_CONST               None
              284  COMPARE_OP               is
          286_288  POP_JUMP_IF_FALSE   302  'to 302'

 L. 847       290  LOAD_FAST                'restricted_structural_oc'
          292_294  JUMP_IF_TRUE_OR_POP   298  'to 298'
              296  LOAD_FAST                'all_structural_oc'
            298_0  COME_FROM           292  '292'
              298  STORE_FAST               'restricted_structural_oc'
              300  JUMP_FORWARD        312  'to 312'
            302_0  COME_FROM           286  '286'

 L. 849       302  LOAD_FAST                'restricted_structural_oc'
          304_306  JUMP_IF_TRUE_OR_POP   310  'to 310'
              308  BUILD_LIST_0          0 
            310_0  COME_FROM           304  '304'
              310  STORE_FAST               'restricted_structural_oc'
            312_0  COME_FROM           300  '300'
              312  JUMP_FORWARD        318  'to 318'
            314_0  COME_FROM           260  '260'

 L. 851       314  LOAD_FAST                'all_structural_oc'
              316  STORE_FAST               'restricted_structural_oc'
            318_0  COME_FROM           312  '312'

 L. 852       318  LOAD_GLOBAL              ldap0
              320  LOAD_ATTR                schema
              322  LOAD_ATTR                models
              324  LOAD_METHOD              SchemaElementOIDSet

 L. 853       326  LOAD_FAST                'app'
              328  LOAD_ATTR                schema

 L. 854       330  LOAD_GLOBAL              ObjectClass

 L. 855       332  LOAD_FAST                'restricted_structural_oc'

 L. 852       334  CALL_METHOD_3         3  ''
              336  STORE_FAST               'restricted_structural_oc_set'

 L. 857       338  LOAD_GLOBAL              ldap0
              340  LOAD_ATTR                schema
              342  LOAD_ATTR                models
              344  LOAD_METHOD              Entry

 L. 858       346  LOAD_FAST                'app'
              348  LOAD_ATTR                schema

 L. 859       350  LOAD_FAST                'ldif_dn'
              352  LOAD_METHOD              decode
              354  LOAD_FAST                'app'
              356  LOAD_ATTR                ls
              358  LOAD_ATTR                charset
              360  CALL_METHOD_1         1  ''

 L. 860       362  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              364  LOAD_STR                 'ObjectClassForm.<locals>.LDIFTemplateField.<locals>.<dictcomp>'
              366  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              368  LOAD_FAST                'ldif_entry'
              370  LOAD_METHOD              items
              372  CALL_METHOD_0         0  ''
              374  GET_ITER         
              376  CALL_FUNCTION_1       1  ''

 L. 857       378  CALL_METHOD_3         3  ''
              380  STORE_FAST               'entry'

 L. 862       382  LOAD_FAST                'entry'
              384  LOAD_METHOD              get_structural_oc
              386  CALL_METHOD_0         0  ''
              388  STORE_FAST               'soc'

 L. 863       390  LOAD_FAST                'soc'
              392  POP_JUMP_IF_FALSE    72  'to 72'
              394  LOAD_FAST                'soc'
              396  LOAD_FAST                'restricted_structural_oc_set'
              398  COMPARE_OP               in
              400  POP_JUMP_IF_FALSE    72  'to 72'

 L. 864       402  SETUP_FINALLY       422  'to 422'

 L. 865       404  LOAD_FAST                'add_tmpl_dict'
              406  LOAD_FAST                'tmpl_parent_dn'
              408  BINARY_SUBSCR    
              410  LOAD_METHOD              append
              412  LOAD_FAST                'template_name'
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          
              418  POP_BLOCK        
              420  JUMP_BACK            72  'to 72'
            422_0  COME_FROM_FINALLY   402  '402'

 L. 866       422  DUP_TOP          
              424  LOAD_GLOBAL              KeyError
              426  COMPARE_OP               exception-match
          428_430  POP_JUMP_IF_FALSE   452  'to 452'
              432  POP_TOP          
              434  POP_TOP          
              436  POP_TOP          

 L. 867       438  LOAD_FAST                'template_name'
              440  BUILD_LIST_1          1 
              442  LOAD_FAST                'add_tmpl_dict'
              444  LOAD_FAST                'tmpl_parent_dn'
              446  STORE_SUBSCR     
              448  POP_EXCEPT       
              450  JUMP_BACK            72  'to 72'
            452_0  COME_FROM           428  '428'
              452  END_FINALLY      
              454  JUMP_BACK            72  'to 72'

 L. 868       456  LOAD_FAST                'add_tmpl_dict'
          458_460  POP_JUMP_IF_TRUE    496  'to 496'

 L. 870       462  LOAD_STR                 '<p class="ErrorMessage">No usable LDIF templates here. Wrong %s?</p>'

 L. 871       464  LOAD_FAST                'app'
              466  LOAD_ATTR                anchor

 L. 872       468  LOAD_STR                 'dit'

 L. 872       470  LOAD_STR                 'sub-tree'

 L. 873       472  LOAD_STR                 'dn'
              474  LOAD_FAST                'app'
              476  LOAD_ATTR                dn
              478  BUILD_TUPLE_2         2 
              480  BUILD_LIST_1          1 

 L. 874       482  LOAD_STR                 'browse directory tree'

 L. 871       484  LOAD_CONST               ('title',)
              486  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 870       488  BINARY_MODULO    

 L. 877       490  LOAD_STR                 ''

 L. 869       492  BUILD_TUPLE_2         2 
              494  RETURN_VALUE     
            496_0  COME_FROM           458  '458'

 L. 879       496  LOAD_STR                 '<dl>'
              498  BUILD_LIST_1          1 
              500  STORE_FAST               'add_template_html_list'

 L. 880       502  LOAD_GLOBAL              sorted
              504  LOAD_FAST                'add_tmpl_dict'
              506  LOAD_METHOD              keys
              508  CALL_METHOD_0         0  ''
              510  CALL_FUNCTION_1       1  ''
              512  GET_ITER         
              514  FOR_ITER            642  'to 642'
              516  STORE_FAST               'pdn'

 L. 881       518  LOAD_FAST                'add_template_html_list'
              520  LOAD_METHOD              append
              522  LOAD_STR                 '<dt>%s<dt>'

 L. 882       524  LOAD_GLOBAL              SupentryDisplayString
              526  LOAD_FAST                'app'
              528  LOAD_FAST                'pdn'
              530  LOAD_STR                 '%s'
              532  LOAD_CONST               ('supentry_display_tmpl',)
              534  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L. 881       536  BUILD_TUPLE_1         1 
              538  BINARY_MODULO    
              540  CALL_METHOD_1         1  ''
              542  POP_TOP          

 L. 884       544  LOAD_FAST                'add_template_html_list'
              546  LOAD_METHOD              append
              548  LOAD_STR                 '<dd><ul>'
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          

 L. 885       554  LOAD_FAST                'add_tmpl_dict'
              556  LOAD_FAST                'pdn'
              558  BINARY_SUBSCR    
              560  GET_ITER         
              562  FOR_ITER            628  'to 628'
              564  STORE_FAST               'tmpl_name'

 L. 886       566  LOAD_FAST                'add_template_html_list'
              568  LOAD_METHOD              append

 L. 887       570  LOAD_STR                 '<li>%s</li>'

 L. 888       572  LOAD_FAST                'app'
              574  LOAD_ATTR                anchor

 L. 889       576  LOAD_STR                 'add'

 L. 889       578  LOAD_FAST                'app'
              580  LOAD_ATTR                form
              582  LOAD_METHOD              utf2display
              584  LOAD_FAST                'tmpl_name'
              586  CALL_METHOD_1         1  ''

 L. 891       588  LOAD_STR                 'dn'
              590  LOAD_FAST                'pdn'
              592  BUILD_TUPLE_2         2 

 L. 892       594  LOAD_STR                 'add_template'
              596  LOAD_FAST                'tmpl_name'
              598  BUILD_TUPLE_2         2 

 L. 893       600  LOAD_CONST               ('in_ft', 'Template')

 L. 890       602  BUILD_LIST_3          3 

 L. 895       604  LOAD_STR                 'Add entry beneath %s\nbased on template "%s"'
              606  LOAD_FAST                'pdn'
              608  LOAD_FAST                'tmpl_name'
              610  BUILD_TUPLE_2         2 
              612  BINARY_MODULO    

 L. 888       614  LOAD_CONST               ('title',)
              616  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 887       618  BINARY_MODULO    

 L. 886       620  CALL_METHOD_1         1  ''
              622  POP_TOP          
          624_626  JUMP_BACK           562  'to 562'

 L. 899       628  LOAD_FAST                'add_template_html_list'
              630  LOAD_METHOD              append
              632  LOAD_STR                 '</ul></dd>'
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          
          638_640  JUMP_BACK           514  'to 514'

 L. 900       642  LOAD_FAST                'add_template_html_list'
              644  LOAD_METHOD              append
              646  LOAD_STR                 '</dl>'
              648  CALL_METHOD_1         1  ''
              650  POP_TOP          

 L. 901       652  LOAD_STR                 '\n'
              654  LOAD_METHOD              join
              656  LOAD_FAST                'add_template_html_list'
              658  CALL_METHOD_1         1  ''
              660  STORE_FAST               'add_template_field_html'

 L. 902       662  LOAD_STR                 '<p class="WarningMessage">Choose a LDIF template and base DN for new entry</p>'
              664  STORE_FAST               'Msg'

 L. 903       666  LOAD_FAST                'Msg'
              668  LOAD_FAST                'add_template_field_html'
              670  BUILD_TUPLE_2         2 
              672  RETURN_VALUE     
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


def w2l_modifyform--- This code section failed: ---

 L.1263         0  LOAD_FAST                'msg'
                2  POP_JUMP_IF_FALSE    12  'to 12'

 L.1264         4  LOAD_STR                 '<p class="ErrorMessage">%s</p>'
                6  LOAD_FAST                'msg'
                8  BINARY_MODULO    
               10  STORE_FAST               'msg'
             12_0  COME_FROM             2  '2'

 L.1266        12  LOAD_DEREF               'app'
               14  LOAD_ATTR                form
               16  LOAD_METHOD              getInputValue

 L.1267        18  LOAD_STR                 'in_ft'

 L.1268        20  LOAD_DEREF               'app'
               22  LOAD_ATTR                form
               24  LOAD_METHOD              getInputValue
               26  LOAD_STR                 'in_oft'
               28  LOAD_STR                 'Template'
               30  BUILD_LIST_1          1 
               32  CALL_METHOD_2         2  ''

 L.1266        34  CALL_METHOD_2         2  ''

 L.1269        36  LOAD_CONST               0

 L.1266        38  BINARY_SUBSCR    
               40  STORE_FAST               'input_formtype'

 L.1271        42  LOAD_STR                 'in_oc'
               44  LOAD_DEREF               'app'
               46  LOAD_ATTR                form
               48  LOAD_ATTR                input_field_names
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    82  'to 82'

 L.1273        54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 'w2l_modifyform.<locals>.<listcomp>'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               60  LOAD_DEREF               'app'
               62  LOAD_ATTR                form
               64  LOAD_ATTR                field
               66  LOAD_STR                 'in_oc'
               68  BINARY_SUBSCR    
               70  LOAD_ATTR                value
               72  GET_ITER         
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'entry'
               78  LOAD_STR                 'objectClass'
               80  STORE_SUBSCR     
             82_0  COME_FROM            52  '52'

 L.1275        82  LOAD_GLOBAL              read_old_entry
               84  LOAD_DEREF               'app'
               86  LOAD_DEREF               'app'
               88  LOAD_ATTR                dn
               90  LOAD_DEREF               'app'
               92  LOAD_ATTR                schema
               94  LOAD_CONST               None
               96  CALL_FUNCTION_4       4  ''
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'old_entry'
              102  STORE_FAST               'read_writeable_attr_oids'

 L.1276       104  LOAD_FAST                'entry'
              106  POP_JUMP_IF_TRUE    112  'to 112'

 L.1277       108  LOAD_FAST                'old_entry'
              110  STORE_FAST               'entry'
            112_0  COME_FROM           106  '106'

 L.1279       112  LOAD_DEREF               'app'
              114  LOAD_ATTR                form
              116  LOAD_METHOD              getInputValue
              118  LOAD_STR                 'in_wrtattroids'
              120  BUILD_LIST_0          0 
              122  CALL_METHOD_2         2  ''
              124  STORE_FAST               'in_wrtattroids'

 L.1280       126  LOAD_FAST                'in_wrtattroids'
              128  LOAD_STR                 'nonePseudoValue;x-web2ldap-None'
              130  BUILD_LIST_1          1 
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   142  'to 142'

 L.1281       136  LOAD_CONST               None
              138  STORE_FAST               'writeable_attr_oids'
              140  JUMP_FORWARD        170  'to 170'
            142_0  COME_FROM           134  '134'

 L.1282       142  LOAD_FAST                'in_wrtattroids'
              144  POP_JUMP_IF_FALSE   166  'to 166'

 L.1283       146  LOAD_CLOSURE             'app'
              148  BUILD_TUPLE_1         1 
              150  LOAD_SETCOMP             '<code_object <setcomp>>'
              152  LOAD_STR                 'w2l_modifyform.<locals>.<setcomp>'
              154  MAKE_FUNCTION_8          'closure'
              156  LOAD_FAST                'in_wrtattroids'
              158  GET_ITER         
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'writeable_attr_oids'
              164  JUMP_FORWARD        170  'to 170'
            166_0  COME_FROM           144  '144'

 L.1285       166  LOAD_FAST                'read_writeable_attr_oids'
              168  STORE_FAST               'writeable_attr_oids'
            170_0  COME_FROM           164  '164'
            170_1  COME_FROM           140  '140'

 L.1287       170  LOAD_FAST                'input_formtype'
              172  LOAD_STR                 'OC'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   208  'to 208'

 L.1289       178  LOAD_GLOBAL              ObjectClassForm
              180  LOAD_DEREF               'app'
              182  LOAD_GLOBAL              decode_list
              184  LOAD_FAST                'entry'
              186  LOAD_STR                 'objectClass'
              188  BINARY_SUBSCR    
              190  LOAD_STR                 'ascii'
              192  CALL_FUNCTION_2       2  ''
              194  LOAD_FAST                'entry'
              196  LOAD_METHOD              get_structural_oc
              198  CALL_METHOD_0         0  ''
              200  CALL_FUNCTION_3       3  ''
              202  POP_TOP          

 L.1290       204  LOAD_CONST               None
              206  RETURN_VALUE     
            208_0  COME_FROM           176  '176'

 L.1292       208  LOAD_GLOBAL              decode_list
              210  LOAD_FAST                'entry'
              212  LOAD_STR                 'objectClass'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               None
              218  LOAD_CONST               None
              220  BUILD_SLICE_2         2 
              222  BINARY_SUBSCR    
              224  LOAD_STR                 'ascii'
              226  LOAD_CONST               ('encoding',)
              228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              230  STORE_FAST               'existing_object_classes'

 L.1294       232  LOAD_GLOBAL              InputFormEntry

 L.1295       234  LOAD_DEREF               'app'

 L.1295       236  LOAD_DEREF               'app'
              238  LOAD_ATTR                dn

 L.1295       240  LOAD_DEREF               'app'
              242  LOAD_ATTR                schema

 L.1296       244  LOAD_FAST                'entry'

 L.1296       246  LOAD_FAST                'writeable_attr_oids'

 L.1296       248  LOAD_FAST                'existing_object_classes'

 L.1296       250  LOAD_FAST                'invalid_attrs'

 L.1294       252  LOAD_CONST               ('invalid_attrs',)
              254  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              256  STORE_FAST               'input_form_entry'

 L.1298       258  LOAD_FAST                'input_form_entry'
              260  LOAD_METHOD              attribute_types
              262  CALL_METHOD_0         0  ''
              264  UNPACK_SEQUENCE_2     2 
              266  STORE_FAST               'required_attrs_dict'
              268  STORE_FAST               'allowed_attrs_dict'

 L.1299       270  LOAD_GLOBAL              nomatching_attrs
              272  LOAD_DEREF               'app'
              274  LOAD_ATTR                schema
              276  LOAD_FAST                'input_form_entry'
              278  LOAD_FAST                'allowed_attrs_dict'
              280  LOAD_FAST                'required_attrs_dict'
              282  CALL_FUNCTION_4       4  ''
              284  STORE_FAST               'nomatching_attrs_dict'

 L.1301       286  LOAD_GLOBAL              SupentryDisplayString
              288  LOAD_DEREF               'app'
              290  LOAD_DEREF               'app'
              292  LOAD_ATTR                parent_dn
              294  CALL_FUNCTION_2       2  ''
              296  STORE_FAST               'supentry_display_string'

 L.1303       298  LOAD_FAST                'writeable_attr_oids'
              300  LOAD_CONST               None
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   326  'to 326'

 L.1304       308  LOAD_DEREF               'app'
              310  LOAD_ATTR                form
              312  LOAD_METHOD              hiddenFieldHTML
              314  LOAD_STR                 'in_wrtattroids'
              316  LOAD_STR                 'nonePseudoValue;x-web2ldap-None'
              318  LOAD_STR                 ''
              320  CALL_METHOD_3         3  ''
              322  STORE_FAST               'in_wrtattroids_values'
              324  JUMP_FORWARD        356  'to 356'
            326_0  COME_FROM           304  '304'

 L.1306       326  LOAD_STR                 ''
              328  LOAD_METHOD              join
              330  LOAD_CLOSURE             'app'
              332  BUILD_TUPLE_1         1 
              334  LOAD_LISTCOMP            '<code_object <listcomp>>'
              336  LOAD_STR                 'w2l_modifyform.<locals>.<listcomp>'
              338  MAKE_FUNCTION_8          'closure'

 L.1308       340  LOAD_FAST                'writeable_attr_oids'
          342_344  JUMP_IF_TRUE_OR_POP   348  'to 348'
              346  BUILD_LIST_0          0 
            348_0  COME_FROM           342  '342'

 L.1306       348  GET_ITER         
              350  CALL_FUNCTION_1       1  ''
              352  CALL_METHOD_1         1  ''
              354  STORE_FAST               'in_wrtattroids_values'
            356_0  COME_FROM           324  '324'

 L.1311       356  LOAD_DEREF               'app'
              358  LOAD_ATTR                ls
              360  LOAD_ATTR                relax_rules
          362_364  POP_JUMP_IF_FALSE   380  'to 380'

 L.1312       366  LOAD_STR                 ''
              368  LOAD_METHOD              join

 L.1313       370  LOAD_FAST                'msg'

 L.1314       372  LOAD_STR                 '<p class="WarningMessage">Relax Rules Control enabled! Be sure you know what you are doing!</p>'

 L.1312       374  BUILD_TUPLE_2         2 
              376  CALL_METHOD_1         1  ''
              378  STORE_FAST               'msg'
            380_0  COME_FROM           362  '362'

 L.1318       380  LOAD_FAST                'input_formtype'
              382  LOAD_STR                 'Template'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   458  'to 458'

 L.1319       390  LOAD_FAST                'input_form_entry'
              392  LOAD_METHOD              get_html_templates
              394  LOAD_STR                 'input_template'
              396  CALL_METHOD_1         1  ''
              398  UNPACK_SEQUENCE_2     2 
              400  STORE_FAST               'template_oc'
              402  STORE_FAST               '_'

 L.1320       404  LOAD_FAST                'template_oc'
          406_408  POP_JUMP_IF_TRUE    430  'to 430'

 L.1321       410  LOAD_STR                 ''
              412  LOAD_METHOD              join

 L.1322       414  LOAD_FAST                'msg'

 L.1323       416  LOAD_STR                 '<p class="WarningMessage">No templates defined for chosen object classes.</p>'

 L.1321       418  BUILD_TUPLE_2         2 
              420  CALL_METHOD_1         1  ''
              422  STORE_FAST               'msg'

 L.1325       424  LOAD_STR                 'Table'
              426  STORE_FAST               'input_formtype'
              428  JUMP_FORWARD        458  'to 458'
            430_0  COME_FROM           406  '406'

 L.1326       430  LOAD_DEREF               'app'
              432  LOAD_ATTR                ls
              434  LOAD_ATTR                relax_rules
          436_438  POP_JUMP_IF_FALSE   458  'to 458'

 L.1327       440  LOAD_STR                 ''
              442  LOAD_METHOD              join

 L.1328       444  LOAD_FAST                'msg'

 L.1329       446  LOAD_STR                 '<p class="WarningMessage">Forced to table input because Relax Rules Control is enabled.</p>'

 L.1327       448  BUILD_TUPLE_2         2 
              450  CALL_METHOD_1         1  ''
              452  STORE_FAST               'msg'

 L.1331       454  LOAD_STR                 'Table'
              456  STORE_FAST               'input_formtype'
            458_0  COME_FROM           436  '436'
            458_1  COME_FROM           428  '428'
            458_2  COME_FROM           386  '386'

 L.1333       458  LOAD_GLOBAL              web2ldap
              460  LOAD_ATTR                app
              462  LOAD_ATTR                gui
              464  LOAD_ATTR                top_section

 L.1334       466  LOAD_DEREF               'app'

 L.1335       468  LOAD_GLOBAL              H1_MSG
              470  LOAD_DEREF               'app'
              472  LOAD_ATTR                command
              474  BINARY_SUBSCR    

 L.1336       476  LOAD_GLOBAL              web2ldap
              478  LOAD_ATTR                app
              480  LOAD_ATTR                gui
              482  LOAD_METHOD              main_menu
              484  LOAD_DEREF               'app'
              486  CALL_METHOD_1         1  ''

 L.1337       488  BUILD_LIST_0          0 

 L.1333       490  LOAD_CONST               ('context_menu_list',)
              492  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              494  POP_TOP          

 L.1340       496  LOAD_DEREF               'app'
              498  LOAD_ATTR                outf
              500  LOAD_METHOD              write

 L.1341       502  LOAD_GLOBAL              INPUT_FORM_BEGIN_TMPL
              504  LOAD_ATTR                format

 L.1342       506  LOAD_GLOBAL              H1_MSG
              508  LOAD_DEREF               'app'
              510  LOAD_ATTR                command
              512  BINARY_SUBSCR    

 L.1343       514  LOAD_FAST                'msg'

 L.1344       516  LOAD_FAST                'supentry_display_string'

 L.1345       518  LOAD_DEREF               'app'
              520  LOAD_ATTR                begin_form
              522  LOAD_DEREF               'app'
              524  LOAD_ATTR                command
              526  LOAD_STR                 'POST'
              528  LOAD_STR                 'multipart/form-data'
              530  LOAD_CONST               ('enctype',)
              532  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.1346       534  LOAD_DEREF               'app'
              536  LOAD_ATTR                form
              538  LOAD_METHOD              hiddenFieldHTML
              540  LOAD_STR                 'dn'
              542  LOAD_DEREF               'app'
              544  LOAD_ATTR                dn
              546  LOAD_STR                 ''
              548  CALL_METHOD_3         3  ''

 L.1347       550  LOAD_DEREF               'app'
              552  LOAD_ATTR                form
              554  LOAD_METHOD              hiddenFieldHTML
              556  LOAD_STR                 'in_oft'
              558  LOAD_FAST                'input_formtype'
              560  LOAD_STR                 ''
              562  CALL_METHOD_3         3  ''

 L.1341       564  LOAD_CONST               ('text_heading', 'text_msg', 'text_supentry', 'form_begin', 'field_dn', 'field_currentformtype')
              566  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'

 L.1340       568  CALL_METHOD_1         1  ''
              570  POP_TOP          

 L.1351       572  LOAD_DEREF               'app'
              574  LOAD_ATTR                outf
              576  LOAD_METHOD              write

 L.1352       578  LOAD_STR                 '\n'
              580  LOAD_METHOD              join

 L.1353       582  LOAD_DEREF               'app'
              584  LOAD_ATTR                form
              586  LOAD_METHOD              hiddenFieldHTML
              588  LOAD_STR                 'in_assertion'
              590  LOAD_GLOBAL              AssertionFilter
              592  LOAD_DEREF               'app'
              594  LOAD_FAST                'entry'
              596  CALL_FUNCTION_2       2  ''
              598  LOAD_STR                 ''
              600  CALL_METHOD_3         3  ''

 L.1354       602  LOAD_STR                 '\n'
              604  LOAD_METHOD              join
              606  LOAD_CLOSURE             'app'
              608  BUILD_TUPLE_1         1 
              610  LOAD_LISTCOMP            '<code_object <listcomp>>'
              612  LOAD_STR                 'w2l_modifyform.<locals>.<listcomp>'
              614  MAKE_FUNCTION_8          'closure'

 L.1356       616  LOAD_DEREF               'app'
              618  LOAD_ATTR                form
              620  LOAD_METHOD              getInputValue
              622  LOAD_STR                 'in_oldattrtypes'
              624  LOAD_FAST                'entry'
              626  LOAD_METHOD              keys
              628  CALL_METHOD_0         0  ''
              630  CALL_METHOD_2         2  ''

 L.1354       632  GET_ITER         
              634  CALL_FUNCTION_1       1  ''
              636  CALL_METHOD_1         1  ''

 L.1358       638  LOAD_FAST                'in_wrtattroids_values'

 L.1352       640  BUILD_TUPLE_3         3 
              642  CALL_METHOD_1         1  ''

 L.1351       644  CALL_METHOD_1         1  ''
              646  POP_TOP          

 L.1362       648  LOAD_FAST                'input_formtype'
              650  LOAD_STR                 'Template'
              652  COMPARE_OP               ==
          654_656  POP_JUMP_IF_FALSE   674  'to 674'

 L.1363       658  LOAD_FAST                'input_form_entry'
              660  LOAD_ATTR                template_output

 L.1364       662  LOAD_STR                 'input_template'

 L.1365       664  LOAD_CONST               False

 L.1363       666  LOAD_CONST               ('display_duplicate_attrs',)
              668  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              670  POP_TOP          
              672  JUMP_FORWARD        732  'to 732'
            674_0  COME_FROM           654  '654'

 L.1368       674  LOAD_FAST                'input_formtype'
              676  LOAD_STR                 'Table'
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   714  'to 714'

 L.1369       684  LOAD_FAST                'input_form_entry'
              686  LOAD_METHOD              table_input

 L.1371       688  LOAD_FAST                'required_attrs_dict'
              690  LOAD_STR                 'Required attributes'
              692  BUILD_TUPLE_2         2 

 L.1372       694  LOAD_FAST                'allowed_attrs_dict'
              696  LOAD_STR                 'Allowed attributes'
              698  BUILD_TUPLE_2         2 

 L.1373       700  LOAD_FAST                'nomatching_attrs_dict'
              702  LOAD_STR                 'Other attributes'
              704  BUILD_TUPLE_2         2 

 L.1370       706  BUILD_TUPLE_3         3 

 L.1369       708  CALL_METHOD_1         1  ''
              710  POP_TOP          
              712  JUMP_FORWARD        732  'to 732'
            714_0  COME_FROM           680  '680'

 L.1377       714  LOAD_FAST                'input_formtype'
              716  LOAD_STR                 'LDIF'
              718  COMPARE_OP               ==
          720_722  POP_JUMP_IF_FALSE   732  'to 732'

 L.1378       724  LOAD_FAST                'input_form_entry'
              726  LOAD_METHOD              ldif_input
              728  CALL_METHOD_0         0  ''
              730  POP_TOP          
            732_0  COME_FROM           720  '720'
            732_1  COME_FROM           712  '712'
            732_2  COME_FROM           672  '672'

 L.1380       732  LOAD_DEREF               'app'
              734  LOAD_ATTR                outf
              736  LOAD_METHOD              write
              738  LOAD_STR                 '</form>'
              740  CALL_METHOD_1         1  ''
              742  POP_TOP          

 L.1381       744  LOAD_GLOBAL              web2ldap
              746  LOAD_ATTR                app
              748  LOAD_ATTR                gui
              750  LOAD_METHOD              footer
              752  LOAD_DEREF               'app'
              754  CALL_METHOD_1         1  ''
              756  POP_TOP          

Parse error at or near `LOAD_SETCOMP' instruction at offset 150
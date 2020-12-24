# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/compiler.py
# Compiled at: 2020-04-01 07:23:01
# Size of source mod 2**32: 39612 bytes
from sqlalchemy.dialects.postgresql.base import PGExecutionContext, PGDDLCompiler
from sqlalchemy.sql import crud, selectable, util, elements, compiler, functions, operators, expression
from sqlalchemy import exc
from sqlalchemy.sql.annotation import Annotated
from sqlalchemy.sql.compiler import RESERVED_WORDS, LEGAL_CHARACTERS, ILLEGAL_INITIAL_CHARACTERS, BIND_PARAMS, BIND_PARAMS_ESC, OPERATORS, BIND_TEMPLATES, FUNCTIONS, EXTRACT_MAP, COMPOUND_KEYWORDS
from sqlalchemy.dialects import postgresql
from oedialect import error
DEFAULT_SCHEMA = 'sandbox'

class OEDDLCompiler(PGDDLCompiler):

    def __str__(self):
        return ''

    def visit_create_table(self, create):
        jsn = {'request_type':'put', 
         'command':'schema/{schema}/tables/{table}/'.format(schema=create.element.schema if create.element.schema else DEFAULT_SCHEMA,
           table=create.element.name)}
        first_pk = False
        cols = []
        for create_column in create.columns:
            column = create_column.element
            cd = {'name':column.name, 
             'is_nullable':column.nullable, 
             'data_type':self.type_compiler.process(column.type), 
             'primary_key':column.primary_key, 
             'autoincrement':column.autoincrement}
            cd['foreign_key'] = []
            for fk in column.foreign_keys:
                cd['foreign_key'].append({'schema':fk.column.table.schema, 
                 'table':fk.column.table.name, 
                 'column':fk.column.name})
            else:
                cols.append(cd)

        else:
            jsn['constraints'] = self.create_table_constraints((create.element),
              _include_foreign_key_constraints=(create.include_foreign_key_constraints))
            jsn['columns'] = cols
            return jsn

    def create_table_constraints(self, table, _include_foreign_key_constraints=None):
        constraints = []
        if table.primary_key:
            constraints.append(table.primary_key)
        else:
            all_fkcs = table.foreign_key_constraints
            if _include_foreign_key_constraints is not None:
                omit_fkcs = all_fkcs.difference(_include_foreign_key_constraints)
            else:
                omit_fkcs = set()
        constraints.extend([c for c in table._sorted_constraints if c is not table.primary_key if c not in omit_fkcs])
        return [p for p in (getattr(constraint, 'use_alter', False) or self.process(constraint) for constraint in constraints if constraint._create_rule is None or constraint._create_rule(self) if self.dialect.supports_alter) if p is not None]

    def visit_create_sequence(self, create):
        jsn = {'request_type':'put', 
         'command':'schema/{schema}/sequences/{seq}/'.format(schema=create.element.schema if create.element.schema else DEFAULT_SCHEMA,
           seq=create.element.name), 
         'requires_connection':True}
        if hasattr(create.element, 'increment'):
            if create.element.increment is not None:
                jsn['increment'] = create.element.increment
        if hasattr(create.element, 'start'):
            if create.element.start is not None:
                jsn['start'] = create.element.start
        if hasattr(create.element, 'minvalue'):
            if create.element.minvalue is not None:
                jsn['minvalue'] = create.element.minvalue
        if hasattr(create.element, 'maxvalue'):
            if create.element.maxvalue is not None:
                jsn['maxvalue'] = create.element.maxvalue
        if hasattr(create.element, 'nomaxvalue'):
            if create.element.nominvalue is not None:
                jsn['nominvalue'] = create.element.nominvalue
        if hasattr(create.element, 'nomaxvalue'):
            if create.element.nomaxvalue is not None:
                jsn['nomaxvalue'] = create.element.nomaxvalue
        if hasattr(create.element, 'cache'):
            if create.element.cache is not None:
                jsn['cache'] = create.element.cache
        if hasattr(create.element, 'order'):
            if create.element.order is True:
                jsn['order'] = create.element.order
        if hasattr(create.element, 'cycle'):
            if create.element.cycle is not None:
                jsn['cycle'] = create.element.cycle
        if hasattr(create.element, 'optional'):
            if create.element.optional is not None:
                jsn['optional'] = create.element.optional
        return jsn

    def visit_drop_sequence(self, drop):
        return {'request_type':'delete', 
         'command':'schema/{schema}/sequences/{seq}/'.format(schema=drop.element.schema if drop.element.schema else DEFAULT_SCHEMA,
           seq=drop.element.name)}

    def visit_create_column(self, create, first_pk=False):
        column = create.element
        if column.system:
            return
        jsn = self.get_column_specification(column,
          first_pk=first_pk)
        const = [self.process(constraint) for constraint in column.constraints]
        if const:
            jsn['constraints'] = const
        return jsn

    def get_column_specification(self, column, **kwargs):
        jsn = {}
        jsn['name'] = self.preparer.format_column(column)
        jsn['type'] = self.dialect.type_compiler.process((column.type), type_expression=column)
        default = self.get_column_default_string(column)
        if default is not None:
            jsn['default'] = default
        if not column.nullable:
            jsn['nullable'] = 'False'
        return jsn

    def visit_drop_table(self, drop):
        jsn = {'request_type':'delete', 
         'command':'schema/{schema}/tables/{table}/'.format(schema=drop.element.schema if drop.element.schema else DEFAULT_SCHEMA,
           table=drop.element.name)}
        return jsn

    def visit_create_index(self, create):
        pass

    def visit_primary_key_constraint(self, constraint):
        if len(constraint) == 0:
            return []
        jsn = {'constraint_type': 'primary_key'}
        if constraint.name is not None:
            jsn['name'] = self.preparer.format_constraint(constraint)
        jsn['columns'] = [c.name for c in constraint.columns_autoinc_first if constraint._implicit_generated else constraint.columns]
        return jsn

    def visit_foreign_key_constraint(self, constraint):
        preparer = self.preparer
        jsn = {'constraint_type': 'foreign_key'}
        if constraint.name is not None:
            jsn['name'] = self.preparer.format_constraint(constraint)
        remote_table = list(constraint.elements)[0].column.table
        jsn['columns'] = [f.parent.name for f in constraint.elements]
        jsn['target_table'] = self.define_constraint_remote_table(constraint, remote_table, preparer)
        jsn['target_columns'] = [f.column.name for f in constraint.elements]
        jsn['match'] = self.define_constraint_match(constraint)
        jsn['cascades'] = self.define_constraint_cascades(constraint)
        jsn['deferrable'] = self.define_constraint_deferrability(constraint)
        return jsn

    def visit_unique_constraint(self, constraint):
        jsn = {'type': 'unique'}
        if constraint.name is not None:
            jsn['name'] = self.preparer.format_constraint(constraint)
        jsn['columns'] = [c.name for c in constraint]
        jsn['deferrable'] = self.define_constraint_deferrability(constraint)
        return jsn

    def visit_column_check_constraint(self, constraint):
        raise NotImplementedError


class OECompiler(postgresql.psycopg2.PGCompiler):

    def __str__(self):
        return ''

    def visit_clauselist(self, clauselist, **kw):
        sep = clauselist.operator
        if sep is None:
            sep = ' '
        else:
            sep = OPERATORS[clauselist.operator]
        return [s for s in ((c._compiler_dispatch)(self, **kw) for c in clauselist.clauses) if s]

    def visit_unary(self, unary, **kw):
        if unary.operator:
            if unary.modifier:
                raise exc.CompileError('Unary expression does not support operator and modifier simultaneously')
            disp = self._get_operator_dispatch(unary.operator, 'unary', 'operator')
            if disp:
                return disp(unary, (unary.operator), **kw)
            return (self._generate_generic_unary_operator)(
             unary, (OPERATORS[unary.operator]), **kw)
        else:
            if unary.modifier:
                disp = self._get_operator_dispatch(unary.modifier, 'unary', 'modifier')
                if disp:
                    return disp(unary, (unary.modifier), **kw)
                return (self._generate_generic_unary_modifier)(
                 unary, (OPERATORS[unary.modifier]), **kw)
            else:
                raise exc.CompileError('Unary expression has no operator or modifier')

    def visit_grouping(self, grouping, asfrom=False, **kwargs):
        """"
        TODO:
        """
        return {'type':'grouping', 
         'grouping':grouping.element._compiler_dispatch(self, **kwargs)}

    def visit_join(self, join, asfrom=False, **kwargs):
        d = {'type': 'join'}
        if join.full:
            d['join_type'] = 'FULL OUTER JOIN'
        else:
            if join.isouter:
                d['join_type'] = 'LEFT OUTER JOIN'
            else:
                d['join_type'] = 'JOIN '
        d['left'] = (join.left._compiler_dispatch)(self, asfrom=True, **kwargs)
        d['right'] = (join.right._compiler_dispatch)(self, asfrom=True, **kwargs)
        d['on'] = (join.onclause._compiler_dispatch)(self, **kwargs)
        return d

    def bindparam_string(self, name, positional_names=None, expanding=False, **kw):
        if self.positional:
            if positional_names is not None:
                positional_names.append(name)
            else:
                self.positiontup.append(name)
        if expanding:
            raise NotImplementedError
            self.contains_expanding_parameters = True
            return '([EXPANDING_%s])' % name
        return lambda d: d[name]

    def visit_insert(self, insert_stmt, **kw):
        self.stack.append({'correlate_froms':set(), 
         'asfrom_froms':set(), 
         'selectable':insert_stmt})
        self.isinsert = True
        crud_params = (crud._get_crud_params)(self, insert_stmt, **kw)
        if not crud_params:
            if not self.dialect.supports_default_values:
                if not self.dialect.supports_empty_insert:
                    raise exc.CompileError("The '%s' dialect with current database version settings does not support empty inserts." % self.dialect.name)
        elif insert_stmt._has_multi_parameters:
            if not self.dialect.supports_multivalues_insert:
                raise exc.CompileError("The '%s' dialect with current database version settings does not support in-place multirow inserts." % self.dialect.name)
            crud_params_single = crud_params[0]
        else:
            crud_params_single = crud_params
        preparer = self.preparer
        supports_default_values = self.dialect.supports_default_values
        jsn = {'command': 'advanced/insert'}
        if insert_stmt._prefixes:
            text += (self._generate_prefixes)(insert_stmt, 
             (insert_stmt._prefixes), **kw)
        table_text = insert_stmt.table._compiler_dispatch(self,
          asfrom=True, iscrud=True)
        if insert_stmt._hints:
            dialect_hints = dict([(
             table, hint_text) for (table, dialect), hint_text in insert_stmt._hints.items() if dialect in ('*', self.dialect.name)])
            if insert_stmt.table in dialect_hints:
                table_text = self.format_from_hint_text(table_text, insert_stmt.table, dialect_hints[insert_stmt.table], True)
        jsn['table'] = table_text['table']
        jsn['schema'] = table_text.get('schema', DEFAULT_SCHEMA)
        if not (crud_params_single or supports_default_values):
            jsn['fields'] = [preparer.format_column(c[0]) for c in crud_params_single]
        if self.returning or insert_stmt._returning:
            self.returning = self.returning or insert_stmt._returning
            returning_clause = self.returning_clause(insert_stmt, self.returning)
            if self.returning_precedes_values:
                jsn['returning_insert'] = returning_clause
        if insert_stmt.select is not None:
            jsn['values'] = (self.process)((self._insert_from_select), **kw)
            jsn['method'] = 'select'
        else:
            if not crud_params:
                if supports_default_values:
                    jsn['values'] = ' DEFAULT VALUES'
                else:
                    if insert_stmt._has_multi_parameters:
                        jsn['values'] = [[c[1] for c in crud_param_set] for crud_param_set in crud_params]
                    else:
                        jsn['values'] = [
                         [c[1] for c in crud_params]]
            elif self.returning:
                jsn['returning'] = self.returning_precedes_values or returning_clause
            return jsn

    def visit_getitem_binary(self, binary, operator, **kw):
        return {'type':'operator', 
         'operator':'getitem', 
         'operands':[
          (self.process)((binary.left), **kw),
          (self.process)((binary.right), **kw)]}

    def visit_slice(self, element, **kw):
        return {'type':'slice', 
         'start':self.process(element.start, **kw), 
         'stop':self.process(element.stop, **kw)}

    def visit_alias(self, alias, asfrom=False, ashint=False, iscrud=False, fromhints=None, **kwargs):
        if asfrom or ashint:
            if isinstance(alias.name, elements._truncated_label):
                alias_name = self._truncated_identifier('alias', alias.name)
        else:
            alias_name = alias.name
        if ashint:
            return self.preparer.format_alias(alias, alias_name)
        if asfrom:
            ret = (alias.original._compiler_dispatch)(self, asfrom=True, **kwargs)
            ret['alias'] = self.preparer.format_alias(alias, alias_name)
            if fromhints:
                if alias in fromhints:
                    ret = self.format_from_hint_text(ret, alias, fromhints[alias], iscrud)
            return ret
        return (alias.original._compiler_dispatch)(self, **kwargs)

    def visit_delete(self, delete_stmt, **kw):
        self.stack.append({'correlate_froms':set([delete_stmt.table]),  'asfrom_froms':set([delete_stmt.table]), 
         'selectable':delete_stmt})
        self.isdelete = True
        jsn = {'command': 'advanced/delete'}
        if delete_stmt._prefixes:
            text += (self._generate_prefixes)(delete_stmt, 
             (delete_stmt._prefixes), **kw)
        else:
            table_text = delete_stmt.table._compiler_dispatch(self,
              asfrom=True, iscrud=True)
            if delete_stmt._hints:
                dialect_hints = dict([(
                 table, hint_text) for (table, dialect), hint_text in delete_stmt._hints.items() if dialect in ('*', self.dialect.name)])
                if delete_stmt.table in dialect_hints:
                    table_text = self.format_from_hint_text(table_text, delete_stmt.table, dialect_hints[delete_stmt.table], True)
            else:
                dialect_hints = None
        jsn['table'] = table_text['table']
        jsn['schema'] = table_text.get('schema', DEFAULT_SCHEMA)
        if delete_stmt._returning:
            self.returning = delete_stmt._returning
            if self.returning_precedes_values:
                jsn['returning_delete'] = ' ' + self.returning_clause(delete_stmt, delete_stmt._returning)
        if delete_stmt._whereclause is not None:
            t = delete_stmt._whereclause._compiler_dispatch(self)
            if t:
                jsn['where'] = t
        if self.returning:
            if not self.returning_precedes_values:
                jsn['returning'] = self.returning_clause(delete_stmt, delete_stmt._returning)
        self.stack.pop(-1)
        return jsn

    def visit_table(self, table, asfrom=False, iscrud=False, ashint=False, fromhints=None, **kwargs):
        if asfrom or ashint:
            jsn = {'type': 'table'}
            if getattr(table, 'schema', None):
                jsn['schema'] = table.schema
            else:
                jsn['schema'] = DEFAULT_SCHEMA
            jsn['table'] = table.name
            return jsn
        raise NotImplementedError('visit_table (%s)' % table.name)

    def visit_select(self, select, asfrom=False, parens=True, fromhints=None, compound_index=0, nested_join_translation=False, select_wraps_for=None, **kwargs):
        jsn = {'command':'advanced/search', 
         'type':'select'}
        needs_nested_translation = select.use_labels and not nested_join_translation and not self.stack and not self.dialect.supports_right_nested_joins
        if needs_nested_translation:
            transformed_select = self._transform_select_for_nested_joins(select)
            text = (self.visit_select)(
 transformed_select, asfrom=asfrom, 
             parens=parens, fromhints=fromhints, 
             compound_index=compound_index, 
             nested_join_translation=True, **kwargs)
        else:
            toplevel = not self.stack
            entry = self._default_stack_entry if toplevel else self.stack[(-1)]
            populate_result_map = toplevel or compound_index == 0 and entry.get('need_result_map_for_compound', False) or entry.get('need_result_map_for_nested', False)
            if not populate_result_map:
                if 'add_to_result_map' in kwargs:
                    del kwargs['add_to_result_map']
            elif needs_nested_translation:
                if populate_result_map:
                    self._transform_result_map_for_nested_joins(select, transformed_select)
                return jsn
                froms = self._setup_select_stack(select, entry, asfrom)
                column_clause_args = kwargs.copy()
                column_clause_args.update({'within_label_clause':False, 
                 'within_columns_clause':False})
                if select._hints:
                    hint_text, byfrom = self._setup_select_hints(select)
                    if hint_text:
                        text += hint_text + ' '
            else:
                byfrom = None
        if select._distinct:
            jsn['distinct'] = True
        inner_columns = [c for c in [self._label_select_column(select,
          column,
          populate_result_map,
          asfrom, column_clause_args,
          name=name) for name, column in select._columns_plus_names] if c is not None]
        if populate_result_map:
            if select_wraps_for is not None:
                wrapped_inner_columns = set(select_wraps_for.inner_columns)
                translate = dict(((
                 outer, inner.pop()) for outer, inner in [(
                 outer,
                 outer.proxy_set.intersection(wrapped_inner_columns)) for outer in select.inner_columns] if inner))
                self._result_columns = [(
                 key, name, tuple((translate.get(o, o) for o in obj)), type_) for key, name, obj, type_ in self._result_columns]
        jsn = self._compose_select_body(jsn, select, inner_columns, froms, byfrom, kwargs)
        if select._statement_hints:
            per_dialect = [ht for dialect_name, ht in select._statement_hints if dialect_name in ('*', self.dialect.name)]
            if per_dialect:
                text += ' ' + self.get_statement_hint_text(per_dialect)
        if self.ctes:
            if self._is_toplevel_select(select):
                text = self._render_cte_clause() + text
        if select._suffixes:
            text += ' ' + (self._generate_prefixes)(
             select, (select._suffixes), **kwargs)
        self.stack.pop(-1)
        if asfrom:
            if parens:
                return jsn
        return jsn

    def visit_update(self, update_stmt, asfrom=False, **kw):
        toplevel = not self.stack
        self.stack.append({'correlate_froms':set([update_stmt.table]), 
         'asfrom_froms':set([update_stmt.table]), 
         'selectable':update_stmt})
        extra_froms = update_stmt._extra_froms
        d = {'command': 'advanced/update'}
        d['table'] = update_stmt.table.name
        if update_stmt.table.schema:
            d['schema'] = update_stmt.table.schema.name
        crud_params = (crud._setup_crud_params)(
         self, update_stmt, (crud.ISUPDATE), **kw)
        include_table = extra_froms and self.render_table_with_column_in_update_from
        d['fields'] = [c[0]._compiler_dispatch(self, include_table=include_table) for c in crud_params]
        d['values'] = [c[1] for c in crud_params]
        if update_stmt._whereclause is not None:
            t = (self.process)((update_stmt._whereclause), **kw)
            if t:
                d['where'] = t
        limit = self.update_limit_clause(update_stmt)
        if limit:
            d['limit'] = limit
        return d

    def visit_compound_select--- This code section failed: ---

 L. 682         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                stack
                4  UNARY_NOT        
                6  STORE_FAST               'toplevel'

 L. 684         8  LOAD_FAST                'toplevel'
               10  POP_JUMP_IF_FALSE    18  'to 18'
               12  LOAD_DEREF               'self'
               14  LOAD_ATTR                _default_stack_entry
               16  JUMP_FORWARD         26  'to 26'
             18_0  COME_FROM            10  '10'
               18  LOAD_DEREF               'self'
               20  LOAD_ATTR                stack
               22  LOAD_CONST               -1
               24  BINARY_SUBSCR    
             26_0  COME_FROM            16  '16'
               26  STORE_FAST               'entry'

 L. 685        28  LOAD_FAST                'toplevel'
               30  JUMP_IF_TRUE_OR_POP    50  'to 50'

 L. 686        32  LOAD_FAST                'compound_index'
               34  LOAD_CONST               0
               36  COMPARE_OP               ==
               38  JUMP_IF_FALSE_OR_POP    50  'to 50'

 L. 687        40  LOAD_FAST                'entry'
               42  LOAD_METHOD              get
               44  LOAD_STR                 'need_result_map_for_compound'
               46  LOAD_CONST               False
               48  CALL_METHOD_2         2  ''
             50_0  COME_FROM            38  '38'
             50_1  COME_FROM            30  '30'

 L. 685        50  STORE_FAST               'need_result_map'

 L. 689        52  LOAD_DEREF               'self'
               54  LOAD_ATTR                stack
               56  LOAD_METHOD              append

 L. 691        58  LOAD_FAST                'entry'
               60  LOAD_STR                 'correlate_froms'
               62  BINARY_SUBSCR    

 L. 692        64  LOAD_FAST                'entry'
               66  LOAD_STR                 'asfrom_froms'
               68  BINARY_SUBSCR    

 L. 693        70  LOAD_FAST                'cs'

 L. 694        72  LOAD_FAST                'need_result_map'

 L. 690        74  LOAD_CONST               ('correlate_froms', 'asfrom_froms', 'selectable', 'need_result_map_for_compound')
               76  BUILD_CONST_KEY_MAP_4     4 

 L. 689        78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 697        82  LOAD_DEREF               'self'
               84  LOAD_ATTR                compound_keywords
               86  LOAD_METHOD              get
               88  LOAD_FAST                'cs'
               90  LOAD_ATTR                keyword
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'keyword'

 L. 699        96  LOAD_FAST                'keyword'

 L. 700        98  LOAD_STR                 'select'

 L. 702       100  LOAD_CLOSURE             'asfrom'
              102  LOAD_CLOSURE             'kwargs'
              104  LOAD_CLOSURE             'self'
              106  BUILD_TUPLE_3         3 
              108  LOAD_LISTCOMP            '<code_object <listcomp>>'
              110  LOAD_STR                 'OECompiler.visit_compound_select.<locals>.<listcomp>'
              112  MAKE_FUNCTION_8          'closure'

 L. 705       114  LOAD_GLOBAL              enumerate
              116  LOAD_FAST                'cs'
              118  LOAD_ATTR                selects
              120  CALL_FUNCTION_1       1  ''

 L. 702       122  GET_ITER         
              124  CALL_FUNCTION_1       1  ''

 L. 699       126  LOAD_CONST               ('keyword', 'type', 'selects')
              128  BUILD_CONST_KEY_MAP_3     3 
              130  STORE_FAST               'jsn'

 L. 708       132  LOAD_FAST                'cs'
              134  LOAD_ATTR                _group_by_clause
              136  LOAD_ATTR                _compiler_dispatch

 L. 709       138  LOAD_DEREF               'self'

 L. 708       140  BUILD_TUPLE_1         1 
              142  LOAD_STR                 'asfrom'

 L. 709       144  LOAD_DEREF               'asfrom'

 L. 708       146  BUILD_MAP_1           1 

 L. 709       148  LOAD_DEREF               'kwargs'

 L. 708       150  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              152  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              154  STORE_FAST               'group_by'

 L. 710       156  LOAD_FAST                'group_by'
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 711       160  LOAD_FAST                'group_by'
              162  LOAD_FAST                'jsn'
              164  LOAD_STR                 'group_by'
              166  STORE_SUBSCR     
            168_0  COME_FROM           158  '158'

 L. 713       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                order_by_clause
              172  LOAD_FAST                'cs'
              174  BUILD_TUPLE_1         1 
              176  LOAD_DEREF               'kwargs'
              178  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              180  STORE_FAST               'order_by'

 L. 715       182  LOAD_FAST                'order_by'
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 716       186  LOAD_FAST                'order_by'
              188  LOAD_FAST                'jsn'
              190  LOAD_STR                 'order_by'
              192  STORE_SUBSCR     
            194_0  COME_FROM           184  '184'

 L. 718       194  LOAD_FAST                'cs'
              196  LOAD_ATTR                _limit_clause
              198  LOAD_CONST               None
              200  COMPARE_OP               is-not
              202  POP_JUMP_IF_TRUE    214  'to 214'

 L. 719       204  LOAD_FAST                'cs'
              206  LOAD_ATTR                _offset_clause
              208  LOAD_CONST               None
              210  COMPARE_OP               is-not

 L. 718       212  POP_JUMP_IF_FALSE   228  'to 228'
            214_0  COME_FROM           202  '202'

 L. 720       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                limit_clause
              218  LOAD_FAST                'cs'
              220  BUILD_TUPLE_1         1 
              222  LOAD_DEREF               'kwargs'
              224  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 718       226  JUMP_IF_TRUE_OR_POP   230  'to 230'
            228_0  COME_FROM           212  '212'

 L. 720       228  LOAD_STR                 ''
            230_0  COME_FROM           226  '226'

 L. 718       230  STORE_FAST               'boundaries'

 L. 722       232  LOAD_FAST                'boundaries'
              234  POP_JUMP_IF_FALSE   246  'to 246'

 L. 723       236  LOAD_FAST                'jsn'
              238  LOAD_METHOD              update
              240  LOAD_FAST                'boundaries'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           234  '234'

 L. 728       246  LOAD_DEREF               'self'
              248  LOAD_ATTR                stack
              250  LOAD_METHOD              pop
              252  LOAD_CONST               -1
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L. 733       258  LOAD_FAST                'toplevel'
          260_262  POP_JUMP_IF_FALSE   272  'to 272'

 L. 734       264  LOAD_STR                 'advanced/search'
              266  LOAD_FAST                'jsn'
              268  LOAD_STR                 'command'
              270  STORE_SUBSCR     
            272_0  COME_FROM           260  '260'

 L. 736       272  LOAD_FAST                'jsn'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 228_0

    def visit_cast(self, cast, **kwargs):
        return {'type':'cast', 
         'source':cast.clause._compiler_dispatch(self, **kwargs), 
         'as':cast.typeclause._compiler_dispatch(self, **kwargs)}

    def visit_over(self, over, **kwargs):
        return {'type':'over', 
         'function':over.func._compiler_dispatch(self, **kwargs), 
         'clauses':[{'type':word, 
          'clause':clause._compiler_dispatch(self, **kwargs)} for word, clause in (
          (
           'PARTITION', over.partition_by),
          (
           'ORDER', over.order_by)) if clause is not None if len(clause)]}

    def visit_funcfilter(self, funcfilter, **kwargs):
        return {'type':'funcfilter', 
         'function':funcfilter.func._compiler_dispatch(self, **kwargs), 
         'where':funcfilter.criterion._compiler_dispatch(self, **kwargs)}

    def visit_extract(self, extract, **kwargs):
        field = self.extract_map.get(extract.field, extract.field)
        return {'type':'extract', 
         'field':field, 
         'expression':extract.expr._compiler_dispatch(self, **kwargs)}

    def visit_label(self, label, add_to_result_map=None, within_label_clause=False, within_columns_clause=False, render_label_as_label=None, **kw):
        render_label_with_as = within_columns_clause and not within_label_clause
        render_label_only = render_label_as_label is label
        d = {'type': 'label'}
        if isinstance(label.name, elements._truncated_label):
            labelname = self._truncated_identifier('colident', label.name)
        else:
            labelname = label.name
        d['label'] = labelname
        if render_label_with_as:
            if add_to_result_map is not None:
                add_to_result_map(labelname, label.name, (
                 label, labelname) + label._alt_names, label.type)
            d = {'type':'label', 
             'element':label.element._compiler_dispatch(
 self, within_columns_clause=True, 
              within_label_clause=True, **kw), 
             'label':self.preparer.format_label(label, labelname)}
        d['element'] = (label.element._compiler_dispatch)(
 self, within_columns_clause=False, **kw)
        return d

    def visit_function(self, func, add_to_result_map=None, **kwargs):
        if add_to_result_map is not None:
            add_to_result_map(func.name, func.name, (), func.type)
        disp = getattr(self, 'visit_%s_func' % func.name.lower(), None)
        if disp:
            return disp(func, **kwargs)
        name = FUNCTIONS.get(func.__class__, func.name)
        return {'type':'function',  'function':'.'.join(list(func.packagenames) + [name]), 
         'operands':self.function_argspec(func, **kwargs)}

    def visit_column(self, column, add_to_result_map=None, include_table=True, **kwargs):
        name = orig_name = column.name
        if name is None:
            raise exc.CompileError("Cannot compile Column object until its 'name' is assigned.")
        else:
            is_literal = column.is_literal
            if not is_literal:
                if isinstance(name, elements._truncated_label):
                    name = self._truncated_identifier('colident', name)
            else:
                if add_to_result_map is not None:
                    add_to_result_map(name, orig_name, (
                     column, name, column.key), column.type)
                if is_literal:
                    name = self.escape_literal_column(name)
                jsn = {'type':'column', 
                 'column':name,  'is_literal':is_literal}
                table = column.table
                if not table is None:
                    if not (include_table and table.named_with_column):
                        return jsn
                        tablename = table.name
                        if isinstance(tablename, elements._truncated_label):
                            jsn['alias'] = self._truncated_identifier('alias', tablename)
                else:
                    jsn['table'] = tablename
                    if table.schema:
                        jsn['schema'] = table.schema
                    else:
                        jsn['schema'] = DEFAULT_SCHEMA
        return jsn

    def visit_null(self, expr, **kw):
        pass

    def _generate_generic_binary(self, binary, opstring, **kw):
        return {'type':'operator', 
         'operands':[
          (binary.left._compiler_dispatch)(self, **kw),
          (binary.right._compiler_dispatch)(self, **kw)], 
         'operator':opstring}

    def _generate_generic_unary_operator(self, unary, opstring, **kw):
        return {'type':'operator', 
         'operator':opstring, 
         'operands':[
          (unary.element._compiler_dispatch)(self, **kw)]}

    def _generate_generic_unary_modifier(self, unary, opstring, **kw):
        return {'type':'modifier', 
         'operator':opstring, 
         'operands':[
          (unary.element._compiler_dispatch)(self, **kw)]}

    def _label_select_column(self, select, column, populate_result_map, asfrom, column_clause_args, name=None, within_columns_clause=True):
        """produce labeled columns present in a select()."""
        if column.type._has_column_expression and populate_result_map:
            col_expr = column.type.column_expression(column)
            add_to_result_map = lambda keyname, name, objects, type_: self._add_to_result_map(keyname, name, (
             column,) + objects, type_)
        else:
            col_expr = column
            if populate_result_map:
                add_to_result_map = self._add_to_result_map
            else:
                add_to_result_map = None
        if not within_columns_clause:
            result_expr = col_expr
        else:
            if isinstance(column, elements.Label):
                if col_expr is not column:
                    result_expr = compiler._CompileLabel(col_expr,
                      (column.name),
                      alt_names=(
                     column.element,))
                else:
                    result_expr = col_expr
            else:
                if select is not None and name:
                    result_expr = compiler._CompileLabel(col_expr,
                      name,
                      alt_names=(
                     column._key_label,))
                else:
                    if asfrom and isinstance(column, elements.ColumnClause) and (column.is_literal or column.table) is not None:
                        result_expr = isinstance(column.table, selectable.Select) or compiler._CompileLabel(col_expr, (elements._as_truncated(column.name)),
                          alt_names=(
                         column.key,))
                    else:
                        if not isinstance(column, elements.TextClause):
                            if not isinstance(column, elements.UnaryExpression) or column.wraps_column_expression:
                                if not hasattr(column, 'name') or isinstance(column, functions.Function):
                                    result_expr = compiler._CompileLabel(col_expr, column.anon_label)
                        elif col_expr is not column:
                            result_expr = compiler._CompileLabel(col_expr, (elements._as_truncated(column.name)),
                              alt_names=(
                             column.key,))
                        else:
                            result_expr = col_expr
        column_clause_args.update(within_columns_clause=within_columns_clause,
          add_to_result_map=add_to_result_map)
        return (result_expr._compiler_dispatch)(
         self, **column_clause_args)

    def _compose_select_body(self, jsn, select, inner_columns, froms, byfrom, kwargs):
        jsn['fields'] = inner_columns
        if froms:
            if select._hints:
                jsn['from'] = [(f._compiler_dispatch)(self, asfrom=True, fromhints=byfrom, **kwargs) for f in froms]
            else:
                jsn['from'] = [(f._compiler_dispatch)(self, asfrom=True, **kwargs) for f in froms]
        else:
            jsn['from'] = self.default_from()
        if select._whereclause is not None:
            t = (select._whereclause._compiler_dispatch)(self, **kwargs)
            if t:
                jsn['where'] = t
        if select._group_by_clause.clauses:
            group_by = (select._group_by_clause._compiler_dispatch)(
             self, **kwargs)
            if group_by:
                jsn['group_by'] = group_by
        if select._having is not None:
            t = (select._having._compiler_dispatch)(self, **kwargs)
            if t:
                jsn['having'] = t
        if select._order_by_clause.clauses:
            jsn['order_by'] = (self.order_by_clause)(select, **kwargs)
        if select._limit_clause is not None or select._offset_clause is not None:
            jsn.update((self.limit_clause)(select, **kwargs))
        if select._for_update_arg is not None:
            jsn['for_update'] = (self.for_update_clause)(select, **kwargs)
        return jsn

    def _generate_prefixes(self, stmt, prefixes, **kw):
        clause = ' '.join(((prefix._compiler_dispatch)(self, **kw) for prefix, dialect_name in prefixes if dialect_name is None or dialect_name == self.dialect.name))
        if clause:
            clause += ' '
        return clause

    def _setup_select_stack(self, select, entry, asfrom):
        correlate_froms = entry['correlate_froms']
        asfrom_froms = entry['asfrom_froms']
        if asfrom:
            froms = select._get_display_froms(explicit_correlate_froms=(correlate_froms.difference(asfrom_froms)),
              implicit_correlate_froms=())
        else:
            froms = select._get_display_froms(explicit_correlate_froms=correlate_froms,
              implicit_correlate_froms=asfrom_froms)
        new_correlate_froms = set((selectable._from_objects)(*froms))
        all_correlate_froms = new_correlate_froms.union(correlate_froms)
        new_entry = {'asfrom_froms':new_correlate_froms, 
         'correlate_froms':all_correlate_froms, 
         'selectable':select}
        self.stack.append(new_entry)
        return froms

    def limit_clause(self, select, **kw):
        d = {}
        if select._limit_clause is not None:
            d['limit'] = (self.process)((select._limit_clause), **kw)
        if select._offset_clause is not None:
            d['offset'] = (self.process)((select._offset_clause), **kw)
        return d

    def returning_clause(self, stmt, returning_cols):
        columns = [self._label_select_column(None, c, True, False, {}) for c in expression._select_iterables(returning_cols)]
        return columns

    def order_by_clause(self, select, **kw):
        order_by = (select._order_by_clause._compiler_dispatch)(self, **kw)
        if order_by:
            return order_by
        return {}

    def for_update_clause(self, select, **kw):
        return {'for_update': True}
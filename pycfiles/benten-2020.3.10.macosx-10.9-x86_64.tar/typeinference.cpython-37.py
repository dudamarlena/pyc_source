# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/cwl/typeinference.py
# Compiled at: 2019-12-06 21:04:36
# Size of source mod 2**32: 3640 bytes
from typing import List
from .basetype import CWLBaseType, MapSubjectPredicate, TypeCheck, Match
from .unknowntype import CWLUnknownType
from .anytype import CWLAnyType
from .namespacedtype import CWLNameSpacedType

def infer_type--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              check_types
                2  LOAD_FAST                'node'
                4  LOAD_FAST                'allowed_types'
                6  LOAD_FAST                'key'
                8  LOAD_FAST                'map_sp'
               10  CALL_FUNCTION_4       4  '4 positional arguments'
               12  STORE_FAST               'type_check_results'

 L.  14        14  SETUP_LOOP          128  'to 128'
               16  LOAD_FAST                'type_check_results'
               18  GET_ITER         
             20_0  COME_FROM            34  '34'
               20  FOR_ITER             46  'to 46'
               22  STORE_FAST               'tcr'

 L.  15        24  LOAD_FAST                'tcr'
               26  LOAD_ATTR                match
               28  LOAD_GLOBAL              Match
               30  LOAD_ATTR                Yes
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    20  'to 20'

 L.  16        36  LOAD_FAST                'tcr'
               38  LOAD_ATTR                cwl_type
               40  STORE_FAST               'res'

 L.  17        42  BREAK_LOOP       
               44  JUMP_BACK            20  'to 20'
               46  POP_BLOCK        

 L.  19        48  SETUP_LOOP          128  'to 128'
               50  LOAD_FAST                'type_check_results'
               52  GET_ITER         
             54_0  COME_FROM            68  '68'
               54  FOR_ITER             80  'to 80'
               56  STORE_FAST               'tcr'

 L.  20        58  LOAD_FAST                'tcr'
               60  LOAD_ATTR                match
               62  LOAD_GLOBAL              Match
               64  LOAD_ATTR                Maybe
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    54  'to 54'

 L.  21        70  LOAD_FAST                'tcr'
               72  LOAD_ATTR                cwl_type
               74  STORE_FAST               'res'

 L.  22        76  BREAK_LOOP       
               78  JUMP_BACK            54  'to 54'
               80  POP_BLOCK        

 L.  24        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'type_check_results'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  LOAD_CONST               1
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L.  25        94  LOAD_FAST                'type_check_results'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_ATTR                cwl_type
              102  STORE_FAST               'res'
              104  JUMP_FORWARD        128  'to 128'
            106_0  COME_FROM            92  '92'

 L.  27       106  LOAD_GLOBAL              CWLUnknownType
              108  LOAD_STR                 '(unknown)'

 L.  28       110  LOAD_LISTCOMP            '<code_object <listcomp>>'
              112  LOAD_STR                 'infer_type.<locals>.<listcomp>'
              114  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              116  LOAD_FAST                'type_check_results'
              118  GET_ITER         
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_CONST               ('name', 'expected')
              124  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              126  STORE_FAST               'res'
            128_0  COME_FROM           104  '104'
            128_1  COME_FROM_LOOP       48  '48'
            128_2  COME_FROM_LOOP       14  '14'

 L.  29       128  LOAD_FAST                'res'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 128


def check_types(node, allowed_types, key, map_sp) -> List[TypeCheck]:
    type_check_results = []
    explicit_type = get_explicit_type_str(node, key, map_sp)
    if explicit_type is not None:
        if ':' in explicit_type:
            return [
             TypeCheck(CWLNameSpacedType(explicit_type))]
        for _type in allowed_types:
            if isinstance(_type, CWLAnyType):
                req_type = _type.if_you_can_be_anything_be_this_kind(explicit_type)
                if req_type is not None:
                    return [
                     TypeCheck(req_type)]
                return [
                 TypeCheck(CWLUnknownType(name=explicit_type, expected=(_type.all_possible_type_names())),
                   match=(Match.No))]
                if explicit_type == _type.name:
                    return [
                     TypeCheck(_type)]

        return [
         TypeCheck(CWLUnknownType(name=explicit_type,
           expected=[t.name for t in allowed_types]),
           match=(Match.No))]
    for _type in allowed_types:
        if _type.name == 'null':
            if node is None:
                return [
                 TypeCheck(CWLBaseType(name=_type))]
                type_check_results += [TypeCheck(CWLBaseType(name=_type), match=(Match.No))]
                continue
            elif _type.name == 'string':
                if node is None:
                    return [
                     TypeCheck(_type)]
                if isinstance(node, str):
                    type_check_results += [TypeCheck(_type, match=(Match.Maybe))]
            else:
                type_check_results += [TypeCheck(_type, match=(Match.No))]
            continue
            if _type.name in ('boolean', 'int', 'long'):
                if node is None or isinstance(node, (str, bool, int)):
                    return [
                     TypeCheck(_type)]
        else:
            type_check_results += [TypeCheck(_type, match=(Match.No))]
            continue
        check_result = _type.check(node, key, map_sp)
        if check_result.match == Match.Yes:
            return [
             check_result]
        type_check_results += [check_result]

    return type_check_results


def get_explicit_type_str(node, key: str, map_sp: MapSubjectPredicate):
    if map_sp is not None:
        if map_sp.subject == 'class':
            return key
        return
    else:
        if isinstance(node, dict):
            return node.get('class')
        return
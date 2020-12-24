# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse37base.py
# Compiled at: 2020-04-20 11:36:16
"""
Python 3.7 base code. We keep non-custom-generated grammar rules out of this file.
"""
from uncompyle6.scanners.tok import Token
from uncompyle6.parser import ParserError, PythonParser, PythonParserSingle, nop_func
from uncompyle6.parsers.treenode import SyntaxTree
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parsers.reducecheck import and_check, ifelsestmt, iflaststmt, ifstmt, ifstmts_jump, or_check, testtrue, tryelsestmtl3, while1stmt, while1elsestmt

class Python37BaseParser(PythonParser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        self.added_rules = set()
        super(Python37BaseParser, self).__init__(SyntaxTree, 'stmts', debug=debug_parser)
        self.new_rules = set()

    @staticmethod
    def call_fn_name(token):
        """Customize CALL_FUNCTION to add the number of positional arguments"""
        if token.attr is not None:
            return '%s_%i' % (token.kind, token.attr)
        else:
            return '%s_0' % token.kind
        return

    def add_make_function_rule(self, rule, opname, attr, customize):
        """Python 3.3 added a an addtional LOAD_STR before MAKE_FUNCTION and
        this has an effect on many rules.
        """
        new_rule = rule % 'LOAD_STR '
        self.add_unique_rule(new_rule, opname, attr, customize)

    def custom_build_class_rule(self, opname, i, token, tokens, customize):
        """
        # Should the first rule be somehow folded into the 2nd one?
        build_class ::= LOAD_BUILD_CLASS mkfunc
                        LOAD_CLASSNAME {expr}^n-1 CALL_FUNCTION_n
                        LOAD_CONST CALL_FUNCTION_n
        build_class ::= LOAD_BUILD_CLASS mkfunc
                        expr
                        call
                        CALL_FUNCTION_3
         """
        for i in range(i + 1, len(tokens)):
            if tokens[i].kind.startswith('MAKE_FUNCTION'):
                break
            elif tokens[i].kind.startswith('MAKE_CLOSURE'):
                break

        assert i < len(tokens), 'build_class needs to find MAKE_FUNCTION or MAKE_CLOSURE'
        assert tokens[(i + 1)].kind == 'LOAD_STR', 'build_class expecting CONST after MAKE_FUNCTION/MAKE_CLOSURE'
        call_fn_tok = None
        for i in range(i, len(tokens)):
            if tokens[i].kind.startswith('CALL_FUNCTION'):
                call_fn_tok = tokens[i]
                break

        if not call_fn_tok:
            raise RuntimeError('build_class custom rule for %s needs to find CALL_FUNCTION' % opname)
        call_function = call_fn_tok.kind
        if call_function.startswith('CALL_FUNCTION_KW'):
            self.addRule('classdef ::= build_class_kw store', nop_func)
            rule = 'build_class_kw ::= LOAD_BUILD_CLASS mkfunc %sLOAD_CONST %s' % ('expr ' * (call_fn_tok.attr - 1), call_function)
        else:
            call_function = self.call_fn_name(call_fn_tok)
            rule = 'build_class ::= LOAD_BUILD_CLASS mkfunc %s%s' % ('expr ' * (call_fn_tok.attr - 1), call_function)
        self.addRule(rule, nop_func)
        return

    def customize_grammar_rules--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL           0  'False'
                3  STORE_FAST           28  'is_pypy'

 L. 113         6  LOAD_GLOBAL           2  'frozenset'
                9  LOAD_CONST               ('BEFORE', 'BUILD', 'CALL', 'CONTINUE', 'DELETE', 'FORMAT', 'GET', 'JUMP', 'LOAD', 'LOOKUP', 'MAKE', 'RETURN', 'RAISE', 'SETUP', 'UNPACK')
               12  CALL_FUNCTION_1       1  None
               15  STORE_FAST           30  'customize_instruction_basenames'

 L. 141        18  LOAD_GLOBAL           4  'set'
               21  LOAD_CONST               ('BUILD_TUPLE_UNPACK_WITH_CALL',)
               24  CALL_FUNCTION_1       1  None
               27  STORE_FAST           11  'custom_ops_processed'

 L. 146        30  LOAD_GLOBAL           2  'frozenset'
               33  BUILD_LIST_0          0 
               36  DUP_TOP          
               37  STORE_FAST           27  '_[1]'
               40  LOAD_FAST             1  'tokens'
               43  GET_ITER         
               44  FOR_ITER             16  'to 63'
               47  STORE_FAST           31  't'
               50  LOAD_FAST            27  '_[1]'
               53  LOAD_FAST            31  't'
               56  LOAD_ATTR             9  'kind'
               59  LIST_APPEND      
               60  JUMP_BACK            44  'to 44'
               63  DELETE_FAST          27  '_[1]'
               66  CALL_FUNCTION_1       1  None
               69  LOAD_FAST             0  'self'
               72  STORE_ATTR           11  'seen_ops'

 L. 147        75  LOAD_GLOBAL           2  'frozenset'
               78  BUILD_LIST_0          0 
               81  DUP_TOP          
               82  STORE_FAST           27  '_[1]'
               85  LOAD_FAST             0  'self'
               88  LOAD_ATTR            11  'seen_ops'
               91  GET_ITER         
               92  FOR_ITER             26  'to 121'
               95  STORE_FAST            7  'opname'
               98  LOAD_FAST            27  '_[1]'
              101  LOAD_FAST             7  'opname'
              104  LOAD_FAST             7  'opname'
              107  LOAD_ATTR            13  'rfind'
              110  LOAD_CONST               '_'
              113  CALL_FUNCTION_1       1  None
              116  SLICE+2          
              117  LIST_APPEND      
              118  JUMP_BACK            92  'to 92'
              121  DELETE_FAST          27  '_[1]'
              124  CALL_FUNCTION_1       1  None
              127  LOAD_FAST             0  'self'
              130  STORE_ATTR           14  'seen_op_basenames'

 L. 154       133  LOAD_CONST               'PyPy'
              136  LOAD_FAST             2  'customize'
              139  COMPARE_OP            6  in
              142  JUMP_IF_FALSE        26  'to 171'
            145_0  THEN                     172
              145  POP_TOP          

 L. 155       146  LOAD_GLOBAL          16  'True'
              149  STORE_FAST           28  'is_pypy'

 L. 156       152  LOAD_FAST             0  'self'
              155  LOAD_ATTR            17  'addRule'
              158  LOAD_CONST               '\n              stmt ::= assign3_pypy\n              stmt ::= assign2_pypy\n              assign3_pypy       ::= expr expr expr store store store\n              assign2_pypy       ::= expr expr store store\n              stmt               ::= if_exp_lambda\n              stmt               ::= if_exp_not_lambda\n              if_exp_lambda      ::= expr jmp_false expr return_if_lambda\n                                     return_lambda LAMBDA_MARKER\n              if_exp_not_lambda  ::= expr jmp_true expr return_if_lambda\n                                     return_lambda LAMBDA_MARKER\n              '

 L. 169       161  LOAD_GLOBAL          18  'nop_func'
              164  CALL_FUNCTION_2       2  None
              167  POP_TOP          
              168  JUMP_FORWARD          1  'to 172'
            171_0  COME_FROM           142  '142'
              171  POP_TOP          
            172_0  COME_FROM           168  '168'

 L. 172       172  LOAD_GLOBAL          19  'len'
              175  LOAD_FAST             1  'tokens'
              178  CALL_FUNCTION_1       1  None
              181  STORE_FAST           26  'n'

 L. 175       184  LOAD_GLOBAL           0  'False'
              187  STORE_FAST           34  'has_get_iter_call_function1'

 L. 176       190  SETUP_LOOP           96  'to 289'
              193  LOAD_GLOBAL          22  'enumerate'
              196  LOAD_FAST             1  'tokens'
              199  CALL_FUNCTION_1       1  None
              202  GET_ITER         
              203  FOR_ITER             82  'to 288'
              206  UNPACK_SEQUENCE_2     2 
              209  STORE_FAST           20  'i'
              212  STORE_FAST           29  'token'

 L. 177       215  LOAD_FAST            29  'token'
              218  LOAD_CONST               'GET_ITER'
              221  COMPARE_OP            2  ==
              224  JUMP_IF_FALSE        57  'to 284'
              227  POP_TOP          
              228  LOAD_FAST            20  'i'
              231  LOAD_FAST            26  'n'
              234  LOAD_CONST               2
              237  BINARY_SUBTRACT  
              238  COMPARE_OP            0  <
              241  JUMP_IF_FALSE        40  'to 284'
              244  POP_TOP          
              245  LOAD_FAST             0  'self'
              248  LOAD_ATTR            25  'call_fn_name'
              251  LOAD_FAST             1  'tokens'
              254  LOAD_FAST            20  'i'
              257  LOAD_CONST               1
              260  BINARY_ADD       
              261  BINARY_SUBSCR    
              262  CALL_FUNCTION_1       1  None
              265  LOAD_CONST               'CALL_FUNCTION_1'
              268  COMPARE_OP            2  ==
              271  JUMP_IF_FALSE        10  'to 284'
              274  POP_TOP          

 L. 182       275  LOAD_GLOBAL          16  'True'
              278  STORE_FAST           34  'has_get_iter_call_function1'
              281  JUMP_BACK           203  'to 203'
            284_0  COME_FROM           271  '271'
            284_1  COME_FROM           241  '241'
            284_2  COME_FROM           224  '224'
              284  POP_TOP          
              285  JUMP_BACK           203  'to 203'
              288  POP_BLOCK        
            289_0  COME_FROM           190  '190'

 L. 184       289  SETUP_LOOP         5131  'to 5423'
              292  LOAD_GLOBAL          22  'enumerate'
              295  LOAD_FAST             1  'tokens'
              298  CALL_FUNCTION_1       1  None
              301  GET_ITER         
              302  FOR_ITER           5117  'to 5422'
              305  UNPACK_SEQUENCE_2     2 
              308  STORE_FAST           20  'i'
              311  STORE_FAST           29  'token'

 L. 185       314  LOAD_FAST            29  'token'
              317  LOAD_ATTR             9  'kind'
              320  STORE_FAST            7  'opname'

 L. 189       323  LOAD_FAST             7  'opname'
              326  LOAD_FAST             7  'opname'
              329  LOAD_ATTR            26  'find'
              332  LOAD_CONST               '_'
              335  CALL_FUNCTION_1       1  None
              338  SLICE+2          
              339  LOAD_FAST            30  'customize_instruction_basenames'
              342  COMPARE_OP            7  not-in
              345  JUMP_IF_TRUE         13  'to 361'
              348  POP_TOP          
              349  LOAD_FAST             7  'opname'
              352  LOAD_FAST            11  'custom_ops_processed'
              355  COMPARE_OP            6  in
            358_0  COME_FROM           345  '345'
              358  JUMP_IF_FALSE         7  'to 368'
            361_0  THEN                     369
              361  POP_TOP          

 L. 193       362  CONTINUE            302  'to 302'
              365  JUMP_FORWARD          1  'to 369'
            368_0  COME_FROM           358  '358'
              368  POP_TOP          
            369_0  COME_FROM           365  '365'

 L. 195       369  LOAD_FAST             7  'opname'
              372  LOAD_FAST             7  'opname'
              375  LOAD_ATTR            13  'rfind'
              378  LOAD_CONST               '_'
              381  CALL_FUNCTION_1       1  None
              384  SLICE+2          
              385  STORE_FAST            5  'opname_base'

 L. 199       388  LOAD_FAST             7  'opname'
              391  LOAD_CONST               'LOAD_ASSERT'
              394  COMPARE_OP            2  ==
              397  JUMP_IF_FALSE        39  'to 439'
              400  POP_TOP          
              401  LOAD_CONST               'PyPy'
              404  LOAD_FAST             2  'customize'
              407  COMPARE_OP            6  in
              410  JUMP_IF_FALSE        26  'to 439'
              413  POP_TOP          

 L. 200       414  LOAD_CONST               '\n                stmt ::= JUMP_IF_NOT_DEBUG stmts COME_FROM\n                '
              417  STORE_FAST            6  'rules_str'

 L. 203       420  LOAD_FAST             0  'self'
              423  LOAD_ATTR            29  'add_unique_doc_rules'
              426  LOAD_FAST             6  'rules_str'
              429  LOAD_FAST             2  'customize'
              432  CALL_FUNCTION_2       2  None
              435  POP_TOP          
              436  JUMP_BACK           302  'to 302'
            439_0  COME_FROM           410  '410'
            439_1  COME_FROM           397  '397'
              439  POP_TOP          

 L. 205       440  LOAD_FAST             7  'opname'
              443  LOAD_CONST               'BEFORE_ASYNC_WITH'
              446  COMPARE_OP            2  ==
              449  JUMP_IF_FALSE        66  'to 518'
              452  POP_TOP          

 L. 206       453  LOAD_CONST               '\n                   stmt            ::= async_with_stmt\n                   stmt            ::= async_with_as_stmt\n                '
              456  STORE_FAST            6  'rules_str'

 L. 211       459  LOAD_FAST             0  'self'
              462  LOAD_ATTR            30  'version'
              465  LOAD_CONST               3.8
              468  COMPARE_OP            0  <
              471  JUMP_IF_FALSE        14  'to 488'
              474  POP_TOP          

 L. 212       475  LOAD_FAST             6  'rules_str'
              478  LOAD_CONST               '\n                      stmt                 ::= async_with_stmt SETUP_ASYNC_WITH\n                      c_stmt               ::= c_async_with_stmt SETUP_ASYNC_WITH\n                      async_with_stmt      ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               suite_stmts_opt\n                                               POP_BLOCK LOAD_CONST\n                                               async_with_post\n                      c_async_with_stmt    ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               c_suite_stmts_opt\n                                               POP_BLOCK LOAD_CONST\n                                               async_with_post\n                      async_with_stmt      ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               suite_stmts_opt\n                                               async_with_post\n                      c_async_with_stmt    ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               c_suite_stmts_opt\n                                               async_with_post\n                      async_with_as_stmt   ::= expr\n                                               async_with_pre\n                                               store\n                                               suite_stmts_opt\n                                               POP_BLOCK LOAD_CONST\n                                               async_with_post\n                      c_async_with_as_stmt ::= expr\n                                              async_with_pre\n                                              store\n                                              c_suite_stmts_opt\n                                              POP_BLOCK LOAD_CONST\n                                              async_with_post\n                      async_with_as_stmt   ::= expr\n                                              async_with_pre\n                                              store\n                                              suite_stmts_opt\n                                              async_with_post\n                      c_async_with_as_stmt ::= expr\n                                              async_with_pre\n                                              store\n                                              suite_stmts_opt\n                                              async_with_post\n                    '
              481  INPLACE_ADD      
              482  STORE_FAST            6  'rules_str'
              485  JUMP_FORWARD         11  'to 499'
            488_0  COME_FROM           471  '471'
              488  POP_TOP          

 L. 261       489  LOAD_FAST             6  'rules_str'
              492  LOAD_CONST               '\n                      async_with_pre       ::= BEFORE_ASYNC_WITH GET_AWAITABLE LOAD_CONST YIELD_FROM SETUP_ASYNC_WITH\n                      async_with_post      ::= BEGIN_FINALLY COME_FROM_ASYNC_WITH\n                                               WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                               WITH_CLEANUP_FINISH END_FINALLY\n                      async_with_stmt      ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               suite_stmts\n                                               POP_TOP POP_BLOCK\n                                               async_with_post\n                      c_async_with_stmt    ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               c_suite_stmts\n                                               POP_TOP POP_BLOCK\n                                               async_with_post\n                      async_with_stmt      ::= expr\n                                               async_with_pre\n                                               POP_TOP\n                                               suite_stmts\n                                               POP_BLOCK\n                                               BEGIN_FINALLY\n                                               WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                               WITH_CLEANUP_FINISH POP_FINALLY LOAD_CONST RETURN_VALUE\n                                               COME_FROM_ASYNC_WITH\n                                               WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                               WITH_CLEANUP_FINISH END_FINALLY\n                      c_async_with_stmt   ::= expr\n                                              async_with_pre\n                                              POP_TOP\n                                              c_suite_stmts\n                                              POP_BLOCK\n                                              BEGIN_FINALLY\n                                              WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                              WITH_CLEANUP_FINISH POP_FINALLY LOAD_CONST RETURN_VALUE\n                                              COME_FROM_ASYNC_WITH\n                                              WITH_CLEANUP_START GET_AWAITABLE LOAD_CONST YIELD_FROM\n                                              WITH_CLEANUP_FINISH END_FINALLY\n                      async_with_as_stmt   ::= expr\n                                               async_with_pre\n                                               store suite_stmts\n                                               POP_TOP POP_BLOCK\n                                               async_with_post\n                      c_async_with_as_stmt ::= expr\n                                               async_with_pre\n                                               store suite_stmts\n                                               POP_TOP POP_BLOCK\n                                               async_with_post\n                      async_with_as_stmt   ::= expr\n                                               async_with_pre\n                                               store suite_stmts\n                                               POP_BLOCK async_with_post\n                      c_async_with_as_stmt ::= expr\n                                               async_with_pre\n                                               store suite_stmts\n                                               POP_BLOCK async_with_post\n                    '
              495  INPLACE_ADD      
              496  STORE_FAST            6  'rules_str'
            499_0  COME_FROM           485  '485'

 L. 319       499  LOAD_FAST             0  'self'
              502  LOAD_ATTR            17  'addRule'
              505  LOAD_FAST             6  'rules_str'
              508  LOAD_GLOBAL          18  'nop_func'
              511  CALL_FUNCTION_2       2  None
              514  POP_TOP          
              515  JUMP_BACK           302  'to 302'
            518_0  COME_FROM           449  '449'
              518  POP_TOP          

 L. 321       519  LOAD_FAST             5  'opname_base'
              522  LOAD_CONST               'BUILD_CONST_KEY_MAP'
              525  COMPARE_OP            2  ==
              528  JUMP_IF_FALSE        49  'to 580'
              531  POP_TOP          

 L. 322       532  LOAD_CONST               'expr '
              535  LOAD_FAST            29  'token'
              538  LOAD_ATTR            31  'attr'
              541  BINARY_MULTIPLY  
              542  STORE_FAST           16  'kvlist_n'

 L. 323       545  LOAD_CONST               'dict ::= %sLOAD_CONST %s'
              548  LOAD_FAST            16  'kvlist_n'
              551  LOAD_FAST             7  'opname'
              554  BUILD_TUPLE_2         2 
              557  BINARY_MODULO    
              558  STORE_FAST           25  'rule'

 L. 324       561  LOAD_FAST             0  'self'
              564  LOAD_ATTR            17  'addRule'
              567  LOAD_FAST            25  'rule'
              570  LOAD_GLOBAL          18  'nop_func'
              573  CALL_FUNCTION_2       2  None
              576  POP_TOP          
              577  JUMP_BACK           302  'to 302'
            580_0  COME_FROM           528  '528'
              580  POP_TOP          

 L. 326       581  LOAD_FAST             7  'opname'
              584  LOAD_ATTR            34  'startswith'
              587  LOAD_CONST               'BUILD_LIST_UNPACK'
              590  CALL_FUNCTION_1       1  None
              593  JUMP_IF_FALSE        71  'to 667'
              596  POP_TOP          

 L. 327       597  LOAD_FAST            29  'token'
              600  LOAD_ATTR            31  'attr'
              603  STORE_FAST           32  'v'

 L. 328       606  LOAD_CONST               'build_list_unpack ::= %s%s'
              609  LOAD_CONST               'expr '
              612  LOAD_FAST            32  'v'
              615  BINARY_MULTIPLY  
              616  LOAD_FAST             7  'opname'
              619  BUILD_TUPLE_2         2 
              622  BINARY_MODULO    
              623  STORE_FAST           25  'rule'

 L. 329       626  LOAD_FAST             0  'self'
              629  LOAD_ATTR            17  'addRule'
              632  LOAD_FAST            25  'rule'
              635  LOAD_GLOBAL          18  'nop_func'
              638  CALL_FUNCTION_2       2  None
              641  POP_TOP          

 L. 330       642  LOAD_CONST               'expr ::= build_list_unpack'
              645  STORE_FAST           25  'rule'

 L. 331       648  LOAD_FAST             0  'self'
              651  LOAD_ATTR            17  'addRule'
              654  LOAD_FAST            25  'rule'
              657  LOAD_GLOBAL          18  'nop_func'
              660  CALL_FUNCTION_2       2  None
              663  POP_TOP          
              664  JUMP_BACK           302  'to 302'
            667_0  COME_FROM           593  '593'
              667  POP_TOP          

 L. 333       668  LOAD_FAST             5  'opname_base'
              671  LOAD_CONST               ('BUILD_MAP', 'BUILD_MAP_UNPACK')
              674  COMPARE_OP            6  in
              677  JUMP_IF_FALSE       440  'to 1120'
              680  POP_TOP          

 L. 335       681  LOAD_FAST             7  'opname'
              684  LOAD_CONST               'BUILD_MAP_UNPACK'
              687  COMPARE_OP            2  ==
              690  JUMP_IF_FALSE        20  'to 713'
              693  POP_TOP          

 L. 336       694  LOAD_FAST             0  'self'
              697  LOAD_ATTR            17  'addRule'
              700  LOAD_CONST               '\n                        expr       ::= unmap_dict\n                        unmap_dict ::= dict_comp BUILD_MAP_UNPACK\n                        '

 L. 341       703  LOAD_GLOBAL          18  'nop_func'
              706  CALL_FUNCTION_2       2  None
              709  POP_TOP          

 L. 343       710  JUMP_FORWARD         66  'to 779'
            713_0  COME_FROM           690  '690'
              713  POP_TOP          

 L. 344       714  LOAD_FAST             7  'opname'
              717  LOAD_ATTR            34  'startswith'
              720  LOAD_CONST               'BUILD_MAP_UNPACK_WITH_CALL'
              723  CALL_FUNCTION_1       1  None
              726  JUMP_IF_FALSE        49  'to 778'
            729_0  THEN                     779
              729  POP_TOP          

 L. 345       730  LOAD_FAST            29  'token'
              733  LOAD_ATTR            31  'attr'
              736  STORE_FAST           32  'v'

 L. 346       739  LOAD_CONST               'build_map_unpack_with_call ::= %s%s'
              742  LOAD_CONST               'expr '
              745  LOAD_FAST            32  'v'
              748  BINARY_MULTIPLY  
              749  LOAD_FAST             7  'opname'
              752  BUILD_TUPLE_2         2 
              755  BINARY_MODULO    
              756  STORE_FAST           25  'rule'

 L. 347       759  LOAD_FAST             0  'self'
              762  LOAD_ATTR            17  'addRule'
              765  LOAD_FAST            25  'rule'
              768  LOAD_GLOBAL          18  'nop_func'
              771  CALL_FUNCTION_2       2  None
              774  POP_TOP          
              775  JUMP_FORWARD          1  'to 779'
            778_0  COME_FROM           726  '726'
              778  POP_TOP          
            779_0  COME_FROM           775  '775'
            779_1  COME_FROM           710  '710'

 L. 349       779  LOAD_CONST               'kvlist_%s'
              782  LOAD_FAST            29  'token'
              785  LOAD_ATTR            31  'attr'
              788  BINARY_MODULO    
              789  STORE_FAST           16  'kvlist_n'

 L. 350       792  LOAD_FAST             7  'opname'
              795  LOAD_CONST               'BUILD_MAP_n'
              798  COMPARE_OP            2  ==
              801  JUMP_IF_FALSE       100  'to 904'
            804_0  THEN                     905
              804  POP_TOP          

 L. 352       805  LOAD_CONST               'dict_comp_func ::= BUILD_MAP_n LOAD_FAST for_iter store comp_iter JUMP_BACK RETURN_VALUE RETURN_LAST'
              808  STORE_FAST           25  'rule'

 L. 356       811  LOAD_FAST             0  'self'
              814  LOAD_ATTR            36  'add_unique_rule'
              817  LOAD_FAST            25  'rule'
              820  LOAD_CONST               'dict_comp_func'
              823  LOAD_CONST               1
              826  LOAD_FAST             2  'customize'
              829  CALL_FUNCTION_4       4  None
              832  POP_TOP          

 L. 358       833  LOAD_CONST               'kvlist_n'
              836  STORE_FAST           16  'kvlist_n'

 L. 359       839  LOAD_CONST               'kvlist_n ::=  kvlist_n kv3'
              842  STORE_FAST           25  'rule'

 L. 360       845  LOAD_FAST             0  'self'
              848  LOAD_ATTR            36  'add_unique_rule'
              851  LOAD_FAST            25  'rule'
              854  LOAD_CONST               'kvlist_n'
              857  LOAD_CONST               0
              860  LOAD_FAST             2  'customize'
              863  CALL_FUNCTION_4       4  None
              866  POP_TOP          

 L. 361       867  LOAD_CONST               'kvlist_n ::='
              870  STORE_FAST           25  'rule'

 L. 362       873  LOAD_FAST             0  'self'
              876  LOAD_ATTR            36  'add_unique_rule'
              879  LOAD_FAST            25  'rule'
              882  LOAD_CONST               'kvlist_n'
              885  LOAD_CONST               1
              888  LOAD_FAST             2  'customize'
              891  CALL_FUNCTION_4       4  None
              894  POP_TOP          

 L. 363       895  LOAD_CONST               'dict ::=  BUILD_MAP_n kvlist_n'
              898  STORE_FAST           25  'rule'
              901  JUMP_FORWARD          1  'to 905'
            904_0  COME_FROM           801  '801'
              904  POP_TOP          
            905_0  COME_FROM           901  '901'

 L. 365       905  LOAD_FAST             7  'opname'
              908  LOAD_ATTR            34  'startswith'
              911  LOAD_CONST               'BUILD_MAP_WITH_CALL'
              914  CALL_FUNCTION_1       1  None
              917  JUMP_IF_TRUE        171  'to 1091'
            920_0  THEN                     1092
              920  POP_TOP          

 L. 368       921  LOAD_FAST             7  'opname'
              924  LOAD_ATTR            34  'startswith'
              927  LOAD_CONST               'BUILD_MAP_UNPACK'
              930  CALL_FUNCTION_1       1  None
              933  JUMP_IF_FALSE        86  'to 1022'
            936_0  THEN                     1088
              936  POP_TOP          

 L. 373       937  LOAD_CONST               'LOAD_DICTCOMP'
              940  LOAD_FAST             0  'self'
              943  LOAD_ATTR            11  'seen_ops'
              946  COMPARE_OP            6  in
              949  JUMP_IF_FALSE        43  'to 995'
            952_0  THEN                     996
              952  POP_TOP          

 L. 374       953  LOAD_CONST               'dict ::= %s%s'
              956  LOAD_CONST               'dict_comp '
              959  LOAD_FAST            29  'token'
              962  LOAD_ATTR            31  'attr'
              965  BINARY_MULTIPLY  
              966  LOAD_FAST             7  'opname'
              969  BUILD_TUPLE_2         2 
              972  BINARY_MODULO    
              973  STORE_FAST           25  'rule'

 L. 375       976  LOAD_FAST             0  'self'
              979  LOAD_ATTR            17  'addRule'
              982  LOAD_FAST            25  'rule'
              985  LOAD_GLOBAL          18  'nop_func'
              988  CALL_FUNCTION_2       2  None
              991  POP_TOP          
              992  JUMP_FORWARD          1  'to 996'
            995_0  COME_FROM           949  '949'
              995  POP_TOP          
            996_0  COME_FROM           992  '992'

 L. 376       996  LOAD_CONST               '\n                         expr       ::= unmap_dict\n                         unmap_dict ::= %s%s\n                         '
              999  LOAD_CONST               'expr '
             1002  LOAD_FAST            29  'token'
             1005  LOAD_ATTR            31  'attr'
             1008  BINARY_MULTIPLY  
             1009  LOAD_FAST             7  'opname'
             1012  BUILD_TUPLE_2         2 
             1015  BINARY_MODULO    
             1016  STORE_FAST           25  'rule'
             1019  JUMP_ABSOLUTE      1092  'to 1092'
           1022_0  COME_FROM           933  '933'
             1022  POP_TOP          

 L. 384      1023  LOAD_CONST               '%s ::= %s %s'
             1026  LOAD_FAST            16  'kvlist_n'
             1029  LOAD_CONST               'expr '
             1032  LOAD_FAST            29  'token'
             1035  LOAD_ATTR            31  'attr'
             1038  LOAD_CONST               2
             1041  BINARY_MULTIPLY  
             1042  BINARY_MULTIPLY  
             1043  LOAD_FAST             7  'opname'
             1046  BUILD_TUPLE_3         3 
             1049  BINARY_MODULO    
             1050  STORE_FAST           25  'rule'

 L. 389      1053  LOAD_FAST             0  'self'
             1056  LOAD_ATTR            36  'add_unique_rule'
             1059  LOAD_FAST            25  'rule'
             1062  LOAD_FAST             7  'opname'
             1065  LOAD_FAST            29  'token'
             1068  LOAD_ATTR            31  'attr'
             1071  LOAD_FAST             2  'customize'
             1074  CALL_FUNCTION_4       4  None
             1077  POP_TOP          

 L. 390      1078  LOAD_CONST               'dict ::=  %s'
             1081  LOAD_FAST            16  'kvlist_n'
             1084  BINARY_MODULO    
             1085  STORE_FAST           25  'rule'
             1088  JUMP_FORWARD          1  'to 1092'
           1091_0  COME_FROM           917  '917'
             1091  POP_TOP          
           1092_0  COME_FROM          1088  '1088'

 L. 391      1092  LOAD_FAST             0  'self'
             1095  LOAD_ATTR            36  'add_unique_rule'
             1098  LOAD_FAST            25  'rule'
             1101  LOAD_FAST             7  'opname'
             1104  LOAD_FAST            29  'token'
             1107  LOAD_ATTR            31  'attr'
             1110  LOAD_FAST             2  'customize'
             1113  CALL_FUNCTION_4       4  None
             1116  POP_TOP          
             1117  JUMP_BACK           302  'to 302'
           1120_0  COME_FROM           677  '677'
             1120  POP_TOP          

 L. 393      1121  LOAD_FAST             7  'opname'
             1124  LOAD_ATTR            34  'startswith'
             1127  LOAD_CONST               'BUILD_MAP_UNPACK_WITH_CALL'
             1130  CALL_FUNCTION_1       1  None
             1133  JUMP_IF_FALSE        49  'to 1185'
             1136  POP_TOP          

 L. 394      1137  LOAD_FAST            29  'token'
             1140  LOAD_ATTR            31  'attr'
             1143  STORE_FAST           32  'v'

 L. 395      1146  LOAD_CONST               'build_map_unpack_with_call ::= %s%s'
             1149  LOAD_CONST               'expr '
             1152  LOAD_FAST            32  'v'
             1155  BINARY_MULTIPLY  
             1156  LOAD_FAST             7  'opname'
             1159  BUILD_TUPLE_2         2 
             1162  BINARY_MODULO    
             1163  STORE_FAST           25  'rule'

 L. 396      1166  LOAD_FAST             0  'self'
             1169  LOAD_ATTR            17  'addRule'
             1172  LOAD_FAST            25  'rule'
             1175  LOAD_GLOBAL          18  'nop_func'
             1178  CALL_FUNCTION_2       2  None
             1181  POP_TOP          
             1182  JUMP_BACK           302  'to 302'
           1185_0  COME_FROM          1133  '1133'
             1185  POP_TOP          

 L. 398      1186  LOAD_FAST             7  'opname'
             1189  LOAD_ATTR            34  'startswith'
             1192  LOAD_CONST               'BUILD_TUPLE_UNPACK_WITH_CALL'
             1195  CALL_FUNCTION_1       1  None
             1198  JUMP_IF_FALSE       127  'to 1328'
             1201  POP_TOP          

 L. 399      1202  LOAD_FAST            29  'token'
             1205  LOAD_ATTR            31  'attr'
             1208  STORE_FAST           32  'v'

 L. 400      1211  LOAD_CONST               'build_tuple_unpack_with_call ::= '
             1214  LOAD_CONST               'expr1024 '
             1217  LOAD_GLOBAL          37  'int'
             1220  LOAD_FAST            32  'v'
             1223  LOAD_CONST               1024
             1226  BINARY_FLOOR_DIVIDE
             1227  CALL_FUNCTION_1       1  None
             1230  BINARY_MULTIPLY  
             1231  BINARY_ADD       
             1232  LOAD_CONST               'expr32 '
             1235  LOAD_GLOBAL          37  'int'
             1238  LOAD_FAST            32  'v'
             1241  LOAD_CONST               32
             1244  BINARY_FLOOR_DIVIDE
             1245  LOAD_CONST               32
             1248  BINARY_MODULO    
             1249  CALL_FUNCTION_1       1  None
             1252  BINARY_MULTIPLY  
             1253  BINARY_ADD       
             1254  LOAD_CONST               'expr '
             1257  LOAD_FAST            32  'v'
             1260  LOAD_CONST               32
             1263  BINARY_MODULO    
             1264  BINARY_MULTIPLY  
             1265  BINARY_ADD       
             1266  LOAD_FAST             7  'opname'
             1269  BINARY_ADD       
             1270  STORE_FAST           25  'rule'

 L. 407      1273  LOAD_FAST             0  'self'
             1276  LOAD_ATTR            17  'addRule'
             1279  LOAD_FAST            25  'rule'
             1282  LOAD_GLOBAL          18  'nop_func'
             1285  CALL_FUNCTION_2       2  None
             1288  POP_TOP          

 L. 408      1289  LOAD_CONST               'starred ::= %s %s'
             1292  LOAD_CONST               'expr '
             1295  LOAD_FAST            32  'v'
             1298  BINARY_MULTIPLY  
             1299  LOAD_FAST             7  'opname'
             1302  BUILD_TUPLE_2         2 
             1305  BINARY_MODULO    
             1306  STORE_FAST           25  'rule'

 L. 409      1309  LOAD_FAST             0  'self'
             1312  LOAD_ATTR            17  'addRule'
             1315  LOAD_FAST            25  'rule'
             1318  LOAD_GLOBAL          18  'nop_func'
             1321  CALL_FUNCTION_2       2  None
             1324  POP_TOP          
             1325  JUMP_BACK           302  'to 302'
           1328_0  COME_FROM          1198  '1198'
             1328  POP_TOP          

 L. 411      1329  LOAD_FAST             5  'opname_base'
             1332  LOAD_CONST               ('BUILD_LIST', 'BUILD_SET', 'BUILD_TUPLE', 'BUILD_TUPLE_UNPACK')
             1335  COMPARE_OP            6  in
             1338  JUMP_IF_FALSE       421  'to 1762'
             1341  POP_TOP          

 L. 417      1342  LOAD_FAST            29  'token'
             1345  LOAD_ATTR            31  'attr'
             1348  STORE_FAST           32  'v'

 L. 419      1351  LOAD_GLOBAL           0  'False'
             1354  STORE_FAST            4  'is_LOAD_CLOSURE'

 L. 420      1357  LOAD_FAST             5  'opname_base'
             1360  LOAD_CONST               'BUILD_TUPLE'
             1363  COMPARE_OP            2  ==
             1366  JUMP_IF_FALSE       128  'to 1497'
           1369_0  THEN                     1498
             1369  POP_TOP          

 L. 423      1370  LOAD_GLOBAL          16  'True'
             1373  STORE_FAST            4  'is_LOAD_CLOSURE'

 L. 424      1376  SETUP_LOOP           59  'to 1438'
             1379  LOAD_GLOBAL          39  'range'
             1382  LOAD_FAST            32  'v'
             1385  CALL_FUNCTION_1       1  None
             1388  GET_ITER         
             1389  FOR_ITER             45  'to 1437'
             1392  STORE_FAST           22  'j'

 L. 425      1395  LOAD_FAST             1  'tokens'
             1398  LOAD_FAST            20  'i'
             1401  LOAD_FAST            22  'j'
             1404  BINARY_SUBTRACT  
             1405  LOAD_CONST               1
             1408  BINARY_SUBTRACT  
             1409  BINARY_SUBSCR    
             1410  LOAD_ATTR             9  'kind'
             1413  LOAD_CONST               'LOAD_CLOSURE'
             1416  COMPARE_OP            3  !=
             1419  JUMP_IF_FALSE        11  'to 1433'
             1422  POP_TOP          

 L. 426      1423  LOAD_GLOBAL           0  'False'
             1426  STORE_FAST            4  'is_LOAD_CLOSURE'

 L. 427      1429  BREAK_LOOP       
             1430  JUMP_BACK          1389  'to 1389'
           1433_0  COME_FROM          1419  '1419'
             1433  POP_TOP          
             1434  JUMP_BACK          1389  'to 1389'
             1437  POP_BLOCK        
           1438_0  COME_FROM          1376  '1376'

 L. 428      1438  LOAD_FAST             4  'is_LOAD_CLOSURE'
             1441  JUMP_IF_FALSE        49  'to 1493'
           1444_0  THEN                     1494
             1444  POP_TOP          

 L. 429      1445  LOAD_CONST               'load_closure ::= %s%s'
             1448  LOAD_CONST               'LOAD_CLOSURE '
             1451  LOAD_FAST            32  'v'
             1454  BINARY_MULTIPLY  
             1455  LOAD_FAST             7  'opname'
             1458  BUILD_TUPLE_2         2 
             1461  BINARY_MODULO    
             1462  STORE_FAST           25  'rule'

 L. 430      1465  LOAD_FAST             0  'self'
             1468  LOAD_ATTR            36  'add_unique_rule'
             1471  LOAD_FAST            25  'rule'
             1474  LOAD_FAST             7  'opname'
             1477  LOAD_FAST            29  'token'
             1480  LOAD_ATTR            31  'attr'
             1483  LOAD_FAST             2  'customize'
             1486  CALL_FUNCTION_4       4  None
             1489  POP_TOP          
             1490  JUMP_ABSOLUTE      1498  'to 1498'
           1493_0  COME_FROM          1441  '1441'
             1493  POP_TOP          
             1494  JUMP_FORWARD          1  'to 1498'
           1497_0  COME_FROM          1366  '1366'
             1497  POP_TOP          
           1498_0  COME_FROM          1494  '1494'

 L. 431      1498  LOAD_FAST             4  'is_LOAD_CLOSURE'
             1501  UNARY_NOT        
             1502  JUMP_IF_TRUE         13  'to 1518'
             1505  POP_TOP          
             1506  LOAD_FAST            32  'v'
             1509  LOAD_CONST               0
             1512  COMPARE_OP            2  ==
           1515_0  COME_FROM          1502  '1502'
             1515  JUMP_IF_FALSE       237  'to 1755'
             1518  POP_TOP          

 L. 434      1519  LOAD_FAST            29  'token'
             1522  LOAD_ATTR            31  'attr'
             1525  STORE_FAST           14  'build_count'

 L. 435      1528  LOAD_FAST            14  'build_count'
             1531  LOAD_CONST               1024
             1534  BINARY_FLOOR_DIVIDE
             1535  STORE_FAST           21  'thousands'

 L. 436      1538  LOAD_FAST            14  'build_count'
             1541  LOAD_CONST               32
             1544  BINARY_FLOOR_DIVIDE
             1545  LOAD_CONST               32
             1548  BINARY_MODULO    
             1549  STORE_FAST           18  'thirty32s'

 L. 437      1552  LOAD_FAST            18  'thirty32s'
             1555  LOAD_CONST               0
             1558  COMPARE_OP            4  >
             1561  JUMP_IF_FALSE        40  'to 1604'
           1564_0  THEN                     1605
             1564  POP_TOP          

 L. 438      1565  LOAD_CONST               'expr32 ::=%s'
             1568  LOAD_CONST               ' expr'
             1571  LOAD_CONST               32
             1574  BINARY_MULTIPLY  
             1575  BINARY_MODULO    
             1576  STORE_FAST           25  'rule'

 L. 439      1579  LOAD_FAST             0  'self'
             1582  LOAD_ATTR            36  'add_unique_rule'
             1585  LOAD_FAST            25  'rule'
             1588  LOAD_FAST             5  'opname_base'
             1591  LOAD_FAST            14  'build_count'
             1594  LOAD_FAST             2  'customize'
             1597  CALL_FUNCTION_4       4  None
             1600  POP_TOP          

 L. 440      1601  JUMP_FORWARD          1  'to 1605'
           1604_0  COME_FROM          1561  '1561'
             1604  POP_TOP          
           1605_0  COME_FROM          1601  '1601'

 L. 441      1605  LOAD_FAST            21  'thousands'
             1608  LOAD_CONST               0
             1611  COMPARE_OP            4  >
             1614  JUMP_IF_FALSE        34  'to 1651'
           1617_0  THEN                     1652
             1617  POP_TOP          

 L. 442      1618  LOAD_FAST             0  'self'
             1621  LOAD_ATTR            36  'add_unique_rule'
             1624  LOAD_CONST               'expr1024 ::=%s'
             1627  LOAD_CONST               ' expr32'
             1630  LOAD_CONST               32
             1633  BINARY_MULTIPLY  
             1634  BINARY_MODULO    

 L. 444      1635  LOAD_FAST             5  'opname_base'

 L. 445      1638  LOAD_FAST            14  'build_count'

 L. 446      1641  LOAD_FAST             2  'customize'
             1644  CALL_FUNCTION_4       4  None
             1647  POP_TOP          

 L. 448      1648  JUMP_FORWARD          1  'to 1652'
           1651_0  COME_FROM          1614  '1614'
             1651  POP_TOP          
           1652_0  COME_FROM          1648  '1648'

 L. 449      1652  LOAD_FAST             5  'opname_base'
             1655  LOAD_FAST             5  'opname_base'
             1658  LOAD_ATTR            26  'find'
             1661  LOAD_CONST               '_'
             1664  CALL_FUNCTION_1       1  None
             1667  LOAD_CONST               1
             1670  BINARY_ADD       
             1671  SLICE+1          
             1672  LOAD_ATTR            44  'lower'
             1675  CALL_FUNCTION_0       0  None
             1678  STORE_FAST           17  'collection'

 L. 450      1681  LOAD_CONST               '%s ::= '
             1684  LOAD_FAST            17  'collection'
             1687  BINARY_MODULO    
             1688  LOAD_CONST               'expr1024 '
             1691  LOAD_FAST            21  'thousands'
             1694  BINARY_MULTIPLY  
             1695  BINARY_ADD       
             1696  LOAD_CONST               'expr32 '
             1699  LOAD_FAST            18  'thirty32s'
             1702  BINARY_MULTIPLY  
             1703  BINARY_ADD       
             1704  LOAD_CONST               'expr '
             1707  LOAD_FAST            14  'build_count'
             1710  LOAD_CONST               32
             1713  BINARY_MODULO    
             1714  BINARY_MULTIPLY  
             1715  BINARY_ADD       
             1716  LOAD_FAST             7  'opname'
             1719  BINARY_ADD       
             1720  STORE_FAST           25  'rule'

 L. 457      1723  LOAD_FAST             0  'self'
             1726  LOAD_ATTR            46  'add_unique_rules'
             1729  LOAD_CONST               'expr ::= %s'
             1732  LOAD_FAST            17  'collection'
             1735  BINARY_MODULO    
             1736  LOAD_FAST            25  'rule'
             1739  BUILD_LIST_2          2 
             1742  LOAD_FAST             2  'customize'
             1745  CALL_FUNCTION_2       2  None
             1748  POP_TOP          

 L. 458      1749  CONTINUE            302  'to 302'
             1752  JUMP_BACK           302  'to 302'
           1755_0  COME_FROM          1515  '1515'
             1755  POP_TOP          

 L. 459      1756  CONTINUE            302  'to 302'
             1759  JUMP_BACK           302  'to 302'
           1762_0  COME_FROM          1338  '1338'
             1762  POP_TOP          

 L. 460      1763  LOAD_FAST             5  'opname_base'
             1766  LOAD_CONST               'BUILD_SLICE'
             1769  COMPARE_OP            2  ==
             1772  JUMP_IF_FALSE        98  'to 1873'
             1775  POP_TOP          

 L. 461      1776  LOAD_FAST            29  'token'
             1779  LOAD_ATTR            31  'attr'
             1782  LOAD_CONST               2
             1785  COMPARE_OP            2  ==
             1788  JUMP_IF_FALSE        26  'to 1817'
             1791  POP_TOP          

 L. 462      1792  LOAD_FAST             0  'self'
             1795  LOAD_ATTR            46  'add_unique_rules'
             1798  LOAD_CONST               'expr ::= build_slice2'
             1801  LOAD_CONST               'build_slice2 ::= expr expr BUILD_SLICE_2'
             1804  BUILD_LIST_2          2 

 L. 467      1807  LOAD_FAST             2  'customize'
             1810  CALL_FUNCTION_2       2  None
             1813  POP_TOP          
             1814  JUMP_ABSOLUTE      5419  'to 5419'
           1817_0  COME_FROM          1788  '1788'
             1817  POP_TOP          

 L. 470      1818  LOAD_FAST            29  'token'
             1821  LOAD_ATTR            31  'attr'
             1824  LOAD_CONST               3
             1827  COMPARE_OP            2  ==
             1830  JUMP_IF_TRUE         14  'to 1847'
             1833  POP_TOP          
             1834  LOAD_ASSERT              AssertionError
             1837  LOAD_CONST               'BUILD_SLICE value must be 2 or 3; is %s'
             1840  LOAD_FAST            32  'v'
             1843  BINARY_MODULO    
             1844  RAISE_VARARGS_2       2  None
           1847_0  COME_FROM          1830  '1830'
             1847  POP_TOP          

 L. 473      1848  LOAD_FAST             0  'self'
             1851  LOAD_ATTR            46  'add_unique_rules'
             1854  LOAD_CONST               'expr ::= build_slice3'
             1857  LOAD_CONST               'build_slice3 ::= expr expr expr BUILD_SLICE_3'
             1860  BUILD_LIST_2          2 

 L. 478      1863  LOAD_FAST             2  'customize'
             1866  CALL_FUNCTION_2       2  None
             1869  POP_TOP          
             1870  JUMP_BACK           302  'to 302'
           1873_0  COME_FROM          1772  '1772'
             1873  POP_TOP          

 L. 481      1874  LOAD_FAST             7  'opname'
             1877  LOAD_ATTR            34  'startswith'
             1880  LOAD_CONST               'BUILD_STRING'
             1883  CALL_FUNCTION_1       1  None
             1886  JUMP_IF_FALSE        91  'to 1980'
             1889  POP_TOP          

 L. 482      1890  LOAD_FAST            29  'token'
             1893  LOAD_ATTR            31  'attr'
             1896  STORE_FAST           32  'v'

 L. 483      1899  LOAD_CONST               '\n                    expr                 ::= joined_str\n                    joined_str           ::= %sBUILD_STRING_%d\n                '
             1902  LOAD_CONST               'expr '
             1905  LOAD_FAST            32  'v'
             1908  BINARY_MULTIPLY  
             1909  LOAD_FAST            32  'v'
             1912  BUILD_TUPLE_2         2 
             1915  BINARY_MODULO    
             1916  STORE_FAST            6  'rules_str'

 L. 490      1919  LOAD_FAST             0  'self'
             1922  LOAD_ATTR            29  'add_unique_doc_rules'
             1925  LOAD_FAST             6  'rules_str'
             1928  LOAD_FAST             2  'customize'
             1931  CALL_FUNCTION_2       2  None
             1934  POP_TOP          

 L. 491      1935  LOAD_CONST               'FORMAT_VALUE_ATTR'
             1938  LOAD_FAST             0  'self'
             1941  LOAD_ATTR            11  'seen_ops'
             1944  COMPARE_OP            6  in
             1947  JUMP_IF_FALSE        26  'to 1976'
             1950  POP_TOP          

 L. 492      1951  LOAD_CONST               '\n                      formatted_value_attr ::= expr expr FORMAT_VALUE_ATTR expr BUILD_STRING\n                      expr                 ::= formatted_value_attr\n                    '
             1954  STORE_FAST            6  'rules_str'

 L. 496      1957  LOAD_FAST             0  'self'
             1960  LOAD_ATTR            29  'add_unique_doc_rules'
             1963  LOAD_FAST             6  'rules_str'
             1966  LOAD_FAST             2  'customize'
             1969  CALL_FUNCTION_2       2  None
             1972  POP_TOP          
             1973  JUMP_ABSOLUTE      5419  'to 5419'
           1976_0  COME_FROM          1947  '1947'
             1976  POP_TOP          
             1977  JUMP_BACK           302  'to 302'
           1980_0  COME_FROM          1886  '1886'
             1980  POP_TOP          

 L. 498      1981  LOAD_FAST             7  'opname'
             1984  LOAD_GLOBAL           2  'frozenset'
             1987  LOAD_CONST               ('CALL_FUNCTION', 'CALL_FUNCTION_EX', 'CALL_FUNCTION_EX_KW', 'CALL_FUNCTION_VAR', 'CALL_FUNCTION_VAR_KW')
             1990  CALL_FUNCTION_1       1  None
             1993  COMPARE_OP            6  in
             1996  JUMP_IF_TRUE         16  'to 2015'
             1999  POP_TOP          
             2000  LOAD_FAST             7  'opname'
             2003  LOAD_ATTR            34  'startswith'
             2006  LOAD_CONST               'CALL_FUNCTION_KW'
             2009  CALL_FUNCTION_1       1  None
           2012_0  COME_FROM          1996  '1996'
             2012  JUMP_IF_FALSE        89  'to 2104'
             2015  POP_TOP          

 L. 508      2016  LOAD_FAST             7  'opname'
             2019  LOAD_CONST               'CALL_FUNCTION'
             2022  COMPARE_OP            2  ==
             2025  JUMP_IF_FALSE        42  'to 2070'
             2028  POP_TOP          
             2029  LOAD_FAST            29  'token'
             2032  LOAD_ATTR            31  'attr'
             2035  LOAD_CONST               1
             2038  COMPARE_OP            2  ==
             2041  JUMP_IF_FALSE        26  'to 2070'
           2044_0  THEN                     2071
             2044  POP_TOP          

 L. 509      2045  LOAD_CONST               '\n                     dict_comp    ::= LOAD_DICTCOMP LOAD_STR MAKE_FUNCTION_0 expr\n                                      GET_ITER CALL_FUNCTION_1\n                    classdefdeco1 ::= expr classdefdeco2 CALL_FUNCTION_1\n                    classdefdeco1 ::= expr classdefdeco1 CALL_FUNCTION_1\n                    '
             2048  STORE_FAST           25  'rule'

 L. 515      2051  LOAD_FAST             0  'self'
             2054  LOAD_ATTR            17  'addRule'
             2057  LOAD_FAST            25  'rule'
             2060  LOAD_GLOBAL          18  'nop_func'
             2063  CALL_FUNCTION_2       2  None
             2066  POP_TOP          
             2067  JUMP_FORWARD          1  'to 2071'
           2070_0  COME_FROM          2041  '2041'
           2070_1  COME_FROM          2025  '2025'
             2070  POP_TOP          
           2071_0  COME_FROM          2067  '2067'

 L. 517      2071  LOAD_FAST             0  'self'
             2074  LOAD_ATTR            48  'custom_classfunc_rule'
             2077  LOAD_FAST             7  'opname'
             2080  LOAD_FAST            29  'token'
             2083  LOAD_FAST             2  'customize'
             2086  LOAD_FAST             1  'tokens'
             2089  LOAD_FAST            20  'i'
             2092  LOAD_CONST               1
             2095  BINARY_ADD       
             2096  BINARY_SUBSCR    
             2097  CALL_FUNCTION_4       4  None
             2100  POP_TOP          
             2101  JUMP_BACK           302  'to 302'
           2104_0  COME_FROM          2012  '2012'
             2104  POP_TOP          

 L. 520      2105  LOAD_FAST             5  'opname_base'
             2108  LOAD_CONST               'CALL_METHOD'
             2111  COMPARE_OP            2  ==
             2114  JUMP_IF_FALSE       110  'to 2227'
             2117  POP_TOP          

 L. 523      2118  LOAD_FAST             0  'self'
             2121  LOAD_ATTR            49  'get_pos_kw'
             2124  LOAD_FAST            29  'token'
             2127  CALL_FUNCTION_1       1  None
             2130  UNPACK_SEQUENCE_2     2 
             2133  STORE_FAST           23  'args_pos'
             2136  STORE_FAST            3  'args_kw'

 L. 526      2139  LOAD_GLOBAL          19  'len'
             2142  LOAD_FAST             5  'opname_base'
             2145  CALL_FUNCTION_1       1  None
             2148  LOAD_GLOBAL          19  'len'
             2151  LOAD_CONST               'CALL_METHOD'
             2154  CALL_FUNCTION_1       1  None
             2157  BINARY_SUBTRACT  
             2158  LOAD_CONST               3
             2161  BINARY_FLOOR_DIVIDE
             2162  STORE_FAST            9  'nak'

 L. 527      2165  LOAD_CONST               'call ::= expr '
             2168  LOAD_CONST               'pos_arg '
             2171  LOAD_FAST            23  'args_pos'
             2174  BINARY_MULTIPLY  
             2175  BINARY_ADD       
             2176  LOAD_CONST               'kwarg '
             2179  LOAD_FAST             3  'args_kw'
             2182  BINARY_MULTIPLY  
             2183  BINARY_ADD       
             2184  LOAD_CONST               'expr '
             2187  LOAD_FAST             9  'nak'
             2190  BINARY_MULTIPLY  
             2191  BINARY_ADD       
             2192  LOAD_FAST             7  'opname'
             2195  BINARY_ADD       
             2196  STORE_FAST           25  'rule'

 L. 534      2199  LOAD_FAST             0  'self'
             2202  LOAD_ATTR            36  'add_unique_rule'
             2205  LOAD_FAST            25  'rule'
             2208  LOAD_FAST             7  'opname'
             2211  LOAD_FAST            29  'token'
             2214  LOAD_ATTR            31  'attr'
             2217  LOAD_FAST             2  'customize'
             2220  CALL_FUNCTION_4       4  None
             2223  POP_TOP          
             2224  JUMP_BACK           302  'to 302'
           2227_0  COME_FROM          2114  '2114'
             2227  POP_TOP          

 L. 536      2228  LOAD_FAST             7  'opname'
             2231  LOAD_CONST               'CONTINUE'
             2234  COMPARE_OP            2  ==
             2237  JUMP_IF_FALSE        33  'to 2273'
             2240  POP_TOP          

 L. 537      2241  LOAD_FAST             0  'self'
             2244  LOAD_ATTR            17  'addRule'
             2247  LOAD_CONST               'continue ::= CONTINUE'
             2250  LOAD_GLOBAL          18  'nop_func'
             2253  CALL_FUNCTION_2       2  None
             2256  POP_TOP          

 L. 538      2257  LOAD_FAST            11  'custom_ops_processed'
             2260  LOAD_ATTR            53  'add'
             2263  LOAD_FAST             7  'opname'
             2266  CALL_FUNCTION_1       1  None
             2269  POP_TOP          
             2270  JUMP_BACK           302  'to 302'
           2273_0  COME_FROM          2237  '2237'
             2273  POP_TOP          

 L. 539      2274  LOAD_FAST             7  'opname'
             2277  LOAD_CONST               'CONTINUE_LOOP'
             2280  COMPARE_OP            2  ==
             2283  JUMP_IF_FALSE        33  'to 2319'
             2286  POP_TOP          

 L. 540      2287  LOAD_FAST             0  'self'
             2290  LOAD_ATTR            17  'addRule'
             2293  LOAD_CONST               'continue ::= CONTINUE_LOOP'
             2296  LOAD_GLOBAL          18  'nop_func'
             2299  CALL_FUNCTION_2       2  None
             2302  POP_TOP          

 L. 541      2303  LOAD_FAST            11  'custom_ops_processed'
             2306  LOAD_ATTR            53  'add'
             2309  LOAD_FAST             7  'opname'
             2312  CALL_FUNCTION_1       1  None
             2315  POP_TOP          
             2316  JUMP_BACK           302  'to 302'
           2319_0  COME_FROM          2283  '2283'
             2319  POP_TOP          

 L. 542      2320  LOAD_FAST             7  'opname'
             2323  LOAD_CONST               'DELETE_ATTR'
             2326  COMPARE_OP            2  ==
             2329  JUMP_IF_FALSE        33  'to 2365'
             2332  POP_TOP          

 L. 543      2333  LOAD_FAST             0  'self'
             2336  LOAD_ATTR            17  'addRule'
             2339  LOAD_CONST               'del_stmt ::= expr DELETE_ATTR'
             2342  LOAD_GLOBAL          18  'nop_func'
             2345  CALL_FUNCTION_2       2  None
             2348  POP_TOP          

 L. 544      2349  LOAD_FAST            11  'custom_ops_processed'
             2352  LOAD_ATTR            53  'add'
             2355  LOAD_FAST             7  'opname'
             2358  CALL_FUNCTION_1       1  None
             2361  POP_TOP          
             2362  JUMP_BACK           302  'to 302'
           2365_0  COME_FROM          2329  '2329'
             2365  POP_TOP          

 L. 545      2366  LOAD_FAST             7  'opname'
             2369  LOAD_CONST               'DELETE_DEREF'
             2372  COMPARE_OP            2  ==
             2375  JUMP_IF_FALSE        33  'to 2411'
             2378  POP_TOP          

 L. 546      2379  LOAD_FAST             0  'self'
             2382  LOAD_ATTR            17  'addRule'
             2385  LOAD_CONST               '\n                   stmt           ::= del_deref_stmt\n                   del_deref_stmt ::= DELETE_DEREF\n                   '

 L. 551      2388  LOAD_GLOBAL          18  'nop_func'
             2391  CALL_FUNCTION_2       2  None
             2394  POP_TOP          

 L. 553      2395  LOAD_FAST            11  'custom_ops_processed'
             2398  LOAD_ATTR            53  'add'
             2401  LOAD_FAST             7  'opname'
             2404  CALL_FUNCTION_1       1  None
             2407  POP_TOP          
             2408  JUMP_BACK           302  'to 302'
           2411_0  COME_FROM          2375  '2375'
             2411  POP_TOP          

 L. 554      2412  LOAD_FAST             7  'opname'
             2415  LOAD_CONST               'DELETE_SUBSCR'
             2418  COMPARE_OP            2  ==
             2421  JUMP_IF_FALSE        33  'to 2457'
             2424  POP_TOP          

 L. 555      2425  LOAD_FAST             0  'self'
             2428  LOAD_ATTR            17  'addRule'
             2431  LOAD_CONST               '\n                    del_stmt ::= delete_subscript\n                    delete_subscript ::= expr expr DELETE_SUBSCR\n                   '

 L. 560      2434  LOAD_GLOBAL          18  'nop_func'
             2437  CALL_FUNCTION_2       2  None
             2440  POP_TOP          

 L. 562      2441  LOAD_FAST            11  'custom_ops_processed'
             2444  LOAD_ATTR            53  'add'
             2447  LOAD_FAST             7  'opname'
             2450  CALL_FUNCTION_1       1  None
             2453  POP_TOP          
             2454  JUMP_BACK           302  'to 302'
           2457_0  COME_FROM          2421  '2421'
             2457  POP_TOP          

 L. 564      2458  LOAD_FAST             7  'opname'
             2461  LOAD_CONST               'FORMAT_VALUE'
             2464  COMPARE_OP            2  ==
             2467  JUMP_IF_FALSE        26  'to 2496'
             2470  POP_TOP          

 L. 565      2471  LOAD_CONST               '\n                    expr              ::= formatted_value1\n                    formatted_value1  ::= expr FORMAT_VALUE\n                '
             2474  STORE_FAST            6  'rules_str'

 L. 569      2477  LOAD_FAST             0  'self'
             2480  LOAD_ATTR            29  'add_unique_doc_rules'
             2483  LOAD_FAST             6  'rules_str'
             2486  LOAD_FAST             2  'customize'
             2489  CALL_FUNCTION_2       2  None
             2492  POP_TOP          
             2493  JUMP_BACK           302  'to 302'
           2496_0  COME_FROM          2467  '2467'
             2496  POP_TOP          

 L. 571      2497  LOAD_FAST             7  'opname'
             2500  LOAD_CONST               'FORMAT_VALUE_ATTR'
             2503  COMPARE_OP            2  ==
             2506  JUMP_IF_FALSE        26  'to 2535'
             2509  POP_TOP          

 L. 572      2510  LOAD_CONST               '\n                expr              ::= formatted_value2\n                formatted_value2  ::= expr expr FORMAT_VALUE_ATTR\n                '
             2513  STORE_FAST            6  'rules_str'

 L. 576      2516  LOAD_FAST             0  'self'
             2519  LOAD_ATTR            29  'add_unique_doc_rules'
             2522  LOAD_FAST             6  'rules_str'
             2525  LOAD_FAST             2  'customize'
             2528  CALL_FUNCTION_2       2  None
             2531  POP_TOP          
             2532  JUMP_BACK           302  'to 302'
           2535_0  COME_FROM          2506  '2506'
             2535  POP_TOP          

 L. 578      2536  LOAD_FAST             7  'opname'
             2539  LOAD_CONST               'GET_ITER'
             2542  COMPARE_OP            2  ==
             2545  JUMP_IF_FALSE        33  'to 2581'
             2548  POP_TOP          

 L. 579      2549  LOAD_FAST             0  'self'
             2552  LOAD_ATTR            17  'addRule'
             2555  LOAD_CONST               '\n                    expr      ::= get_iter\n                    get_iter  ::= expr GET_ITER\n                    '

 L. 584      2558  LOAD_GLOBAL          18  'nop_func'
             2561  CALL_FUNCTION_2       2  None
             2564  POP_TOP          

 L. 586      2565  LOAD_FAST            11  'custom_ops_processed'
             2568  LOAD_ATTR            53  'add'
             2571  LOAD_FAST             7  'opname'
             2574  CALL_FUNCTION_1       1  None
             2577  POP_TOP          
             2578  JUMP_BACK           302  'to 302'
           2581_0  COME_FROM          2545  '2545'
             2581  POP_TOP          

 L. 587      2582  LOAD_FAST             7  'opname'
             2585  LOAD_CONST               'GET_AITER'
             2588  COMPARE_OP            2  ==
             2591  JUMP_IF_FALSE        20  'to 2614'
             2594  POP_TOP          

 L. 588      2595  LOAD_FAST             0  'self'
             2598  LOAD_ATTR            17  'addRule'
             2601  LOAD_CONST               '\n                    expr                ::= generator_exp_async\n                    generator_exp_async ::= load_genexpr LOAD_STR MAKE_FUNCTION_0 expr\n                                            GET_AITER CALL_FUNCTION_1\n\n                    stmt                ::= genexpr_func_async\n\n                    func_async_prefix   ::= _come_froms SETUP_EXCEPT GET_ANEXT LOAD_CONST YIELD_FROM\n                    func_async_middle   ::= POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT\n                                            DUP_TOP LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_TRUE\n                                            END_FINALLY COME_FROM\n                    genexpr_func_async  ::= LOAD_FAST func_async_prefix\n                                            store func_async_middle comp_iter\n                                            JUMP_BACK COME_FROM\n                                            POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_TOP\n\n                    expr                ::= list_comp_async\n                    list_comp_async     ::= LOAD_LISTCOMP LOAD_STR MAKE_FUNCTION_0\n                                            expr GET_AITER CALL_FUNCTION_1\n                                            GET_AWAITABLE LOAD_CONST\n                                            YIELD_FROM\n\n                    expr                ::= list_comp_async\n                    list_afor2          ::= func_async_prefix\n                                            store func_async_middle list_iter\n                                            JUMP_BACK COME_FROM\n                                            POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_TOP\n                    list_comp_async     ::= BUILD_LIST_0 LOAD_FAST list_afor2\n                    get_aiter           ::= LOAD_DEREF GET_AITER\n                    list_afor           ::= get_aiter list_afor2\n                    list_iter           ::= list_afor\n                   '

 L. 621      2604  LOAD_GLOBAL          18  'nop_func'
             2607  CALL_FUNCTION_2       2  None
             2610  POP_TOP          
             2611  JUMP_BACK           302  'to 302'
           2614_0  COME_FROM          2591  '2591'
             2614  POP_TOP          

 L. 623      2615  LOAD_FAST             7  'opname'
             2618  LOAD_CONST               'JUMP_IF_NOT_DEBUG'
             2621  COMPARE_OP            2  ==
             2624  JUMP_IF_FALSE        42  'to 2669'
             2627  POP_TOP          

 L. 624      2628  LOAD_FAST            29  'token'
             2631  LOAD_ATTR            31  'attr'
             2634  STORE_FAST           32  'v'

 L. 625      2637  LOAD_FAST             0  'self'
             2640  LOAD_ATTR            17  'addRule'
             2643  LOAD_CONST               '\n                    stmt        ::= assert_pypy\n                    stmt        ::= assert2_pypy", nop_func)\n                    assert_pypy ::=  JUMP_IF_NOT_DEBUG expr jmp_true\n                                     LOAD_ASSERT RAISE_VARARGS_1 COME_FROM\n                    assert2_pypy ::= JUMP_IF_NOT_DEBUG assert_expr jmp_true\n                                     LOAD_ASSERT expr CALL_FUNCTION_1\n                                     RAISE_VARARGS_1 COME_FROM\n                    assert2_pypy ::= JUMP_IF_NOT_DEBUG expr jmp_true\n                                     LOAD_ASSERT expr CALL_FUNCTION_1\n                                     RAISE_VARARGS_1 COME_FROM,\n                    '

 L. 638      2646  LOAD_GLOBAL          18  'nop_func'
             2649  CALL_FUNCTION_2       2  None
             2652  POP_TOP          

 L. 640      2653  LOAD_FAST            11  'custom_ops_processed'
             2656  LOAD_ATTR            53  'add'
             2659  LOAD_FAST             7  'opname'
             2662  CALL_FUNCTION_1       1  None
             2665  POP_TOP          
             2666  JUMP_BACK           302  'to 302'
           2669_0  COME_FROM          2624  '2624'
             2669  POP_TOP          

 L. 641      2670  LOAD_FAST             7  'opname'
             2673  LOAD_CONST               'LOAD_BUILD_CLASS'
             2676  COMPARE_OP            2  ==
             2679  JUMP_IF_FALSE        29  'to 2711'
             2682  POP_TOP          

 L. 642      2683  LOAD_FAST             0  'self'
             2686  LOAD_ATTR            54  'custom_build_class_rule'
             2689  LOAD_FAST             7  'opname'
             2692  LOAD_FAST            20  'i'
             2695  LOAD_FAST            29  'token'
             2698  LOAD_FAST             1  'tokens'
             2701  LOAD_FAST             2  'customize'
             2704  CALL_FUNCTION_5       5  None
             2707  POP_TOP          
             2708  JUMP_BACK           302  'to 302'
           2711_0  COME_FROM          2679  '2679'
             2711  POP_TOP          

 L. 644      2712  LOAD_FAST             7  'opname'
             2715  LOAD_CONST               'LOAD_CLASSDEREF'
             2718  COMPARE_OP            2  ==
             2721  JUMP_IF_FALSE        33  'to 2757'
             2724  POP_TOP          

 L. 646      2725  LOAD_FAST             0  'self'
             2728  LOAD_ATTR            17  'addRule'
             2731  LOAD_CONST               'expr ::= LOAD_CLASSDEREF'
             2734  LOAD_GLOBAL          18  'nop_func'
             2737  CALL_FUNCTION_2       2  None
             2740  POP_TOP          

 L. 647      2741  LOAD_FAST            11  'custom_ops_processed'
             2744  LOAD_ATTR            53  'add'
             2747  LOAD_FAST             7  'opname'
             2750  CALL_FUNCTION_1       1  None
             2753  POP_TOP          
             2754  JUMP_BACK           302  'to 302'
           2757_0  COME_FROM          2721  '2721'
             2757  POP_TOP          

 L. 648      2758  LOAD_FAST             7  'opname'
             2761  LOAD_CONST               'LOAD_CLASSNAME'
             2764  COMPARE_OP            2  ==
             2767  JUMP_IF_FALSE        33  'to 2803'
             2770  POP_TOP          

 L. 649      2771  LOAD_FAST             0  'self'
             2774  LOAD_ATTR            17  'addRule'
             2777  LOAD_CONST               'expr ::= LOAD_CLASSNAME'
             2780  LOAD_GLOBAL          18  'nop_func'
             2783  CALL_FUNCTION_2       2  None
             2786  POP_TOP          

 L. 650      2787  LOAD_FAST            11  'custom_ops_processed'
             2790  LOAD_ATTR            53  'add'
             2793  LOAD_FAST             7  'opname'
             2796  CALL_FUNCTION_1       1  None
             2799  POP_TOP          
             2800  JUMP_BACK           302  'to 302'
           2803_0  COME_FROM          2767  '2767'
             2803  POP_TOP          

 L. 651      2804  LOAD_FAST             7  'opname'
             2807  LOAD_CONST               'LOAD_DICTCOMP'
             2810  COMPARE_OP            2  ==
             2813  JUMP_IF_FALSE        59  'to 2875'
             2816  POP_TOP          

 L. 652      2817  LOAD_FAST            34  'has_get_iter_call_function1'
             2820  JUMP_IF_FALSE        35  'to 2858'
           2823_0  THEN                     2859
             2823  POP_TOP          

 L. 653      2824  LOAD_CONST               'dict_comp ::= LOAD_DICTCOMP %sMAKE_FUNCTION_0 expr GET_ITER CALL_FUNCTION_1'
             2827  STORE_FAST           12  'rule_pat'

 L. 657      2830  LOAD_FAST             0  'self'
             2833  LOAD_ATTR            56  'add_make_function_rule'
             2836  LOAD_FAST            12  'rule_pat'
             2839  LOAD_FAST             7  'opname'
             2842  LOAD_FAST            29  'token'
             2845  LOAD_ATTR            31  'attr'
             2848  LOAD_FAST             2  'customize'
             2851  CALL_FUNCTION_4       4  None
             2854  POP_TOP          

 L. 658      2855  JUMP_FORWARD          1  'to 2859'
           2858_0  COME_FROM          2820  '2820'
             2858  POP_TOP          
           2859_0  COME_FROM          2855  '2855'

 L. 659      2859  LOAD_FAST            11  'custom_ops_processed'
             2862  LOAD_ATTR            53  'add'
             2865  LOAD_FAST             7  'opname'
             2868  CALL_FUNCTION_1       1  None
             2871  POP_TOP          
             2872  JUMP_BACK           302  'to 302'
           2875_0  COME_FROM          2813  '2813'
             2875  POP_TOP          

 L. 660      2876  LOAD_FAST             7  'opname'
             2879  LOAD_CONST               'LOAD_ATTR'
             2882  COMPARE_OP            2  ==
             2885  JUMP_IF_FALSE        33  'to 2921'
             2888  POP_TOP          

 L. 661      2889  LOAD_FAST             0  'self'
             2892  LOAD_ATTR            17  'addRule'
             2895  LOAD_CONST               '\n                  expr      ::= attribute\n                  attribute ::= expr LOAD_ATTR\n                  '

 L. 666      2898  LOAD_GLOBAL          18  'nop_func'
             2901  CALL_FUNCTION_2       2  None
             2904  POP_TOP          

 L. 668      2905  LOAD_FAST            11  'custom_ops_processed'
             2908  LOAD_ATTR            53  'add'
             2911  LOAD_FAST             7  'opname'
             2914  CALL_FUNCTION_1       1  None
             2917  POP_TOP          
             2918  JUMP_BACK           302  'to 302'
           2921_0  COME_FROM          2885  '2885'
             2921  POP_TOP          

 L. 669      2922  LOAD_FAST             7  'opname'
             2925  LOAD_CONST               'LOAD_LISTCOMP'
             2928  COMPARE_OP            2  ==
             2931  JUMP_IF_FALSE        42  'to 2976'
             2934  POP_TOP          

 L. 670      2935  LOAD_FAST             0  'self'
             2938  LOAD_ATTR            36  'add_unique_rule'
             2941  LOAD_CONST               'expr ::= listcomp'
             2944  LOAD_FAST             7  'opname'
             2947  LOAD_FAST            29  'token'
             2950  LOAD_ATTR            31  'attr'
             2953  LOAD_FAST             2  'customize'
             2956  CALL_FUNCTION_4       4  None
             2959  POP_TOP          

 L. 671      2960  LOAD_FAST            11  'custom_ops_processed'
             2963  LOAD_ATTR            53  'add'
             2966  LOAD_FAST             7  'opname'
             2969  CALL_FUNCTION_1       1  None
             2972  POP_TOP          
             2973  JUMP_BACK           302  'to 302'
           2976_0  COME_FROM          2931  '2931'
             2976  POP_TOP          

 L. 672      2977  LOAD_FAST             7  'opname'
             2980  LOAD_CONST               'LOAD_NAME'
             2983  COMPARE_OP            2  ==
             2986  JUMP_IF_FALSE        65  'to 3054'
             2989  POP_TOP          

 L. 673      2990  LOAD_FAST            29  'token'
             2993  LOAD_ATTR            31  'attr'
             2996  LOAD_CONST               '__annotations__'
             2999  COMPARE_OP            2  ==
             3002  JUMP_IF_FALSE        45  'to 3050'
             3005  POP_TOP          
             3006  LOAD_CONST               'SETUP_ANNOTATIONS'
             3009  LOAD_FAST             0  'self'
             3012  LOAD_ATTR            11  'seen_ops'
             3015  COMPARE_OP            6  in
             3018  JUMP_IF_FALSE        29  'to 3050'
             3021  POP_TOP          

 L. 677      3022  LOAD_CONST               'LOAD_ANNOTATION'
             3025  LOAD_FAST            29  'token'
             3028  STORE_ATTR            9  'kind'

 L. 678      3031  LOAD_FAST             0  'self'
             3034  LOAD_ATTR            17  'addRule'
             3037  LOAD_CONST               '\n                        stmt       ::= SETUP_ANNOTATIONS\n                        stmt       ::= ann_assign\n                        ann_assign ::= expr LOAD_ANNOTATION LOAD_STR STORE_SUBSCR\n                        '

 L. 684      3040  LOAD_GLOBAL          18  'nop_func'
             3043  CALL_FUNCTION_2       2  None
             3046  POP_TOP          

 L. 686      3047  JUMP_ABSOLUTE      5419  'to 5419'
           3050_0  COME_FROM          3018  '3018'
           3050_1  COME_FROM          3002  '3002'
             3050  POP_TOP          
             3051  JUMP_BACK           302  'to 302'
           3054_0  COME_FROM          2986  '2986'
             3054  POP_TOP          

 L. 687      3055  LOAD_FAST             7  'opname'
             3058  LOAD_CONST               'LOAD_SETCOMP'
             3061  COMPARE_OP            2  ==
             3064  JUMP_IF_FALSE        75  'to 3142'
             3067  POP_TOP          

 L. 689      3068  LOAD_FAST            34  'has_get_iter_call_function1'
             3071  JUMP_IF_FALSE        51  'to 3125'
           3074_0  THEN                     3126
             3074  POP_TOP          

 L. 690      3075  LOAD_FAST             0  'self'
             3078  LOAD_ATTR            17  'addRule'
             3081  LOAD_CONST               'expr ::= set_comp'
             3084  LOAD_GLOBAL          18  'nop_func'
             3087  CALL_FUNCTION_2       2  None
             3090  POP_TOP          

 L. 691      3091  LOAD_CONST               'set_comp ::= LOAD_SETCOMP %sMAKE_FUNCTION_0 expr GET_ITER CALL_FUNCTION_1'
             3094  STORE_FAST           12  'rule_pat'

 L. 695      3097  LOAD_FAST             0  'self'
             3100  LOAD_ATTR            56  'add_make_function_rule'
             3103  LOAD_FAST            12  'rule_pat'
             3106  LOAD_FAST             7  'opname'
             3109  LOAD_FAST            29  'token'
             3112  LOAD_ATTR            31  'attr'
             3115  LOAD_FAST             2  'customize'
             3118  CALL_FUNCTION_4       4  None
             3121  POP_TOP          

 L. 696      3122  JUMP_FORWARD          1  'to 3126'
           3125_0  COME_FROM          3071  '3071'
             3125  POP_TOP          
           3126_0  COME_FROM          3122  '3122'

 L. 697      3126  LOAD_FAST            11  'custom_ops_processed'
             3129  LOAD_ATTR            53  'add'
             3132  LOAD_FAST             7  'opname'
             3135  CALL_FUNCTION_1       1  None
             3138  POP_TOP          
             3139  JUMP_BACK           302  'to 302'
           3142_0  COME_FROM          3064  '3064'
             3142  POP_TOP          

 L. 698      3143  LOAD_FAST             7  'opname'
             3146  LOAD_CONST               'LOOKUP_METHOD'
             3149  COMPARE_OP            2  ==
             3152  JUMP_IF_FALSE        33  'to 3188'
             3155  POP_TOP          

 L. 700      3156  LOAD_FAST             0  'self'
             3159  LOAD_ATTR            17  'addRule'
             3162  LOAD_CONST               '\n                             expr      ::= attribute\n                             attribute ::= expr LOOKUP_METHOD\n                             '

 L. 705      3165  LOAD_GLOBAL          18  'nop_func'
             3168  CALL_FUNCTION_2       2  None
             3171  POP_TOP          

 L. 707      3172  LOAD_FAST            11  'custom_ops_processed'
             3175  LOAD_ATTR            53  'add'
             3178  LOAD_FAST             7  'opname'
             3181  CALL_FUNCTION_1       1  None
             3184  POP_TOP          
             3185  JUMP_BACK           302  'to 302'
           3188_0  COME_FROM          3152  '3152'
             3188  POP_TOP          

 L. 708      3189  LOAD_FAST             7  'opname'
             3192  LOAD_ATTR            34  'startswith'
             3195  LOAD_CONST               'MAKE_CLOSURE'
             3198  CALL_FUNCTION_1       1  None
             3201  JUMP_IF_FALSE       650  'to 3854'
             3204  POP_TOP          

 L. 712      3205  LOAD_FAST             7  'opname'
             3208  LOAD_CONST               'MAKE_CLOSURE_0'
             3211  COMPARE_OP            2  ==
             3214  JUMP_IF_FALSE        42  'to 3259'
             3217  POP_TOP          
             3218  LOAD_CONST               'LOAD_DICTCOMP'
             3221  LOAD_FAST             0  'self'
             3224  LOAD_ATTR            11  'seen_ops'
             3227  COMPARE_OP            6  in
             3230  JUMP_IF_FALSE        26  'to 3259'
           3233_0  THEN                     3260
             3233  POP_TOP          

 L. 716      3234  LOAD_CONST               '\n                        dict_comp ::= load_closure LOAD_DICTCOMP LOAD_STR\n                                      MAKE_CLOSURE_0 expr\n                                      GET_ITER CALL_FUNCTION_1\n                    '
             3237  STORE_FAST           25  'rule'

 L. 721      3240  LOAD_FAST             0  'self'
             3243  LOAD_ATTR            17  'addRule'
             3246  LOAD_FAST            25  'rule'
             3249  LOAD_GLOBAL          18  'nop_func'
             3252  CALL_FUNCTION_2       2  None
             3255  POP_TOP          
             3256  JUMP_FORWARD          1  'to 3260'
           3259_0  COME_FROM          3230  '3230'
           3259_1  COME_FROM          3214  '3214'
             3259  POP_TOP          
           3260_0  COME_FROM          3256  '3256'

 L. 723      3260  LOAD_FAST            29  'token'
             3263  LOAD_ATTR            31  'attr'
             3266  UNPACK_SEQUENCE_3     3 
             3269  STORE_FAST           23  'args_pos'
             3272  STORE_FAST            3  'args_kw'
             3275  STORE_FAST           15  'annotate_args'

 L. 726      3278  LOAD_CONST               2
             3281  STORE_FAST           22  'j'

 L. 727      3284  LOAD_FAST            28  'is_pypy'
             3287  JUMP_IF_TRUE         34  'to 3324'
             3290  POP_TOP          
             3291  LOAD_FAST            20  'i'
             3294  LOAD_FAST            22  'j'
             3297  COMPARE_OP            5  >=
             3300  JUMP_IF_FALSE        70  'to 3373'
             3303  POP_TOP          
             3304  LOAD_FAST             1  'tokens'
             3307  LOAD_FAST            20  'i'
             3310  LOAD_FAST            22  'j'
             3313  BINARY_SUBTRACT  
             3314  BINARY_SUBSCR    
             3315  LOAD_CONST               'LOAD_LAMBDA'
             3318  COMPARE_OP            2  ==
           3321_0  COME_FROM          3300  '3300'
           3321_1  COME_FROM          3287  '3287'
             3321  JUMP_IF_FALSE        49  'to 3373'
           3324_0  THEN                     3374
             3324  POP_TOP          

 L. 728      3325  LOAD_CONST               'mklambda ::= %sload_closure LOAD_LAMBDA %%s%s'
             3328  LOAD_CONST               'pos_arg '
             3331  LOAD_FAST            23  'args_pos'
             3334  BINARY_MULTIPLY  
             3335  LOAD_FAST             7  'opname'
             3338  BUILD_TUPLE_2         2 
             3341  BINARY_MODULO    
             3342  STORE_FAST           12  'rule_pat'

 L. 732      3345  LOAD_FAST             0  'self'
             3348  LOAD_ATTR            56  'add_make_function_rule'
             3351  LOAD_FAST            12  'rule_pat'
             3354  LOAD_FAST             7  'opname'
             3357  LOAD_FAST            29  'token'
             3360  LOAD_ATTR            31  'attr'
             3363  LOAD_FAST             2  'customize'
             3366  CALL_FUNCTION_4       4  None
             3369  POP_TOP          
             3370  JUMP_FORWARD          1  'to 3374'
           3373_0  COME_FROM          3321  '3321'
             3373  POP_TOP          
           3374_0  COME_FROM          3370  '3370'

 L. 734      3374  LOAD_FAST            34  'has_get_iter_call_function1'
             3377  JUMP_IF_FALSE       324  'to 3704'
             3380  POP_TOP          

 L. 735      3381  LOAD_CONST               'generator_exp ::= %sload_closure load_genexpr %%s%s expr GET_ITER CALL_FUNCTION_1'
             3384  LOAD_CONST               'pos_arg '
             3387  LOAD_FAST            23  'args_pos'
             3390  BINARY_MULTIPLY  
             3391  LOAD_FAST             7  'opname'
             3394  BUILD_TUPLE_2         2 
             3397  BINARY_MODULO    
             3398  STORE_FAST           12  'rule_pat'

 L. 739      3401  LOAD_FAST             0  'self'
             3404  LOAD_ATTR            56  'add_make_function_rule'
             3407  LOAD_FAST            12  'rule_pat'
             3410  LOAD_FAST             7  'opname'
             3413  LOAD_FAST            29  'token'
             3416  LOAD_ATTR            31  'attr'
             3419  LOAD_FAST             2  'customize'
             3422  CALL_FUNCTION_4       4  None
             3425  POP_TOP          

 L. 741      3426  LOAD_FAST            34  'has_get_iter_call_function1'
             3429  JUMP_IF_FALSE       268  'to 3700'
             3432  POP_TOP          

 L. 742      3433  LOAD_FAST            28  'is_pypy'
             3436  JUMP_IF_TRUE         34  'to 3473'
             3439  POP_TOP          
             3440  LOAD_FAST            20  'i'
             3443  LOAD_FAST            22  'j'
             3446  COMPARE_OP            5  >=
             3449  JUMP_IF_FALSE        70  'to 3522'
             3452  POP_TOP          
             3453  LOAD_FAST             1  'tokens'
             3456  LOAD_FAST            20  'i'
             3459  LOAD_FAST            22  'j'
             3462  BINARY_SUBTRACT  
             3463  BINARY_SUBSCR    
             3464  LOAD_CONST               'LOAD_LISTCOMP'
             3467  COMPARE_OP            2  ==
           3470_0  COME_FROM          3449  '3449'
           3470_1  COME_FROM          3436  '3436'
             3470  JUMP_IF_FALSE        49  'to 3522'
           3473_0  THEN                     3523
             3473  POP_TOP          

 L. 748      3474  LOAD_CONST               'listcomp ::= %sload_closure LOAD_LISTCOMP %%s%s expr GET_ITER CALL_FUNCTION_1'
             3477  LOAD_CONST               'pos_arg '
             3480  LOAD_FAST            23  'args_pos'
             3483  BINARY_MULTIPLY  
             3484  LOAD_FAST             7  'opname'
             3487  BUILD_TUPLE_2         2 
             3490  BINARY_MODULO    
             3491  STORE_FAST           12  'rule_pat'

 L. 753      3494  LOAD_FAST             0  'self'
             3497  LOAD_ATTR            56  'add_make_function_rule'
             3500  LOAD_FAST            12  'rule_pat'
             3503  LOAD_FAST             7  'opname'
             3506  LOAD_FAST            29  'token'
             3509  LOAD_ATTR            31  'attr'
             3512  LOAD_FAST             2  'customize'
             3515  CALL_FUNCTION_4       4  None
             3518  POP_TOP          
             3519  JUMP_FORWARD          1  'to 3523'
           3522_0  COME_FROM          3470  '3470'
             3522  POP_TOP          
           3523_0  COME_FROM          3519  '3519'

 L. 756      3523  LOAD_FAST            28  'is_pypy'
             3526  JUMP_IF_TRUE         34  'to 3563'
             3529  POP_TOP          
             3530  LOAD_FAST            20  'i'
             3533  LOAD_FAST            22  'j'
             3536  COMPARE_OP            5  >=
             3539  JUMP_IF_FALSE        70  'to 3612'
             3542  POP_TOP          
             3543  LOAD_FAST             1  'tokens'
             3546  LOAD_FAST            20  'i'
             3549  LOAD_FAST            22  'j'
             3552  BINARY_SUBTRACT  
             3553  BINARY_SUBSCR    
             3554  LOAD_CONST               'LOAD_SETCOMP'
             3557  COMPARE_OP            2  ==
           3560_0  COME_FROM          3539  '3539'
           3560_1  COME_FROM          3526  '3526'
             3560  JUMP_IF_FALSE        49  'to 3612'
           3563_0  THEN                     3613
             3563  POP_TOP          

 L. 757      3564  LOAD_CONST               'set_comp ::= %sload_closure LOAD_SETCOMP %%s%s expr GET_ITER CALL_FUNCTION_1'
             3567  LOAD_CONST               'pos_arg '
             3570  LOAD_FAST            23  'args_pos'
             3573  BINARY_MULTIPLY  
             3574  LOAD_FAST             7  'opname'
             3577  BUILD_TUPLE_2         2 
             3580  BINARY_MODULO    
             3581  STORE_FAST           12  'rule_pat'

 L. 762      3584  LOAD_FAST             0  'self'
             3587  LOAD_ATTR            56  'add_make_function_rule'
             3590  LOAD_FAST            12  'rule_pat'
             3593  LOAD_FAST             7  'opname'
             3596  LOAD_FAST            29  'token'
             3599  LOAD_ATTR            31  'attr'
             3602  LOAD_FAST             2  'customize'
             3605  CALL_FUNCTION_4       4  None
             3608  POP_TOP          
             3609  JUMP_FORWARD          1  'to 3613'
           3612_0  COME_FROM          3560  '3560'
             3612  POP_TOP          
           3613_0  COME_FROM          3609  '3609'

 L. 765      3613  LOAD_FAST            28  'is_pypy'
             3616  JUMP_IF_TRUE         34  'to 3653'
             3619  POP_TOP          
             3620  LOAD_FAST            20  'i'
             3623  LOAD_FAST            22  'j'
             3626  COMPARE_OP            5  >=
             3629  JUMP_IF_FALSE        64  'to 3696'
             3632  POP_TOP          
             3633  LOAD_FAST             1  'tokens'
             3636  LOAD_FAST            20  'i'
             3639  LOAD_FAST            22  'j'
             3642  BINARY_SUBTRACT  
             3643  BINARY_SUBSCR    
             3644  LOAD_CONST               'LOAD_DICTCOMP'
             3647  COMPARE_OP            2  ==
           3650_0  COME_FROM          3629  '3629'
           3650_1  COME_FROM          3616  '3616'
             3650  JUMP_IF_FALSE        43  'to 3696'
             3653  POP_TOP          

 L. 766      3654  LOAD_FAST             0  'self'
             3657  LOAD_ATTR            36  'add_unique_rule'
             3660  LOAD_CONST               'dict_comp ::= %sload_closure LOAD_DICTCOMP %s expr GET_ITER CALL_FUNCTION_1'
             3663  LOAD_CONST               'pos_arg '
             3666  LOAD_FAST            23  'args_pos'
             3669  BINARY_MULTIPLY  
             3670  LOAD_FAST             7  'opname'
             3673  BUILD_TUPLE_2         2 
             3676  BINARY_MODULO    

 L. 770      3677  LOAD_FAST             7  'opname'

 L. 771      3680  LOAD_FAST            29  'token'
             3683  LOAD_ATTR            31  'attr'

 L. 772      3686  LOAD_FAST             2  'customize'
             3689  CALL_FUNCTION_4       4  None
             3692  POP_TOP          
             3693  JUMP_ABSOLUTE      3701  'to 3701'
           3696_0  COME_FROM          3650  '3650'
             3696  POP_TOP          
             3697  JUMP_ABSOLUTE      3705  'to 3705'
           3700_0  COME_FROM          3429  '3429'
             3700  POP_TOP          
             3701  JUMP_FORWARD          1  'to 3705'
           3704_0  COME_FROM          3377  '3377'
             3704  POP_TOP          
           3705_0  COME_FROM          3701  '3701'

 L. 775      3705  LOAD_FAST             3  'args_kw'
             3708  LOAD_CONST               0
             3711  COMPARE_OP            4  >
             3714  JUMP_IF_FALSE        10  'to 3727'
             3717  POP_TOP          

 L. 776      3718  LOAD_CONST               'kwargs '
             3721  STORE_FAST           10  'kwargs_str'
             3724  JUMP_FORWARD          7  'to 3734'
           3727_0  COME_FROM          3714  '3714'
             3727  POP_TOP          

 L. 778      3728  LOAD_CONST               ''
             3731  STORE_FAST           10  'kwargs_str'
           3734_0  COME_FROM          3724  '3724'

 L. 780      3734  LOAD_CONST               'mkfunc ::= %s%s%s load_closure LOAD_CODE LOAD_STR %s'
             3737  LOAD_CONST               'expr '
             3740  LOAD_FAST            23  'args_pos'
             3743  BINARY_MULTIPLY  
             3744  LOAD_FAST            10  'kwargs_str'
             3747  LOAD_CONST               'expr '
             3750  LOAD_FAST            15  'annotate_args'
             3753  BINARY_MULTIPLY  
             3754  LOAD_FAST             7  'opname'
             3757  BUILD_TUPLE_4         4 
             3760  BINARY_MODULO    
             3761  STORE_FAST           25  'rule'

 L. 787      3764  LOAD_FAST             0  'self'
             3767  LOAD_ATTR            36  'add_unique_rule'
             3770  LOAD_FAST            25  'rule'
             3773  LOAD_FAST             7  'opname'
             3776  LOAD_FAST            29  'token'
             3779  LOAD_ATTR            31  'attr'
             3782  LOAD_FAST             2  'customize'
             3785  CALL_FUNCTION_4       4  None
             3788  POP_TOP          

 L. 789      3789  LOAD_FAST             3  'args_kw'
             3792  LOAD_CONST               0
             3795  COMPARE_OP            2  ==
             3798  JUMP_IF_FALSE        49  'to 3850'
             3801  POP_TOP          

 L. 790      3802  LOAD_CONST               'mkfunc ::= %sload_closure load_genexpr %s'
             3805  LOAD_CONST               'pos_arg '
             3808  LOAD_FAST            23  'args_pos'
             3811  BINARY_MULTIPLY  
             3812  LOAD_FAST             7  'opname'
             3815  BUILD_TUPLE_2         2 
             3818  BINARY_MODULO    
             3819  STORE_FAST           25  'rule'

 L. 794      3822  LOAD_FAST             0  'self'
             3825  LOAD_ATTR            36  'add_unique_rule'
             3828  LOAD_FAST            25  'rule'
             3831  LOAD_FAST             7  'opname'
             3834  LOAD_FAST            29  'token'
             3837  LOAD_ATTR            31  'attr'
             3840  LOAD_FAST             2  'customize'
             3843  CALL_FUNCTION_4       4  None
             3846  POP_TOP          
             3847  JUMP_ABSOLUTE      5419  'to 5419'
           3850_0  COME_FROM          3798  '3798'
             3850  POP_TOP          

 L. 796      3851  JUMP_BACK           302  'to 302'
           3854_0  COME_FROM          3201  '3201'
             3854  POP_TOP          

 L. 797      3855  LOAD_FAST             5  'opname_base'
             3858  LOAD_ATTR            34  'startswith'
             3861  LOAD_CONST               'MAKE_FUNCTION'
             3864  CALL_FUNCTION_1       1  None
             3867  JUMP_IF_FALSE       943  'to 4813'
             3870  POP_TOP          

 L. 798      3871  LOAD_FAST            29  'token'
             3874  LOAD_ATTR            31  'attr'
             3877  UNPACK_SEQUENCE_4     4 
             3880  STORE_FAST           23  'args_pos'
             3883  STORE_FAST            3  'args_kw'
             3886  STORE_FAST           15  'annotate_args'
             3889  STORE_FAST           19  'closure'

 L. 799      3892  LOAD_FAST            23  'args_pos'
             3895  LOAD_FAST             3  'args_kw'
             3898  BINARY_ADD       
             3899  LOAD_FAST            15  'annotate_args'
             3902  BINARY_ADD       
             3903  STORE_FAST            8  'stack_count'

 L. 800      3906  LOAD_FAST            19  'closure'
             3909  JUMP_IF_FALSE        93  'to 4005'
             3912  POP_TOP          

 L. 801      3913  LOAD_FAST            23  'args_pos'
             3916  JUMP_IF_FALSE        34  'to 3953'
             3919  POP_TOP          

 L. 802      3920  LOAD_CONST               'mklambda ::= %s%s%s%s'
             3923  LOAD_CONST               'expr '
             3926  LOAD_FAST             8  'stack_count'
             3929  BINARY_MULTIPLY  
             3930  LOAD_CONST               'load_closure '
             3933  LOAD_FAST            19  'closure'
             3936  BINARY_MULTIPLY  
             3937  LOAD_CONST               'BUILD_TUPLE_1 LOAD_LAMBDA LOAD_STR '
             3940  LOAD_FAST             7  'opname'
             3943  BUILD_TUPLE_4         4 
             3946  BINARY_MODULO    
             3947  STORE_FAST           25  'rule'
             3950  JUMP_FORWARD         24  'to 3977'
           3953_0  COME_FROM          3916  '3916'
             3953  POP_TOP          

 L. 809      3954  LOAD_CONST               'mklambda ::= %s%s%s'
             3957  LOAD_CONST               'load_closure '
             3960  LOAD_FAST            19  'closure'
             3963  BINARY_MULTIPLY  
             3964  LOAD_CONST               'LOAD_LAMBDA LOAD_STR '
             3967  LOAD_FAST             7  'opname'
             3970  BUILD_TUPLE_3         3 
             3973  BINARY_MODULO    
             3974  STORE_FAST           25  'rule'
           3977_0  COME_FROM          3950  '3950'

 L. 814      3977  LOAD_FAST             0  'self'
             3980  LOAD_ATTR            36  'add_unique_rule'
             3983  LOAD_FAST            25  'rule'
             3986  LOAD_FAST             7  'opname'
             3989  LOAD_FAST            29  'token'
             3992  LOAD_ATTR            31  'attr'
             3995  LOAD_FAST             2  'customize'
             3998  CALL_FUNCTION_4       4  None
             4001  POP_TOP          
             4002  JUMP_FORWARD         46  'to 4051'
           4005_0  COME_FROM          3909  '3909'
             4005  POP_TOP          

 L. 817      4006  LOAD_CONST               'mklambda ::= %sLOAD_LAMBDA LOAD_STR %s'
             4009  LOAD_CONST               'expr '
             4012  LOAD_FAST             8  'stack_count'
             4015  BINARY_MULTIPLY  
             4016  LOAD_FAST             7  'opname'
             4019  BUILD_TUPLE_2         2 
             4022  BINARY_MODULO    
             4023  STORE_FAST           25  'rule'

 L. 821      4026  LOAD_FAST             0  'self'
             4029  LOAD_ATTR            36  'add_unique_rule'
             4032  LOAD_FAST            25  'rule'
             4035  LOAD_FAST             7  'opname'
             4038  LOAD_FAST            29  'token'
             4041  LOAD_ATTR            31  'attr'
             4044  LOAD_FAST             2  'customize'
             4047  CALL_FUNCTION_4       4  None
             4050  POP_TOP          
           4051_0  COME_FROM          4002  '4002'

 L. 823      4051  LOAD_CONST               'mkfunc ::= %s%s%s%s'
             4054  LOAD_CONST               'expr '
             4057  LOAD_FAST             8  'stack_count'
             4060  BINARY_MULTIPLY  
             4061  LOAD_CONST               'load_closure '
             4064  LOAD_FAST            19  'closure'
             4067  BINARY_MULTIPLY  
             4068  LOAD_CONST               'LOAD_CODE LOAD_STR '
             4071  LOAD_FAST             7  'opname'
             4074  BUILD_TUPLE_4         4 
             4077  BINARY_MODULO    
             4078  STORE_FAST           25  'rule'

 L. 829      4081  LOAD_FAST             0  'self'
             4084  LOAD_ATTR            36  'add_unique_rule'
             4087  LOAD_FAST            25  'rule'
             4090  LOAD_FAST             7  'opname'
             4093  LOAD_FAST            29  'token'
             4096  LOAD_ATTR            31  'attr'
             4099  LOAD_FAST             2  'customize'
             4102  CALL_FUNCTION_4       4  None
             4105  POP_TOP          

 L. 831      4106  LOAD_FAST            34  'has_get_iter_call_function1'
             4109  JUMP_IF_FALSE       222  'to 4334'
           4112_0  THEN                     4335
             4112  POP_TOP          

 L. 832      4113  LOAD_CONST               'generator_exp ::= %sload_genexpr %%s%s expr GET_ITER CALL_FUNCTION_1'
             4116  LOAD_CONST               'pos_arg '
             4119  LOAD_FAST            23  'args_pos'
             4122  BINARY_MULTIPLY  
             4123  LOAD_FAST             7  'opname'
             4126  BUILD_TUPLE_2         2 
             4129  BINARY_MODULO    
             4130  STORE_FAST           12  'rule_pat'

 L. 836      4133  LOAD_FAST             0  'self'
             4136  LOAD_ATTR            56  'add_make_function_rule'
             4139  LOAD_FAST            12  'rule_pat'
             4142  LOAD_FAST             7  'opname'
             4145  LOAD_FAST            29  'token'
             4148  LOAD_ATTR            31  'attr'
             4151  LOAD_FAST             2  'customize'
             4154  CALL_FUNCTION_4       4  None
             4157  POP_TOP          

 L. 837      4158  LOAD_CONST               'generator_exp ::= %sload_closure load_genexpr %%s%s expr GET_ITER CALL_FUNCTION_1'
             4161  LOAD_CONST               'pos_arg '
             4164  LOAD_FAST            23  'args_pos'
             4167  BINARY_MULTIPLY  
             4168  LOAD_FAST             7  'opname'
             4171  BUILD_TUPLE_2         2 
             4174  BINARY_MODULO    
             4175  STORE_FAST           12  'rule_pat'

 L. 841      4178  LOAD_FAST             0  'self'
             4181  LOAD_ATTR            56  'add_make_function_rule'
             4184  LOAD_FAST            12  'rule_pat'
             4187  LOAD_FAST             7  'opname'
             4190  LOAD_FAST            29  'token'
             4193  LOAD_ATTR            31  'attr'
             4196  LOAD_FAST             2  'customize'
             4199  CALL_FUNCTION_4       4  None
             4202  POP_TOP          

 L. 842      4203  LOAD_FAST            28  'is_pypy'
             4206  JUMP_IF_TRUE         34  'to 4243'
             4209  POP_TOP          
             4210  LOAD_FAST            20  'i'
             4213  LOAD_CONST               2
             4216  COMPARE_OP            5  >=
             4219  JUMP_IF_FALSE       108  'to 4330'
             4222  POP_TOP          
             4223  LOAD_FAST             1  'tokens'
             4226  LOAD_FAST            20  'i'
             4229  LOAD_CONST               2
             4232  BINARY_SUBTRACT  
             4233  BINARY_SUBSCR    
             4234  LOAD_CONST               'LOAD_LISTCOMP'
             4237  COMPARE_OP            2  ==
           4240_0  COME_FROM          4219  '4219'
           4240_1  COME_FROM          4206  '4206'
             4240  JUMP_IF_FALSE        87  'to 4330'
           4243_0  THEN                     4331
             4243  POP_TOP          

 L. 846      4244  LOAD_CONST               'listcomp ::= load_closure LOAD_LISTCOMP %%s%s expr GET_ITER CALL_FUNCTION_1'
             4247  LOAD_FAST             7  'opname'
             4250  BUILD_TUPLE_1         1 
             4253  BINARY_MODULO    
             4254  STORE_FAST           12  'rule_pat'

 L. 850      4257  LOAD_FAST             0  'self'
             4260  LOAD_ATTR            56  'add_make_function_rule'
             4263  LOAD_FAST            12  'rule_pat'
             4266  LOAD_FAST             7  'opname'
             4269  LOAD_FAST            29  'token'
             4272  LOAD_ATTR            31  'attr'
             4275  LOAD_FAST             2  'customize'
             4278  CALL_FUNCTION_4       4  None
             4281  POP_TOP          

 L. 853      4282  LOAD_CONST               'listcomp ::= %sLOAD_LISTCOMP %%s%s expr GET_ITER CALL_FUNCTION_1'
             4285  LOAD_CONST               'expr '
             4288  LOAD_FAST            23  'args_pos'
             4291  BINARY_MULTIPLY  
             4292  LOAD_FAST             7  'opname'
             4295  BUILD_TUPLE_2         2 
             4298  BINARY_MODULO    
             4299  STORE_FAST           12  'rule_pat'

 L. 857      4302  LOAD_FAST             0  'self'
             4305  LOAD_ATTR            56  'add_make_function_rule'
             4308  LOAD_FAST            12  'rule_pat'
             4311  LOAD_FAST             7  'opname'
             4314  LOAD_FAST            29  'token'
             4317  LOAD_ATTR            31  'attr'
             4320  LOAD_FAST             2  'customize'
             4323  CALL_FUNCTION_4       4  None
             4326  POP_TOP          
             4327  JUMP_ABSOLUTE      4335  'to 4335'
           4330_0  COME_FROM          4240  '4240'
             4330  POP_TOP          
             4331  JUMP_FORWARD          1  'to 4335'
           4334_0  COME_FROM          4109  '4109'
             4334  POP_TOP          
           4335_0  COME_FROM          4331  '4331'

 L. 861      4335  LOAD_FAST            28  'is_pypy'
             4338  JUMP_IF_TRUE         34  'to 4375'
             4341  POP_TOP          
             4342  LOAD_FAST            20  'i'
             4345  LOAD_CONST               2
             4348  COMPARE_OP            5  >=
             4351  JUMP_IF_FALSE        77  'to 4431'
             4354  POP_TOP          
             4355  LOAD_FAST             1  'tokens'
             4358  LOAD_FAST            20  'i'
             4361  LOAD_CONST               2
             4364  BINARY_SUBTRACT  
             4365  BINARY_SUBSCR    
             4366  LOAD_CONST               'LOAD_LAMBDA'
             4369  COMPARE_OP            2  ==
           4372_0  COME_FROM          4351  '4351'
           4372_1  COME_FROM          4338  '4338'
             4372  JUMP_IF_FALSE        56  'to 4431'
             4375  POP_TOP          

 L. 862      4376  LOAD_CONST               'mklambda ::= %s%sLOAD_LAMBDA %%s%s'
             4379  LOAD_CONST               'pos_arg '
             4382  LOAD_FAST            23  'args_pos'
             4385  BINARY_MULTIPLY  
             4386  LOAD_CONST               'kwarg '
             4389  LOAD_FAST             3  'args_kw'
             4392  BINARY_MULTIPLY  
             4393  LOAD_FAST             7  'opname'
             4396  BUILD_TUPLE_3         3 
             4399  BINARY_MODULO    
             4400  STORE_FAST           12  'rule_pat'

 L. 867      4403  LOAD_FAST             0  'self'
             4406  LOAD_ATTR            56  'add_make_function_rule'
             4409  LOAD_FAST            12  'rule_pat'
             4412  LOAD_FAST             7  'opname'
             4415  LOAD_FAST            29  'token'
             4418  LOAD_ATTR            31  'attr'
             4421  LOAD_FAST             2  'customize'
             4424  CALL_FUNCTION_4       4  None
             4427  POP_TOP          
             4428  JUMP_BACK           302  'to 302'
           4431_0  COME_FROM          4372  '4372'
             4431  POP_TOP          

 L. 868      4432  CONTINUE            302  'to 302'

 L. 870      4435  LOAD_FAST            29  'token'
             4438  LOAD_ATTR            31  'attr'
             4441  UNPACK_SEQUENCE_4     4 
             4444  STORE_FAST           23  'args_pos'
             4447  STORE_FAST            3  'args_kw'
             4450  STORE_FAST           15  'annotate_args'
             4453  STORE_FAST           19  'closure'

 L. 872      4456  LOAD_CONST               2
             4459  STORE_FAST           22  'j'

 L. 874      4462  LOAD_FAST            34  'has_get_iter_call_function1'
             4465  JUMP_IF_FALSE       139  'to 4607'
           4468_0  THEN                     4608
             4468  POP_TOP          

 L. 875      4469  LOAD_CONST               'generator_exp ::= %sload_genexpr %%s%s expr GET_ITER CALL_FUNCTION_1'
             4472  LOAD_CONST               'pos_arg '
             4475  LOAD_FAST            23  'args_pos'
             4478  BINARY_MULTIPLY  
             4479  LOAD_FAST             7  'opname'
             4482  BUILD_TUPLE_2         2 
             4485  BINARY_MODULO    
             4486  STORE_FAST           12  'rule_pat'

 L. 879      4489  LOAD_FAST             0  'self'
             4492  LOAD_ATTR            56  'add_make_function_rule'
             4495  LOAD_FAST            12  'rule_pat'
             4498  LOAD_FAST             7  'opname'
             4501  LOAD_FAST            29  'token'
             4504  LOAD_ATTR            31  'attr'
             4507  LOAD_FAST             2  'customize'
             4510  CALL_FUNCTION_4       4  None
             4513  POP_TOP          

 L. 881      4514  LOAD_FAST            28  'is_pypy'
             4517  JUMP_IF_TRUE         34  'to 4554'
             4520  POP_TOP          
             4521  LOAD_FAST            20  'i'
             4524  LOAD_FAST            22  'j'
             4527  COMPARE_OP            5  >=
             4530  JUMP_IF_FALSE        70  'to 4603'
             4533  POP_TOP          
             4534  LOAD_FAST             1  'tokens'
             4537  LOAD_FAST            20  'i'
             4540  LOAD_FAST            22  'j'
             4543  BINARY_SUBTRACT  
             4544  BINARY_SUBSCR    
             4545  LOAD_CONST               'LOAD_LISTCOMP'
             4548  COMPARE_OP            2  ==
           4551_0  COME_FROM          4530  '4530'
           4551_1  COME_FROM          4517  '4517'
             4551  JUMP_IF_FALSE        49  'to 4603'
           4554_0  THEN                     4604
             4554  POP_TOP          

 L. 887      4555  LOAD_CONST               'listcomp ::= %sLOAD_LISTCOMP %%s%s expr GET_ITER CALL_FUNCTION_1'
             4558  LOAD_CONST               'expr '
             4561  LOAD_FAST            23  'args_pos'
             4564  BINARY_MULTIPLY  
             4565  LOAD_FAST             7  'opname'
             4568  BUILD_TUPLE_2         2 
             4571  BINARY_MODULO    
             4572  STORE_FAST           12  'rule_pat'

 L. 891      4575  LOAD_FAST             0  'self'
             4578  LOAD_ATTR            56  'add_make_function_rule'
             4581  LOAD_FAST            12  'rule_pat'
             4584  LOAD_FAST             7  'opname'
             4587  LOAD_FAST            29  'token'
             4590  LOAD_ATTR            31  'attr'
             4593  LOAD_FAST             2  'customize'
             4596  CALL_FUNCTION_4       4  None
             4599  POP_TOP          
             4600  JUMP_ABSOLUTE      4608  'to 4608'
           4603_0  COME_FROM          4551  '4551'
             4603  POP_TOP          
             4604  JUMP_FORWARD          1  'to 4608'
           4607_0  COME_FROM          4465  '4465'
             4607  POP_TOP          
           4608_0  COME_FROM          4604  '4604'

 L. 896      4608  LOAD_FAST            28  'is_pypy'
             4611  JUMP_IF_TRUE         34  'to 4648'
             4614  POP_TOP          
             4615  LOAD_FAST            20  'i'
             4618  LOAD_FAST            22  'j'
             4621  COMPARE_OP            5  >=
             4624  JUMP_IF_FALSE        77  'to 4704'
             4627  POP_TOP          
             4628  LOAD_FAST             1  'tokens'
             4631  LOAD_FAST            20  'i'
             4634  LOAD_FAST            22  'j'
             4637  BINARY_SUBTRACT  
             4638  BINARY_SUBSCR    
             4639  LOAD_CONST               'LOAD_LAMBDA'
             4642  COMPARE_OP            2  ==
           4645_0  COME_FROM          4624  '4624'
           4645_1  COME_FROM          4611  '4611'
             4645  JUMP_IF_FALSE        56  'to 4704'
           4648_0  THEN                     4705
             4648  POP_TOP          

 L. 897      4649  LOAD_CONST               'mklambda ::= %s%sLOAD_LAMBDA %%s%s'
             4652  LOAD_CONST               'pos_arg '
             4655  LOAD_FAST            23  'args_pos'
             4658  BINARY_MULTIPLY  
             4659  LOAD_CONST               'kwarg '
             4662  LOAD_FAST             3  'args_kw'
             4665  BINARY_MULTIPLY  
             4666  LOAD_FAST             7  'opname'
             4669  BUILD_TUPLE_3         3 
             4672  BINARY_MODULO    
             4673  STORE_FAST           12  'rule_pat'

 L. 902      4676  LOAD_FAST             0  'self'
             4679  LOAD_ATTR            56  'add_make_function_rule'
             4682  LOAD_FAST            12  'rule_pat'
             4685  LOAD_FAST             7  'opname'
             4688  LOAD_FAST            29  'token'
             4691  LOAD_ATTR            31  'attr'
             4694  LOAD_FAST             2  'customize'
             4697  CALL_FUNCTION_4       4  None
             4700  POP_TOP          
             4701  JUMP_FORWARD          1  'to 4705'
           4704_0  COME_FROM          4645  '4645'
             4704  POP_TOP          
           4705_0  COME_FROM          4701  '4701'

 L. 904      4705  LOAD_FAST             3  'args_kw'
             4708  LOAD_CONST               0
             4711  COMPARE_OP            2  ==
             4714  JUMP_IF_FALSE        35  'to 4752'
             4717  POP_TOP          

 L. 905      4718  LOAD_CONST               'no_kwargs'
             4721  STORE_FAST           13  'kwargs'

 L. 906      4724  LOAD_FAST             0  'self'
             4727  LOAD_ATTR            36  'add_unique_rule'
             4730  LOAD_CONST               'no_kwargs ::='
             4733  LOAD_FAST             7  'opname'
             4736  LOAD_FAST            29  'token'
             4739  LOAD_ATTR            31  'attr'
             4742  LOAD_FAST             2  'customize'
             4745  CALL_FUNCTION_4       4  None
             4748  POP_TOP          
             4749  JUMP_FORWARD          7  'to 4759'
           4752_0  COME_FROM          4714  '4714'
             4752  POP_TOP          

 L. 908      4753  LOAD_CONST               'kwargs'
             4756  STORE_FAST           13  'kwargs'
           4759_0  COME_FROM          4749  '4749'

 L. 911      4759  LOAD_CONST               'mkfunc ::= %s%s %s%s'
             4762  LOAD_CONST               'pos_arg '
             4765  LOAD_FAST            23  'args_pos'
             4768  BINARY_MULTIPLY  
             4769  LOAD_FAST            13  'kwargs'
             4772  LOAD_CONST               'LOAD_CODE LOAD_STR '
             4775  LOAD_FAST             7  'opname'
             4778  BUILD_TUPLE_4         4 
             4781  BINARY_MODULO    
             4782  STORE_FAST           25  'rule'

 L. 917      4785  LOAD_FAST             0  'self'
             4788  LOAD_ATTR            36  'add_unique_rule'
             4791  LOAD_FAST            25  'rule'
             4794  LOAD_FAST             7  'opname'
             4797  LOAD_FAST            29  'token'
             4800  LOAD_ATTR            31  'attr'
             4803  LOAD_FAST             2  'customize'
             4806  CALL_FUNCTION_4       4  None
             4809  POP_TOP          
             4810  JUMP_BACK           302  'to 302'
           4813_0  COME_FROM          3867  '3867'
             4813  POP_TOP          

 L. 919      4814  LOAD_FAST             7  'opname'
             4817  LOAD_CONST               'MAKE_FUNCTION_8'
             4820  COMPARE_OP            2  ==
             4823  JUMP_IF_FALSE        88  'to 4914'
             4826  POP_TOP          

 L. 920      4827  LOAD_CONST               'LOAD_DICTCOMP'
             4830  LOAD_FAST             0  'self'
             4833  LOAD_ATTR            11  'seen_ops'
             4836  COMPARE_OP            6  in
             4839  JUMP_IF_FALSE        26  'to 4868'
             4842  POP_TOP          

 L. 922      4843  LOAD_CONST               '\n                       dict_comp ::= load_closure LOAD_DICTCOMP LOAD_STR\n                                     MAKE_FUNCTION_8 expr\n                                     GET_ITER CALL_FUNCTION_1\n                       '
             4846  STORE_FAST           25  'rule'

 L. 927      4849  LOAD_FAST             0  'self'
             4852  LOAD_ATTR            17  'addRule'
             4855  LOAD_FAST            25  'rule'
             4858  LOAD_GLOBAL          18  'nop_func'
             4861  CALL_FUNCTION_2       2  None
             4864  POP_TOP          
             4865  JUMP_ABSOLUTE      5419  'to 5419'
           4868_0  COME_FROM          4839  '4839'
             4868  POP_TOP          

 L. 928      4869  LOAD_CONST               'LOAD_SETCOMP'
             4872  LOAD_FAST             0  'self'
             4875  LOAD_ATTR            11  'seen_ops'
             4878  COMPARE_OP            6  in
             4881  JUMP_IF_FALSE        26  'to 4910'
             4884  POP_TOP          

 L. 929      4885  LOAD_CONST               '\n                       set_comp ::= load_closure LOAD_SETCOMP LOAD_STR\n                                    MAKE_FUNCTION_8 expr\n                                    GET_ITER CALL_FUNCTION_1\n                       '
             4888  STORE_FAST           25  'rule'

 L. 934      4891  LOAD_FAST             0  'self'
             4894  LOAD_ATTR            17  'addRule'
             4897  LOAD_FAST            25  'rule'
             4900  LOAD_GLOBAL          18  'nop_func'
             4903  CALL_FUNCTION_2       2  None
             4906  POP_TOP          
             4907  JUMP_ABSOLUTE      5419  'to 5419'
           4910_0  COME_FROM          4881  '4881'
             4910  POP_TOP          
             4911  JUMP_BACK           302  'to 302'
           4914_0  COME_FROM          4823  '4823'
             4914  POP_TOP          

 L. 936      4915  LOAD_FAST             7  'opname'
             4918  LOAD_CONST               'RETURN_VALUE_LAMBDA'
             4921  COMPARE_OP            2  ==
             4924  JUMP_IF_FALSE        33  'to 4960'
             4927  POP_TOP          

 L. 937      4928  LOAD_FAST             0  'self'
             4931  LOAD_ATTR            17  'addRule'
             4934  LOAD_CONST               '\n                    return_lambda ::= ret_expr RETURN_VALUE_LAMBDA\n                    '

 L. 941      4937  LOAD_GLOBAL          18  'nop_func'
             4940  CALL_FUNCTION_2       2  None
             4943  POP_TOP          

 L. 943      4944  LOAD_FAST            11  'custom_ops_processed'
             4947  LOAD_ATTR            53  'add'
             4950  LOAD_FAST             7  'opname'
             4953  CALL_FUNCTION_1       1  None
             4956  POP_TOP          
             4957  JUMP_BACK           302  'to 302'
           4960_0  COME_FROM          4924  '4924'
             4960  POP_TOP          

 L. 944      4961  LOAD_FAST             7  'opname'
             4964  LOAD_CONST               'RAISE_VARARGS_0'
             4967  COMPARE_OP            2  ==
             4970  JUMP_IF_FALSE        33  'to 5006'
             4973  POP_TOP          

 L. 945      4974  LOAD_FAST             0  'self'
             4977  LOAD_ATTR            17  'addRule'
             4980  LOAD_CONST               '\n                    stmt        ::= raise_stmt0\n                    raise_stmt0 ::= RAISE_VARARGS_0\n                    '

 L. 950      4983  LOAD_GLOBAL          18  'nop_func'
             4986  CALL_FUNCTION_2       2  None
             4989  POP_TOP          

 L. 952      4990  LOAD_FAST            11  'custom_ops_processed'
             4993  LOAD_ATTR            53  'add'
             4996  LOAD_FAST             7  'opname'
             4999  CALL_FUNCTION_1       1  None
             5002  POP_TOP          
             5003  JUMP_BACK           302  'to 302'
           5006_0  COME_FROM          4970  '4970'
             5006  POP_TOP          

 L. 953      5007  LOAD_FAST             7  'opname'
             5010  LOAD_CONST               'RAISE_VARARGS_1'
             5013  COMPARE_OP            2  ==
             5016  JUMP_IF_FALSE        33  'to 5052'
             5019  POP_TOP          

 L. 954      5020  LOAD_FAST             0  'self'
             5023  LOAD_ATTR            17  'addRule'
             5026  LOAD_CONST               '\n                    stmt        ::= raise_stmt1\n                    raise_stmt1 ::= expr RAISE_VARARGS_1\n                    '

 L. 959      5029  LOAD_GLOBAL          18  'nop_func'
             5032  CALL_FUNCTION_2       2  None
             5035  POP_TOP          

 L. 961      5036  LOAD_FAST            11  'custom_ops_processed'
             5039  LOAD_ATTR            53  'add'
             5042  LOAD_FAST             7  'opname'
             5045  CALL_FUNCTION_1       1  None
             5048  POP_TOP          
             5049  JUMP_BACK           302  'to 302'
           5052_0  COME_FROM          5016  '5016'
             5052  POP_TOP          

 L. 962      5053  LOAD_FAST             7  'opname'
             5056  LOAD_CONST               'RAISE_VARARGS_2'
             5059  COMPARE_OP            2  ==
             5062  JUMP_IF_FALSE        33  'to 5098'
             5065  POP_TOP          

 L. 963      5066  LOAD_FAST             0  'self'
             5069  LOAD_ATTR            17  'addRule'
             5072  LOAD_CONST               '\n                    stmt        ::= raise_stmt2\n                    raise_stmt2 ::= expr expr RAISE_VARARGS_2\n                    '

 L. 968      5075  LOAD_GLOBAL          18  'nop_func'
             5078  CALL_FUNCTION_2       2  None
             5081  POP_TOP          

 L. 970      5082  LOAD_FAST            11  'custom_ops_processed'
             5085  LOAD_ATTR            53  'add'
             5088  LOAD_FAST             7  'opname'
             5091  CALL_FUNCTION_1       1  None
             5094  POP_TOP          
             5095  JUMP_BACK           302  'to 302'
           5098_0  COME_FROM          5062  '5062'
             5098  POP_TOP          

 L. 972      5099  LOAD_FAST             7  'opname'
             5102  LOAD_CONST               'SETUP_EXCEPT'
             5105  COMPARE_OP            2  ==
             5108  JUMP_IF_FALSE        33  'to 5144'
             5111  POP_TOP          

 L. 973      5112  LOAD_FAST             0  'self'
             5115  LOAD_ATTR            17  'addRule'
             5118  LOAD_CONST               '\n                    try_except     ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK\n                                       except_handler opt_come_from_except\n\n                    tryelsestmt    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK\n                                       except_handler else_suite come_from_except_clauses\n\n                    tryelsestmt    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK\n                                       except_handler else_suite come_froms\n\n                    tryelsestmtl   ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK\n                                       except_handler else_suitel come_from_except_clauses\n\n                    stmt             ::= tryelsestmtl3\n                    tryelsestmtl3    ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK\n                                         except_handler COME_FROM else_suitel\n                                         opt_come_from_except\n                    '

 L. 992      5121  LOAD_GLOBAL          18  'nop_func'
             5124  CALL_FUNCTION_2       2  None
             5127  POP_TOP          

 L. 994      5128  LOAD_FAST            11  'custom_ops_processed'
             5131  LOAD_ATTR            53  'add'
             5134  LOAD_FAST             7  'opname'
             5137  CALL_FUNCTION_1       1  None
             5140  POP_TOP          
             5141  JUMP_BACK           302  'to 302'
           5144_0  COME_FROM          5108  '5108'
             5144  POP_TOP          

 L. 996      5145  LOAD_FAST             7  'opname'
             5148  LOAD_CONST               'SETUP_WITH'
             5151  COMPARE_OP            2  ==
             5154  JUMP_IF_FALSE        66  'to 5223'
             5157  POP_TOP          

 L. 997      5158  LOAD_CONST               '\n                  stmt       ::= with\n                  stmt       ::= withasstmt\n\n                  with       ::= expr SETUP_WITH POP_TOP suite_stmts_opt COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                  withasstmt ::= expr SETUP_WITH store suite_stmts_opt COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n\n                  with       ::= expr\n                                 SETUP_WITH POP_TOP suite_stmts_opt\n                                 POP_BLOCK LOAD_CONST COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                  withasstmt ::= expr\n                                 SETUP_WITH store suite_stmts_opt\n                                 POP_BLOCK LOAD_CONST COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n\n                  with       ::= expr\n                                 SETUP_WITH POP_TOP suite_stmts_opt\n                                 POP_BLOCK LOAD_CONST COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                  withasstmt ::= expr\n                                 SETUP_WITH store suite_stmts_opt\n                                 POP_BLOCK LOAD_CONST COME_FROM_WITH\n                                 WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                '
             5161  STORE_FAST            6  'rules_str'

 L.1024      5164  LOAD_FAST             0  'self'
             5167  LOAD_ATTR            30  'version'
             5170  LOAD_CONST               3.8
             5173  COMPARE_OP            0  <
             5176  JUMP_IF_FALSE        14  'to 5193'
             5179  POP_TOP          

 L.1025      5180  LOAD_FAST             6  'rules_str'
             5183  LOAD_CONST               '\n                    with     ::= expr SETUP_WITH POP_TOP suite_stmts_opt POP_BLOCK\n                                   LOAD_CONST\n                                   WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n                    '
             5186  INPLACE_ADD      
             5187  STORE_FAST            6  'rules_str'
             5190  JUMP_FORWARD         11  'to 5204'
           5193_0  COME_FROM          5176  '5176'
             5193  POP_TOP          

 L.1031      5194  LOAD_FAST             6  'rules_str'
             5197  LOAD_CONST               '\n                      with    ::= expr\n                                     SETUP_WITH POP_TOP suite_stmts_opt\n                                     POP_BLOCK LOAD_CONST COME_FROM_WITH\n                                     WITH_CLEANUP_START WITH_CLEANUP_FINISH END_FINALLY\n\n                      withasstmt ::= expr\n                                     SETUP_WITH store suite_stmts_opt\n                                     POP_BLOCK LOAD_CONST COME_FROM_WITH\n\n                       with    ::= expr SETUP_WITH POP_TOP suite_stmts_opt POP_BLOCK\n                                     BEGIN_FINALLY COME_FROM_WITH\n                                     WITH_CLEANUP_START WITH_CLEANUP_FINISH\n                                     END_FINALLY\n                    '
             5200  INPLACE_ADD      
             5201  STORE_FAST            6  'rules_str'
           5204_0  COME_FROM          5190  '5190'

 L.1046      5204  LOAD_FAST             0  'self'
             5207  LOAD_ATTR            17  'addRule'
             5210  LOAD_FAST             6  'rules_str'
             5213  LOAD_GLOBAL          18  'nop_func'
             5216  CALL_FUNCTION_2       2  None
             5219  POP_TOP          
             5220  JUMP_BACK           302  'to 302'
           5223_0  COME_FROM          5154  '5154'
             5223  POP_TOP          

 L.1048      5224  LOAD_FAST             5  'opname_base'
             5227  LOAD_CONST               ('UNPACK_EX',)
             5230  COMPARE_OP            6  in
             5233  JUMP_IF_FALSE        61  'to 5297'
             5236  POP_TOP          

 L.1049      5237  LOAD_FAST            29  'token'
             5240  LOAD_ATTR            31  'attr'
             5243  UNPACK_SEQUENCE_2     2 
             5246  STORE_FAST           24  'before_count'
             5249  STORE_FAST           33  'after_count'

 L.1050      5252  LOAD_CONST               'unpack ::= '
             5255  LOAD_FAST             7  'opname'
             5258  BINARY_ADD       
             5259  LOAD_CONST               ' store'
             5262  LOAD_FAST            24  'before_count'
             5265  LOAD_FAST            33  'after_count'
             5268  BINARY_ADD       
             5269  LOAD_CONST               1
             5272  BINARY_ADD       
             5273  BINARY_MULTIPLY  
             5274  BINARY_ADD       
             5275  STORE_FAST           25  'rule'

 L.1053      5278  LOAD_FAST             0  'self'
             5281  LOAD_ATTR            17  'addRule'
             5284  LOAD_FAST            25  'rule'
             5287  LOAD_GLOBAL          18  'nop_func'
             5290  CALL_FUNCTION_2       2  None
             5293  POP_TOP          
             5294  JUMP_BACK           302  'to 302'
           5297_0  COME_FROM          5233  '5233'
             5297  POP_TOP          

 L.1055      5298  LOAD_FAST             5  'opname_base'
             5301  LOAD_CONST               ('UNPACK_TUPLE', 'UNPACK_SEQUENCE')
             5304  COMPARE_OP            6  in
             5307  JUMP_IF_FALSE        41  'to 5351'
             5310  POP_TOP          

 L.1056      5311  LOAD_CONST               'unpack ::= '
             5314  LOAD_FAST             7  'opname'
             5317  BINARY_ADD       
             5318  LOAD_CONST               ' store'
             5321  LOAD_FAST            29  'token'
             5324  LOAD_ATTR            31  'attr'
             5327  BINARY_MULTIPLY  
             5328  BINARY_ADD       
             5329  STORE_FAST           25  'rule'

 L.1057      5332  LOAD_FAST             0  'self'
             5335  LOAD_ATTR            17  'addRule'
             5338  LOAD_FAST            25  'rule'
             5341  LOAD_GLOBAL          18  'nop_func'
             5344  CALL_FUNCTION_2       2  None
             5347  POP_TOP          
             5348  JUMP_BACK           302  'to 302'
           5351_0  COME_FROM          5307  '5307'
             5351  POP_TOP          

 L.1059      5352  LOAD_FAST             5  'opname_base'
             5355  LOAD_CONST               'UNPACK_LIST'
             5358  COMPARE_OP            2  ==
             5361  JUMP_IF_FALSE        54  'to 5418'
             5364  POP_TOP          

 L.1060      5365  LOAD_CONST               'unpack_list ::= '
             5368  LOAD_FAST             7  'opname'
             5371  BINARY_ADD       
             5372  LOAD_CONST               ' store'
             5375  LOAD_FAST            29  'token'
             5378  LOAD_ATTR            31  'attr'
             5381  BINARY_MULTIPLY  
             5382  BINARY_ADD       
             5383  STORE_FAST           25  'rule'

 L.1061      5386  LOAD_FAST             0  'self'
             5389  LOAD_ATTR            17  'addRule'
             5392  LOAD_FAST            25  'rule'
             5395  LOAD_GLOBAL          18  'nop_func'
             5398  CALL_FUNCTION_2       2  None
             5401  POP_TOP          

 L.1062      5402  LOAD_FAST            11  'custom_ops_processed'
             5405  LOAD_ATTR            53  'add'
             5408  LOAD_FAST             7  'opname'
             5411  CALL_FUNCTION_1       1  None
             5414  POP_TOP          

 L.1063      5415  JUMP_BACK           302  'to 302'
           5418_0  COME_FROM          5361  '5361'
             5418  POP_TOP          

 L.1065      5419  JUMP_BACK           302  'to 302'
             5422  POP_BLOCK        
           5423_0  COME_FROM           289  '289'

 L.1067      5423  BUILD_MAP             0 
             5426  DUP_TOP          
             5427  LOAD_CONST               '_ifstmts_jump'
             5430  LOAD_GLOBAL          64  'ifstmts_jump'
             5433  ROT_THREE        
             5434  STORE_SUBSCR     
             5435  DUP_TOP          
             5436  LOAD_CONST               'and'
             5439  LOAD_GLOBAL          65  'and_check'
             5442  ROT_THREE        
             5443  STORE_SUBSCR     
             5444  DUP_TOP          
             5445  LOAD_CONST               'ifelsestmt'
             5448  LOAD_GLOBAL          66  'ifelsestmt'
             5451  ROT_THREE        
             5452  STORE_SUBSCR     
             5453  DUP_TOP          
             5454  LOAD_CONST               'ifelsestmtl'
             5457  LOAD_GLOBAL          66  'ifelsestmt'
             5460  ROT_THREE        
             5461  STORE_SUBSCR     
             5462  DUP_TOP          
             5463  LOAD_CONST               'iflaststmt'
             5466  LOAD_GLOBAL          67  'iflaststmt'
             5469  ROT_THREE        
             5470  STORE_SUBSCR     
             5471  DUP_TOP          
             5472  LOAD_CONST               'iflaststmtl'
             5475  LOAD_GLOBAL          67  'iflaststmt'
             5478  ROT_THREE        
             5479  STORE_SUBSCR     
             5480  DUP_TOP          
             5481  LOAD_CONST               'ifstmt'
             5484  LOAD_GLOBAL          68  'ifstmt'
             5487  ROT_THREE        
             5488  STORE_SUBSCR     
             5489  DUP_TOP          
             5490  LOAD_CONST               'ifstmtl'
             5493  LOAD_GLOBAL          68  'ifstmt'
             5496  ROT_THREE        
             5497  STORE_SUBSCR     
             5498  DUP_TOP          
             5499  LOAD_CONST               'or'
             5502  LOAD_GLOBAL          69  'or_check'
             5505  ROT_THREE        
             5506  STORE_SUBSCR     
             5507  DUP_TOP          
             5508  LOAD_CONST               'testtrue'
             5511  LOAD_GLOBAL          70  'testtrue'
             5514  ROT_THREE        
             5515  STORE_SUBSCR     
             5516  DUP_TOP          
             5517  LOAD_CONST               'testfalsel'
             5520  LOAD_GLOBAL          70  'testtrue'
             5523  ROT_THREE        
             5524  STORE_SUBSCR     
             5525  DUP_TOP          
             5526  LOAD_CONST               'while1elsestmt'
             5529  LOAD_GLOBAL          71  'while1elsestmt'
             5532  ROT_THREE        
             5533  STORE_SUBSCR     
             5534  DUP_TOP          
             5535  LOAD_CONST               'while1stmt'
             5538  LOAD_GLOBAL          72  'while1stmt'
             5541  ROT_THREE        
             5542  STORE_SUBSCR     
             5543  DUP_TOP          
             5544  LOAD_CONST               'try_elsestmtl38'
             5547  LOAD_GLOBAL          73  'tryelsestmtl3'
             5550  ROT_THREE        
             5551  STORE_SUBSCR     
             5552  LOAD_FAST             0  'self'
             5555  STORE_ATTR           74  'reduce_check_table'

 L.1084      5558  LOAD_CONST               'AST'
             5561  LOAD_FAST             0  'self'
             5564  LOAD_ATTR            75  'check_reduce'
             5567  LOAD_CONST               'and'
             5570  STORE_SUBSCR     

 L.1085      5571  LOAD_CONST               'noAST'
             5574  LOAD_FAST             0  'self'
             5577  LOAD_ATTR            75  'check_reduce'
             5580  LOAD_CONST               'annotate_tuple'
             5583  STORE_SUBSCR     

 L.1086      5584  LOAD_CONST               'AST'
             5587  LOAD_FAST             0  'self'
             5590  LOAD_ATTR            75  'check_reduce'
             5593  LOAD_CONST               'aug_assign1'
             5596  STORE_SUBSCR     

 L.1087      5597  LOAD_CONST               'AST'
             5600  LOAD_FAST             0  'self'
             5603  LOAD_ATTR            75  'check_reduce'
             5606  LOAD_CONST               'aug_assign2'
             5609  STORE_SUBSCR     

 L.1088      5610  LOAD_CONST               'noAST'
             5613  LOAD_FAST             0  'self'
             5616  LOAD_ATTR            75  'check_reduce'
             5619  LOAD_CONST               'while1stmt'
             5622  STORE_SUBSCR     

 L.1089      5623  LOAD_CONST               'noAST'
             5626  LOAD_FAST             0  'self'
             5629  LOAD_ATTR            75  'check_reduce'
             5632  LOAD_CONST               'while1elsestmt'
             5635  STORE_SUBSCR     

 L.1090      5636  LOAD_CONST               'AST'
             5639  LOAD_FAST             0  'self'
             5642  LOAD_ATTR            75  'check_reduce'
             5645  LOAD_CONST               '_ifstmts_jump'
             5648  STORE_SUBSCR     

 L.1091      5649  LOAD_CONST               'AST'
             5652  LOAD_FAST             0  'self'
             5655  LOAD_ATTR            75  'check_reduce'
             5658  LOAD_CONST               'ifelsestmt'
             5661  STORE_SUBSCR     

 L.1092      5662  LOAD_CONST               'AST'
             5665  LOAD_FAST             0  'self'
             5668  LOAD_ATTR            75  'check_reduce'
             5671  LOAD_CONST               'ifelsestmtl'
             5674  STORE_SUBSCR     

 L.1093      5675  LOAD_CONST               'AST'
             5678  LOAD_FAST             0  'self'
             5681  LOAD_ATTR            75  'check_reduce'
             5684  LOAD_CONST               'iflaststmt'
             5687  STORE_SUBSCR     

 L.1094      5688  LOAD_CONST               'AST'
             5691  LOAD_FAST             0  'self'
             5694  LOAD_ATTR            75  'check_reduce'
             5697  LOAD_CONST               'iflaststmtl'
             5700  STORE_SUBSCR     

 L.1095      5701  LOAD_CONST               'AST'
             5704  LOAD_FAST             0  'self'
             5707  LOAD_ATTR            75  'check_reduce'
             5710  LOAD_CONST               'ifstmt'
             5713  STORE_SUBSCR     

 L.1096      5714  LOAD_CONST               'AST'
             5717  LOAD_FAST             0  'self'
             5720  LOAD_ATTR            75  'check_reduce'
             5723  LOAD_CONST               'ifstmtl'
             5726  STORE_SUBSCR     

 L.1097      5727  LOAD_CONST               'AST'
             5730  LOAD_FAST             0  'self'
             5733  LOAD_ATTR            75  'check_reduce'
             5736  LOAD_CONST               'import_from37'
             5739  STORE_SUBSCR     

 L.1098      5740  LOAD_CONST               'AST'
             5743  LOAD_FAST             0  'self'
             5746  LOAD_ATTR            75  'check_reduce'
             5749  LOAD_CONST               'or'
             5752  STORE_SUBSCR     

 L.1099      5753  LOAD_CONST               'tokens'
             5756  LOAD_FAST             0  'self'
             5759  LOAD_ATTR            75  'check_reduce'
             5762  LOAD_CONST               'testtrue'
             5765  STORE_SUBSCR     

 L.1100      5766  LOAD_CONST               'tokens'
             5769  LOAD_FAST             0  'self'
             5772  LOAD_ATTR            75  'check_reduce'
             5775  LOAD_CONST               'testfalsel'
             5778  STORE_SUBSCR     

Parse error at or near `COME_FROM' instruction at offset 4813_0

    def custom_classfunc_rule(self, opname, token, customize, next_token):
        """
        call ::= expr {expr}^n CALL_FUNCTION_n
        call ::= expr {expr}^n CALL_FUNCTION_VAR_n
        call ::= expr {expr}^n CALL_FUNCTION_VAR_KW_n
        call ::= expr {expr}^n CALL_FUNCTION_KW_n

        classdefdeco2 ::= LOAD_BUILD_CLASS mkfunc {expr}^n-1 CALL_FUNCTION_n
        """
        (args_pos, args_kw) = self.get_pos_kw(token)
        nak = (len(opname) - len('CALL_FUNCTION')) // 3
        uniq_param = args_kw + args_pos
        if frozenset(('GET_AWAITABLE', 'YIELD_FROM')).issubset(self.seen_ops):
            rule = 'async_call ::= expr ' + 'pos_arg ' * args_pos + 'kwarg ' * args_kw + 'expr ' * nak + token.kind + ' GET_AWAITABLE LOAD_CONST YIELD_FROM'
            self.add_unique_rule(rule, token.kind, uniq_param, customize)
            self.add_unique_rule('expr ::= async_call', token.kind, uniq_param, customize)
        if opname.startswith('CALL_FUNCTION_VAR'):
            token.kind = self.call_fn_name(token)
            if opname.endswith('KW'):
                kw = 'expr '
            else:
                kw = ''
            rule = 'call ::= expr expr ' + 'pos_arg ' * args_pos + 'kwarg ' * args_kw + kw + token.kind
            self.add_unique_rule(rule, token.kind, args_pos, customize)
        else:
            token.kind = self.call_fn_name(token)
            uniq_param = args_kw + args_pos
            rule = 'call ::= expr ' + 'pos_arg ' * args_pos + 'kwarg ' * args_kw + 'expr ' * nak + token.kind
            self.add_unique_rule(rule, token.kind, uniq_param, customize)
            if 'LOAD_BUILD_CLASS' in self.seen_ops:
                if next_token == 'CALL_FUNCTION' and next_token.attr == 1 and args_pos > 1:
                    rule = 'classdefdeco2 ::= LOAD_BUILD_CLASS mkfunc %s%s_%d' % ('expr ' * (args_pos - 1), opname, args_pos)
                    self.add_unique_rule(rule, token.kind, uniq_param, customize)

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        lhs = rule[0]
        n = len(tokens)
        last = min(last, n - 1)
        fn = self.reduce_check_table.get(lhs, None)
        try:
            if fn:
                return fn(self, lhs, n, rule, ast, tokens, first, last)
        except:
            import sys, traceback
            print 'Exception in %s %s\n' + 'rule: %s\n' + 'offsets %s .. %s' % (fn.__name__, sys.exc_info()[1], rule, tokens[first].offset, tokens[last].offset)
            print traceback.print_tb(sys.exc_info()[2], -1)
            raise ParserError(tokens[last], tokens[last].off2int(), self.debug['rules'])

        if lhs in ('aug_assign1', 'aug_assign2') and ast[0][0] == 'and':
            return True
        elif lhs == 'annotate_tuple':
            return not isinstance(tokens[first].attr, tuple)
        elif lhs == 'import_from37':
            importlist37 = ast[3]
            alias37 = importlist37[0]
            if importlist37 == 'importlist37':
                if alias37 == 'alias37':
                    store = alias37[1]
                else:
                    raise store == 'store' or AssertionError
                return alias37[0].attr != store[0].attr
            return False
        return False
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\FormulaEvaluator.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 78845 bytes
__doc__ = '\nCreated on Jan 9, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
from arelle import XPathContext, XbrlConst, XmlUtil, XbrlUtil, XmlValidate
from arelle.FunctionXs import xsString
from arelle.ModelObject import ModelObject
from arelle.ModelFormulaObject import aspectModels, Aspect, aspectModelAspect, ModelFormula, ModelTuple, ModelExistenceAssertion, ModelValueAssertion, ModelFactVariable, ModelGeneralVariable, ModelVariable, ModelParameter, ModelFilter, ModelAspectCover, ModelBooleanFilter, ModelTypedDimension
from arelle.PrototypeInstanceObject import DimValuePrototype
from arelle.PythonUtil import OrderedSet
from arelle.ModelValue import QName
import datetime, time, logging, re
from decimal import Decimal
from math import log10, isnan, isinf, fabs
from arelle.Locale import format_string
from collections import defaultdict
ModelDimensionValue = None
ModelFact = None
expressionVariablesPattern = re.compile('([^$]*)([$]\\w[\\w:.-]*)([^$]*)')
EMPTYSET = set()

def init():
    global ModelDimensionValue
    global ModelFact
    if ModelDimensionValue is None:
        from arelle.ModelInstanceObject import ModelDimensionValue, ModelFact


def evaluate(xpCtx, varSet, variablesInScope=False, uncoveredAspectFacts=None):
    if variablesInScope:
        stackedEvaluations = (
         xpCtx.evaluations, xpCtx.evaluationHashDicts)
    else:
        xpCtx.varBindings = {}
        uncoveredAspectFacts = {}
    xpCtx.evaluations = []
    xpCtx.evaluationHashDicts = {}
    try:
        xpCtx.variableSet = varSet
        if isinstance(varSet, ModelExistenceAssertion):
            varSet.evaluationsCount = 0
        if xpCtx.formulaOptions.timeVariableSetEvaluation:
            varSet.timeEvaluationStarted = timeEvaluationsStarted = time.time()
        varSet.evaluationNumber = 0
        initialTraceCount = xpCtx.modelXbrl.logCount.get(logging.getLevelName('INFO'), 0)
        evaluateVar(xpCtx, varSet, 0, {}, uncoveredAspectFacts)
        if isinstance(varSet, ModelExistenceAssertion):
            prog = varSet.testProg
            if prog:
                assertionParamQnames = []
                for varRel in varSet.orderedVariableRelationships:
                    varQname = varRel.variableQname
                    var = varRel.toModelObject
                    if isinstance(var, ModelParameter) and varQname not in xpCtx.inScopeVars:
                        assertionParamQnames.append(varQname)
                        xpCtx.inScopeVars[varQname] = xpCtx.inScopeVars.get(var.parameterQname)

                result = xpCtx.evaluateBooleanValue(prog, contextItem=(varSet.evaluationsCount))
                for varQname in assertionParamQnames:
                    xpCtx.inScopeVars.pop(varQname)

            else:
                result = varSet.evaluationsCount > 0
            if result:
                varSet.countSatisfied += 1
            else:
                varSet.countNotSatisfied += 1
            if xpCtx.formulaOptions.traceSatisfiedAssertions and result or (xpCtx.formulaOptions.traceUnsatisfiedAssertions or xpCtx.formulaOptions.errorUnsatisfiedAssertions) and not result:
                xpCtx.modelXbrl.log('ERROR' if (xpCtx.formulaOptions.errorUnsatisfiedAssertions and not result) else 'INFO',
                  ('formula:assertionSatisfied' if result else 'formula:assertionUnsatisfied'),
                  (_('%(label)s')),
                  modelObject=varSet,
                  label=(varSet.logLabel()),
                  messageCodes=('formula:assertionSatisfied', 'formula:assertionUnsatisfied'))
            if xpCtx.formulaOptions.traceVariableSetExpressionResult:
                xpCtx.modelXbrl.info('formula:trace', (_('Existence Assertion %(xlinkLabel)s \nResult: %(result)s')),
                  modelObject=varSet,
                  xlinkLabel=(varSet.xlinkLabel),
                  result=result)
            msg = varSet.message(result)
            if msg is not None:
                xpCtx.inScopeVars[XbrlConst.qnEaTestExpression] = varSet.test
                xpCtx.modelXbrl.info(('message:' + (varSet.id or varSet.xlinkLabel or _('unlabeled variableSet'))), (msg.evaluate(xpCtx)),
                  modelObject=varSet,
                  messageCodes=('message:{variableSetID|xlinkLabel}', ))
                xpCtx.inScopeVars.pop(XbrlConst.qnEaTestExpression)
        if xpCtx.formulaOptions.traceVariableSetExpressionResult:
            if initialTraceCount == xpCtx.modelXbrl.logCount.get(logging._checkLevel('INFO'), 0):
                xpCtx.modelXbrl.info('formula:trace', (_('Variable set %(xlinkLabel)s had no xpCtx.evaluations')),
                  modelObject=varSet,
                  xlinkLabel=(varSet.xlinkLabel))
        if xpCtx.formulaOptions.timeVariableSetEvaluation:
            xpCtx.modelXbrl.info('formula:time', (_('Variable set %(xlinkLabel)s time for %(count)s evaluations: %(time)s')),
              modelObject=varSet,
              xlinkLabel=(varSet.xlinkLabel),
              count=(varSet.evaluationNumber),
              time=(format_string(xpCtx.modelXbrl.modelManager.locale, '%.3f', time.time() - timeEvaluationsStarted)))
        xpCtx.variableSet = None
    except XPathContext.XPathException as err:
        xpCtx.modelXbrl.error((err.code), (_('Variable set %(label)s \nException: %(error)s')),
          modelObject=varSet,
          label=(varSet.logLabel()),
          error=(err.message))
        xpCtx.variableSet = None

    if xpCtx.formulaOptions.traceVariableSetExpressionResult:
        xpCtx.modelXbrl.info('formula:trace', (_('Variable set %(xlinkLabel)s evaluations: %(evaluations)s x %(variables)s')),
          modelObject=varSet,
          xlinkLabel=(varSet.xlinkLabel),
          evaluations=(len(xpCtx.evaluations)),
          variables=(max(len(e) for e in xpCtx.evaluations) if xpCtx.evaluations else 0))
    else:
        del xpCtx.evaluations[:]
        xpCtx.evaluationHashDicts.clear()
        if variablesInScope:
            xpCtx.evaluations, xpCtx.evaluationHashDicts = stackedEvaluations
        else:
            for vb in xpCtx.varBindings.values():
                vb.close()

            xpCtx.varBindings.clear()
            uncoveredAspectFacts.clear()


def evaluateVar--- This code section failed: ---

 L. 123         0  LOAD_FAST                'varIndex'
                2  LOAD_GLOBAL              len
                4  LOAD_DEREF               'varSet'
                6  LOAD_ATTR                orderedVariableRelationships
                8  CALL_FUNCTION_1       1  ''
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE  1884  'to 1884'

 L. 125        16  LOAD_CONST               False
               18  STORE_FAST               'anyFactVar'

 L. 125        20  LOAD_CONST               False
               22  STORE_FAST               'anyBoundFactVar'

 L. 126        24  SETUP_LOOP           64  'to 64'
               26  LOAD_DEREF               'xpCtx'
               28  LOAD_ATTR                varBindings
               30  LOAD_ATTR                values
               32  CALL_FUNCTION_0       0  ''
               34  GET_ITER         
               36  FOR_ITER             62  'to 62'
               38  STORE_FAST               'vb'

 L. 127        40  LOAD_FAST                'vb'
               42  LOAD_ATTR                isFactVar
               44  POP_JUMP_IF_FALSE    36  'to 36'

 L. 128        46  LOAD_CONST               True
               48  STORE_FAST               'anyFactVar'

 L. 129        50  LOAD_FAST                'vb'
               52  LOAD_ATTR                isFallback
               54  POP_JUMP_IF_TRUE     36  'to 36'

 L. 129        56  LOAD_CONST               True
               58  STORE_FAST               'anyBoundFactVar'
               60  JUMP_BACK            36  'to 36'
               62  POP_BLOCK        
             64_0  COME_FROM_LOOP       24  '24'

 L. 130        64  LOAD_DEREF               'xpCtx'
               66  LOAD_ATTR                varBindings
               68  POP_JUMP_IF_FALSE   118  'to 118'
               70  LOAD_FAST                'anyFactVar'
               72  POP_JUMP_IF_FALSE   118  'to 118'
               74  LOAD_FAST                'anyBoundFactVar'
               76  UNARY_NOT        
               78  POP_JUMP_IF_FALSE   118  'to 118'

 L. 131        80  LOAD_DEREF               'xpCtx'
               82  LOAD_ATTR                formulaOptions
               84  LOAD_ATTR                traceVariableSetExpressionResult
               86  POP_JUMP_IF_FALSE   114  'to 114'

 L. 132        88  LOAD_DEREF               'xpCtx'
               90  LOAD_ATTR                modelXbrl
               92  LOAD_ATTR                info
               94  LOAD_STR                 'formula:trace'

 L. 133        96  LOAD_GLOBAL              _
               98  LOAD_STR                 'Variable set %(xlinkLabel)s skipped evaluation, all fact variables have fallen back'
              100  CALL_FUNCTION_1       1  ''

 L. 134       102  LOAD_DEREF               'varSet'
              104  LOAD_DEREF               'varSet'
              106  LOAD_ATTR                xlinkLabel
              108  LOAD_CONST               ('modelObject', 'xlinkLabel')
              110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              112  POP_TOP          
            114_0  COME_FROM            86  '86'

 L. 135       114  LOAD_CONST               None
              116  RETURN_END_IF    
            118_0  COME_FROM            78  '78'
            118_1  COME_FROM            72  '72'
            118_2  COME_FROM            68  '68'

 L. 137       118  LOAD_GLOBAL              set
              120  LOAD_GENEXPR             '<code_object <genexpr>>'
              122  LOAD_STR                 'evaluateVar.<locals>.<genexpr>'
              124  MAKE_FUNCTION_0          ''
              126  LOAD_DEREF               'xpCtx'
              128  LOAD_ATTR                varBindings
              130  LOAD_ATTR                values
              132  CALL_FUNCTION_0       0  ''
              134  GET_ITER         
              136  CALL_FUNCTION_1       1  ''
              138  CALL_FUNCTION_1       1  ''
              140  STORE_DEREF              'fbVars'

 L. 140       142  LOAD_GLOBAL              dict
              144  LOAD_CLOSURE             'fbVars'
              146  BUILD_TUPLE_1         1 
              148  LOAD_GENEXPR             '<code_object <genexpr>>'
              150  LOAD_STR                 'evaluateVar.<locals>.<genexpr>'
              152  MAKE_FUNCTION_8          'closure'
              154  LOAD_DEREF               'xpCtx'
              156  LOAD_ATTR                varBindings
              158  LOAD_ATTR                items
              160  CALL_FUNCTION_0       0  ''
              162  GET_ITER         
              164  CALL_FUNCTION_1       1  ''
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'thisEvaluation'

 L. 141       170  LOAD_GLOBAL              evaluationIsUnnecessary
              172  LOAD_FAST                'thisEvaluation'
              174  LOAD_DEREF               'xpCtx'
              176  CALL_FUNCTION_2       2  ''
              178  POP_JUMP_IF_FALSE   350  'to 350'

 L. 142       182  LOAD_DEREF               'xpCtx'
              184  LOAD_ATTR                formulaOptions
              186  LOAD_ATTR                traceVariableSetExpressionResult
              188  POP_JUMP_IF_FALSE   216  'to 216'

 L. 143       190  LOAD_DEREF               'xpCtx'
              192  LOAD_ATTR                modelXbrl
              194  LOAD_ATTR                info
              196  LOAD_STR                 'formula:trace'

 L. 144       198  LOAD_GLOBAL              _
              200  LOAD_STR                 'Variable set %(xlinkLabel)s skipped non-different or fallback evaluation, duplicates another evaluation'
              202  CALL_FUNCTION_1       1  ''

 L. 145       204  LOAD_DEREF               'varSet'
              206  LOAD_DEREF               'varSet'
              208  LOAD_ATTR                xlinkLabel
              210  LOAD_CONST               ('modelObject', 'xlinkLabel')
              212  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              214  POP_TOP          
            216_0  COME_FROM           188  '188'

 L. 146       216  LOAD_DEREF               'varSet'
              218  DUP_TOP          
              220  LOAD_ATTR                evaluationNumber
              222  LOAD_CONST               1
              224  INPLACE_ADD      
              226  ROT_TWO          
              228  STORE_ATTR               evaluationNumber

 L. 147       230  LOAD_DEREF               'xpCtx'
              232  LOAD_ATTR                formulaOptions
              234  LOAD_ATTR                timeVariableSetEvaluation
              236  POP_JUMP_IF_FALSE   306  'to 306'

 L. 148       240  LOAD_GLOBAL              time
              242  LOAD_ATTR                time
              244  CALL_FUNCTION_0       0  ''
              246  STORE_FAST               'now'

 L. 149       248  LOAD_DEREF               'xpCtx'
              250  LOAD_ATTR                modelXbrl
              252  LOAD_ATTR                info
              254  LOAD_STR                 'formula:time'

 L. 150       256  LOAD_GLOBAL              _
              258  LOAD_STR                 'Variable set %(xlinkLabel)s skipped evaluation %(count)s: %(time)s sec'
              260  CALL_FUNCTION_1       1  ''

 L. 151       262  LOAD_DEREF               'varSet'
              264  LOAD_DEREF               'varSet'
              266  LOAD_ATTR                xlinkLabel
              268  LOAD_DEREF               'varSet'
              270  LOAD_ATTR                evaluationNumber

 L. 152       272  LOAD_GLOBAL              format_string
              274  LOAD_DEREF               'xpCtx'
              276  LOAD_ATTR                modelXbrl
              278  LOAD_ATTR                modelManager
              280  LOAD_ATTR                locale
              282  LOAD_STR                 '%.3f'
              284  LOAD_FAST                'now'
              286  LOAD_DEREF               'varSet'
              288  LOAD_ATTR                timeEvaluationStarted
              290  BINARY_SUBTRACT  
              292  CALL_FUNCTION_3       3  ''
              294  LOAD_CONST               ('modelObject', 'xlinkLabel', 'count', 'time')
              296  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              298  POP_TOP          

 L. 153       300  LOAD_FAST                'now'
              302  LOAD_DEREF               'varSet'
              304  STORE_ATTR               timeEvaluationStarted
            306_0  COME_FROM           236  '236'

 L. 154       306  LOAD_DEREF               'xpCtx'
              308  LOAD_ATTR                isRunTimeExceeded
              310  POP_JUMP_IF_FALSE   322  'to 322'

 L. 154       314  LOAD_GLOBAL              XPathContext
              316  LOAD_ATTR                RunTimeExceededException
              318  CALL_FUNCTION_0       0  ''
              320  RAISE_VARARGS_1       1  ''
            322_0  COME_FROM           310  '310'

 L. 155       322  LOAD_DEREF               'xpCtx'
              324  LOAD_ATTR                modelXbrl
              326  LOAD_ATTR                profileActivity
              328  LOAD_STR                 '...   evaluation {0} (skipped)'
              330  LOAD_ATTR                format
              332  LOAD_DEREF               'varSet'
              334  LOAD_ATTR                evaluationNumber
              336  CALL_FUNCTION_1       1  ''
              338  LOAD_CONST               10.0
              340  LOAD_CONST               ('minTimeToShow',)
              342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              344  POP_TOP          

 L. 156       346  LOAD_CONST               None
              348  RETURN_END_IF    
            350_0  COME_FROM           178  '178'

 L. 157       350  LOAD_DEREF               'xpCtx'
              352  LOAD_ATTR                modelXbrl
              354  LOAD_ATTR                profileActivity
              356  LOAD_STR                 '...   evaluation {0}'
              358  LOAD_ATTR                format
              360  LOAD_DEREF               'varSet'
              362  LOAD_ATTR                evaluationNumber
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_CONST               10.0
              368  LOAD_CONST               ('minTimeToShow',)
              370  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              372  POP_TOP          

 L. 158       374  SETUP_LOOP          454  'to 454'
              376  LOAD_FAST                'thisEvaluation'
              378  LOAD_ATTR                items
              380  CALL_FUNCTION_0       0  ''
              382  GET_ITER         
              384  FOR_ITER            452  'to 452'
              386  UNPACK_SEQUENCE_2     2 
              388  STORE_FAST               'vQn'
              390  STORE_FAST               'vBoundFact'

 L. 160       392  LOAD_FAST                'vQn'
              394  LOAD_DEREF               'xpCtx'
              396  LOAD_ATTR                evaluationHashDicts
              398  COMPARE_OP               not-in
              400  POP_JUMP_IF_FALSE   418  'to 418'

 L. 160       404  LOAD_GLOBAL              defaultdict
              406  LOAD_GLOBAL              set
              408  CALL_FUNCTION_1       1  ''
              410  LOAD_DEREF               'xpCtx'
              412  LOAD_ATTR                evaluationHashDicts
              414  LOAD_FAST                'vQn'
              416  STORE_SUBSCR     
            418_0  COME_FROM           400  '400'

 L. 161       418  LOAD_DEREF               'xpCtx'
              420  LOAD_ATTR                evaluationHashDicts
              422  LOAD_FAST                'vQn'
              424  BINARY_SUBSCR    
              426  LOAD_GLOBAL              hash
              428  LOAD_FAST                'vBoundFact'
              430  CALL_FUNCTION_1       1  ''
              432  BINARY_SUBSCR    
              434  LOAD_ATTR                add
              436  LOAD_GLOBAL              len
              438  LOAD_DEREF               'xpCtx'
              440  LOAD_ATTR                evaluations
              442  CALL_FUNCTION_1       1  ''
              444  CALL_FUNCTION_1       1  ''
              446  POP_TOP          
              448  JUMP_BACK           384  'to 384'
              452  POP_BLOCK        
            454_0  COME_FROM_LOOP      374  '374'

 L. 162       454  LOAD_DEREF               'xpCtx'
              456  LOAD_ATTR                evaluations
              458  LOAD_ATTR                append
              460  LOAD_FAST                'thisEvaluation'
              462  CALL_FUNCTION_1       1  ''
              464  POP_TOP          

 L. 164       466  SETUP_LOOP          652  'to 652'
              468  LOAD_DEREF               'varSet'
              470  LOAD_ATTR                preconditions
              472  GET_ITER         
              474  FOR_ITER            650  'to 650'
              476  STORE_FAST               'precondition'

 L. 165       478  LOAD_FAST                'precondition'
              480  LOAD_ATTR                evalTest
              482  LOAD_DEREF               'xpCtx'
              484  CALL_FUNCTION_1       1  ''
              486  STORE_FAST               'result'

 L. 166       488  LOAD_DEREF               'xpCtx'
              490  LOAD_ATTR                formulaOptions
              492  LOAD_ATTR                traceVariableSetExpressionResult
              494  POP_JUMP_IF_FALSE   530  'to 530'

 L. 167       498  LOAD_DEREF               'xpCtx'
              500  LOAD_ATTR                modelXbrl
              502  LOAD_ATTR                info
              504  LOAD_STR                 'formula:trace'

 L. 168       506  LOAD_GLOBAL              _
              508  LOAD_STR                 'Variable set %(xlinkLabel)s \nPrecondition %(precondition)s \nResult: %(result)s'
              510  CALL_FUNCTION_1       1  ''

 L. 169       512  LOAD_DEREF               'varSet'
              514  LOAD_DEREF               'varSet'
              516  LOAD_ATTR                xlinkLabel
              518  LOAD_FAST                'precondition'
              520  LOAD_ATTR                xlinkLabel
              522  LOAD_FAST                'result'
              524  LOAD_CONST               ('modelObject', 'xlinkLabel', 'precondition', 'result')
              526  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              528  POP_TOP          
            530_0  COME_FROM           494  '494'

 L. 170       530  LOAD_FAST                'result'
              532  POP_JUMP_IF_TRUE    474  'to 474'

 L. 171       536  LOAD_DEREF               'xpCtx'
              538  LOAD_ATTR                formulaOptions
              540  LOAD_ATTR                timeVariableSetEvaluation
              542  POP_JUMP_IF_FALSE   626  'to 626'

 L. 172       546  LOAD_DEREF               'varSet'
              548  DUP_TOP          
              550  LOAD_ATTR                evaluationNumber
              552  LOAD_CONST               1
              554  INPLACE_ADD      
              556  ROT_TWO          
              558  STORE_ATTR               evaluationNumber

 L. 173       560  LOAD_GLOBAL              time
              562  LOAD_ATTR                time
              564  CALL_FUNCTION_0       0  ''
              566  STORE_FAST               'now'

 L. 174       568  LOAD_DEREF               'xpCtx'
              570  LOAD_ATTR                modelXbrl
              572  LOAD_ATTR                info
              574  LOAD_STR                 'formula:time'

 L. 175       576  LOAD_GLOBAL              _
              578  LOAD_STR                 'Variable set %(xlinkLabel)s precondition blocked evaluation %(count)s: %(time)s sec'
              580  CALL_FUNCTION_1       1  ''

 L. 176       582  LOAD_DEREF               'varSet'
              584  LOAD_DEREF               'varSet'
              586  LOAD_ATTR                xlinkLabel
              588  LOAD_DEREF               'varSet'
              590  LOAD_ATTR                evaluationNumber

 L. 177       592  LOAD_GLOBAL              format_string
              594  LOAD_DEREF               'xpCtx'
              596  LOAD_ATTR                modelXbrl
              598  LOAD_ATTR                modelManager
              600  LOAD_ATTR                locale
              602  LOAD_STR                 '%.3f'
              604  LOAD_FAST                'now'
              606  LOAD_DEREF               'varSet'
              608  LOAD_ATTR                timeEvaluationStarted
              610  BINARY_SUBTRACT  
              612  CALL_FUNCTION_3       3  ''
              614  LOAD_CONST               ('modelObject', 'xlinkLabel', 'count', 'time')
              616  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              618  POP_TOP          

 L. 178       620  LOAD_FAST                'now'
              622  LOAD_DEREF               'varSet'
              624  STORE_ATTR               timeEvaluationStarted
            626_0  COME_FROM           542  '542'

 L. 179       626  LOAD_DEREF               'xpCtx'
              628  LOAD_ATTR                isRunTimeExceeded
              630  POP_JUMP_IF_FALSE   642  'to 642'

 L. 179       634  LOAD_GLOBAL              XPathContext
              636  LOAD_ATTR                RunTimeExceededException
              638  CALL_FUNCTION_0       0  ''
              640  RAISE_VARARGS_1       1  ''
            642_0  COME_FROM           630  '630'

 L. 180       642  LOAD_CONST               None
              644  RETURN_VALUE     
              646  JUMP_BACK           474  'to 474'
              650  POP_BLOCK        
            652_0  COME_FROM_LOOP      466  '466'

 L. 183       652  LOAD_GLOBAL              isinstance
              654  LOAD_DEREF               'varSet'
              656  LOAD_GLOBAL              ModelExistenceAssertion
              658  CALL_FUNCTION_2       2  ''
              660  POP_JUMP_IF_FALSE   682  'to 682'

 L. 184       664  LOAD_DEREF               'varSet'
              666  DUP_TOP          
              668  LOAD_ATTR                evaluationsCount
              670  LOAD_CONST               1
              672  INPLACE_ADD      
              674  ROT_TWO          
              676  STORE_ATTR               evaluationsCount
              678  JUMP_ABSOLUTE      3288  'to 3288'
              682  ELSE                     '1882'

 L. 186       682  LOAD_GLOBAL              isinstance
              684  LOAD_DEREF               'varSet'
              686  LOAD_GLOBAL              ModelTuple
              688  CALL_FUNCTION_2       2  ''
              690  POP_JUMP_IF_FALSE   706  'to 706'

 L. 187       694  LOAD_STR                 '(tuple)'
              696  STORE_FAST               'result'

 L. 188       698  LOAD_STR                 'Tuple'
              700  STORE_FAST               'traceOf'
              702  JUMP_FORWARD       1300  'to 1300'
              706  ELSE                     '1300'

 L. 189       706  LOAD_GLOBAL              isinstance
              708  LOAD_DEREF               'varSet'
              710  LOAD_GLOBAL              ModelFormula
              712  CALL_FUNCTION_2       2  ''
              714  POP_JUMP_IF_FALSE   738  'to 738'

 L. 190       718  LOAD_DEREF               'xpCtx'
              720  LOAD_ATTR                evaluate
              722  LOAD_DEREF               'varSet'
              724  LOAD_ATTR                valueProg
              726  CALL_FUNCTION_1       1  ''
              728  STORE_FAST               'result'

 L. 191       730  LOAD_STR                 'Formula'
              732  STORE_FAST               'traceOf'
              734  JUMP_FORWARD       1300  'to 1300'
              738  ELSE                     '1300'

 L. 192       738  LOAD_GLOBAL              isinstance
              740  LOAD_DEREF               'varSet'
              742  LOAD_GLOBAL              ModelValueAssertion
              744  CALL_FUNCTION_2       2  ''
              746  POP_JUMP_IF_FALSE  1300  'to 1300'

 L. 193       750  LOAD_DEREF               'xpCtx'
              752  LOAD_ATTR                evaluateBooleanValue
              754  LOAD_DEREF               'varSet'
              756  LOAD_ATTR                testProg
              758  CALL_FUNCTION_1       1  ''
              760  STORE_FAST               'result'

 L. 194       762  LOAD_FAST                'result'
              764  POP_JUMP_IF_FALSE   784  'to 784'

 L. 194       768  LOAD_DEREF               'varSet'
              770  DUP_TOP          
              772  LOAD_ATTR                countSatisfied
              774  LOAD_CONST               1
              776  INPLACE_ADD      
              778  ROT_TWO          
              780  STORE_ATTR               countSatisfied
              782  JUMP_FORWARD        798  'to 798'
              784  ELSE                     '798'

 L. 195       784  LOAD_DEREF               'varSet'
              786  DUP_TOP          
              788  LOAD_ATTR                countNotSatisfied
              790  LOAD_CONST               1
              792  INPLACE_ADD      
              794  ROT_TWO          
              796  STORE_ATTR               countNotSatisfied
            798_0  COME_FROM           782  '782'

 L. 196       798  LOAD_DEREF               'varSet'
              800  LOAD_ATTR                message
              802  LOAD_FAST                'result'
              804  CALL_FUNCTION_1       1  ''
              806  STORE_FAST               'msg'

 L. 197       808  LOAD_FAST                'msg'
              810  LOAD_CONST               None
              812  COMPARE_OP               is-not
              814  POP_JUMP_IF_FALSE   902  'to 902'

 L. 198       818  LOAD_DEREF               'varSet'
              820  LOAD_ATTR                test
              822  LOAD_DEREF               'xpCtx'
              824  LOAD_ATTR                inScopeVars
              826  LOAD_GLOBAL              XbrlConst
              828  LOAD_ATTR                qnVaTestExpression
              830  STORE_SUBSCR     

 L. 199       832  LOAD_DEREF               'xpCtx'
              834  LOAD_ATTR                modelXbrl
              836  LOAD_ATTR                info
              838  LOAD_STR                 'message:'
              840  LOAD_DEREF               'varSet'
              842  LOAD_ATTR                id
              844  JUMP_IF_TRUE_OR_POP   862  'to 862'
              848  LOAD_DEREF               'varSet'
              850  LOAD_ATTR                xlinkLabel
              852  JUMP_IF_TRUE_OR_POP   862  'to 862'
              856  LOAD_GLOBAL              _
              858  LOAD_STR                 'unlabeled variableSet'
              860  CALL_FUNCTION_1       1  ''
            862_0  COME_FROM           852  '852'
            862_1  COME_FROM           844  '844'
              862  BINARY_ADD       

 L. 200       864  LOAD_FAST                'msg'
              866  LOAD_ATTR                evaluate
              868  LOAD_DEREF               'xpCtx'
              870  CALL_FUNCTION_1       1  ''

 L. 201       872  LOAD_DEREF               'varSet'

 L. 202       874  LOAD_DEREF               'varSet'
              876  LOAD_ATTR                logLabel
              878  CALL_FUNCTION_0       0  ''

 L. 203       880  LOAD_CONST               ('message:{variableSetID|xlinkLabel}',)
              882  LOAD_CONST               ('modelObject', 'label', 'messageCodes')
              884  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              886  POP_TOP          

 L. 204       888  LOAD_DEREF               'xpCtx'
              890  LOAD_ATTR                inScopeVars
              892  LOAD_ATTR                pop
              894  LOAD_GLOBAL              XbrlConst
              896  LOAD_ATTR                qnVaTestExpression
              898  CALL_FUNCTION_1       1  ''
              900  POP_TOP          
            902_0  COME_FROM           814  '814'

 L. 205       902  LOAD_DEREF               'xpCtx'
              904  LOAD_ATTR                formulaOptions
              906  LOAD_ATTR                traceSatisfiedAssertions
              908  POP_JUMP_IF_FALSE   918  'to 918'
              912  LOAD_FAST                'result'
            914_0  COME_FROM           908  '908'
              914  POP_JUMP_IF_TRUE    946  'to 946'

 L. 206       918  LOAD_DEREF               'xpCtx'
              920  LOAD_ATTR                formulaOptions
              922  LOAD_ATTR                traceUnsatisfiedAssertions
              924  POP_JUMP_IF_TRUE    938  'to 938'

 L. 207       928  LOAD_DEREF               'xpCtx'
              930  LOAD_ATTR                formulaOptions
              932  LOAD_ATTR                errorUnsatisfiedAssertions
            934_0  COME_FROM           924  '924'
              934  POP_JUMP_IF_FALSE  1296  'to 1296'
              938  LOAD_FAST                'result'
              940  UNARY_NOT        
            942_0  COME_FROM           934  '934'
            942_1  COME_FROM           914  '914'
              942  POP_JUMP_IF_FALSE  1296  'to 1296'

 L. 208       946  LOAD_DEREF               'varSet'
              948  BUILD_LIST_1          1 
              950  STORE_FAST               '_modelObjects'

 L. 209       952  BUILD_LIST_0          0 
              954  STORE_FAST               'factVarBindings'

 L. 210       956  SETUP_LOOP         1200  'to 1200'
              958  LOAD_GLOBAL              sorted
              960  LOAD_DEREF               'xpCtx'
              962  LOAD_ATTR                varBindings
              964  LOAD_ATTR                values
              966  CALL_FUNCTION_0       0  ''
              968  LOAD_LAMBDA              '<code_object <lambda>>'
              970  LOAD_STR                 'evaluateVar.<locals>.<lambda>'
              972  MAKE_FUNCTION_0          ''
              974  LOAD_CONST               ('key',)
              976  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              978  GET_ITER         
              980  FOR_ITER           1198  'to 1198'
              982  STORE_FAST               'vb'

 L. 211       984  LOAD_FAST                'vb'
              986  LOAD_ATTR                isFallback
              988  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 212       992  LOAD_FAST                'factVarBindings'
              994  LOAD_ATTR                append
              996  LOAD_STR                 ', \n${}: fallback {}'
              998  LOAD_ATTR                format
             1000  LOAD_FAST                'vb'
             1002  LOAD_ATTR                qname
             1004  LOAD_DEREF               'xpCtx'
             1006  LOAD_ATTR                flattenSequence
             1008  LOAD_FAST                'vb'
             1010  LOAD_ATTR                values
             1012  CALL_FUNCTION_1       1  ''
             1014  CALL_FUNCTION_2       2  ''
             1016  CALL_FUNCTION_1       1  ''
             1018  POP_TOP          
             1020  JUMP_FORWARD       1194  'to 1194'
             1022  ELSE                     '1194'

 L. 214      1022  LOAD_FAST                'vb'
             1024  LOAD_ATTR                isBindAsSequence
             1026  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 215      1030  LOAD_GLOBAL              isinstance
             1032  LOAD_FAST                'vb'
             1034  LOAD_ATTR                yieldedEvaluation
             1036  LOAD_GLOBAL              list
             1038  CALL_FUNCTION_2       2  ''
             1040  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 216      1044  LOAD_FAST                '_modelObjects'
             1046  LOAD_ATTR                extend
             1048  LOAD_FAST                'vb'
             1050  LOAD_ATTR                yieldedEvaluation
             1052  CALL_FUNCTION_1       1  ''
             1054  POP_TOP          
             1056  JUMP_FORWARD       1082  'to 1082'
             1058  ELSE                     '1082'

 L. 217      1058  LOAD_FAST                'vb'
             1060  LOAD_ATTR                yieldedFact
             1062  LOAD_CONST               None
             1064  COMPARE_OP               is-not
             1066  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 218      1070  LOAD_FAST                '_modelObjects'
             1072  LOAD_ATTR                append
             1074  LOAD_FAST                'vb'
             1076  LOAD_ATTR                yieldedFact
             1078  CALL_FUNCTION_1       1  ''
             1080  POP_TOP          
           1082_0  COME_FROM          1066  '1066'
           1082_1  COME_FROM          1056  '1056'
           1082_2  COME_FROM          1040  '1040'

 L. 219      1082  LOAD_FAST                'vb'
             1084  LOAD_ATTR                yieldedFact
             1086  LOAD_CONST               None
             1088  COMPARE_OP               is-not
             1090  POP_JUMP_IF_FALSE   980  'to 980'

 L. 220      1094  LOAD_FAST                'vb'
             1096  LOAD_ATTR                yieldedFact
             1098  LOAD_ATTR                isItem
             1100  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 221      1104  LOAD_FAST                'factVarBindings'
             1106  LOAD_ATTR                append
             1108  LOAD_STR                 ', \n${}: {} context {}'
             1110  LOAD_ATTR                format
             1112  LOAD_FAST                'vb'
             1114  LOAD_ATTR                qname
             1116  LOAD_FAST                'vb'
             1118  LOAD_ATTR                yieldedFact
             1120  LOAD_ATTR                qname
             1122  LOAD_FAST                'vb'
             1124  LOAD_ATTR                yieldedFactContext
             1126  LOAD_ATTR                id
             1128  CALL_FUNCTION_3       3  ''
             1130  CALL_FUNCTION_1       1  ''
             1132  POP_TOP          
             1134  JUMP_FORWARD       1194  'to 1194'
             1136  ELSE                     '1194'

 L. 222      1136  LOAD_FAST                'vb'
             1138  LOAD_ATTR                yieldedFact
             1140  LOAD_ATTR                isTuple
             1142  POP_JUMP_IF_FALSE   980  'to 980'
             1146  LOAD_GLOBAL              isinstance
             1148  LOAD_FAST                'vb'
             1150  LOAD_ATTR                yieldedFact
             1152  LOAD_ATTR                parentElement
             1154  LOAD_GLOBAL              ModelFact
             1156  CALL_FUNCTION_2       2  ''
             1158  POP_JUMP_IF_FALSE   980  'to 980'

 L. 223      1162  LOAD_FAST                'factVarBindings'
             1164  LOAD_ATTR                append
             1166  LOAD_STR                 ', \n${}: {} tuple {}'
             1168  LOAD_ATTR                format
             1170  LOAD_FAST                'vb'
             1172  LOAD_ATTR                qname
             1174  LOAD_FAST                'vb'
             1176  LOAD_ATTR                yieldedFact
             1178  LOAD_ATTR                qname
             1180  LOAD_FAST                'vb'
             1182  LOAD_ATTR                yieldedFact
             1184  LOAD_ATTR                parentElement
             1186  LOAD_ATTR                qname
             1188  CALL_FUNCTION_3       3  ''
             1190  CALL_FUNCTION_1       1  ''
             1192  POP_TOP          
           1194_0  COME_FROM          1134  '1134'
           1194_1  COME_FROM          1020  '1020'
             1194  JUMP_BACK           980  'to 980'
             1198  POP_BLOCK        
           1200_0  COME_FROM_LOOP      956  '956'

 L. 224      1200  LOAD_DEREF               'xpCtx'
             1202  LOAD_ATTR                modelXbrl
             1204  LOAD_ATTR                log

 L. 225      1206  LOAD_DEREF               'xpCtx'
             1208  LOAD_ATTR                formulaOptions
             1210  LOAD_ATTR                errorUnsatisfiedAssertions
             1212  POP_JUMP_IF_FALSE  1228  'to 1228'
             1216  LOAD_FAST                'result'
             1218  UNARY_NOT        
             1220  POP_JUMP_IF_FALSE  1228  'to 1228'
             1224  LOAD_STR                 'ERROR'
             1226  JUMP_FORWARD       1230  'to 1230'
           1228_0  COME_FROM          1212  '1212'
             1228  LOAD_STR                 'INFO'
           1230_0  COME_FROM          1226  '1226'

 L. 226      1230  LOAD_FAST                'result'
             1232  POP_JUMP_IF_FALSE  1240  'to 1240'
             1236  LOAD_STR                 'formula:assertionSatisfied'
             1238  JUMP_FORWARD       1242  'to 1242'
             1240  ELSE                     '1242'
             1240  LOAD_STR                 'formula:assertionUnsatisfied'
           1242_0  COME_FROM          1238  '1238'

 L. 227      1242  LOAD_GLOBAL              _
             1244  LOAD_STR                 '%(label)s%(factVarBindings)s'
             1246  CALL_FUNCTION_1       1  ''

 L. 228      1248  LOAD_FAST                '_modelObjects'
             1250  LOAD_DEREF               'varSet'
             1252  LOAD_ATTR                logLabel
             1254  CALL_FUNCTION_0       0  ''

 L. 229      1256  LOAD_STR                 ''
             1258  LOAD_ATTR                join
             1260  LOAD_FAST                'factVarBindings'
             1262  CALL_FUNCTION_1       1  ''
             1264  LOAD_FAST                'factVarBindings'
             1266  POP_JUMP_IF_FALSE  1274  'to 1274'
             1270  LOAD_STR                 '\n'
             1272  JUMP_FORWARD       1276  'to 1276'
             1274  ELSE                     '1276'
             1274  LOAD_STR                 ''
           1276_0  COME_FROM          1272  '1272'
             1276  BINARY_ADD       

 L. 230      1278  LOAD_CONST               ('formula:assertionSatisfied', 'formula:assertionUnsatisfied')
             1280  LOAD_CONST               ('modelObject', 'label', 'factVarBindings', 'messageCodes')
             1282  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1284  POP_TOP          

 L. 231      1286  LOAD_FAST                '_modelObjects'
             1288  LOAD_CONST               None
             1290  LOAD_CONST               None
             1292  BUILD_SLICE_2         2 
             1294  DELETE_SUBSCR    
           1296_0  COME_FROM           942  '942'

 L. 232      1296  LOAD_STR                 'Value Assertion'
             1298  STORE_FAST               'traceOf'
           1300_0  COME_FROM           746  '746'
           1300_1  COME_FROM           734  '734'
           1300_2  COME_FROM           702  '702'

 L. 233      1300  LOAD_DEREF               'xpCtx'
             1302  LOAD_ATTR                formulaOptions
             1304  LOAD_ATTR                traceVariableSetExpressionResult
             1306  POP_JUMP_IF_FALSE  1404  'to 1404'

 L. 234      1310  LOAD_DEREF               'varSet'
             1312  LOAD_ATTR                logLabel
             1314  CALL_FUNCTION_0       0  ''
             1316  STORE_FAST               'label'

 L. 235      1318  LOAD_DEREF               'varSet'
             1320  LOAD_ATTR                expression
             1322  STORE_FAST               'expression'

 L. 236      1324  LOAD_DEREF               'xpCtx'
             1326  LOAD_ATTR                modelXbrl
             1328  LOAD_ATTR                info
             1330  LOAD_STR                 'formula:trace'

 L. 237      1332  LOAD_GLOBAL              _
             1334  LOAD_STR                 '%(variableSetType)s %(xlinkLabel)s{0} \nExpression: %(expression)s \nEvaluated: %(evaluatedExpression)s \nResult: %(result)s'
             1336  CALL_FUNCTION_1       1  ''
             1338  LOAD_ATTR                format

 L. 238      1340  LOAD_FAST                'label'
             1342  POP_JUMP_IF_FALSE  1350  'to 1350'
             1346  LOAD_STR                 ' \n%(label)s'
             1348  JUMP_FORWARD       1352  'to 1352'
             1350  ELSE                     '1352'
             1350  LOAD_STR                 ''
           1352_0  COME_FROM          1348  '1348'
             1352  CALL_FUNCTION_1       1  ''

 L. 239      1354  LOAD_DEREF               'varSet'
             1356  LOAD_FAST                'traceOf'
             1358  LOAD_DEREF               'varSet'
             1360  LOAD_ATTR                xlinkLabel

 L. 240      1362  LOAD_FAST                'label'
             1364  LOAD_FAST                'result'
             1366  LOAD_FAST                'expression'

 L. 241      1368  LOAD_STR                 ''
             1370  LOAD_ATTR                join
             1372  LOAD_CLOSURE             'varSet'
             1374  LOAD_CLOSURE             'xpCtx'
             1376  BUILD_TUPLE_2         2 
             1378  LOAD_GENEXPR             '<code_object <genexpr>>'
             1380  LOAD_STR                 'evaluateVar.<locals>.<genexpr>'
             1382  MAKE_FUNCTION_8          'closure'

 L. 242      1384  LOAD_GLOBAL              expressionVariablesPattern
             1386  LOAD_ATTR                findall
             1388  LOAD_FAST                'expression'
             1390  CALL_FUNCTION_1       1  ''
             1392  GET_ITER         
             1394  CALL_FUNCTION_1       1  ''
             1396  CALL_FUNCTION_1       1  ''
             1398  LOAD_CONST               ('modelObject', 'variableSetType', 'xlinkLabel', 'label', 'result', 'expression', 'evaluatedExpression')
             1400  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1402  POP_TOP          
           1404_0  COME_FROM          1306  '1306'

 L. 244      1404  LOAD_GLOBAL              isinstance
             1406  LOAD_DEREF               'varSet'
             1408  LOAD_GLOBAL              ModelFormula
             1410  CALL_FUNCTION_2       2  ''
             1412  POP_JUMP_IF_FALSE  1444  'to 1444'
             1416  LOAD_DEREF               'varSet'
             1418  LOAD_ATTR                outputInstanceQname
             1420  LOAD_DEREF               'xpCtx'
             1422  LOAD_ATTR                inScopeVars
             1424  COMPARE_OP               in
             1426  POP_JUMP_IF_FALSE  1444  'to 1444'

 L. 245      1430  LOAD_GLOBAL              produceOutputFact
             1432  LOAD_DEREF               'xpCtx'
             1434  LOAD_DEREF               'varSet'
             1436  LOAD_FAST                'result'
             1438  CALL_FUNCTION_3       3  ''
             1440  STORE_FAST               'newFact'
             1442  JUMP_FORWARD       1448  'to 1448'
           1444_0  COME_FROM          1412  '1412'

 L. 247      1444  LOAD_CONST               None
             1446  STORE_FAST               'newFact'
           1448_0  COME_FROM          1442  '1442'

 L. 248      1448  LOAD_DEREF               'varSet'
             1450  LOAD_ATTR                hasConsistencyAssertion
             1452  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 249      1456  LOAD_CONST               0
             1458  LOAD_CONST               ('FormulaConsisAsser',)
             1460  IMPORT_NAME              arelle
             1462  IMPORT_FROM              FormulaConsisAsser
             1464  STORE_FAST               'FormulaConsisAsser'
             1466  POP_TOP          

 L. 250      1468  LOAD_FAST                'FormulaConsisAsser'
             1470  LOAD_ATTR                evaluate
             1472  LOAD_DEREF               'xpCtx'
             1474  LOAD_DEREF               'varSet'
             1476  LOAD_FAST                'newFact'
             1478  CALL_FUNCTION_3       3  ''
             1480  POP_TOP          
           1482_0  COME_FROM          1452  '1452'

 L. 252      1482  LOAD_DEREF               'xpCtx'
             1484  LOAD_ATTR                formulaOptions
             1486  LOAD_ATTR                timeVariableSetEvaluation
             1488  POP_JUMP_IF_FALSE  1572  'to 1572'

 L. 253      1492  LOAD_DEREF               'varSet'
             1494  DUP_TOP          
             1496  LOAD_ATTR                evaluationNumber
             1498  LOAD_CONST               1
             1500  INPLACE_ADD      
             1502  ROT_TWO          
             1504  STORE_ATTR               evaluationNumber

 L. 254      1506  LOAD_GLOBAL              time
             1508  LOAD_ATTR                time
             1510  CALL_FUNCTION_0       0  ''
             1512  STORE_FAST               'now'

 L. 255      1514  LOAD_DEREF               'xpCtx'
             1516  LOAD_ATTR                modelXbrl
             1518  LOAD_ATTR                info
             1520  LOAD_STR                 'formula:time'

 L. 256      1522  LOAD_GLOBAL              _
             1524  LOAD_STR                 'Variable set %(xlinkLabel)s completed evaluation %(count)s: %(time)s sec'
             1526  CALL_FUNCTION_1       1  ''

 L. 257      1528  LOAD_DEREF               'varSet'
             1530  LOAD_DEREF               'varSet'
             1532  LOAD_ATTR                xlinkLabel
             1534  LOAD_DEREF               'varSet'
             1536  LOAD_ATTR                evaluationNumber

 L. 258      1538  LOAD_GLOBAL              format_string
             1540  LOAD_DEREF               'xpCtx'
             1542  LOAD_ATTR                modelXbrl
             1544  LOAD_ATTR                modelManager
             1546  LOAD_ATTR                locale
             1548  LOAD_STR                 '%.3f'
             1550  LOAD_FAST                'now'
             1552  LOAD_DEREF               'varSet'
             1554  LOAD_ATTR                timeEvaluationStarted
             1556  BINARY_SUBTRACT  
             1558  CALL_FUNCTION_3       3  ''
             1560  LOAD_CONST               ('modelObject', 'xlinkLabel', 'count', 'time')
             1562  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1564  POP_TOP          

 L. 259      1566  LOAD_FAST                'now'
             1568  LOAD_DEREF               'varSet'
             1570  STORE_ATTR               timeEvaluationStarted
           1572_0  COME_FROM          1488  '1488'

 L. 260      1572  LOAD_DEREF               'xpCtx'
             1574  LOAD_ATTR                isRunTimeExceeded
             1576  POP_JUMP_IF_FALSE  1588  'to 1588'

 L. 260      1580  LOAD_GLOBAL              XPathContext
             1582  LOAD_ATTR                RunTimeExceededException
             1584  CALL_FUNCTION_0       0  ''
             1586  RAISE_VARARGS_1       1  ''
           1588_0  COME_FROM          1576  '1576'

 L. 263      1588  SETUP_LOOP         3288  'to 3288'
             1592  LOAD_DEREF               'xpCtx'
             1594  LOAD_ATTR                modelXbrl
             1596  LOAD_ATTR                relationshipSet
             1598  LOAD_GLOBAL              XbrlConst
             1600  LOAD_ATTR                variablesScope
             1602  CALL_FUNCTION_1       1  ''
             1604  LOAD_ATTR                fromModelObject
             1606  LOAD_DEREF               'varSet'
             1608  CALL_FUNCTION_1       1  ''
             1610  GET_ITER         
             1612  FOR_ITER           1878  'to 1878'
             1616  STORE_FAST               'varScopeRel'

 L. 264      1618  SETUP_EXCEPT       1796  'to 1796'

 L. 265      1620  LOAD_FAST                'varScopeRel'
             1622  LOAD_ATTR                variableQname
             1624  STORE_FAST               'resultQname'

 L. 266      1626  LOAD_FAST                'resultQname'
             1628  POP_JUMP_IF_FALSE  1698  'to 1698'

 L. 267      1632  LOAD_DEREF               'xpCtx'
             1634  LOAD_ATTR                inScopeVars
             1636  LOAD_ATTR                get
             1638  LOAD_FAST                'resultQname'
             1640  CALL_FUNCTION_1       1  ''
             1642  STORE_FAST               'overriddenInScopeVar'

 L. 268      1644  LOAD_FAST                'result'
             1646  LOAD_DEREF               'xpCtx'
             1648  LOAD_ATTR                inScopeVars
             1650  LOAD_FAST                'resultQname'
             1652  STORE_SUBSCR     

 L. 269      1654  LOAD_GLOBAL              VariableBinding
             1656  LOAD_DEREF               'xpCtx'
             1658  LOAD_FAST                'varScopeRel'
             1660  CALL_FUNCTION_2       2  ''
             1662  STORE_FAST               'vb'

 L. 270      1664  LOAD_FAST                'result'
             1666  LOAD_FAST                'vb'
             1668  STORE_ATTR               yieldedEvaluation

 L. 271      1670  LOAD_FAST                'newFact'
             1672  LOAD_FAST                'vb'
             1674  STORE_ATTR               yieldedFact

 L. 272      1676  LOAD_DEREF               'xpCtx'
             1678  LOAD_ATTR                varBindings
             1680  LOAD_ATTR                get
             1682  LOAD_FAST                'resultQname'
             1684  CALL_FUNCTION_1       1  ''
             1686  STORE_FAST               'overriddenVarBinding'

 L. 273      1688  LOAD_FAST                'vb'
             1690  LOAD_DEREF               'xpCtx'
             1692  LOAD_ATTR                varBindings
             1694  LOAD_FAST                'resultQname'
             1696  STORE_SUBSCR     
           1698_0  COME_FROM          1628  '1628'

 L. 274      1698  LOAD_GLOBAL              evaluate
             1700  LOAD_DEREF               'xpCtx'
             1702  LOAD_FAST                'varScopeRel'
             1704  LOAD_ATTR                toModelObject
             1706  LOAD_CONST               True
             1708  LOAD_FAST                'uncoveredAspectFacts'
             1710  CALL_FUNCTION_4       4  ''
             1712  POP_TOP          

 L. 275      1714  LOAD_FAST                'resultQname'
             1716  POP_JUMP_IF_FALSE  1792  'to 1792'

 L. 276      1720  LOAD_DEREF               'xpCtx'
             1722  LOAD_ATTR                inScopeVars
             1724  LOAD_ATTR                pop
             1726  LOAD_FAST                'resultQname'
             1728  CALL_FUNCTION_1       1  ''
             1730  POP_TOP          

 L. 277      1732  LOAD_FAST                'overriddenInScopeVar'
             1734  LOAD_CONST               None
             1736  COMPARE_OP               is-not
             1738  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 278      1742  LOAD_FAST                'overriddenInScopeVar'
             1744  LOAD_DEREF               'xpCtx'
             1746  LOAD_ATTR                inScopeVars
             1748  LOAD_FAST                'resultQname'
             1750  STORE_SUBSCR     
           1752_0  COME_FROM          1738  '1738'

 L. 279      1752  LOAD_DEREF               'xpCtx'
             1754  LOAD_ATTR                varBindings
             1756  LOAD_ATTR                pop
             1758  LOAD_FAST                'resultQname'
             1760  CALL_FUNCTION_1       1  ''
             1762  POP_TOP          

 L. 280      1764  LOAD_FAST                'overriddenVarBinding'
             1766  LOAD_CONST               None
             1768  COMPARE_OP               is-not
             1770  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 281      1774  LOAD_FAST                'overriddenVarBinding'
             1776  LOAD_DEREF               'xpCtx'
             1778  LOAD_ATTR                varBindings
             1780  LOAD_FAST                'resultQname'
             1782  STORE_SUBSCR     
           1784_0  COME_FROM          1770  '1770'

 L. 282      1784  LOAD_FAST                'vb'
             1786  LOAD_ATTR                close
             1788  CALL_FUNCTION_0       0  ''
             1790  POP_TOP          
           1792_0  COME_FROM          1716  '1716'
             1792  POP_BLOCK        
             1794  JUMP_FORWARD       1874  'to 1874'
           1796_0  COME_FROM_EXCEPT   1618  '1618'

 L. 283      1796  DUP_TOP          
             1798  LOAD_GLOBAL              XPathContext
             1800  LOAD_ATTR                XPathException
             1802  COMPARE_OP               exception-match
             1804  POP_JUMP_IF_FALSE  1872  'to 1872'
             1808  POP_TOP          
             1810  STORE_FAST               'err'
             1812  POP_TOP          
             1814  SETUP_FINALLY      1862  'to 1862'

 L. 284      1816  LOAD_DEREF               'xpCtx'
             1818  LOAD_ATTR                modelXbrl
             1820  LOAD_ATTR                error
             1822  LOAD_FAST                'err'
             1824  LOAD_ATTR                code

 L. 285      1826  LOAD_GLOBAL              _
             1828  LOAD_STR                 'Variable set chained in scope of variable set %(variableset)s \nException: \n%(error)s'
             1830  CALL_FUNCTION_1       1  ''

 L. 286      1832  LOAD_DEREF               'varSet'
             1834  LOAD_FAST                'varScopeRel'
             1836  LOAD_ATTR                toModelObject
             1838  BUILD_TUPLE_2         2 
             1840  LOAD_DEREF               'varSet'
             1842  LOAD_ATTR                logLabel
             1844  CALL_FUNCTION_0       0  ''
             1846  LOAD_FAST                'err'
             1848  LOAD_ATTR                message
             1850  LOAD_CONST               ('modelObject', 'variableSet', 'error')
             1852  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1854  POP_TOP          
             1856  POP_BLOCK        
             1858  POP_EXCEPT       
             1860  LOAD_CONST               None
           1862_0  COME_FROM_FINALLY  1814  '1814'
             1862  LOAD_CONST               None
             1864  STORE_FAST               'err'
             1866  DELETE_FAST              'err'
             1868  END_FINALLY      
             1870  JUMP_FORWARD       1874  'to 1874'
             1872  END_FINALLY      
           1874_0  COME_FROM          1870  '1870'
           1874_1  COME_FROM          1794  '1794'
             1874  JUMP_BACK          1612  'to 1612'
             1878  POP_BLOCK        
             1880  JUMP_FORWARD       3288  'to 3288'
             1884  ELSE                     '3288'

 L. 290      1884  LOAD_DEREF               'varSet'
             1886  LOAD_ATTR                orderedVariableRelationships
             1888  LOAD_FAST                'varIndex'
             1890  BINARY_SUBSCR    
             1892  STORE_FAST               'varRel'

 L. 291      1894  LOAD_FAST                'varRel'
             1896  LOAD_ATTR                variableQname
             1898  STORE_FAST               'varQname'

 L. 292      1900  LOAD_GLOBAL              VariableBinding
             1902  LOAD_DEREF               'xpCtx'
             1904  LOAD_FAST                'varRel'
             1906  CALL_FUNCTION_2       2  ''
             1908  STORE_FAST               'vb'

 L. 293      1910  LOAD_FAST                'vb'
             1912  LOAD_ATTR                var
             1914  STORE_FAST               'var'

 L. 294      1916  LOAD_FAST                'vb'
             1918  LOAD_ATTR                isFactVar
             1920  POP_JUMP_IF_FALSE  2776  'to 2776'

 L. 295      1924  LOAD_GLOBAL              set
             1926  LOAD_GLOBAL              aspectModels
             1928  LOAD_DEREF               'varSet'
             1930  LOAD_ATTR                aspectModel
             1932  BINARY_SUBSCR    
             1934  CALL_FUNCTION_1       1  ''
             1936  LOAD_FAST                'vb'
             1938  STORE_ATTR               aspectsDefined

 L. 296      1940  LOAD_CONST               None
             1942  LOAD_FAST                'vb'
             1944  STORE_ATTR               values

 L. 297      1946  LOAD_FAST                'var'
             1948  LOAD_ATTR                hasNoVariableDependencies
             1950  STORE_FAST               'varHasNoVariableDependencies'

 L. 298      1952  LOAD_FAST                'var'
             1954  LOAD_ATTR                nils
             1956  LOAD_STR                 'true'
             1958  COMPARE_OP               ==
             1960  STORE_DEREF              'varHasNilFacts'

 L. 299      1962  LOAD_FAST                'varHasNoVariableDependencies'
             1964  POP_JUMP_IF_FALSE  2040  'to 2040'
             1968  LOAD_FAST                'varQname'
             1970  LOAD_FAST                'cachedFilteredFacts'
             1972  COMPARE_OP               in
             1974  POP_JUMP_IF_FALSE  2040  'to 2040'

 L. 300      1978  LOAD_FAST                'cachedFilteredFacts'
             1980  LOAD_FAST                'varQname'
             1982  BINARY_SUBSCR    
             1984  UNPACK_SEQUENCE_3     3 
             1986  STORE_FAST               'facts'
             1988  LOAD_FAST                'vb'
             1990  STORE_ATTR               aspectsDefined
             1992  LOAD_FAST                'vb'
             1994  STORE_ATTR               aspectsCovered

 L. 301      1996  LOAD_DEREF               'xpCtx'
             1998  LOAD_ATTR                formulaOptions
             2000  LOAD_ATTR                traceVariableFilterWinnowing
             2002  POP_JUMP_IF_FALSE  2380  'to 2380'

 L. 302      2006  LOAD_DEREF               'xpCtx'
             2008  LOAD_ATTR                modelXbrl
             2010  LOAD_ATTR                info
             2012  LOAD_STR                 'formula:trace'

 L. 303      2014  LOAD_GLOBAL              _
             2016  LOAD_STR                 'Fact Variable %(variable)s: start with %(factCount)s facts previously cached after explicit filters'
             2018  CALL_FUNCTION_1       1  ''

 L. 304      2020  LOAD_FAST                'var'
             2022  LOAD_FAST                'varQname'
             2024  LOAD_GLOBAL              len
             2026  LOAD_FAST                'facts'
             2028  CALL_FUNCTION_1       1  ''
             2030  LOAD_CONST               ('modelObject', 'variable', 'factCount')
             2032  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2034  POP_TOP          
             2036  JUMP_FORWARD       2380  'to 2380'
           2040_0  COME_FROM          1964  '1964'

 L. 306      2040  LOAD_FAST                'var'
             2042  LOAD_ATTR                fromInstanceQnames
             2044  POP_JUMP_IF_FALSE  2062  'to 2062'

 L. 307      2048  LOAD_STR                 'grp:'
             2050  LOAD_GLOBAL              str
             2052  LOAD_FAST                'varQname'
             2054  CALL_FUNCTION_1       1  ''
             2056  BINARY_ADD       
             2058  STORE_FAST               'groupFilteredFactsKey'
             2060  JUMP_FORWARD       2078  'to 2078'
             2062  ELSE                     '2078'

 L. 308      2062  LOAD_DEREF               'varHasNilFacts'
             2064  POP_JUMP_IF_FALSE  2074  'to 2074'

 L. 309      2068  LOAD_STR                 'grp:stdInstWithNils'
             2070  STORE_FAST               'groupFilteredFactsKey'
             2072  JUMP_FORWARD       2078  'to 2078'
             2074  ELSE                     '2078'

 L. 311      2074  LOAD_STR                 'grp:stdInstNonNil'
             2076  STORE_FAST               'groupFilteredFactsKey'
           2078_0  COME_FROM          2072  '2072'
           2078_1  COME_FROM          2060  '2060'

 L. 312      2078  LOAD_FAST                'groupFilteredFactsKey'
             2080  LOAD_FAST                'cachedFilteredFacts'
             2082  COMPARE_OP               in
             2084  POP_JUMP_IF_FALSE  2138  'to 2138'

 L. 313      2088  LOAD_FAST                'cachedFilteredFacts'
             2090  LOAD_FAST                'groupFilteredFactsKey'
             2092  BINARY_SUBSCR    
             2094  STORE_FAST               'facts'

 L. 314      2096  LOAD_DEREF               'xpCtx'
             2098  LOAD_ATTR                formulaOptions
             2100  LOAD_ATTR                traceVariableFilterWinnowing
             2102  POP_JUMP_IF_FALSE  2252  'to 2252'

 L. 315      2106  LOAD_DEREF               'xpCtx'
             2108  LOAD_ATTR                modelXbrl
             2110  LOAD_ATTR                info
             2112  LOAD_STR                 'formula:trace'

 L. 316      2114  LOAD_GLOBAL              _
             2116  LOAD_STR                 'Fact Variable %(variable)s: start with %(factCount)s facts previously cached before variable filters'
             2118  CALL_FUNCTION_1       1  ''

 L. 317      2120  LOAD_FAST                'var'
             2122  LOAD_FAST                'varQname'
             2124  LOAD_GLOBAL              len
             2126  LOAD_FAST                'facts'
             2128  CALL_FUNCTION_1       1  ''
             2130  LOAD_CONST               ('modelObject', 'variable', 'factCount')
             2132  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2134  POP_TOP          
             2136  JUMP_FORWARD       2252  'to 2252'
             2138  ELSE                     '2252'

 L. 319      2138  LOAD_GLOBAL              set
             2140  LOAD_ATTR                union
             2142  LOAD_CLOSURE             'varHasNilFacts'
             2144  BUILD_TUPLE_1         1 
             2146  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2148  LOAD_STR                 'evaluateVar.<locals>.<listcomp>'
             2150  MAKE_FUNCTION_8          'closure'

 L. 320      2152  LOAD_FAST                'vb'
             2154  LOAD_ATTR                instances
             2156  GET_ITER         
             2158  CALL_FUNCTION_1       1  ''
             2160  CALL_FUNCTION_EX      0  ''
             2162  STORE_FAST               'facts'

 L. 321      2164  LOAD_DEREF               'xpCtx'
             2166  LOAD_ATTR                formulaOptions
             2168  LOAD_ATTR                traceVariableFilterWinnowing
             2170  POP_JUMP_IF_FALSE  2204  'to 2204'

 L. 322      2174  LOAD_DEREF               'xpCtx'
             2176  LOAD_ATTR                modelXbrl
             2178  LOAD_ATTR                info
             2180  LOAD_STR                 'formula:trace'

 L. 323      2182  LOAD_GLOBAL              _
             2184  LOAD_STR                 'Fact Variable %(variable)s filtering: start with %(factCount)s facts'
             2186  CALL_FUNCTION_1       1  ''

 L. 324      2188  LOAD_FAST                'var'
             2190  LOAD_FAST                'varQname'
             2192  LOAD_GLOBAL              len
             2194  LOAD_FAST                'facts'
             2196  CALL_FUNCTION_1       1  ''
             2198  LOAD_CONST               ('modelObject', 'variable', 'factCount')
             2200  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2202  POP_TOP          
           2204_0  COME_FROM          2170  '2170'

 L. 326      2204  LOAD_GLOBAL              checkVarSetFilterInfo
             2206  LOAD_DEREF               'varSet'
             2208  CALL_FUNCTION_1       1  ''
             2210  POP_TOP          

 L. 327      2212  LOAD_GLOBAL              trialFilterFacts
             2214  LOAD_DEREF               'xpCtx'
             2216  LOAD_FAST                'vb'
             2218  LOAD_FAST                'facts'
             2220  LOAD_DEREF               'varSet'
             2222  LOAD_ATTR                groupFilterRelationships
             2224  LOAD_STR                 'group'
             2226  LOAD_DEREF               'varSet'
             2228  LOAD_CONST               ('varSet',)
             2230  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2232  STORE_FAST               'facts'

 L. 329      2234  LOAD_FAST                'vb'
             2236  LOAD_ATTR                aspectsCovered
             2238  LOAD_ATTR                clear
             2240  CALL_FUNCTION_0       0  ''
             2242  POP_TOP          

 L. 330      2244  LOAD_FAST                'facts'
             2246  LOAD_FAST                'cachedFilteredFacts'
             2248  LOAD_FAST                'groupFilteredFactsKey'
             2250  STORE_SUBSCR     
           2252_0  COME_FROM          2136  '2136'
           2252_1  COME_FROM          2102  '2102'

 L. 332      2252  LOAD_GLOBAL              checkVarFilterInfo
             2254  LOAD_FAST                'var'
             2256  CALL_FUNCTION_1       1  ''
             2258  POP_TOP          

 L. 333      2260  LOAD_GLOBAL              trialFilterFacts
             2262  LOAD_DEREF               'xpCtx'
             2264  LOAD_FAST                'vb'
             2266  LOAD_FAST                'facts'
             2268  LOAD_FAST                'var'
             2270  LOAD_ATTR                filterRelationships
             2272  LOAD_CONST               None
             2274  LOAD_FAST                'var'
             2276  LOAD_CONST               ('var',)
             2278  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2280  STORE_FAST               'facts'

 L. 336      2282  SETUP_LOOP         2342  'to 2342'
             2284  LOAD_FAST                'facts'
             2286  GET_ITER         
             2288  FOR_ITER           2340  'to 2340'
             2290  STORE_FAST               'fact'

 L. 337      2292  LOAD_FAST                'fact'
             2294  LOAD_ATTR                isItem
             2296  POP_JUMP_IF_FALSE  2288  'to 2288'
             2300  LOAD_FAST                'fact'
             2302  LOAD_ATTR                context
             2304  LOAD_CONST               None
             2306  COMPARE_OP               is-not
             2308  POP_JUMP_IF_FALSE  2288  'to 2288'

 L. 338      2312  LOAD_FAST                'vb'
             2314  DUP_TOP          
             2316  LOAD_ATTR                aspectsDefined
             2318  LOAD_FAST                'fact'
             2320  LOAD_ATTR                context
             2322  LOAD_ATTR                dimAspects
             2324  LOAD_DEREF               'xpCtx'
             2326  LOAD_ATTR                defaultDimensionAspects
             2328  CALL_FUNCTION_1       1  ''
             2330  INPLACE_OR       
             2332  ROT_TWO          
             2334  STORE_ATTR               aspectsDefined
             2336  JUMP_BACK          2288  'to 2288'
             2340  POP_BLOCK        
           2342_0  COME_FROM_LOOP     2282  '2282'

 L. 339      2342  LOAD_GLOBAL              coverAspectCoverFilterDims
             2344  LOAD_DEREF               'xpCtx'
             2346  LOAD_FAST                'vb'
             2348  LOAD_FAST                'var'
             2350  LOAD_ATTR                filterRelationships
             2352  CALL_FUNCTION_3       3  ''
             2354  POP_TOP          

 L. 340      2356  LOAD_FAST                'varHasNoVariableDependencies'
             2358  POP_JUMP_IF_FALSE  2380  'to 2380'

 L. 341      2362  LOAD_FAST                'facts'
             2364  LOAD_FAST                'vb'
             2366  LOAD_ATTR                aspectsDefined
             2368  LOAD_FAST                'vb'
             2370  LOAD_ATTR                aspectsCovered
             2372  BUILD_TUPLE_3         3 
             2374  LOAD_FAST                'cachedFilteredFacts'
             2376  LOAD_FAST                'varQname'
             2378  STORE_SUBSCR     
           2380_0  COME_FROM          2358  '2358'
           2380_1  COME_FROM          2036  '2036'

 L. 342      2380  LOAD_GLOBAL              bool
             2382  LOAD_FAST                'var'
             2384  LOAD_ATTR                fallbackValueProg
             2386  CALL_FUNCTION_1       1  ''
             2388  STORE_FAST               'considerFallback'

 L. 343      2390  LOAD_DEREF               'varSet'
             2392  LOAD_ATTR                implicitFiltering
             2394  LOAD_STR                 'true'
             2396  COMPARE_OP               ==
             2398  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 344      2402  LOAD_GLOBAL              any
             2404  LOAD_GENEXPR             '<code_object <genexpr>>'
             2406  LOAD_STR                 'evaluateVar.<locals>.<genexpr>'
             2408  MAKE_FUNCTION_0          ''
             2410  LOAD_DEREF               'xpCtx'
             2412  LOAD_ATTR                varBindings
             2414  LOAD_ATTR                values
             2416  CALL_FUNCTION_0       0  ''
             2418  GET_ITER         
             2420  CALL_FUNCTION_1       1  ''
             2422  CALL_FUNCTION_1       1  ''
             2424  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 345      2428  LOAD_GLOBAL              len
             2430  LOAD_FAST                'facts'
             2432  CALL_FUNCTION_1       1  ''
             2434  STORE_FAST               'factCount'

 L. 346      2436  LOAD_GLOBAL              implicitFilter
             2438  LOAD_DEREF               'xpCtx'
             2440  LOAD_FAST                'vb'
             2442  LOAD_FAST                'facts'
             2444  LOAD_FAST                'uncoveredAspectFacts'
             2446  CALL_FUNCTION_4       4  ''
             2448  STORE_FAST               'facts'

 L. 348      2450  LOAD_FAST                'considerFallback'
             2452  POP_JUMP_IF_FALSE  2664  'to 2664'
             2456  LOAD_FAST                'varHasNoVariableDependencies'
             2458  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 349      2462  LOAD_FAST                'factCount'
             2464  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 351      2468  LOAD_GLOBAL              len
             2470  LOAD_FAST                'facts'
             2472  CALL_FUNCTION_1       1  ''
             2474  LOAD_CONST               0
             2476  COMPARE_OP               >
             2478  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 352      2482  LOAD_GLOBAL              len
             2484  LOAD_DEREF               'xpCtx'
             2486  LOAD_ATTR                varBindings
             2488  CALL_FUNCTION_1       1  ''
             2490  LOAD_CONST               1
             2492  COMPARE_OP               >
             2494  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 353      2498  LOAD_GLOBAL              len
             2500  LOAD_FAST                'vb'
             2502  LOAD_ATTR                aspectsDefined
             2504  CALL_FUNCTION_1       1  ''
             2506  STORE_DEREF              'numVbAspectsdDefined'

 L. 354      2508  LOAD_CONST               True
             2510  STORE_FAST               'trial_for_svc_311_1_like'

 L. 355      2512  LOAD_FAST                'trial_for_svc_311_1_like'
             2514  POP_JUMP_IF_FALSE  2630  'to 2630'

 L. 356      2518  LOAD_CONST               0
             2520  STORE_FAST               'numNotCompletlyDefinedBindings'

 L. 357      2522  SETUP_LOOP         2614  'to 2614'
             2524  LOAD_DEREF               'xpCtx'
             2526  LOAD_ATTR                varBindings
             2528  LOAD_ATTR                values
             2530  CALL_FUNCTION_0       0  ''
             2532  GET_ITER         
             2534  FOR_ITER           2612  'to 2612'
             2536  STORE_FAST               '_vb'

 L. 358      2538  LOAD_GLOBAL              len
             2540  LOAD_FAST                '_vb'
             2542  LOAD_ATTR                aspectsDefined
             2544  CALL_FUNCTION_1       1  ''
             2546  STORE_FAST               'num_VbAspectsdDefined'

 L. 359      2548  LOAD_FAST                'num_VbAspectsdDefined'
             2550  LOAD_DEREF               'numVbAspectsdDefined'
             2552  COMPARE_OP               !=
             2554  POP_JUMP_IF_FALSE  2534  'to 2534'

 L. 360      2558  LOAD_DEREF               'numVbAspectsdDefined'
             2560  LOAD_FAST                'num_VbAspectsdDefined'
             2562  COMPARE_OP               >
             2564  POP_JUMP_IF_FALSE  2598  'to 2598'

 L. 361      2568  LOAD_FAST                '_vb'
             2570  LOAD_ATTR                aspectsDefined
             2572  LOAD_ATTR                issubset
             2574  LOAD_FAST                'vb'
             2576  LOAD_ATTR                aspectsDefined
             2578  CALL_FUNCTION_1       1  ''
             2580  POP_JUMP_IF_FALSE  2586  'to 2586'

 L. 362      2584  JUMP_FORWARD       2596  'to 2596'
             2586  ELSE                     '2596'

 L. 364      2586  LOAD_FAST                'numNotCompletlyDefinedBindings'
             2588  LOAD_CONST               1
             2590  INPLACE_ADD      
             2592  STORE_FAST               'numNotCompletlyDefinedBindings'

 L. 365      2594  BREAK_LOOP       
           2596_0  COME_FROM          2584  '2584'
             2596  JUMP_FORWARD       2608  'to 2608'
             2598  ELSE                     '2608'

 L. 367      2598  LOAD_FAST                'numNotCompletlyDefinedBindings'
             2600  LOAD_CONST               1
             2602  INPLACE_ADD      
             2604  STORE_FAST               'numNotCompletlyDefinedBindings'

 L. 368      2606  BREAK_LOOP       
           2608_0  COME_FROM          2596  '2596'
             2608  JUMP_BACK          2534  'to 2534'
             2612  POP_BLOCK        
           2614_0  COME_FROM_LOOP     2522  '2522'

 L. 369      2614  LOAD_FAST                'numNotCompletlyDefinedBindings'
             2616  LOAD_CONST               0
             2618  COMPARE_OP               ==
             2620  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 370      2624  LOAD_CONST               False
             2626  STORE_FAST               'considerFallback'
             2628  JUMP_FORWARD       2664  'to 2664'
             2630  ELSE                     '2664'

 L. 372      2630  LOAD_GLOBAL              all
             2632  LOAD_CLOSURE             'numVbAspectsdDefined'
             2634  BUILD_TUPLE_1         1 
             2636  LOAD_GENEXPR             '<code_object <genexpr>>'
             2638  LOAD_STR                 'evaluateVar.<locals>.<genexpr>'
             2640  MAKE_FUNCTION_8          'closure'
             2642  LOAD_DEREF               'xpCtx'
             2644  LOAD_ATTR                varBindings
             2646  LOAD_ATTR                values
             2648  CALL_FUNCTION_0       0  ''
             2650  GET_ITER         
             2652  CALL_FUNCTION_1       1  ''
             2654  CALL_FUNCTION_1       1  ''
             2656  POP_JUMP_IF_FALSE  2664  'to 2664'

 L. 373      2660  LOAD_CONST               False
             2662  STORE_FAST               'considerFallback'
           2664_0  COME_FROM          2656  '2656'
           2664_1  COME_FROM          2628  '2628'
           2664_2  COME_FROM          2620  '2620'
           2664_3  COME_FROM          2494  '2494'
           2664_4  COME_FROM          2478  '2478'
           2664_5  COME_FROM          2464  '2464'
           2664_6  COME_FROM          2458  '2458'
           2664_7  COME_FROM          2452  '2452'
           2664_8  COME_FROM          2424  '2424'
           2664_9  COME_FROM          2398  '2398'

 L. 375      2664  LOAD_FAST                'facts'
             2666  LOAD_FAST                'vb'
             2668  STORE_ATTR               facts

 L. 376      2670  LOAD_DEREF               'xpCtx'
             2672  LOAD_ATTR                formulaOptions
             2674  LOAD_ATTR                traceVariableFiltersResult
             2676  POP_JUMP_IF_FALSE  2712  'to 2712'

 L. 377      2680  LOAD_DEREF               'xpCtx'
             2682  LOAD_ATTR                modelXbrl
             2684  LOAD_ATTR                info
             2686  LOAD_STR                 'formula:trace'

 L. 378      2688  LOAD_GLOBAL              _
             2690  LOAD_STR                 'Fact Variable %(variable)s: filters result %(result)s'
             2692  CALL_FUNCTION_1       1  ''

 L. 379      2694  LOAD_FAST                'var'
             2696  LOAD_FAST                'varQname'
             2698  LOAD_GLOBAL              str
             2700  LOAD_FAST                'vb'
             2702  LOAD_ATTR                facts
             2704  CALL_FUNCTION_1       1  ''
             2706  LOAD_CONST               ('modelObject', 'variable', 'result')
             2708  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2710  POP_TOP          
           2712_0  COME_FROM          2676  '2676'

 L. 380      2712  LOAD_FAST                'considerFallback'
             2714  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 381      2718  LOAD_DEREF               'xpCtx'
             2720  LOAD_ATTR                evaluate
             2722  LOAD_FAST                'var'
             2724  LOAD_ATTR                fallbackValueProg
             2726  CALL_FUNCTION_1       1  ''
             2728  LOAD_FAST                'vb'
             2730  STORE_ATTR               values

 L. 382      2732  LOAD_DEREF               'xpCtx'
             2734  LOAD_ATTR                formulaOptions
             2736  LOAD_ATTR                traceVariableExpressionResult
             2738  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 383      2742  LOAD_DEREF               'xpCtx'
             2744  LOAD_ATTR                modelXbrl
             2746  LOAD_ATTR                info
             2748  LOAD_STR                 'formula:trace'

 L. 384      2750  LOAD_GLOBAL              _
             2752  LOAD_STR                 'Fact Variable %(variable)s: fallbackValue result %(result)s'
             2754  CALL_FUNCTION_1       1  ''

 L. 385      2756  LOAD_FAST                'var'
             2758  LOAD_FAST                'varQname'
             2760  LOAD_GLOBAL              str
             2762  LOAD_FAST                'vb'
             2764  LOAD_ATTR                values
             2766  CALL_FUNCTION_1       1  ''
             2768  LOAD_CONST               ('modelObject', 'variable', 'result')
             2770  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2772  POP_TOP          
             2774  JUMP_FORWARD       2916  'to 2916'
             2776  ELSE                     '2916'

 L. 386      2776  LOAD_FAST                'vb'
             2778  LOAD_ATTR                isGeneralVar
             2780  POP_JUMP_IF_FALSE  2892  'to 2892'

 L. 387      2784  LOAD_FAST                'var'
             2786  LOAD_ATTR                fromInstanceQnames
             2788  POP_JUMP_IF_FALSE  2814  'to 2814'

 L. 388      2792  LOAD_CLOSURE             'xpCtx'
             2794  BUILD_TUPLE_1         1 
             2796  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2798  LOAD_STR                 'evaluateVar.<locals>.<listcomp>'
             2800  MAKE_FUNCTION_8          'closure'

 L. 389      2802  LOAD_FAST                'var'
             2804  LOAD_ATTR                fromInstanceQnames
             2806  GET_ITER         
             2808  CALL_FUNCTION_1       1  ''
             2810  STORE_FAST               'contextItem'
             2812  JUMP_FORWARD       2824  'to 2824'
             2814  ELSE                     '2824'

 L. 394      2814  LOAD_DEREF               'xpCtx'
             2816  LOAD_ATTR                modelXbrl
             2818  LOAD_ATTR                modelDocument
             2820  LOAD_ATTR                xmlRootElement
             2822  STORE_FAST               'contextItem'
           2824_0  COME_FROM          2812  '2812'

 L. 395      2824  LOAD_DEREF               'xpCtx'
             2826  LOAD_ATTR                flattenSequence
             2828  LOAD_DEREF               'xpCtx'
             2830  LOAD_ATTR                evaluate
             2832  LOAD_FAST                'var'
             2834  LOAD_ATTR                selectProg
             2836  LOAD_FAST                'contextItem'
             2838  LOAD_CONST               ('contextItem',)
             2840  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2842  CALL_FUNCTION_1       1  ''
             2844  LOAD_FAST                'vb'
             2846  STORE_ATTR               values

 L. 396      2848  LOAD_DEREF               'xpCtx'
             2850  LOAD_ATTR                formulaOptions
             2852  LOAD_ATTR                traceVariableExpressionResult
             2854  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 397      2858  LOAD_DEREF               'xpCtx'
             2860  LOAD_ATTR                modelXbrl
             2862  LOAD_ATTR                info
             2864  LOAD_STR                 'formula:trace'

 L. 398      2866  LOAD_GLOBAL              _
             2868  LOAD_STR                 'General Variable %(variable)s: select result %(result)s'
             2870  CALL_FUNCTION_1       1  ''

 L. 399      2872  LOAD_FAST                'var'
             2874  LOAD_FAST                'varQname'
             2876  LOAD_GLOBAL              str
             2878  LOAD_FAST                'vb'
             2880  LOAD_ATTR                values
             2882  CALL_FUNCTION_1       1  ''
             2884  LOAD_CONST               ('modelObject', 'variable', 'result')
             2886  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2888  POP_TOP          
             2890  JUMP_FORWARD       2916  'to 2916'
             2892  ELSE                     '2916'

 L. 400      2892  LOAD_FAST                'vb'
             2894  LOAD_ATTR                isParameter
             2896  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 401      2900  LOAD_DEREF               'xpCtx'
             2902  LOAD_ATTR                inScopeVars
             2904  LOAD_ATTR                get
             2906  LOAD_FAST                'var'
             2908  LOAD_ATTR                parameterQname
             2910  CALL_FUNCTION_1       1  ''
             2912  LOAD_FAST                'vb'
             2914  STORE_ATTR               parameterValue
           2916_0  COME_FROM          2896  '2896'
           2916_1  COME_FROM          2890  '2890'
           2916_2  COME_FROM          2854  '2854'
           2916_3  COME_FROM          2774  '2774'
           2916_4  COME_FROM          2738  '2738'
           2916_5  COME_FROM          2714  '2714'

 L. 403      2916  LOAD_DEREF               'xpCtx'
             2918  LOAD_ATTR                varBindings
             2920  LOAD_ATTR                get
             2922  LOAD_FAST                'varQname'
             2924  CALL_FUNCTION_1       1  ''
             2926  STORE_FAST               'overriddenVarBinding'

 L. 404      2928  LOAD_FAST                'vb'
             2930  LOAD_DEREF               'xpCtx'
             2932  LOAD_ATTR                varBindings
             2934  LOAD_FAST                'varQname'
             2936  STORE_SUBSCR     

 L. 405      2938  SETUP_LOOP         3248  'to 3248'
             2942  LOAD_FAST                'vb'
             2944  LOAD_ATTR                evaluationResults
             2946  GET_ITER         
             2948  FOR_ITER           3246  'to 3246'
             2952  STORE_FAST               'evaluationResult'

 L. 406      2954  LOAD_DEREF               'xpCtx'
             2956  LOAD_ATTR                inScopeVars
             2958  LOAD_ATTR                get
             2960  LOAD_FAST                'varQname'
             2962  CALL_FUNCTION_1       1  ''
             2964  STORE_FAST               'overriddenInScopeVar'

 L. 407      2966  LOAD_FAST                'evaluationResult'
             2968  LOAD_DEREF               'xpCtx'
             2970  LOAD_ATTR                inScopeVars
             2972  LOAD_FAST                'varQname'
             2974  STORE_SUBSCR     

 L. 408      2976  BUILD_MAP_0           0 
             2978  STORE_FAST               'evaluationContributedUncoveredAspects'

 L. 409      2980  LOAD_FAST                'vb'
             2982  LOAD_ATTR                isFactVar
             2984  POP_JUMP_IF_FALSE  3080  'to 3080'
             2988  LOAD_FAST                'vb'
             2990  LOAD_ATTR                isFallback
             2992  UNARY_NOT        
             2994  POP_JUMP_IF_FALSE  3080  'to 3080'

 L. 411      2998  SETUP_LOOP         3080  'to 3080'
             3000  LOAD_FAST                'vb'
             3002  LOAD_ATTR                aspectsDefined
             3004  LOAD_FAST                'vb'
             3006  LOAD_ATTR                aspectsCovered
             3008  BINARY_OR        
             3010  GET_ITER         
             3012  FOR_ITER           3078  'to 3078'
             3014  STORE_FAST               'aspect'

 L. 412      3016  LOAD_FAST                'uncoveredAspectFacts'
             3018  LOAD_ATTR                get
             3020  LOAD_FAST                'aspect'
             3022  CALL_FUNCTION_1       1  ''
             3024  LOAD_CONST               None
             3026  COMPARE_OP               is
             3028  POP_JUMP_IF_FALSE  3012  'to 3012'

 L. 413      3032  LOAD_FAST                'uncoveredAspectFacts'
             3034  LOAD_ATTR                get
             3036  LOAD_FAST                'aspect'
             3038  LOAD_STR                 'none'
             3040  CALL_FUNCTION_2       2  ''
             3042  LOAD_FAST                'evaluationContributedUncoveredAspects'
             3044  LOAD_FAST                'aspect'
             3046  STORE_SUBSCR     

 L. 414      3048  LOAD_FAST                'vb'
             3050  LOAD_ATTR                hasAspectValueCovered
             3052  LOAD_FAST                'aspect'
             3054  CALL_FUNCTION_1       1  ''
             3056  POP_JUMP_IF_FALSE  3064  'to 3064'
             3060  LOAD_CONST               None
             3062  JUMP_FORWARD       3068  'to 3068'
             3064  ELSE                     '3068'
             3064  LOAD_FAST                'vb'
             3066  LOAD_ATTR                yieldedFact
           3068_0  COME_FROM          3062  '3062'
             3068  LOAD_FAST                'uncoveredAspectFacts'
             3070  LOAD_FAST                'aspect'
             3072  STORE_SUBSCR     
             3074  JUMP_BACK          3012  'to 3012'
             3078  POP_BLOCK        
           3080_0  COME_FROM_LOOP     2998  '2998'
           3080_1  COME_FROM          2994  '2994'
           3080_2  COME_FROM          2984  '2984'

 L. 415      3080  LOAD_DEREF               'xpCtx'
             3082  LOAD_ATTR                formulaOptions
             3084  LOAD_ATTR                traceVariableFiltersResult
             3086  POP_JUMP_IF_FALSE  3124  'to 3124'

 L. 416      3090  LOAD_DEREF               'xpCtx'
             3092  LOAD_ATTR                modelXbrl
             3094  LOAD_ATTR                info
             3096  LOAD_STR                 'formula:trace'

 L. 417      3098  LOAD_GLOBAL              _
             3100  LOAD_STR                 '%(variableType)s %(variable)s: bound value %(result)s'
             3102  CALL_FUNCTION_1       1  ''

 L. 418      3104  LOAD_FAST                'var'
             3106  LOAD_FAST                'vb'
             3108  LOAD_ATTR                resourceElementName
             3110  LOAD_FAST                'varQname'
             3112  LOAD_GLOBAL              str
             3114  LOAD_FAST                'evaluationResult'
             3116  CALL_FUNCTION_1       1  ''
             3118  LOAD_CONST               ('modelObject', 'variableType', 'variable', 'result')
             3120  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             3122  POP_TOP          
           3124_0  COME_FROM          3086  '3086'

 L. 419      3124  LOAD_DEREF               'xpCtx'
             3126  LOAD_ATTR                isRunTimeExceeded
             3128  POP_JUMP_IF_FALSE  3140  'to 3140'

 L. 419      3132  LOAD_GLOBAL              XPathContext
             3134  LOAD_ATTR                RunTimeExceededException
             3136  CALL_FUNCTION_0       0  ''
             3138  RAISE_VARARGS_1       1  ''
           3140_0  COME_FROM          3128  '3128'

 L. 420      3140  LOAD_GLOBAL              evaluateVar
             3142  LOAD_DEREF               'xpCtx'
             3144  LOAD_DEREF               'varSet'
             3146  LOAD_FAST                'varIndex'
             3148  LOAD_CONST               1
             3150  BINARY_ADD       
             3152  LOAD_FAST                'cachedFilteredFacts'
             3154  LOAD_FAST                'uncoveredAspectFacts'
             3156  CALL_FUNCTION_5       5  ''
             3158  POP_TOP          

 L. 421      3160  LOAD_DEREF               'xpCtx'
             3162  LOAD_ATTR                inScopeVars
             3164  LOAD_ATTR                pop
             3166  LOAD_FAST                'varQname'
             3168  CALL_FUNCTION_1       1  ''
             3170  POP_TOP          

 L. 422      3172  LOAD_FAST                'overriddenInScopeVar'
             3174  LOAD_CONST               None
             3176  COMPARE_OP               is-not
             3178  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 423      3182  LOAD_FAST                'overriddenInScopeVar'
             3184  LOAD_DEREF               'xpCtx'
             3186  LOAD_ATTR                inScopeVars
             3188  LOAD_FAST                'varQname'
             3190  STORE_SUBSCR     
           3192_0  COME_FROM          3178  '3178'

 L. 424      3192  SETUP_LOOP         3242  'to 3242'
             3194  LOAD_FAST                'evaluationContributedUncoveredAspects'
             3196  LOAD_ATTR                items
             3198  CALL_FUNCTION_0       0  ''
             3200  GET_ITER         
             3202  FOR_ITER           3240  'to 3240'
             3204  UNPACK_SEQUENCE_2     2 
             3206  STORE_FAST               'aspect'
             3208  STORE_FAST               'priorFact'

 L. 425      3210  LOAD_FAST                'priorFact'
             3212  LOAD_STR                 'none'
             3214  COMPARE_OP               ==
             3216  POP_JUMP_IF_FALSE  3228  'to 3228'

 L. 426      3220  LOAD_FAST                'uncoveredAspectFacts'
             3222  LOAD_FAST                'aspect'
             3224  DELETE_SUBSCR    
             3226  JUMP_FORWARD       3236  'to 3236'
             3228  ELSE                     '3236'

 L. 428      3228  LOAD_FAST                'priorFact'
             3230  LOAD_FAST                'uncoveredAspectFacts'
             3232  LOAD_FAST                'aspect'
             3234  STORE_SUBSCR     
           3236_0  COME_FROM          3226  '3226'
             3236  JUMP_BACK          3202  'to 3202'
             3240  POP_BLOCK        
           3242_0  COME_FROM_LOOP     3192  '3192'
             3242  JUMP_BACK          2948  'to 2948'
             3246  POP_BLOCK        
           3248_0  COME_FROM_LOOP     2938  '2938'

 L. 429      3248  LOAD_DEREF               'xpCtx'
             3250  LOAD_ATTR                varBindings
             3252  LOAD_ATTR                pop
             3254  LOAD_FAST                'varQname'
             3256  CALL_FUNCTION_1       1  ''
             3258  POP_TOP          

 L. 430      3260  LOAD_FAST                'vb'
             3262  LOAD_ATTR                close
             3264  CALL_FUNCTION_0       0  ''
             3266  POP_TOP          

 L. 431      3268  LOAD_FAST                'overriddenVarBinding'
             3270  LOAD_CONST               None
             3272  COMPARE_OP               is-not
             3274  POP_JUMP_IF_FALSE  3288  'to 3288'

 L. 432      3278  LOAD_FAST                'overriddenVarBinding'
             3280  LOAD_DEREF               'xpCtx'
             3282  LOAD_ATTR                varBindings
             3284  LOAD_FAST                'varQname'
             3286  STORE_SUBSCR     
           3288_0  COME_FROM          3274  '3274'
           3288_1  COME_FROM          1880  '1880'

Parse error at or near `JUMP_FORWARD' instruction at offset 1880


def checkVarFilterInfo(var):
    try:
        ff = var.filterInfo
        return
    except:
        pass

    var.noComplHandledFilterRels = []
    var.complHandledFilterRels = []
    var.unHandledFilterRels = []
    for varFilterRel in var.filterRelationships:
        _filter = varFilterRel.toModelObject
        handled = False
        _filter = varFilterRel.toModelObject
        if isinstance(_filter, ModelTypedDimension):
            try:
                tmp = _filter.dimQname
                if tmp:
                    if not _filter.test:
                        if varFilterRel.isComplemented:
                            var.complHandledFilterRels.append((varFilterRel, tmp))
                        else:
                            var.noComplHandledFilterRels.append((varFilterRel, tmp))
                        handled = True
            except:
                pass

            if not handled:
                var.unHandledFilterRels.append(varFilterRel)

    if len(var.noComplHandledFilterRels) > 0 or len(var.complHandledFilterRels) > 0:
        var.filterInfo = True
    else:
        var.filterInfo = False


def checkVarSetFilterInfo(varSet):
    try:
        ff = varSet.filterInfo
        return
    except:
        pass

    varSet.noComplHandledFilterRels = []
    varSet.complHandledFilterRels = []
    varSet.unHandledFilterRels = []
    for varFilterRel in varSet.groupFilterRelationships:
        _filter = varFilterRel.toModelObject
        handled = False
        _filter = varFilterRel.toModelObject
        if isinstance(_filter, ModelTypedDimension):
            try:
                tmp = _filter.dimQname
                if tmp:
                    if not _filter.test:
                        if varFilterRel.isComplemented:
                            varSet.complHandledFilterRels.append((varFilterRel, tmp))
                        else:
                            varSet.noComplHandledFilterRels.append((varFilterRel, tmp))
                        handled = True
            except:
                pass

            if not handled:
                varSet.unHandledFilterRels.append(varFilterRel)

    if len(varSet.noComplHandledFilterRels) > 0 or len(varSet.complHandledFilterRels) > 0:
        varSet.filterInfo = True
    else:
        varSet.filterInfo = False


def trialFilterFacts(xpCtx, vb, facts, filterRelationships, filterType, var=None, varSet=None):
    typeLbl = filterType + ' ' if filterType else ''
    orFilter = filterType == 'or'
    groupFilter = filterType == 'group'
    if orFilter:
        factSet = set()
    filterInfo = None
    if filterType is None:
        if var is not None:
            filterInfo = var.filterInfo
            noComplHandledFilterRels = var.noComplHandledFilterRels
            complHandledFilterRels = var.complHandledFilterRels
            unHandledFilterRels = var.unHandledFilterRels
    if groupFilter:
        if varSet is not None:
            filterInfo = varSet.filterInfo
            noComplHandledFilterRels = varSet.noComplHandledFilterRels
            complHandledFilterRels = varSet.complHandledFilterRels
            unHandledFilterRels = varSet.unHandledFilterRels
    if filterInfo is not None:
        if filterInfo and len(noComplHandledFilterRels) > 0:
            for varFilterRel, dimQname in noComplHandledFilterRels:
                _filter = varFilterRel.toModelObject
                if varFilterRel.isCovered:
                    vb.aspectsCovered |= _filter.aspectsCovered(vb)

            filterRelationships = unHandledFilterRels
            outFacts = set()
            for fact in facts:
                if fact.isItem:
                    for varFilterRel, dimQname in noComplHandledFilterRels:
                        dim = fact.context.qnameDims.get(dimQname)
                        if dim is not None:
                            outFacts.add(fact)

            facts = outFacts
            if len(facts) == 0:
                return facts
    for varFilterRel in filterRelationships:
        _filter = varFilterRel.toModelObject
        if isinstance(_filter, ModelFilter):
            if filterType is None:
                if len(facts) == 0:
                    pass
            else:
                result = _filter.filterxpCtxvbfactsvarFilterRel.isComplemented
                if xpCtx.formulaOptions.traceVariableFilterWinnowing:
                    allFacts = ''
                    for fact in facts:
                        allFacts += str(fact)

                    (
                     xpCtx.modelXbrl.info('formula:trace', (_('Fact Variable %(variable)s %(filterType)s %(filter)s filter %(xlinkLabel)s passes %(factCount)s facts %(allFacts)s')),
                       modelObject=(vb.var),
                       variable=(vb.qname),
                       filterType=typeLbl,
                       filter=(_filter.localName),
                       xlinkLabel=(_filter.xlinkLabel),
                       factCount=(len(result)),
                       allFacts=allFacts),)
                if orFilter:
                    factSet |= result
                else:
                    facts = result
            if not groupFilter and varFilterRel.isCovered:
                vb.aspectsCovered |= _filter.aspectsCovered(vb)

    if orFilter:
        facts = factSet
    if filterInfo is not None:
        if filterInfo:
            if len(complHandledFilterRels) > 0:
                for varFilterRel, dimQname in complHandledFilterRels:
                    _filter = varFilterRel.toModelObject
                    if varFilterRel.isCovered:
                        vb.aspectsCovered |= _filter.aspectsCovered(vb)

                outFacts = set()
                for fact in facts:
                    if fact.isItem:
                        for varFilterRel, dimQname in complHandledFilterRels:
                            dim = fact.context.qnameDims.get(dimQname)
                            if dim is None:
                                outFacts.add(fact)

                facts = outFacts
    return facts


def filterFacts(xpCtx, vb, facts, filterRelationships, filterType):
    typeLbl = filterType + ' ' if filterType else ''
    orFilter = filterType == 'or'
    groupFilter = filterType == 'group'
    if orFilter:
        factSet = set()
    for varFilterRel in filterRelationships:
        _filter = varFilterRel.toModelObject
        if isinstance(_filter, ModelFilter):
            result = _filter.filterxpCtxvbfactsvarFilterRel.isComplemented
            if xpCtx.formulaOptions.traceVariableFilterWinnowing:
                (
                 xpCtx.modelXbrl.info('formula:trace', (_('Fact Variable %(variable)s %(filterType)s %(filter)s filter %(xlinkLabel)s passes %(factCount)s facts')),
                   modelObject=(vb.var),
                   variable=(vb.qname),
                   filterType=typeLbl,
                   filter=(_filter.localName),
                   xlinkLabel=(_filter.xlinkLabel),
                   factCount=(len(result))),)
            if orFilter:
                factSet |= result
            else:
                facts = result
            if not groupFilter and varFilterRel.isCovered:
                vb.aspectsCovered |= _filter.aspectsCovered(vb)

    if orFilter:
        return factSet
    else:
        return facts


def coverAspectCoverFilterDims(xpCtx, vb, filterRelationships):
    for varFilterRel in filterRelationships:
        _filter = varFilterRel.toModelObject
        if isinstance(_filter, ModelAspectCover):
            if varFilterRel.isCovered:
                vb.aspectsCovered |= _filter.dimAspectsCovered(vb)
        else:
            if isinstance(_filter, ModelBooleanFilter):
                if varFilterRel.isCovered:
                    coverAspectCoverFilterDims(xpCtx, vb, _filter.filterRelationships)


def isVbTupleWithOnlyAnUncoveredDimension(xpCtx, vb, facts):
    vbUncoveredAspects = (vb.aspectsDefined | xpCtx.dimensionsAspectUniverse) - vb.aspectsCovered - {Aspect.DIMENSIONS}
    return vbUncoveredAspects and all(isinstance(a, QName) for a in vbUncoveredAspects) and all(f.isTuple for f in facts)


def implicitFilter(xpCtx, vb, facts, uncoveredAspectFacts):
    aspects = (vb.aspectsDefined | _DICT_SET(uncoveredAspectFacts.keys())) - vb.aspectsCovered - {Aspect.DIMENSIONS}
    if not aspects:
        if isVbTupleWithOnlyAnUncoveredDimension(xpCtx, vb, facts):
            return []
        return facts
    else:
        if len(xpCtx.varBindings) == 1:
            f = uncoveredAspectFacts.get(Aspect.DIMENSIONS)
            if isinstance(f, ModelFact):
                if f.isTuple:
                    if all(f is None for a, f in uncoveredAspectFacts.items() if a != Aspect.DIMENSIONS):
                        if isVbTupleWithOnlyAnUncoveredDimension(xpCtx, next(iter(xpCtx.varBindings.values())), (f,)):
                            return []
                        return facts
        else:
            if xpCtx.formulaOptions.traceVariableFilterWinnowing:
                _facts = facts
                for aspect in aspects:
                    if uncoveredAspectFacts.get(aspect, 'none') is not None:
                        _facts = [fact for fact in _facts if aspectMatchesxpCtxuncoveredAspectFacts.get(aspect)factaspect]
                        a = str(aspect) if isinstance(aspect, QName) else Aspect.label[aspect]
                        xpCtx.modelXbrl.info('formula:trace', (_('Fact Variable %(variable)s implicit filter %(aspect)s passes %(factCount)s facts')),
                          modelObject=(vb.var),
                          variable=(vb.qname),
                          aspect=a,
                          factCount=(len(facts)))
                        if len(_facts) == 0:
                            break

            else:
                testableAspectFacts = [(aspect, uncoveredAspectFacts.get(aspect)) for aspect in aspects if uncoveredAspectFacts.get(aspect, 'none') is not None]
                if testableAspectFacts:
                    _facts = [fact for fact in facts if all(aspectMatchesxpCtxuncoveredAspectFactfactaspect for aspect, uncoveredAspectFact in testableAspectFacts)]
                else:
                    _facts = facts
        return _facts


def aspectsMatch(xpCtx, fact1, fact2, aspects):
    return all(aspectMatchesxpCtxfact1fact2aspect for aspect in aspects)


def aspectMatches(xpCtx, fact1, fact2, aspect):
    if fact1 is None:
        return False
    else:
        if aspect == 1:
            return fact2 is not None and fact1.modelXbrl != fact2.modelXbrl or fact1.parentElement == fact2.parentElement
        elif aspect == 2:
            return fact2 is not None and fact1.qname == fact2.qname
        elif fact1.isTuple or fact2.isTuple:
            return fact1.isTuple and fact2.isTuple
        elif aspect == 5:
            u1 = fact1.unit
            u2 = fact2.unit if fact2 is not None else None
            if u1 is not None:
                return u1.isEqualTo(u2)
            else:
                return u2 is None
        else:
            c1 = fact1.context
            c2 = fact2.context if fact2 is not None else None
            if c1 is None or c2 is None and aspect != 10:
                return False
            if c1 is c2:
                return True
            if not isinstance(aspect, QName):
                if aspect == 4:
                    return c1.isPeriodEqualTo(c2)
                else:
                    if aspect == 3:
                        return c1.isEntityIdentifierEqualTo(c2)
                    if aspect == 6:
                        return XbrlUtil.nodesCorrespond((fact1.modelXbrl), (c1.segment), (c2.segment), dts2=(fact2.modelXbrl))
                    if aspect == 7:
                        return XbrlUtil.nodesCorrespond((fact1.modelXbrl), (c1.scenario), (c2.scenario), dts2=(fact2.modelXbrl))
                if aspect == 8 or aspect == 9:
                    nXs1 = c1.nonDimValues(aspect)
                    nXs2 = c2.nonDimValues(aspect)
                    lXs1 = len(nXs1)
                    lXs2 = len(nXs2)
                    if lXs1 != lXs2:
                        return False
                    else:
                        if lXs1 > 0:
                            for i in range(lXs1):
                                if not XbrlUtil.nodesCorrespond((fact1.modelXbrl), (nXs1[i]), (nXs2[i]), dts2=(fact2.modelXbrl)):
                                    return False

                        return True
            else:
                dimValue1 = c1.dimValue(aspect)
                if c2 is None:
                    if dimValue1 is None:
                        return True
                    else:
                        return False
                dimValue2 = c2.dimValue(aspect)
                if isinstance(dimValue1, ModelDimensionValue):
                    if dimValue1.isExplicit:
                        if isinstance(dimValue2, QName):
                            if dimValue1.memberQname != dimValue2:
                                return False
                        else:
                            if isinstance(dimValue2, (ModelDimensionValue, DimValuePrototype)):
                                if dimValue2.isTyped:
                                    return False
                                if dimValue1.memberQname != dimValue2.memberQname:
                                    return False
                            else:
                                if dimValue2 is None:
                                    return False
                    else:
                        if dimValue1.isTyped:
                            if isinstance(dimValue2, QName):
                                return False
                            if isinstance(dimValue2, (ModelDimensionValue, DimValuePrototype)):
                                if dimValue2.isExplicit:
                                    return False
                            else:
                                if dimValue1.dimension.typedDomainElement in xpCtx.modelXbrl.modelFormulaEqualityDefinitions:
                                    equalityDefinition = xpCtx.modelXbrl.modelFormulaEqualityDefinitions[dimValue1.dimension.typedDomainElement]
                                    return equalityDefinition.evalTest(xpCtx, fact1, fact2)
                                else:
                                    return XbrlUtil.nodesCorrespond((fact1.modelXbrl), (dimValue1.typedMember), (dimValue2.typedMember), dts2=(fact2.modelXbrl)) or False
                        else:
                            if dimValue2 is None:
                                return False
                else:
                    if isinstance(dimValue1, QName):
                        if isinstance(dimValue2, QName):
                            if fact1.modelXbrl == fact2.modelXbrl and dimValue1 != dimValue2:
                                return False
                        else:
                            if isinstance(dimValue2, (ModelDimensionValue, DimValuePrototype)):
                                if dimValue2.isTyped:
                                    return False
                                if dimValue1 != dimValue2.memberQname:
                                    return False
                            else:
                                if dimValue2 is None and fact1.modelXbrl == fact2.modelXbrl:
                                    return False
                    elif dimValue1 is None:
                        if isinstance(dimValue2, QName):
                            if fact1.modelXbrl == fact2.modelXbrl:
                                return False
                        elif dimValue2 is not None:
                            return False
        return True


def factsPartitions(xpCtx, facts, aspects):
    factsPartitions = []
    for fact in facts:
        matched = False
        for partition in factsPartitions:
            if aspectsMatchxpCtxfactpartition[0]aspects:
                partition.append(fact)
                matched = True
                break

        if not matched:
            factsPartitions.append([fact])

    return factsPartitions


def evaluationIsUnnecessary(thisEval, xpCtx):
    otherEvals = xpCtx.evaluations
    if otherEvals:
        otherEvalHashDicts = xpCtx.evaluationHashDicts
        if all(e is None for e in thisEval.values()):
            return True
        otherEvalSets = [otherEvalHashDicts[vQn][hash(vBoundFact)] for vQn, vBoundFact in thisEval.items() if vBoundFact is not None if vQn in otherEvalHashDicts if hash(vBoundFact) in otherEvalHashDicts[vQn]]
        if otherEvalSets:
            matchingEvals = [otherEvals[i] for i in (set.intersection)(*otherEvalSets)]
        else:
            matchingEvals = otherEvals
        varBindings = xpCtx.varBindings
        vQnDependentOnOtherVarFallenBackButBoundInOtherEval = set(vQn for vQn, vBoundFact in thisEval.items() if vBoundFact is not None if any(varBindings[varRefQn].isFallback and any(m[varRefQn] is not None for m in matchingEvals) for varRefQn in varBindings[vQn].var.variableRefs()))
        return any(all([vBoundFact == matchingEval[vQn] for vQn, vBoundFact in thisEval.items() if vBoundFact is not None if vQn not in vQnDependentOnOtherVarFallenBackButBoundInOtherEval]) for matchingEval in matchingEvals)
    else:
        return False


def produceOutputFact(xpCtx, formula, result):
    priorErrorCount = len(xpCtx.modelXbrl.errors)
    isTuple = isinstance(formula, ModelTuple)
    conceptQname = formulaAspectValuexpCtxformulaAspect.CONCEPT'xbrlfe:missingConceptRule'
    if isinstance(conceptQname, VariableBindingError):
        xpCtx.modelXbrl.error((conceptQname.err), (_('Formula %(label)s concept: %(concept)s')),
          modelObject=formula,
          label=(formula.logLabel()),
          concept=(conceptQname.msg))
        modelConcept = None
    else:
        modelConcept = xpCtx.modelXbrl.qnameConcepts[conceptQname]
    if modelConcept is None or (not modelConcept.isTuple if isTuple else not modelConcept.isItem):
        xpCtx.modelXbrl.error('xbrlfe:missingConceptRule', (_('Formula %(label)s concept %(concept)s is not a %(element)s')),
          modelObject=formula,
          label=(formula.logLabel()),
          concept=conceptQname,
          element=(formula.localName))
    outputLocation = formulaAspectValuexpCtxformulaAspect.LOCATION_RULENone
    entityIdentScheme = isTuple or formulaAspectValuexpCtxformulaAspect.SCHEME'xbrlfe:missingEntityIdentifierRule'
    if isinstance(entityIdentScheme, VariableBindingError):
        xpCtx.modelXbrl.error((str(entityIdentScheme)), (_('Formula %(label)s entity identifier scheme: %(scheme)s')),
          modelObject=formula,
          label=(formula.logLabel()),
          scheme=(entityIdentScheme.msg))
        entityIdentValue = None
    else:
        entityIdentValue = formulaAspectValuexpCtxformulaAspect.VALUE'xbrlfe:missingEntityIdentifierRule'
    if isinstance(entityIdentValue, VariableBindingError):
        xpCtx.modelXbrl.error((str(entityIdentScheme)), (_('Formula %(label)s entity identifier value: %(entityIdentifier)s')),
          modelObject=formula,
          label=(formula.logLabel()),
          entityIdentifier=(entityIdentValue.msg))
    periodType = formulaAspectValuexpCtxformulaAspect.PERIOD_TYPE'xbrlfe:missingPeriodRule'
    periodStart = None
    periodEndInstant = None
    if isinstance(periodType, VariableBindingError):
        xpCtx.modelXbrl.error((str(periodType)), (_('Formula %(label)s period type: %(periodType)s')),
          modelObject=formula,
          label=(formula.logLabel()),
          periodType=(periodType.msg))
    else:
        if periodType == 'instant':
            periodEndInstant = formulaAspectValuexpCtxformulaAspect.INSTANT'xbrlfe:missingPeriodRule'
            if isinstance(periodEndInstant, VariableBindingError):
                xpCtx.modelXbrl.error((str(periodEndInstant)), (_('Formula %(label)s period end: %(period)s')),
                  modelObject=formula,
                  label=(formula.logLabel()),
                  period=(periodEndInstant.msg))
        else:
            if periodType == 'duration':
                periodStart = formulaAspectValuexpCtxformulaAspect.START'xbrlfe:missingPeriodRule'
                if isinstance(periodStart, VariableBindingError):
                    xpCtx.modelXbrl.error((str(periodStart)), (_('Formula %(label)s period start: %(period)s')),
                      modelObject=formula,
                      label=(formula.logLabel()),
                      period=(periodStart.msg))
                periodEndInstant = formulaAspectValuexpCtxformulaAspect.END'xbrlfe:missingPeriodRule'
                if isinstance(periodEndInstant, VariableBindingError):
                    xpCtx.modelXbrl.error((str(periodEndInstant)), (_('Formula %(label)s period end: %(period)s')),
                      modelObject=formula,
                      label=(formula.logLabel()),
                      period=(periodEndInstant.msg))
            if modelConcept is not None:
                if modelConcept.isNumeric:
                    unitSource = formulaAspectValuexpCtxformulaAspect.UNIT_MEASURESNone
                    multDivBy = formulaAspectValuexpCtxformulaAspect.MULTIPLY_BY'xbrlfe:missingUnitRule'
                    if isinstance(multDivBy, VariableBindingError):
                        xpCtx.modelXbrl.error((str(multDivBy) if isinstance(multDivBy, VariableBindingError) else 'xbrlfe:missingUnitRule'), (_('Formula %(label)s unit: %(unit)s')),
                          modelObject=formula,
                          label=(formula.logLabel()),
                          unit=(multDivBy.msg))
                        multiplyBy = ()
                        divideBy = ()
                    else:
                        divMultBy = formulaAspectValuexpCtxformulaAspect.DIVIDE_BY'xbrlfe:missingUnitRule'
                        if isinstance(divMultBy, VariableBindingError):
                            xpCtx.modelXbrl.error((str(multDivBy) if isinstance(divMultBy, VariableBindingError) else 'xbrlfe:missingUnitRule'), (_('Formula %(label)s unit: %(unit)s')),
                              modelObject=formula,
                              label=(formula.logLabel()),
                              unit=(divMultBy.msg))
                            multiplyBy = ()
                            divideBy = ()
                        else:
                            multiplyBy = unitSource[0] + multDivBy[0] + divMultBy[1]
                            divideBy = unitSource[1] + multDivBy[1] + divMultBy[0]
                            lookForCommonUnits = True
                            while lookForCommonUnits:
                                lookForCommonUnits = False
                                for commonUnit in multiplyBy:
                                    if commonUnit in divideBy:
                                        multiplyBy = tuple(u for u in multiplyBy if u != commonUnit)
                                        divideBy = tuple(u for u in divideBy if u != commonUnit)
                                        lookForCommonUnits = True
                                        break

                            if len(multiplyBy) == 0:
                                if Aspect.MULTIPLY_BY not in formula.aspectValues:
                                    if Aspect.MULTIPLY_BY not in formula.aspectProgs:
                                        if Aspect.DIVIDE_BY not in formula.aspectValues:
                                            if Aspect.DIVIDE_BY not in formula.aspectProgs:
                                                xpCtx.modelXbrl.error('xbrlfe:missingUnitRule', (_('Formula %(label)s')),
                                                  modelObject=formula,
                                                  label=(formula.logLabel()))
                                multiplyBy = (
                                 XbrlConst.qnXbrliPure,)
            segOCCs = []
            scenOCCs = []
            if formula.aspectModel == 'dimensional':
                dimAspects = {}
                dimQnames = formulaAspectValuexpCtxformulaAspect.DIMENSIONSNone
                if dimQnames:
                    for dimQname in dimQnames:
                        dimConcept = xpCtx.modelXbrl.qnameConcepts[dimQname]
                        dimErr = 'xbrlfe:missing{0}DimensionRule'.format('typed' if (dimConcept is not None and dimConcept.isTypedDimension) else 'explicit')
                        dimValue = formulaAspectValuexpCtxformuladimQnamedimErr
                        if isinstance(dimValue, VariableBindingError):
                            xpCtx.modelXbrl.error(dimErr, (_('Formula %(label)s dimension %(dimension)s: %(value)s')),
                              modelObject=formula,
                              label=(formula.logLabel()),
                              dimension=dimQname,
                              value=(dimValue.msg))
                        else:
                            if dimConcept.isTypedDimension:
                                if isinstance(dimValue, list):
                                    if len(dimValue) != 1 or not isinstance(dimValue[0], ModelObject):
                                        xpCtx.modelXbrl.error('xbrlfe:wrongXpathResultForTypedDimensionRule', (_('Formula %(label)s dimension %(dimension)s value is not a node: %(value)s')),
                                          modelObject=formula,
                                          label=(formula.logLabel()),
                                          dimension=dimQname,
                                          value=dimValue)
                                    else:
                                        dimValue = dimValue[0]
                                dimAspects[dimQname] = dimValue
                            elif dimValue is not None:
                                if xpCtx.modelXbrl.qnameDimensionDefaults.get(dimQname) != dimValue:
                                    dimAspects[dimQname] = dimValue

                segOCCs = formulaAspectValuexpCtxformulaAspect.NON_XDT_SEGMENTNone
                scenOCCs = formulaAspectValuexpCtxformulaAspect.NON_XDT_SCENARIONone
                for occElt in xpCtx.flattenSequence((segOCCs, scenOCCs)):
                    if isinstance(occElt, ModelObject) and occElt.namespaceURI == XbrlConst.xbrldi:
                        xpCtx.modelXbrl.error('xbrlfe:badSubsequentOCCValue', (_('Formula %(label)s OCC element %(occ)s covers a dimensional aspect')),
                          modelObject=(
                         formula, occElt),
                          label=(formula.logLabel()),
                          occ=(occElt.elementQname))

            else:
                dimAspects = None
                segOCCs = formulaAspectValuexpCtxformulaAspect.COMPLETE_SEGMENTNone
                scenOCCs = formulaAspectValuexpCtxformulaAspect.COMPLETE_SCENARIONone
            if priorErrorCount < len(xpCtx.modelXbrl.errors):
                return
        outputInstanceQname = formula.outputInstanceQname
        outputXbrlInstance = xpCtx.inScopeVars[outputInstanceQname]
        xbrlElt = outputXbrlInstance.modelDocument.xmlRootElement
        newFact = None
        if isTuple:
            newFact = outputXbrlInstance.createFact(conceptQname, parent=outputLocation, afterSibling=(xpCtx.outputLastFact.get(outputInstanceQname)))
        else:
            prevCntx = outputXbrlInstance.matchContext(entityIdentScheme, entityIdentValue, periodType, periodStart, periodEndInstant, dimAspects, segOCCs, scenOCCs)
            if prevCntx is not None:
                cntxId = prevCntx.id
                newCntxElt = prevCntx
            else:
                newCntxElt = outputXbrlInstance.createContext(entityIdentScheme, entityIdentValue, periodType,
                  periodStart, periodEndInstant, conceptQname, dimAspects, segOCCs, scenOCCs, afterSibling=(xpCtx.outputLastContext.get(outputInstanceQname)),
                  beforeSibling=(xpCtx.outputFirstFact.get(outputInstanceQname)))
                cntxId = newCntxElt.id
                xpCtx.outputLastContext[outputInstanceQname] = newCntxElt
    if modelConcept.isNumeric:
        prevUnit = outputXbrlInstance.matchUnit(multiplyBy, divideBy)
        if prevUnit is not None:
            unitId = prevUnit.id
            newUnitElt = prevUnit
        else:
            newUnitElt = outputXbrlInstance.createUnit(multiplyBy, divideBy, afterSibling=(xpCtx.outputLastUnit.get(outputInstanceQname)),
              beforeSibling=(xpCtx.outputFirstFact.get(outputInstanceQname)))
            unitId = newUnitElt.id
            xpCtx.outputLastUnit[outputInstanceQname] = newUnitElt
        attrs = [
         (
          'contextRef', cntxId)]
        precision = None
        decimals = None
        if modelConcept.isNumeric:
            attrs.append(('unitRef', unitId))
        value = formula.evaluate(xpCtx)
        valueSeqLen = len(value)
        if valueSeqLen > 1:
            xpCtx.modelXbrl.error('xbrlfe:nonSingletonOutputValue', (_('Formula %(label)s value is a sequence of length %(valueSequenceLength)s')),
              modelObject=formula,
              label=(formula.logLabel()),
              valueSequenceLength=valueSeqLen)
        else:
            if valueSeqLen == 0:
                attrs.append((XbrlConst.qnXsiNil, 'true'))
                v = None
            else:
                if modelConcept.isNumeric:
                    if not modelConcept.isFraction:
                        if formula.hasDecimals:
                            decimals = formula.evaluateRule(xpCtx, Aspect.DECIMALS)
                            attrs.append(('decimals', decimals))
                        else:
                            if formula.hasPrecision:
                                precision = formula.evaluateRule(xpCtx, Aspect.PRECISION)
                            else:
                                precision = 0
                            attrs.append(('precision', precision))
                x = value[0]
                if isinstance(x, float):
                    if isnan(x) or precision and (isinf(precision) or precision == 0) or decimals and isinf(decimals):
                        v = xsString(xpCtx, None, x)
                    else:
                        if decimals is not None:
                            v = '%.*f' % (int(decimals), x)
                        else:
                            if precision is not None and precision != 0:
                                a = fabs(x)
                                log = log10(a) if a != 0 else 0
                                v = '%.*f' % (int(precision) - int(log) - (1 if a >= 1 else 0), x)
                else:
                    v = xsString(xpCtx, None, x)
    elif isinstance(x, Decimal):
        if x.is_nan() or precision and (isinf(precision) or precision == 0) or decimals and isinf(decimals):
            v = xsString(xpCtx, None, x)
        else:
            if decimals is not None:
                v = '%.*f' % (int(decimals), x)
            elif precision is not None:
                if precision != 0:
                    a = x.copy_abs()
                    log = a.log10() if a != 0 else 0
                    v = '%.*f' % (int(precision) - int(log) - (1 if a >= 1 else 0), x)
            else:
                v = xsString(xpCtx, None, x)
    else:
        if isinstance(x, QName):
            v = XmlUtil.addQnameValue(xbrlElt, x)
        else:
            if isinstance(x, datetime.datetime):
                v = XmlUtil.dateunionValue(x)
            else:
                v = xsString(xpCtx, None, x)
            newFact = outputXbrlInstance.createFact(conceptQname, attributes=attrs, text=v, parent=outputLocation,
              afterSibling=(xpCtx.outputLastFact.get(outputInstanceQname)))
        if newFact is not None:
            xpCtx.outputLastFact[outputInstanceQname] = newFact
            if outputInstanceQname not in xpCtx.outputFirstFact:
                xpCtx.outputFirstFact[outputInstanceQname] = newFact
        return newFact


def formulaAspectValue(xpCtx, formula, aspect, srcMissingErr):
    ruleValue = formula.evaluateRule(xpCtx, aspect)
    if ruleValue is not None:
        if aspect in (Aspect.CONCEPT,
         Aspect.VALUE, Aspect.SCHEME,
         Aspect.PERIOD_TYPE, Aspect.START, Aspect.END, Aspect.INSTANT):
            return ruleValue
        if isinstance(aspect, QName):
            if ruleValue != XbrlConst.qnFormulaDimensionSAV:
                return ruleValue
    sourceQname = formula.source(aspect)
    formulaUncovered = sourceQname == XbrlConst.qnFormulaUncovered
    if aspect == Aspect.LOCATION_RULE:
        if sourceQname is None:
            return xpCtx.inScopeVars[formula.outputInstanceQname].modelDocument.xmlRootElement
    if aspect == Aspect.DIMENSIONS:
        if formulaUncovered:
            aspectSourceValue = set()
        else:
            if srcMissingErr is None:
                aspectSourceValue = None
            else:
                if formulaUncovered:
                    if isinstance(aspect, QName):
                        aspectSourceValue = None
                    else:
                        aspectSourceValue = xbrlfe_undefinedSAV
                else:
                    aspectSourceValue = VariableBindingError(srcMissingErr, _('neither source {0}, nor an aspect rule, were found.').format(sourceQname if sourceQname else ''))
    else:
        for vb in xpCtx.varBindings.values():
            if vb.isFactVar and not vb.isFallback:
                if aspect == Aspect.DIMENSIONS:
                    if formulaUncovered:
                        aspectSourceValue |= vb.aspectValue(aspect)
                if formulaUncovered:
                    if vb.hasAspectValueUncovered(aspect):
                        aspectSourceValue = vb.aspectValue(aspect)
                        break
                if sourceQname == vb.qname:
                    if not vb.isBindAsSequence or vb.hasAspectValueUncovered(aspect):
                        aspectSourceValue = vb.aspectValue(aspect)
                    else:
                        aspectSourceValue = VariableBindingError('xbrlfe:sequenceSAVConflicts', _("source, {0}, contains the QName of a fact variable that binds as a sequence where that fact's aspect rule covers this filtered aspect").format(sourceQname))
                    break
            else:
                if aspect == Aspect.LOCATION_RULE:
                    if sourceQname == vb.qname:
                        aspectSourceValue = vb.aspectValue(aspect)
                        break

        if aspect in (Aspect.CONCEPT, Aspect.LOCATION_RULE,
         Aspect.VALUE, Aspect.SCHEME,
         Aspect.PERIOD_TYPE, Aspect.START, Aspect.END, Aspect.INSTANT) or isinstance(aspect, QName):
            return aspectSourceValue
        if aspect == Aspect.UNIT_MEASURES:
            augment = formula.evaluateRule(xpCtx, Aspect.AUGMENT)
            if aspectSourceValue:
                if not augment or augment == 'true':
                    return aspectSourceValue
            return ((), ())
        else:
            if aspect in (Aspect.MULTIPLY_BY, Aspect.DIVIDE_BY):
                if sourceQname:
                    if aspectSourceValue:
                        return aspectSourceValue
                return (ruleValue, ())
            elif aspect == Aspect.DIMENSIONS:
                if aspectSourceValue is None:
                    aspectSourceValue = set()
                else:
                    if ruleValue is None:
                        ruleValueSet = set()
                    else:
                        ruleValueSet = set(ruleValue)
                    omitDims = formula.evaluateRule(xpCtx, Aspect.OMIT_DIMENSIONS)
                    if omitDims is None:
                        omitDimsSet = set()
                    else:
                        omitDimsSet = set(omitDims)
                return (aspectSourceValue | ruleValueSet) - omitDimsSet
    if isinstance(aspect, QName):
        return aspectSourceValue
    if aspect in (Aspect.COMPLETE_SEGMENT, Aspect.COMPLETE_SCENARIO,
     Aspect.NON_XDT_SEGMENT, Aspect.NON_XDT_SCENARIO):
        occFragments = []
        occEmpty = ruleValue and ruleValue[0] == XbrlConst.qnFormulaOccEmpty
        if not occEmpty:
            if aspectSourceValue:
                occFragments.extend(aspectSourceValue)
        if ruleValue:
            occFragments.extend(ruleValue[1 if occEmpty else 0:])
        return occFragments


def uncoveredAspectValue(xpCtx, aspect):
    for vb in xpCtx.varBindings.values():
        if vb.isFactVar:
            if not vb.isFallback:
                if vb.hasAspectValueUncovered(aspect):
                    return vb.aspectValue(aspect)


def variableBindingIsFallback(xpCtx, variableQname):
    for vb in xpCtx.varBindings.values():
        if vb.qname == variableQname:
            return vb.isFactVar and vb.isFallback

    return False


def uncoveredVariableSetAspects(xpCtx):
    aspectsDefined = set()
    aspectsCovered = set()
    for vb in xpCtx.varBindings.values():
        if vb.isFactVar and not vb.isFallback:
            aspectsCovered |= vb.aspectsCovered
            aspectsDefined |= vb.aspectsDefined

    return aspectsDefined - aspectsCovered


class VariableBindingError:

    def __init__(self, err, msg=None):
        self.err = err
        self.msg = msg

    def __repr__(self):
        return self.err


def orderAspects(aspects):
    d = {}
    for aspect in aspects:
        if isinstance(aspect, QName):
            d[aspect.localName] = aspect
        else:
            d[str(aspect)] = aspect

    result = []
    for key in sorted(d.keys()):
        result.append(d[key])

    return result


xbrlfe_undefinedSAV = VariableBindingError('xbrlfe:undefinedSAV')

class VariableBinding:

    def __init__(self, xpCtx, varRel=None, boundFact=None):
        self.xpCtx = xpCtx
        if varRel is not None:
            self.qname = varRel.variableQname
            self.var = varRel.toModelObject
        else:
            self.qname = self.var = None
        self.aspectsDefined = set()
        self.aspectsCovered = set()
        self.isFactVar = isinstance(self.var, ModelFactVariable)
        self.isGeneralVar = isinstance(self.var, ModelGeneralVariable)
        self.isParameter = isinstance(self.var, ModelParameter)
        self.isFormulaResult = isinstance(self.var, ModelFormula)
        self.isBindAsSequence = self.var.bindAsSequence == 'true' if isinstance(self.var, ModelVariable) else False
        self.yieldedFact = boundFact
        self.yieldedFactResult = None
        self.isFallback = False
        self.instances = [inst for qn in self.var.fromInstanceQnames for inst in xpCtx.flattenSequence(xpCtx.inScopeVars[qn])] if (self.var is not None and self.var.fromInstanceQnames) else ([
         xpCtx.modelXbrl])

    def close(self):
        self.__dict__.clear()

    @property
    def resourceElementName(self):
        if self.isFactVar:
            return _('Fact Variable')
        else:
            if self.isGeneralVar:
                return _('General Variable')
            else:
                if self.isParameter:
                    return _('Parameter')
                else:
                    if isinstance(self.var, ModelTuple):
                        return _('Tuple')
                    if isinstance(self.var, ModelFormula):
                        return _('Formula')
                if isinstance(self.var, ModelValueAssertion):
                    return _('ValueAssertion')
            if isinstance(self.var, ModelExistenceAssertion):
                return _('ExistenceAssertion')

    def matchesSubPartitions(self, partition, aspects):
        if self.var.matches == 'true':
            return [partition]
        else:
            subpartition0 = []
            subpartitions = [
             subpartition0]
            matches = defaultdict(list)
            for fact in partition:
                matched = False
                for i, fact2 in enumerate(subpartition0):
                    if aspectsMatchself.xpCtxfactfact2aspects:
                        matches[i].append(fact)
                        matched = True
                        break

                if not matched:
                    subpartition0.append(fact)

            if matches:
                matchIndices = sorted(matches.keys())
                matchIndicesLen = len(matchIndices)

                def addSubpartition(l):
                    if l == matchIndicesLen:
                        subpartitions.append(subpartition0.copy())
                    else:
                        i = matchIndices[l]
                        for matchedFact in matches[i]:
                            nextSubpartition = len(subpartitions)
                            addSubpartition(l + 1)
                            for j in range(nextSubpartition, len(subpartitions)):
                                subpartitions[j][i] = matchedFact

                addSubpartition(0)
            return subpartitions

    @property
    def evaluationResults(self):
        if self.isFactVar:
            if self.isBindAsSequence:
                if self.facts:
                    for factsPartition in factsPartitions(self.xpCtx, self.facts, orderAspects(self.aspectsDefined - self.aspectsCovered)):
                        for matchesSubPartition in self.matchesSubPartitions(factsPartition, self.aspectsDefined):
                            self.yieldedFact = matchesSubPartition[0]
                            self.yieldedFactContext = self.yieldedFact.context
                            self.yieldedEvaluation = matchesSubPartition
                            self.isFallback = False
                            yield matchesSubPartition

            else:
                for fact in self.facts:
                    self.yieldedFact = fact
                    self.yieldedFactContext = self.yieldedFact.context
                    self.yieldedEvaluation = fact
                    self.isFallback = False
                    yield fact

            if self.values:
                self.yieldedFact = None
                self.yieldedFactContext = None
                self.yieldedEvaluation = 'fallback'
                self.isFallback = True
                yield self.values
        else:
            if self.isGeneralVar:
                self.yieldedFact = None
                self.yieldedFactContext = None
                self.isFallback = False
                if self.isBindAsSequence:
                    self.yieldedEvaluation = self.values
                    yield self.values
                else:
                    for value in self.values:
                        self.yieldedEvaluation = value
                        yield value

            elif self.isParameter:
                self.yieldedFact = None
                self.yieldedEvaluation = None
                self.isFallback = False
                yield self.parameterValue

    def matchableBoundFact(self, fbVars):
        if self.isFallback or self.isParameter or self.isGeneralVar:
            return
        else:
            if self.isBindAsSequence:
                return tuple(self.yieldedEvaluation)
            if self.isFormulaResult:
                return self.yieldedFact
            return self.yieldedEvaluation

    def hasDimension(self, dimension):
        return dimension in self.definedDimensions

    def hasDimensionValueDefined(self, dimension):
        return dimension in self.definedDimensions

    def definedDimensions(self, dimension):
        if self.yieldedFact.isItem:
            if self.yieldedFact.context is not None:
                return self.yieldedFact.context.dimAspects(self.xpCtx.defaultDimensionAspects)
        return set()

    def isDimensionalValid(self, dimension):
        return False

    def hasAspectValueUncovered(self, aspect):
        if aspect in aspectModelAspect:
            aspect = aspectModelAspect[aspect]
        return aspect in self.aspectsDefined and aspect not in self.aspectsCovered

    def hasAspectValueCovered(self, aspect):
        if aspect in aspectModelAspect:
            aspect = aspectModelAspect[aspect]
        return aspect in self.aspectsCovered

    def aspectsNotCovered(self, aspects):
        return set(a for a in aspects if not self.hasAspectValueCovered(a))

    def hasAspectValueDefined(self, aspect):
        if aspect in aspectModelAspect:
            aspect = aspectModelAspect[aspect]
        return aspect in self.aspectsDefined

    def aspectValue(self, aspect):
        fact = self.yieldedFact
        if fact is None:
            if aspect == Aspect.DIMENSIONS:
                return set()
            else:
                return
        if aspect == Aspect.LOCATION:
            return fact.getparent()
        if aspect == Aspect.LOCATION_RULE:
            return fact
        if aspect == Aspect.CONCEPT:
            return fact.qname
        if fact.isTuple or fact.context is None:
            return
        if aspect == Aspect.PERIOD:
            return fact.context.period
        if aspect == Aspect.PERIOD_TYPE:
            if fact.context.isInstantPeriod:
                return 'instant'
            else:
                if fact.context.isStartEndPeriod:
                    return 'duration'
                if fact.context.isForeverPeriod:
                    return 'forever'
                return
        if aspect == Aspect.INSTANT:
            return fact.context.instantDatetime
        if aspect == Aspect.START:
            return fact.context.startDatetime
        if aspect == Aspect.END:
            return fact.context.endDatetime
        if aspect == Aspect.ENTITY_IDENTIFIER:
            return fact.context.entityIdentifierElement
        if aspect == Aspect.SCHEME:
            return fact.context.entityIdentifier[0]
        if aspect == Aspect.VALUE:
            return fact.context.entityIdentifier[1]
        if aspect in (Aspect.COMPLETE_SEGMENT, Aspect.COMPLETE_SCENARIO,
         Aspect.NON_XDT_SEGMENT, Aspect.NON_XDT_SCENARIO):
            return fact.context.nonDimValues(aspect)
        if aspect == Aspect.DIMENSIONS:
            return fact.context.dimAspects(self.xpCtx.defaultDimensionAspects)
        if isinstance(aspect, QName):
            return fact.context.dimValue(aspect)
        if fact.unit is not None:
            if aspect == Aspect.UNIT:
                return fact.unit
            if aspect in (Aspect.UNIT_MEASURES, Aspect.MULTIPLY_BY, Aspect.DIVIDE_BY):
                return fact.unit.measures
# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Stylesheet.py
# Compiled at: 2006-07-30 11:45:47
__doc__ = '\nxsl:stylesheet / xsl:transform implementation;\nvarious stylesheet internals\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import sys
from xml.dom import Node, XMLNS_NAMESPACE
from Ft.Lib import Set
from Ft.Xml import XPath
from Ft.Xml.XPath import Conversions
from Ft.Xml.Xslt import XSL_NAMESPACE, XsltElement, XsltException, Error
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo
from Ft.Xml.Xslt import XsltContext, PatternList
from Ft.Xml.Xslt import OutputParameters, MessageSource
from Ft.Xml.Xslt.LiteralElement import LiteralElement
__all__ = [
 'MatchTree', 'StylesheetElement']

def MatchTree(patterns, context):
    """
    Returns all nodes, from context on down, that match the patterns
    """
    state = context.copy()
    children = context.node.childNodes
    attributes = context.node.xpathAttributes or None
    matched = patterns.xsltKeyPrep(context, context.node)
    pos = 1
    size = len(children)
    for node in children:
        (context.node, context.position, context.size) = (
         node, pos, size)
        map(lambda x, y: x.extend(y), matched, MatchTree(patterns, context))
        pos += 1

    if attributes:
        size = len(attributes)
        pos = 1
        for node in attributes:
            (context.node, context.position, context.size) = (
             node, pos, size)
            map(lambda x, y: x.extend(y), matched, patterns.xsltKeyPrep(context, node))
            pos += 1

    context.set(state)
    return matched
    return


class StylesheetElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Seq(ContentInfo.Rep(ContentInfo.QName(XSL_NAMESPACE, 'xsl:import')), ContentInfo.TopLevelElements)
    legalAttrs = {'id': AttributeInfo.Id(), 'extension-element-prefixes': AttributeInfo.Prefixes(), 'exclude-result-prefixes': AttributeInfo.Prefixes(), 'version': AttributeInfo.Number(required=1)}
    doesSetup = doesPrime = doesIdle = 0

    def __init__(self, root, namespaceUri, localName, baseUri):
        XsltElement.__init__(self, root, namespaceUri, localName, baseUri)
        self.reset1()
        return

    def reset1(self):
        self.matchTemplates = {}
        self.namedTemplates = {}
        self.globalVars = {}
        self.initialFunctions = {}
        return

    def reset2(self):
        self.outputParams = OutputParameters.OutputParameters()
        self.spaceRules = []
        self.namespaceAliases = {}
        self.decimalFormats = {}
        return

    def setup(self):
        """
        Called only once, at the first initialization
        """
        self.reset2()
        space_rules = []
        global_vars = []
        top_level_elements = {'namespace-alias': [], 'decimal-format': [], 'strip-space': space_rules, 'preserve-space': space_rules, 'output': [], 'template': [], 'key': [], 'variable': global_vars, 'param': global_vars}
        reduce(lambda ignored, child, toplevel=top_level_elements: child.expandedName[0] == XSL_NAMESPACE and toplevel.get(child.expandedName[1], []).append(child), self.children, 'ignored')
        self._setupNamespaceAliases(top_level_elements['namespace-alias'])
        self._setupDecimalFormats(top_level_elements['decimal-format'])
        self._setupWhitespaceRules(space_rules)
        self._setupOutput(top_level_elements['output'])
        self._setupTemplates(top_level_elements['template'])
        self._setupKeys(top_level_elements['key'])
        if self.namespaceAliases:
            self._setupLiteralElements(self)
        self._setupTopLevelVarParams(global_vars)
        return

    def _setupNamespaceAliases(self, aliases):
        merged = {}
        for alias in aliases:
            stylesheet_ns = alias.namespaces[alias._stylesheet_prefix]
            if stylesheet_ns in merged:
                existing = merged[stylesheet_ns].importIndex
                if existing < alias.importIndex:
                    merged[stylesheet_ns] = alias
                elif existing == alias.importIndex:
                    raise XsltException(Error.DUPLICATE_NAMESPACE_ALIAS, alias._stylesheet_prefix)
            else:
                merged[stylesheet_ns] = alias

        for (stylesheet_ns, alias) in merged.items():
            namespace = alias.namespaces[alias._result_prefix]
            prefix = alias._result_prefix
            self.namespaceAliases[stylesheet_ns] = (namespace, prefix)

        return

    def _setupDecimalFormats(self, decimal_formats):
        for df in decimal_formats:
            (name, format) = df.getFormatInfo()
            existing = self.decimalFormats.get(name)
            if existing and existing != format:
                if name:
                    if name[0]:
                        name = df.namespaces[name[0]] + ':' + name[1]
                    else:
                        name = name[1]
                else:
                    name = '#default'
                raise XsltException(Error.DUPLICATE_DECIMAL_FORMAT, name)
            self.decimalFormats[name] = format

        if None not in self.decimalFormats:
            self.decimalFormats[None] = ('.', ',', 'Infinity', '-', 'NaN', '%', unichr(8240), '0', '#', ';')
        return
        return

    def _setupWhitespaceRules(self, space_rules):
        space_rules.sort(lambda a, b: cmp(a.importIndex, b.importIndex))
        merged = {}
        for rule in space_rules:
            (strip, elements) = rule.getWhitespaceInfo()
            for eName in elements:
                merged[eName] = strip

        star = None
        prefix_star = []
        for ((namespace, local), strip) in merged.items():
            rule = (
             namespace, local, strip)
            if local == '*':
                if namespace:
                    prefix_star.append(rule)
                else:
                    star = rule
            else:
                self.spaceRules.append(rule)

        self.spaceRules.extend(prefix_star)
        star and self.spaceRules.append(star)
        return
        return

    def _setupOutput(self, outputs):
        outputs.sort(lambda a, b: cmp(a.importIndex, b.importIndex))
        for output in outputs:
            self.outputParams.parse(output)

        return

    def _setupTemplates(self, templates):
        named_tpls = self.namedTemplates
        match_tpls = self.matchTemplates
        shortcuts = []
        for (template, position) in zip(templates, xrange(len(templates))):
            (shorts, name) = template.getTemplateInfo(position)
            if name:
                existing = named_tpls.get(name)
                if existing:
                    if existing.importIndex == template.importIndex:
                        raise XsltException(Error.DUPLICATE_NAMED_TEMPLATE, name)
                    elif existing.importIndex > template.importIndex:
                        pass
                    else:
                        named_tpls[name] = template
                else:
                    named_tpls[name] = template
            shortcuts.extend(shorts)

        shortcuts.sort()
        shortcuts.reverse()
        for (sort_key, template_info) in shortcuts:
            (mode, pattern_info, (node_type, expanded_name)) = template_info
            pattern_info = (
             sort_key, pattern_info)
            mode_table = match_tpls.get(mode)
            if not mode_table:
                mode_table = match_tpls[mode] = {}
            type_table = mode_table.get(node_type)
            if not type_table:
                if node_type == Node.ELEMENT_NODE:
                    type_list = [pattern_info]
                    mode_table[node_type] = {expanded_name: type_list}
                else:
                    mode_table[node_type] = [
                     pattern_info]
            elif node_type == Node.ELEMENT_NODE:
                type_list = type_table.get(expanded_name)
                if not type_list:
                    type_table[expanded_name] = [
                     pattern_info]
                else:
                    type_list.append(pattern_info)
            else:
                type_table.append(pattern_info)

        return

    def _setupKeys(self, keys):
        self._keys = {}
        for key in keys:
            (name, info) = key.getKeyInfo()
            if name not in self._keys:
                self._keys[name] = [
                 info]
            else:
                self._keys[name].append(info)

        return

    def _setupLiteralElements(self, node):
        if isinstance(node, LiteralElement):
            node.fixupAliases(self.namespaceAliases)
        for child in node.children or []:
            self._setupLiteralElements(child)

        return

    def _setupTopLevelVarParams(self, global_vars):
        self._topVariables = (index, ordered) = ({}, [])
        for vp in global_vars:
            existing = index.get(vp._name)
            if vp.importIndex > (existing and existing.importIndex or -1):
                index[vp._name] = vp
                ordered.append(vp)

        return

    def primeStylesheet(self, contextNode, processor, topLevelParams, docUri):
        doc = contextNode.rootNode
        context = XsltContext.XsltContext(doc, 1, 1, processorNss=self.namespaces, stylesheet=self, processor=processor, extFunctionMap=processor.extFunctions)
        baseUri = docUri or getattr(context.node, 'refUri', None)
        context.addDocument(doc, baseUri)
        for instruction in self.root.primeInstructions:
            instruction.prime(processor, context)

        self.initialFunctions.update(context.functions)
        overridden_params = {}
        for (split_name, value) in topLevelParams.items():
            if not isinstance(split_name, tuple):
                try:
                    split_name = self.expandQName(split_name)
                except KeyError:
                    continue

            overridden_params[split_name] = value

        for vnode in self._topVariables[1]:
            self._computeGlobalVar(vnode._name, context, [], [], overridden_params, processor)
            self.globalVars.update(context.varBindings)

        return
        return

    def _computeGlobalVar(self, vname, context, processed, deferred, overriddenParams, processor):
        vnode = self._topVariables[0][vname]
        if vnode in deferred:
            raise XsltException(Error.CIRCULAR_VAR, vname[0], vname[1])
        if vnode in processed:
            return
        if vnode.expandedName[1][0] == 'p':
            if vname in overriddenParams:
                context.varBindings[vname] = overriddenParams[vname]
            else:
                finished = 0
                while not finished:
                    orig_depth = len(processor.writers)
                    try:
                        vnode.instantiate(context, processor)
                        finished = 1
                    except XPath.RuntimeException, e:
                        if e.errorCode == XPath.RuntimeException.UNDEFINED_VARIABLE:
                            depth = len(processor.writers)
                            for i in xrange(depth - orig_depth):
                                processor.writers.pop()

                            deferred.append(vnode)
                            self._computeGlobalVar((e.params[0], e.params[1]), context, processed, deferred, overriddenParams, processor)
                            deferred.remove(vnode)
                        else:
                            raise

                overriddenParams[vname] = context.varBindings[vname]
        finished = 0
        while not finished:
            orig_depth = len(processor.writers)
            try:
                vnode.instantiate(context, processor)
                finished = 1
            except XPath.RuntimeException, e:
                if e.errorCode == XPath.RuntimeException.UNDEFINED_VARIABLE:
                    depth = len(processor.writers)
                    for i in xrange(depth - orig_depth):
                        processor.writers.pop()

                    deferred.append(vnode)
                    self._computeGlobalVar((e.params[0], e.params[1]), context, processed, deferred, overriddenParams, processor)
                    deferred.remove(vnode)
                else:
                    raise

        processed.append(vnode)
        return

    def updateKey(self, doc, keyName, processor):
        """
        Update a particular key for a new document
        """
        from pprint import pprint
        if doc not in processor.keys:
            processor.keys[doc] = {}
        if keyName not in processor.keys[doc]:
            key_values = processor.keys[doc][keyName] = {}
        else:
            key_values = processor.keys[doc][keyName]
        try:
            keys = self._keys[keyName]
        except KeyError:
            return

        updates = {}
        for key in keys:
            (match_pattern, use_expr, namespaces) = key
            context = XsltContext.XsltContext(doc, 1, 1, processorNss=namespaces, processor=processor, extFunctionMap=self.initialFunctions)
            patterns = PatternList([match_pattern], namespaces)
            matched = MatchTree(patterns, context)[0]
            for node in matched:
                state = context.copy()
                context.node = node
                key_value_list = use_expr.evaluate(context)
                if not isinstance(key_value_list, list):
                    key_value_list = [
                     key_value_list]
                for key_value in key_value_list:
                    key_value = Conversions.StringValue(key_value)
                    if key_value not in updates:
                        updates[key_value] = [
                         node]
                    else:
                        updates[key_value].append(node)

                context.set(state)

        for key_value in updates:
            if key_value in key_values:
                nodes = Set.Union(key_values[key_value], updates[key_value])
            else:
                nodes = Set.Unique(updates[key_value])
            key_values[key_value] = nodes

        return

    def updateAllKeys(self, context, processor):
        """
        Update all the keys for all documents in the context
        Only used as an override for the default lazy key eval
        """
        for keyName in self._keys:
            for doc in context.documents.values():
                self.updateKey(doc, keyName, processor)

        return

    def idle(self, contextNode, processor, baseUri=None):
        for instruction in self.root.idleInstructions:
            instruction.idle(processor)

        return

    def reset(self):
        """
        Called whenever the processor is reset, i.e. after each run
        Also called whenever multiple stylesheets are appended to
        a processor, because the new top-level elements from the
        new stylesheet need to be processed into the main one
        """
        self.reset1()
        self.reset2()
        return

    def getNamedTemplates(self):
        return self.namedTemplates.copy()

    def getGlobalVariables(self):
        return self.globalVars.copy()

    def getInitialFunctions(self):
        return self.initialFunctions.copy()

    def applyTemplates--- This code section failed: ---

 L. 529         0  LOAD_FAST             1  'context'
                3  LOAD_ATTR             1  'currentNode'
                6  STORE_FAST           18  'save_current'

 L. 530         9  LOAD_FAST             1  'context'
               12  LOAD_ATTR             3  'node'
               15  DUP_TOP          
               16  STORE_FAST           20  'node'
               19  LOAD_FAST             1  'context'
               22  STORE_ATTR            1  'currentNode'

 L. 531        25  LOAD_FAST             0  'self'
               28  LOAD_FAST             1  'context'
               31  STORE_ATTR            5  'stylesheet'

 L. 536        34  LOAD_FAST             0  'self'
               37  LOAD_ATTR             6  'matchTemplates'
               40  LOAD_ATTR             7  'get'
               43  LOAD_FAST             1  'context'
               46  LOAD_ATTR             8  'mode'
               49  CALL_FUNCTION_1       1  None
               52  STORE_FAST           14  'mode_table'

 L. 537        55  LOAD_FAST            14  'mode_table'
               58  UNARY_NOT        
               59  JUMP_IF_FALSE         8  'to 70'
             62_0  THEN                     71
               62  POP_TOP          

 L. 539        63  LOAD_CONST               0
               66  RETURN_VALUE     
               67  JUMP_FORWARD          1  'to 71'
             70_0  COME_FROM            59  '59'
               70  POP_TOP          
             71_0  COME_FROM            67  '67'

 L. 541        71  BUILD_LIST_0          0 
               74  STORE_FAST           26  'patterns'

 L. 542        77  LOAD_FAST            20  'node'
               80  LOAD_ATTR            11  'nodeType'
               83  STORE_FAST            7  'node_type'

 L. 543        86  LOAD_FAST             7  'node_type'
               89  LOAD_GLOBAL          13  'Node'
               92  LOAD_ATTR            14  'ELEMENT_NODE'
               95  COMPARE_OP            2  ==
               98  JUMP_IF_FALSE        98  'to 199'
              101  POP_TOP          

 L. 544       102  LOAD_FAST            14  'mode_table'
              105  LOAD_ATTR             7  'get'
              108  LOAD_FAST             7  'node_type'
              111  CALL_FUNCTION_1       1  None
              114  STORE_FAST            8  'table'

 L. 545       117  LOAD_FAST             8  'table'
              120  JUMP_IF_FALSE        72  'to 195'
              123  POP_TOP          

 L. 546       124  LOAD_FAST            20  'node'
              127  LOAD_ATTR            16  'namespaceURI'
              130  LOAD_FAST            20  'node'
              133  LOAD_ATTR            17  'localName'
              136  BUILD_TUPLE_2         2 
              139  STORE_FAST           23  'key'

 L. 548       142  LOAD_FAST            26  'patterns'
              145  LOAD_ATTR            19  'extend'
              148  LOAD_FAST             8  'table'
              151  LOAD_ATTR             7  'get'
              154  LOAD_FAST            23  'key'
              157  BUILD_LIST_0          0 
              160  CALL_FUNCTION_2       2  None
              163  CALL_FUNCTION_1       1  None
              166  POP_TOP          

 L. 550       167  LOAD_FAST            26  'patterns'
              170  LOAD_ATTR            19  'extend'
              173  LOAD_FAST             8  'table'
              176  LOAD_ATTR             7  'get'
              179  LOAD_GLOBAL          20  'None'
              182  BUILD_LIST_0          0 
              185  CALL_FUNCTION_2       2  None
              188  CALL_FUNCTION_1       1  None
              191  POP_TOP          
              192  JUMP_ABSOLUTE       225  'to 225'
            195_0  COME_FROM           120  '120'
              195  POP_TOP          
              196  JUMP_FORWARD         26  'to 225'
            199_0  COME_FROM            98  '98'
              199  POP_TOP          

 L. 552       200  LOAD_FAST            26  'patterns'
              203  LOAD_ATTR            19  'extend'
              206  LOAD_FAST            14  'mode_table'
              209  LOAD_ATTR             7  'get'
              212  LOAD_FAST             7  'node_type'
              215  BUILD_LIST_0          0 
              218  CALL_FUNCTION_2       2  None
              221  CALL_FUNCTION_1       1  None
              224  POP_TOP          
            225_0  COME_FROM           196  '196'

 L. 556       225  LOAD_FAST            26  'patterns'
              228  LOAD_ATTR            19  'extend'
              231  LOAD_FAST            14  'mode_table'
              234  LOAD_ATTR             7  'get'
              237  LOAD_GLOBAL          20  'None'
              240  BUILD_LIST_0          0 
              243  CALL_FUNCTION_2       2  None
              246  CALL_FUNCTION_1       1  None
              249  POP_TOP          

 L. 559       250  LOAD_FAST            26  'patterns'
              253  UNARY_NOT        
              254  JUMP_IF_FALSE         8  'to 265'
            257_0  THEN                     266
              257  POP_TOP          

 L. 560       258  LOAD_CONST               0
              261  RETURN_VALUE     
              262  JUMP_FORWARD          1  'to 266'
            265_0  COME_FROM           254  '254'
              265  POP_TOP          
            266_0  COME_FROM           262  '262'

 L. 564       266  LOAD_FAST             4  'maxImport'
              269  LOAD_GLOBAL          20  'None'
              272  COMPARE_OP            9  is-not
              275  JUMP_IF_FALSE        25  'to 303'
            278_0  THEN                     304
              278  POP_TOP          

 L. 565       279  LOAD_GLOBAL          22  'filter'
              282  LOAD_FAST             4  'maxImport'
              285  LOAD_LAMBDA              '<code_object <lambda>>'
              288  MAKE_FUNCTION_1       1  None
              291  LOAD_FAST            26  'patterns'
              294  CALL_FUNCTION_2       2  None
              297  STORE_FAST           26  'patterns'
              300  JUMP_FORWARD          1  'to 304'
            303_0  COME_FROM           275  '275'
              303  POP_TOP          
            304_0  COME_FROM           300  '300'

 L. 568       304  LOAD_FAST            26  'patterns'
              307  LOAD_ATTR            23  'sort'
              310  CALL_FUNCTION_0       0  None
              313  POP_TOP          

 L. 569       314  LOAD_FAST            26  'patterns'
              317  LOAD_ATTR            24  'reverse'
              320  CALL_FUNCTION_0       0  None
              323  POP_TOP          

 L. 571       324  JUMP_FORWARD          4  'to 331'
              327  JUMP_IF_FALSE       150  'to 480'
              330  POP_TOP          
            331_0  COME_FROM           324  '324'

 L. 575       331  SETUP_LOOP          619  'to 953'
              334  LOAD_FAST            26  'patterns'
              337  GET_ITER         
              338  FOR_ITER            135  'to 476'
              341  UNPACK_SEQUENCE_2     2 
              344  STORE_FAST           22  'sort_key'
              347  UNPACK_SEQUENCE_3     3 
              350  STORE_FAST           11  'pattern'
              353  STORE_FAST           10  'axis_type'
              356  STORE_FAST           16  'template'

 L. 576       359  LOAD_FAST            16  'template'
              362  LOAD_ATTR            29  'namespaces'
              365  LOAD_FAST             1  'context'
              368  STORE_ATTR           30  'processorNss'

 L. 577       371  LOAD_FAST            11  'pattern'
              374  LOAD_ATTR            31  'match'
              377  LOAD_FAST             1  'context'
              380  LOAD_FAST             1  'context'
              383  LOAD_ATTR             3  'node'
              386  LOAD_FAST            10  'axis_type'
              389  CALL_FUNCTION_3       3  None
              392  JUMP_IF_FALSE        77  'to 472'
              395  POP_TOP          

 L. 579       396  DELETE_FAST          26  'patterns'

 L. 581       399  LOAD_FAST             1  'context'
              402  LOAD_ATTR            32  'varBindings'
              405  STORE_FAST            5  'current_variables'

 L. 582       408  LOAD_FAST             0  'self'
              411  LOAD_ATTR            34  'globalVars'
              414  LOAD_FAST             1  'context'
              417  STORE_ATTR           32  'varBindings'

 L. 583       420  SETUP_FINALLY        23  'to 446'

 L. 584       423  LOAD_FAST            16  'template'
              426  LOAD_ATTR            35  'instantiate'
              429  LOAD_FAST             1  'context'
              432  LOAD_FAST             2  'processor'
              435  LOAD_FAST             3  'params'
              438  CALL_FUNCTION_3       3  None
              441  POP_TOP          
              442  POP_BLOCK        
              443  LOAD_CONST               None
            446_0  COME_FROM           420  '420'

 L. 586       446  LOAD_FAST            18  'save_current'
              449  LOAD_FAST             1  'context'
              452  STORE_ATTR            1  'currentNode'

 L. 587       455  LOAD_FAST             5  'current_variables'
              458  LOAD_FAST             1  'context'
              461  STORE_ATTR           32  'varBindings'
              464  END_FINALLY      

 L. 588       465  LOAD_CONST               1
              468  RETURN_VALUE     
              469  JUMP_BACK           338  'to 338'
            472_0  COME_FROM           392  '392'
              472  POP_TOP          
              473  JUMP_BACK           338  'to 338'
              476  POP_BLOCK        
              477  JUMP_FORWARD        473  'to 953'
            480_0  COME_FROM           327  '327'
              480  POP_TOP          

 L. 594       481  LOAD_FAST            26  'patterns'
              484  LOAD_CONST               -1
              487  BINARY_SUBSCR    
              488  LOAD_CONST               0
              491  BINARY_SUBSCR    
              492  UNPACK_SEQUENCE_3     3 
              495  STORE_FAST           21  'highest_import'
              498  STORE_FAST           17  'highest_priority'
              501  STORE_FAST           19  'last_position'

 L. 595       504  BUILD_LIST_0          0 
              507  STORE_FAST           13  'matches'

 L. 596       510  SETUP_LOOP          148  'to 661'
              513  LOAD_FAST            26  'patterns'
              516  GET_ITER         
              517  FOR_ITER            140  'to 660'
              520  UNPACK_SEQUENCE_2     2 
              523  STORE_FAST           22  'sort_key'
              526  UNPACK_SEQUENCE_3     3 
              529  STORE_FAST           11  'pattern'
              532  STORE_FAST           10  'axis_type'
              535  STORE_FAST           16  'template'

 L. 597       538  LOAD_FAST            22  'sort_key'
              541  UNPACK_SEQUENCE_3     3 
              544  STORE_FAST           25  'import_index'
              547  STORE_FAST           12  'priority'
              550  STORE_FAST           27  'position'

 L. 599       553  LOAD_FAST            25  'import_index'
              556  LOAD_FAST            21  'highest_import'
              559  COMPARE_OP            0  <
              562  JUMP_IF_TRUE         23  'to 588'
              565  POP_TOP          
              566  LOAD_FAST            25  'import_index'
              569  LOAD_FAST            21  'highest_import'
              572  COMPARE_OP            2  ==
              575  JUMP_IF_FALSE        10  'to 588'
              578  POP_TOP          
              579  LOAD_FAST            12  'priority'
              582  LOAD_FAST            17  'highest_priority'
              585  COMPARE_OP            0  <
            588_0  COME_FROM           575  '575'
            588_1  COME_FROM           562  '562'
              588  JUMP_IF_FALSE         5  'to 596'
            591_0  THEN                     597
              591  POP_TOP          

 L. 603       592  BREAK_LOOP       
              593  JUMP_FORWARD          1  'to 597'
            596_0  COME_FROM           588  '588'
              596  POP_TOP          
            597_0  COME_FROM           593  '593'

 L. 605       597  LOAD_FAST            16  'template'
              600  LOAD_ATTR            29  'namespaces'
              603  LOAD_FAST             1  'context'
              606  STORE_ATTR           30  'processorNss'

 L. 606       609  LOAD_FAST            11  'pattern'
              612  LOAD_ATTR            31  'match'
              615  LOAD_FAST             1  'context'
              618  LOAD_FAST             1  'context'
              621  LOAD_ATTR             3  'node'
              624  LOAD_FAST            10  'axis_type'
              627  CALL_FUNCTION_3       3  None
              630  JUMP_IF_FALSE        23  'to 656'
              633  POP_TOP          

 L. 607       634  LOAD_FAST            13  'matches'
              637  LOAD_ATTR            45  'append'
              640  LOAD_FAST            16  'template'
              643  LOAD_FAST            11  'pattern'
              646  BUILD_TUPLE_2         2 
              649  CALL_FUNCTION_1       1  None
              652  POP_TOP          
              653  JUMP_BACK           517  'to 517'
            656_0  COME_FROM           630  '630'
              656  POP_TOP          
              657  JUMP_BACK           517  'to 517'
              660  POP_BLOCK        
            661_0  COME_FROM           510  '510'

 L. 609       661  LOAD_GLOBAL          46  'len'
              664  LOAD_FAST            13  'matches'
              667  CALL_FUNCTION_1       1  None
              670  LOAD_CONST               1
              673  COMPARE_OP            4  >
              676  JUMP_IF_FALSE       198  'to 877'
            679_0  THEN                     878
              679  POP_TOP          

 L. 611       680  BUILD_LIST_0          0 
              683  STORE_FAST            6  'locations'

 L. 612       686  SETUP_LOOP           60  'to 749'
              689  LOAD_FAST            13  'matches'
              692  GET_ITER         
              693  FOR_ITER             52  'to 748'
              696  UNPACK_SEQUENCE_2     2 
              699  STORE_FAST           16  'template'
              702  STORE_FAST           11  'pattern'

 L. 613       705  LOAD_FAST             6  'locations'
              708  LOAD_ATTR            45  'append'
              711  LOAD_FAST            16  'template'
              714  LOAD_ATTR            48  'baseUri'
              717  LOAD_FAST            16  'template'
              720  LOAD_ATTR            49  'lineNumber'
              723  LOAD_FAST            16  'template'
              726  LOAD_ATTR            50  'columnNumber'
              729  LOAD_GLOBAL          51  'repr'
              732  LOAD_FAST            11  'pattern'
              735  CALL_FUNCTION_1       1  None
              738  BUILD_TUPLE_4         4 
              741  CALL_FUNCTION_1       1  None
              744  POP_TOP          
              745  JUMP_BACK           693  'to 693'
              748  POP_BLOCK        
            749_0  COME_FROM           686  '686'

 L. 617       749  LOAD_FAST             6  'locations'
              752  LOAD_ATTR            23  'sort'
              755  CALL_FUNCTION_0       0  None
              758  POP_TOP          

 L. 619       759  BUILD_LIST_0          0 
              762  DUP_TOP          
              763  LOAD_ATTR            45  'append'
              766  STORE_FAST            9  '_[1]'
              769  LOAD_FAST             6  'locations'
              772  GET_ITER         
              773  FOR_ITER             23  'to 799'
              776  STORE_FAST           15  'location'
              779  LOAD_FAST             9  '_[1]'
              782  LOAD_GLOBAL          54  'MessageSource'
              785  LOAD_ATTR            55  'TEMPLATE_CONFLICT_LOCATION'
              788  LOAD_FAST            15  'location'
              791  BINARY_MODULO    
              792  CALL_FUNCTION_1       1  None
              795  POP_TOP          
              796  JUMP_BACK           773  'to 773'
              799  DELETE_FAST           9  '_[1]'
              802  STORE_FAST            6  'locations'

 L. 623       805  LOAD_GLOBAL          56  'XsltException'
              808  LOAD_GLOBAL          57  'Error'
              811  LOAD_ATTR            58  'MULTIPLE_MATCH_TEMPLATES'

 L. 624       814  LOAD_FAST             1  'context'
              817  LOAD_ATTR             3  'node'
              820  LOAD_CONST               '\n'
              823  LOAD_ATTR            59  'join'
              826  LOAD_FAST             6  'locations'
              829  CALL_FUNCTION_1       1  None
              832  CALL_FUNCTION_3       3  None
              835  STORE_FAST           24  'exception'

 L. 626       838  JUMP_FORWARD          4  'to 845'
              841  JUMP_IF_FALSE        23  'to 867'
            844_0  THEN                     874
              844  POP_TOP          
            845_0  COME_FROM           838  '838'

 L. 627       845  LOAD_FAST             2  'processor'
              848  LOAD_ATTR            61  'warning'
              851  LOAD_GLOBAL          62  'str'
              854  LOAD_FAST            24  'exception'
              857  CALL_FUNCTION_1       1  None
              860  CALL_FUNCTION_1       1  None
              863  POP_TOP          
              864  JUMP_ABSOLUTE       878  'to 878'
            867_0  COME_FROM           841  '841'
              867  POP_TOP          

 L. 629       868  LOAD_FAST            24  'exception'
              871  RAISE_VARARGS_1       1  None
              874  JUMP_FORWARD          1  'to 878'
            877_0  COME_FROM           676  '676'
              877  POP_TOP          
            878_0  COME_FROM           874  '874'

 L. 631       878  LOAD_FAST            13  'matches'
              881  JUMP_IF_FALSE        68  'to 952'
            884_0  THEN                     953
              884  POP_TOP          

 L. 632       885  LOAD_FAST            13  'matches'
              888  LOAD_CONST               0
              891  BINARY_SUBSCR    
              892  LOAD_CONST               0
              895  BINARY_SUBSCR    
              896  STORE_FAST           16  'template'

 L. 634       899  DELETE_FAST          26  'patterns'

 L. 635       902  DELETE_FAST          13  'matches'

 L. 638       905  LOAD_FAST            16  'template'
              908  LOAD_ATTR            29  'namespaces'
              911  LOAD_FAST             1  'context'
              914  STORE_ATTR           30  'processorNss'

 L. 639       917  LOAD_FAST            16  'template'
              920  LOAD_ATTR            35  'instantiate'
              923  LOAD_FAST             1  'context'
              926  LOAD_FAST             2  'processor'
              929  LOAD_FAST             3  'params'
              932  CALL_FUNCTION_3       3  None
              935  POP_TOP          

 L. 640       936  LOAD_FAST            18  'save_current'
              939  LOAD_FAST             1  'context'
              942  STORE_ATTR            1  'currentNode'

 L. 641       945  LOAD_CONST               1
              948  RETURN_VALUE     
              949  JUMP_FORWARD          1  'to 953'
            952_0  COME_FROM           881  '881'
              952  POP_TOP          
            953_0  COME_FROM           331  '331'

 L. 644       953  LOAD_CONST               0
              956  RETURN_VALUE     
              957  LOAD_CONST               None
              960  RETURN_VALUE     

Parse error at or near `SETUP_LOOP' instruction at offset 331

    def __getstate__(self):
        self.root.sourceNodes = {}
        self._input_source = None
        return self.__dict__
        return
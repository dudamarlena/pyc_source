# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\minixsv\xsvalSchema.py
# Compiled at: 2008-08-08 10:45:32
import string, re, os
from decimal import Decimal
from genxmlif.xmlifUtils import collapseString
from minixsv import *
from xsvalBase import XsValBase, TagException
from xsvalUtils import substituteSpecialEscChars
_localFacetDict = {(XSD_NAMESPACE, 'list'): ('length', 'minLength', 'maxLength', 'enumeration', 'pattern', 'whiteSpace'), (XSD_NAMESPACE, 'union'): ('enumeration', 'pattern', 'whiteSpace'), (XSD_NAMESPACE, 'anySimpleType'): 'whiteSpace'}

class XsValSchema(XsValBase):
    __module__ = __name__

    def validate(self, inputTree, xsdTree):
        XsValBase.validate(self, inputTree, xsdTree)
        self._initInternalAttributes(self.inputRoot)
        self._updateLookupTables(self.inputRoot, self.xsdLookupDict)
        self._includeAndImport(self.inputTree, self.inputTree, self.xsdIncludeDict, self.xsdLookupDict)
        if not self.errorHandler.hasErrors():
            self.xsdIdDict = {}
            self._checkSchemaSecondLevel()
        self.inputRoot['__WellknownSchemasImported__'] = 'false'

    def _checkSchemaSecondLevel(self):
        targetNamespace = self.inputRoot.getAttribute('targetNamespace')
        if targetNamespace == '':
            self.errorHandler.raiseError('Empty string not allowed for target namespace!', self.inputRoot)
        self._checkElementNodesSecondLevel()
        self._checkNotationNodesSecondLevel()
        self._checkAnyNodesSecondLevel()
        self._checkGroupNodesSecondLevel()
        self._checkAttrGroupNodesSecondLevel()
        self._checkAttributeNodesSecondLevel()
        self._checkAnyAttributesSecondLevel()
        if self.errorHandler.hasErrors():
            return
        self._checkComplexTypesSecondLevel()
        self._checkSimpleTypesSecondLevel()
        self._checkParticlesSecondLevel()
        self._checkIdentityConstraintsSecondLevel()
        self._checkKeysSecondLevel()
        self._checkKeyRefsSecondLevel()

    def _checkElementNodesSecondLevel(self):
        elementNodes = self.inputRoot.getElementsByTagNameNS(self.inputNsURI, 'element')
        for elementNode in elementNodes:
            if not elementNode.hasAttribute('name') and not elementNode.hasAttribute('ref'):
                self._addError("Element must have 'name' or 'ref' attribute!", elementNode)
                continue
            if elementNode.hasAttribute('ref'):
                for attrName in ('name', 'type', 'form'):
                    if elementNode.hasAttribute(attrName):
                        self._addError("Element with 'ref' attribute must not have %s attribute!" % repr(attrName), elementNode)
                        continue

            complexTypeNode = elementNode.getFirstChildNS(self.inputNsURI, 'complexType')
            simpleTypeNode = elementNode.getFirstChildNS(self.inputNsURI, 'simpleType')
            if elementNode.hasAttribute('ref') and (complexTypeNode != None or simpleTypeNode != None):
                self._addError("Element with 'ref' attribute must not have type definition!", elementNode)
                continue
            if elementNode.hasAttribute('type') and (complexTypeNode != None or simpleTypeNode != None):
                self._addError("Element with 'type' attribute must not have type definition!", elementNode)
                continue
            if elementNode.hasAttribute('ref'):
                for forbiddenAttr in ('block', 'nillable', 'default', 'fixed'):
                    if elementNode.hasAttribute(forbiddenAttr):
                        self._addError("Element with 'ref' attribute must not have %s attribute!" % repr(forbiddenAttr), elementNode)

                self._checkReference(elementNode, self.xsdElementDict)
            if elementNode.hasAttribute('type'):
                self._checkType(elementNode, 'type', self.xsdTypeDict)
            self._checkNodeId(elementNode)
            self._checkOccurs(elementNode)
            self._checkFixedDefault(elementNode)

        return

    def _checkNotationNodesSecondLevel(self):
        notationNodes = self.inputRoot.getElementsByTagNameNS(self.inputNsURI, 'notation')
        for notationNode in notationNodes:
            if not notationNode.hasAttribute('public') and not notationNode.hasAttribute('system'):
                self._addError("Notation must have 'public' or 'system' attribute!", notationNode)

    def _checkAnyNodesSecondLevel(self):
        anyNodes = self.inputRoot.getElementsByTagNameNS(self.inputNsURI, 'any')
        for anyNode in anyNodes:
            self._checkOccurs(anyNode)
            self._checkNodeId(anyNode)

    def _checkGroupNodesSecondLevel(self):
        groupNodes = self.inputRoot.getElementsByTagNameNS(self.inputNsURI, 'group')
        for groupNode in groupNodes:
            self._checkNodeId(groupNode)
            if groupNode.hasAttribute('ref'):
                self._checkReference(groupNode, self.xsdGroupDict)
                self._checkOccurs(groupNode)

        if self.errorHandler.hasErrors():
            return

    def _checkGroupNodeCircularDef(self, groupNode, groupNameDict):
        (childGroupsRefNodes, dummy, dummy) = groupNode.getXPathList('.//%sgroup' % self.inputNsPrefixString)
        for childGroupRefNode in childGroupsRefNodes:
            if childGroupRefNode.hasAttribute('ref'):
                childGroupNode = self.xsdGroupDict[childGroupRefNode.getQNameAttribute('ref')]
                if not groupNameDict.has_key(childGroupNode['name']):
                    groupNameDict[childGroupNode['name']] = 1
                    self._checkGroupNodeCircularDef(childGroupNode, groupNameDict)
                else:
                    self._addError('Circular definition of group %s!' % repr(childGroupNode['name']), childGroupNode)

    def _checkAttrGroupNodesSecondLevel(self):
        attributeGroupNodes = self.inputRoot.getElementsByTagNameNS(self.inputNsURI, 'attributeGroup')
        for attributeGroupNode in attributeGroupNodes:
            if attributeGroupNode.hasAttribute('ref'):
                self._checkReference(attributeGroupNode, self.xsdAttrGroupDict)
            self._checkNodeId(attributeGroupNode)

    def _checkAttributeNodesSecondLevel(self):
        attributeNodes = self.inputRoot.getElementsByTagNameNS(XSD_NAMESPACE, 'attribute')
        for attributeNode in attributeNodes:
            if os.path.basename(attributeNode.getFilePath()) != 'XMLSchema-instance.xsd':
                if attributeNode.getParentNode() == self.inputRoot or self._getAttributeFormDefault(attributeNode) == 'qualified':
                    if self._getTargetNamespace(attributeNode) == XSI_NAMESPACE:
                        self._addError("Target namespace of an attribute must not match '%s'!" % XSI_NAMESPACE, attributeNode)
            if not attributeNode.hasAttribute('name') and not attributeNode.hasAttribute('ref'):
                self._addError("Attribute must have 'name' or 'ref' attribute!", attributeNode)
                continue
            if attributeNode.getAttribute('name') == 'xmlns':
                self._addError("Attribute must not match 'xmlns'!", attributeNode)
            if attributeNode.hasAttribute('ref'):
                if attributeNode.hasAttribute('name'):
                    self._addError("Attribute may have 'name' OR 'ref' attribute!", attributeNode)
                if attributeNode.hasAttribute('type'):
                    self._addError("Attribute may have 'type' OR 'ref' attribute!", attributeNode)
                if attributeNode.hasAttribute('form'):
                    self._addError("Attribute 'form' is not allowed in this context!", attributeNode)
                if attributeNode.getFirstChildNS(XSD_NAMESPACE, 'simpleType') != None:
                    self._addError("Attribute may only have 'ref' attribute OR 'simpleType' child!", attributeNode)
                self._checkReference(attributeNode, self.xsdAttributeDict)
            if attributeNode.hasAttribute('type'):
                if attributeNode.getFirstChildNS(XSD_NAMESPACE, 'simpleType') != None:
                    self._addError("Attribute may only have 'type' attribute OR 'simpleType' child!", attributeNode)
                self._checkType(attributeNode, 'type', self.xsdTypeDict, (XSD_NAMESPACE, 'simpleType'))
            use = attributeNode.getAttribute('use')
            if use in ('required', 'prohibited') and attributeNode.hasAttribute('default'):
                self._addError("Attribute 'default' is not allowed, because 'use' is '%s'!" % use, attributeNode)
            self._checkNodeId(attributeNode, unambiguousPerFile=0)
            self._checkFixedDefault(attributeNode)

        return

    def _checkAnyAttributesSecondLevel(self):
        (anyAttributeNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%sanyAttribute' % self.inputNsPrefixString)
        for anyAttributeNode in anyAttributeNodes:
            self._checkNodeId(anyAttributeNode)

    def _checkComplexTypesSecondLevel(self):
        prefix = self.inputNsPrefixString
        (contentNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)scomplexContent/%(prefix)srestriction | .//%(prefix)scomplexContent/%(prefix)sextension' % vars())
        for contentNode in contentNodes:
            self._checkType(contentNode, 'base', self.xsdTypeDict, (XSD_NAMESPACE, 'complexType'))

        (contentNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)ssimpleContent/%(prefix)srestriction | .//%(prefix)ssimpleContent/%(prefix)sextension' % vars())
        for contentNode in contentNodes:
            baseNsName = contentNode.getQNameAttribute('base')
            if baseNsName != (XSD_NAMESPACE, 'anyType'):
                typeNsName = contentNode.getParentNode().getNsName()
                self._checkBaseType(contentNode, baseNsName, self.xsdTypeDict, typeNsName)
            else:
                self._addError("Referred type must not be 'anyType'!", contentNode)
            self._checkNodeId(contentNode)

        (complexTypeNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)scomplexType | .//%(prefix)sextension' % vars())
        for complexTypeNode in complexTypeNodes:
            validAttrDict = {}
            self._updateAttributeDict(complexTypeNode, validAttrDict, 1)
            idAttrNode = None
            for (key, val) in validAttrDict.items():
                attrType = val['RefNode'].getQNameAttribute('type')
                if attrType == (XSD_NAMESPACE, 'ID'):
                    if not idAttrNode:
                        idAttrNode = val['Node']
                    else:
                        self._addError('Two attribute declarations of complex type are IDs!', val['Node'])

            self._checkNodeId(complexTypeNode)

        (contentNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)scomplexType/%(prefix)s*' % vars())
        for contentNode in contentNodes:
            self._checkOccurs(contentNode)

        (contentNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)scomplexContent | .//%(prefix)ssimpleContent' % vars())
        for contentNode in contentNodes:
            self._checkNodeId(contentNode)

        return

    def _checkParticlesSecondLevel(self):
        prefix = self.inputNsPrefixString
        (particleNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)sall | .//%(prefix)schoice | .//%(prefix)ssequence' % vars())
        for particleNode in particleNodes:
            elementTypeDict = {}
            elementNameDict = {}
            groupNameDict = {}
            self._checkContainedElements(particleNode, particleNode.getLocalName(), elementNameDict, elementTypeDict, groupNameDict)
            self._checkOccurs(particleNode)
            self._checkNodeId(particleNode)

    def _checkContainedElements--- This code section failed: ---

 L. 336         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             1  'inputNsPrefixString'
                6  STORE_FAST           10  'prefix'

 L. 337         9  SETUP_LOOP          617  'to 629'
               12  LOAD_FAST             1  'node'
               15  LOAD_ATTR             4  'getChildren'
               18  CALL_FUNCTION_0       0  None
               21  GET_ITER         
               22  FOR_ITER            603  'to 628'
               25  STORE_FAST           12  'childNode'

 L. 338        28  LOAD_FAST            12  'childNode'
               31  LOAD_ATTR             6  'getLocalName'
               34  CALL_FUNCTION_0       0  None
               37  STORE_FAST            6  'childParticleType'

 L. 339        40  LOAD_FAST             6  'childParticleType'
               43  LOAD_CONST               ('sequence', 'choice', 'all')
               46  COMPARE_OP            6  in
               49  JUMP_IF_FALSE        35  'to 87'
               52  POP_TOP          

 L. 340        53  BUILD_MAP             0 
               56  STORE_FAST            7  'dummy'

 L. 341        59  LOAD_FAST             0  'self'
               62  LOAD_ATTR             9  '_checkContainedElements'
               65  LOAD_FAST            12  'childNode'
               68  LOAD_FAST             6  'childParticleType'
               71  LOAD_FAST             7  'dummy'
               74  LOAD_FAST             4  'elementTypeDict'
               77  LOAD_FAST             5  'groupNameDict'
               80  CALL_FUNCTION_5       5  None
               83  POP_TOP          
               84  JUMP_BACK            22  'to 22'
             87_0  COME_FROM            49  '49'
               87  POP_TOP          

 L. 342        88  LOAD_FAST             6  'childParticleType'
               91  LOAD_CONST               'group'
               94  COMPARE_OP            6  in
               97  JUMP_IF_FALSE       257  'to 357'
              100  POP_TOP          

 L. 343       101  LOAD_FAST            12  'childNode'
              104  LOAD_CONST               'ref'
              107  BINARY_SUBSCR    
              108  LOAD_CONST               None
              111  COMPARE_OP            3  !=
              114  JUMP_IF_FALSE       165  'to 282'
              117  POP_TOP          

 L. 344       118  LOAD_FAST             0  'self'
              121  LOAD_ATTR            13  'xsdGroupDict'
              124  LOAD_FAST            12  'childNode'
              127  LOAD_ATTR            14  'getQNameAttribute'
              130  LOAD_CONST               'ref'
              133  CALL_FUNCTION_1       1  None
              136  BINARY_SUBSCR    
              137  STORE_FAST            8  'childGroupNode'

 L. 345       140  LOAD_FAST             5  'groupNameDict'
              143  LOAD_ATTR            16  'has_key'
              146  LOAD_FAST             8  'childGroupNode'
              149  LOAD_CONST               'name'
              152  BINARY_SUBSCR    
              153  CALL_FUNCTION_1       1  None
              156  JUMP_IF_TRUE         89  'to 248'
              159  POP_TOP          

 L. 346       160  LOAD_CONST               1
              163  LOAD_FAST             5  'groupNameDict'
              166  LOAD_FAST             8  'childGroupNode'
              169  LOAD_CONST               'name'
              172  BINARY_SUBSCR    
              173  STORE_SUBSCR     

 L. 347       174  SETUP_LOOP          102  'to 279'
              177  LOAD_FAST             8  'childGroupNode'
              180  LOAD_ATTR             4  'getChildren'
              183  CALL_FUNCTION_0       0  None
              186  GET_ITER         
              187  FOR_ITER             54  'to 244'
              190  STORE_FAST            9  'cChildNode'

 L. 348       193  LOAD_FAST             9  'cChildNode'
              196  LOAD_ATTR             6  'getLocalName'
              199  CALL_FUNCTION_0       0  None
              202  LOAD_CONST               'annotation'
              205  COMPARE_OP            3  !=
              208  JUMP_IF_FALSE        29  'to 240'
              211  POP_TOP          

 L. 349       212  LOAD_FAST             0  'self'
              215  LOAD_ATTR             9  '_checkContainedElements'
              218  LOAD_FAST             9  'cChildNode'
              221  LOAD_FAST             2  'particleType'
              224  LOAD_FAST             3  'elementNameDict'
              227  LOAD_FAST             4  'elementTypeDict'
              230  LOAD_FAST             5  'groupNameDict'
              233  CALL_FUNCTION_5       5  None
              236  POP_TOP          
              237  JUMP_BACK           187  'to 187'
            240_0  COME_FROM           208  '208'
              240  POP_TOP          
              241  JUMP_BACK           187  'to 187'
              244  POP_BLOCK        
              245  JUMP_ABSOLUTE       354  'to 354'
            248_0  COME_FROM           156  '156'
              248  POP_TOP          

 L. 351       249  LOAD_FAST             0  'self'
              252  LOAD_ATTR            20  '_addError'
              255  LOAD_CONST               'Circular definition of group %s!'
              258  LOAD_GLOBAL          21  'repr'
              261  LOAD_FAST             8  'childGroupNode'
              264  LOAD_CONST               'name'
              267  BINARY_SUBSCR    
              268  CALL_FUNCTION_1       1  None
              271  BINARY_MODULO    
              272  LOAD_FAST            12  'childNode'
              275  CALL_FUNCTION_2       2  None
              278  POP_TOP          
            279_0  COME_FROM           174  '174'
              279  JUMP_ABSOLUTE       625  'to 625'
            282_0  COME_FROM           114  '114'
              282  POP_TOP          

 L. 353       283  SETUP_LOOP          339  'to 625'
              286  LOAD_FAST            12  'childNode'
              289  LOAD_ATTR             4  'getChildren'
              292  CALL_FUNCTION_0       0  None
              295  GET_ITER         
              296  FOR_ITER             54  'to 353'
              299  STORE_FAST            9  'cChildNode'

 L. 354       302  LOAD_FAST             9  'cChildNode'
              305  LOAD_ATTR             6  'getLocalName'
              308  CALL_FUNCTION_0       0  None
              311  LOAD_CONST               'annotation'
              314  COMPARE_OP            3  !=
              317  JUMP_IF_FALSE        29  'to 349'
              320  POP_TOP          

 L. 355       321  LOAD_FAST             0  'self'
              324  LOAD_ATTR             9  '_checkContainedElements'
              327  LOAD_FAST             9  'cChildNode'
              330  LOAD_FAST             2  'particleType'
              333  LOAD_FAST             3  'elementNameDict'
              336  LOAD_FAST             4  'elementTypeDict'
              339  LOAD_FAST             5  'groupNameDict'
              342  CALL_FUNCTION_5       5  None
              345  POP_TOP          
              346  JUMP_BACK           296  'to 296'
            349_0  COME_FROM           317  '317'
              349  POP_TOP          
              350  JUMP_BACK           296  'to 296'
              353  POP_BLOCK        
            354_0  COME_FROM           283  '283'
              354  JUMP_BACK            22  'to 22'
            357_0  COME_FROM            97  '97'
              357  POP_TOP          

 L. 357       358  LOAD_FAST            12  'childNode'
              361  LOAD_ATTR             6  'getLocalName'
              364  CALL_FUNCTION_0       0  None
              367  LOAD_CONST               'any'
              370  COMPARE_OP            2  ==
              373  JUMP_IF_FALSE        19  'to 395'
              376  POP_TOP          

 L. 358       377  LOAD_FAST            12  'childNode'
              380  LOAD_ATTR            22  'getAttribute'
              383  LOAD_CONST               'namespace'
              386  CALL_FUNCTION_1       1  None
              389  STORE_FAST           11  'elementName'
              392  JUMP_FORWARD         28  'to 423'
            395_0  COME_FROM           373  '373'
              395  POP_TOP          

 L. 360       396  LOAD_FAST            12  'childNode'
              399  LOAD_ATTR            24  'getAttributeOrDefault'
              402  LOAD_CONST               'name'
              405  LOAD_FAST            12  'childNode'
              408  LOAD_ATTR            22  'getAttribute'
              411  LOAD_CONST               'ref'
              414  CALL_FUNCTION_1       1  None
              417  CALL_FUNCTION_2       2  None
              420  STORE_FAST           11  'elementName'
            423_0  COME_FROM           392  '392'

 L. 362       423  LOAD_FAST            12  'childNode'
              426  LOAD_ATTR            25  'hasAttribute'
              429  LOAD_CONST               'type'
              432  CALL_FUNCTION_1       1  None
              435  JUMP_IF_FALSE       101  'to 539'
            438_0  THEN                     540
              438  POP_TOP          

 L. 363       439  LOAD_FAST             4  'elementTypeDict'
              442  LOAD_ATTR            16  'has_key'
              445  LOAD_FAST            11  'elementName'
              448  CALL_FUNCTION_1       1  None
              451  JUMP_IF_TRUE         18  'to 472'
            454_0  THEN                     536
              454  POP_TOP          

 L. 364       455  LOAD_FAST            12  'childNode'
              458  LOAD_CONST               'type'
              461  BINARY_SUBSCR    
              462  LOAD_FAST             4  'elementTypeDict'
              465  LOAD_FAST            11  'elementName'
              468  STORE_SUBSCR     
              469  JUMP_ABSOLUTE       540  'to 540'
            472_0  COME_FROM           451  '451'
              472  POP_TOP          

 L. 365       473  LOAD_FAST            12  'childNode'
              476  LOAD_CONST               'type'
              479  BINARY_SUBSCR    
              480  LOAD_FAST             4  'elementTypeDict'
              483  LOAD_FAST            11  'elementName'
              486  BINARY_SUBSCR    
              487  COMPARE_OP            3  !=
              490  JUMP_IF_FALSE        42  'to 535'
            493_0  THEN                     536
              493  POP_TOP          

 L. 366       494  LOAD_FAST             0  'self'
              497  LOAD_ATTR            20  '_addError'
              500  LOAD_CONST               'Element %s has identical name and different types within %s!'
              503  LOAD_GLOBAL          21  'repr'
              506  LOAD_FAST            11  'elementName'
              509  CALL_FUNCTION_1       1  None
              512  LOAD_GLOBAL          21  'repr'
              515  LOAD_FAST             2  'particleType'
              518  CALL_FUNCTION_1       1  None
              521  BUILD_TUPLE_2         2 
              524  BINARY_MODULO    
              525  LOAD_FAST            12  'childNode'
              528  CALL_FUNCTION_2       2  None
              531  POP_TOP          
              532  JUMP_ABSOLUTE       540  'to 540'
            535_0  COME_FROM           490  '490'
              535  POP_TOP          
              536  JUMP_FORWARD          1  'to 540'
            539_0  COME_FROM           435  '435'
              539  POP_TOP          
            540_0  COME_FROM           536  '536'

 L. 367       540  LOAD_FAST             2  'particleType'
              543  LOAD_CONST               'sequence'
              546  COMPARE_OP            3  !=
              549  JUMP_IF_FALSE        72  'to 624'
              552  POP_TOP          

 L. 368       553  LOAD_FAST             3  'elementNameDict'
              556  LOAD_ATTR            16  'has_key'
              559  LOAD_FAST            11  'elementName'
              562  CALL_FUNCTION_1       1  None
              565  JUMP_IF_TRUE         14  'to 582'
              568  POP_TOP          

 L. 369       569  LOAD_CONST               1
              572  LOAD_FAST             3  'elementNameDict'
              575  LOAD_FAST            11  'elementName'
              578  STORE_SUBSCR     
              579  JUMP_ABSOLUTE       625  'to 625'
            582_0  COME_FROM           565  '565'
              582  POP_TOP          

 L. 371       583  LOAD_FAST             0  'self'
              586  LOAD_ATTR            20  '_addError'
              589  LOAD_CONST               'Element %s is not unique within %s!'
              592  LOAD_GLOBAL          21  'repr'
              595  LOAD_FAST            11  'elementName'
              598  CALL_FUNCTION_1       1  None
              601  LOAD_GLOBAL          21  'repr'
              604  LOAD_FAST             2  'particleType'
              607  CALL_FUNCTION_1       1  None
              610  BUILD_TUPLE_2         2 
              613  BINARY_MODULO    
              614  LOAD_FAST            12  'childNode'
              617  CALL_FUNCTION_2       2  None
              620  POP_TOP          
              621  JUMP_BACK            22  'to 22'
            624_0  COME_FROM           549  '549'
              624  POP_TOP          
              625  JUMP_BACK            22  'to 22'
              628  POP_BLOCK        
            629_0  COME_FROM             9  '9'
              629  LOAD_CONST               None
              632  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 279

    def _checkSimpleTypesSecondLevel(self):
        prefix = self.inputNsPrefixString
        (simpleTypeNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)ssimpleType' % vars())
        for simpleTypeNode in simpleTypeNodes:
            self._checkNodeId(simpleTypeNode)

        (restrictionNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)ssimpleType/%(prefix)srestriction' % vars())
        for restrictionNode in restrictionNodes:
            self._checkNodeId(restrictionNode)
            if not restrictionNode.hasAttribute('base') and restrictionNode.getFirstChildNS(self.inputNsURI, 'simpleType') == None:
                self._addError("Simple type restriction must have 'base' attribute or 'simpleType' child tag!", restrictionNode)
            if restrictionNode.hasAttribute('base') and restrictionNode.getFirstChildNS(self.inputNsURI, 'simpleType') != None:
                self._addError("Simple type restriction must not have 'base' attribute and 'simpleType' child tag!", restrictionNode)
            if restrictionNode.hasAttribute('base'):
                self._checkType(restrictionNode, 'base', self.xsdTypeDict)
            minExcl = restrictionNode.getFirstChildNS(self.inputNsURI, 'minExclusive')
            minIncl = restrictionNode.getFirstChildNS(self.inputNsURI, 'minInclusive')
            if minExcl != None and minIncl != None:
                self._addError("Restriction attributes 'minExclusive' and 'minInclusive' cannot be defined together!", restrictionNode)
            maxExcl = restrictionNode.getFirstChildNS(self.inputNsURI, 'maxExclusive')
            maxIncl = restrictionNode.getFirstChildNS(self.inputNsURI, 'maxInclusive')
            if maxExcl != None and maxIncl != None:
                self._addError("Restriction attributes 'maxExclusive' and 'maxInclusive' cannot be defined together!", restrictionNode)

        for restrictionNode in restrictionNodes:
            try:
                if restrictionNode.hasAttribute('base'):
                    facetNsName = self._getFacetType(restrictionNode, [restrictionNode.getParentNode()], self.xsdTypeDict)
                    if not facetNsName:
                        continue
                    if _localFacetDict.has_key(facetNsName):
                        suppFacets = _localFacetDict[facetNsName]
                    else:
                        (suppFacets, dummy, dummy) = self.xsdTypeDict[facetNsName].getXPathList('.//hfp:hasFacet/@name' % vars())
                    specifiedFacets = {'length': None, 'minLength': None, 'maxLength': None, 'minExclusive': None, 'minInclusive': None, 'maxExclusive': None, 'maxInclusive': None, 'totalDigits': None, 'fractionDigits': None}
                    for childNode in restrictionNode.getChildren():
                        if childNode.getLocalName() in suppFacets:
                            if specifiedFacets.has_key(childNode.getLocalName()):
                                specifiedFacets[childNode.getLocalName()] = childNode['value']
                            facetElementNode = self.xsdElementDict[childNode.getNsName()]
                            try:
                                self._checkElementTag(facetElementNode, restrictionNode, (childNode,), 0)
                            except TagException, errInst:
                                self._addError(errInst.errstr, errInst.node, errInst.endTag)
                            else:
                                if childNode.getLocalName() in ('enumeration', 'minExclusive',
                                                                'minInclusive', 'maxExclusive',
                                                                'maxInclusive'):
                                    simpleTypeReturnDict = self._checkSimpleType(restrictionNode, 'base', childNode, 'value', childNode['value'], None, checkAttribute=1)
                                    if simpleTypeReturnDict != None and simpleTypeReturnDict.has_key('orderedValue'):
                                        if childNode.getLocalName() != 'enumeration':
                                            specifiedFacets[childNode.getLocalName()] = simpleTypeReturnDict['orderedValue']
                        elif childNode.getLocalName() == 'enumeration':
                            self._checkSimpleType(restrictionNode, 'base', childNode, 'value', childNode['value'], None, checkAttribute=1)
                        elif childNode.getLocalName() != 'annotation':
                            self._addError('Facet %s not allowed for base type %s!' % (childNode.getLocalName(), repr(restrictionNode['base'])), childNode)

                    if specifiedFacets['length'] != None:
                        if specifiedFacets['minLength'] != None or specifiedFacets['maxLength'] != None:
                            self._addError("Facet 'minLength' and 'maxLength' not allowed if facet 'length' is specified!", restrictionNode)
                    elif specifiedFacets['maxLength'] != None and specifiedFacets['minLength'] != None:
                        if int(specifiedFacets['maxLength']) < int(specifiedFacets['minLength']):
                            self._addError("Facet 'maxLength' < facet 'minLength'!", restrictionNode)
                    if specifiedFacets['totalDigits'] != None and specifiedFacets['fractionDigits'] != None:
                        if int(specifiedFacets['totalDigits']) < int(specifiedFacets['fractionDigits']):
                            self._addError("Facet 'totalDigits' must be >= 'fractionDigits'!", restrictionNode)
                    if specifiedFacets['minExclusive'] != None and specifiedFacets['minInclusive'] != None:
                        self._addError("Facets 'minExclusive' and 'minInclusive' are mutually exclusive!", restrictionNode)
                    if specifiedFacets['maxExclusive'] != None and specifiedFacets['maxInclusive'] != None:
                        self._addError("Facets 'maxExclusive' and 'maxInclusive' are mutually exclusive!", restrictionNode)
                    minValue = specifiedFacets['minExclusive']
                    if specifiedFacets['minInclusive'] != None:
                        minValue = specifiedFacets['minInclusive']
                    maxValue = specifiedFacets['maxExclusive']
                    if specifiedFacets['maxInclusive'] != None:
                        maxValue = specifiedFacets['maxInclusive']
                    if minValue != None and maxValue != None and maxValue < minValue:
                        self._addError('maxValue facet < minValue facet!', restrictionNode)
            except TagException:
                self._addError('Primitive type for base type not found!', restrictionNode)

        (listNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)slist' % vars())
        for listNode in listNodes:
            self._checkNodeId(listNode)
            if not listNode.hasAttribute('itemType') and listNode.getFirstChildNS(self.inputNsURI, 'simpleType') == None:
                self._addError("List type must have 'itemType' attribute or 'simpleType' child tag!", listNode)
            elif listNode.hasAttribute('itemType') and listNode.getFirstChildNS(self.inputNsURI, 'simpleType') != None:
                self._addError("List type must not have 'itemType' attribute and 'simpleType' child tag!", listNode)
            elif listNode.hasAttribute('itemType'):
                itemType = self._checkType(listNode, 'itemType', self.xsdTypeDict)
                if self.xsdTypeDict.has_key(itemType):
                    if self.xsdTypeDict[itemType].getLocalName() != 'simpleType':
                        self._addError('ItemType %s must be a simple type!' % repr(itemType), listNode)
                    elif self.xsdTypeDict[itemType].getFirstChild().getLocalName() == 'list':
                        self._addError('ItemType %s must not be a list type!' % repr(itemType), listNode)

        (unionNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)ssimpleType/%(prefix)sunion' % vars())
        for unionNode in unionNodes:
            self._checkNodeId(unionNode)
            if not unionNode.hasAttribute('memberTypes'):
                for childNode in unionNode.getChildren():
                    if childNode.getLocalName() != 'annotation':
                        break
                else:
                    self._addError('Union must not be empty!', unionNode)
            else:
                for memberType in string.split(unionNode['memberTypes']):
                    memberNsName = unionNode.qName2NsName(memberType, 1)
                    self._checkBaseType(unionNode, memberNsName, self.xsdTypeDict)
                    if self.xsdTypeDict.has_key(memberNsName):
                        if self.xsdTypeDict[memberNsName].getLocalName() != 'simpleType':
                            self._addError('MemberType %s must be a simple type!' % repr(memberNsName), unionNode)

        (patternNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%(prefix)spattern' % vars())
        for patternNode in patternNodes:
            pattern = patternNode['value']
            try:
                pattern = substituteSpecialEscChars(pattern)
                try:
                    test = re.compile(pattern)
                except Exception, errstr:
                    self._addError(str(errstr), patternNode)
                    self._addError('%s is not a valid regular expression!' % repr(patternNode['value']), patternNode)

            except SyntaxError, errInst:
                self._addError(repr(errInst[0]), patternNode)

        return

    def _checkIdentityConstraintsSecondLevel(self):
        (identityConstraintNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%sunique' % self.inputNsPrefixString)
        for identityConstraintNode in identityConstraintNodes:
            self._checkNodeId(identityConstraintNode)
            selectorNode = identityConstraintNode.getFirstChildNS(XSD_NAMESPACE, 'selector')
            self._checkNodeId(selectorNode)
            try:
                (completeChildList, attrNodeList, attrNsNameFirst) = identityConstraintNode.getParentNode().getXPathList(selectorNode['xpath'], selectorNode)
                if attrNsNameFirst != None:
                    self._addError('Selection of attributes is not allowed for selector!', selectorNode)
            except Exception, errstr:
                self._addError(errstr, selectorNode)

            try:
                fieldNode = identityConstraintNode.getFirstChildNS(XSD_NAMESPACE, 'field')
                identityConstraintNode.getParentNode().getXPathList(fieldNode['xpath'], fieldNode)
                self._checkNodeId(fieldNode)
            except Exception, errstr:
                self._addError(errstr, fieldNode)

        return

    def _checkKeysSecondLevel(self):
        (keyNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%skey' % self.inputNsPrefixString)
        for keyNode in keyNodes:
            self._checkNodeId(keyNode)
            fieldNode = keyNode.getFirstChildNS(XSD_NAMESPACE, 'field')
            if fieldNode != None:
                self._checkNodeId(fieldNode)

        return

    def _checkKeyRefsSecondLevel(self):
        (keyrefNodes, dummy, dummy) = self.inputRoot.getXPathList('.//%skeyref' % self.inputNsPrefixString)
        for keyrefNode in keyrefNodes:
            self._checkNodeId(keyrefNode)
            self._checkKeyRef(keyrefNode, self.xsdIdentityConstrDict)

    def _checkFixedDefault(self, node):
        if node.hasAttribute('default') and node.hasAttribute('fixed'):
            self._addError("%s may have 'default' OR 'fixed' attribute!" % repr(node.getLocalName()), node)
        if node.hasAttribute('default'):
            self._checkSimpleType(node, 'type', node, 'default', node['default'], None, checkAttribute=1)
        if node.hasAttribute('fixed'):
            self._checkSimpleType(node, 'type', node, 'fixed', node['fixed'], None, checkAttribute=1)
        return

    def _checkReference(self, node, dict):
        baseNsName = node.getQNameAttribute('ref')
        if dict.has_key(baseNsName):
            refNode = dict[baseNsName]
            fixedValue = node.getAttribute('fixed')
            fixedRefValue = refNode.getAttribute('fixed')
            if fixedValue != None and fixedRefValue != None and fixedValue != fixedRefValue:
                self._addError('Fixed value %s of attribute does not match fixed value %s of reference!' % (repr(fixedValue), repr(fixedRefValue)), node)
        else:
            self._addError('Reference %s not found!' % repr(baseNsName), node)
        return

    def _checkType(self, node, typeAttrName, dict, typeNsName=None):
        baseNsName = node.getQNameAttribute(typeAttrName)
        self._checkBaseType(node, baseNsName, dict, typeNsName)
        return baseNsName

    def _checkBaseType(self, node, baseNsName, dict, typeNsName=None):
        if not dict.has_key(baseNsName) and baseNsName != (XSD_NAMESPACE, 'anySimpleType'):
            self._addError('Definition of type %s not found!' % repr(baseNsName), node)
        elif typeNsName != None:
            if typeNsName == (XSD_NAMESPACE, 'simpleContent'):
                if node.getNsName() == (XSD_NAMESPACE, 'restriction'):
                    if baseNsName != (XSD_NAMESPACE, 'anySimpleType') and dict[baseNsName].getNsName() == (XSD_NAMESPACE, 'complexType') and dict[baseNsName].getFirstChild().getNsName() == typeNsName:
                        pass
                    else:
                        self._addError('Referred type %s must be a complex type with simple content!' % repr(baseNsName), node)
                elif baseNsName == (XSD_NAMESPACE, 'anySimpleType') or dict[baseNsName].getNsName() == (XSD_NAMESPACE, 'simpleType') or dict[baseNsName].getNsName() == (XSD_NAMESPACE, 'complexType') and dict[baseNsName].getFirstChild().getNsName() == typeNsName:
                    pass
                else:
                    self._addError('Referred type %s must be a simple type or a complex type with simple content!' % repr(baseNsName), node)
            elif typeNsName == (XSD_NAMESPACE, 'simpleType') and baseNsName == (XSD_NAMESPACE, 'anySimpleType'):
                pass
            elif dict[baseNsName].getNsName() != typeNsName:
                self._addError('Referred type %s must be a %s!' % (repr(baseNsName), repr(typeNsName)), node)
        return

    def _checkKeyRef(self, keyrefNode, dict):
        baseNsName = keyrefNode.getQNameAttribute('refer')
        if not dict.has_key(baseNsName):
            self._addError('keyref refers unknown key %s!' % repr(baseNsName), keyrefNode)
        else:
            keyNode = dict[baseNsName]['Node']
            if keyNode.getNsName() not in ((XSD_NAMESPACE, 'key'), (XSD_NAMESPACE, 'unique')):
                self._addError('reference to non-key constraint %s!' % repr(baseNsName), keyrefNode)
            if len(keyrefNode.getChildrenNS(XSD_NAMESPACE, 'field')) != len(keyNode.getChildrenNS(XSD_NAMESPACE, 'field')):
                self._addError('key/keyref field size mismatch!', keyrefNode)

    def _checkOccurs(self, node):
        minOccurs = node.getAttributeOrDefault('minOccurs', '1')
        maxOccurs = node.getAttributeOrDefault('maxOccurs', '1')
        if maxOccurs != 'unbounded':
            if string.atoi(minOccurs) > string.atoi(maxOccurs):
                self._addError('Attribute minOccurs > maxOccurs!', node)

    def _checkNodeId(self, node, unambiguousPerFile=1):
        if node.hasAttribute('id'):
            if unambiguousPerFile:
                nodeId = (
                 node.getAbsUrl(), collapseString(node['id']))
            else:
                nodeId = collapseString(node['id'])
            if not self.xsdIdDict.has_key(nodeId):
                self.xsdIdDict[nodeId] = node
            else:
                self._addError('There are multiple occurences of ID value %s!' % repr(nodeId), node)

    def _getFacetType(self, node, parentNodeList, xsdTypeDict):
        baseNsName = node.getQNameAttribute('base')
        try:
            baseNode = xsdTypeDict[baseNsName]
        except:
            self._addError('Base type %s must be an atomic simple type definition or a builtin type!' % repr(baseNsName), node)
            return

        if baseNode in parentNodeList:
            self._addError('Circular type definition (type is contained in its own type hierarchy)!', node)
            return
        if baseNode.getNsName() == (XSD_NAMESPACE, 'simpleType'):
            if baseNode.getAttribute('facetType') != None:
                facetType = baseNode.qName2NsName(baseNode['facetType'], 1)
                node.getParentNode()['facetType'] = node.nsName2QName(facetType)
                return facetType
            else:
                for baseNodeType in ('list', 'union'):
                    if baseNode.getFirstChildNS(XSD_NAMESPACE, baseNodeType) != None:
                        return (
                         XSD_NAMESPACE, baseNodeType)
                else:
                    parentNodeList.append(node)
                    return self._getFacetType(baseNode.getFirstChildNS(XSD_NAMESPACE, 'restriction'), parentNodeList, xsdTypeDict)
        else:
            self._addError('Base type %s must be an atomic simple type definition or a builtin type!' % repr(baseNsName), node)
            return
        return
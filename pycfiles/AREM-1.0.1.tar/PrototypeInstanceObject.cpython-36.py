# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\PrototypeInstanceObject.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 10867 bytes
from arelle import XmlUtil
from arelle.ModelValue import QName
from arelle.ModelObject import ModelObject
Aspect = None

class FactPrototype:

    def __init__(self, v, aspectValues=None):
        global Aspect
        if Aspect is None:
            from arelle.ModelFormulaObject import Aspect
        else:
            self.modelXbrl = v.modelXbrl
            if aspectValues is None:
                aspectValues = {}
            else:
                self.aspectEntryObjectId = aspectValues.get('aspectEntryObjectId', None)
                if Aspect.CONCEPT in aspectValues:
                    qname = aspectValues[Aspect.CONCEPT]
                    self.qname = qname
                    self.concept = v.modelXbrl.qnameConcepts.get(qname)
                    self.isItem = self.concept is not None and self.concept.isItem
                    self.isTuple = self.concept is not None and self.concept.isTuple
                else:
                    self.qname = None
                    self.concept = None
                    self.isItem = False
                    self.isTuple = False
                if Aspect.LOCATION in aspectValues:
                    self.parent = aspectValues[Aspect.LOCATION]
                    try:
                        self.isTuple = self.parent.isTuple
                    except AttributeError:
                        self.isTuple = False

                self.parent = v.modelXbrl.modelDocument.xmlRootElement
            self.isNumeric = self.concept is not None and self.concept.isNumeric
            self.context = ContextPrototype(v, aspectValues)
            if Aspect.UNIT in aspectValues:
                self.unit = UnitPrototype(v, aspectValues)
            else:
                self.unit = None
        self.factObjectId = None

    def clear(self):
        if self.context is not None:
            self.context.clear()
        self.__dict__.clear()

    def objectId(self):
        return '_factPrototype_' + str(self.qname)

    def getparent(self):
        return self.parent

    @property
    def propertyView(self):
        dims = self.context.qnameDims
        return (
         (
          'concept', str(self.qname) if self.concept is not None else 'not specified'),
         ('dimensions', '({0})'.format(len(dims)),
          tuple((dimVal.propertyView if dimVal is not None else (str(dim.qname), 'None')) for dim, dimVal in sorted((dims.items()), key=(lambda i: i[0])) if hasattr(dimVal, 'propertyView'))) if dims else ())

    @property
    def viewConcept(self):
        return self


class ContextPrototype:

    def __init__(self, v, aspectValues):
        self.modelXbrl = v.modelXbrl
        self.segDimVals = {}
        self.scenDimVals = {}
        self.qnameDims = {}
        self.entityIdentifierHash = self.entityIdentifier = None
        self.isStartEndPeriod = self.isInstantPeriod = self.isForeverPeriod = False
        for aspect, aspectValue in aspectValues.items():
            if aspect == Aspect.PERIOD_TYPE:
                if aspectValue == 'forever':
                    self.isForeverPeriod = True
                else:
                    if aspectValue == 'instant':
                        self.isInstantPeriod = True
                    elif aspectValue == 'duration':
                        self.isStartEndPeriod = True
            elif aspect == Aspect.START:
                self.isStartEndPeriod = True
                self.startDatetime = aspectValue
            elif aspect == Aspect.END:
                self.isStartEndPeriod = True
                self.endDatetime = aspectValue
            elif aspect == Aspect.INSTANT:
                self.isInstantPeriod = True
                self.endDatetime = self.instantDatetime = aspectValue
            elif isinstance(aspect, QName):
                try:
                    contextElement = aspectValue.contextElement
                    aspectValue = aspectValue.memberQname or aspectValue.typedMember
                except AttributeError:
                    contextElement = v.modelXbrl.qnameDimensionContextElement.get(aspect)

                if v.modelXbrl.qnameDimensionDefaults.get(aspect) != aspectValue:
                    try:
                        dimConcept = v.modelXbrl.qnameConcepts[aspect]
                        dimValPrototype = DimValuePrototype(v, dimConcept, aspect, aspectValue, contextElement)
                        self.qnameDims[aspect] = dimValPrototype
                        if contextElement != 'scenario':
                            self.segDimVals[dimConcept] = dimValPrototype
                        else:
                            self.scenDimVals[dimConcept] = dimValPrototype
                    except KeyError:
                        pass

            else:
                if isinstance(aspectValue, ModelObject):
                    if aspect == Aspect.PERIOD:
                        context = aspectValue.getparent()
                        for contextPeriodAttribute in ('isForeverPeriod', 'isStartEndPeriod',
                                                       'isInstantPeriod', 'startDatetime',
                                                       'endDatetime', 'instantDatetime',
                                                       'periodHash'):
                            setattr(self, contextPeriodAttribute, getattr(context, contextPeriodAttribute, None))

                    elif aspect == Aspect.ENTITY_IDENTIFIER:
                        context = aspectValue.getparent().getparent()
                        for entityIdentAttribute in ('entityIdentifier', 'entityIdentifierHash'):
                            setattr(self, entityIdentAttribute, getattr(context, entityIdentAttribute, None))

    def clear(self):
        try:
            for dim in self.qnameDims.values():
                if isinstance(dim, DimValuePrototype):
                    dim.clear()

        except AttributeError:
            pass

        self.__dict__.clear()

    def dimValue(self, dimQname):
        """(ModelDimension or QName) -- ModelDimension object if dimension is reported (in either context element), or QName of dimension default if there is a default, otherwise None"""
        try:
            return self.qnameDims[dimQname]
        except KeyError:
            try:
                return self.modelXbrl.qnameDimensionDefaults[dimQname]
            except KeyError:
                return

    def dimValues(self, contextElement, oppositeContextElement=False):
        if not oppositeContextElement:
            if contextElement == 'segment':
                return self.segDimVals
            return self.scenDimVals
        else:
            if contextElement == 'segment':
                return self.scenDimVals
            return self.segDimVals

    def nonDimValues(self, contextElement):
        return []

    def isEntityIdentifierEqualTo(self, cntx2):
        return self.entityIdentifierHash is None or self.entityIdentifierHash == cntx2.entityIdentifierHash

    def isPeriodEqualTo(self, cntx2):
        if self.isForeverPeriod:
            return cntx2.isForeverPeriod
        else:
            if self.isStartEndPeriod:
                if not cntx2.isStartEndPeriod:
                    return False
                else:
                    return self.startDatetime == cntx2.startDatetime and self.endDatetime == cntx2.endDatetime
            if self.isInstantPeriod:
                if not cntx2.isInstantPeriod:
                    return False
                else:
                    return self.instantDatetime == cntx2.instantDatetime
            return False


class DimValuePrototype:

    def __init__(self, v, dimConcept, dimQname, mem, contextElement):
        from arelle.ModelValue import QName
        if dimConcept is None:
            dimConcept = v.modelXbrl.qnameConcepts.get(dimQname)
        else:
            self.dimension = dimConcept
            self.dimensionQname = dimQname
            self.contextElement = contextElement
            if isinstance(mem, QName):
                self.isExplicit = True
                self.isTyped = False
                self.memberQname = mem
                self.member = v.modelXbrl.qnameConcepts.get(mem)
                self.typedMember = None
            else:
                self.isExplicit = False
            self.isTyped = True
            self.typedMember = mem
            self.memberQname = None
            self.member = None

    def clear(self):
        self.__dict__.clear()

    @property
    def propertyView(self):
        if self.isExplicit:
            return (str(self.dimensionQname), str(self.memberQname))
        else:
            return (
             str(self.dimensionQname),
             XmlUtil.xmlstring((self.typedMember), stripXmlns=True, prettyPrint=True) if isinstance(self.typedMember, ModelObject) else 'None')


class UnitPrototype:

    def __init__(self, v, aspectValues):
        self.modelXbrl = v.modelXbrl
        self.hash = self.measures = self.isSingleMeasure = None
        for aspect, aspectValue in aspectValues.items():
            if aspect == Aspect.UNIT:
                for unitAttribute in ('measures', 'hash', 'isSingleMeasure', 'isDivide'):
                    setattr(self, unitAttribute, getattr(aspectValue, unitAttribute, None))

    def clear(self):
        self.__dict__.clear()

    def isEqualTo(self, unit2):
        if unit2 is None or unit2.hash != self.hash:
            return False
        else:
            return unit2 is self or self.measures == unit2.measures

    @property
    def propertyView(self):
        measures = self.measures
        if measures[1]:
            return tuple(('mul', m) for m in measures[0]) + tuple(('div', d) for d in measures[1])
        else:
            return tuple(('measure', m) for m in measures[0])


class XbrlPrototype:

    def __init__(self, modelManager, uri, *arg, **kwarg):
        self.modelManager = modelManager
        self.errors = []
        self.skipDTS = False
        from arelle.PrototypeDtsObject import DocumentPrototype
        self.modelDocument = DocumentPrototype(self, uri)

    def close(self):
        self.modelDocument.clear()
        self.__dict__.clear()
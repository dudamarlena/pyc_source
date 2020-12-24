# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cabio/pathways.py
# Compiled at: 2010-06-24 16:12:02
import cabig.cabio.CaBioWSQueryService_client as services
from cabig.cacore.ws.proxy import *
schema = services.ns5

class BiochemicalReaction(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.BiochemicalReaction'
    id = ProxyAttr('id')
    source = ProxyAttr('source')
    evidenceCodeCollection = ProxyAssoc('evidenceCodeCollection', True)
    participantCollection = ProxyAssoc('participantCollection', True)
    pathwayCollection = ProxyAssoc('pathwayCollection', True)
    referenceCollection = ProxyAssoc('referenceCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.BiochemicalReaction_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class ComplexComponent(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.ComplexComponent'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)
    complex = ProxyAssoc('complex', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.ComplexComponent_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class ComplexEntity(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.ComplexEntity'
    id = ProxyAttr('id')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)
    complexComponentCollection = ProxyAssoc('complexComponentCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.ComplexEntity_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Condition(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Condition'
    id = ProxyAttr('id')
    name = ProxyAttr('name')
    interaction = ProxyAssoc('interaction', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Condition_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class EntityAccession(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.EntityAccession'
    accession = ProxyAttr('accession')
    database = ProxyAttr('database')
    id = ProxyAttr('id')
    physicalEntityCollection = ProxyAssoc('physicalEntityCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.EntityAccession_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class EntityName(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.EntityName'
    id = ProxyAttr('id')
    name = ProxyAttr('name')
    physicalEntityCollection = ProxyAssoc('physicalEntityCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.EntityName_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class FamilyMember(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.FamilyMember'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)
    familyCollection = ProxyAssoc('familyCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.FamilyMember_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class GeneRegulation(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.GeneRegulation'
    id = ProxyAttr('id')
    source = ProxyAttr('source')
    evidenceCodeCollection = ProxyAssoc('evidenceCodeCollection', True)
    participantCollection = ProxyAssoc('participantCollection', True)
    pathwayCollection = ProxyAssoc('pathwayCollection', True)
    referenceCollection = ProxyAssoc('referenceCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.GeneRegulation_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Input(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Input'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Input_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Interaction(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Interaction'
    id = ProxyAttr('id')
    source = ProxyAttr('source')
    evidenceCodeCollection = ProxyAssoc('evidenceCodeCollection', True)
    participantCollection = ProxyAssoc('participantCollection', True)
    pathwayCollection = ProxyAssoc('pathwayCollection', True)
    referenceCollection = ProxyAssoc('referenceCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Interaction_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Macroprocess(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Macroprocess'
    id = ProxyAttr('id')
    source = ProxyAttr('source')
    name = ProxyAttr('name')
    evidenceCodeCollection = ProxyAssoc('evidenceCodeCollection', True)
    participantCollection = ProxyAssoc('participantCollection', True)
    pathwayCollection = ProxyAssoc('pathwayCollection', True)
    referenceCollection = ProxyAssoc('referenceCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Macroprocess_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class NegativeControl(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.NegativeControl'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.NegativeControl_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Output(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Output'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Output_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class Participant(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.Participant'
    id = ProxyAttr('id')
    interaction = ProxyAssoc('interaction', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.Participant_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class PathwayReference(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.PathwayReference'
    id = ProxyAttr('id')
    source = ProxyAttr('source')
    evidenceCodeCollection = ProxyAssoc('evidenceCodeCollection', True)
    participantCollection = ProxyAssoc('participantCollection', True)
    pathwayCollection = ProxyAssoc('pathwayCollection', True)
    referenceCollection = ProxyAssoc('referenceCollection', True)
    pathway = ProxyAssoc('pathway', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.PathwayReference_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class PhysicalEntity(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.PhysicalEntity'
    id = ProxyAttr('id')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.PhysicalEntity_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class PhysicalParticipant(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.PhysicalParticipant'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.PhysicalParticipant_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class PositiveControl(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.PositiveControl'
    id = ProxyAttr('id')
    activityState = ProxyAttr('activityState')
    location = ProxyAttr('location')
    postTranslationalMod = ProxyAttr('postTranslationalMod')
    interaction = ProxyAssoc('interaction', False)
    physicalEntity = ProxyAssoc('physicalEntity', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.PositiveControl_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class ProteinEntity(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.ProteinEntity'
    id = ProxyAttr('id')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)
    proteinCollection = ProxyAssoc('proteinCollection', True)
    subunitCollection = ProxyAssoc('subunitCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.ProteinEntity_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class ProteinSubunit(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.ProteinSubunit'
    id = ProxyAttr('id')
    startPosition = ProxyAttr('startPosition')
    stopPosition = ProxyAttr('stopPosition')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)
    proteinCollection = ProxyAssoc('proteinCollection', True)
    subunitCollection = ProxyAssoc('subunitCollection', True)
    whole = ProxyAssoc('whole', False)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.ProteinSubunit_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class RNAEntity(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.RNAEntity'
    id = ProxyAttr('id')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)
    nucleicAcidSequenceCollection = ProxyAssoc('nucleicAcidSequenceCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.RNAEntity_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return


class SmallMoleculeEntity(WSBean):
    arrayType = services.ns1.ArrayOf_xsd_anyType_Def(None).pyclass
    className = 'gov.nih.nci.cabio.pathways.SmallMoleculeEntity'
    id = ProxyAttr('id')
    entityAccessionCollection = ProxyAssoc('entityAccessionCollection', True)
    entityNameCollection = ProxyAssoc('entityNameCollection', True)
    memberCollection = ProxyAssoc('memberCollection', True)
    physicalParticipantCollection = ProxyAssoc('physicalParticipantCollection', True)
    agentCollection = ProxyAssoc('agentCollection', True)

    def __init__(self, holder=None, service=None, **kwargs):
        if not holder:
            holder = schema.SmallMoleculeEntity_Def(None).pyclass()
        WSBean.__init__(self, holder, service=service, **kwargs)
        return
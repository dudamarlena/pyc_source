# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/interfaces.py
# Compiled at: 2015-11-03 03:53:39
from zope.interface import Interface

class IBikaHealth(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    A layer specific for this add-on product.
    This interface is referred in browserlayer.xml.
    All views and viewlets register against this layer will appear on
    your Plone site only when the add-on installer has been run.
    """
    pass


class IPatient(Interface):
    """Patient"""
    pass


class IPatients(Interface):
    """Patient folder"""
    pass


class IDoctor(Interface):
    """Doctor"""
    pass


class IDoctors(Interface):
    """Doctor folder"""
    pass


class IDrugs(Interface):
    """"""
    pass


class IDrugProhibitions(Interface):
    """"""
    pass


class IImmunizations(Interface):
    """"""
    pass


class ISymptoms(Interface):
    """"""
    pass


class IDiseases(Interface):
    """"""
    pass


class IAetiologicAgents(Interface):
    """"""
    pass


class ITreatments(Interface):
    """"""
    pass


class IVaccinationCenter(Interface):
    """"""
    pass


class IVaccinationCenters(Interface):
    """"""
    pass


class ICaseStatuses(Interface):
    """"""
    pass


class ICaseOutcomes(Interface):
    """"""
    pass


class ICaseSyndromicClassifications(Interface):
    """"""
    pass


class IEpidemiologicalYears(Interface):
    """"""
    pass


class IIdentifierTypes(Interface):
    """"""
    pass


class IInsuranceCompany(Interface):
    """"""
    pass


class IInsuranceCompanies(Interface):
    """"""
    pass


class IEthnicity(Interface):
    """
    Ethnicity content type marker
    """
    pass


class IEthnicities(Interface):
    """
    Ethnicities content folder marker
    """
    pass
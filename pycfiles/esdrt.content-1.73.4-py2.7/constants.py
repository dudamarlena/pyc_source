# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/constants.py
# Compiled at: 2019-05-21 05:08:42
""" LDAP Role mapping constants.
"""
LDAP_BASE = 'extranet-esd'
LDAP_SECRETARIAT = LDAP_BASE + '-secretariat'
LDAP_ESD = LDAP_BASE + '-esdreview'
LDAP_LR = LDAP_ESD + '-leadreview'
LDAP_RE = LDAP_ESD + '-reviewexp'
LDAP_GHG = LDAP_BASE + '-ghginv'
LDAP_QE = LDAP_GHG + '-qualityexpert'
LDAP_SR = LDAP_GHG + '-sr'
LDAP_COUNTRIES = LDAP_BASE + '-countries'
LDAP_MSA = LDAP_COUNTRIES + '-msa'
LDAP_MSE = LDAP_COUNTRIES + '-msexpert'
ROLE_MSA = 'MSAuthority'
ROLE_MSE = 'MSExpert'
ROLE_LR = 'LeadReviewer'
ROLE_RP1 = 'ReviewerPhase1'
ROLE_RP2 = 'ReviewerPhase2'
ROLE_QE = 'QualityExpert'
ROLE_SE = 'SectorExpert'
ROLE_RE = 'ReviewExpert'
ROLE_CP = 'CounterPart'
__all__ = ('LDAP_BASE', 'LDAP_SECRETARIAT', 'LDAP_ESD', 'LDAP_GHG', 'LDAP_COUNTRIES',
           'LDAP_LR', 'LDAP_RE', 'LDAP_QE', 'LDAP_SR', 'LDAP_MSA', 'LDAP_MSE', 'ROLE_MSA',
           'ROLE_MSE', 'ROLE_LR', 'ROLE_RP1', 'ROLE_RP2', 'ROLE_QE', 'ROLE_SE', 'ROLE_RE',
           'ROLE_CP')
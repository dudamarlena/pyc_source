# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/Extensions/transitionscripts.py
# Compiled at: 2011-10-12 13:31:11


def schoolDirSend(self, state_change):
    """ sends an email to the school's director """
    print 'schoolDirSend called !!!'


def schoolDirApprove(self, state_change):
    """ school's director sends an email to the contributor to inform him """
    print 'schoolDirApprove called !!!'


def DIPDirSend(self, state_change):
    """ sends an email to the DIP's responsible for RD (Andenmatten) """
    print 'DIPDirSend called !!!'


def acceptAttribution(self, state_change):
    """ tests if all attribution objects in this projet are published
    If it's the case : it sends an email to contributors and supervisors """
    print 'acceptAttribution called !!!'


def rejectAttribution(self, state_change):
    """ schoolDir reject attribution 
    it sends an email to the contributor and RD """
    print 'rejectAttribution called !!!'


def reviseAttribution(self, state_change):
    """ schoolDir ask for a revision of the attribution 
    it sends an email to the contributor and RD """
    print 'reviseAttribution called !!!'


def testAllAttributions(self, state_change):
    u""" tests if all attribution objects in this projet are accepted (peut être un mix 
    entre accepted et renounced)
    If it's the case : it sends an email to contributors, schools and supervisors 
    et change l'état du projet à "on" (en cours)"""
    print 'testAllAttributions called !!!'


def bilanReject(self, state_change):
    """ sends an email to contributors to ask for a complement on the bilan """
    print 'bilanReject called !!!'


def bilanFeedback(self, state_change):
    """ sends an email to contributors to give a feedback on the bilan """
    print 'bilanFeedback called !!!'


def notesFeedback(self, state_change):
    """ sends an email to contributors to give a feedback on meeting notes """
    print 'notesFeedback called !!!'
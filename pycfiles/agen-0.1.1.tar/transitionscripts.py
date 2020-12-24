# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/serge/Documents/inf/p4.2.4/rd/src/ageliaco.rd2/ageliaco/rd2/Extensions/transitionscripts.py
# Compiled at: 2013-02-25 07:53:40
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import log
from Products.CMFCore.utils import getToolByName

def archiveCycle(self, state_change):
    """ sends an email to the school's director """
    print 'archiveCycle called !!!'


def finaliseCycle(self, state_change):
    """ sends an email to the school's director """
    print 'archiveCycle called !!!'


def attributeCycle(self, state_change):
    """ sends an email to the school's director """
    print 'attributeCycle called !!!'


def publishProjet(self, state_change):
    """ finish any active cycle """
    print 'attributeCycle called !!!'


def activateCycle(self, state_change):
    """ activate Cycle and moving it to known projet or new one """
    print 'activateCycle called !!!'
    dest_folder = None
    workflowTool = getToolByName(self, 'portal_workflow')
    contentObject = state_change.object
    parent = contentObject.aq_parent
    parentState = workflowTool.getStatusOf('rd2.projet-workflow', parent)['review_state']
    if parentState == 'encours':
        return
    else:
        portal = self.portal_url.getPortalObject()
        catalog = getToolByName(portal, 'portal_catalog')
        cat = catalog(portal_type='ageliaco.rd2.projets', review_state='published')
        if not len(cat):
            log('No ageliaco.rd2.projets published => cannot migrate cycle to projet !')
            return
        projets = cat[0].getObject()
        objectOwner = contentObject.Creator()
        projetPath = contentObject.projet
        if not projetPath:
            if 'depot-de-projet' in parent.absolute_url().split('/'):
                projet = createContentInContainer(projets, 'ageliaco.rd2.projet', title=contentObject.Title, duration=1, presentation=' ')
            else:
                contentObject.projet = parent.absolute_url()
        else:
            projetId = projetPath.split('/')[(-1)]
            print projetPath, projetId, projets
            projet = projets[projetId]
            if not projet:
                log('Problem, cannot find projet %s in %s !' % (projetPath, projets.id))
                return
            parent = contentObject.aq_parent
            print 'Parent : ', parent, contentObject.id, parent.objectIds()
            try:
                print 'try cut OK!'
                projet.manage_pasteObjects(parent.manage_cutObjects(contentObject.id))
            except:
                print "couldn't cut => then copy instead"
                projet.manage_pasteObjects(parent.manage_copyObjects(contentObject.id))

        return
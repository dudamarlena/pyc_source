# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/tests/base.py
# Compiled at: 2008-11-11 20:26:20
from zope.interface import implements
from Testing import ZopeTestCase as ztc
from Products.CMFPlone.tests import PloneTestCase
from Products.SecureMailHost.SecureMailHost import SecureMailHost as Base
from Products.MailHost.interfaces import IMailHost
ztc.installProduct('eCards')
PRODUCTS = [
 'eCards']
PloneTestCase.setupPloneSite(products=PRODUCTS)

class eCardTestCase(PloneTestCase.PloneTestCase):
    """Base class for integration tests for the 'eCards' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
    __module__ = __name__

    def setupCollection(self):
        """We're needing to frequently setup an eCardCollection object
           We abstract this step out to our test base class, to save on the repetitive code.
        """
        self.folder.invokeFactory('eCardCollection', 'collection')

    def setupContainedECard(self):
        """We're needing to frequently setup a contained eCard object within a collection.
           We abstract this step out to our test base class, to save on the repetitive code.
        """
        if 'collection' not in self.folder.objectIds():
            self.setupCollection()
        self.folder.collection.invokeFactory('eCard', 'ecard')

    def massECardProducer(self, numCards):
        """Some tests will depend upon a mass of
           eCards existing.  This method accepts
           an integer with a number of 
        """
        if 'collection' not in self.folder.objectIds():
            self.setupCollection()
        self.setRoles(['Manager'])
        if numCards:
            for cardidx in range(1, numCards):
                self.folder.collection.invokeFactory('eCard', 'ecard%s' % str(cardidx))
                self.portal.portal_workflow.doActionFor(eval('self.folder.collection.ecard%s' % str(cardidx)), 'publish')

        self.logout()
        self.login('test_user_1_')

    def determineRemainderOffset(self, numCards):
        """If we determine on our eCard Collection that we want 4 cards per row,
           but we've add 5 cards.  The two dimensional array will look like:
             [[1,2,3,4],[5,,,,]]
           
           Whereas if the user wants 4 cards per row and there are 4 cards, the array
           looks like:
           
             [[1,2,3,4],]
           
           This helper method helps us to determine whether we need to account for
           that remainder trailing subrow in our tests.
        """
        if numCards % self.folder.collection.getECardsPerRow() != 0:
            return 1
        return 0


class MailHostMock(Base):
    """
    mock up the send method so that emails do not actually get sent
    during unit tests we can use this to verify that the notification
    process is still working as expected
    """
    __module__ = __name__
    implements(IMailHost)

    def __init__(self, id):
        Base.__init__(self, id, smtp_notls=True)
        self.mail_text = ''
        self.n_mails = 0
        self.mto = ''
        self.mfrom = ''
        self.subject = ''

    def send(self, mail_text, full_to_address, full_from_address, subject):
        self.mail_text = mail_text
        self.mto = full_to_address
        self.mfrom = full_from_address
        self.subject = subject
        self.n_mails += 1
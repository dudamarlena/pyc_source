# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/tests/test_browserviews.py
# Compiled at: 2008-11-11 20:26:20
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from base64 import decodestring
from Products.eCards.tests import base
from Products.CMFCore.utils import getToolByName
from Products.MailHost.interfaces import IMailHost
from Globals import package_home
PACKAGE_HOME = package_home(globals())

def loadImage(name, size=0):
    """Load image from testing directory
    """
    path = os.path.join(PACKAGE_HOME, 'input', name)
    fd = open(path, 'rb')
    data = fd.read()
    fd.close()
    return data


TEST_GIF = loadImage('test.gif')

class TestCollectionBrowserViews(base.eCardTestCase):
    """ Ensure that our eCardCollection's browser
        view
    """
    __module__ = __name__

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow
        self.setupCollection()
        self.view = self.folder.collection.restrictedTraverse('ecardcollection_browserview')

    def testCollectionGetECardsForView(self):
        self.setupContainedECard()
        self.failUnless(len(self.folder.collection.objectIds()))
        self.failIf(self.view.getCardsForView())
        self.setRoles(['Manager'])
        self.workflow.doActionFor(self.folder.collection.ecard, 'publish')
        self.failUnless(self.view.getCardsForView())
        self.logout()
        self.login('test_user_1_')

    def testCollectionViewECardsDictReturnsNeededData(self):
        self.setupContainedECard()
        self.setRoles(['Manager'])
        self.workflow.doActionFor(self.folder.collection.ecard, 'publish')
        self.logout()
        self.login('test_user_1_')
        cardDict = self.view.getCardsForView()[0][0]
        for key in ('title', 'description', 'thumbnail_html', 'url', 'width'):
            self.failUnless(cardDict.has_key(key), 'Key %s does not exist                 in our card dict' % key)

    def testGetECardsPerRowReturnsEmptyListWithNoECards(self):
        self.assertEqual(5, self.folder.collection.getECardsPerRow())
        self.failIf(self.view.getCardsForView())

    def testGetECardsForViewTwoDimensionalArray(self):
        numCards = 7
        self.massECardProducer(numCards)
        cardsInCollection = len(self.folder.collection.objectIds())
        self.assertEqual(numCards - 1, cardsInCollection)
        self.assertEqual(5, self.folder.collection.getECardsPerRow())
        self.assertEqual(len(self.view.getCardsForView()), cardsInCollection / self.folder.collection.getECardsPerRow() + self.determineRemainderOffset(cardsInCollection))
        self.assertEqual(len(self.view.getCardsForView()[(-1)]), self.folder.collection.getECardsPerRow())
        self.assertEqual(len([ eCardDict for eCardDict in self.view.getCardsForView()[(-1)] if eCardDict != '' ]), cardsInCollection % self.folder.collection.getECardsPerRow() or self.folder.collection.getECardsPerRow())
        self.folder.collection.setECardsPerRow(3)
        self.assertEqual(len(self.view.getCardsForView()), cardsInCollection / self.folder.collection.getECardsPerRow() + self.determineRemainderOffset(cardsInCollection))
        self.assertEqual(len(self.view.getCardsForView()[(-1)]), self.folder.collection.getECardsPerRow())
        self.assertEqual(len([ eCardDict for eCardDict in self.view.getCardsForView()[(-1)] if eCardDict != '' ]), cardsInCollection % self.folder.collection.getECardsPerRow() or self.folder.collection.getECardsPerRow())
        self.folder.collection.setECardsPerRow(6)
        self.assertEqual(len(self.view.getCardsForView()), cardsInCollection / self.folder.collection.getECardsPerRow() + self.determineRemainderOffset(cardsInCollection))
        self.assertEqual(len(self.view.getCardsForView()[(-1)]), cardsInCollection % self.folder.collection.getECardsPerRow() or self.folder.collection.getECardsPerRow())

    def testAppropriateThumbSchemaImageReturnedByView(self):
        self.setupContainedECard()
        self.setRoles(['Manager'])
        self.workflow.doActionFor(self.folder.collection.ecard, 'publish')
        self.folder.collection.ecard.setImage(TEST_GIF, mimetype='image/gif', filename='test.gif')
        self.failUnless('image_thumb' in self.view.getCardsForView()[0][0]['thumbnail_html'])
        self.folder.collection.ecard.setThumb(TEST_GIF, mimetype='image/gif', filename='testthumb.gif')
        self.failUnless('thumb_thumb' in self.view.getCardsForView()[0][0]['thumbnail_html'])
        self.logout()
        self.login('test_user_1_')

    def testThumbSizeOverrideableOnCollectionLevel(self):
        self.setupContainedECard()
        self.setRoles(['Manager'])
        self.workflow.doActionFor(self.folder.collection.ecard, 'publish')
        self.folder.collection.ecard.setImage(TEST_GIF, mimetype='image/gif', filename='test.gif')
        self.failUnless('image_thumb' in self.view.getCardsForView()[0][0]['thumbnail_html'])
        self.folder.collection.ecard.setThumb(TEST_GIF, mimetype='image/gif', filename='testthumb.gif')
        self.failUnless('thumb_thumb' in self.view.getCardsForView()[0][0]['thumbnail_html'])
        self.folder.collection.setThumbSize('mini')
        self.failUnless('thumb_mini' in self.view.getCardsForView()[0][0]['thumbnail_html'])
        self.folder.collection.setThumbSize('original')
        self.failUnless('thumb' in self.view.getCardsForView()[0][0]['thumbnail_html'])

    def testViewReturnsECardsWithinCollectionOnly(self):
        self.setupContainedECard()
        self.folder.invokeFactory('eCardCollection', 'mycollection')
        self.folder.mycollection.invokeFactory('eCard', 'myecard')
        self.setRoles(['Manager'])
        self.workflow.doActionFor(self.folder.collection.ecard, 'publish')
        self.workflow.doActionFor(self.folder.mycollection.myecard, 'publish')
        self.logout()
        self.login('test_user_1_')
        self.failIf(len(self.folder.collection.objectIds()) < len([ eCardDict for eCardDict in self.view.getCardsForView()[0] if eCardDict != '' ]))

    def testViewReturnsECardsAsOrderedByPositionInParent(self):
        for i in range(4):
            self.folder.collection.invokeFactory('eCard', 'ecard%s' % i)
            self.setRoles(['Manager'])
            self.workflow.doActionFor(self.folder.collection[('ecard%s' % i)], 'publish')

        self.folder.collection.moveObjectsByDelta(['ecard2'], -100)
        self.folder.collection.moveObjectsByDelta(['ecard1'], 100)
        for i in range(4):
            self.folder.collection[('ecard%s' % i)].reindexObject(idxs=['getObjPositionInParent'])

        self.logout()
        self.login('test_user_1_')
        self.assertEqual([ ecard_obj.absolute_url() for ecard_obj in self.folder.collection.objectValues() ], [ ecard['url'] for ecard in self.view.getCardsForView()[0] if ecard != '' ])


class TestECardPopupBrowserViews(base.eCardTestCase):
    """ Ensure that our eCardCollection's browser
        view
    """
    __module__ = __name__

    def afterSetUp(self):
        sm = self.portal.getSiteManager()
        sm.registerUtility(base.MailHostMock('MailHost'), IMailHost)
        self.mailhost = getToolByName(self.portal, 'MailHost')
        self.setupCollection()
        self.setupContainedECard()
        self.view = self.folder.collection.ecard.restrictedTraverse('ecardpopup_browserview')

    def testPopupViewSendsEmail(self):
        mail_to = 'jane@example.com'
        mail_from = 'john@example.com'
        options = {'subject': 'Jane has sent you an eCard!', 'friend_first_name': 'Jane', 'comment': "You'll love this picture!", 'sender_first_name': 'John', 'credits': 'Photo courtesy of Plone Foundation', 'emailAppendedMessage': 'Make a contribution at Plone.org', 'image_url': 'http://nohost/ecardimage'}
        self.view.sendECard(message=self.portal.portal_skins.ecards_templates.email_template(**options), full_to_address=mail_to, full_from_address=mail_from, subject=options['subject'])
        self.assertEqual(self.mailhost.n_mails, 1)
        self.assertEqual(self.mailhost.mto, mail_to)
        self.assertEqual(self.mailhost.mfrom, mail_from)
        decoded_mail_text = decodestring(self.mailhost.mail_text)
        for v in options.values():
            self.failUnless(v in decoded_mail_text, 'The value %s was not found in the mail text')

    def testPopupViewStripNewLines(self):
        for s in ('Message', '\nMessage', '\rMessage', '\n\rMessage\n\r'):
            self.assertEqual('Message', self.view.stripNewLines(s))


if __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCollectionBrowserViews))
    suite.addTest(makeSuite(TestECardPopupBrowserViews))
    return suite
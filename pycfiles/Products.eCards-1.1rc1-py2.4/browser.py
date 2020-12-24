# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/browser.py
# Compiled at: 2008-11-11 20:26:20
import email
from email.Header import Header
from email.MIMEText import MIMEText
from email.Utils import formatdate
from zope.interface import implements
from Acquisition import aq_parent
from Products import Five
from Products.CMFCore.utils import getToolByName
from Products.eCards.interfaces import IECardCollectionView, IECardPopupView

class eCardCollectionView(Five.BrowserView):
    """See IECardCollectionView
    """
    __module__ = __name__
    implements(IECardCollectionView)

    def _tag_method(self, ecard):
        """Gets the preferred tag method 
           on the object dependent upon 
           the existing of an image in thumb field
        """
        if ecard.getThumb():
            return ecard.thumbtag
        else:
            return ecard.tag

    def _thumb_size(self, ecard):
        """Gets the preferred thumb tag
           method
        """
        collection = aq_parent(ecard)
        thumbName = collection.getThumbSize()
        if thumbName == 'original':
            return ''
        return '%s' % thumbName

    def getCardsForView(self):
        """See IECardCollectionView"""
        catalog = getToolByName(self.context, 'portal_catalog')
        params = {'portal_type': 'eCard', 'review_state': 'published', 'path': ('/').join(self.context.getPhysicalPath()), 'sort_on': 'getObjPositionInParent'}
        cards = catalog.searchResults(params)
        numECardsPerRow = self.context.getECardsPerRow() or 5
        nestedCardList = []
        subCards = []
        for i in range(len(cards)):
            if len(subCards) == numECardsPerRow:
                nestedCardList.append(subCards)
                subCards = []
            card_obj = cards[i].getObject()
            tag = self._tag_method(card_obj)
            card_dict = {'title': card_obj.Title(), 'description': card_obj.Description() or card_obj.Title(), 'url': card_obj.absolute_url(), 'width': card_obj.getWidth()}
            if self._thumb_size(card_obj):
                card_dict['thumbnail_html'] = tag(scale=self._thumb_size(card_obj), css_class='ecardThumb')
            else:
                card_dict['thumbnail_html'] = tag(css_class='ecardThumb')
            subCards.append(card_dict)
            if i == len(cards) - 1:
                for i in range(numECardsPerRow - len(subCards)):
                    subCards.append('')

                nestedCardList.append(subCards)

        return nestedCardList


class eCardPopupView(Five.BrowserView):
    """See IECardPopupView
    """
    __module__ = __name__
    implements(IECardPopupView)

    def _make_html_email(self, **kw):
        """ Helper function relies heavily upon Python's 
            email Message module to construct our HTML mail.
        """
        msg = MIMEText(kw['message'], 'html', _charset='UTF-8')
        msg['Subject'] = Header(kw['subject'], 'UTF-8')
        msg['From'] = kw['full_from_address']
        msg['To'] = kw['full_to_address']
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = email.Utils.make_msgid()
        return msg

    def stripNewLines(self, str):
        """See IECardPopupView"""
        s = str.replace('\r', '')
        s = s.replace('\n', '')
        return s

    def sendECard(self, **kw):
        """See IECardPopupView"""
        msg = self._make_html_email(subject=kw['subject'], message=kw['message'], full_from_address=kw['full_from_address'], full_to_address=kw['full_to_address'])
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send(msg.as_string(), kw['full_to_address'], kw['full_from_address'], kw['subject'])
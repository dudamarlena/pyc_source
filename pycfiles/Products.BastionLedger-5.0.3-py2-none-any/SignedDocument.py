# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionCrypto/SignedDocument.py
# Compiled at: 2012-03-06 02:26:51
__doc__ = '$id$'
__version__ = '$Revision: 67 $'[11:-2]
import AccessControl
from zExceptions.unauthorized import Unauthorized
from Acquisition import aq_base
from Products.ATContentTypes.content.document import ATDocument as Document
from Products.CMFCore.permissions import View, ModifyPortalContent
from Permissions import sign_documents
from DocumentTemplate.DT_Util import html_quote
from zope.structuredtext.html import HTML
from App.Common import rfc1123_date
from Products.CMFCore.utils import getToolByName
import BastionPGPKey
format_stx = HTML()
try:
    from webdav.Lockable import wl_isLocked
except ImportError:

    def wl_isLocked(ob):
        return 0


def html_headcheck(html):
    """ Return 'true' if document looks HTML-ish enough.

    If true bodyfinder() will be able to find the HTML body.
    """
    lowerhtml = html.lower()
    if lowerhtml.find('<html') == -1:
        return 0
    else:
        if _htfinder.match(lowerhtml):
            return 1
        return 0


class SignedDocument(Document):
    meta_type = portal_type = 'SignedDocument'
    icon = 'misc_/BastionCrypto/signed_document_icon'
    __ac_permissions__ = Document.__ac_permissions__ + (
     (
      View, ('no_signatures', 'pgp_headers', 'pgp_trailers')),
     (
      sign_documents, ('sign_bastioncrypto', 'PUT')))
    _stx_level = 'ignored'

    def _getPortalTypeName(self):
        return self.meta_type

    def no_signatures(self, text=None):
        """
        return raw text with PGP boundaries removed
        """
        if text == None:
            text = getattr(aq_base(self), 'text', '')
        if text:
            return BastionPGPKey.remove_pgp_clearsign_boundary(text)
        else:
            return ''

    def pgp_headers(self):
        """
        return the PGP boundary headers
        """
        return BastionPGPKey.pgp_headers(self.text)

    def pgp_trailers(self):
        """
        return the PGP boundary footers
        """
        return BastionPGPKey.pgp_trailers(self.text)

    def signatoryIds(self):
        """ returns a list of PGP Key ID's for all the signatories """
        return map(lambda x: x[0], self.signatories)

    def _edit(self, text, text_format='', safety_belt=''):
        """ Edit the Document - Parses headers and cooks the body"""
        headers = {}
        if not text_format:
            text_format = self.text_format
        text = text.replace('\r', '')
        if text != getattr(aq_base(self), 'text', ''):
            self.text = text
            cooked_text = BastionPGPKey.remove_pgp_clearsign_boundary(self.text)
            self.signatories = BastionPGPKey.parse_signatories(self.text)
            if text_format == 'html':
                self.cooked_text = cooked_text
            elif text_format == 'plain':
                self.cooked_text = html_quote(cooked_text).replace('\n', '<br />')
            else:
                self.cooked_text = format_stx(cooked_text, level=self._stx_level)

    def edit(self, text_format='text/html', text='', file='', safety_belt=''):
        """
        *used to be WorkflowAction(_edit)
        To add webDav support, we need to check if the content is locked, and if
        so return ResourceLockedError if not, call _edit.

        Note that this method expects to be called from a web form, and so
        disables header processing
        """
        self.failIfLocked()
        if file and type(file) is not type(''):
            contents = file.read()
            if contents:
                text = self.text = contents
        if html_headcheck(text):
            text = bodyfinder(text)
        self.setFormat(text_format)
        self._edit(text=text, text_format=text_format, safety_belt=safety_belt)
        self.reindexObject()

    def CookedBody(self, stx_level=None, setlevel=0):
        """        The prepared basic rendering of an object.  For Documents, this
        means pre-rendered structured text, or what was between the
        <BODY> tags of HTML.

        If the format is html, and 'stx_level' is not passed in or is the
        same as the object's current settings, return the cached cooked
        text.  Otherwise, recook.  If we recook and 'setlevel' is true,
        then set the recooked text and stx_level on the object.
        """
        if self.text_format == 'html' or self.text_format == 'plain' or stx_level is None or stx_level == self._stx_level:
            return self.cooked_text
        else:
            cooked = format_stx(self.cooked_text, stx_level)
            if setlevel:
                self._stx_level = stx_level
                self.cooked_text = cooked
            return cooked
            return

    def EditableBody(self):
        """        The editable body of text.  This is the raw structured text, or
        in the case of HTML, what was between the <BODY> tags.
        """
        return self.no_signatures()

    def handleText(self, text, format=None, stx_level=None):
        """ Handles the raw text, returning headers, body, format """
        headers = {}
        if not format:
            format = self.guessFormat(text)
        if format == 'html':
            parser = SimpleHTMLParser()
            parser.feed(text)
            headers.update(parser.metatags)
            if parser.title:
                headers['Title'] = parser.title
            body = bodyfinder(text)
        else:
            (headers, body) = parseHeadersBody(text, headers)
            if stx_level:
                self._stx_level = stx_level
        return (
         headers, body, format)

    def guessFormat(self, text):
        """ Simple stab at guessing the inner format of the text """
        if html_headcheck(text):
            return 'html'
        else:
            return 'structured-text'

    def sign_bastioncrypto(self, REQUEST, RESPONSE):
        """
        return the raw text suitable for our bastioncryptosign to clearsign it
        the Content-Type is set to application/x-crypto-signable
        """
        r = []
        r.append('url:%s' % self.absolute_url())
        r.append('lock:1')
        member = getToolByName(self, 'portal_membership').getAuthenticatedMember()
        key_id = member.getProperty('email')
        r.append('arguments:--clearsign')
        try:
            if REQUEST._auth[(-1)] == '\n':
                auth = REQUEST._auth[:-1]
            else:
                auth = REQUEST._auth
            r.append('auth:%s' % auth)
        except:
            pass

        r.append('cookie:%s' % REQUEST.environ.get('HTTP_COOKIE', ''))
        if wl_isLocked(self):
            mt = getToolByName(self, 'portal_membership')
            user_id = member.getId()
            for lock in self.wl_lockValues():
                if not lock.isValid():
                    continue
                creator = lock.getCreator()
                if creator and creator[1] == user_id:
                    r.append('lock-token:%s' % lock.getLockToken())
                    if REQUEST.get('borrow_lock'):
                        r.append('borrow_lock:1')
                    break

        r.append('')
        RESPONSE.setHeader('Last-Modified', rfc1123_date())
        RESPONSE.setHeader('Content-Type', 'application/x-bastioncrypto')
        r.append(self.text)
        return ('\n').join(r)

    def PUT(self, REQUEST, RESPONSE):
        """
        return from our bastioncrypto (and anything else which is 
        supposedly signing this thing) ...
        """
        self.dav__init(REQUEST, RESPONSE)
        self.dav__simpleifhandler(REQUEST, RESPONSE, refresh=1)
        self._edit(REQUEST['BODYFILE'].read())
        RESPONSE.setStatus(204)
        return RESPONSE


AccessControl.class_init.InitializeClass(SignedDocument)

def addSignedDocument(self, id, title=''):
    """
    Plone ctor for Signed Document
    """
    self._setObject(id, SignedDocument(id, title=title))
    return id
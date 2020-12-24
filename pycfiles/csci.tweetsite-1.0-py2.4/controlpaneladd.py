# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/browser/controlpaneladd.py
# Compiled at: 2009-11-18 10:43:10
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from csci.tweetsite import tweetsiteMessageFactory as _
from lib import twitter
from Products.CMFCore.utils import getToolByName
from lib import wwpLib
import time, random
from email.Header import make_header
from email.MIMEMessage import Message
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class IcontrolPanelAddSchema(interface.Interface):
    __module__ = __name__
    username = schema.TextLine(title='Owner user: new or existing', description='enter username', required=True, readonly=False, default=None)
    email = schema.TextLine(title='NEW USERS ONLY: User email address', description='(to send account details to)', required=False, readonly=False, default=None)
    twitterAccount = schema.TextLine(title='Twitter accounts to add and associate', description='MUST be a valid Twitter account', required=False, readonly=False, default=None)

    @interface.invariant
    def invariant_testFeed(input):
        try:
            api = twitter.Api(username=input.twitterAccount)
            statuses = api.GetUserTimeline(input.twitterAccount)
        except:
            raise interface.Invalid(_('Some error occurred !'))


class controlPanelAdd(formbase.PageForm):
    __module__ = __name__
    form_fields = form.FormFields(IcontrolPanelAddSchema)
    label = _('Add account')
    description = _('')

    @form.action('Create')
    def actionCreate(self, action, data):
        userid = wwpLib.nametoid(data['username'])
        regtool = getToolByName(self.context, 'portal_registration')
        memtool = getToolByName(self.context, 'portal_membership')
        urltool = getToolByName(self.context, 'portal_url')
        portal = urltool.getPortalObject()
        acl_users = getToolByName(portal, 'acl_users')
        userexists = False
        try:
            user = memtool.getMemberById(userid)
            if user is not None:
                userexists = True
        except:
            pass

        if not userexists:
            email = data['email']
            passwd = ''
            i = 0
            while i < 10:
                passwd += str(int(random.random() * 9))
                i += 1

            properties = {'username': userid, 'fullname': data['username'], 'email': email}
            regtool.addMember(userid, passwd, properties=properties)
            mTo = email
            mFrom = self.context.email_from_address
            mSubj = 'Account Details'
            message = 'Your account has been activated:<br>=================================<br>'
            message += '<br><br>Please login using the following details<br><br>'
            message += '------------------------------------------------------------------' + '<br>'
            message += 'Username : ' + str(userid) + '<br>'
            message += 'Password : ' + str(passwd) + '<br>'
            message += '------------------------------------------------------------------' + '<br>'
            message += '<a href="' + self.context.absolute_url() + '/login_form">Click Here to Log in</a><br>'
            message_b = 'Your account has been activated:\n=================================\n'
            message_b += '\n\nPlease login using the following details\n\n'
            message_b += '------------------------------------------------------------------' + '\n'
            message_b += 'Username : ' + str(userid) + '\n'
            message_b += 'Password : ' + str(passwd) + '\n'
            message_b += '------------------------------------------------------------------' + '\n'
            message_b += 'login page: ' + self.context.absolute_url() + '/login_form\n'
            wwpLib.sendEmail(self.context, mTo, mFrom, mSubj, message, message_b)
        root_app = portal.restrictedTraverse('')
        portal = root_app
        item_path_fromroot = ('/').join(self.context.getPhysicalPath())
        app_loc = portal.restrictedTraverse(item_path_fromroot)
        feedtitle = data['twitterAccount']
        feedid = wwpLib.nametoid(data['twitterAccount'])
        if not app_loc.hasObject(feedid):
            app_loc.invokeFactory(type_name='onlineFeed', id=feedid)
        item_checkout = item_path_fromroot + '/' + feedid
        app_loc = portal.restrictedTraverse(str(item_checkout))
        app_loc.setTitle(feedtitle)
        app_loc.setFeed_username(feedtitle)
        app_loc.setActive_feed(True)
        app_loc.setLastpost = str(time.time())
        workflow = getToolByName(self.context, 'portal_workflow')
        review_state = workflow.getInfoFor(app_loc, 'review_state')
        if review_state != 'published':
            error = workflow.doActionFor(app_loc, 'publish', comment='publised programmatically')
        app_loc.reindexObject()
        memtool.setLocalRoles(app_loc, [userid], 'Editor', reindex=1)
        app_loc.reindexObject()
        return

    @form.action('Cancel')
    def actionCancel(self, action, data):
        self.request.response.redirect(self.context.absolute_url() + '/')
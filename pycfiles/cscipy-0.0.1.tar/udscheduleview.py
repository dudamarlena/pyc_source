# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/fourthplinth/browser/udscheduleview.py
# Compiled at: 2009-09-07 05:23:37
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from csci.fourthplinth import fourthplinthMessageFactory as _
import datetime, urllib, re
from Products.statusmessages.interfaces import IStatusMessage
import time, twitter

class IUDscheduleView(Interface):
    """
    UDschedule view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class UDscheduleView(BrowserView):
    """
    UDschedule browser view
    """
    __module__ = __name__
    implements(IUDscheduleView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update_schedule(self):
        """this updates the page schedule and creates the twitter schedule"""
        today = datetime.date.today()
        today_t = str(today) + ' ' + '00:10'
        now_date = datetime.datetime.now()
        when_date = datetime.datetime(*time.strptime(today_t, '%Y-%m-%d %H:%M')[:5])
        print '---checking for updates---', now_date
        if not hasattr(self.context, 'lastpost'):
            self.context.lastpost = '0ೌ'
        if not hasattr(self.context, 'tschedule'):
            self.context.tschedule = ()
        if self.context.debugmode:
            self.context.lastpost = '0ೌ'
        if today != self.context.lastpost:
            if now_date > when_date:
                print '------getting new schedule---'
                now_date = datetime.datetime.now()
                fpurl = 'http://www.oneandother.co.uk/participants/day?day='
                fpurl += str(now_date).replace('/', '-')[:10]
                raw_page = urllib.urlopen(fpurl)
                raw_page = raw_page.read()
                rawstr = '<li\\ class=".+">\\s*<span\\ class=\'starts_at\'>\\s*<span\\ class=\'time\'>(?P<hour>\\d+)\n                \\s*</span>\\s*<span\\ class=\'am-pm\'>(?P<ampm>\\w+)\n                \\s*</span>\\s*<span\\ class=\'corners\'>\\s*</span>\\s*</span>\\s*<span\\ class=\'avatar\'>\\s*<img\\ alt=".+"\\ src="(?P<avatar>.+)"\\ />\n                \\s*<span\\ class=\'corners\'></span>\\s*</span>\\s*<span\\ class=\'name-wrapper\'>\\s*<span\\ class=\'name\'>\n                ((\\s*<a.+?"(?P<upath>.+?)">(?P<uname>\\w*)</a>)|\\s*Anonymous)'
                compile_obj = re.compile(rawstr, re.MULTILINE | re.VERBOSE)
                match_obj = compile_obj.findall(raw_page)
                twitter_schedule = ()
                schedule_html = '<h2>Schedule for ' + str(now_date).replace('/', '-')[:10] + '</h2><br><br><table width=400px border=0px padding=5px ALIGN="CENTER">'
                for partisipant in match_obj:
                    hour = str(partisipant[0])
                    ampm = str(partisipant[1])
                    avatar = str(partisipant[2])
                    uurl = 'http://www.oneandother.co.uk' + str(partisipant[5])
                    uname = str(partisipant[6])
                    if uname == '' or uname == ' ':
                        uname = 'Anonymous'
                    schedule_html += '<tr><td><h2>' + hour + ' ' + ampm + '</h2></td><td><img src="' + avatar + '" /></td><td><a href="' + uurl + '">' + uname + '</a></td></tr>'
                    if ampm == 'PM':
                        if hour != '12':
                            hour = str(int(hour) + 12)
                    if ampm == 'AM':
                        if hour == '12':
                            hour = '00'
                    twitstring = str(now_date).replace('-', '/')[:10] + ', ' + hour + ':00, ' + hour + ':00 - ' + uname + ' is just starting on the Fourth Plinth'
                    twitter_schedule += (twitstring,)

                schedule_html += '</table>'
                self.context.schedule_html = schedule_html
                self.context.tschedule += twitter_schedule
                root_app = self.context.restrictedTraverse('news')
                news_id = 'Fourth Plinth ' + str(today)
                news_id = news_id.replace(' ', '-')
                news_id = news_id.replace(':', '-')
                news_item = root_app.invokeFactory(type_name='News Item', id=news_id, title='Fourth Plinth Schedule on ' + str(today), description='The following people are on the plinth', text=schedule_html)
                root_app.reindexObject()
                root_app = self.context.restrictedTraverse('news/' + news_id)
                urltool = getToolByName(self.context, 'portal_url')
                workflow = getToolByName(self.context, 'portal_workflow')
                review_state = workflow.getInfoFor(root_app, 'review_state')
                if review_state != 'published':
                    error = workflow.doActionFor(root_app, 'publish', comment='publised programmatically')
                self.context.lastpost = today
        now_date = datetime.datetime.now()
        for post in self.context.tschedule:
            post_list = post.split(',')
            if len(post_list) > 3:
                IStatusMessage(self.request).addStatusMessage(_('Badly formatted Tweet', len(post_list)), type='error')
            twit_date = post_list[0]
            twit_time = post_list[1]
            twit_text = post_list[2]
            when_date = datetime.datetime(*time.strptime(twit_date + twit_time, '%Y/%m/%d %H:%M')[:5])
            if now_date >= when_date:
                print '------posting a tweet---', twit_text[:50]
                if self.context.tusername == '':
                    IStatusMessage(self.request).addStatusMessage(_('Username not set! Cannot post'), type='error')
                if self.context.tpassword == '':
                    IStatusMessage(self.request).addStatusMessage(_('Password not set! Cannot post'), type='error')
                api = twitter.Api(username=self.context.tusername, password=self.context.tpassword)
                statuses = api.PostUpdate(status=twit_text[:140], in_reply_to_status_id=None)
                tweetstogo_out = ()
                for item in self.context.tschedule:
                    if item != post:
                        tweetstogo_out += (item,)

                self.context.tschedule = tweetstogo_out

        return '---updates complete---'

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _('a dummy string')
        return {'dummy': dummy}
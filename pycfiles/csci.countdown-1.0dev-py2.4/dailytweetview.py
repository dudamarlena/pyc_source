# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/countdown/browser/dailytweetview.py
# Compiled at: 2009-09-16 06:09:12
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from csci.countdown import countdownMessageFactory as _
import datetime, time, urllib, twitter

class IdailytweetView(Interface):
    """
    dailytweet view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class dailytweetView(BrowserView):
    """
    dailytweet browser view
    """
    __module__ = __name__
    implements(IdailytweetView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def daily_tweet(self):
        today = datetime.date.today()
        if not hasattr(self.context, 'lastpost'):
            self.context.lastpost = '0ೌ'
        if self.context.debugmode:
            self.context.lastpost = '0ೌ'
        if today != self.context.lastpost:
            tweet1_text = str(self.context.returned_dates['days']) + ' days to go to Christmas!'
            tweet1_time = '08:00'
            tweet1_date = str(datetime.date.today()).replace('-', '/')
            tweets_topost = ()
            tweets_topost += (str(tweet1_date) + ', ' + str(tweet1_time) + ', ' + str(tweet1_text),)
            self.context.tweetschedule = tweets_topost
            self.context.lastpost = today
        try:
            print '---trying---'
            gmt_page = urllib.urlopen("http://www.righthearted.com/runner.py?TZ_DATA_['London']")
            gmt_page = gmt_page.readlines()
            gmt_offsets = {}
            for loc in gmt_page:
                loc = loc.replace('\n', '')
                loc = loc.split('=')
                gmt_offsets[loc[0]] = int(loc[1])

            self.context.gmt_offsets = gmt_offsets
            print '---sucess---'
        except:
            print '---failed---'
            if hasattr(self.context, 'gmt_offsets'):
                print '---got old one---'
                gmt_offsets = self.context.gmt_offsets
            else:
                print '---got new one---'
                gmt_offsets = {}
                gmt_offsets['London'] = 0
                self.context.gmt_offsets = gmt_offsets

        now_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=gmt_offsets['London'])
        for post in self.context.tweetschedule:
            post_list = post.split(',')
            twit_date = post_list[0]
            twit_time = post_list[1]
            twit_text = post_list[2]
            orig_time = time.strptime(twit_date + twit_time, '%Y/%m/%d %H:%M')
            orig_time = time.mktime(orig_time)
            orig_time += -121
            new_time = time.localtime(orig_time)
            when_date = datetime.datetime(*new_time[:5])
            if now_date >= when_date:
                api = twitter.Api(username=self.context.tuser, password=self.context.tpass)
                statuses = api.PostUpdate(status=twit_text[:140], in_reply_to_status_id=None)
                tweetstogo_out = ()
                for item in self.context.tweetschedule:
                    if item != post:
                        tweetstogo_out += (item,)

                self.context.tweetschedule = tweetstogo_out

        return '---updates complete---'
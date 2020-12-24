# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/plugins/following/kssviews.py
# Compiled at: 2009-07-12 09:10:38
from Acquisition import aq_inner
from collective.sylvester.browser.kssviews import BaseSylvesterKssView, kssactionplus

class FollowingKssView(BaseSylvesterKssView):
    __module__ = __name__

    @kssactionplus
    def refreshFollowing(self, user_ids=None):
        """
        Refresh a a few friendlets.
        """
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        view = context.restrictedTraverse('@@collective.sylvester.dashboard')
        mapping = view.GetUsersStatuses(user_ids=user_ids)
        for di in mapping.items():
            user = di['user']
            statuses = ['statuses']
            html = self.viewletMacroContent('collective.sylvester.friendletmanager', 'collective.sylvester.friendlet', 'main', friend=user, statuses=statuses)
            selector = ksscore.getHtmlIdSelector('collective-sylvester-friendlet-friend%s' % user_id)
            ksscore.replaceHTML(selector, html)
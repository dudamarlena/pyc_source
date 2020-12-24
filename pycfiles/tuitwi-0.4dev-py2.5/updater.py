# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tuitwi/updater.py
# Compiled at: 2010-06-30 10:58:42
import curses, tweepy, tweepy.parsers, threading, string, re, locale, const

class Updater(threading.Thread):
    """ 一定の間隔でジョブキューに更新処理を入れる """

    def __init__(self, queue, conf):
        self._queue = queue
        self._stopevent = threading.Event()
        self._sleepperiod = conf.get('options', {}).get('update_interval', 60)
        self._dm_reply_interval = conf.get('options', {}).get('reply_check_interval', 20)
        self._count = self._dm_reply_interval
        threading.Thread.__init__(self)

    def run(self):
        u"""メインループ"""
        while not self._stopevent.isSet():
            self._queue.put(('GetFriendsTimeline', ))
            self._count += 1
            if self._count >= self._dm_reply_interval:
                self._count = 0
                self._queue.put(('GetReplies', ))
            self._stopevent.wait(self._sleepperiod)

    def join(self, timeout=None):
        u"""スレッドを停止して終了を待つ"""
        self._stopevent.set()
        threading.Thread.join(self, timeout)


class TwitterCommunicator(threading.Thread):
    """ジョブキューをもとに、更新処理などを行なう."""

    def __init__(self, queue, form, lock, conf):
        self._queue = queue
        self._form = form
        self._lock = lock
        self._conf = conf
        self._stopevent = threading.Event()
        self._since_id = 0
        self._rpl_since_id = 0
        self._dm_since_id = 0
        tkn = tweepy.oauth.OAuthToken(self._conf['access_token']['key'], self._conf['access_token']['secret'])
        oauth_auth = tweepy.OAuthHandler(const.CONSUMER_KEY, const.CONSUMER_SECRET)
        oauth_auth.access_token = tkn
        self._api = tweepy.API(oauth_auth)
        self._funcs = {}
        self._funcs['GetFriendsTimeline'] = self._GetFriendsTimeline
        self._funcs['GetDirectMessages'] = self._GetDirectMessages
        self._funcs['GetReplies'] = self._GetReplies
        self._funcs['PostUpdate'] = self._PostUpdate
        self._funcs['DestroyStatus'] = self._DestroyStatus
        self._funcs['CreateFavorite'] = self._CreateFavorite
        self._funcs['DestroyFavorite'] = self._DestroyFavorite
        self._funcs['Quit'] = self._Quit
        threading.Thread.__init__(self)

    def run(self):
        while not self._stopevent.isSet():
            job = self._queue.get()
            self._funcs[job[0]](job[1:])

    def join(self, timeout=None):
        u"""スレッドを停止して終了を待つ"""
        self._stopevent.set()
        self._queue.put(('Quit', ))
        threading.Thread.join(self, timeout)

    def _translateTimeline(self, timeline):
        u"""改行を空白に変更したり、CP932とかの問題を解決する"""

        def translate(text):
            text = re.sub('(' + ('|').join(string.whitespace) + ')', ' ', text)
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            text = text.replace('―', '—')
            text = text.replace('～', '〜')
            text = text.replace('－', '−')
            text = text.replace('∥', '‖')
            text = text.replace('￢', '¬')
            text = text.replace('￡', '£')
            text = text.replace('￠', '¢')
            return text

        for status in timeline:
            status.text = translate(status.text)
            status.user.name = translate(status.user.name)

    def _GetFriendsTimeline(self, args):
        u"""TLを取得する"""
        try:
            if self._since_id:
                timeline = self._api.friends_timeline(since_id=self._since_id)
            else:
                timeline = self._api.friends_timeline(count=200)
            msg = 'TLの取得に成功しました'
        except Exception, e:
            msg = 'TLの取得に失敗しました'
            timeline = []

        self._translateTimeline(timeline)
        self._lock.acquire()
        try:
            if timeline:
                self._form.controls['view_tab'].update_timeline(timeline)
                self._since_id = timeline[0].id
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

    def _GetReplies(self, args):
        u"""Replyを取得する"""
        try:
            if self._rpl_since_id:
                timeline = self._api.mentions(since_id=self._rpl_since_id)
            else:
                timeline = self._api.mentions()
            msg = 'Replyの取得に成功しました'
        except Exception, e:
            msg = 'Replyの取得に失敗しました'
            timeline = []

        self._translateTimeline(timeline)
        self._lock.acquire()
        try:
            if timeline:
                self._form.controls['view_tab'].update_replies(timeline)
                self._rpl_since_id = timeline[0].id
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

    def _GetDirectMessages(self, args):
        u"""DMを取得する"""
        try:
            if self._dm_since_id:
                timeline = self._api.direct_messages(since_id=self._dm_since_id)
            else:
                timeline = self._api.direct_messages()
            msg = 'DMの取得に成功しました'
        except Exception, e:
            msg = 'DMの取得に失敗しました'
            timeline = []

        self._translateTimeline(timeline)
        self._lock.acquire()
        try:
            if timeline:
                self._form.controls['view_tab'].update_directmessages(timeline)
                self._dm_since_id = timeline[0].id
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

    def _PostUpdate(self, args):
        u"""発言する"""
        text = args[0]
        reply_id = args[1]
        try:
            status = self._api.update_status(text.encode('utf-8'), reply_id)
            msg = 'Postに成功しました'
        except Exception, e:
            status = None
            msg = 'Postに失敗しました'

        self._lock.acquire()
        try:
            if status is not None:
                timeline = [
                 status]
                self._translateTimeline(timeline)
                self._form.controls['view_tab'].update_timeline(timeline)
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

        return

    def _CreateFavorite(self, args):
        status = args[0]
        try:
            st = self._api.create_favorite(status.id)
            msg = 'favに成功しました'
        except Exception, e:
            st = None
            msg = 'favに失敗しました'

        self._lock.acquire()
        try:
            if st is not None:
                status.favorited = True
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

        return

    def _DestroyFavorite(self, args):
        status = args[0]
        try:
            st = self._api.destroy_favorite(status.id)
            msg = 'fav削除に成功しました'
        except Exception, e:
            st = None
            msg = 'fav削除に失敗しました'

        self._lock.acquire()
        try:
            if st is not None:
                status.favorited = False
            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

        return

    def _DestroyStatus(self, args):
        u"""削除する"""
        deleted = False
        try:
            self._api.destroy_status(args[0])
            msg = '削除に成功しました'
            deleted = True
        except Exception, e:
            msg = '削除に失敗しました'

        self._lock.acquire()
        try:
            if deleted:
                for win in self._form.controls['view_tab'].wins:
                    win['win'].delete(args[0])

            self._form.controls['status_line'].text = msg
            self._form.draw()
            curses.doupdate()
        finally:
            self._lock.release()

    def _Quit(self, arg):
        pass
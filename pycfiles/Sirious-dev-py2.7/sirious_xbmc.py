# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sirious/plugins/sirious_xbmc.py
# Compiled at: 2011-11-28 11:10:12
import urllib
from sirious import SiriPlugin, SiriObjects

class SiriousXBMC(SiriPlugin):

    def __init__(self, user, passwd, host, port):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    def send_message(self, phrase, plist, match_groups):
        message = match_groups[0]
        message = message[0].upper() + message[1:]
        kwargs = {'message': message}
        root = SiriObjects.AddViews()
        root.make_root(ref_id=self.proxy.ref_id, dialogPhase='Confirmation')
        root.views = [
         SiriObjects.Utterance(text="Here's your message to XBMC.", dialogIdentifier='createSms#willSendSms', speakableText="Ok, here's your message to XBMC.@{tts#\x1b\\pause=1500\\} Ready to send it?", listenAfterSpeaking=True),
         SiriObjects.SMSSnippet(smss=[
          SiriObjects.SMS(message=message, outgoing=True, recipients=['XBMC'])])]
        self.ask_views(self.handle_confirm, root, handler_kwargs=kwargs)

    send_message.triggers = ['Tell (?:the TV|XBMC) (.*)$']

    def handle_confirm(self, phrase, plist, message):
        self.proxy.blocking = True
        phrase = phrase.strip().lower()
        if phrase in ('no', 'cancel'):
            return
        if phrase in ('yes', 'ok'):
            url = 'http://%s:%s@%s:%s/xbmcCmds/xbmcHttp?' % (self.user, self.passwd, self.host, self.port)
            args = 'command=ExecBuiltIn(Notification(Sirious%20Notification,' + urllib.quote(message.strip()) + '))'
            urllib.urlopen(url + args).read()
            root = SiriObjects.AddViews(temporary=True)
            root.make_root(ref_id=self.proxy.ref_id)
            root.views = [
             SiriObjects.Utterance(text="Ok, I've sent your message")]
            self.proxy.inject_plist(root.to_dict())
            return
        self.ask(self.handle_confirm, 'Please respond yes or no', handler_kwargs={'message': message})

    def play_movie(self, phrase, plist, match_groups, movies=None):
        pass

    play_movie.triggers = [
     'play an? (new|)?([a-z ]+)?movie']
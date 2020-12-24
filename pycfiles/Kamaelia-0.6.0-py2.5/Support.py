# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/IRCLogger/Support.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.File.Writing import SimpleFileWriter
import os, Kamaelia.Support.Protocol.IRC, time
logging = True
lastlog = time.time()

def cannedResponse():
    return [
     "Hi, I'm a bot. I've been put here to answer faq's and log the channel.",
     "I've not really been configured yet, so I won't do much here yet :-)"]


def cannedYesTheyreAround():
    return [
     "Hi, I'm a bot. I've been put here to answer faq's and log the channel.",
     "I've not really been configured yet, so I won't do much here yet :-)"]


def respondToQueries(self, msg):
    """Takes a BasicLogger as its first argument. If this function recognizes
    "msg" as a command, then it sends back the appropriate response to IRC
    """
    replyLines = ''
    tag = 'PRIVMSG'
    if msg[0] == 'PRIVMSG' and msg[3].split(':')[0] == self.name:
        words = msg[3].split()
        if words[1] == 'logfile':
            replyLines = [
             self.logname]
        elif words[1] == 'infofile':
            replyLines = [
             self.infoname]
        elif words[1] == 'help':
            replyLines = [
             'Name: %s   Channel: %s' % (self.name, self.channel),
             'I do a simple job -- recording all channel traffic.',
             "Lines prefixed by [off] won't get recorded",
             "I respond to the following: 'logfile', 'infofile', 'help', 'date', 'time', 'dance', 'poke', 'slap', 'ecky', 'boo', and 'reload {modulename}'."]
        elif words[1] == 'date':
            replyLines = [
             self.currentDateString()]
        elif words[1] == 'time':
            replyLines = [
             self.currentTimeString()]
        elif words[1] == 'dance':
            tag = 'ME'
            replyLines = ['does the macarena']
        elif words[1] == 'poke':
            replyLines = [
             'Not the eye! Not the eye!']
        elif words[1] == 'slap':
            replyLines = [
             'Ouch!']
        elif words[1] == 'ecky':
            replyLines = [
             'Ptang!']
        elif words[1] == 'boo':
            replyLines = [
             "Nice try, but that didn't scare me"]
        elif words[1] == 'learn':
            replyLines = [
             'OK, trying, but not ready to do that yet - I will though' + str(len(words))]
    if msg[0] == 'PRIVMSG':
        words = [ x.lower() for x in msg[3].split() ]
        if 'any' in words and ('mentors' in words or 'mentor' in words):
            replyLines = cannedResponse()
        elif 'when' in words and ('feedback' in words or 'expect' in words):
            replyLines = cannedResponse()
        elif 'when' in words and ('feedback' in words or 'expect' in words):
            replyLines = cannedResponse()
        elif 'i' in words and ('have' in words or 'had' in words) and ('question' in words or 'query' in words or 'doubt' in words):
            replyLines = cannedResponse()
        elif 'who' in words and 'can' in words and 'i' in words and 'ask' in words and ('soc' in words or 'gcos' in words or 'gsoc' in words):
            replyLines = cannedResponse()
        elif ('about' in words or 'around' in words) and ('is' in words or 'are' in words) and ('mentors-' in words or 'ms-' in words or 'mhrd' in words or 'lawouach' in words):
            replyLines = cannedYesTheyreAround()
        elif 'anyone' in words and 'seen' in words and ('mentors-' in words or 'ms-' in words or 'mhrd' in words or 'lawouach' in words):
            replyLines = cannedYesTheyreAround()
        elif 'hi' in words and ('everybody' in words or 'evreybody' in words):
            replyLines = [
             'hi']
        elif 'kamaeliabot' in words:
            if 'bonjour' in words:
                replyLines = [
                 'Bonjour']
            elif 'parrot' in words:
                replyLines = [
                 repr(words)]
        if replyLines == '':
            if 'anyone' in words and 'know' in words:
                replyLines = [
                 'Hm?']
    if replyLines:
        for reply in replyLines:
            self.send((tag, self.channel, reply), 'irc')
            self.send(self.format('Reply: %s \n' % reply), 'outbox')


def TimedOutformat(data):
    """    prepends a timestamp onto formatted data and ignores all privmsgs prefixed
    by "[off]"
    """
    if data[0] == 'PRIVMSG' and data[3][0:5] == '[off]':
        return
    if type(data) == type(''):
        formatted = data
    else:
        formatted = Kamaelia.Support.Protocol.IRC.outformat(data)
    curtime = time.gmtime()
    timestamp = time.strftime('[%H:%M] ', curtime)
    if formatted:
        return timestamp + formatted


def HTMLOutformat(data):
    """each formatted line becomes a line on a table."""
    global logging
    if logging:
        head = '            <tr><td>'
        end = '</td></tr>\n'
        formatted = TimedOutformat(data)
        if formatted:
            formatted = formatted.replace('<', '&lt ')
            formatted = formatted.replace('>', '&gt')
            return head + formatted.rstrip() + end


def AppendingFileWriter(filename):
    """appends to instead of overwrites logs"""
    return SimpleFileWriter(filename, mode='ab')


def LoggerWriter(filename):
    """
    puts an html header in front of every file it opens. Does not make well-
    formed HTML, as files are closed without closing the HTML tags. However,
    most browsers don't have a problem with this. =D
    """
    htmlhead = '<html><body><table>\n'
    if not os.path.exists(filename):
        f = open(filename, 'wb')
        f.write(htmlhead)
        f.close()
    return SimpleFileWriter(filename, mode='ab')


def currentDateString():
    """returns the current date in YYYY-MM-DD format"""
    curtime = time.gmtime()
    return time.strftime('%Y-%m-%d', curtime)


def currentTimeString():
    """returns the current time in hour:minute:second format"""
    curtime = time.gmtime()
    return time.strftime('%H:%M:%S', curtime)


def getFilenames(logdir, channel):
    """returns tuple (logname, infoname) according to the parameters given"""
    name = logdir + channel.lstrip('#') + currentDateString()
    return (name + '_log.html', name + '_info.html')


outformat = HTMLOutformat
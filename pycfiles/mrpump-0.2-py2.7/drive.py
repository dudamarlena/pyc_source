# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/drive.py
# Compiled at: 2012-05-05 15:28:20
import logging, tweepy, cPickle, errno, time

def loop(api, seconds, already_seen_filename, my_screen_name, handler):
    log = logging.getLogger('drive')
    orig_seconds = seconds
    try:
        already_seen = cPickle.load(file(already_seen_filename))
    except IOError as e:
        if e.errno == errno.ENOENT:
            already_seen = set()
        else:
            raise

    while True:
        log.debug('fetching DMs')
        try:
            fetched = api.direct_messages()
        except tweepy.TweepError as e:
            log.error('while fetching DMs: %s', e.reason)
            if 'status code = 503' in e.reason:
                seconds *= 1.2
                log.info('Got 503, now sleeping %.2f seconds', seconds)

        dms = dict([ (dm.id, dm) for dm in fetched ])
        log.debug('%d DMs', len(dms.keys()))
        new = set(dms.keys()) - already_seen
        log.debug('%d new DMs', len(new))
        for id in new:
            dm = dms[id]
            if dm.sender.screen_name == my_screen_name:
                log.debug('ignoring DM %r %r from myself', id, dm.text)
            else:
                log.info('<< %s: %r', dm.sender.screen_name, dm.text)

                def reply(text):
                    text = text[:140]
                    try:
                        unique_nonce = str(int(time.time()))[-3:]
                        api.send_direct_message(screen_name=dm.sender.screen_name, text=unique_nonce + ' ' + text)
                        log.info('>> %s: %r', dm.sender.screen_name, text)
                    except tweepy.TweepError as e:
                        log.error('TweepError during reply: %s', e.reason)

                handler(dm.sender.screen_name, dm.text, reply)

        already_seen = set(dms.keys())
        cPickle.dump(already_seen, file(already_seen_filename, 'w'))
        log.debug('sleeping')
        time.sleep(seconds)
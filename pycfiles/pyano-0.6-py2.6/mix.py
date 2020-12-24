# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/mix.py
# Compiled at: 2010-11-11 16:21:25
import subprocess
from config import conf, POST

class MixError(Exception):
    pass


def send_mail(to, orig, subj, chain, n_copies, msg):
    args = [
     conf.mixmaster, '--mail', '--to=' + to, '--subject=' + subj, '--copies=' + str(n_copies)]
    if orig:
        args.append('--header=From: ' + orig)
    if chain:
        args.append('--chain=' + (',').join(chain))
    send_mix(args, msg)


def send_news(newsgroups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg):
    args = [
     conf.mixmaster, '--subject=' + subj, '--copies=' + str(n_copies)]
    if orig:
        args.append('--header=From: ' + orig)
    if no_archive:
        args.append('--header=X-No-Archive: yes')
    if mail2news != POST:
        args.extend(['--mail', '--to=' + mail2news])
        args.append('--header=Newsgroups: ' + newsgroups)
    else:
        args.extend(['--post', '--post-to=' + newsgroups])
    if refs:
        args.append('--header=References: ' + refs)
    if hashcash:
        args.append('--header=X-HashCash: ' + hashcash)
    if chain:
        args.append('--chain=' + (',').join(chain))
    send_mix(args, msg)


def send_mix(args, msg):
    try:
        mix = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = mix.communicate(msg)
        if err.find('Error') >= 0:
            raise MixError('Mixmaster process returned the following error: ' + str(err) + '. Sending failed.')
    except OSError:
        raise MixError('Could not find mixmaster binary.')
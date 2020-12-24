# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/validate.py
# Compiled at: 2010-11-11 16:27:32
import re, random
from stats import stats, bad_mail2news
from config import conf, NONE, RANDOM, POST

class InputError(Exception):
    pass


def val_email_local(local):
    ac = "[a-zA-Z0-9_!#\\$%&'*+\\-=?\\^`{|}~]"
    m = re.compile('^(' + ac + '+\\.)*' + ac + '+$')
    if not m.match(local):
        raise InputError()


def val_dot_seq(server):
    ac = '[a-zA-Z0-9+\\-_]'
    m = re.compile('^(' + ac + '+\\.)+' + ac + '+$')
    if not m.match(server):
        raise InputError()


def val_email(addr):
    m = re.compile('^("?[\\w ]*"? *<)?([^>]+)>?$')
    ok = m.match(addr)
    try:
        if not ok:
            raise InputError()
        email = ok.group(2)
        parts = email.split('@')
        if len(parts) != 2:
            raise InputError()
        val_email_local(parts[0])
        val_dot_seq(parts[1])
    except InputError:
        if addr:
            raise InputError(addr + ' is not a valid email address.')
        raise InputError('Please enter an email address.')


def val_newsgroups(newsgroups):
    groups = newsgroups.split(',')
    for group in groups:
        val_dot_seq(group)


def val_references(refs):
    m = re.compile('^<(.*)>$')
    try:
        for ref in refs.split(' '):
            ok = m.match(ref)
            if not ok:
                raise InputError()
            val_email(ok.group(1))

    except:
        raise InputError(ref + ' is not a valid reference.')


def val_mail2news(mail2news):
    for addr in mail2news.split(','):
        try:
            val_email(addr)
        except InputError:
            raise InputError(mail2news + ' is not a valid mail2news gateway')


def val_hashcash(hc):
    m = re.compile('[a-zA-Z0-9_:+\\-=; ]+')
    if not m.match(hc):
        raise InputError(hc + ' is not a valid hashcash.')


def val_n_copies(n_copies):
    if n_copies <= 0 or n_copies > conf.max_copies:
        raise InputError('Invalid number of copies.')


def parse_chain(fs, m2n=None):
    chain = []
    for i in range(0, conf.chain_max_length):
        chain_str = 'chain' + str(i)
        if chain_str not in fs:
            break
        remailer = str(fs[chain_str])
        if remailer == NONE:
            break
        elif remailer == RANDOM:
            chain.append('*')
        elif remailer in chain:
            raise InputError('Cannot use the same remailer twice in the same chain.')
        elif remailer in stats:
            chain.append(remailer)
        else:
            raise InputError(remailer + ' is not a valid remailer.')

    if chain:
        last = chain[(len(chain) - 1)]
        if stats[last].middleman:
            raise InputError('Cannot select a "middleman" remailer as your final remailer.')
        if m2n:
            if m2n == POST and not stats[last].post:
                raise InputError(last + 'does not have the "post" option configured.')
            elif m2n in bad_mail2news:
                if last in bad_mail2news[m2n]:
                    raise InputError(last + ' is not compatible with the mail2news gateway ' + m2n + '.')
        for i in range(0, len(chain) - 1):
            cur = chain[i]
            next = chain[(i + 1)]
            if next in stats[cur].broken:
                raise InputError('Cannot use known broken chain: (' + cur + ' ' + next + ').')

    return chain
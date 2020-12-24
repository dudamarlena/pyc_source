# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/stats.py
# Compiled at: 2010-11-11 21:44:18
import re
from config import conf, POST

class RemailerStats:

    def __init__(self, name, latency, uptime):
        self.name = name
        self.latency = latency
        self.uptime = uptime
        self.broken = []
        self.allow_from = False
        self.middleman = False
        self.post = False


stats = {}
bad_mail2news = {}

def parse_stats():
    try:
        _read_mlist()
        try:
            _read_allow_from()
        except IOError:
            pass

    except IOError:
        stats.clear()

    try:
        _read_bad_mail2news()
    except IOError:
        bad_mail2news.clear()


def _read_mlist():
    with open(conf.mlist2, 'r') as (f):
        n = 0
        in_stats_block = False
        in_broken_block = False
        for line in f:
            n += 1
            if n == 4:
                in_stats_block = True
            elif in_stats_block:
                elems = line.split()
                if len(elems) == 0:
                    in_stats_block = False
                else:
                    name = elems[0]
                    latency = elems[2]
                    uptime = float(elems[4].strip('%'))
                    stats[name] = RemailerStats(name, latency, uptime)
            elif 'Broken type-II remailer chains' in line:
                in_broken_block = True
            elif in_broken_block:
                elems = line.strip().strip('()').split()
                if len(elems) == 0:
                    in_broken_block = False
                else:
                    stats[elems[0]].broken.append(elems[1])
            elif '=' in line:
                name = line[11:].split('"', 1)[0]
                rem_stats = stats[name]
                rem_stats.middleman = 'middle' in line
                rem_stats.post = 'post' in line


def _read_allow_from():
    with open(conf.allow_from, 'r') as (f):
        in_from_block = False
        m = re.compile('<td>(\\w+)</td>')
        for line in f:
            if line.find('User Supplied From') >= 0:
                in_from_block = True
            if in_from_block:
                ok = m.search(line)
                if ok:
                    name = ok.group(1)
                    if name in stats:
                        stats[name].allow_from = True


def format_stats(name):
    rem = stats[name]
    s = rem.name.ljust(12) + rem.latency.rjust(5) + (str(rem.uptime) + '%').rjust(7)
    if rem.middleman:
        s += ' M'
    else:
        s += '  '
    if rem.allow_from:
        s += 'F'
    else:
        s += ' '
    if rem.post:
        s += 'P'
    else:
        s += ' '
    if rem.broken:
        s += ' (breaks: '
        for remailer in rem.broken:
            s += remailer + ','

        s = s.rstrip(',')
        s += ')'
    return s


def uptime_sort():
    remailers = stats.keys()
    remailers.sort(cmp=lambda x, y: cmp(stats[y].uptime, stats[x].uptime))
    return remailers


def _read_bad_mail2news():
    with open(conf.bad_mail2news, 'r') as (f):
        for line in f:
            elems = line.split('>')
            if len(elems) == 2:
                remailer = elems[0].strip()
                gateway = elems[1].strip()
                if 'BAD' in gateway:
                    gateway = gateway.split()[0]
                    if gateway == 'Post:':
                        gateway = POST
                    if gateway not in bad_mail2news:
                        bad_mail2news[gateway] = set([])
                    bad_mail2news[gateway].add(remailer)


def format_bad_mail2news(gateway):
    out = gateway.ljust(25)
    bad = bad_mail2news[gateway]
    if bad:
        out += ' (BAD: '
        for remailer in bad:
            out += remailer + ','

        out = out.rstrip(',')
        out += ')'
    return out


def mail2news_pref_sort():
    gateways = bad_mail2news.keys()
    gateways.sort(cmp=_mail2news_cmp)
    return gateways


def _mail2news_cmp(gate1, gate2):
    if gate1 in conf.mail2news:
        if gate2 in conf.mail2news:
            return cmp(conf.mail2news.index(gate1), conf.mail2news.index(gate2))
        else:
            return -1
    else:
        if gate2 in conf.mail2news:
            return 1
        else:
            return 0
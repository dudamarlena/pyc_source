# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/.local/lib/python2.7/site-packages/specialDNS/info.py
# Compiled at: 2012-01-01 16:33:09
import add, json, os
names = ()
trustedNS = 'ns1.afraid.org'
cdir = os.path.join(os.path.expanduser('~'), '.config')
if not os.path.exists(cdir):
    os.makedirs(cdir)
config = os.path.join(cdir, 'specialDNS.json')

def load():
    global names
    global trustedNS
    try:
        with open(config) as (inp):
            names, trustedNS = json.load(inp)
    except Exception as e:
        print e
        initialize()


def save():
    with open(config, 'wt') as (out):
        json.dump((names, trustedNS), out, sort_keys=True, indent=4)


def initialize():
    global trustedNS
    doSave = False
    print 'Enter a trusted name server (default ' + trustedNS + ')'
    ns = raw_input('> ').strip()
    if len(ns) > 0:
        doSave = True
        trustedNS = ns
    add.add()
    if doSave:
        save()


load()
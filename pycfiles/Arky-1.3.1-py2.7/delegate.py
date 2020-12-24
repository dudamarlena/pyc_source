# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arky\cli\delegate.py
# Compiled at: 2018-01-01 17:01:03
"""
Usage: 
    delegate link [<secret>] [<2ndSecret>]
    delegate unlink
    delegate save <name>
    delegate status
    delegate voters
    delegate forged

Subcommands:
    link   : link to delegate using secret passphrases. If secret passphrases
             contains spaces, it must be enclosed within double quotes
             (ie "secret with spaces").
    unlink : unlink delegate.
    save   : encrypt account using pin code and save it localy.
    status : show information about linked delegate.
    voters : show voters contributions ([address - vote] pairs).
    forged : show forge report.
"""
import arky
from .. import cfg
from .. import rest
from .. import util
from . import DATA
from . import input
from . import checkSecondKeys
from . import checkRegisteredTx
from .account import link as _link
from .account import save
import io, os, sys, collections

def _whereami():
    if DATA.account and not DATA.delegate:
        _loadDelegate()
    if DATA.delegate:
        return 'delegate[%s]' % DATA.delegate['username']
    else:
        return 'delegate'


def _loadDelegate():
    if DATA.account:
        resp = rest.GET.api.delegates.get(publicKey=DATA.account['publicKey'], returnKey='delegate')
        if resp.get('publicKey', False):
            DATA.delegate = resp
            return True
        return False


def link(param):
    _link(dict(param, **{'--escrow': False}))
    if not _loadDelegate():
        sys.stdout.write('Not a delegate\n')
        unlink(param)


def status(param):
    if DATA.delegate:
        account = rest.GET.api.accounts(address=DATA.account['address'], returnKey='account')
        util.prettyPrint(dict(account, **DATA.delegate))


def unlink(param):
    DATA.delegate.clear()


def forged(param):
    if DATA.delegate:
        resp = rest.GET.api.delegates.forging.getForgedByAccount(generatorPublicKey=DATA.account['publicKey'])
        if resp.pop('success'):
            util.prettyPrint(dict([k, float(v) / 100000000] for k, v in resp.items()))


def voters(param):
    if DATA.delegate:
        accounts = rest.GET.api.delegates.voters(publicKey=DATA.delegate['publicKey']).get('accounts', [])
        sum_ = 0.0
        log = collections.OrderedDict()
        for addr, vote in sorted([ [c['address'], float(c['balance']) / 100000000] for c in accounts ], key=lambda e: e[(-1)]):
            log[addr] = '%.3f' % vote
            sum_ += vote

        log['%d voters' % len(accounts)] = '%.3f' % sum_
        util.prettyPrint(log)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\db\old_updates.py
# Compiled at: 2012-11-23 17:34:14
"""This module allows the update of old databases to new formats
To avoid cyclic references dont import db stuff on base level
"""
from __future__ import absolute_import, unicode_literals, print_function
import logging
logger = logging.getLogger(__name__)
import datetime, BTrees.OOBTree as _oo, BTrees.IOBTree as _io, persistent.list as _pl
from banta.db import models as _mods

def v1(root):
    import banta.utils
    bills = root[b'bills']
    new_bills = _io.IOBTree()
    for b in bills.values():
        if isinstance(b, _mods.Bill):
            b.time = banta.utils.dateTimeToInt(b.date)
            new_bills[b.time] = b

    root[b'bills'] = new_bills
    root[b'providers'] = _oo.OOBTree()


def v2(root):
    root[b'users'] = _pl.PersistentList()
    default_user = _mods.User(b'User')
    root[b'users'].append(default_user)
    for b in root[b'bills'].values():
        if b.user is None:
            b.user = default_user

    root[b'moves'] = _io.IOBTree()
    return


def v3(root):
    if b'categories' not in root:
        root[b'categories'] = _pl.PersistentList()
        root[b'categories'].append(_mods.Category(b'Rubro Principal'))


def v4(root):
    for prod in root[b'products'].values():
        prod.description = b''
        prod.pack_units = 1
        prod.buy_price = 0.0
        prod.external_code = b''

    root[b'buys'] = _io.IOBTree()


def v5(root):
    root[b'limits'] = _pl.PersistentList()


def v6(root):
    for u in root[b'users']:
        u.balance = 0.0


def v7(root):
    clients = root[b'clients']
    for oldkey in clients.keys()[:]:
        newkey = oldkey.decode(b'utf-8', b'ignore')
        client = clients[oldkey]
        del clients[oldkey]
        client.code = newkey
        clients[newkey] = client

    products = root[b'products']
    for oldkey in products.keys()[:]:
        newkey = oldkey.decode(b'utf-8', b'ignore')
        prod = products[oldkey]
        del products[oldkey]
        prod.code = newkey
        products[newkey] = prod


def v8(root):
    """'Move' the objects... the path has changed, so the class-link of the objects is broken
        now they link to a non-existent class because the class code is not stored in the same path
        as before"""
    root[b'printer'].__class__ = _mods.Printer
    for tp in root[b'typePays']:
        tp.__class__ = _mods.TypePay

    root[b'typePays']._p_changed = True
    for user in root[b'users']:
        user.__class__ = _mods.User

    root[b'users']._p_changed = True
    for cat in root[b'categories']:
        cat.__class__ = _mods.Category

    root[b'categories']._p_changed = True
    for lim in root[b'limits']:
        lim.__class__ = _mods.Limit
        if lim.product:
            lim.product.__class__ = _mods.Product
            lim._p_changed = True

    for c in root[b'clients'].values():
        c.__class__ = _mods.Client
        root[b'clients'][c.code] = c

    for prov in root[b'providers'].values():
        prov.__class__ = _mods.Provider
        root[b'providers'][prov.code] = prov

    for move in root[b'moves'].values():
        move.__class__ = _mods.Move
        if move.product:
            move.product.__class__ = _mods.Product
            move._p_changed = True
        root[b'moves'][move.time] = move

    for buy in root[b'buys'].values():
        buy.__class__ = _mods.Buy
        if buy.product:
            buy.product.__class__ = _mods.Product
            buy._p_changed = True
        root[b'buys'][buy.time] = buy

    for prod in root[b'products'].values():
        prod.__class__ = _mods.Product
        if prod.provider:
            prod.provider.__class__ = _mods.Provider
        if prod.category:
            prod.category.__class__ = _mods.Category
        prod._p_changed = True
        root[b'products'][prod.code] = prod

    for bill in root[b'bills'].values():
        bill.__class__ = _mods.Bill
        if bill.client:
            bill.client.__class__ = _mods.Client
        if bill.ptype:
            bill.ptype.__class__ = _mods.TypePay
        if bill.user:
            bill.user.__class__ = _mods.User
        for i in bill.items:
            i.__class__ = _mods.Item
            if i.product:
                i.product.__class__ = _mods.Product
                i.product = i.product
                if i.product.category:
                    i.product.category.__class__ = _mods.Category
                    i.product.categry = i.product.category
                    if i.product.provider:
                        i.product.provider.__class__ = _mods.Provider
                        i.product.provider = i.product.provider
                        i.product._p_changed = True
            i._p_changed = True

        bill.items._p_changed = True
        bill._p_changed = True
        root[b'bills'][bill.time] = bill

    root._p_changed = True


def v9(root):
    old_clients = root[b'clients']
    new_clients = _io.IOBTree()
    for i, c in enumerate(old_clients.values()):
        c.idn = i
        new_clients[i] = c

    root[b'clients'] = new_clients
    for prod in root[b'products'].values():
        prod.setName(prod.name)

    for cli in root[b'clients'].values():
        cli.setName(cli.name)
        cli.setAddress(cli.address)


def blankInit(root):
    """Initializes the database from zero.
        """
    typePays = b'typePays'
    root[typePays] = _pl.PersistentList()
    root[typePays].append(_mods.TypePay(b'Efectivo'))
    root[typePays].append(_mods.TypePay(b'Tarjeta de Crédito (con recargo)', 0.1))
    root[typePays].append(_mods.TypePay(b'Cheque (con recargo)', 0.2))
    root[b'providers'] = _oo.OOBTree()
    root[b'products'] = _oo.OOBTree()
    root[b'clients'] = _io.IOBTree()
    cli_code = b'00000000'
    cli = _mods.Client(cli_code, b'Consumidor Final', doc_type=_mods.Client.DOC_DNI)
    cli.idn = 0
    root[b'clients'][cli.idn] = cli
    root[b'bills'] = _io.IOBTree()
    root[b'expire_date'] = datetime.date.today() - datetime.timedelta(days=5)
    root[b'license'] = _mods.LICENSE_FREE
    root[b'current_date'] = datetime.date.today()
    root[b'printer'] = _mods.Printer()
    root[b'users'] = _pl.PersistentList()
    root[b'users'].append(_mods.User(b'User'))
    root[b'moves'] = _io.IOBTree()
    root[b'buys'] = _io.IOBTree()
    root[b'limits'] = _pl.PersistentList()
    root[b'categories'] = _pl.PersistentList()
    root[b'categories'].append(_mods.Category(b'Rubro principal'))
    root[b'version'] = 9


UPDATES = {7: v8, 
   8: v9}

def init(zodb):
    """Initializes the db, and leave it in its most updated form"""
    update(zodb, b'version', blankInit, UPDATES)


def update(zodb, version_key, init_callback, update_callbacks):
    keys = update_callbacks.keys()
    keys.sort()
    latest = keys[(-1)] + 1
    version = zodb.root.get(version_key)
    if version is None:
        init_callback(zodb.root)
        msg = b"Database initialized on '%s'." % (version_key,)
        zodb.commit(b'system', msg)
        logger.info(msg)
    else:
        logger.info(b'Checking database version.... Aplying updates if necesary. Might take a while')
        for v_from in range(version, latest):
            update_callbacks[v_from](zodb.root)
            zodb.root[version_key] = v_from + 1
            msg = b"Database upgraded to version '%s':%s " % (version_key, v_from + 1)
            zodb.commit(b'system', msg)
            logger.info(msg)

    zodb.commit()
    return
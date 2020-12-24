# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\banta\db\updates.py
# Compiled at: 2013-02-01 16:52:58
"""This module allows the update of old databases to new formats
To avoid cyclic references dont import db stuff on base level
"""
from __future__ import absolute_import, unicode_literals, print_function
import logging
logger = logging.getLogger(__name__)
import datetime, BTrees.OOBTree as _oo, BTrees.IOBTree as _io, persistent.list as _pl
from banta.db import models as _mods

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


def v10(root):
    for u in root[b'users']:
        u.password = b''

    for cli in root[b'clients'].values():
        if cli.tax_type > 5:
            cli.tax_type -= 1


def v11(root):
    root[b'typeTax'] = _pl.PersistentList()
    root[b'typeTax'].append(_mods.TypeTax(b'Exento', 0))
    root[b'typeTax'].append(_mods.TypeTax(b'Bien de cambio', 0.21))
    root[b'typeTax'].append(_mods.TypeTax(b'Bien de uso', 0.105))
    root[b'typeTax'].append(_mods.TypeTax(b'Cigarrillos', 0.0667))
    root[b'typeTax'].append(_mods.TypeTax(b'Teléfono', 0.27))


def v12(root):
    v11(root)
    taxes = root[b'typeTax']
    for pro in root[b'products'].values():
        indice = pro.tax_type
        if isinstance(indice, int):
            try:
                pro.tax_type = taxes[indice]
            except:
                pro.tax_type = taxes[0]

        else:
            pro.tax_type = taxes[0]

    for b in root[b'bills'].values():
        for i in b.items:
            indice = getattr(i, b'tax_type', 0)
            if isinstance(indice, int):
                try:
                    i.tax_type = taxes[indice]
                except:
                    i.tax_type = taxes[0]

            else:
                i.tax_type = taxes[0]


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
    cli = _mods.Client(cli_code, b'Consumidor Final', doc_type=_mods.Client.DOC_DNI, save=False)
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
    root[b'typeTax'] = _pl.PersistentList()
    root[b'typeTax'].append(_mods.TypeTax(b'Exento', 0))
    root[b'typeTax'].append(_mods.TypeTax(b'Bien de cambio', 0.21))
    root[b'typeTax'].append(_mods.TypeTax(b'Bien de uso', 0.105))
    root[b'typeTax'].append(_mods.TypeTax(b'Cigarrillos', 0.0667))
    root[b'typeTax'].append(_mods.TypeTax(b'Teléfono', 0.27))
    root[b'version'] = 11


UPDATES = {8: v9, 
   9: v10, 
   10: v11, 
   11: v12}

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

    return
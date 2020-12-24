# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/Base/brand.py
# Compiled at: 2013-01-08 07:18:21
import logging
from Acquisition import aq_base
from lbn.zenoss.packutils import addZenPackObjects
from config import PROJECTNAME
logger = logging.getLogger(PROJECTNAME)
info = logger.info
ZENPACKS = (
 ('ZenPacks.lbn.Base', 'Last Bastion Network shims for Zenoss'),
 ('ZenPacks.lbn.ZopeMonitor', 'Performance statistics of (remote) Zope server'),
 ('ZenPacks.lbn.LDAPMonitor', 'Performance statistics of (remote) LDAP server'),
 ('ZenPacks.oie.Kannel', 'Performance statistics of (remote) Kannel SMPP/SMSC server'))

def addBranding(dmd, zenpack):
    """
    Add LBN Manufacturer/Software into Zenoss
    """
    manufacturers = dmd.Manufacturers
    if not getattr(aq_base(manufacturers), 'LBN', None):
        info('adding Manufacturer - LBN')
        manufacturers.manage_addProduct['ZenModel'].manage_addManufacturer('LBN')
        manufacturers.LBN.manage_changeProperties(url='http://au.last-bastion.net', supportNumber='+61 2 8399 1271', address1='407 The Foundry, 181 Lawson Street', address2='Darlington', city='Sydney', state='NSW', country='Australia', zip='2008')
    lbn = manufacturers.LBN
    products = lbn.products
    for (packname, desc) in ZENPACKS:
        if not getattr(aq_base(products), packname, None):
            info('adding product - %s' % packname)
            lbn.manage_addSoftware(prodName=packname)
            getattr(products, packname).manage_changeProperties(description=desc)

    if not getattr(aq_base(products), 'BastionLinux', None):
        info('adding software - BastionLinux')
        lbn.manage_addSoftware(prodName='BastionLinux', isOS=True)
        bl = products.BastionLinux
        bl.manage_changeProperties(description='Enterprise Zope/Plone/Zenoss Distro http://linux.last-bastion.net')
    addZenPackObjects(zenpack, (lbn,))
    return
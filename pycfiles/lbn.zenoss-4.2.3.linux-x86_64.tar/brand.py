# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/brand.py
# Compiled at: 2010-09-09 07:19:41
from Acquisition import aq_base
from packutils import addZenPackObjects
ZENPACKS = (
 ('ZenMaster', "Master Zenoss for collecting stats from other remote Zenoss's"),
 ('ZenSlave', 'Slave Zenoss for reporting stats to ZenMaster'),
 ('ZopeMonitor', 'Performance statistics of remote Zope instance'))

def addBranding(dmd, zenpack):
    """
    Add LBN Manufacturer/Software into Zenoss
    """
    manufacturers = dmd.Manufacturers
    if not getattr(aq_base(manufacturers), 'LBN', None):
        manufacturers.manage_addProduct['ZenModel'].manage_addManufacturer('LBN')
        manufacturers.LBN.manage_changeProperties(url='http://au.last-bastion.net', supportNumber='+61 2 8399 1271', address1='Unit 407, 181 Lawson Street', address2='Darlington', city='Sydney', state='NSW', country='Australia', zip='2008')
    lbn = manufacturers.LBN
    products = lbn.products
    for zpack in ZENPACKS:
        packname = 'ZenPacks.lbn.%s' % zpack[0]
        if not getattr(aq_base(products), packname, None):
            lbn.manage_addSoftware(prodName=packname)
            getattr(products, packname).manage_changeProperties(description=zpack[1])

    if not getattr(aq_base(products), 'BastionLinux', None):
        lbn.manage_addSoftware(prodName='BastionLinux', isOS=True)
        bl = products.BastionLinux
        bl.manage_changeProperties(description='Enterprise Zope/Plone/Zenoss Distro http://linux.last-bastion.net')
    addZenPackObjects(zenpack, (lbn,))
    return
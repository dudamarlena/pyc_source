# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/monkeypatches.py
# Compiled at: 2013-02-04 11:58:00
import logging, os, sys, OFS
from App.ImageFile import ImageFile
from App.special_dtml import DTMLFile
GLOBALS = globals()
logger = logging.getLogger('lbn.zenoss')

def noop(*args, **kw):
    pass


logger.info('monkeypatching ZenUtils.Security')
from Products.ZenUtils import Security
Security._createInitialUser = noop
logger.info('turning off IPv6')

def ipv6_available():
    return False


from Products.ZenUtils import Utils
Utils.ipv6_available = ipv6_available
from ZPublisher.Converters import type_converters, field2string
type_converters['password'] = field2string
from Products.ZenModel.ZenModelRM import ZenModelRM
ZenModelRM.manage_propertiesForm = DTMLFile('dtml/properties', GLOBALS, property_extensible_schema__=1)
logger.info('added type converters: password, keyedselection')
from Products.ZenRelations.ToManyRelationshipBase import ToManyRelationshipBase, RelationshipBase
ToManyRelationshipBase.manage_options = ToManyRelationshipBase.manage_options + OFS.SimpleItem.SimpleItem.manage_options
from Products.ZenRelations.ToManyRelationship import ToManyRelationship
_remoteRemoveOrig = ToManyRelationship._remoteRemove

def _remoteRemove(self, obj=None):
    """
    remove an object from the far side of this relationship
    if no object is passed in remove all objects
    """
    try:
        _remoteRemoveOrig(self, obj)
    except (AttributeError, ValueError):
        pass


ToManyRelationship._remoteRemove = _remoteRemove
from Products import OFSP
OFSP.misc_ = misc_ = {}
for icon in ('ZenossInfo_icon', 'RelationshipManager_icon', 'portletmanager'):
    misc_[icon] = ImageFile('www/%s.gif' % icon, GLOBALS)

from Products.ZenWidgets.PortletManager import PortletManager
PortletManager.icon = 'misc_/OFSP/portletmanager'
from Products.ZenModel.ZenossInfo import ZenossInfo
ZenossInfo.icon = 'misc_/OFSP/ZenossInfo_icon'
from Products.ZenRelations.RelationshipManager import RelationshipManager
RelationshipManager.icon = 'misc_/OFSP/RelationshipManager_icon'
logger.info('added ZMI icons')
import AccessControl
from Products.ZenRelations.ZItem import ZItem
ZItem.manage_options = AccessControl.Owned.Owned.manage_options + ({'label': 'Interfaces', 'action': 'manage_interfaces'},)
from Products.ZenUtils import Skins
findZenPackRootOrig = Skins.findZenPackRoot

def findZenPackRoot(base):
    if base.find('site-packages') != -1:
        dirs = base.split(os.path.sep)
        ndx = dirs.index('site-packages')
        return ('.').join(dirs[ndx + 1:-1])
    return findZenPackRootOrig(base)


Skins.findZenPackRoot = findZenPackRoot
from Products.ZenModel.ZenPackLoader import ZPLSkins, ZPLBin, ZPLLibExec
ZPLSkinsload = ZPLSkins.load
ZPLSkinsunload = ZPLSkins.unload
ZPLBinload = ZPLBin.load
ZPLLibExecload = ZPLLibExec.load

def skinLoad(self, pack, app):
    try:
        ZPLSkinsload(self, pack, app)
    except Exception, e:
        logger.warn(str(e), exc_info=True)


def skinUnload(self, pack, app, leaveObjects=False):
    try:
        ZPLSkinsunload(self, pack, app, leaveObjects)
    except Exception, e:
        logger.warn(str(e), exc_info=True)


def binLoad(self, pack, app):
    try:
        ZPLBinload(self, pack, app)
    except Exception, e:
        logger.warn(str(e), exc_info=True)


def libexecLoad(self, pack, app):
    try:
        ZPLLibExecload(self, pack, app)
    except Exception, e:
        logger.warn(str(e), exc_info=True)


ZPLSkins.load = skinLoad
ZPLSkins.unload = skinUnload
ZPLBin.load = binLoad
ZPLLibExec.load = libexecLoad
from Products.ZenModel.ZenPack import ZenPack
ZenPack.meta_data = 'ZenPack'

def createZProperties(self, app=None, REQUEST=None):
    """
    Create zProperties in the ZenPack's self.packZProperties
    
    @param app: ZenPack
    @type app: ZenPack object
    """
    devices = app and app.zport.dmd.Devices or self.zport.dmd.Devices
    for (name, value, pType) in self.packZProperties:
        if not devices.hasProperty(name):
            devices._setProperty(name, value, pType)
        if not getattr(devices, name):
            setattr(devices, name, value)

    if REQUEST:
        return self.manage_main(self, REQUEST)


ZenPack.createZProperties = createZProperties
logger.info('added ZMI-recoverable ZenPack createZProperties')
from Products.ZenUtils.CmdBase import CmdBase
getConfigFileDefaultsOrig = CmdBase.getConfigFileDefaults

def getConfigFileDefaults(self, filename):
    """
    Parse a config file 
    """
    try:
        return getConfigFileDefaultsOrig(self, filename)
    except IOError:
        pass


CmdBase.getConfigFileDefaults = getConfigFileDefaults
logger.info('stop zope.conf being stomped on')
pyver = sys.version[:3]
if sys <= '2.6':
    import subprocess

    def check_output(args):
        """ simplified check_output implementation for py2.6 """
        return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]


    subprocess.check_output = check_output
    logger.info('monkeypatched subprocess.check_output')

    class NullHandler(logging.Handler):
        lock = None

        def emit(self, record):
            pass

        def handle(self, record):
            pass

        def createLock(self):
            return


    logging.NullHandler = NullHandler
    logger.info('monkeypatched logging.NullHandler')
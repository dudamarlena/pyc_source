# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./PortableServer__POA.py
# Compiled at: 2018-07-20 10:03:27
# Size of source mod 2**32: 2561 bytes
import omniORB
from omniORB import CORBA, PortableServer
import _omnipy

class ServantManager(PortableServer.Servant):
    _NP_RepositoryId = PortableServer.ServantManager._NP_RepositoryId
    _omni_op_d = {}
    _omni_special = 1


ServantManager._omni_skeleton = ServantManager

class ServantActivator(ServantManager):
    _NP_RepositoryId = PortableServer.ServantActivator._NP_RepositoryId
    _omni_op_d = {'incarnate':PortableServer.ServantActivator._d_incarnate, 
     'etherealize':PortableServer.ServantActivator._d_etherealize}
    _omni_op_d.update(ServantManager._omni_op_d)
    _omni_special = 1


ServantActivator._omni_skeleton = ServantActivator

class ServantLocator(ServantManager):
    _NP_RepositoryId = PortableServer.ServantLocator._NP_RepositoryId
    _omni_op_d = {'preinvoke':PortableServer.ServantLocator._d_preinvoke, 
     'postinvoke':PortableServer.ServantLocator._d_postinvoke}
    _omni_op_d.update(ServantManager._omni_op_d)
    _omni_special = 1


ServantLocator._omni_skeleton = ServantLocator

class AdapterActivator(PortableServer.Servant):
    _NP_RepositoryId = PortableServer.AdapterActivator._NP_RepositoryId
    _omni_op_d = {'unknown_adapter': PortableServer.AdapterActivator._d_unknown_adapter}
    _omni_special = 1


AdapterActivator._omni_skeleton = AdapterActivator
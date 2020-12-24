# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/registry.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 3355 bytes


def _gridengineBatchSystemFactory():
    from toil.batchSystems.gridengine import GridEngineBatchSystem
    return GridEngineBatchSystem


def _parasolBatchSystemFactory():
    from toil.batchSystems.parasol import ParasolBatchSystem
    return ParasolBatchSystem


def _lsfBatchSystemFactory():
    from toil.batchSystems.lsf import LSFBatchSystem
    return LSFBatchSystem


def _singleMachineBatchSystemFactory():
    from toil.batchSystems.singleMachine import SingleMachineBatchSystem
    return SingleMachineBatchSystem


def _mesosBatchSystemFactory():
    from toil.batchSystems.mesos.batchSystem import MesosBatchSystem
    return MesosBatchSystem


def _slurmBatchSystemFactory():
    from toil.batchSystems.slurm import SlurmBatchSystem
    return SlurmBatchSystem


def _torqueBatchSystemFactory():
    from toil.batchSystems.torque import TorqueBatchSystem
    return TorqueBatchSystem


def _htcondorBatchSystemFactory():
    from toil.batchSystems.htcondor import HTCondorBatchSystem
    return HTCondorBatchSystem


def _kubernetesBatchSystemFactory():
    from toil.batchSystems.kubernetes import KubernetesBatchSystem
    return KubernetesBatchSystem


_DEFAULT_REGISTRY = {'parasol':_parasolBatchSystemFactory, 
 'singleMachine':_singleMachineBatchSystemFactory, 
 'single_machine':_singleMachineBatchSystemFactory, 
 'gridEngine':_gridengineBatchSystemFactory, 
 'gridengine':_gridengineBatchSystemFactory, 
 'lsf':_lsfBatchSystemFactory, 
 'LSF':_lsfBatchSystemFactory, 
 'mesos':_mesosBatchSystemFactory, 
 'Mesos':_mesosBatchSystemFactory, 
 'slurm':_slurmBatchSystemFactory, 
 'Slurm':_slurmBatchSystemFactory, 
 'torque':_torqueBatchSystemFactory, 
 'Torque':_torqueBatchSystemFactory, 
 'htcondor':_htcondorBatchSystemFactory, 
 'HTCondor':_htcondorBatchSystemFactory, 
 'kubernetes':_kubernetesBatchSystemFactory, 
 'Kubernetes':_kubernetesBatchSystemFactory, 
 'k8s':_kubernetesBatchSystemFactory}
_UNIQUE_NAME = {
 'parasol',
 'singleMachine',
 'gridEngine',
 'LSF',
 'Mesos',
 'Slurm',
 'Torque',
 'HTCondor',
 'Kubernetes'}
_batchSystemRegistry = _DEFAULT_REGISTRY.copy()
_batchSystemNames = set(_UNIQUE_NAME)

def addBatchSystemFactory(key, batchSystemFactory):
    _batchSystemNames.add(key)
    _batchSystemRegistry[key] = batchSystemFactory


def batchSystemFactoryFor(batchSystem):
    return _batchSystemRegistry[batchSystem]


def defaultBatchSystem():
    return 'singleMachine'


def uniqueNames():
    return list(_batchSystemNames)


def batchSystems():
    list(set(_batchSystemRegistry.values()))
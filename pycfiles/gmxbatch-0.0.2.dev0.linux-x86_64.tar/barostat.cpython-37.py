# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/environment/barostat.py
# Compiled at: 2020-02-18 07:08:19
# Size of source mod 2**32: 598 bytes


class Barostat:
    ref_pressure: float
    couplingtype: str
    tau: float
    compressibility: float
    algorithm = 'Parrinello-Rahman'
    algorithm: str

    def __init__(self, ref_pressure: float, tau: float, compressibility: float=4.6e-05, couplingtype: str='isotropic', algorithm: str='Parrinello-Rahman'):
        self.ref_pressure = ref_pressure
        self.couplingtype = couplingtype
        self.compressibility = compressibility
        self.tau = tau
        self.algorithm = algorithm

    def __repr__(self) -> str:
        return f"Barostat:\n  {self.ref_pressure:.3f}"
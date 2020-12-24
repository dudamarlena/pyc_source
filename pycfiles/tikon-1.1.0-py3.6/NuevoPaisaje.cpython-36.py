# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\NuevoPaisaje.py
# Compiled at: 2017-02-20 10:45:05
# Size of source mod 2**32: 1187 bytes
from tikon.Coso import Simulable

class Paisaje(Simulable):
    __doc__ = '\n    \n    '
    ext = '.psj'

    def _prep_obs_exper(símismo, exper):
        raise NotImplementedError

    def _procesar_predics_calib(símismo):
        raise NotImplementedError

    def incrementar(símismo, paso, i, extrn):
        raise NotImplementedError

    def _sacar_líms_coefs_interno(símismo):
        raise NotImplementedError

    def _llenar_coefs(símismo, n_rep_parám, calibs, comunes, usar_especificadas):
        raise NotImplementedError

    def dibujar(símismo, mostrar=True, archivo=None, exper=None):
        raise NotImplementedError

    def _procesar_validación(símismo):
        raise NotImplementedError

    def _prep_args_simul_exps(símismo, exper, n_rep_estoc, n_rep_paráms):
        raise NotImplementedError

    def _actualizar_vínculos_exps(símismo, experimento, corresp):
        raise NotImplementedError

    def _sacar_coefs_interno(símismo):
        raise NotImplementedError
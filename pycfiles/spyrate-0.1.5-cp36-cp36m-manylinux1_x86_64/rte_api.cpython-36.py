# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-req-build-aao45hdu/spyrate/rte/rte_api.py
# Compiled at: 2019-07-30 06:23:08
# Size of source mod 2**32: 4256 bytes
"""
This module contains the API definitions needed to compile CFFI wrappers
"""

class RTEAPIDefinition(object):
    __doc__ = '\n    class holding C API definitions\n    '

    def __init__(self, precision='double'):
        """
        Create API definition object

        Args:
            precision (string, optional):
                whether the library has been compiled with single or double
                precision. Should be one of :code:`single` or :code:`double`.
                Defaults to :code:`double`.
        """
        self.precision_dict = {}
        self.precision_def_dict = {}
        self._precision = precision
        self.precision_dict['single'] = 'float'
        self.precision_dict['double'] = 'double'
        self.precision_def_dict['single'] = '-DRTE_SINGLE_PRECISION'
        self.precision_def_dict['double'] = '-DRTE_DOUBLE_PRECISION'

    @property
    def bc_gpt_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void apply_BC_gpt(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *inc_flux, {0} *fluxdn);\n\n       '.format(library_precision)

    @property
    def bc_factor_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void apply_BC_factor(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *inc_flux, {0} *factor, {0} *fluxdn);\n\n        '.format(library_precision)

    @property
    def bc_0_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void apply_BC_0(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *fluxdn);\n\n       '.format(library_precision)

    @property
    def lw_solver_noscat_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void lw_solver_noscat(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *D, {0} *weight, {0} *tau, {0} *lay_source,\n   {0} *lev_source_inc, {0} *lev_source_dec, {0} *sfc_emis,\n   {0} *sfc_src, {0} *radn_up, {0} *radn_down);\n\n       '.format(library_precision)

    @property
    def lw_solver_noscat_gauss_quad_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void lw_solver_noscat_GaussQuad(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *nmus,  {0} *Ds, {0} *weights, {0} *tau, {0} *lay_source,\n   {0} *lev_source_inc, {0} *lev_source_dec, {0} *sfc_emis,\n   {0} *sfc_src, {0} *flux_up, {0} *flux_down);\n\n       '.format(library_precision)

    @property
    def lw_solver_2stream_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void lw_solver_2stream(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *tau, {0} *ssa, {0} *g, {0} *lay_source,\n   {0} *lev_source_inc, {0} *lev_source_dec, {0} *sfc_emis,\n   {0} *sfc_src, {0} *flux_up, {0} *flux_down);\n\n       '.format(library_precision)

    @property
    def sw_solver_noscat_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void sw_solver_noscat(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *tau, {0} *mu0, {0} *flux_dir);\n\n       '.format(library_precision)

    @property
    def sw_solver_2stream_api(self):
        """
        return the specified property
        """
        library_precision = self.precision_dict[self._precision]
        return '\n   void sw_solver_2stream(int *ncol, int *nlay, int *ngpt,\n   bool *top_at_1, {0} *tau, {0} *ssa, {0} *g, {0} *mu0,\n   {0} *sfc_alb_dir, {0} *sfc_alb_dif, {0} *flux_up,\n   {0} *flux_dn, {0} *flux_dir);\n\n       '.format(library_precision)

    @property
    def compiler_def(self):
        """
        return the specified property
        """
        return self.precision_def_dict[self._precision]
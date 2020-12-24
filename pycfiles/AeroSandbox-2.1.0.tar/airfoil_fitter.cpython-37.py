# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\tools\airfoil_fitter\airfoil_fitter.py
# Compiled at: 2020-04-24 00:37:16
# Size of source mod 2**32: 18348 bytes
"""
Functions to fit automatic-differentiable models to aerodynamic data from an airfoil.
Requires the xfoil package from PyPI; see aerosandbox.geometry for more information on this.
"""
from aerosandbox.geometry import *
from aerosandbox.tools.fitting import *
from aerosandbox.tools.miscellaneous import eng_string, remove_nans
import plotly.express as px
import plotly.graph_objects as go
import dill as pickle, multiprocessing_on_dill as mp, time

class AirfoilFitter:

    def __init__(self, airfoil, parallel=True, verbose=True):
        airfoil.has_xfoil_data()
        self.airfoil = airfoil
        self.verbose = verbose

    @staticmethod
    def fit_weights(x):
        return 1 + 3 * (x['Cl'] >= 0) * (x['alpha'] >= 0)

    def plot_xfoil_alpha_Re(self, y_data_name, model=None, params_solved=None, title=None, log_z=False, show=True):
        """
        See the docstring of the "fit" function in aerosandbox.tools.casadi_tools for syntax.
        :param model:
        :param x_data:
        :param y_data:
        :param params_solved:
        :param title:
        :param show:
        :return:
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=(self.airfoil.xfoil_data_1D['alpha']),
          y=(self.airfoil.xfoil_data_1D['Re']),
          z=(self.airfoil.xfoil_data_1D[y_data_name]),
          mode='markers',
          marker=dict(size=2,
          color='black')))
        if model is not None:
            n = 60
            linspace = lambda x: np.linspace(np.min(x), np.max(x), n)
            logspace = lambda x: np.logspace(np.log10(np.min(x)), np.log10(np.max(x)), n)
            x1 = linspace(self.airfoil.xfoil_data_1D['alpha'])
            x2 = logspace(self.airfoil.xfoil_data_1D['Re'])
            X1, X2 = np.meshgrid(x1, x2)
            x_model = {'alpha':X1.reshape(-1), 
             'Re':X2.reshape(-1)}
            y_model = np.array(model(x_model, params_solved)).reshape((n, n))
            fig.add_trace(go.Surface(contours={}, x=x1,
              y=x2,
              z=y_model,
              surfacecolor=(np.log10(y_model) if log_z else y_model),
              colorscale='plasma'))
        fig.update_layout(scene=dict(xaxis=dict(title='Alpha'),
          yaxis=dict(type='log',
          title='Re'),
          zaxis=dict(type=('log' if log_z else 'linear'),
          title='f(alpha, Re)')),
          title=title)
        if show:
            fig.show()
        return fig

    def fit_xfoil_data_Cl(self, supercritical_Re_threshold=1000000.0, subcritical_Re_threshold=50000.0, plot_fit=True):
        d = self.airfoil.xfoil_data_1D
        raw_sigmoid = lambda x: x / (1 + x ** 4) ** 0.25

        def sigmoid(x, x_cent, x_scale, y_cent, y_scale, raw_sigmoid=raw_sigmoid):
            return y_cent + y_scale * raw_sigmoid((x - x_cent) / x_scale)

        def model_Cl_turbulent(x, p, sigmoid=sigmoid):
            log10_Re = cas.log10(x['Re'])
            Cl_turbulent = sigmoid(x['alpha'], p['clt_a_c'], p['clt_a_s'], p['clt_cl_c'], p['clt_cl_s']) + p['clt_clre'] * log10_Re
            return Cl_turbulent

        Cl_turbulent_params_guess = {'clt_a_c':0, 
         'clt_a_s':12, 
         'clt_cl_c':0, 
         'clt_cl_s':1.5, 
         'clt_clre':0}
        Cl_turbulent_param_bounds = {'clt_a_c':(None, None), 
         'clt_a_s':(0, None), 
         'clt_cl_c':(None, None), 
         'clt_cl_s':(0, 4), 
         'clt_clre':(None, None)}
        Cl_turbulent_params_solved = fit(model=model_Cl_turbulent,
          x_data=d,
          y_data=(d['Cl']),
          param_guesses=Cl_turbulent_params_guess,
          param_bounds=Cl_turbulent_param_bounds,
          weights=((d['Re'] >= supercritical_Re_threshold) * self.fit_weights(d)),
          verbose=(self.verbose))

        def model_Cl_laminar(x, p, sigmoid=sigmoid):
            Cl_laminar = p['cll_cla'] * x['alpha'] + p['cll_cl0'] + sigmoid(x['alpha'], p['clld_a_c'], p['clld_a_s'], 0, p['clld_cl_s'])
            return Cl_laminar

        Cl_laminar_params_guess = {'cll_cla':0.04, 
         'cll_cl0':0, 
         'clld_a_c':0, 
         'clld_a_s':2, 
         'clld_cl_s':0.1}
        Cl_laminar_param_bounds = {'cll_cla':(0.01, 0.2), 
         'cll_cl0':(None, 1.5), 
         'clld_a_c':(-8, 8), 
         'clld_a_s':(0, 8), 
         'clld_cl_s':(0, 0.4)}
        Cl_laminar_params_solved = fit(model=model_Cl_laminar,
          x_data=d,
          y_data=(d['Cl']),
          param_guesses=Cl_laminar_params_guess,
          param_bounds=Cl_laminar_param_bounds,
          weights=((d['Re'] <= subcritical_Re_threshold) * self.fit_weights(d)),
          verbose=(self.verbose))

        def model_Cl_blend(x, p, sigmoid=sigmoid, model_Cl_turbulent=model_Cl_turbulent, model_Cl_laminar=model_Cl_laminar):
            v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x
            log10_Re = cas.log10(x['Re'])
            blend_input = -p['clb_hardness'] * (p['clb_Re1'] - log10_Re)
            blend = sigmoid(blend_input, 0, 1, 0.5, 0.5)
            Cl = blend * model_Cl_turbulent(x, p) + (1 - blend) * model_Cl_laminar(x, p)
            return Cl

        Cl_blend_params_guess = {**Cl_turbulent_params_solved, **Cl_laminar_params_solved, **{'clb_hardness':3, 
         'clb_Re1':5}}
        Cl_blend_param_bounds = {'clb_hardness':(0.01, 100), 
         'clb_Re1':(3, 6)}
        Cl_blend_params_solved = fit(model=model_Cl_blend,
          x_data=d,
          y_data=(d['Cl']),
          param_guesses=Cl_blend_params_guess,
          param_bounds={**{k:(v, v) for k, v in Cl_laminar_params_solved.items()}, **{k:(v, v) for k, v in Cl_turbulent_params_solved.items()}, **Cl_blend_param_bounds},
          weights=(self.fit_weights(d)),
          verbose=(self.verbose))
        Cl_blend_params_solved = fit(model=model_Cl_blend,
          x_data=d,
          y_data=(d['Cl']),
          param_guesses=Cl_blend_params_solved,
          param_bounds={**Cl_laminar_param_bounds, **Cl_turbulent_param_bounds, **Cl_blend_param_bounds},
          weights=(self.fit_weights(d)),
          verbose=(self.verbose))
        if plot_fit:
            self.plot_xfoil_alpha_Re(y_data_name='Cl',
              model=model_Cl_blend,
              params_solved=Cl_blend_params_solved,
              title='Fit: Lift Coefficient (Blend)')

        def Cl_function(alpha, Re, Cl_blend_params_solved=Cl_blend_params_solved, model_Cl_blend=model_Cl_blend):
            return model_Cl_blend(x={'alpha':alpha, 
             'Re':Re},
              p=Cl_blend_params_solved)

        self.Cl_function = Cl_function
        return Cl_function

    def fit_xfoil_data_Cd(self, supercritical_Re_threshold=1000000.0, subcritical_Re_threshold=50000.0, plot_fit=True):
        d = self.airfoil.xfoil_data_1D
        raw_sigmoid = lambda x: x / (1 + x ** 4) ** 0.25

        def sigmoid(x, x_cent, x_scale, y_cent, y_scale, raw_sigmoid=raw_sigmoid):
            return y_cent + y_scale * raw_sigmoid((x - x_cent) / x_scale)

        def model_log10_Cd_turbulent(x, p, sigmoid=sigmoid):
            v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x
            log10_Re_eff = cas.log10(x['Re']) - 6
            a_scaled = x['alpha'] - p['cdt_a_Cd0'] - p['cdt_a_Cd0_Re'] * log10_Re_eff
            log10_Cd_turbulent = p['cdt_0'] + p['cdt_Re1'] * log10_Re_eff + p['cdt_av_scale'] * v(a_scaled, p['cdt_av_k'], p['cdt_av_a'])
            return log10_Cd_turbulent

        model_Cd_turbulent = lambda *args: 10 ** model_log10_Cd_turbulent(*args)
        log10_Cd_turbulent_params_guess = {'cdt_0':-2.5, 
         'cdt_a_Cd0':3, 
         'cdt_a_Cd0_Re':-1, 
         'cdt_Re1':-0.2, 
         'cdt_av_scale':0.07, 
         'cdt_av_k':10, 
         'cdt_av_a':0}
        log10_Cd_turbulent_param_bounds = {'cdt_av_k': (0.01, 100)}
        Cd_turbulent_params_solved = fit(model=model_log10_Cd_turbulent,
          x_data=d,
          y_data=(cas.log10(d['Cd'])),
          param_guesses=log10_Cd_turbulent_params_guess,
          param_bounds=log10_Cd_turbulent_param_bounds,
          weights=((d['Re'] >= supercritical_Re_threshold) * self.fit_weights(d)),
          verbose=(self.verbose))

        def model_log10_Cd_laminar(x, p, sigmoid=sigmoid):
            v = lambda x, k, a: (k + x ** 2) ** 0.5 + a * x
            log10_Re_eff = cas.log10(x['Re']) - 6
            a_scaled = x['alpha'] - p['cdl_a_Cd0'] - p['cdl_a_Cd0_Re'] * log10_Re_eff
            log10_Cd_laminar = p['cdl_0'] + p['cdl_Re1'] * log10_Re_eff + p['cdl_av_scale'] * v(a_scaled, p['cdl_av_k'], p['cdl_av_a'])
            return log10_Cd_laminar

        model_Cd_laminar = lambda *args: 10 ** model_log10_Cd_laminar(*args)
        log10_Cd_laminar_params_guess = {'cdl_0':-2.5, 
         'cdl_a_Cd0':3, 
         'cdl_a_Cd0_Re':-1, 
         'cdl_Re1':-0.2, 
         'cdl_av_scale':0.07, 
         'cdl_av_k':10, 
         'cdl_av_a':0}
        log10_Cd_laminar_param_bounds = {'cdl_av_k': (0.01, 100)}
        Cd_laminar_params_solved = fit(model=model_log10_Cd_laminar,
          x_data=d,
          y_data=(cas.log10(d['Cd'])),
          param_guesses=log10_Cd_laminar_params_guess,
          param_bounds=log10_Cd_laminar_param_bounds,
          weights=((d['Re'] <= subcritical_Re_threshold) * self.fit_weights(d)),
          verbose=(self.verbose))

        def model_log10_Cd_blend(x, p, sigmoid=sigmoid, model_log10_Cd_turbulent=model_log10_Cd_turbulent, model_log10_Cd_laminar=model_log10_Cd_laminar):
            log10_Re_eff = cas.log10(x['Re']) - 5
            alpha_eff = x['alpha']
            blend_input = p['cdb_0'] - p['cdb_Re1'] * log10_Re_eff - p['cdb_a1'] * alpha_eff / 10 - p['cdb_a2'] * (alpha_eff / 10) ** 2
            blend = sigmoid(blend_input, 0, 1, 0.5, 0.5)
            log10_Cd = blend * model_log10_Cd_turbulent(x, p) + (1 - blend) * model_log10_Cd_laminar(x, p)
            return log10_Cd

        model_Cd_blend = lambda *args: 10 ** model_log10_Cd_blend(*args)
        log10_Cd_blend_params_guess = {**Cd_turbulent_params_solved, **Cd_laminar_params_solved, **{'cdb_0':0, 
         'cdb_Re1':-5, 
         'cdb_a1':0, 
         'cdb_a2':0}}
        log10_Cd_blend_param_bounds = {'cdb_0': (-1, 1)}
        Cd_blend_params_solved = fit(model=model_log10_Cd_blend,
          x_data=d,
          y_data=(cas.log10(d['Cd'])),
          param_guesses=log10_Cd_blend_params_guess,
          param_bounds={**{k:(v, v) for k, v in Cd_laminar_params_solved.items()}, **{k:(v, v) for k, v in Cd_turbulent_params_solved.items()}, **log10_Cd_blend_param_bounds},
          weights=(self.fit_weights(d)),
          verbose=(self.verbose))
        Cd_blend_params_solved = fit(model=model_log10_Cd_blend,
          x_data=d,
          y_data=(cas.log10(d['Cd'])),
          param_guesses=Cd_blend_params_solved,
          param_bounds={**log10_Cd_laminar_param_bounds, **log10_Cd_turbulent_param_bounds, **log10_Cd_blend_param_bounds},
          weights=(self.fit_weights(d)),
          verbose=(self.verbose))
        if plot_fit:
            self.plot_xfoil_alpha_Re(y_data_name='Cd',
              model=model_Cd_blend,
              params_solved=Cd_blend_params_solved,
              title='Fit: Drag Coefficient (Blend)',
              log_z=True)

        def Cd_function(alpha, Re, Cd_blend_params_solved=Cd_blend_params_solved, model_log10_Cd_blend=model_log10_Cd_blend):
            return 10 ** model_log10_Cd_blend(x={'alpha':alpha, 
             'Re':Re},
              p=Cd_blend_params_solved)

        self.Cd_function = Cd_function
        return Cd_function
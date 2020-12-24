# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Matemáticas\Ecuaciones.py
# Compiled at: 2017-09-11 13:48:28
# Size of source mod 2**32: 36409 bytes
import numpy as np, tikon.Matemáticas.Incert as Incert
ecs_orgs = {'Crecimiento':{'Modif':{'Nada':{},  'Ninguna':{'r': {'límites':(0, np.inf),  'inter':None}}, 
   'Log Normal Temperatura':{'t':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'p':{'límites':(
      0, np.inf), 
     'inter':None}}}, 
  'Ecuación':{'Nada':{},  'Exponencial':{},  'Logístico':{'K': {'límites':(0, np.inf),  'inter':None}}, 
   'Logístico Presa':{'K': {'límites':(0, np.inf),  'inter':[
           'presa']}}, 
   'Logístico Depredación':{'K': {'límites':(0, np.inf),  'inter':[
           'presa']}}, 
   'Constante':{'n': {'límites':(0, np.inf),  'inter':None}}, 
   'Externo Cultivo':{}}}, 
 'Depredación':{'Ecuación': {'Nada':{},  'Tipo I_Dependiente presa':{'a': {'límites':(0, 1),  'inter':[
                       'presa', 'huésped']}}, 
               'Tipo II_Dependiente presa':{'a':{'límites':(0, 1), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo III_Dependiente presa':{'a':{'límites':(0, 1), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo I_Dependiente ratio':{'a': {'límites':(0, 1),  'inter':[
                       'presa', 'huésped']}}, 
               'Tipo II_Dependiente ratio':{'a':{'límites':(0, 1), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo III_Dependiente ratio':{'a':{'límites':(0, 1), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Beddington-DeAngelis':{'a':{'límites':(0, 1), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'c':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo I_Hassell-Varley':{'a':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'm':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo II_Hassell-Varley':{'a':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'm':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Tipo III_Hassell-Varley':{'a':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'm':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}, 
               'Kovai':{'a':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':[
                  'presa', 'huésped']}}}}, 
 'Muertes':{'Ecuación': {'Nada':{},  'Constante':{'q': {'límites':(0, 1),  'inter':None}}, 
               'Log Normal Temperatura':{'t':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                'p':{'límites':(
                  0, np.inf), 
                 'inter':None}}, 
               'Asimptótico Humedad':{'a':{'límites':(
                  0, np.inf), 
                 'inter':None}, 
                'b':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}}, 
               'Sigmoidal Temperatura':{'a':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                'b':{'límites':(
                  0, np.inf), 
                 'inter':None}}}}, 
 'Edad':{'Ecuación': {'Nada':{},  'Días':{},  'Días grados':{'mín':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                'máx':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}}, 
               'Brière Temperatura':{'t_dev_mín':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                't_letal':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}}, 
               'Logan Temperatura':{'rho':{'límites':(0, 1), 
                 'inter':None}, 
                'delta':{'límites':(0, 1), 
                 'inter':None}, 
                't_letal':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}}, 
               'Brière No Linear Temperatura':{'t_dev_mín':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                't_letal':{'límites':(
                  -np.inf, np.inf), 
                 'inter':None}, 
                'm':{'límites':(
                  0, np.inf), 
                 'inter':None}}}}, 
 'Transiciones':{'Prob':{'Nada':{},  'Constante':{'q': {'límites':(0, 1),  'inter':None}}, 
   'Normal':{'mu':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'sigma':{'límites':(
      0, np.inf), 
     'inter':None}}, 
   'Triang':{'a':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'b':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'c':{'límites':(
      0, np.inf), 
     'inter':None}}, 
   'Cauchy':{'u':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'f':{'límites':(
      0, np.inf), 
     'inter':None}}, 
   'Gamma':{'u':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'f':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'a':{'límites':(
      0, np.inf), 
     'inter':None}}, 
   'Logística':{'u':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'f':{'límites':(
      0, np.inf), 
     'inter':None}}, 
   'T':{'k':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'mu':{'límites':(
      0, np.inf), 
     'inter':None}, 
    'sigma':{'límites':(
      0, np.inf), 
     'inter':None}}}, 
  'Mult':{'Nada':{},  'Linear':{'a': {'límites':(0, np.inf),  'inter':None}}}}, 
 'Reproducción':{'Prob': {'Nada':{},  'Constante':{'a': {'límites':(0, np.inf),  'inter':None}}, 
           'Depredación':{'n': {'límites':(0, np.inf),  'inter':[
                   'presa']}}, 
           'Normal':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'mu':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'sigma':{'límites':(
              0, np.inf), 
             'inter':None}}, 
           'Triang':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'a':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'b':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'c':{'límites':(
              0, np.inf), 
             'inter':None}}, 
           'Cauchy':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'u':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'f':{'límites':(
              0, np.inf), 
             'inter':None}}, 
           'Gamma':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'u':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'f':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'a':{'límites':(
              0, np.inf), 
             'inter':None}}, 
           'Logística':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'u':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'f':{'límites':(
              0, np.inf), 
             'inter':None}}, 
           'T':{'n':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'k':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'mu':{'límites':(
              0, np.inf), 
             'inter':None}, 
            'sigma':{'límites':(
              0, np.inf), 
             'inter':None}}}}, 
 'Movimiento':{},  'Error':{'Dist': {'Normal': {'sigma': {'límites':(0, 1),  'inter':None}}}}}
ecs_suelo = {'profund':{'límites':(
   0, np.inf), 
  'unid':'cm', 
  'cód_DSSAT':'SLDP', 
  'tmñ_DSSAT':5}, 
 'albedo':{'límites':(0, 1), 
  'unid':None, 
  'cód_DSSAT':'SALB', 
  'tmñ_DSSAT':5}, 
 'límite_evap':{'límites':(
   0, np.inf), 
  'unid':'cm', 
  'cód_DSSAT':'SLU1', 
  'tmñ_DSSAT':5}, 
 'taza_drenaje':{'límites':(0, 1), 
  'unid':'día -1', 
  'cód_DSSAT':'SLDR', 
  'tmñ_DSSAT':5}, 
 'factor_drenaje_SCS':{'límites':(30, 100), 
  'unid':None, 
  'cód_DSSAT':'SLDR', 
  'tmñ_DSSAT':5}, 
 'factor_mineral':{'límites':(0, 1), 
  'unid':None, 
  'cód_DSSAT':'SLNF', 
  'tmñ_DSSAT':5}, 
 'factor_fotosyn':{'límites':(0, 1), 
  'unid':None, 
  'cód_DSSAT':'SLPF', 
  'tmñ_DSSAT':5}, 
 'niveles':{'límites':(
   0, np.inf), 
  'unid':'cm', 
  'cód_DSSAT':'SLB', 
  'tmñ_DSSAT':5}, 
 'P_extract':{'límites':(
   0, np.inf), 
  'unid':'mg kg-1', 
  'cód_DSSAT':'SLPX', 
  'tmñ_DSSAT':5}, 
 'P_total':{'límites':(
   0, np.inf), 
  'unid':'mg kg-1', 
  'cód_DSSAT':'SLPT', 
  'tmñ_DSSAT':5}, 
 'P_orgán':{'límites':(
   0, np.inf), 
  'unid':'mg kg -1', 
  'cód_DSSAT':'SLPO', 
  'tmñ_DSSAT':5}, 
 'CaCO3':{'límites':(
   0, np.inf), 
  'unid':'g kg-1', 
  'cód_DSSAT':'SLCA', 
  'tmñ_DSSAT':5}, 
 'Al':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLAL', 
  'tmñ_DSSAT':5}, 
 'Fe':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLFE', 
  'tmñ_DSSAT':5}, 
 'Mn':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLMN', 
  'tmñ_DSSAT':5}, 
 'satur_base':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLBS', 
  'tmñ_DSSAT':5}, 
 'isoterm_P_a':{'límites':(
   0, np.inf), 
  'unid':'mmol kg-1', 
  'cód_DSSAT':'SLPA', 
  'tmñ_DSSAT':5}, 
 'isoterm_P_b':{'límites':(
   0, np.inf), 
  'unid':'mmol kg-1', 
  'cód_DSSAT':'SLPB', 
  'tmñ_DSSAT':5}, 
 'K_intercamb':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLKE', 
  'tmñ_DSSAT':5}, 
 'Mg':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLMG', 
  'tmñ_DSSAT':5}, 
 'Na':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-|', 
  'cód_DSSAT':'SLNA', 
  'tmñ_DSSAT':5}, 
 'S':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SLSU', 
  'tmñ_DSSAT':5}, 
 'conduct_eléc':{'límites':(
   0, np.inf), 
  'unid':'seimen', 
  'cód_DSSAT':'SLEC', 
  'tmñ_DSSAT':5}, 
 'límite_bajo':{'límites':(
   0, np.inf), 
  'unid':None, 
  'cód_DSSAT':'SLLL', 
  'tmñ_DSSAT':5}, 
 'límite_alto':{'límites':(
   0, np.inf), 
  'unid':None, 
  'cód_DSSAT':'SDUL', 
  'tmñ_DSSAT':5}, 
 'límite_alto_sat':{'límites':(
   0, np.inf), 
  'unid':None, 
  'cód_DSSAT':'SSAT', 
  'tmñ_DSSAT':5}, 
 'factor_crec_raíz':{'límites':(0, 1), 
  'unid':None, 
  'cód_DSSAT':'SRGF', 
  'tmñ_DSSAT':5}, 
 'cond_hídr_sat':{'límites':(
   0, np.inf), 
  'unid':'cm h-1', 
  'cód_DSSAT':'SSKS', 
  'tmñ_DSSAT':5}, 
 'densidad_suelo':{'límites':(
   0, np.inf), 
  'unid':'g cm-3', 
  'cód_DSSAT':'SBDM', 
  'tmñ_DSSAT':5}, 
 'C_org':{'límites':(0, 100), 
  'unid':None, 
  'cód_DSSAT':'SLOC', 
  'tmñ_DSSAT':5}, 
 'frac_arcill':{'límites':(0, 100), 
  'unid':None, 
  'cód_DSSAT':'SLCL', 
  'tmñ_DSSAT':5}, 
 'frac_lim':{'límites':(0, 100), 
  'unid':None, 
  'cód_DSSAT':'SLSI', 
  'tmñ_DSSAT':5}, 
 'frac_rocas':{'límites':(0, 100), 
  'unid':None, 
  'cód_DSSAT':'SLCF', 
  'tmñ_DSSAT':5}, 
 'N_total':{'límites':(0, 100), 
  'unid':None, 
  'cód_DSSAT':'SLNI', 
  'tmñ_DSSAT':5}, 
 'pH_agua':{'límites':(
   -np.inf, np.inf), 
  'unid':None, 
  'cód_DSSAT':'SLHW', 
  'tmñ_DSSAT':5}, 
 'pH_tamp':{'límites':(
   -np.inf, np.inf), 
  'unid':None, 
  'cód_DSSAT':'SLHB', 
  'tmñ_DSSAT':5}, 
 'poten_intercamb_cat':{'límites':(
   0, np.inf), 
  'unid':'cmol kg-1', 
  'cód_DSSAT':'SCEC', 
  'tmñ_DSSAT':5}}
ecs_cult = {'Día_corto_crít':{'límites':(
   0, np.inf), 
  'unid':'horas', 
  'cultivos':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                    'cód':'CSDL', 
                                    'unid':'horas'}}}}}, 
 'Pend_desarroll_fotoper':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'PPSEN', 
                                   'unid':'1/hora'}}}}, 
 'Tiempo_emerg_flor':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'EM-FL', 
                                   'unid':'días'}}}}, 
 'Tiempo_flor_fruta':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'FL-SH', 
                                   'unid':'días'}}}}, 
 'Tiempo_flor_sem':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'FL-SD', 
                                   'unid':'días'}}}}, 
 'Tiempo_sem_matur':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SD-PM', 
                                   'unid':'días'}}}}, 
 'Tiempo_flor_finhoja':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'FL-LF', 
                                   'unid':'días'}}}}, 
 'Foto_máx':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'LFMAX', 
                                   'unid':'mg CO2/(m2*s)'}}}}, 
 'Superfi_spec_hoja':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SLAVR', 
                                   'unid':'cm2/g'}}}}, 
 'Tamañ_hoja_máx':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SIZLF', 
                                   'unid':'cm2'}}}}, 
 'Máx_crec_semfrut':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'XFRT', 
                                   'unid':'días'}}}}, 
 'Peso_sem_máx':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'WTPSD', 
                                   'unid':'g'}}}}, 
 'Tiempo_llenar_sem':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SFDUR', 
                                   'unid':'días'}}}}, 
 'Sem_por_frut':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SDPDV', 
                                   'unid':'semillas'}}}}, 
 'Tiempo_llen_sem_opt':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'PODUR', 
                                   'unid':'días'}}}}, 
 'Ratio_sem_frut':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'THRSH', 
                                   'unid':None}}}}, 
 'Frac_prot_sem':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SDPRO', 
                                   'unid':None}}}}, 
 'Frac_aceit_sem':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'variedad', 
                                   'cód':'SDLIP', 
                                   'unid':None}}}}, 
 'Grupo_matur':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'MG', 
                                   'unid':''}}}}, 
 'Indic_adapt_temp':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'TM', 
                                   'unid':''}}}}, 
 'Taza_rep_min':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'THVAR', 
                                   'unid':''}}}}, 
 'Tiempo_siembr_emer':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'PL-EM', 
                                   'unid':'días'}}}}, 
 'Tiempo_emer_hoja':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'EM-V1', 
                                   'unid':'días'}}}}, 
 'Tiempo_hoja_finjuv':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'V1-JU', 
                                   'unid':'días'}}}}, 
 'Tiempo_inducflor':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'JU-R0', 
                                   'unid':'días'}}}}, 
 'Prop_tiemp_flor_frut':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'PM06', 
                                   'unid':''}}}}, 
 'Prop_tiemp_sem_mat':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'PM09', 
                                   'unid':''}}}}, 
 'Tiemp_frut':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'LNGSH', 
                                   'unid':'días'}}}}, 
 'Tiemp_matfis_matcos':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'R7-R8', 
                                   'unid':'días'}}}}, 
 'Tiemp_flor_hoja':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'FL-VS', 
                                   'unid':'días'}}}}, 
 'Taza_aparenc_hoja':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'TRIFL', 
                                   'unid':'días'}}}}, 
 'Anch_rel_ecotipo':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'RWDTH', 
                                   'unid':''}}}}, 
 'Altura_rel_ecotipo':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'RHGHT', 
                                   'unid':''}}}}, 
 'Aumen_sensit_día':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'R1PPO', 
                                   'unid':'h'}}}}, 
 'Temp_min_flor':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'OPTBI', 
                                   'unid':'C'}}}}, 
 'Pend_desarroll_flor':{'tomate': {'DSSAT': {'CROPGRO': {'tipo':'ecotipo', 
                                   'cód':'SLOBI', 
                                   'unid':''}}}}}

def gen_ec_inic--- This code section failed: ---

 L. 920         0  LOAD_FAST                'd'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 921         8  BUILD_MAP_0           0 
               10  STORE_FAST               'd'
             12_0  COME_FROM             6  '6'

 L. 924        12  SETUP_LOOP          210  'to 210'
               14  LOAD_FAST                'd_ecs'
               16  LOAD_ATTR                items
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  GET_ITER         
               22  FOR_ITER            208  'to 208'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'll'
               28  STORE_FAST               'v'

 L. 926        30  LOAD_GLOBAL              type
               32  LOAD_FAST                'v'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_GLOBAL              dict
               38  COMPARE_OP               is
               40  POP_JUMP_IF_FALSE    22  'to 22'

 L. 928        42  BUILD_MAP_0           0 
               44  LOAD_FAST                'd'
               46  LOAD_FAST                'll'
               48  STORE_SUBSCR     

 L. 930        50  LOAD_STR                 'límites'
               52  LOAD_FAST                'v'
               54  COMPARE_OP               in
               56  POP_JUMP_IF_FALSE   186  'to 186'

 L. 935        58  LOAD_STR                 'inter'
               60  LOAD_FAST                'v'
               62  LOAD_ATTR                keys
               64  CALL_FUNCTION_0       0  '0 positional arguments'
               66  COMPARE_OP               not-in
               68  POP_JUMP_IF_TRUE     82  'to 82'
               70  LOAD_FAST                'v'
               72  LOAD_STR                 'inter'
               74  BINARY_SUBSCR    
               76  LOAD_CONST               None
               78  COMPARE_OP               is
             80_0  COME_FROM            68  '68'
               80  POP_JUMP_IF_FALSE   106  'to 106'

 L. 937        82  LOAD_GLOBAL              Incert
               84  LOAD_ATTR                límites_a_texto_dist
               86  LOAD_FAST                'v'
               88  LOAD_STR                 'límites'
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  LOAD_FAST                'd'
               96  LOAD_FAST                'll'
               98  BINARY_SUBSCR    
              100  LOAD_STR                 '0'
              102  STORE_SUBSCR     
              104  JUMP_ABSOLUTE       204  'to 204'
              106  ELSE                     '184'

 L. 941       106  BUILD_MAP_0           0 
              108  LOAD_FAST                'd'
              110  LOAD_FAST                'll'
              112  STORE_SUBSCR     

 L. 943       114  LOAD_FAST                'inter'
              116  LOAD_CONST               None
              118  COMPARE_OP               is-not
              120  POP_JUMP_IF_FALSE   204  'to 204'

 L. 945       122  SETUP_LOOP          184  'to 184'
              124  LOAD_FAST                'inter'
              126  LOAD_FAST                'v'
              128  LOAD_STR                 'inter'
              130  BINARY_SUBSCR    
              132  BINARY_SUBSCR    
              134  GET_ITER         
              136  FOR_ITER            180  'to 180'
              138  STORE_FAST               'i'

 L. 947       140  BUILD_MAP_0           0 
              142  LOAD_FAST                'd'
              144  LOAD_FAST                'll'
              146  BINARY_SUBSCR    
              148  LOAD_FAST                'i'
              150  STORE_SUBSCR     

 L. 950       152  LOAD_GLOBAL              Incert
              154  LOAD_ATTR                límites_a_texto_dist
              156  LOAD_FAST                'v'
              158  LOAD_STR                 'límites'
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  LOAD_FAST                'd'
              166  LOAD_FAST                'll'
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'i'
              172  BINARY_SUBSCR    
              174  LOAD_STR                 '0'
              176  STORE_SUBSCR     
              178  JUMP_BACK           136  'to 136'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP      122  '122'
              182  JUMP_ABSOLUTE       204  'to 204'

 L. 953       184  JUMP_ABSOLUTE       206  'to 206'
              186  ELSE                     '204'

 L. 958       186  LOAD_GLOBAL              gen_ec_inic
              188  LOAD_FAST                'v'
              190  LOAD_FAST                'inter'
              192  LOAD_FAST                'd'
              194  LOAD_FAST                'll'
              196  BINARY_SUBSCR    
              198  LOAD_CONST               ('d_ecs', 'inter', 'd')
              200  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              202  POP_TOP          
              204  CONTINUE             22  'to 22'

 L. 962       206  JUMP_BACK            22  'to 22'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP       12  '12'

 L. 965       210  LOAD_FAST                'd'
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 184
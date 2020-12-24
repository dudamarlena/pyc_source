# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\RAE\RedAE.py
# Compiled at: 2017-11-13 15:40:29
# Size of source mod 2**32: 132796 bytes
import math as mat, os
from copy import deepcopy as copiar
from warnings import warn as avisar
import numpy as np
from ..Coso import Simulable, dic_a_lista
from ..Matemáticas import Distribuciones as Ds, Ecuaciones as Ec, Arte
from ..Matemáticas.Incert import validar_matr_pred
from . import Insecto as Ins
from .Gen_organismos import generar_org
from .Organismo import Organismo
from datetime import datetime as ft

class Red(Simulable):
    __doc__ = '\n    Una Red representa una red agroecológica. Trae varios `Organismos` juntos para interactuar. Aquí se implementan\n    los cálculos de todas las ecuaciones controlando las dinámicas de poblaciones de los organismos, tanto como las\n    interacciones entre ellos. Una red tiene la propiedad interesante de poder tomar datos iniciales para varias\n    parcelas al mismo tiempo y de simular las dinámicas de cada parcela simultáneamente por el uso de matrices.\n    Esto permite el empleo de un único objeto de red para modelizar las dinámicas de poblaciones en una cantidad\n    ilimitada de parcelas al mismo tiempo. Esto también facilita mucho el cálculo del movimiento de organismos entre\n    varias parcelas.\n    '
    ext = '.red'
    dic_info_ecs = None

    def __init__(símismo, nombre, proyecto, organismos=None):
        """
        :param nombre: El nombre de la red.
        :type nombre: str

        :param organismos: Una lista de objetos o nombres de organismos para añadir a la red, o una instancia única
        de un tal objeto.
        :type organismos: list[Organismo]

        """
        super().__init__(nombre=nombre, proyecto=proyecto)
        símismo.receta['estr']['Organismos'] = {}
        símismo.organismos = {}
        símismo.etapas = []
        símismo.núms_etapas = {}
        símismo.dists = {'Trans':{},  'Repr':{}}
        símismo.ecs = {}
        símismo.orden = {}
        símismo.índices_cohortes = []
        símismo.fantasmas = {}
        símismo.parasitoides = {'índices':(),  'adultos':{},  'juvs':{}}
        símismo.predics = {'Pobs':np.array([]), 
         'Depredación':np.array([]), 
         'Crecimiento':np.array([]), 
         'Reproducción':np.array([]), 
         'Muertes':np.array([]), 
         'Transiciones':np.array([]), 
         'Movimiento':np.array([]), 
         'Cohortes':{},  'Matrices':{}}
        símismo.info_exps = {'etps_interés':{},  'combin_etps':{},  'combin_etps_obs':{},  'parcelas':{},  'superficies':{},  'egrs':{}}
        símismo.l_egresos = [
         'Pobs', 'Crecimiento', 'Reproducción', 'Transiciones', 'Muertes']
        if type(organismos) is not list:
            organismos = [
             organismos]
        if organismos is not None:
            for org in organismos:
                símismo.añadir_org(org)

    def añadir_org(símismo, organismo):
        """
        Esta función añade un organismo a la red.

        :param organismo: El organismo que hay que añadir a la red
        :type organismo: Organismo | str
        """
        if isinstance(organismo, Organismo):
            nombre = organismo.nombre
            obj_org = organismo
        else:
            raise TypeError('"{}" debe ser de tipo Organismo o de texto.'.format(organismo))
        dic_org = símismo.receta['estr']['Organismos'][nombre] = {}
        dic_org['config'] = organismo.config
        dic_org['proyecto'] = organismo.proyecto
        dic_org['ext'] = organismo.ext
        símismo.organismos[nombre] = obj_org
        símismo.objetos.append(obj_org)
        símismo.listo = False

    def quitar_org(símismo, organismo):
        """
        Esta función quita un organismo de la Red.

        :param organismo: El organismo para quitar
        :type organismo: Organismo or str
        """
        if isinstance(organismo, Organismo):
            obj_org = organismo
            nombre = organismo.nombre
        elif isinstance(organismo, str):
            nombre = organismo
            try:
                obj_org = símismo.organismos[organismo]
            except KeyError:
                raise KeyError('El organismo especificado no existía en esta red.')

        else:
            raise TypeError
        try:
            símismo.receta['estr']['Organismos'].pop(nombre)
            símismo.organismos.pop(nombre)
        except KeyError:
            raise KeyError('El organismo especificado no existía en esta red.')

        símismo.objetos.remove(obj_org)
        símismo.listo = False

    def actualizar(símismo):
        """
        Actualiza la lista de etapas y las matrices de coeficientes de la red y de sus objetos.

        """
        for nombre, dic_org in símismo.receta['estr']['Organismos'].items():
            if nombre not in símismo.organismos:
                archivo_org = os.path.join(dic_org['proyecto'], nombre + dic_org['ext'])
                archivo_org_prep = símismo._prep_directorio(directorio=archivo_org)
                if os.path.isfile(archivo_org_prep):
                    símismo.organismos[nombre] = generar_org(archivo_org_prep)
                else:
                    raise ValueError('No se encontró el organismo "{}" donde lo esperábamos: \n\t{}'.format(nombre, archivo_org_prep))
                símismo.organismos[nombre].config = dic_org['config']

        for org in símismo.organismos:
            if org not in símismo.receta['estr']['Organismos']:
                símismo.organismos.pop(org)

        símismo.etapas.clear()
        símismo.fantasmas.clear()
        símismo.núms_etapas.clear()
        símismo.parasitoides['adultos'].clear()
        símismo.parasitoides['juvs'].clear()
        n = 0
        for nombre_org, org in sorted(símismo.organismos.items()):
            símismo.núms_etapas[nombre_org] = {}
            for etp in org.etapas:
                nombre_etp = etp['nombre']
                dic_etp = dict(org=nombre_org, nombre=nombre_etp,
                  dic=etp,
                  conf=(org.config[nombre_etp]),
                  coefs=(org.receta['coefs'][nombre_etp]))
                símismo.etapas.append(dic_etp)
                símismo.núms_etapas[nombre_org][nombre_etp] = n
                n += 1

        for n_etp, etp in enumerate(símismo.etapas):
            dic_hués = etp['conf']['huésped']
            if len(dic_hués):
                obj_org_inf = símismo.organismos[etp['org']]
                d_info_parás = símismo.parasitoides['adultos'][n_etp] = {'n_fants':[],  'n_vícs':[],  'n_entra':[]}
                n_juv = símismo.núms_etapas[obj_org_inf.nombre]['juvenil']
                símismo.parasitoides['juvs'][n_juv] = n_etp
                for org_hués, d_org_hués in dic_hués.items():
                    obj_org_hués = símismo.organismos[org_hués]
                    n_prim = min([símismo.núms_etapas[org_hués][x] for x in d_org_hués['entra']])
                    n_sale = símismo.núms_etapas[org_hués][d_org_hués['sale']]
                    d_info_parás['n_entra'] = [símismo.núms_etapas[org_hués][x] for x in d_org_hués['entra']]
                    n_rel_prim = símismo.etapas[n_prim]['dic']['posición']
                    n_rel_sale = símismo.etapas[n_sale]['dic']['posición']
                    l_d_etps_hués = [x for x in símismo.organismos[org_hués].etapas[n_rel_prim:n_rel_sale + 1]]
                    nombre_etp_larva_inf = obj_org_inf.etapas[0]['nombre']
                    n_larva = símismo.núms_etapas[obj_org_inf.nombre][nombre_etp_larva_inf]
                    for d_etp_hués in l_d_etps_hués:
                        n_etp_hués = d_etp_hués['posición']
                        n_etp_fant = len(símismo.etapas)
                        d_info_parás['n_fants'].append(n_etp_fant)
                        d_info_parás['n_vícs'].append(n_etp_hués)
                        nombre_etp_hués = d_etp_hués['nombre']
                        dic_estr = {'nombre':'Infectando a %s_%s' % (org_hués, nombre_etp_hués), 
                         'posición':0, 
                         'ecs':copiar(obj_org_hués.receta['estr'][nombre_etp_hués]['ecs'])}
                        conf = obj_org_hués.config[nombre_etp_hués]
                        coefs = copiar_dic_coefs(obj_org_hués.receta['coefs'][nombre_etp_hués])
                        if n_etp_hués <= len(l_d_etps_hués) - 1:
                            nombre_etp_inf_0 = obj_org_inf.etapas[0]['nombre']
                            n_etp_inf_0 = símismo.núms_etapas[obj_org_inf.nombre][nombre_etp_inf_0]
                            n_trans = n_etp_fant + 1 - n_etp_inf_0
                        else:
                            n_trans = 1
                            prob_trans = símismo.etapas[n_larva]['dic']['ecs']['Transiciones']['Prob']
                            ec_edad = símismo.etapas[n_larva]['dic']['ecs']['Edad']['Ecuación']
                            mult_trans = símismo.etapas[n_larva]['dic']['ecs']['Transiciones']['Mult']
                            coefs_prob_trans = símismo.etapas[n_larva]['coefs']['Transiciones']['Prob'][prob_trans]
                            coefs_edad = símismo.etapas[n_larva]['coefs']['Edad']['Ecuación'][ec_edad]
                            coefs_mult_trans = símismo.etapas[n_larva]['coefs']['Transiciones']['Mult'][mult_trans]
                            dic_estr['ecs']['Transiciones']['Prob'] = prob_trans
                            dic_estr['ecs']['Edad']['Ecuación'] = ec_edad
                            dic_estr['ecs']['Transiciones']['Mult'] = mult_trans
                            coefs['Transiciones']['Prob'][prob_trans] = coefs_prob_trans
                            coefs['Edad']['Ecuación'][ec_edad] = coefs_edad
                            coefs['Transiciones']['Mult'][mult_trans] = coefs_mult_trans
                        dic_estr['trans'] = n_trans
                        dic_etp = dict(org=(etp['org']), nombre=(dic_estr['nombre']),
                          dic=dic_estr,
                          conf=conf,
                          coefs=coefs)
                        símismo.etapas.append(dic_etp)
                        símismo.núms_etapas[etp['org']][dic_estr['nombre']] = n_etp_fant
                        n_etp_hués_abs = símismo.núms_etapas[org_hués][nombre_etp_hués]
                        if n_etp_hués_abs not in símismo.fantasmas.keys():
                            símismo.fantasmas[n_etp_hués_abs] = {}
                        símismo.fantasmas[n_etp_hués_abs][etp['org']] = n_etp_fant

        índs_parás = [p for n_p, d_p in símismo.parasitoides['adultos'].items() for p in [n_p] * len(d_p['n_entra'])]
        índs_víc = [v for d in símismo.parasitoides['adultos'].values() for v in d['n_entra']]
        símismo.parasitoides['índices'] = (índs_parás, índs_víc)
        símismo.ecs.clear()
        for categ in Ec.ecs_orgs:
            símismo.ecs[categ] = {}
            for sub_categ in Ec.ecs_orgs[categ]:
                símismo.ecs[categ][sub_categ] = {}
                for tipo_ec in Ec.ecs_orgs[categ][sub_categ]:
                    if tipo_ec != 'Nada':
                        índs_etps = [n for n, d in enumerate(símismo.etapas) if d['dic']['ecs'][categ][sub_categ] == tipo_ec]
                        if len(índs_etps):
                            símismo.ecs[categ][sub_categ][tipo_ec] = índs_etps

        for org in símismo.organismos.values():
            if isinstance(org, Ins.Parasitoide):
                n_etp = símismo.núms_etapas[org.nombre]['juvenil']
                dic_estr = símismo.etapas[n_etp]['dic']['ecs']['Transiciones']
                dic_edad = símismo.etapas[n_etp]['dic']['ecs']['Edad']
                tipo_ed = dic_edad['Ecuación']
                tipo_mult = dic_estr['Mult']
                tipo_prob = dic_estr['Prob']
                if tipo_prob != 'Nada':
                    símismo.ecs['Transiciones']['Mult'][tipo_mult].remove(n_etp)
                    símismo.ecs['Transiciones']['Prob'][tipo_prob].remove(n_etp)
                if tipo_ed != 'Nada':
                    símismo.ecs['Edad']['Ecuación'][tipo_ed].remove(n_etp)

        for n_etp, d_etp in enumerate(símismo.etapas):
            if not len(d_etp['conf']['presa']) and not len(d_etp['conf']['huésped']):
                tipo_depred = símismo.etapas[n_etp]['dic']['ecs']['Depredación']['Ecuación']
                if tipo_depred != 'Nada':
                    símismo.ecs['Depredación']['Ecuación'][tipo_depred].remove(n_etp)

        símismo.orden['trans'] = np.full((len(símismo.etapas)), (-1), dtype=(np.int))
        símismo.orden['repr'] = np.full((len(símismo.etapas)), (-1), dtype=(np.int))
        for nombre_org, org in símismo.núms_etapas.items():
            n_etp_mín = min(org.values())
            for etp, n_etp in org.items():
                d_etp = símismo.etapas[n_etp]['dic']
                if d_etp['ecs']['Transiciones']['Prob'] != 'Nada':
                    símismo.orden['trans'][n_etp] = d_etp['trans'] + n_etp_mín if d_etp['trans'] != -1 else -1
                if d_etp['ecs']['Reproducción']['Prob'] != 'Nada':
                    símismo.orden['repr'][n_etp] = d_etp['repr'] + n_etp_mín if d_etp['repr'] != -1 else -1

        í_cohs = símismo.índices_cohortes
        í_cohs.clear()
        for n_etp, etp in enumerate(símismo.etapas):
            req_cohs = any([n_etp in l_etps for l_etps in símismo.ecs['Edad']['Ecuación'].values()])
            if req_cohs:
                í_cohs.append(n_etp)

        símismo._actualizar_vínculos_exps()
        símismo.listo = True

    def dibujar(símismo, mostrar=True, directorio=None, exper=None, n_líneas=0, incert='componentes'):
        """
        Ver la documentación de `Simulable`.

        :type mostrar: bool
        :type directorio: str
        :type n_líneas: int
        :type exper: list[str]

        :param incert: El tipo de incertidumbre que querremos incluir en el gráfico.
        :type incert: str

        """
        if exper is None:
            exper = list(símismo.predics_exps.keys())
        if type(exper) is str:
            exper = [
             exper]
        l_m_preds = símismo.dic_simul['l_m_preds_todas']
        l_ubic_m_preds = símismo.dic_simul['l_ubics_m_preds']
        l_m_obs = símismo.dic_simul['l_m_obs_todas']
        for i, m in enumerate(l_m_preds):
            n_parc = m.shape[0]
            n_etp = len(símismo.etapas)
            ubic = l_ubic_m_preds[i]
            exp = ubic[0]
            egr = ubic[1]
            if exp not in exper:
                pass
            else:
                dir_img = (os.path.join)(directorio, *ubic)
                for i_parc in range(n_parc):
                    prc = símismo.info_exps['parcelas'][exp][i_parc]
                    for i_etp, d_etp in enumerate(símismo.etapas):
                        etp = d_etp['nombre']
                        org = d_etp['org']
                        if len(m.shape) == 5:
                            try:
                                if l_m_obs[i] is None:
                                    vec_obs = None
                                else:
                                    vec_obs = l_m_obs[i][i_parc, i_etp, :]
                            except IndexError:
                                vec_obs = None

                            matr_pred = m[i_parc, :, :, i_etp, :]
                            if egr == 'Transiciones':
                                op = 'Recip- '
                            else:
                                if egr == 'Reproducción':
                                    op = 'Desde- '
                                else:
                                    op = ''
                                if n_parc > 1:
                                    título = 'Parcela "{prc}", {op}"{org}", etapa "{etp}"'.format(prc=prc,
                                      op=op,
                                      org=org,
                                      etp=etp)
                                else:
                                    título = '{op}{org}, etapa "{etp}"'.format(op=op, org=org, etp=etp)
                            Arte.graficar_pred(matr_predic=matr_pred, vector_obs=vec_obs, título=título,
                              etiq_y=egr,
                              n_líneas=n_líneas,
                              incert=incert,
                              mostrar=mostrar,
                              directorio=dir_img)
                        else:
                            presas = [símismo.núms_etapas[o][e] for o, d_e in símismo.etapas[n_etp]['conf']['presa'].items() for e in d_e]
                            huéspedes = [símismo.núms_etapas[o][e] for o, d_e in símismo.etapas[n_etp]['conf']['huésped'].items() for e in d_e['entra']]
                            víctimas = presas + huéspedes
                            for n_etp_víc in víctimas:
                                etp_víc = símismo.etapas[n_etp_víc]['nombre']
                                org_víc = símismo.etapas[n_etp_víc]['org']
                                matr_pred = m[n_parc, ..., n_etp, n_etp_víc, :]
                                if n_parc > 1:
                                    título = 'Parcela "{prc}", {org}, etapa "{etp}" atacando a "{org_víc}", etapa "{etp_víc}"'.format(prc=prc,
                                      org=org,
                                      etp=etp,
                                      org_víc=org_víc,
                                      etp_víc=etp_víc)
                                else:
                                    título = '{org}, etapa "{etp}" atacando a "{org_víc}", etapa "{etp_víc}"'.format(org=org,
                                      etp=etp,
                                      org_víc=org_víc,
                                      etp_víc=etp_víc)
                                Arte.graficar_pred(matr_predic=matr_pred, título=título,
                                  etiq_y='Depredación',
                                  n_líneas=n_líneas,
                                  incert=incert,
                                  mostrar=mostrar,
                                  directorio=dir_img)

    def _calc_depred(símismo, pobs, depred, extrn, paso):
        """
        Calcula la depredación entre los varios organismos de la red. Aquí se implementan todas las ecuaciones
        de depredación posibles; el programa escoje la ecuación apropiada para cada depredador.
        El libro "A primer of Ecology" es una buena referencia a las ecuaciones incluidas aquí, tanto como
        Abrams PA, Ginzburg LR. 2000. The nature of predation: prey dependent, ratio dependent or neither?
            Trends Ecol Evol 15(8):337-341.

        Respuestas funcionales (y = consumo de presa por cápita de depredador, D = población del depredador,
        P = población de la presa; a, b y c son constantes):

            Tipo I:
                y = a*P
                Generalmente no recomendable. Incluido aquí por puro interés científico.

            Tipo II:
                y = a*P / (P + b)

            Tipo III:
                y = a*P^2 / (P^2 + b)

            Dependencia en la presa quiere decir que el modelo está dependiente de la población de la presa únicamente
            (como los ejemplos arriba). Ecuaciones dependientes en el ratio se calculan de manera similar, pero
            reemplazando P con (P/D) en las ecuaciones arriba.

            Beddington-DeAngelis:
                J.R. Beddington. Mutual interference between parasites and its effect on searching efficiency. J.
                    Anim. Ecol., 44 (1975), pp. 331–340
                D.L. DeAngelis, et al. A model for trophic interaction Ecology, 56 (1975), pp. 881–892

                Usamos una forma matemáticamente equivalente a la en el artículo, y que facilita el establecimiento de
                  distribuciones a prioris para los parámetros:
                y = a*P / (b + P + c*D)

            Hassell-Varley:
                M.P. Hassell, G.C. Varley. New inductive population model for insect parasites and its bearing on
                    biological control. Nature, 223 (1969), pp. 1133–1136

                P en las respuestas funcionales arriba cambia a P/(D^m)

            Kovai (Asíntota doble):
                y = a*(1 - e^(-u/(a*D))); u = P + e^(-P/b) - b

                  a es el máximo de consumo de presa por depredador (cuando las presas son abundantes y los
                    depredadores no compiten entre sí mismos)

                  b es la densidad de presas a la cuál, donde hay suficientemente pocos depredadores para causar
                    competition entre ellos, los depredadores consumirán a/e presas por depredador.

        :param pobs: matriz numpy de poblaciones actuales.
        :type pobs: np.ndarray

        :param extrn: Un diccionario con datos externos
        :type extrn: dict

        :param paso: El paso de tiempo de la simulación.
        :type paso: int

        """
        tipos_ec = símismo.ecs['Depredación']['Ecuación']
        if not len(tipos_ec):
            return
        coefs = símismo.coefs_act_númzds['Depredación']['Ecuación']
        dens = np.divide(pobs, extrn['superficies'].reshape(pobs.shape[0], 1, 1, 1))[..., np.newaxis, :]
        for tp_ec, í_etps in tipos_ec.items():
            cf = coefs[tp_ec]
            depred_etp = np.take(depred, í_etps, axis=3)
            if tp_ec == 'Tipo I_Dependiente presa':
                np.multiply(pobs, (cf['a']), out=depred_etp)
            else:
                if tp_ec == 'Tipo II_Dependiente presa':
                    np.multiply(dens, (cf['a'] / (dens + cf['b'])), out=depred_etp)
                else:
                    if tp_ec == 'Tipo III_Dependiente presa':
                        np.multiply((np.square(dens)), (cf['a'] / (np.square(dens) + cf['b'])), out=depred_etp)
                    else:
                        if tp_ec == 'Tipo I_Dependiente ratio':
                            dens_depred = dens[:, :, :, í_etps]
                            np.multiply((dens / dens_depred), (cf['a']), out=depred_etp)
                        else:
                            if tp_ec == 'Tipo II_Dependiente ratio':
                                dens_depred = dens[:, :, :, í_etps]
                                np.multiply((dens / dens_depred), (cf['a'] / (dens / dens_depred + cf['b'])), out=depred_etp)
                            else:
                                if tp_ec == 'Tipo III_Dependiente ratio':
                                    dens_depred = dens[:, :, :, í_etps]
                                    np.multiply((np.square(dens / dens_depred)), (cf['a'] / (np.square(dens / dens_depred) + cf['b'])), out=depred_etp)
                                else:
                                    if tp_ec == 'Beddington-DeAngelis':
                                        dens_depred = dens[:, :, :, í_etps]
                                        np.multiply(dens, (cf['a'] / (cf['b'] + dens + cf['c'] * dens_depred)), out=depred_etp)
                                    else:
                                        if tp_ec == 'Tipo I_Hassell-Varley':
                                            dens_depred = dens[:, :, :, í_etps]
                                            np.multiply((dens / dens_depred ** cf['m']), (cf['a']), out=depred_etp)
                                        else:
                                            if tp_ec == 'Tipo II_Hassell-Varley':
                                                dens_depred = dens[:, :, :, í_etps]
                                                np.multiply((dens / dens_depred ** cf['m']), (cf['a'] / (dens / dens_depred ** cf['m'] + cf['b'])), out=depred_etp)
                                            else:
                                                if tp_ec == 'Tipo III_Hassell-Varley':
                                                    dens_depred = dens[:, :, :, í_etps]
                                                    np.multiply((dens / dens_depred ** cf['m']), (cf['a'] / (dens / dens_depred ** cf['m'] + cf['b'])), out=depred_etp)
                                                else:
                                                    if tp_ec == 'Kovai':
                                                        dens_depred = dens[:, :, :, 0, í_etps, np.newaxis]
                                                        presa_efec = np.add(dens, np.multiply(cf['b'], np.subtract(np.exp(np.divide(-dens, cf['b'])), 1)))
                                                        ratio = presa_efec / dens_depred
                                                        np.multiply((cf['a']), (np.subtract(1, np.exp(np.divide(-np.where(ratio == np.inf, [0], ratio), cf['a'])))),
                                                          out=depred_etp)
                                                        probs_conj(depred_etp, pesos=(cf['a']), máx=1, eje=4)
                                                    else:
                                                        raise ValueError('Tipo de ecuación "%s" no reconodico para cálculos de depradación.' % tp_ec)
            depred[:, :, :, í_etps, :] = depred_etp

        depred[np.isnan(depred)] = 0
        np.multiply(depred, (extrn['superficies'].reshape(depred.shape[0], 1, 1, 1, 1)), out=depred)
        np.multiply(depred, (np.multiply(pobs, paso)[(..., np.newaxis)]), out=depred)
        probs_conj(depred, pesos=1, máx=pobs, eje=3)
        depred[np.isnan(depred)] = 0
        np.floor(depred, out=depred)
        depred_por_presa = np.sum(depred, axis=3)
        np.subtract(pobs, depred_por_presa, out=pobs)
        depred_infec = np.zeros_like(depred)
        índs_parás, índs_víc = símismo.parasitoides['índices']
        depred_infec[(..., índs_parás, índs_víc)] = depred[(..., índs_parás, índs_víc)]
        depred_por_presa_sin_infec = np.subtract(depred_por_presa, np.sum(depred_infec, axis=3))
        símismo._quitar_de_cohortes(muertes=(depred_por_presa_sin_infec[(..., símismo.índices_cohortes)]))
        for n_parás, d_parás in símismo.parasitoides['adultos'].items():
            índ_entra = d_parás['n_entra']
            índ_recip = d_parás['n_fants'][:len(índ_entra)]
            símismo._quitar_de_cohortes(muertes=(depred_infec[(..., n_parás, símismo.índices_cohortes)]), í_don=índ_entra,
              í_recip=índ_recip)
            pobs[(..., índ_recip)] += depred_infec[(..., n_parás, índ_entra)]

    def _calc_crec(símismo, pobs, crec, extrn, paso):
        """
        Calcula las reproducciones y las transiciones de etapas de crecimiento

        :param pobs: Matriz numpy de poblaciones actuales. Eje 0 =
        :type pobs: np.ndarray

        :param extrn: Diccionario de factores externos a la red (plantas, clima, etc.)
        :type extrn: dict

        :param paso: El paso para la simulación.
        :type paso: int

        """
        tipos_ec = símismo.ecs['Crecimiento']['Ecuación']
        modifs = símismo.ecs['Crecimiento']['Modif']
        if not len(tipos_ec):
            return
        coefs_ec = símismo.coefs_act_númzds['Crecimiento']['Ecuación']
        coefs_mod = símismo.coefs_act_númzds['Crecimiento']['Modif']
        for mod, í_etps in modifs.items():
            r = np.take(crec, í_etps, axis=3)
            cf = coefs_mod[mod]
            if mod == 'Ninguna':
                np.multiply((cf['r']), paso, out=r)
            else:
                if mod == 'Log Normal Temperatura':
                    np.multiply((cf['r'] * paso), (mat.exp(-0.5 * (mat.log(extrn['temp_máx'] / cf['t']) / cf['p']) ** 2)), out=r)
                else:
                    raise ValueError
            crec[:, :, :, í_etps] = r

        for tp_ec, í_etps in tipos_ec.items():
            crec_etp = np.take(crec, í_etps, axis=3)
            pobs_etps = pobs[:, :, :, í_etps]
            cf = coefs_ec[tp_ec]
            if tp_ec == 'Exponencial':
                np.multiply(pobs_etps, crec_etp, out=crec_etp)
            else:
                if tp_ec == 'Logístico':
                    np.multiply(crec_etp, (pobs_etps * (1 - pobs_etps / cf['K'])), out=crec_etp)
                else:
                    if tp_ec == 'Logístico Presa':
                        k = np.nansum((np.multiply(pobs, cf['K'])), axis=3)
                        np.multiply(crec_etp, (pobs_etps * (1 - pobs_etps / k)), out=crec_etp)
                        np.maximum(crec_etp, (-pobs_etps), out=crec_etp)
                    else:
                        if tp_ec == 'Logístico Depredación':
                            depred = símismo.predics['Depred'][..., í_etps, :]
                            k = np.nansum((np.multiply(depred, cf['K'])), axis=3)
                            np.multiply(crec_etp, (pobs_etps * (1 - pobs_etps / k)), out=crec_etp)
                            np.maximum(crec_etp, (-pobs_etps), out=crec_etp)
                        else:
                            if tp_ec == 'Constante':
                                nueva_pob = cf['n']
                                np.subtract(nueva_pob, pobs_etps, out=crec_etp)
                            elif tp_ec == 'Externo Cultivo':
                                try:
                                    np.subtract((extrn['Plantas']), pobs_etps, out=crec_etp)
                                except (KeyError, TypeError):
                                    pass

                            else:
                                raise ValueError('Ecuación de crecimiento "%s" no reconocida.' % tp_ec)
            crec[:, :, :, í_etps] = crec_etp

        crec[np.isnan(crec)] = 0
        np.floor(crec)
        np.add(pobs, crec, out=pobs)

    def _calc_edad(símismo, extrn, edades, paso):
        """

        :param extrn:
        :type extrn:
        :param paso:
        :type paso:

        """
        edad_extra = edades
        tipos_edad = símismo.ecs['Edad']['Ecuación']
        coefs_ed = símismo.coefs_act_númzds['Edad']['Ecuación']
        for tp_ed, í_etps in tipos_edad.items():
            cf_ed = coefs_ed[tp_ed]
            if tp_ed == 'Días':
                edad_extra[(..., í_etps)] = 1
            elif tp_ed == 'Días Grados':
                edad_extra[(..., í_etps)] = días_grados((extrn['temp_máx']), (extrn['temp_mín']), umbrales=(
                 cf_ed['mín'], cf_ed['máx']))
            elif tp_ed == 'Brière Temperatura':
                edad_extra[(..., í_etps)] = extrn['temp_prom'] * (extrn['temp_prom'] - cf_ed['t_dev_mín']) * mat.sqrt(cf_ed['t_letal'] - extrn['temp_prom'])
            else:
                if tp_ed == 'Brière No Linear Temperatura':
                    edad_extra[(..., í_etps)] = extrn['temp_prom'] * (extrn['temp_prom'] - cf_ed['t_dev_mín']) * mat.pow(cf_ed['t_letal'] - extrn['temp_prom'], 1 / cf_ed['m'])
                else:
                    if tp_ed == 'Logan Temperatura':
                        edad_extra[(..., í_etps)] = mat.exp(cf_ed['rho'] * extrn['temp_prom']) - mat.exp(cf_ed['rho'] * cf_ed['t_letal'] - (cf_ed['t_letal'] - extrn['temp_prom']) / cf_ed['delta'])
                    else:
                        raise ValueError('No reconozco el tipo de ecuación "%s" para la edad.' % tp_ed)

        np.multiply(edad_extra, paso, out=edad_extra)

    def _calc_reprod(símismo, pobs, paso, reprod, depred):
        """
        Esta función calcula las reproducciones de las etapas.

        :param pobs: La matriz de poblaciones actuales de la red. Ejes tales como indicado arriba.
        :type pobs: np.ndarray

        :param paso: El paso para la simulación.
        :type paso: int

        """
        tipos_probs = símismo.ecs['Reproducción']['Prob']
        coefs_pr = símismo.coefs_act_númzds['Reproducción']['Prob']
        for tp_prob, í_etps in tipos_probs.items():
            cf = coefs_pr[tp_prob]
            pob_etp = np.take(pobs, í_etps, axis=3)
            n_recip = [símismo.orden['repr'][n] for n in í_etps]
            repr_etp_recip = np.take(reprod, í_etps, axis=3)
            if tp_prob == 'Constante':
                np.multiply((cf['a']), (pob_etp * paso), out=repr_etp_recip)
            else:
                if tp_prob == 'Depredación':
                    np.sum((np.multiply(cf['n'], depred[..., í_etps, :])), axis=(-1), out=repr_etp_recip)
                else:
                    edad_extra = símismo.predics['Edades']
                    símismo._trans_cohortes(cambio_edad=(edad_extra[(..., í_etps)]), etps=í_etps, dists=(símismo.dists['Repr'][tp_prob]),
                      matr_egr=repr_etp_recip,
                      quitar=False)
                    np.multiply((cf['n']), repr_etp_recip, out=repr_etp_recip)
            reprod[(..., n_recip)] = repr_etp_recip

        np.round(reprod, out=reprod)
        np.add(pobs, reprod, out=pobs)
        if len(símismo.índices_cohortes):
            símismo._añadir_a_cohortes(nuevos=(reprod[(..., símismo.índices_cohortes)]))

    def _calc_muertes(símismo, pobs, muertes, extrn, paso):
        """
        Esta función calcula las muertes de causas ambientales de la etapa.

        :param extrn: Un diccionario con las condiciones exógenas a la red
        :type extrn: dict

        :param pobs: La matriz de poblaciones actuales de la red. Ejes tales como indicado arriba.
        :type pobs: np.ndarray

        :param paso: El paso para la simulación.
        :type paso: int

        """
        tipos_ec = símismo.ecs['Muertes']['Ecuación']
        if not len(tipos_ec):
            return
        coefs = símismo.coefs_act_númzds['Muertes']['Ecuación']
        for tp_ec, í_etps in tipos_ec.items():
            cf = coefs[tp_ec]
            muerte_etp = np.take(muertes, í_etps, axis=3)
            pob_etp = np.take(pobs, í_etps, axis=3)
            if tp_ec == 'Constante':
                np.multiply(pob_etp, (cf['q']), out=muerte_etp)
            else:
                if tp_ec == 'Log Normal Temperatura':
                    sobrevivencia = mat.exp(-0.5 * (mat.log(extrn['temp_máx'] / cf['t']) / cf['p']) ** 2)
                    np.multiply(pob_etp, (1 - sobrevivencia), out=muerte_etp)
                else:
                    if tp_ec == 'Asimptótico Humedad':
                        sobrevivencia = np.maximum([0], np.subtract(1, mat.exp(-cf['a'] * (extrn['humedad'] - cf['b']))))
                        np.multiply(pob_etp, (1 - sobrevivencia), out=muerte_etp)
                    else:
                        if tp_ec == 'Sigmoidal Temperatura':
                            sobrevivencia = 1 / (1 + mat.exp((extrn['temp_máx'] - cf['a']) / cf['b']))
                            np.multiply(pob_etp, (1 - sobrevivencia), out=muerte_etp)
                        else:
                            raise ValueError
            muertes[:, :, :, í_etps] = muerte_etp

        np.multiply(muertes, paso, out=muertes)
        np.round(muertes, out=muertes)
        if len(símismo.índices_cohortes):
            símismo._quitar_de_cohortes(muertes[(..., símismo.índices_cohortes)])
        np.subtract(pobs, muertes, out=pobs)

    def _calc_trans(símismo, pobs, paso, trans):
        """
        Esta función calcula las transiciones de organismos de una etapa a otra. Esto puede incluir muerte por
        viejez.

        :param pobs:
        :type pobs: np.ndarray

        :param paso:
        :type paso: int

        :param trans:
        :type trans:

        """
        tipos_probs = símismo.ecs['Transiciones']['Prob']
        tipos_mult = símismo.ecs['Transiciones']['Mult']
        coefs_pr = símismo.coefs_act_númzds['Transiciones']['Prob']
        coefs_mt = símismo.coefs_act_númzds['Transiciones']['Mult']
        for tp_prob, í_etps in tipos_probs.items():
            cf = coefs_pr[tp_prob]
            trans_etp = np.take(trans, í_etps, axis=3)
            if tp_prob == 'Constante':
                np.multiply(pobs, (1 - (1 - cf['q']) ** paso), out=trans_etp)
            else:
                edad_extra = símismo.predics['Edades']
                símismo._trans_cohortes(cambio_edad=(edad_extra[(..., í_etps)]), etps=í_etps, dists=(símismo.dists['Trans'][tp_prob]),
                  matr_egr=trans_etp)
            trans[(..., í_etps)] = trans_etp

        np.floor(trans, out=trans)
        np.subtract(pobs, trans, out=pobs)
        orden_recip = símismo.orden['trans']
        nuevos = np.zeros_like(trans)
        for tp_mult, í_etps in tipos_mult.items():
            if tp_mult == 'Linear':
                trans[(..., í_etps)] *= coefs_mt[tp_mult]['a']
                np.floor(trans)
            else:
                raise ValueError('Tipo de multiplicación "{}" no reconocida.'.format(tp_mult))

        for i in range(len(símismo.etapas)):
            i_recip = orden_recip[i]
            if i_recip != -1:
                nuevos[(..., i_recip)] += trans[(..., i)]

        np.add(pobs, nuevos, out=pobs)
        if len(símismo.índices_cohortes):
            símismo._añadir_a_cohortes(nuevos=(nuevos[(..., símismo.índices_cohortes)]))

    def _calc_mov(símismo, pobs, paso, extrn):
        """
        Calcula la imigración y emigración de organismos entre parcelas

        :param pobs:
        :type pobs: np.narray

        :param paso:
        :type paso: int

        :param extrn:
        :type extrn: dict

        """
        mov = símismo.predics['Movimiento']
        tipos_ec = símismo.ecs['Movimiento']
        coefs = símismo.coefs_act_númzds['Movimiento']
        for ec in tipos_ec:
            mobil = NotImplemented
            modif_peso = NotImplemented
            superficie = NotImplemented
            peso = superficie * modif_peso
            mov = NotImplemented

        edades = NotImplemented
        símismo._añadir_a_cohortes(nuevos=mov, edad=edades)
        pobs += mov

    def _calc_ruido(símismo, pobs, paso):
        """

        :param pobs:
        :type pobs: np.ndarray
        :param paso:
        :type paso: int
        """
        ruido = np.empty(pobs.shape)
        tipos_ruido = símismo.ecs['Error']['Dist']
        coefs_ruido = símismo.coefs_act_númzds['Error']['Dist']
        for tp_ruido, í_etps in tipos_ruido.items():
            cf_ruido = coefs_ruido[tp_ruido]
            if tp_ruido == 'Normal':
                ruido[(..., í_etps)] = cf_ruido['sigma'] * paso
            else:
                raise ValueError

        np.multiply(pobs, ruido, out=ruido)
        np.maximum(1, ruido, out=ruido)
        np.round((np.random.normal(0, ruido)), out=ruido)
        ruido = np.where(-ruido > pobs, -pobs, ruido)
        np.add(ruido, pobs, out=pobs)
        símismo._ajustar_cohortes(cambio=(ruido[(..., símismo.índices_cohortes)]))

    def _inic_pobs_const(símismo):
        dic = símismo.ecs['Crecimiento']['Ecuación']
        if 'Constante' in dic.keys():
            for n_etp in range(len(símismo.etapas)):
                if n_etp in dic['Constante']:
                    í_etp = dic['Constante'].index(n_etp)
                    pobs_inic = símismo.coefs_act_númzds['Crecimiento']['Ecuación']['Constante']['n'][:, í_etp]
                    símismo.predics['Pobs'][(..., n_etp, 0)] = pobs_inic

    def incrementar(símismo, paso, i, detalles, mov=False, extrn=None):
        símismo.predics['Pobs'][(..., i)] = símismo.predics['Pobs'][(..., i - 1)]
        pobs = símismo.predics['Pobs'][(..., i)]
        if detalles:
            depred = símismo.predics['Depredación'][(..., i)]
            crec = símismo.predics['Crecimiento'][(..., i)]
            muertes = símismo.predics['Muertes'][(..., i)]
            trans = símismo.predics['Transiciones'][(..., i)]
            reprod = símismo.predics['Reproducción'][(..., i)]
        else:
            depred = símismo.predics['Depredación']
            crec = símismo.predics['Crecimiento']
            muertes = símismo.predics['Muertes']
            trans = símismo.predics['Transiciones']
            reprod = símismo.predics['Reproducción']
        edades = símismo.predics['Edades']
        antes_0 = ft.now()
        símismo._calc_depred(pobs=pobs, paso=paso, depred=depred, extrn=extrn)
        t_depred = ft.now() - antes_0
        antes = ft.now()
        símismo._calc_crec(pobs=pobs, extrn=extrn, crec=crec, paso=paso)
        t_crec = ft.now() - antes
        antes = ft.now()
        símismo._calc_muertes(pobs=pobs, muertes=muertes, extrn=extrn, paso=paso)
        t_muertes = ft.now() - antes
        antes = ft.now()
        símismo._calc_edad(extrn=extrn, paso=paso, edades=edades)
        t_edad = ft.now() - antes
        antes = ft.now()
        símismo._calc_trans(pobs=pobs, paso=paso, trans=trans)
        t_trans = ft.now() - antes
        antes = ft.now()
        símismo._calc_reprod(pobs=pobs, paso=paso, reprod=reprod, depred=depred)
        t_reprod = ft.now() - antes
        if mov:
            símismo._calc_mov(pobs=pobs, extrn=extrn, paso=paso)
        antes = ft.now()
        símismo._calc_ruido(pobs=pobs, paso=paso)
        fin = ft.now()
        t_ruido = fin - antes_0

    def _procesar_simul(símismo):
        """
        Ver la documentación de `Simulable`.
        """
        for exp, predic in símismo.dic_simul['d_predics_exps'].items():
            tamaño_superficies = símismo.info_exps['superficies'][exp]
            for egr in símismo.info_exps['egrs'][exp]:
                np.divide((predic[egr]), tamaño_superficies, out=(predic[egr]))
                for i, fants in símismo.fantasmas.items():
                    índ_fants = list(fants.values())
                    predic[egr][..., i, :] += np.sum((predic[egr][..., índ_fants, :]), axis=(-2))

                for ad, dic in símismo.parasitoides['adultos'].items():
                    índ_fants = dic['n_fants']
                    d_juvs = símismo.parasitoides['juvs']
                    índ_juv = next(x for x in d_juvs if d_juvs[x] == ad)
                    predic[egr][..., índ_juv, :] += np.sum((predic[egr][..., índ_fants, :]), axis=(-2))

                try:
                    combin_etps = símismo.info_exps['combin_etps'][exp][egr]
                    for i in combin_etps:
                        predic[egr][..., i, :] += np.sum((predic[egr][..., combin_etps[i], :]), axis=(-2))

                except KeyError:
                    pass

    def _analizar_valid(símismo):
        """
        Ver documentación de Simulable.
        Esta función valida las predicciones de una corrida de validación.

        :return: Un diccionario, organizado por experimento, organismo y etapa, del ajuste del modelo.
        :rtype: dict

        """
        matr_preds_total = None
        vector_obs_total = None
        valids_detalles = {}
        d_obs_valid = símismo.dic_simul['d_obs_valid']
        d_matrs_valid = símismo.dic_simul['matrs_valid']
        n_etps = len(símismo.etapas)
        for exp, d_obs_exp in d_obs_valid.items():
            valids_detalles[exp] = {}
            for egr, matr in d_obs_exp.items():
                n_parc = d_obs_exp[egr].shape[0]
                for n_p in range(n_parc):
                    parc = símismo.info_exps['parcelas'][exp][n_p]
                    for n_etp in range(n_etps):
                        vec_obs = matr[n_p, n_etp, :]
                        if np.sum(~np.isnan(vec_obs)) == 0:
                            continue
                        matr_preds = d_matrs_valid[exp][egr][n_p, ..., n_etp, :]
                        org = símismo.etapas[n_etp]['org']
                        etp = símismo.etapas[n_etp]['nombre']
                        if org not in valids_detalles[exp]:
                            valids_detalles[exp][org] = {}
                        valids_detalles[exp][org][etp] = {}
                        valids_detalles[exp][org][etp][parc] = validar_matr_pred(matr_predic=matr_preds,
                          vector_obs=vec_obs)
                        if matr_preds_total is None:
                            matr_preds_total = matr_preds
                            vector_obs_total = vec_obs
                        else:
                            matr_preds_total = np.append(matr_preds_total, matr_preds, axis=(-1))
                            vector_obs_total = np.append(vector_obs_total, vec_obs, axis=(-1))

        valid = validar_matr_pred(matr_predic=matr_preds_total, vector_obs=vector_obs_total)
        return {'Valid':valid, 
         'Valid detallades':valids_detalles}

    def _procesar_matrs_sens(símismo):
        """
        Ver la documentación de `Coso`.
        :return:
        :rtype: (list[np.ndarray], list[list[str]])
        """
        l_matrs_pred = símismo.dic_simul['l_m_preds_todas']
        l_ubics_m_preds = símismo.dic_simul['l_ubics_m_preds']
        l_preds_proc = []
        l_ubics_preds_proc = []
        for m, u in zip(l_matrs_pred, l_ubics_m_preds):
            n_parc = m.shape[0]
            for i_prc in range(n_parc):
                exp = u[0]
                prc = símismo.info_exps['parcelas'][exp][i_prc]
                for i_etp, d_etp in enumerate(símismo.etapas):
                    etp = d_etp['nombre']
                    org = d_etp['org']
                    if len(m.shape) == 5:
                        matr_pred = m[i_prc, :, :, i_etp, :]
                        mu = np.mean(matr_pred, axis=0)
                        sigma = np.std(matr_pred, axis=0)
                        ubic_mu = u + [prc, org, etp, mu]
                        ubic_sigma = u + [prc, org, etp, sigma]
                        l_preds_proc += mu
                        l_ubics_preds_proc += ubic_mu
                        l_preds_proc += sigma
                        l_ubics_preds_proc += ubic_sigma
                    else:
                        presas = [símismo.núms_etapas[o][e] for o, d_e in símismo.etapas[i_etp]['conf']['presa'].items() for e in d_e]
                        huéspedes = [símismo.núms_etapas[o][e] for o, d_e in símismo.etapas[i_etp]['conf']['huésped'].items() for e in d_e['entra']]
                        víctimas = presas + huéspedes
                        for i_etp_víc in víctimas:
                            etp_víc = símismo.etapas[i_etp_víc]['nombre']
                            org_víc = símismo.etapas[i_etp_víc]['org']
                            matr_pred = m[prc, ..., i_etp, i_etp_víc, :]
                            mu = np.mean(matr_pred, axis=0)
                            sigma = np.std(matr_pred, axis=0)
                            ubic_mu = u + [prc, org, etp, org_víc, etp_víc, mu]
                            ubic_sigma = u + [prc, org, etp, org_víc, etp_víc, sigma]
                            l_preds_proc += mu
                            l_ubics_preds_proc += ubic_mu
                            l_preds_proc += sigma
                            l_ubics_preds_proc += ubic_sigma

        return (
         l_preds_proc, l_ubics_preds_proc)

    def _sacar_líms_coefs_interno(símismo):
        """
        No hay nada nada que hacer aquí, visto que una red no tiene coeficientes propios. Devolvemos
        una lista vacía.
        """
        return []

    def _sacar_coefs_interno(símismo):
        """
        No hay nada nada que hacer, visto que una Red no tiene coeficientes propios.
        """
        return ([], [])

    def añadir_exp(símismo, experimento, corresp=None, corresp_pobs=None, corresp_crec=None, corresp_repr=None, corresp_trans=None, corresp_muertes=None):
        """
        Esta función permite conectar un Experimento con una Red, especificando diccionarios de correspondencia para
        cada tipo de egreso posible. No es necesario especificar todas las correspondencias, sino únicamente las
        que aplican a este Experimento. Si todos los tipos de egresos tienen los mismos nombres de columnas en el
        Experimento, se puede usar el parámetro general `corresp` para aplicar las mismas correspondencias a todos.

        :param experimento:
        :type experimento: Experimento

        :param corresp: El valor automático para correspondencias.
        :type corresp: dict

        :param corresp_pobs: Correspondencias para observaciones de población.
        :type corresp_pobs: dict

        :param corresp_crec: Correspondencias para observaciones de crecimiento.
        :type corresp_crec: dict

        :param corresp_repr: Correspondencias para observaciones de reproducción.
        :type corresp_repr: dict

        :param corresp_trans: Correspondencias para observaciones de transiciones.
        :type corresp_trans: dict

        :param corresp_muertes: Correspondencias para observaciones de muertes.
        :type corresp_muertes: dict
        """
        corresp_mod = {}
        conv_corresps = {'Pobs':corresp_pobs, 
         'Crecimiento':corresp_crec,  'Reproducción':corresp_repr,  'Transiciones':corresp_trans, 
         'Muertes':corresp_muertes}
        for ll, cor in conv_corresps.items():
            if cor is not None:
                corresp_mod[ll] = cor
            else:
                if corresp is not None:
                    corresp_mod[ll] = corresp

        if all(x is None for x in corresp_mod.values()):
            raise ValueError('Hay que especificar al menos un diccionario de correspondencia para conectarun Experimento a la Red.')
        super().añadir_exp(experimento=experimento, corresp=corresp_mod)

    def _actualizar_vínculos_exps(símismo):
        """
        Ver la documentación de Simulable.

        Esta función llenará el diccionario símismo.info_exps, lo cuál contiene la información necesaria para
          conectar las predicciones de una Red con los datos observados en un Experimento. Este diccionario tiene
          cuatro partes:
            2. 'etps_interés': Una lista de los números de las etapas en la Red que corresponden
            3. 'combin_etps': Un diccionario de las etapas cuyas predicciones hay que combinar. Tiene la forma
                general {n_etp: [n otras etapas], n_etp2: [], etc.},
                donde las llaves del diccionario son números enteros, no texto.
            4. 'ubic_obs': Un formato tuple con matrices con la información de dónde hay que sacar los datos de
                observaciones para cada día y cada etapa. Para hacer: cada parcela.

        """
        for categ_info in símismo.info_exps.values():
            categ_info.clear()

        for exp, d in símismo.exps.items():
            obj_exp = d['Exp']
            d_corresp = d['Corresp'].copy()
            etps_interés = símismo.info_exps['etps_interés'][exp] = {}
            combin_etps = símismo.info_exps['combin_etps'][exp] = {}
            combin_etps_obs = símismo.info_exps['combin_etps_obs'][exp] = {}
            egrs = símismo.info_exps['egrs'][exp] = []
            parc = símismo.info_exps['parcelas'][exp] = obj_exp.obt_parcelas(tipo=(símismo.ext))
            símismo.info_exps['superficies'][exp] = obj_exp.superficies(parc)
            for egr in símismo.l_egresos:
                if obj_exp.obt_datos_rae(egr) is not None:
                    egrs.append(egr)

            for egr, corresp in d_corresp.items():
                if egr not in egrs:
                    pass
                else:
                    etps_interés_egr = etps_interés[egr] = {}
                    combin_etps_egr = combin_etps[egr] = {}
                    combin_etps_obs_egr = combin_etps_obs[egr] = {}
                    nombres_cols = obj_exp.obt_datos_rae(egr)['cols']
                    for org in corresp:
                        d_org = corresp[org]
                        if org not in símismo.receta['estr']['Organismos']:
                            avisar('El organismo "{}" no existe en la red "{}". Se excluirá del experimento "{}".'.format(org, símismo.nombre, exp))
                            corresp.pop(org)
                        for etp in list(d_org):
                            if etp not in símismo.núms_etapas[org]:
                                avisar('Organismo "{}" no tiene etapa "{}". Se excluirá del experimento "{}".'.format(org, etp, exp))
                                d_org.pop(etp)

                    l_cols_cum = []
                    l_etps_cum = []
                    for org, d_org in corresp.items():
                        for etp, d_etp in d_org.items():
                            l_cols = d_etp
                            if type(l_cols) is not list:
                                l_cols = [
                                 l_cols]
                            l_cols.sort()
                            n_etp = símismo.núms_etapas[org][etp]
                            if len(l_cols) > 1:
                                combin_etps_obs_egr[n_etp] = [nombres_cols.index(c) for c in l_cols]
                            if l_cols in l_cols_cum:
                                n_otra_etp = l_etps_cum[l_cols_cum.index(l_cols)]
                                if n_otra_etp not in combin_etps_egr:
                                    combin_etps_egr[n_otra_etp] = []
                                combin_etps_egr[n_otra_etp].append(n_etp)
                            else:
                                l_cols_cum.append(l_cols)
                                l_etps_cum.append(n_etp)
                                etps_interés_egr[n_etp] = nombres_cols.index(l_cols[0])

    def _gen_dic_predics_exps(símismo, exper, n_rep_estoc, n_rep_parám, paso, n_pasos, detalles):
        """

        :return:
        :rtype: dict
        """
        d_predics_exps = símismo.dic_simul['d_predics_exps']
        n_etps = len(símismo.etapas)
        n_cohs = len(símismo.índices_cohortes)
        for exp in exper:
            try:
                obj_exp = símismo.exps[exp]['Exp']
            except KeyError:
                raise ValueError('El experimento "{}" no está vinculado con esta Red.'.format(exp))

            n_parc = len(obj_exp.obt_parcelas(tipo=(símismo.ext)))
            n_pasos_exp = n_pasos[exp]
            dic_predics = símismo._gen_dic_matr_predic(n_parc=n_parc,
              n_rep_estoc=n_rep_estoc,
              n_rep_parám=n_rep_parám,
              n_etps=n_etps,
              n_pasos=n_pasos_exp,
              n_cohs=n_cohs,
              detalles=detalles)
            l_pobs_inic = [
             None] * len(símismo.etapas)
            combin_etps = símismo.info_exps['combin_etps'][exp]['Pobs']
            for n_etp, i in símismo.info_exps['etps_interés'][exp]['Pobs'].items():
                matr_obs_inic = obj_exp.obt_datos_rae('Pobs', por_parcela=True)['datos'][:, i, 0]
                combin_etps_obs = símismo.info_exps['combin_etps_obs'][exp]
                if n_etp in combin_etps_obs:
                    for col_otra in combin_etps_obs[n_etp]:
                        datos_otra = obj_exp.obt_datos_rae('Pobs', por_parcela=True)['datos'][:, col_otra, 0]
                        np.sum(matr_obs_inic, datos_otra, out=matr_obs_inic)

                if n_etp not in combin_etps:
                    l_pobs_inic[n_etp] = matr_obs_inic
                else:
                    etps_compart = [
                     n_etp] + combin_etps[n_etp]
                    div = np.floor(np.divide(matr_obs_inic, len(etps_compart)))
                    resto = np.remainder(matr_obs_inic, len(etps_compart))
                    for j, n in enumerate(etps_compart):
                        l_pobs_inic[n] = np.add(div, np.less(j, resto))

            for n_etp, i in símismo.info_exps['etps_interés'][exp]['Pobs'].items():
                matr_obs_inic = l_pobs_inic[n_etp]
                org = símismo.organismos[símismo.etapas[n_etp]['org']]
                etp = símismo.etapas[n_etp]['nombre']
                juvenil_paras = isinstance(org, Ins.Parasitoide) and etp == 'juvenil'
                if not juvenil_paras:
                    dic_predics['Pobs'][(..., n_etp, 0)] = matr_obs_inic[:, np.newaxis, np.newaxis]
                else:
                    l_etps_víc = [víc for víc, d in símismo.fantasmas.items() if org.nombre in d]
                    n_etps_víc = len(l_etps_víc)
                    l_etps_fant = [d[org.nombre] for d in símismo.fantasmas.values() if org.nombre in d]
                    l_pobs_víc = np.array([l_pobs_inic[j] for j in l_etps_víc])
                    pobs_total_etps_víc = np.sum(l_pobs_víc, axis=0)
                    if np.sum(matr_obs_inic > pobs_total_etps_víc):
                        raise ValueError('Tenemos una complicacioncita con los datos inicales para el experimento"{}".\nNo es posible tener más poblaciones iniciales de juveniles de parasitoides que hay\nindivíduos de etapas potencialmente hospederas.\n¿No estás de acuerdo?')
                    matr_pobs_etps_fant = np.zeros((n_etps_víc, *matr_obs_inic.shape), dtype=int)
                    copia_matr = matr_obs_inic.copy()
                    matr_pobs_etps_fant_cum = np.cumsum((l_pobs_víc[::-1]), axis=0)[::-1]
                    for v in range(n_etps_víc):
                        p = np.divide(copia_matr, matr_pobs_etps_fant_cum[v])
                        aloc = np.minimum(np.random.binomial(l_pobs_víc[v], p), copia_matr)
                        if v < n_etps_víc - 1:
                            aloc = np.maximum(aloc, copia_matr - matr_pobs_etps_fant_cum[(v + 1)])
                        else:
                            aloc = np.maximum(aloc, copia_matr)
                        matr_pobs_etps_fant[v] += aloc
                        copia_matr -= aloc

                    for n_etp_víc, n_etp_fant, pobs in zip(l_etps_víc, l_etps_fant, matr_pobs_etps_fant):
                        dic_predics['Pobs'][(..., n_etp_fant, 0)] += pobs
                        dic_predics['Pobs'][(..., n_etp_víc, 0)] -= pobs

            símismo._añadir_a_cohortes(dic_predic=dic_predics, nuevos=(dic_predics['Pobs'][(..., símismo.índices_cohortes, 0)]))
            d_predics_exps[exp] = dic_predics

        if detalles:
            d_preds = {x:{e:d_x[e] for e in símismo.l_egresos} for x, d_x in d_predics_exps.items()}
        else:
            d_preds = {x:{'Pobs': d_x['Pobs']} for x, d_x in d_predics_exps.items()}
        l_preds = símismo.dic_simul['l_m_preds_todas']
        dic_a_lista(d=d_preds, l=l_preds, l_u=(símismo.dic_simul['l_ubics_m_preds']))

    def _gen_dics_valid(símismo, exper, paso, n_pasos, n_rep_estoc, n_rep_parám):
        d_obs = símismo.dic_simul['d_obs_valid']
        d_valid = símismo.dic_simul['matrs_valid']
        d_preds_v = {}
        d_índs = {}
        for exp in exper:
            obj_exp = símismo.exps[exp]['Exp']
            nombres_parc = obj_exp.obt_parcelas(tipo=(símismo.ext))
            n_parc = len(nombres_parc)
            for egr in símismo.l_egresos:
                if egr in símismo.info_exps['egrs'][exp]:
                    for d in [d_obs, d_valid, d_preds_v, d_índs]:
                        if exp not in d:
                            d[exp] = {}

                    datos = obj_exp.obt_datos_rae(egr, por_parcela=False)
                    días = datos['días']
                    n_días = len(días)
                    n_etps = len(símismo.etapas)
                    d_obs[exp][egr] = matr_obs = np.empty((n_parc, n_etps, n_días))
                    matr_obs[:] = np.nan
                    parc = [nombres_parc.index(x) for x in datos['parc']]
                    etps = list(símismo.info_exps['etps_interés'][exp][egr].keys())
                    etps_bd = list(símismo.info_exps['etps_interés'][exp][egr].values())
                    vals = datos['datos'][:, etps_bd, :]
                    matr_obs[parc, etps, :] = vals
                    for e, l_c in símismo.info_exps['combin_etps_obs'][exp][egr].items():
                        vals = datos['datos'][:, l_c, :]
                        matr_obs[:, e, :] += np.sum(vals, axis=1)

                    d_preds_v[exp][egr] = símismo.dic_simul['d_predics_exps'][exp][egr]
                    d_valid[exp][egr] = np.empty((n_parc, n_rep_estoc, n_rep_parám, n_etps, n_días))
                    días_ex = [d for d in días if d % paso == 0]
                    días_inter = [d for d in días if d % paso != 0]
                    í_p_ex = [d // paso for d in días_ex]
                    í_v_ex = [np.where(días == d)[0][0] for d in días_ex]
                    í_v_ínt = [i for i in range(n_días) if i not in í_v_ex]
                    í_p_ínt_0 = [mat.floor(d / paso) for d in días_inter]
                    í_p_ínt_1 = [mat.ceil(d / paso) for d in días_inter]
                    pesos = [d % paso / paso for d in días_inter]
                    índs = {'exactos':(
                      í_v_ex, í_p_ex), 
                     'interpol':(
                      í_v_ínt, í_p_ínt_0, í_p_ínt_1, pesos)}
                    d_índs[exp][egr] = índs

        símismo.dic_simul['d_l_m_valid'] = {'Normal': dic_a_lista(d_valid)}
        símismo.dic_simul['d_l_m_predics_v'] = {'Normal': dic_a_lista(d_preds_v)}
        símismo.dic_simul['d_l_í_valid'] = {'Normal': dic_a_lista(d_índs, ll_f='exactos')}
        l_m_preds_v = dic_a_lista(d_preds_v)
        l_m_obs_v = dic_a_lista(d_obs)
        l_m_preds_todas = símismo.dic_simul['l_m_preds_todas']

        def temp(m, l):
            try:
                return l.index(m)
            except ValueError:
                return

        l_m_obs_todas = [l_m_obs_v[temp(m, l_m_preds_v)] if temp(m, l_m_preds_v) is not None else None for í, m in enumerate(l_m_preds_todas)]
        símismo.dic_simul['l_m_obs_todas'].extend(l_m_obs_todas)

    def _gen_dics_calib(símismo, exper):
        l_obs_v = dic_a_lista(símismo.dic_simul['d_obs_valid'])
        d_obs_c = símismo.dic_simul['d_obs_calib']
        d_índs_calib = símismo.dic_simul['d_l_í_calib']
        d_índs_calib['Normal'] = []
        n_obs_cumul = 0
        for m in l_obs_v:
            válidos = ~np.isnan(m)
            n_obs = np.sum(válidos)
            parc, etps, días = np.where(válidos)
            d_info = {'índs':(
              parc, etps, días), 
             'rango':[n_obs_cumul, n_obs_cumul + n_obs]}
            d_índs_calib['Normal'].append(d_info)
            n_obs_cumul += n_obs

        símismo.dic_simul['d_calib']['Normal'] = {'mu':np.empty(n_obs_cumul), 
         'sigma':np.empty(n_obs_cumul)}
        d_obs_c['Normal'] = np.empty(n_obs_cumul)
        for i, m in enumerate(l_obs_v):
            parc, etps, días = d_índs_calib['Normal'][i]['índs']
            r = d_índs_calib['Normal'][i]['rango']
            d_obs_c['Normal'][r[0]:r[1]] = m[(parc, etps, días)]

    def _llenar_coefs(símismo, nombre_simul, n_rep_parám, calibs=None, dib_dists=False):
        """
        Ver la documentación de Coso.

        :type n_rep_parám: int
        :type calibs: list | str
        :type dib_dists: bool
        :type calibs: list

        """
        if calibs is None:
            calibs = []
        n_etapas = len(símismo.etapas)
        símismo.coefs_act.clear()
        for categ, dic_categ in Ec.ecs_orgs.items():
            símismo.coefs_act[categ] = {}
            for subcateg in dic_categ:
                símismo.coefs_act[categ][subcateg] = {}
                for tipo_ec, índs_etps in símismo.ecs[categ][subcateg].items():
                    coefs_act = símismo.coefs_act[categ][subcateg][tipo_ec] = {}
                    for parám, d_parám in Ec.ecs_orgs[categ][subcateg][tipo_ec].items():
                        if d_parám['inter'] is None:
                            tamaño_matr = (n_rep_parám, len(índs_etps))
                        else:
                            tamaño_matr = (n_rep_parám, len(índs_etps), n_etapas)
                        coefs_act[parám] = np.empty(tamaño_matr, dtype=object)
                        coefs_act[parám][:] = np.nan
                        for i, n_etp in enumerate(índs_etps):
                            matr_etp = coefs_act[parám][:, i, ...]
                            d_parám_etp = símismo.etapas[n_etp]['coefs'][categ][subcateg][tipo_ec][parám]
                            if d_parám['inter'] is None:
                                matr_etp[:] = d_parám_etp[nombre_simul]
                                if dib_dists:
                                    directorio_dib = os.path.join(símismo.proyecto, símismo.nombre, nombre_simul, 'Gráficos simulación', 'Dists', categ, subcateg, tipo_ec, parám)
                                    directorio_dib = símismo._prep_directorio(directorio=directorio_dib)
                                    título = símismo.etapas[n_etp]['org'] + ', ' + símismo.etapas[n_etp]['nombre']
                                    Arte.graficar_dists(dists=[d for x, d in d_parám_etp.items() if x in calibs if type(d) is str],
                                      valores=matr_etp,
                                      título=título,
                                      archivo=directorio_dib)
                            else:
                                for tipo_inter in d_parám['inter']:
                                    if tipo_inter == 'presa' or tipo_inter == 'huésped':
                                        for org_víc, v in símismo.etapas[n_etp]['conf'][tipo_inter].items():
                                            if tipo_inter == 'presa':
                                                l_etps_víc = v
                                            else:
                                                l_etps_víc = v['entra']
                                            for etp_víc in l_etps_víc:
                                                n_etp_víc = símismo.núms_etapas[org_víc][etp_víc]
                                                l_n_etps_víc = [
                                                 n_etp_víc]
                                                if n_etp_víc in símismo.fantasmas:
                                                    obj_org = símismo.organismos[símismo.etapas[n_etp]['org']]
                                                    if not isinstance(obj_org, Ins.Parasitoide):
                                                        l_n_etps_víc += list(símismo.fantasmas[n_etp_víc].values())
                                                for n in l_n_etps_víc:
                                                    matr_etp[:, n] = d_parám_etp[org_víc][etp_víc][nombre_simul]
                                                    if dib_dists:
                                                        directorio_dib = os.path.join(símismo.proyecto, símismo.nombre, nombre_simul, 'Gráficos simulación', 'Dists', categ, subcateg, tipo_ec, parám)
                                                        directorio_dib = símismo._prep_directorio(directorio=directorio_dib)
                                                        título = símismo.etapas[n_etp]['org'] + ', ' + símismo.etapas[n_etp]['nombre'] + ' _ ' + org_víc + ', ' + etp_víc
                                                        Arte.graficar_dists(dists=[d for x, d in d_parám_etp[org_víc][etp_víc].items() if x in calibs if type(d) is str],
                                                          valores=(matr_etp[:, n]),
                                                          título=título,
                                                          archivo=directorio_dib)

                                    else:
                                        raise ValueError('Interacción "%s" no reconocida.' % tipo_inter)

    def especificar_apriori(símismo, **kwargs):
        """
        Una Red no tiene parámetros para especificar.
        """
        raise NotImplementedError('No hay parámetros para especificar en una Red.')

    def _justo_antes_de_simular(símismo):
        """
        Esta función hace cosas que hay que hacer justo antes de cada simulación (en particular, cosas que tienen
        que ver con los valores de los parámetros, pero que no hay que hacer a cada paso de la simulación.

        """
        símismo._prep_dists()
        símismo._inic_pobs_const()

    def _sacar_coefs_no_espec(símismo):
        """
        Una Red no tiene coeficientes.

        """
        return {}

    def _prep_dists(símismo):
        """
        Esta función inicializa los diccionarios de distribuciones de la Red.
        """
        símismo.dists['Trans'].clear()
        símismo.dists['Repr'].clear()
        for categ, corto in zip(['Transiciones', 'Reproducción'], ['Trans', 'Repr']):
            for tp_dist, í_etps in símismo.ecs[categ]['Prob'].items():
                if tp_dist not in ('Nada', 'Constante'):
                    paráms_dist = símismo.coefs_act_númzds[categ]['Prob'][tp_dist]
                    if tp_dist == 'Normal':
                        paráms = dict(loc=(paráms_dist['mu']), scale=(paráms_dist['sigma']))
                    else:
                        if tp_dist == 'Triang':
                            paráms = dict(loc=(paráms_dist['a']), scale=(paráms_dist['b']), c=(paráms_dist['c']))
                        else:
                            if tp_dist == 'Cauchy':
                                paráms = dict(loc=(paráms_dist['u']), scale=(paráms_dist['f']))
                            else:
                                if tp_dist == 'Gamma':
                                    paráms = dict(loc=(paráms_dist['u']), scale=(paráms_dist['f']), a=(paráms_dist['a']))
                                else:
                                    if tp_dist == 'T':
                                        paráms = dict(loc=(paráms_dist['mu']), scale=(paráms_dist['sigma']), df=(paráms_dist['k']))
                                    else:
                                        raise ValueError('La distribución "{}" no tiene definición.'.format(tp_dist))
                    símismo.dists[corto][tp_dist] = (Ds.dists[tp_dist]['scipy'])(**paráms)

    def _trans_cohortes(símismo, cambio_edad, etps, dists, matr_egr, quitar=True):
        """
        Esta funcion maneja transiciones (basadas en edades) desde cohortes.

        :param cambio_edad: Una matriz multidimensional con los cambios en las edades de cada cohorte de la etapa.
        Notar que la edad puede ser 'edad' en el sentido tradicional del término, tanto como la 'edad' del organismo
        medida por otro método (por ejemplo, exposición cumulativo a días grados). Los ejes son iguales que en 'pobs'.
        :type cambio_edad: np.ndarray

        :param etps: Los índices de las etapas (en la lista de etapas de la Red) que estamos transicionando ahora.
        :type etps: list

        :param dists: Una distribución con parámetros en forma de matrices.
        :type dists: estad._distn_infrastructure.rv_frozen.

        :param matr_egr: Una matriz en la cual guardar los resultados.
        :type matr_egr: np.ndarray

        :param quitar: Si hay que quitar las etapas que transicionaron (útil para cálculos de reproducción).
        :type quitar: bool

        """
        í_etps_coh = [símismo.índices_cohortes.index(x) for x in etps]
        edades = símismo.predics['Cohortes']['Edades'][(..., í_etps_coh)]
        pobs = símismo.predics['Cohortes']['Pobs'][(..., í_etps_coh)]
        dens_cum_eds = dists.cdf(edades)
        probs = np.divide(np.subtract(dists.cdf(edades + cambio_edad), dens_cum_eds), np.subtract(1, dens_cum_eds))
        probs[np.isnan(probs)] = 1
        n_cambian = np.floor(np.multiply(pobs, probs))
        símismo.predics['Cohortes']['Edades'][(..., í_etps_coh)] += cambio_edad
        if quitar:
            símismo.predics['Cohortes']['Pobs'][(..., í_etps_coh)] -= n_cambian
        np.sum(n_cambian, axis=0, out=matr_egr)

    def _añadir_a_cohortes(símismo, nuevos, edad=0, dic_predic=None):
        """
        Esta función agrega nuevos miembros a un cohorte existente.

        :param nuevos: La matriz de poblaciones para agregar. Eje 0: Parcela, Eje 1: Repetición estocástica, Eje 2:
        Repetición paramétrica, Eje 3: Etapa.
        :type nuevos: np.ndarray

        :param edad: Las edades iniciales de los nuevos miembros al cohorte. El valor automático es, naturalmente, 0.
        (Esto se puede cambiar si estamos transicionando cohortes existentes de un otro cohorte.) Si es una
        matriz, debe tener la misma forma que `nuevos`.
        :type edad: np.ndarray

        :param dic_predic: Un diccionario opcional con la matriz de predicciones. Si cohortes es `None`, se
        utilizará la matriz de la simulación actual.
        :type dic_predic: dict
        """
        if dic_predic is None:
            dic_predic = símismo.predics
        else:
            cohortes = dic_predic['Cohortes']
            if not len(símismo.índices_cohortes):
                return
            else:
                return np.sum(nuevos) or None
        matr_pobs = cohortes['Pobs']
        matr_eds = cohortes['Edades']
        matr_eds[matr_pobs == 0] = 0
        i_cohs = np.argmin(matr_eds, axis=0).ravel()
        í_parc, í_estoc, í_parám, í_etps = dic_predic['Matrices']['í_ejes_cohs']
        tmñ = dic_predic['Matrices']['tmñ_para_cohs']
        eds_mín = matr_eds[(i_cohs, í_parc, í_estoc, í_parám, í_etps)].reshape(tmñ)
        pobs_coresp_í = matr_pobs[(i_cohs, í_parc, í_estoc, í_parám, í_etps)].reshape(tmñ)
        eds_mín = np.where(pobs_coresp_í == 0, [0], eds_mín)
        peso_ed_ya = np.divide(pobs_coresp_í, np.add(nuevos, pobs_coresp_í))
        peso_ed_ya[np.isnan(peso_ed_ya)] = 0
        eds_prom = np.add(np.multiply(eds_mín, peso_ed_ya), np.multiply(edad, np.subtract(1, peso_ed_ya)))
        matr_eds[(i_cohs, í_parc, í_estoc, í_parám, í_etps)] = eds_prom.ravel()
        matr_pobs[(i_cohs, í_parc, í_estoc, í_parám, í_etps)] += nuevos.ravel()

    def _quitar_de_cohortes(símismo, muertes, í_don=None, í_recip=None):
        """
        Esta funciôn quita individuos de los cohortes de la Red.

        :param muertes: La matriz de muertes aleatorias a quitar del cohorte. Eje 0: Parcela,
        Eje 1: Repetición estocástica, Eje 2: Repetición paramétrica, Eje 3: Etapa.
        :type muertes: np.ndarray

        :param í_don:
        :type í_don: np.ndarray

        :param í_recip:
        :type í_recip: np.ndarray

        """
        pobs = símismo.predics['Cohortes']['Pobs']
        edades = símismo.predics['Cohortes']['Edades']
        muertes = muertes.copy()
        pobs_cums = np.cumsum((pobs[::-1]), axis=0)[::-1]
        for n_día in range(pobs.shape[0]):
            if np.sum(muertes) == 0:
                return
            else:
                pobs_coh = pobs[(n_día, ...)]
                if n_día < pobs.shape[0] - 1:
                    quitar = np.floor(np.multiply(np.divide(pobs_coh, pobs_cums[n_día]), muertes))
                    quitar[np.isnan(quitar)] = 0
                    quitar = np.minimum(np.maximum(quitar, muertes - pobs_cums[(n_día + 1)]), muertes)
                    np.subtract(muertes, quitar, out=muertes)
                else:
                    quitar = muertes
            np.subtract(pobs_coh, quitar, out=pobs_coh)
            if í_recip is not None:
                if í_don is None:
                    raise ValueError
                í_recip_coh = [símismo.índices_cohortes.index(x) for x in í_recip]
                í_don_coh = [símismo.índices_cohortes.index(x) for x in í_don]
                eds = edades[(n_día, ...)]
                nuevos = np.zeros_like(quitar)
                nuevos[(..., í_recip_coh)] = quitar[(..., í_don_coh)]
                símismo._añadir_a_cohortes(nuevos=nuevos, edad=eds)

    def _ajustar_cohortes(símismo, cambio):
        """
        Esta función ajusta las poblaciones de cohortes. Es muy útil cuando no sabemos si el cambio es positivo o
        negativo.

        :param cambio: El cambio en poblaciones, en el mismo formato que la matriz de población.
        :type cambio: np.ndarray

        """
        positivos = np.where(cambio > 0, cambio, [0])
        negativos = np.where(cambio < 0, -cambio, [0])
        símismo._añadir_a_cohortes(nuevos=positivos)
        símismo._quitar_de_cohortes(muertes=negativos)

    @staticmethod
    def _gen_dic_matr_predic(n_parc, n_rep_estoc, n_rep_parám, n_etps, n_pasos, n_cohs, detalles, n_grupos_coh=10):
        """
        Esta función genera un diccionario con matrices del tamaño apropiado para guardar las predicciones del modelo.
        Por usar una función auxiliar, se facilita la generación de matrices para simulaciones de muchos experimentos.

        :param n_parc: El número de parcelas
        :type n_parc: int

        :param n_rep_estoc: El número de repeticiones estocásticas
        :type n_rep_estoc: int

        :param n_rep_parám: El número de repeticiones paramétricas
        :type n_rep_parám: int

        :param n_etps: El número de etapas de organismos en la Red.
        :type n_etps: int

        :param n_pasos: El número de pasos para la simulación
        :type n_pasos: int

        :param n_cohs: El número de etapas con cohortes para algo.
        :type n_cohs: int

        :param n_grupos_coh: El número de categorías de edad distintas en cada cohorte.
        :type n_grupos_coh: int

        :return: Un diccionario del formato de símismo.predics según las especificaciones en los argumentos de la
        función.
        :rtype: dict
        """
        if detalles:
            tamaño_normal = (
             n_parc, n_rep_estoc, n_rep_parám, n_etps, n_pasos)
            tamaño_pobs = tamaño_normal
            tamaño_depr = (n_parc, n_rep_estoc, n_rep_parám, n_etps, n_etps, n_pasos)
        else:
            tamaño_normal = (
             n_parc, n_rep_estoc, n_rep_parám, n_etps)
            tamaño_pobs = (n_parc, n_rep_estoc, n_rep_parám, n_etps, n_pasos)
            tamaño_depr = (n_parc, n_rep_estoc, n_rep_parám, n_etps, n_etps)
        tamaño_edades = (n_parc, n_rep_estoc, n_rep_parám, n_etps)
        dic = {'Pobs':np.zeros(shape=tamaño_pobs), 
         'Depredación':np.zeros(shape=tamaño_depr), 
         'Crecimiento':np.zeros(shape=tamaño_normal), 
         'Edades':np.zeros(shape=tamaño_edades), 
         'Reproducción':np.zeros(shape=tamaño_normal), 
         'Muertes':np.zeros(shape=tamaño_normal), 
         'Transiciones':np.zeros(shape=tamaño_normal), 
         'Movimiento':np.zeros(shape=tamaño_normal), 
         'Cohortes':{},  'Matrices':{'í_ejes_cohs':(),  'tmñ_para_cohs':(
           n_parc, n_rep_estoc, n_rep_parám, n_cohs)}}
        if n_cohs > 0:
            cohortes = dic['Cohortes']
            cohortes['Pobs'] = np.zeros(shape=(n_grupos_coh, n_parc, n_rep_estoc, n_rep_parám, n_cohs))
            cohortes['Edades'] = np.zeros(shape=(n_grupos_coh, n_parc, n_rep_estoc, n_rep_parám, n_cohs))
            í_ejes_cohs = (
             np.repeat(range(n_parc), n_rep_estoc * n_rep_parám * n_cohs),
             np.tile(np.repeat(range(n_rep_estoc), n_rep_parám * n_cohs), [n_parc]),
             np.tile(np.repeat(range(n_rep_parám), n_cohs), [n_parc * n_rep_estoc]),
             np.tile(range(n_cohs), [n_parc * n_rep_estoc * n_rep_parám]))
            dic['Matrices']['í_ejes_cohs'] = í_ejes_cohs
        return dic


def días_grados(mín, máx, umbrales, método='Triangular', corte='Horizontal'):
    """
    Esta función calcula los días grados basados en vectores de temperaturas mínimas y máximas diarias.
    Información sobre los métodos utilizados aquí se puede encontrar en:
    http://www.ipm.ucdavis.edu/WEATHER/ddconcepts.html

    :param mín:
    :type mín: float
    :param máx:
    :type máx: float
    :param umbrales:
    :type umbrales: tuple
    :param método:
    :type método: str
    :param corte:
    :type corte: str
    :return: número de días grados (número entero)
    :rtype: int
    """
    if método == 'Triangular':
        sup_arriba = max(12 * (máx - umbrales[1]) ** 2 / (máx - mín), 0) / 24
        sup_centro = max(12 * (umbrales[1] - umbrales[0]) ** 2 / (umbrales[1] - mín), 0) / 24
        sup_lados = max(24 * (máx - umbrales[1]) * umbrales[(1 - umbrales[0])] / (máx - mín), 0) / 24
    else:
        if método == 'Sinusoidal':
            amp = (máx - mín) / 2
            prom = (máx + mín) / 2
            if umbrales[1] >= máx:
                intersect_máx = 0
                sup_arriba = 0
            else:
                intersect_máx = 24 * mat.acos((umbrales[1] - prom) / amp)
                sup_arriba = 2 * (intersect_máx * (prom - máx) + 2 * mat.pi / 24 * mat.sin(2 * mat.pi / 24 * intersect_máx))
            if umbrales[0] <= mín:
                intersect_mín = intersect_máx
            else:
                intersect_mín = 24 * mat.acos((umbrales[0] - prom) / amp)
            sup_centro = 2 * intersect_máx * (máx - mín)
            sup_lados = 2 * (2 * mat.pi / 24 * mat.sin(2 * mat.pi / 24 * intersect_mín) - 2 * mat.pi / 24 * mat.sin(2 * mat.pi / 24 * intersect_máx) + (intersect_mín - intersect_máx) * (umbrales[0] - prom))
        else:
            raise ValueError
        if corte == 'Horizontal':
            días_grd = sup_centro + sup_lados
        else:
            if corte == 'Intermediario':
                días_grd = sup_centro + sup_lados - sup_arriba
            else:
                if corte == 'Vertical':
                    días_grd = sup_lados
                else:
                    if corte == 'Ninguno':
                        días_grd = sup_lados + sup_centro + sup_arriba
                    else:
                        raise ValueError
    return días_grd


def probs_conj(matr, eje, pesos=1, máx=1):
    """
    Esta función utiliza las reglas de probabilidades conjuntas para ajustar depredación con presas o depredadores
    múltiples cuya suma podría sumar más que el total de presas o la capacidad del depredador.

    :param matr: Una matriz con los valores para ajustar.
    :type matr: np.ndarray

    :param eje: El eje según cual hay que hacer los ajustes
    :type eje: int

    :param pesos: Un peso inverso opcional para aplicar a la matriz ántes de hacer los cálculos.
    :type pesos: float | int | np.ndarray

    :param máx: Una matriz o número con los valores máximos para la matriz para ajustar. Si es matriz, debe ser de
    tamaño compatible con matr.
    :type máx: float | int | np.ndarray

    """
    if not isinstance(máx, np.ndarray):
        tamaño = list(matr.shape)
        tamaño.pop(eje)
        máx = np.full(tuple(tamaño), máx)
    ajustados = np.divide(matr, pesos)
    ratio = np.divide(ajustados, np.expand_dims(máx, eje))
    np.multiply(np.expand_dims((np.divide(np.subtract(1, np.product((np.subtract(1, np.where(np.isnan(ratio), [0], ratio))),
      axis=eje)), np.nansum(ratio, axis=eje))),
      axis=eje),
      ajustados,
      out=ajustados)
    ajustados[np.isnan(ajustados)] = 0
    suma = np.sum(ajustados, axis=eje)
    extra = np.where(suma > máx, suma - máx, [0])
    np.multiply(ajustados, np.expand_dims((np.subtract(1, np.divide(extra, suma))), axis=eje), out=ajustados)
    np.multiply(ajustados, pesos, out=matr)


def copiar_dic_refs(d, c=None):
    """
    Esta función copia un diccionario pero deja las referencias a matrices y variables PyMC intactos. Esto permite
    dejar que etapas fantasmas de una víctima de parasitoide tengan los mismos variables que la etapa original y evita
    desdoblar variables en la calibración.

    :param d: El diccinario o la lista para copiar
    :type d: dict | list

    :param c: Para recursiones. No especificar al llamar la función.
    :type c: dict | list

    :return: El diccionario o la lista copiada
    :rtype: dict | list
    """
    if c is None:
        if type(d) is list:
            c = []
        elif type(d) is dict:
            c = {}
    if type(d) is list:
        for n, v in enumerate(d):
            if type(v) is dict:
                c[n] = {}
                copiar_dic_refs(v, c=(c[n]))
            else:
                if type(v) is list:
                    c[n] = []
                    copiar_dic_refs(v, c=(c[n]))
                else:
                    c[n] = v

    else:
        if type(d) is dict:
            for ll, v in d.items():
                if type(v) is dict:
                    c[ll] = {}
                    copiar_dic_refs(v, c=(c[ll]))
                else:
                    if type(v) is list:
                        c[ll] = []
                        copiar_dic_refs(v, c=(c[ll]))
                    else:
                        c[ll] = v

    return c


def copiar_dic_coefs(d, c=None):
    """
    Esta función copia un diccionario pero deja las referencias a matrices y variables PyMC intactos (no hace copia
    del último diccionario anidado, sino una referencia a este). Esto permite dejar que etapas fantasmas de una víctima
    de parasitoide tengan los mismos variables que la etapa original y evita desdoblar variables en la calibración.

    :param d: El diccionario de coeficientes para copiar.
    :type d: dict

    :param c: Para recursiones. No especificar al llamar la función.
    :type c: dict

    :return: Una copia del diccionario con referencias a los últimos diccionarios anidados.
    :rtype: dict
    """
    if c is None:
        c = {}
    for ll, v in d.items():
        if type(v) is dict:
            if any(type(x) is dict for x in v.values()):
                c[ll] = {}
                copiar_dic_coefs(v, c=(c[ll]))
            else:
                c[ll] = v
        else:
            c[ll] = v

    return c
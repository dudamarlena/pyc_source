# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\RAE\Organismo.py
# Compiled at: 2017-10-16 15:04:13
# Size of source mod 2**32: 32414 bytes
import os
from tikon.Coso import Coso
from tikon.Matemáticas import Ecuaciones as Ec
from tikon.Matemáticas.Incert import límites_a_texto_dist

class Organismo(Coso):
    __doc__ = '\n    Esta clase representa cualquier organismo vivo en una red agroecológica.: insectos, agentes de\n    enfermedad, etc. Maneja las ecuaciones y bases de datos de distribuciones probabilísticas para sus parámetros.\n\n    Esta clase se llama directamente muy rara vez, porque se llama más facilmente por el uso de una de sus subclases\n    (Insecto, Enfermedad, etc.). Hablando de subclases, puedes crear más subclases o sub-sub clases si te da las\n    ganas. Por ejemplo, hay subclases de "Insecto" para la mayoría de los ciclos de vida posibles para insectos\n    (Metamórfosis Completa, Metamórfosis Incompleta, etc.) y hacia sub-subclases de estas, si quieres.\n    Un ejemplo de algo que podrías añadir sería una sub-subclase de "Sencillo" para pulgones, o sub-clases de\n    Enfermedades para distintos tipos de enfermedades (enfermedades de insectos, enfermedades de hojas, de raíces,\n    etc.) (¡Marcela!) :)\n\n    Una cosa importante: si quieres crear una nueva subclase, sub-subclase, sub-sub-subclase (no importa), y quieres\n    que la clase tenga métodos (fundiones) propias DISTINTAS de los métodos yá implementados en Organismo aquí,\n    (por ejemplo, el método .parasita() para parasitoides), tendrás que especificar un tipo de extensión de\n    archivo único para tu clase (p.ej., \'.ins\' para Insecto) para que el módulo de Redes pueda distinguir archivos\n    guardados específicos a tu nueva clase.\n\n    '
    ext = '.org'
    dic_info_ecs = Ec.ecs_orgs

    def __init__(símismo, nombre=None, proyecto=None):
        """

        :param nombre: El nombre del organismo
        :type nombre: str
        
        :param proyecto:
        :type proyecto: str

        """
        super().__init__(nombre=nombre, proyecto=proyecto)
        símismo.etapas = []
        símismo.config = {}
        símismo.actualizar()

    def actualizar(símismo):
        """
        Esta función simplemente se asegura de que todo en el organismo esté actualizado según la configuración
        actual en la receta. Si hay cualquier atributo del organismo que depiende de valore(s) en la receta,
        aquí es el lugar par actualizarlos.

        Esta función se llama automáticamente después de funciones tales como "secome()" y "quitar_etapa()".

        """
        símismo.etapas = sorted([x for x in símismo.receta['estr'].values()], key=(lambda d: d['posición']))

    def añadir_etapa(símismo, nombre, posición, ecuaciones, lím_error=0.1):
        """
        Esta función añade una etapa al organismo.

        :param nombre: El nombre de la etapa. Por ejemplo, "huevo", "juvenil_1", "pupa", "adulto"
        :type nombre: str

        :param posición: La posición cronológica de la etapa. Por ejemplo, "huevo" tendría posición 0, etc.
        :type posición: int

        :param ecuaciones: Un diccionario con los tipos de ecuaciones para esta etapa. (Siempre se puede cambiar
        más tarde con la función usar_ecuación()). Notar que las nuevas etapas tendrán TODAS las ecuaciones posibles
        en su diccionario inicial; la especificación de ecuación aquí únicamente determina cual(es) de estas se usarán
        para la calibración, simulación, etc.
        Tiene el formato: {Categoría_1: {subcategoría_1: tipo_de_ecuacion, ...}, Categoría_2: {...}, ...}
        :type ecuaciones: dict

        """
        símismo.verificar_ecs(ecuaciones, etp=nombre)
        for etp, dic_etp in símismo.receta['estr'].items():
            if dic_etp['posición'] >= posición:
                dic_etp['posición'] += 1
            else:
                if dic_etp['trans'] >= posición:
                    dic_etp['trans'] += 1
                if dic_etp['repr'] >= posición:
                    dic_etp['repr'] += 1
            if dic_etp['posición'] == posición - 1:
                dic_etp['trans'] = posición

        dic_etapa = dict(nombre=nombre, posición=posición,
          ecs=(ecuaciones.copy()),
          trans=(-1),
          repr=0)
        símismo.receta['estr'][nombre] = dic_etapa
        símismo.receta['coefs'][nombre] = Ec.gen_ec_inic(Ec.ecs_orgs)
        símismo.config[nombre] = {'presa':{},  'huésped':{}}
        símismo.actualizar()
        if lím_error is not None:
            símismo.especificar_apriori(etapa=nombre, ubic_parám=['Error', 'Dist', 'Normal', 'sigma'], rango=(
             0, lím_error),
              certidumbre=1)

    def quitar_etapa(símismo, nombre):
        """
        Esta función quita una etapa del organismo.
        
        :param nombre: El nombre de la etapa a quitar (p. ej., "huevo" o "adulto")
        :type nombre: str
        """
        posición = símismo.receta['estr'][nombre]['posición']
        símismo.receta['estr'].pop(nombre)
        símismo.receta['coefs']['ecuaciones'].pop(nombre)
        símismo.config.pop(nombre)
        for dic_etp in símismo.receta['estr'].values():
            if dic_etp['posición'] > posición:
                dic_etp['posición'] -= 1
            if dic_etp['trans'] > posición:
                dic_etp['trans'] -= 1
            if dic_etp['repr'] > posición:
                dic_etp['repr'] -= 1

        símismo.actualizar()

    def aplicar_ecuación(símismo, etapa, tipo_ec):
        """
        Esta función aplica una configuración de ecuaciones a una etapa específica del organismo. No borar otras
        ecuaciones, sino simplemente cambia la ecuación activa usada para calibraciones, simulaciones, etc.

        :param etapa: El nombre de la etapa a cual esta ecuación se aplicará
        :type etapa: str

        :param tipo_ec: Un diccionario del tipo de ecuación que se aplicará. Debe tener el formato
        {categoría: {sub_categoría: opción_ecuación, sub_categoría: opción_ecuación, ...}, categoría: ...}
        :type tipo_ec: dict
        """
        símismo.verificar_ecs(ecs=tipo_ec, etp=etapa)
        for categ, dic_categ in tipo_ec.items():
            for sub_categ, opción_ec in dic_categ.items():
                símismo.receta['estr'][etapa]['ecs'][categ][sub_categ] = opción_ec

    def victimiza(símismo, víctima, etps_símismo=None, etps_víctima=None, método='presa', etp_sale=None):
        """
        Esta función establece relaciones de  entre organismos.

        :param víctima: La presa (usar un objeto Organismo, no el nombre de la presa).
        :type víctima: tikon.RAE.Organismo.Organismo

        :param etps_símismo: Lista de los nombres (cadena de carácteres) de las fases del depredador (este organismo)
          que se comen a la presa. Si se deja como "None", tomará todas las fases.
        :type etps_símismo: list | str

        :param etps_víctima: Lista de los nombres (cadena de carácteres) de las fases de la presa que se come el
          depredador (este organismo). Si se deja como "None", tomará todas las fases.
        :type etps_víctima: list | str

        :param método: El tipo de intereacción. Puede ser 'presa' o 'huésped'. '
        :type método: str

        :param etp_sale: La etapa de la cual sale el parasitoide o enfermedad, en caso de método == 'huésped'.
        :type etp_sale: str

        """
        if método not in ('presa', 'huésped'):
            raise ValueError('Método de relación víctima no válido.')
        else:
            if método == 'huésped':
                if etp_sale is None:
                    etp_sale = víctima.etapas[(-1)]['nombre']
                if etps_símismo is None:
                    etps_símismo = [x for x in símismo.receta['estr']]
                if etps_víctima is None:
                    etps_víctima = [x for x in víctima.receta['estr']]
            else:
                if type(etps_víctima) is str:
                    etps_víctima = [
                     etps_víctima]
                if type(etps_símismo) is str:
                    etps_símismo = [
                     etps_símismo]
            if 'juvenil' in etps_símismo:
                etps_símismo.remove('juvenil')
                etps_símismo += [e for e in símismo.receta['estr'] if 'juvenil' in e]
        for e_depred in etps_símismo:
            dic_víc = símismo.config[e_depred][método]
            if víctima.nombre not in dic_víc:
                if método == 'presa':
                    l_etps_víc = dic_víc[víctima.nombre] = []
                else:
                    if método == 'huésped':
                        dic_víc[víctima.nombre] = {'entra':[],  'sale':None}
                        l_etps_víc = dic_víc[víctima.nombre]['entra']
                for e_víc in etps_víctima:
                    if e_víc not in l_etps_víc:
                        l_etps_víc.append(e_víc)

                if método == 'huésped':
                    dic_víc[víctima.nombre]['sale'] = etp_sale

        for categ, dic_categ in Ec.ecs_orgs.items():
            for sub_categ, dic_sub_categ in dic_categ.items():
                for tipo_ec, dic_ec in dic_sub_categ.items():
                    for parám, dic_parám in dic_ec.items():
                        if dic_parám['inter'] is not None and método in dic_parám['inter']:
                            límites = dic_parám['límites']
                            for e_depred in etps_símismo:
                                dic = símismo.receta['coefs'][e_depred][categ][sub_categ][tipo_ec][parám]
                                if víctima.nombre not in dic:
                                    dic[víctima.nombre] = {}
                                for e_víc in etps_víctima:
                                    if e_víc not in dic[víctima.nombre]:
                                        no_informativo = límites_a_texto_dist(límites=límites)
                                        dic[víctima.nombre][e_víc] = {'0': no_informativo}

        símismo.actualizar()

    def novictimiza(símismo, víctima, etps_símismo=None, etps_víctima=None, método='presa'):
        """
        Esta función borra relaciones de depredador y presa entre organismos.

        :param víctima: La presa que ya no se come (usar un objeto Organismo, no el nombre de la presa).
        :type víctima: tikon.RAE.Organismo.Organismo

        :param etps_símismo: Lista de los nombres (cadena de carácteres) de las fases del depredador (este organismo)
          que ya no se comen a la presa. Si se deja como "None", tomará todas las fases.
        :type etps_símismo: list | str

        :param etps_víctima: Lista de los nombres (cadena de carácteres) de las fases de la presa que ya no se come el
          depredador (este organismo). Si se deja como "None", tomará todas las fases.
        :type etps_víctima: list | str

        :param método:
        :type método:

        """
        if método not in ('presa', 'huésped'):
            raise ValueError('Método de relación víctima no válido.')
        else:
            if etps_símismo is None:
                etps_símismo = [x for x in símismo.receta['estr']]
            else:
                if etps_víctima is None:
                    etps_víctima = [x for x in víctima.receta['estr']]
                if type(etps_víctima) is str:
                    etps_víctima = [
                     etps_víctima]
            if type(etps_símismo) is str:
                etps_símismo = [
                 etps_símismo]
        for e_depred in etps_símismo:
            dic_víc = símismo.receta['estr'][e_depred][método]
            if método == 'huésped':
                l_etps_víc = dic_víc[víctima.nombre]['entra']
            else:
                if método == 'presa':
                    l_etps_víc = dic_víc[víctima.nombre]
            for e_víc in etps_víctima:
                try:
                    l_etps_víc.pop(e_víc)
                except KeyError:
                    pass

            if len(l_etps_víc) == 0:
                dic_víc.pop(víctima.nombre)

    def especificar_apriori(símismo, etapa, ubic_parám, rango, certidumbre, org_inter=None, etp_inter=None, dibujar=False):
        """
        Esta función permite al usuario de especificar una distribución especial para el a priori de un parámetro.

        :param etapa: La etapa de este ORganismo a la cual hay que aplicar este a priori.
        :type etapa: str | list

        :param ubic_parám: Una lista de las llaves que traerán uno a través del diccionario de coeficientes del
        Organismo hasta el parámetro de interés.
        :type ubic_parám: list

        :param rango: El rango a cuál queremos limitar el parámetro
        :type rango: tuple

        :param certidumbre: La certidumbre, en (0, 1], que el parámetro se encuentre adentro del rango especificado.
        :type certidumbre: float

        :param org_inter: El nombre de otro organismo con el cual interactúa este Coso para este variable.
        :type org_inter: str

        :param etp_inter: La etapa del organismo con el cual interactua este.
        :type etp_inter: str

        :param dibujar: Si queremos dibujar el resultado o no.
        :type dibujar: bool

        """
        dic_ecs = símismo.dic_info_ecs
        if type(etapa) is list:
            lista_etps = etapa
        else:
            lista_etps = [
             etapa]
        if 'juvenil' in lista_etps:
            lista_etps.remove('juvenil')
            lista_etps += [x for x in símismo.receta['estr'] if 'juvenil' in x]
        dic = dic_ecs
        for llave in ubic_parám:
            try:
                dic = dic[llave]
            except KeyError:
                raise KeyError('Ubicación de parámetro erróneo.')

        try:
            tipo_inter = dic['inter']
        except KeyError:
            tipo_inter = None

        for etp in lista_etps:
            try:
                dic_parám = símismo.receta['coefs'][etapa]
            except KeyError:
                raise ValueError('La etapa "{}" no existe en este organismo.'.format(etp))

            if tipo_inter is None:
                if org_inter is None:
                    l_inter = [None]
                else:
                    raise ValueError('No se puede especificar interacciones para parámetros sin interacciones.')
            else:
                if org_inter is not None:
                    if etp_inter is not None:
                        l_inter = [[org_inter, etp_inter]]
                    else:
                        l_inter = [[org_inter, e] for i in tipo_inter for e in símismo.config[etp][i][org_inter]]
                else:
                    l_inter = [(o, e) for i in tipo_inter for o in símismo.config[etp][i] for e in símismo.config[etp][i][o] if i == 'presa' else símismo.config[etp][i][o]['entra'] if i == 'huésped' else ValueError]
                for inter in l_inter:
                    if dibujar:
                        archivo = (os.path.join)(símismo.proyecto, símismo.nombre, 'A prioris', *ubic_parám)
                        archivo = símismo._prep_directorio(archivo)
                        archivo_final = os.path.join(archivo, etp + '.png')
                        título = 'En ({}, {}), {}%'.format(round(rango[0], 3), round(rango[1], 3), certidumbre * 100)
                    else:
                        archivo_final = título = None
                    símismo._estab_a_priori(dic_ecs=dic_ecs, dic_parám=dic_parám, ubic_parám=ubic_parám, rango=rango,
                      certidumbre=certidumbre,
                      inter=inter,
                      dibujar=dibujar,
                      archivo=archivo_final,
                      título=título)

    def _sacar_coefs_interno(símismo):
        """
        Ver la documentación de Coso.

        :rtype: tuple(list, list)

        """
        lista_coefs = []
        lista_nombres = []
        for etp in símismo.etapas:
            for categ in sorted(Ec.ecs_orgs):
                for sub_categ in sorted(Ec.ecs_orgs[categ]):
                    tipo_ec = símismo.receta['estr'][etp['nombre']]['ecs'][categ][sub_categ]
                    dic_info_paráms = Ec.ecs_orgs[categ][sub_categ][tipo_ec]
                    for parám in sorted(dic_info_paráms):
                        dic = símismo.receta['coefs'][etp['nombre']][categ][sub_categ][tipo_ec][parám]
                        inters = dic_info_paráms[parám]['inter']
                        if inters is None:
                            l_coefs = [dic]
                            l_nombres = [[etp['nombre'], categ, sub_categ, parám]]
                        else:
                            if type(inters) is list:
                                l_coefs = []
                                l_nombres = []
                                for tipo_inter in inters:
                                    for org_inter, v in símismo.config[etp['nombre']][tipo_inter].items():
                                        if tipo_inter == 'huésped':
                                            lista_etps_inter = v['entra']
                                        else:
                                            if tipo_inter == 'presa':
                                                lista_etps_inter = v
                                            else:
                                                raise ValueError
                                        for etp_inter in lista_etps_inter:
                                            l_coefs.append(dic[org_inter][etp_inter])
                                            l_nombres.append([etp['nombre'], categ, sub_categ, parám, org_inter, etp_inter])

                            else:
                                raise ValueError
                        lista_coefs += l_coefs
                        lista_nombres += l_nombres

        return (
         lista_coefs, lista_nombres)

    def _sacar_líms_coefs_interno(símismo):
        lista_líms = []
        for etp in símismo.etapas:
            for categ in sorted(Ec.ecs_orgs):
                for sub_categ in sorted(Ec.ecs_orgs[categ]):
                    tipo_ec = símismo.receta['estr'][etp['nombre']]['ecs'][categ][sub_categ]
                    dic_paráms = Ec.ecs_orgs[categ][sub_categ][tipo_ec]
                    for parám in sorted(dic_paráms):
                        if dic_paráms[parám]['inter'] is None:
                            líms = [
                             dic_paráms[parám]['límites']]
                        else:
                            núm_inter = len(símismo.receta['coefs'][etp['nombre']][categ][sub_categ][tipo_ec][parám])
                            líms = [dic_paráms[parám]['límites']] * núm_inter
                        lista_líms += líms

        return lista_líms

    def _sacar_coefs_no_espec(símismo):
        """
        
        :return: 
        :rtype: dict 
        """
        sin_especif = {}

        def agregar_a_dic(e, c, s_c, t_e, p, o_i=None, e_i=None):
            d = sin_especif
            if e not in d:
                d[e] = {}
            d = d[e]
            if c not in d:
                d[c] = {}
            d = d[c]
            if s_c not in d:
                d[s_c] = {}
            d = d[s_c]
            if o_i is not None:
                if o_i not in d:
                    d[o_i] = {}
                if e_i not in d[o_i]:
                    d[o_i][e_i] = {}
                d = d[o_i][e_i]
            if t_e not in d:
                d[t_e] = []
            d[t_e].append(p)

        for etp in símismo.etapas:
            for categ in sorted(Ec.ecs_orgs):
                if categ == 'Error':
                    pass
                else:
                    for sub_categ in sorted(Ec.ecs_orgs[categ]):
                        tipo_ec = símismo.receta['estr'][etp['nombre']]['ecs'][categ][sub_categ]
                        dic_coefs = símismo.receta['coefs'][etp['nombre']][categ][sub_categ][tipo_ec]
                        dic_info = Ec.ecs_orgs[categ][sub_categ][tipo_ec]
                        for parám in sorted(dic_info):
                            inters = dic_info[parám]['inter']
                            if inters is None:
                                if 'especificado' not in dic_coefs[parám]:
                                    agregar_a_dic(etp['nombre'], categ, sub_categ, tipo_ec, parám)
                            else:
                                if type(inters) is list:
                                    for tipo_inter in inters:
                                        for org_inter, v in símismo.config[etp['nombre']][tipo_inter].items():
                                            if tipo_inter == 'presa':
                                                lista_etps_inter = v
                                            else:
                                                if tipo_inter == 'huésped':
                                                    lista_etps_inter = v['entra']
                                                else:
                                                    raise ValueError
                                            for etp_inter in lista_etps_inter:
                                                dic = dic_coefs[parám][org_inter][etp_inter]
                                                if 'especificado' not in dic:
                                                    agregar_a_dic((etp['nombre']), categ, sub_categ, tipo_ec, parám, o_i=org_inter,
                                                      e_i=etp_inter)

                                else:
                                    raise ValueError

        return sin_especif

    def verificar_ecs(símismo, ecs, etp):
        """
        Esta función verifica que las ecuaciones de una nueva etapa propuesta sean consistentes con las definiciones
        de ecuaciones para Organismos.

        :param ecs: El diccionario de ecuaciones propuestas.
        :type ecs: dict

        :param etp: El nombre de la etapa.
        :type etp: str

        """
        if 'Error' not in ecs:
            ecs['Error'] = {}
            ecs['Error']['Dist'] = 'Normal'
        for categ, d_categ in símismo.dic_info_ecs.items():
            if categ not in ecs:
                raise ValueError('Falta implementar ecuaciones de {} en etapa {} de organismo {}.'.format(categ, etp, símismo.nombre))
            for sub_categ, d_sub_categ in d_categ.items():
                if sub_categ not in ecs[categ]:
                    raise ValueError('Falta implementar ecuaciones de {} para {} en etapa {} de organismo {}.'.format(sub_categ, categ, etp, símismo.nombre))
                tipo_ec = ecs[categ][sub_categ]
                if tipo_ec not in d_sub_categ:
                    raise ValueError('El tipo de ecuación "{}" para {} en {} de etapa {} de organismo {} no está definido en Tiko\'n.'.format(tipo_ec, sub_categ, categ, etp, símismo.nombre))
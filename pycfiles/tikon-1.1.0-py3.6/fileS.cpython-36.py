# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\ModExtern\DSSAT\fileS.py
# Compiled at: 2017-01-26 15:19:48
# Size of source mod 2**32: 7636 bytes
import numpy as np, re, pkg_resources
from tikon.Matemáticas import Ecuaciones as Ec
DSSAT_a_Tikon = dict([(x['cód_DSSAT'], x) for x in Ec.ecs_suelo if 'cód_DSSAT' in x.keys()])

def cargar_suelo(nombre, archivo):
    """
    Esta función carga la información de un suelo de un archivo en particular.

    :param nombre: El nombre del suelo.
    :type nombre: str

    :param archivo: El archivo en el cuál se ubica este suelo.
    :type archivo: str

    :return: Un tuple de los diccionarios de información y de coeficientes del suelo.
    :rtype: tuple[dict, dict]

    """
    with open(archivo) as (d):
        doc = d.readlines()
    princ = next(i for i, l in enumerate(doc) if re.match('\\*{}'.format(nombre), l))
    fin = princ + 1 + next(i for i, l in enumerate(doc[princ + 1:]) if re.match('\\n|\\*[\\w]{10}', l))
    _, info, coefs = decodar(doc[princ:fin])
    return (
     info, coefs)


def cargar_suelos_doc(archivo):
    """
    Esta función carga todos los suelos presentes en un documento de suelos.

    :param archivo: El documento de suelos.
    :type archivo: str

    :return: Un tuple de listas con los nombres, los diccionarios de información y los diccionarios de coeficientes
    de los suelos.
    :rtype: tuple[list[str], list[dict], list[dict]]

    """
    with open(archivo) as (d):
        doc = d.readlines()
    índs_sl = [(n, n + 1 + next(i for i, l_s in enumerate(doc[n + 1:]) if re.match('\n|\\*[\\w]{10}', l_s))) for n, l in enumerate(doc) if re.match('\\*[\\w\\d_]{10}', l)]
    l_dics_coefs = []
    l_dics_info = []
    l_nombres = []
    for u in índs_sl:
        nombre, dic_info, dic_coefs = decodar(doc[u[0]:u[1]])
        l_nombres.append(nombre)
        l_dics_info.append(dic_info)
        l_dics_coefs.append(dic_coefs)

    return (
     l_nombres, l_dics_info, l_dics_coefs)


def decodar(doc_suelo):
    """
    Esta función decoda las líneas de un documento de suelos que corresponden a un suelo en particular.

    :param doc_suelo: Una lista de las líneas correspondiendo a un suelo en un archivo DSSAT.
    :type doc_suelo: list[str]

    :return: Un tuple con el nombre y los diccionarios de información y de coeficientes del suelo.
    :rtype: tuple[str, dict, dict]

    """
    dic_dssat = {}
    info = {}
    l_1 = doc_suelo[0].replace('\n', '')
    nombre = l_1[1:11]
    info['fuente'] = l_1[13:24].strip()
    info['textura'] = l_1[25:30].strip()
    info['descrip'] = l_1[37:].strip()
    dic_dssat['profund'] = l_1[31:36].strip()
    índ_sec_suelo = [(n,
     n + 1 + next((i for i, l_s in enumerate(doc_suelo[n + 1:]) if re.match('@', l_s)), len(doc_suelo))) for n, l in enumerate(doc_suelo) if re.match('@', l)]
    for n, ubic_vars in enumerate(índ_sec_suelo):
        l_vars_dssat = [x.strip() for x in doc_suelo[ubic_vars[0]].replace('@', '').replace('\n', '').split()]
        ubic_vals = np.array([0] + [Ec.ecs_suelo[DSSAT_a_Tikon[v]['tmñ_DSSAT']] for v in l_vars_dssat]).cumsum()
        for var in l_vars_dssat:
            dic_dssat[var] = []

        for l in doc_suelo[ubic_vars[0] + 1:ubic_vars[1]]:
            vals = [float(l[u:ubic_vals[(n + 1)]]) for n, u in enumerate(ubic_vals[:-1])]
            for n_v, var in enumerate(l_vars_dssat):
                dic_dssat[var].append(vals[n_v])

    coefs = {}
    for var_DSSAT, val in dic_dssat:
        try:
            var = DSSAT_a_Tikon[var_DSSAT]
            coefs[var] = dic_dssat[var]
        except KeyError:
            pass

    for var, val in coefs.items():
        val = np.array(val)
        val[val == -99] = np.nan
        if len(val) == 1:
            coefs[var] = val[0]

    return (nombre, info, coefs)


def escribir(archivo, nombre, dic, borrar=False):
    """

    :param archivo:
    :type archivo:

    :param nombre:
    :type nombre:

    :param dic:
    :type dic:

    :param borrar:
    :type borrar:

    """
    ubic_plantilla = pkg_resources.resource_filename('tikon.Cultivo.ModExtern.DSSAT', 'FILES.txt')
    with open(ubic_plantilla, 'r') as (d):
        plantilla = d.readlines()
    nuevas_líneas = []
    for l in plantilla:
        if re.match('@', l):
            nuevas_líneas.append(l)
            l_vars = [x.strip() for x in l.replace('@', '').replace('\n', '').split()]
        else:
            n_niveles = len(dic[l_vars[0]])
            for i in range(n_niveles):
                dic = dict([(Ec.ecs_suelo[v]['cód_DSSAT'], dic[v][i] if dic[v][i] != np.nan else -99) for v in l_vars])
                nuevas_líneas.append(l.format(dic))

    if borrar:
        with open(archivo, 'w') as (d):
            d.write(''.join(nuevas_líneas))
    else:
        with open(archivo, 'r+') as (d):
            doc = d.readlines()
        try:
            ubic_suelo = [(n, n + 1 + next(i for i, l_s in enumerate(doc[n + 1:]) if re.match('\n|\\*[\\w]{10}', l_s))) for n, l in enumerate(doc) if re.match('\\*{}'.format(nombre), l)]
        except StopIteration:
            ubic_suelo = None

        if ubic_suelo is not None:
            doc[ubic_suelo[0]:ubic_suelo[1]] = []
        doc += nuevas_líneas
        with open(archivo, 'w') as (d):
            d.write(''.join(doc))
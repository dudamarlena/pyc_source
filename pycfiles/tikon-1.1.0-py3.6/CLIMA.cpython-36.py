# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\CLIMA.py
# Compiled at: 2017-01-05 16:18:47
# Size of source mod 2**32: 10914 bytes
from COSO import Coso
from tikon.Clima import eval_estaciones
from tikon.Clima import generarmeteo
from tikon.Clima import krigear

class Diario(Coso):

    def __init__(símismo, nombre='', coord=()):
        dic = dict(Lugar='', País=[], Departamento=[], Municipio=[], Cód_lugar=[], Lat=(coord[0]), Long=(coord[1]), Elev=[], Temp_prom=[], Alt_med_temp=[], Alt_med_viento=[], Amp_temp_mens=[], Fecha=[], Rad_sol=[], Temp_máx=[], Temp_mín=[], Precip=[], Temp_conden=[], Viento=[], Rad_foto=[], Hum_rel=[])
        if not len(nombre):
            if len(coord):
                nombre = '%sN_%sW' % (coord[0], coord[1])
        super().__init__(nombre=nombre, ext='día', dic=dic, directorio=(os.path.join('Clima', 'Datos')))

    def buscar(símismo, fecha_inic, fecha_fin):
        lugar = símismo.dic['Lugar']
        coord = (
         símismo.dic['Lat'], símismo.dic['Long'])
        encontrado = faltan_pt = faltan_por = faltan = generamos = False
        estación = {}
        estaciones = {}
        dic = dict(Coord=(), Elev='', Datos=dict(Fecha=[], Precip=[], Rad_sol=[], Temp_máx=[], Temp_mín=[]))
        with open(os.path.join('Clima', 'Estaciones.csv')) as (d):
            doc = d.readlines()
        datos = doc[0].split(',')
        col_estación = datos.index('Estación')
        col_long = datos.index('Longitud')
        col_lat = datos.index('Latitud')
        col_alt = datos.index('Altitud')
        col_municipio = datos.index('Municipio')
        for lín in doc[1:]:
            datos = lín.split(',')
            estaciones[datos[col_estación]] = dict(Estación=(datos[col_estación]), Lat=(datos[col_lat]), Long=(datos[col_long]),
              Elev=(datos[col_alt]),
              Municipio=(datos[col_municipio]))

        lím_distancia = 10
        for i in estaciones:
            if i['Lat'] == coord[0]:
                if i['Long'] == coord[1]:
                    estación = estaciones[i]
                    encontrado = True
                    break
                else:
                    if i['Estación'] == lugar:
                        estación = estaciones[i]
                        encontrado = True
                        break
                    elif dist(coord, dist(estaciones[i]['Lat'], estaciones[i]['Long'])).km < lím_distancia:
                        lím_distancia = dist(estaciones[i]['Lat'], estaciones[i]['Long']).km
                        estación = estaciones[i]
                        encontrado = True

        if encontrado:
            símismo.nombre = estación['Estación']
            símismo.dic['Lugar'] = símismo.nombre
            directorio = os.path.join('Clima', 'Datos', símismo.nombre, '.csv')
            dic, faltan, faltan_pt, faltan_por = cargar_estación(directorio, (estación['Lat'], estación['Long']), estación['Elev'], fecha_inic, fecha_fin)
            if not faltan:
                return
        if not encontrado or faltan:
            for doc_meteogen in os.listdir(os.path.join('Clima', 'Datos', 'Generados')):
                if doc_meteogen.lower() == lugar.lower() + '.día':
                    símismo.nombre = estación['Estación']
                    símismo.dic['Lugar'] = símismo.nombre
                    dic, faltan, faltan_pt, faltan_por = cargar_estación(doc_meteogen, fecha_inic, fecha_fin)
                    if not faltan:
                        return
                    break

        if encontrado:
            estaciones_cercanas = buscar_cercanas(100, coord, estaciones)
            for var in dic['Datos']:
                if var != 'Fecha':
                    if var != 'Coord':
                        fechas_prededidas_cum = estimaciones_cum = []
                        for tipo, tipo_f in [('puntual', faltan_pt), ('extensa', faltan_por)]:
                            while len(tipo_f[var]):
                                estaciones_interés = verificar_fechas(var, estaciones_cercanas, tipo_f[var])
                                a, b, d = eval_estaciones(var, dic, estaciones_interés, tipo)
                                fechas_predecidas = [x for x in d['Fecha'] if x in tipo_f[var] if not np.isnan(d[var].index(x))]
                                predictores = [x[var] for x in d if d['Fecha'] in fechas_predecidas]
                                estimaciones = [a + x * b for x in predictores]
                                estimaciones_cum += estimaciones
                                fechas_prededidas_cum += fechas_predecidas
                                for fecha in fechas_predecidas:
                                    tipo_f[var].pop(tipo_f[var].index(fecha))

                                if not len(estaciones_interés):
                                    break

                        if len(fechas_prededidas_cum):
                            generamos = True
                    for f, d in zip(fechas_prededidas_cum, estimaciones_cum):
                        if f in dic['Fecha']:
                            dic['Datos'][var][dic['Fecha'].index(f)] = d
                        else:
                            dic['Datos'][var].append(d)
                            dic['Fecha'].append(f)

        else:
            estaciones_cercanas = buscar_cercanas(30, coord, estaciones)
            dic = krigear(dic, estaciones_cercanas, fecha_inic, fecha_fin)
            generamos = True
        símismo.dic['Lat'] = dic['Coord'][0]
        símismo.dic['Long'] = dic['Coord'][1]
        símismo.dic['Elev'] = dic['Elev']
        símismo.dic['Fecha'] = [x.strftime('%Y-%m-%d') for x in símismo.dic['Fecha']]
        símismo.dic['Precip'] = dic['Precip']
        símismo.dic['Rad_sol'] = dic['Rad_sol']
        símismo.dic['Temp_máx'] = dic['Temp_máx']
        símismo.dic['Temp_mín'] = dic['Temp_mín']
        if generamos:
            símismo.directorio = os.path.join('Proyectos', 'Clima', 'Generado')
            símismo.guardar()


class Clima(Coso):

    def __init__(símismo, nombre, directorio):
        dic = dict(Lugar='', Cód_lugar=[], Lat=[], Long=[], Elev=[], Temp_prom=[], Amp_temp_mens=[], Rad_dia_prom_anual=[], Tdia_máx_prom_anual=[], Tdia_mín_prom_anual=[], Prec_dia_prom_anual=[], Primerdía_sinhelada_prom=[], Prom_dur_heladas=[], Intercept_angstrom=[], Multiplicador_angstrom=[], Alt_med_temp=[], Alt_med_viento=[], Princ_datos_obs=(), Núm_años_obs=(), Mes=[], Rad_prom_mens=[], Tdía_máx_prom_mens=[], Tdía_mín_prom_mens=[], Prec_total_prom_mens=[], Prom_días_prec_mens=[], Horas_sol_dia_prom_mens=[], Intercept_angstrom_mens=[], Multiplicador_angstrom_mens=[], Prom_rad_dia_seco_mens=[], Varia_rad_dia_seco_mens=[], Prom_rad_dia_lluv_mens=[], Varia_rad_dia_lluv_mens=[], Prom_temp_dia_seco_mens=[], Varia_temp_dia_seco_mens=[], Prom_temp_dia_lluv_mens=[], Varia_temp_dia_lluv_mens=[], Varia_temp_dia_min_prom=[], Alpha_distgamma_prec=[], Prob_lluv_después_seco=[])
        super().__init__(nombre=nombre, ext='cli', dic=dic, directorio=directorio)

    def gendiario(símismo, fecha_inic, fecha_fin):
        diario = Diario(nombre=(símismo.nombre), coord=(símismo.dic['Lat'], símismo.dic['Long']))
        diario.dic['Lugar'] = símismo.dic['Lugar']
        diario.dic['Cód_lugar'] = símismo.dic['Cód_lugar']
        diario.dic['Elev'] = símismo.dic['Elev']
        diario.dic['Fecha'] = [fecha_inic + ft.timedelta(days=x) for x in range((fecha_fin - fecha_inic).days)]
        generados = generarmeteo(símismo.dic, fecha_inic, fecha_fin)
        diario.dic['Rad_sol'] = generados['Rad_sol']
        diario.dic['Temp_máx'] = generados['Temp_máx']
        diario.dic['Temp_mín'] = generados['Temp_mín']
        diario.dic['Precip'] = generados['Precip']
        diario.dic['Temp_conden'] = generados['Temp_conden']
        diario.dic['Viento'] = generados['Viento']
        diario.dic['Rad_foto'] = generados['Rad_foto']
        return diario
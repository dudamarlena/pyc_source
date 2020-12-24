# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Proyectos\Café\Leucoptera_coffeella\L.coffeella.py
# Compiled at: 2017-08-25 13:07:47
# Size of source mod 2**32: 906 bytes
import tikon.RAE.Insecto as Ins, tikon.RAE.Planta as Plt
from tikon.Matemáticas.Experimentos import Experimento
dib_aprioris = False
ops_dib = {'incert':None,  'todas_líneas':True}
proyecto = 'Café\\Leucoptera_coffeella'
Café = Plt.Hojas('Café', proyecto=proyecto)
Café.estimar_densidad(rango=(38000000000.0, 42000000000.0), certidumbre=0.95)
Leucoptera_coffeella = Experimento(nombre='Suconusco_Chiapas', proyecto=proyecto)
Leucoptera_coffeella.agregar_orgs(archivo='Suconusco_Chiapas.csv', col_tiempo='Dia', factor=1)
Leucoptera_coffeella = Ins.MetamCompleta('L.coffeella', proyecto=proyecto, njuvenil=1)
Parasitoide_larvas = Ins.Parasitoide('Parasitoide larvas', proyecto=proyecto)
Parasitoides_pupa = Ins.Parasitoide('Parasitoide pupas', proyecto=proyecto)
Leucoptera_coffeella.secome(Café, etps_depred='juvenil')
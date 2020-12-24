# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Proyectos\Opisina_arenosella\a_prioris.py
# Compiled at: 2017-10-26 16:37:23
# Size of source mod 2**32: 17137 bytes
"""
Estos datos de distribuciones a prioris vienen de la literatura (ver el documento Excel adjunto).
¿Se me olvidó juntarlo? Escríbame: julien.malard@mail.mcgill.ca

Referencia excelente:
http://www.nhm.ac.uk/our-science/data/chalcidoids/database/detail.dsml?VALDATE=1930&ValidAuthBracket=false&FamilyCode
=CC&VALSPECIES=nephantidis&listPageURL=listChalcids.dsml%3FSpecies%3Daeca%26Superfamily%3DChalcidoidea%26Family%3DCha
lcididae%26Genus%3DBrachymeria&tab=biology&HOMCODE=0&VALGENUS=Brachymeria&VALAUTHOR=Gahan&keyword=Fc
"""
a_prioris = {'O. arenosella_senc':[
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Modif', 'Ninguna', 'r'],
    rango=(1.927758, 3.405402),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Ecuación', 'Logístico Presa', 'K'],
    org_inter='Palma de coco',
    etp_inter='planta',
    rango=(0.0004952947003467063, 0.0006146281499692685),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    org_inter='Palma de coco',
    etp_inter='planta',
    rango=(2.2000043269906862e-08, 5.045649639020519e-08),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    org_inter='Palma de coco',
    etp_inter='planta',
    rango=(4.840019038777742e-16, 2.5458580279747892e-15),
    certidumbre=0.8)], 
 'Parasitoide_senc':[
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Modif', 'Ninguna', 'r'],
    rango=(0.32160000000000005, 4.3656),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Ecuación', 'Logístico Presa', 'K'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(1, 1),
    certidumbre=1),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(0.6666666666666666, 4.474416666666667),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(0.4444444444444444, 20.020404506944452),
    certidumbre=0.8)], 
 'Araña':[
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Modif', 'Ninguna', 'r'],
    rango=(0.8333333333333334, 2.5),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Ecuación', 'Logístico Presa', 'K'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(0.6493506493506493, 1.4285714285714286),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Crecimiento', 'Ecuación', 'Logístico Presa', 'K'],
    org_inter='Parasitoide_senc',
    etp_inter='adulto',
    rango=(0.02, 0.1),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(0.7, 1.54),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    org_inter='O. arenosella_senc',
    etp_inter='adulto',
    rango=(10000, 1000000),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    org_inter='Parasitoide_senc',
    etp_inter='adulto',
    rango=(10, 50),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    org_inter='Parasitoide_senc',
    etp_inter='adulto',
    rango=(100000000, 10000000000),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1)], 
 'O. arenosella':[
  dict(etapa='huevo', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(2, 4),
    certidumbre=0.8),
  dict(etapa='huevo', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='huevo', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.025, 0.029),
    certidumbre=0.5),
  dict(etapa='huevo', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil_1', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(4.4000086539813725e-09, 1.0091299278041038e-08),
    certidumbre=0.8),
  dict(etapa='juvenil_1', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(1.9360076155110976e-17, 1.0183432111899155e-16),
    certidumbre=0.8),
  dict(etapa='juvenil_1', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.01, 0.1),
    certidumbre=0.5),
  dict(etapa='juvenil_1', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(5, 9),
    certidumbre=0.8),
  dict(etapa='juvenil_1', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='juvenil_1', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil_2', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(4.4000086539813725e-09, 1.0091299278041038e-08),
    certidumbre=0.8),
  dict(etapa='juvenil_2', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(1.9360076155110976e-17, 1.0183432111899155e-16),
    certidumbre=0.8),
  dict(etapa='juvenil_2', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.00875, 0.06666666666666667),
    certidumbre=0.5),
  dict(etapa='juvenil_2', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(6, 8),
    certidumbre=0.8),
  dict(etapa='juvenil_2', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='juvenil_2', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil_3', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(4.4000086539813725e-09, 1.0091299278041038e-08),
    certidumbre=0.8),
  dict(etapa='juvenil_3', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(1.9360076155110976e-17, 1.0183432111899155e-16),
    certidumbre=0.8),
  dict(etapa='juvenil_3', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.00875, 0.06666666666666667),
    certidumbre=0.5),
  dict(etapa='juvenil_3', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(6, 8),
    certidumbre=0.8),
  dict(etapa='juvenil_3', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='juvenil_3', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil_4', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(4.4000086539813725e-09, 1.0091299278041038e-08),
    certidumbre=0.8),
  dict(etapa='juvenil_4', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(1.9360076155110976e-17, 1.0183432111899155e-16),
    certidumbre=0.8),
  dict(etapa='juvenil_4', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.011666666666666667, 0.125),
    certidumbre=0.5),
  dict(etapa='juvenil_4', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(4, 6),
    certidumbre=0.8),
  dict(etapa='juvenil_4', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='juvenil_4', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil_5', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(4.4000086539813725e-09, 1.0091299278041038e-08),
    certidumbre=0.8),
  dict(etapa='juvenil_5', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(1.9360076155110976e-17, 1.0183432111899155e-16),
    certidumbre=0.8),
  dict(etapa='juvenil_5', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.006363636363636364, 0.08888888888888889),
    certidumbre=0.5),
  dict(etapa='juvenil_5', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(9, 11),
    certidumbre=0.8),
  dict(etapa='juvenil_5', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='juvenil_5', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='pupa', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='pupa', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(7, 9),
    certidumbre=0.8),
  dict(etapa='pupa', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='pupa', ubic_parám=[
   'Muertes', 'Ecuación', 'Constante', 'q'],
    rango=(0.007777777777777778, 0.08571428571428572),
    certidumbre=0.5),
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(2.6, 8.4),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(1, 4),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Reproducción', 'Prob', 'Normal', 'n'],
    rango=(29.5, 126.0),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Reproducción', 'Prob', 'Normal', 'mu'],
    rango=(2.5, 4.5),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Reproducción', 'Prob', 'Normal', 'sigma'],
    rango=(1, 2),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1)], 
 'Parasitoide larvas':[
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(10, 20),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(5, 10),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(0.25, 1.5),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(100000000.0, 1000000000.0),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Mult', 'Linear', 'a'],
    rango=(1, 10),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(9, 11),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(0.5, 0.6),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1)], 
 'Parasitoide pupas':[
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(10, 20),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(5, 10),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'a'],
    rango=(0.25, 1.5),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Depredación', 'Ecuación', 'Kovai', 'b'],
    rango=(100000.0, 3000000.0),
    certidumbre=0.8),
  dict(etapa='adulto', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Mult', 'Linear', 'a'],
    rango=(1, 10),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'mu'],
    rango=(7, 9),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Transiciones', 'Prob', 'Normal', 'sigma'],
    rango=(0.5, 0.6),
    certidumbre=0.8),
  dict(etapa='juvenil', ubic_parám=[
   'Error', 'Dist', 'Normal', 'sigma'],
    rango=(0, 0.01),
    certidumbre=1)]}
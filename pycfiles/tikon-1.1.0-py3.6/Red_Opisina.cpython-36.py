# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Proyectos\Opisina_arenosella\Red_Opisina.py
# Compiled at: 2017-10-24 18:18:54
# Size of source mod 2**32: 1272 bytes
from tikon.RAE.RedAE import Red
import tikon.RAE.Insecto as Ins, tikon.RAE.Planta as Plt
proyecto = 'Opisina_arenosella'
Coco = Plt.Hojas('Coco', proyecto=proyecto)
Ins.Sencillo('Araña', proyecto=proyecto)
O_arenosella = Ins.MetamCompleta('O. arenosella', proyecto=proyecto, njuvenil=5)
Parasitoide_larvas = Ins.Parasitoide('Parasitoide larvas', proyecto=proyecto)
Parasitoide_pupa = Ins.Parasitoide('Parasitoide pupas', proyecto=proyecto)
O_arenosella.secome(Coco, etps_depred='juvenil')
Parasitoide_larvas.parasita(O_arenosella, etps_infec=['juvenil_1', 'juvenil_2', 'juvenil_3'], etp_sale='juvenil_5')
Parasitoide_pupa.parasita(O_arenosella, etps_infec=['pupa'], etp_sale='pupa')
Red_coco = Red(nombre='Red coco_prueba', organismos=[O_arenosella, Parasitoide_larvas, Parasitoide_pupa, Coco], proyecto=proyecto)
Araña = Ins.Sencillo('Araña', proyecto=proyecto)
Araña.secome(O_arenosella, etps_presa=['juvenil', 'adulto'])
Araña.secome(Parasitoide_pupa, etps_presa=['adulto'])
Araña.secome(Parasitoide_larvas, etps_presa=['adulto'])
Red_coco_araña = Red(nombre='Coco araña', proyecto=proyecto, organismos=[
 O_arenosella, Parasitoide_larvas, Parasitoide_pupa, Araña, Coco])
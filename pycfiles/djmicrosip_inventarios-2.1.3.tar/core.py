# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_inventarios\djmicrosip_inventarios\utils\documents\core.py
# Compiled at: 2019-09-17 20:13:06


def InventarioFisicoNewFolio():
    from django_microsip_base.libs.models_base.models import Registry
    registro = Registry.objects.get(nombre='SIG_FOLIO_INVFIS')
    new_folio = '%09d' % (int(registro.valor) + 1)
    registro.valor = new_folio
    registro.save()
    return new_folio
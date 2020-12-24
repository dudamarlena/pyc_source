# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reorden\djmicrosip_reorden\models.py
# Compiled at: 2015-10-22 12:35:21
from django.db import models
from django_microsip_base.libs.models_base.models import Articulo, Registry, Almacen, Proveedor, VentasDocumento, VentasDocumentoDetalle, ComprasDocumento, ComprasDocumentoDetalle, ArticuloClave, InventariosDocumento, InventariosDocumentoDetalle, InventariosConcepto, ConexionDB, Cliente, ClienteClave, ClienteDireccion, Moneda
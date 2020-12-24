# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/postgres/borrar.py
# Compiled at: 2012-10-29 11:33:17
from sqlalchemy.exc import NoSuchTableError
from neptuno import Neptuno
from libpy.conexion import Conexion

def delete(id_usuario, tabla, id_registro, conector=None):
    """
    Borrar un registro de una tabla.
    
    IN
      id_usuario   <int>
      tabla        <str>
      id_registro  <int>
    """
    if conector is None:
        conector = Conexion()
    try:
        la_tabla = Neptuno(conector, tabla, id_usuario)
    except NoSuchTableError:
        la_tabla = Neptuno(conector, str(tabla).replace('vista_busqueda_', ''), id_usuario)

    if la_tabla.delete_registro(id_registro):
        return '{}'
    else:
        raise Exception
        return
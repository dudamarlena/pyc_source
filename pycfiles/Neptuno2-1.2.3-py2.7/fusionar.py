# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neptuno/postgres/fusionar.py
# Compiled at: 2012-10-29 11:33:17
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.expression import select

class ENoExisteRegistro(Exception):

    def __init__(self, id_reg):
        Exception.__init__(self)
        self.id_reg = id_reg

    def __repr__(self):
        return 'No existe el registro %d' % self.id_reg


def merge(nombre_tabla, id_destino, otros_ids, session):
    u"""
    Fusiona uno o más registros (otros_ids) en otro (id_destino), siendo todos ellos
    de la tabla 'nombre_tabla'.
    
    IN
      id_usuario   <int>: Identificador del usuario que se conecta
      nombre_tabla <str>: Nombre de la tabla a la que pertenecen los registros
      id_destino   <int>: Identificador del registro donde se guardará la información
      otros_ids    <list> [<int>, ...]: Lista de ids desde donde se obtendrá la información
    
    OUT
      un JSON de la forma:
      {
       'id_destino': 123,
       'id_origen': 123,
       'num_campos': 123
      }
    
    EXC
      ENoExisteRegistro: Cuando no existe alguno de los registros (origen o destino)
    """
    meta = MetaData(bind=session.bind, reflect=True)
    tabla = Table(nombre_tabla, meta, autoload=True)
    alumno = session.execute(select([tabla], tabla.c.id == id_destino)).fetchone()
    if alumno is None:
        raise ENoExisteRegistro(id_destino)
    for id_otro in otros_ids:
        otro = session.execute(select([tabla], tabla.c.id == id_otro)).fetchone()
        if otro is None:
            raise ENoExisteRegistro(id_otro)

    resultado = {}
    resultado['id_destino'] = id_destino
    resultado['num_campos'] = 0
    for id_otro in otros_ids:
        if id_otro == id_destino:
            continue
        resultado['id_origen'] = id_otro
        alumno = session.execute(select([tabla], tabla.c.id == id_destino)).fetchone()
        otro = session.execute(select([tabla], tabla.c.id == id_otro)).fetchone()
        for t in meta.sorted_tables:
            for fk in t.foreign_keys:
                if fk.references(tabla):
                    qry_update = t.update(fk.parent == id_otro, values={fk.parent: id_destino})
                    session.execute(qry_update)

        session.commit()
        datos = {}
        for k in alumno.keys():
            if k != 'id' and k != 'busqueda':
                if alumno[k] is None and otro[k] != None:
                    datos[k] = otro[k]
                    resultado['num_campos'] += 1

        if datos != {}:
            qry_update = tabla.update(tabla.c.id == id_destino, values=datos)
            session.execute(qry_update)
        qry_delete = tabla.delete(tabla.c.id == id_otro)
        session.execute(qry_delete)
        session.commit()

    return resultado
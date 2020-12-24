# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/protoRules.py
# Compiled at: 2014-05-29 10:16:48
import traceback
ONDELETE_TYPES = (
 ('CASCADE', 'Cascade deletes; the default'),
 ('PROTECT', 'Prevent deletion of the referenced object by raising ProtectedError, a subclass of django.db.IntegrityError'),
 ('SET_NULL', 'Set the ForeignKey null; this is only possible if null is True'),
 ('SET_DEFAULT', 'Set the ForeignKey to its default value; a default for the ForeignKey must be set.  @function si possible'),
 ('DO_NOTHING', 'Use default Db constraint'))
BASE_TYPES = (
 ('string', 'string'),
 ('text', 'text'),
 ('bool', 'bool'),
 ('int', 'int'),
 ('sequence', 'sequence'),
 ('decimal', 'decimal'),
 ('money', 'money'),
 ('combo', 'combo'),
 ('date', 'date'),
 ('datetime', 'datetime'),
 ('time', 'time'))
CRUD_TYPES = (
 ('storeOnly', 'No se presentan nunca (los id, jsonTypes, etc )'),
 ('readOnly', 'No se guarda nunca (usado por reglas de gestion)'),
 ('insertOnly', 'No se actualiza (un campo absorbido al momento de la creacion, ej:direccion de envio'),
 ('updateOnly', 'Al insertar nulo o VrDefault, (estado inicial fijo)'))
DB_ENGINE = (
 ('sqlite3', 'sqlLite3'),
 ('postgres', 'Postgress'),
 ('mysql', 'mySQL'))
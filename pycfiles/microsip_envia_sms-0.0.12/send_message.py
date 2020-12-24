# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\BitBucket\microsip_envia_sms\microsip_envia_sms\send_message.py
# Compiled at: 2015-02-18 18:16:17
import time, re, unidecode, threading, fdb, importlib, sys
from settings import MODULES
from microsip_api.apps.sms.core import SMSMasivo

def execute_sql(sql, **kwargs):
    user = kwargs.get('user', None)
    password = kwargs.get('password', None)
    database = kwargs.get('database', None)
    return_data = kwargs.get('return_data', True)
    db = fdb.connect(host='localhost', user=user, password=password, database=database)
    cur = db.cursor()
    cur.execute(sql)
    data = None
    if return_data:
        data = cur.fetchall()
    try:
        db.commit()
    except Exception as e:
        pass

    cur.close()
    return data


def set_function_interval(func, sec, **kwargs):

    def func_wrapper():
        set_function_interval(func, sec, **kwargs)
        func(**kwargs)

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


errror = False
try:
    from conf import llave as apikey, usuario as user, db_ruta as database, empresa_nombre, modo_pruebas, contrasena as password
except:
    print 'Configuracion de aplicacion invalida'
    time.sleep(5)
    errror = True
else:
    try:
        db = fdb.connect(host='localhost', user=user, password=password, database=database)
        cur = db.cursor()
        cur.close()
    except fdb.DatabaseError as e:
        print 'Error en datos de conexion'
        time.sleep(5)
        errror = True

def checar_base_datos():
    kwargs = {'user': user, 'password': password, 
       'database': database}
    exists = execute_sql("select 1 from rdb$relations where rdb$relation_name = 'SIC_MENSAJES_PENDIENTES'", **kwargs)
    exists_generator = execute_sql("select 1 from rdb$Generators where RDB$GENERATOR_NAME = 'GEN_SIC_MENSAJES_PENDIENTES_ID'", **kwargs)
    kwargs['return_data'] = False
    if not exists_generator:
        execute_sql('\n        CREATE GENERATOR GEN_SIC_MENSAJES_PENDIENTES_ID;\n        ', **kwargs)
    if not exists:
        execute_sql('\n            CREATE TABLE SIC_MENSAJES_PENDIENTES (\n            ID        INTEGER NOT NULL,\n            TELEFONO  TELEFONO_TYPE NOT NULL /* TELEFONO_TYPE = VARCHAR(35) */,\n            CLIENTE   NOMBRE_LARGO /* NOMBRE_CORTO = VARCHAR(30) */,\n            TIPO      NOMBRE_CORTO NOT NULL /* NOMBRE_CORTO = VARCHAR(30) */,\n            VALORES   MEMO NOT NULL /* MEMO = BLOB SUB_TYPE 1 SEGMENT SIZE 80 */,\n            MENSAJE   MEMO,\n            INTENTOS  INTEGER default 0 NOT NULL );\n        ', **kwargs)
    execute_sql('\n        CREATE OR ALTER TRIGGER SIC_MENSAJES_PENDIENTES_BI0 FOR SIC_MENSAJES_PENDIENTES\n        ACTIVE BEFORE INSERT POSITION 0\n        AS\n        BEGIN\n          IF (NEW.id = -1) THEN\n            NEW.ID = GEN_ID(GEN_SIC_MENSAJES_PENDIENTES_ID,1);\n        END\n    ', **kwargs)
    execute_sql('\n        GRANT ALL ON SIC_MENSAJES_PENDIENTES TO USUARIO_MICROSIP\n    ', **kwargs)
    execute_sql("\n        CREATE OR ALTER TRIGGER SIC_MENSAJES_DOCTOS_VE FOR DOCTOS_VE\n        ACTIVE AFTER UPDATE POSITION 0\n        AS\n        declare variable telefono char(80);\n        declare variable cliente_nombre char(100);\n        declare variable valores char(80);\n\n        begin\n          if  (old.aplicado = 'N' AND NEW.aplicado = 'S' AND NEW.tipo_docto ='F' AND not NEW.cliente_id is NULL) THEN\n          begin\n            SELECT telefono1 FROM dirs_clientes WHERE dir_cli_id= NEW.dir_cli_id INTO telefono;\n            select nombre from clientes where cliente_id= new.cliente_id into cliente_nombre;\n            valores = new.folio || ','||new.importe_neto;\n            if (not :telefono is null) then\n            begin\n                INSERT INTO sic_mensajes_pendientes VALUES(-1,:TELEFONO,:cliente_nombre,'GRACIAS',:valores,null,0);\n            end\n          end\n        end\n    ", **kwargs)
    execute_sql("\n        CREATE OR ALTER TRIGGER SIC_MENSAJES_DOCTOS_PV FOR DOCTOS_PV\n        ACTIVE AFTER UPDATE POSITION 0\n        AS\n        declare variable telefono char(80);\n        declare variable cliente_nombre char(100);\n        declare variable valores char(80);\n\n        begin\n          if  (old.aplicado = 'N' AND NEW.aplicado = 'S' AND NEW.tipo_docto ='F' AND not NEW.cliente_id is NULL) THEN\n          begin\n            SELECT telefono1 FROM dirs_clientes WHERE dir_cli_id= NEW.dir_cli_id INTO telefono;\n            select nombre from clientes where cliente_id= new.cliente_id into cliente_nombre;\n            valores = new.folio || ','||new.importe_neto;\n            if (not :telefono is null) then\n            begin\n                INSERT INTO sic_mensajes_pendientes VALUES(-1,:TELEFONO,:cliente_nombre,'GRACIAS',:valores,null,0);\n            end\n          end\n        end\n    ", **kwargs)


def send_message():
    kwargs = {'user': user, 
       'password': password, 
       'database': database}
    messages = execute_sql('Select id,telefono,mensaje,cliente,intentos from SIC_MENSAJES_PENDIENTES where mensaje is not null', **kwargs)
    sms_masivo = SMSMasivo(apikey=apikey, pruebas=modo_pruebas)
    if messages:
        for message in messages:
            message_id = message[0]
            phone = message[1]
            phone = unicode(phone.encode('utf-8'), errors='ignore')
            phone = re.sub('[^0-9]', '', str(phone))
            customer_name = message[3]
            intentos = int(message[4])
            message = message[2].rstrip()
            if intentos > 10:
                kwargs['return_data'] = False
                execute_sql(('delete from SIC_MENSAJES_PENDIENTES where id =%s' % message_id), **kwargs)
                kwargs['return_data'] = True
                print 'Mensaje eliminado por mas de 10 intentos fallidos'
            else:
                kwargs['return_data'] = False
                execute_sql(('update SIC_MENSAJES_PENDIENTES set intentos=intentos+1 where id=%s ' % message_id), **kwargs)
                kwargs['return_data'] = True
                if len(phone) == 10:
                    resultado = sms_masivo.send(mensaje=message, telefono=phone)
                    if resultado['estatus'] == 'ok':
                        kwargs['return_data'] = False
                        execute_sql(('delete from SIC_MENSAJES_PENDIENTES where id =%s' % message_id), **kwargs)
                        print 'mensaje enviado '
                    else:
                        print resultado['mensaje']
                else:
                    print 'Numero Invalido de ' + customer_name


if not errror:
    checar_base_datos()
set_function_interval(send_message, 3)
for module in MODULES:
    module_name = module[0]
    module_reloadtime = module[1]
    try:
        module_config = importlib.import_module(module_name)
    except ImportError as exc:
        sys.stderr.write(('Error: failed to import settings module ({})').format(exc))
    else:
        kwargs = {'user': user, 
           'password': password, 
           'database': database, 
           'empresa_nombre': empresa_nombre}
        set_function_interval(module_config.generate_message, module_reloadtime, **kwargs)
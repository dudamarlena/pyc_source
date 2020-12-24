# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Docode\Desktop\Gimbow\DoCodeDB\procesos\dc_form.py
# Compiled at: 2020-02-17 12:49:29
# Size of source mod 2**32: 1258 bytes
import docode_managebd.procesos_bd as proc_bd

def dc_verificarform(request, model, spinner):
    _spinner = spinner
    fields_ = proc_bd.obtener_campos(model)
    fields_.pop(0)
    respuesta = {}
    respuesta = {'Error':'-1', 
     'mensaje':'', 
     'constraint':'', 
     'registro':None}
    if request.method == 'POST':
        try:
            respuesta = proc_bd.verificar_formulario(request, model)
        except Exception as e:
            try:
                pass
            finally:
                e = None
                del e

    registros = model.objects.all()
    object_name = model._meta.object_name
    appname = model._meta.app_label
    if _spinner == '' or _spinner == None:
        _spinner = 'Spinner.html'
    sub = {'appname':appname, 
     'object_name':object_name, 
     'respuesta':respuesta, 
     'registros':registros, 
     'campos':fields_, 
     'spinner_dc':_spinner}
    return sub
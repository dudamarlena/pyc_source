# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/api/upload.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 2929 bytes
import aiozmq, io
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config
from tempfile import NamedTemporaryFile
from xbus.file_emitter import FileEmitter
from xbus.file_emitter import FileEmitterException
from xbus.monitor.auth import get_logged_user_id
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import EmissionProfile

@view_config(route_name='upload', request_method='POST', renderer='json', http_cache=0)
def upload(request):
    """View to handle file uploads. They are sent to Xbus.
    """
    emission_profile_id = request.params.get('emission_profile_id')
    file = request.params.get('file')
    if not emission_profile_id or file is None:
        raise HTTPBadRequest(json_body={'error': 'No emission profile selected'})
    emission_profile = DBSession.query(EmissionProfile).filter(EmissionProfile.id == emission_profile_id).first()
    if not emission_profile:
        raise HTTPBadRequest(json_body={'error': 'Invalid emission profile'})
    if emission_profile.owner_id != get_logged_user_id(request):
        raise HTTPBadRequest(json_body={'error': 'Emission profile unauthorized'})
    descriptor = emission_profile.input_descriptor.descriptor.decode('utf-8')
    encoding = emission_profile.encoding
    front_url = request.registry.settings['xbus.broker.front.url']
    login = request.registry.settings['xbus.broker.front.login']
    password = request.registry.settings['xbus.broker.front.password']
    with NamedTemporaryFile(prefix='xbus-monitor-upload-') as (f_temp):
        while 1:
            buf = file.file.read(io.DEFAULT_BUFFER_SIZE)
            f_temp.write(buf)
            if len(buf) == 0:
                break

        f_temp.flush()
        f_temp_text = open(f_temp.name, 'r', newline='', encoding=encoding)
        zmq_loop = aiozmq.ZmqEventLoopPolicy().new_event_loop()
        try:
            emitter = FileEmitter(front_url, login, password, [descriptor], loop=zmq_loop)
            zmq_loop.run_until_complete(emitter.login())
            envelope_id = zmq_loop.run_until_complete(emitter.send_files([(f_temp_text, None)], encoding=encoding))
        except FileEmitterException as e:
            raise HTTPBadRequest(json_body={'error': str(e)})

    return {'envelope_id': envelope_id}
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/tests/test_bindgen.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 1098 bytes
from io import StringIO
import os.path
from jeepney.low_level import MessageType, HeaderFields
from jeepney.bindgen import code_from_xml
sample_file = os.path.join(os.path.dirname(__file__), 'secrets_introspect.xml')

def test_bindgen():
    with open(sample_file) as (f):
        xml = f.read()
    sio = StringIO()
    n_interfaces = code_from_xml(xml, path='/org/freedesktop/secrets', bus_name='org.freedesktop.secrets',
      fh=sio)
    if not n_interfaces == 2:
        raise AssertionError
    else:
        binding_ns = {}
        exec(sio.getvalue(), binding_ns)
        Service = binding_ns['Service']
        assert Service.interface == 'org.freedesktop.Secret.Service'
        msg = Service().SearchItems({'service':'foo',  'user':'bar'})
        assert msg.header.message_type is MessageType.method_call
        assert msg.header.fields[HeaderFields.destination] == 'org.freedesktop.secrets'
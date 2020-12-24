# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3d_sphinxext.py
# Compiled at: 2017-05-27 12:54:33
# Size of source mod 2**32: 1691 bytes
from sphinxcontrib.domaintools import custom_domain
import sphinxcontrib.domaintools

def get_objects(self):
    for (type, name), info in self.data['objects'].items():
        yield (
         name, name, type, info[0], info[1],
         self.object_types[type].attrs['searchprio'])


sphinxcontrib.domaintools.CustomDomain.get_objects = get_objects

def setup(app):
    app.add_domain(custom_domain('peng3dDomain', name='peng3d', label='Peng3d', elements=dict(event=dict(objname='peng3d Event', indextemplate='pair: %s; peng3d Event'), pgevent=dict(objname='peng3d Pyglet Event', indextemplate='pair: %s; peng3d Pyglet Event'))))
    return {'version': '1.0'}
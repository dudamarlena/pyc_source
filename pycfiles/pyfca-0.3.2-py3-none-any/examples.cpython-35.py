# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pyfc4/plugins/pcdm/examples.py
# Compiled at: 2018-11-07 08:34:49
# Size of source mod 2**32: 1514 bytes
from pyfc4 import models as _models
from pyfc4.plugins import pcdm

def create_pcdm_demo_resources(repo):
    colors = pcdm.models.PCDMCollection(repo, 'colors')
    colors.create(specify_uri=True)
    green = pcdm.models.PCDMObject(repo, 'green')
    green.create(specify_uri=True)
    yellow = pcdm.models.PCDMObject(repo, 'yellow')
    yellow.create(specify_uri=True)
    colors.members.extend([green.uri, yellow.uri])
    colors.update()
    green.related.append(yellow.uri)
    green.update()
    yellow.related.append(green.uri)
    yellow.update()
    spectrum_green = pcdm.models.PCDMFile(repo, 'green/files/spectrum_green', binary_data='540nm', binary_mimetype='text/plain')
    spectrum_green.create(specify_uri=True)
    spectrum_yellow = pcdm.models.PCDMFile(repo, 'spectrum_yellow', binary_data='570nm', binary_mimetype='text/plain')
    spectrum_yellow.create(specify_uri=True)
    spectrum_yellow.move(yellow.uri + '/files/spectrum_yellow')
    yellow.update()


def delete_pcdm_demo_resources(repo):
    for uri in ['colors', 'green', 'yellow']:
        try:
            repo.get_resource(uri).delete(remove_tombstone=True)
        except:
            print('could not remove: %s' % uri)
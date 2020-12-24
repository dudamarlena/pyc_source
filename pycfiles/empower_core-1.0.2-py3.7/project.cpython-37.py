# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/project.py
# Compiled at: 2020-05-10 06:48:26
# Size of source mod 2**32: 1939 bytes
"""Project Class."""
from importlib import import_module
from pymodm import fields
from empower_core.envmanager.env import Env
from empower_core.launcher import srv_or_die
from empower_core.serialize import serializable_dict
from empower_core.app import EApp

@serializable_dict
class Project(Env):
    __doc__ = 'Project class.\n\n    Attributes:\n        owner: The username of the user that requested this pool\n        desc: A human readable description of the project\n    '
    owner = fields.CharField(required=True)
    desc = fields.CharField(required=True)

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.manager = srv_or_die('projectsmanager')

    def load_service(self, service_id, name, params):
        """Load a service instance."""
        init_method = getattr(import_module(name), 'launch')
        service = init_method(context=self, service_id=service_id, **params)
        if not isinstance(service, EApp):
            raise ValueError('Service %s not EApp type' % name)
        return service

    def to_dict(self):
        output = super().to_dict()
        output['owner'] = self.owner
        output['desc'] = self.desc
        return output
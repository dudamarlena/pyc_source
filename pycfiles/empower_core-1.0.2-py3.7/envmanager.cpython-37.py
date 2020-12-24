# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/envmanager/envmanager.py
# Compiled at: 2020-05-10 08:04:22
# Size of source mod 2**32: 1724 bytes
"""Conf manager."""
import uuid
from empower_core.service import EService
from empower_core.envmanager.env import Env
from empower_core.envmanager.workercallbackshandler import WorkerCallbacksHandler
from empower_core.envmanager.workershandler import WorkersHandler
from empower_core.envmanager.cataloghandler import CatalogHandler
from empower_core.envmanager.envhandler import EnvHandler

class EnvManager(EService):
    __doc__ = 'Environment manager.'
    HANDLERS = [
     WorkersHandler, WorkerCallbacksHandler, CatalogHandler,
     EnvHandler]
    ENV_IMPL = Env
    env = None

    def start(self):
        super().start()
        if not self.ENV_IMPL.objects.all().count():
            self.ENV_IMPL(project_id=(uuid.uuid4())).save()
        self.env = self.ENV_IMPL.objects.first()
        self.env.start_services()

    @property
    def catalog(self):
        """Return available workers."""
        return dict()


def launch(context, service_id):
    """ Initialize the module. """
    return EnvManager(context=context, service_id=service_id)
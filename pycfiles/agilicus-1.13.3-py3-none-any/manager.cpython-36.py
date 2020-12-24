# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/manager.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 2171 bytes
import asyncio, os
from typing import Dict
import yaml
from jinja2 import Template
from . import utils
NAMESPACES = {
 'local', 'development', 'dev', 'stage', 'prod', 'sandbox', 'production'}

class Manager:

    def __init__(self, config=None, path=None, yes=False, namespace=None):
        self.config = config or {}
        self.path = path or os.getcwd()
        self.yes = yes
        self.message_brokers = []
        self.namespace = namespace
        self.init()

    def init(self) -> None:
        pass

    def get(self, name: str, DataClass: type) -> object:
        cfg = self.config.get(name) or {}
        return DataClass(**cfg)

    def message(self, msg: str) -> None:
        """Send a message to third party applications
        """
        for broker in self.message_brokers:
            try:
                broker(msg)
            except Exception as exc:
                utils.error(exc)

    def load_data(self, *paths: str, filename: str=None) -> Dict:
        filename = filename or (self.filename)(*paths)
        if not os.path.isfile(filename):
            raise utils.CommandError('%s file missing' % filename)
        with open(filename, 'r') as (fp):
            data = yaml.load(fp, Loader=(yaml.FullLoader)) or {}
        data_namespace = data.pop(self.namespace, None)
        for namespace in NAMESPACES:
            data.pop(namespace, None)

        if data_namespace:
            data.update(data_namespace)
        data['namespace'] = self.namespace
        return data

    def manifest(self, values, *paths, filename: str=None) -> Dict:
        """Load a manifest file and apply template values
        """
        filename = filename or (self.filename)(*paths)
        with open(filename, 'r') as (fp):
            template = Template(fp.read())
        return yaml.load((template.render(values)), Loader=(yaml.FullLoader))

    def filename(self, *paths) -> str:
        return (os.path.join)(self.path, *paths)

    def copy_env(self, *args, **kw):
        env = os.environ.copy()
        (env.update)(*args, **kw)
        return env

    def wait(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)
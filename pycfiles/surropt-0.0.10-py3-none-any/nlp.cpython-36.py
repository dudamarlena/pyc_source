# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Felipe\surropt\build\lib\surropt\core\options\nlp.py
# Compiled at: 2019-11-06 13:11:24
# Size of source mod 2**32: 2325 bytes
import requests
from requests.exceptions import ConnectionError
from abc import ABC

class NLPOptions(ABC):
    __doc__ = 'Base (abstract) class for setting the NLP solver options.\n\n    All the NLP solvers settings have to be handled through this class and \n    interfaced in the `optimize_nlp` function.\n    '

    @property
    def name(self):
        """The solver name."""
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError("'name' has to be a string.")

    def __init__(self, name: str):
        self.name = name


class DockerNLPOptions(NLPOptions):
    __doc__ = 'Solver options for when using IpOpt solver that is interfaced with a\n    flask application inside a Docker container or WSL enviroment.\n\n    Parameters\n    ----------\n    name : str\n        Custom name to the `NLPOptions` object (i.e. just a identifier, not \n        used as check anywhere else.)\n\n    server_url : str\n        Ip address of the docker server.\n    '

    @property
    def server_url(self):
        """Ip address of the docker server."""
        return self._server_url

    @server_url.setter
    def server_url(self, value):
        if isinstance(value, str):
            self._server_url = value
        else:
            raise ValueError("'server_url' has to be a string.")

    def __init__(self, name, server_url):
        super().__init__(name)
        self.server_url = server_url
        self.test_connection()

    def test_connection(self):
        try:
            response = requests.get(self.server_url)
        except ConnectionError:
            raise ValueError("Couldn't connect to the server URL provided. Make sure that the optimization server is online and communicating properly.")
        else:
            if response.status_code != 200:
                raise ValueError('Connection to the server established. However, the server is unresponsive.')
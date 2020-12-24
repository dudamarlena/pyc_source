# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/authenticate.py
# Compiled at: 2016-10-08 10:29:42
__doc__ = '\n*Authenticate against readability api*\n\n:Author:\n    David Young\n\n:Date Created:\n    September 28, 2015\n'
import sys, os
os.environ['TERM'] = 'vt100'
import readline, glob, pickle
from docopt import docopt
from fundamentals import tools, times

class authenticate:
    """
    *Authenticate against readability api*

    The parser api token is to be found in the polygot settings file (``~/.config/polygot/polygot.yaml``). 

    Read more about readability parser `here <https://www.readability.com/developers/api>`_, or to get your readability parser key sign up to readability and `grab the key here <https://www.readability.com/settings/account>`_

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup a readability parser client:

        .. code-block:: python 

            from polygot import authenticate
            parserClient = authenticate(
                log=log,
                settings=settings
            ).get() 
    """

    def __init__(self, log, settings=False):
        self.log = log
        log.debug("instansiating a new 'authenticate' object")
        self.settings = settings
        return

    def get(self):
        """
        *Get the readability parser client*

        **Return:**
            - ``parserClient`` -- the readability parser client
        """
        self.log.info('starting the ``get`` method')
        from readability import ParserClient
        os.environ['READABILITY_PARSER_TOKEN'] = self.settings['readability']['parser api token']
        parser_client = ParserClient()
        self.log.info('completed the ``get`` method')
        return parser_client
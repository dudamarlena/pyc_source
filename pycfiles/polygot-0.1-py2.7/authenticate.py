# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/polygot/authenticate.py
# Compiled at: 2016-10-08 10:29:42
"""
*Authenticate against readability api*

:Author:
    David Young

:Date Created:
    September 28, 2015
"""
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
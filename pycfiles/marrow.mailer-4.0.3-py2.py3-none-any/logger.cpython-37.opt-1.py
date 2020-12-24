# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/logger.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1617 bytes
import logging
from marrow.mailer import Mailer

class MailHandler(logging.Handler):
    __doc__ = "A class which sends records out via e-mail.\n    \n    This handler should be configured using the same configuration\n    directives that Marrow Mailer itself understands.\n    \n    Be careful how many notifications get sent.\n    \n    It is suggested to use background delivery using the 'dynamic' manager.\n    "

    def __init__(self, *args, **config):
        """Initialize the instance, optionally configuring TurboMail itself.
        
        If no additional arguments are supplied to the handler, re-use any
        existing running TurboMail configuration.
        
        To get around limitations of the INI parser, you can pass in a tuple
        of name, value pairs to populate the dictionary.  (Use `{}` dict
        notation in produciton, though.)
        """
        logging.Handler.__init__(self)
        self.config = dict()
        if args:
            config.update(dict(zip(*[iter(args)] * 2)))
        self.mailer = Mailer(config).start()
        self.config = config

    def emit(self, record):
        """Emit a record."""
        try:
            self.mailer.new(plain=(self.format(record))).send()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


logging.MailHandler = MailHandler
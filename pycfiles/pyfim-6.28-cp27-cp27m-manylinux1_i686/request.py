# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyfiltration/request.py
# Compiled at: 2015-11-14 06:09:33
import functools, logging
from tornado.options import options
from tornado.web import HTTPError
from common.filtration import Filtration
from common.exceptions import FiltrationException, ResponseHandlerException

def filtration_params(arg_key):
    """ filter request params
    :param string arg_key: self.get_validation_args() arg_key
    """

    def _filtration_params(method):

        @functools.wraps(method)
        def _wrapper(self, *args, **kwargs):
            all_params = self.get_validation_args()
            try:
                fparams = Filtration(all_params[arg_key], self).parse()
            except FiltrationException as e:
                logging.info(e.error)
                if e.error:
                    err_message = e.error
                else:
                    err_message = {'sys': '参数错误'}
                raise ResponseHandlerException(err_message)

            kwargs['fparams'] = fparams
            return method(self, *args, **kwargs)

        return _wrapper

    return _filtration_params
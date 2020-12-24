# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.5/site-packages/bankpassweb/result.py
# Compiled at: 2007-11-27 12:52:53


class Result(object):

    def __init__(self, code):
        self.code = code

    @classmethod
    def parse(cls, code):
        if int(code) == 0:
            return Success.parse(code)
        else:
            return Error.parse(code)


class Success(Result):

    @classmethod
    def parse(cls, code):
        if code == '00':
            return Success(code)

    def __init__(self, code):
        super(Success, self).__init__(code)
        assert int(code) == 0
        self.result = 'Successo'


class Error(Result):

    @classmethod
    def parse(self, code):
        for error_class in self.__subclasses__():
            try:
                if error_class.code == code:
                    return error_class(code)
            except AttributeError:
                pass

        return UnknownError(code)

    def __init__(self, code):
        super(Error, self).__init__(code)
        assert code == self.code
        assert int(code) > 0


class SystemDeniedError(Error):
    code = '01'
    result = 'Aut. negata dal sistema'


class ShopRecordError(Error):
    code = '02'
    result = 'Aut. negata per problemi su anag. negozio'


class AuthorizerDownError(Error):
    code = '03'
    result = 'Aut. negata per problemi di comunicazione con i circuiti autorizzativi'


class IssuerDenialError(Error):
    code = '04'
    result = 'Aut. negata dallemittente della carta'


class CardNumberError(Error):
    code = '05'
    result = 'Aut. negata per numero carta errato'


class OtherError(Error):
    code = '06'
    result = 'Errore imprevisto durante lelaborazione della richiesta'


class UnknownError(Error):

    def __init__(self, code):
        super(Error, self).__init__(code)
        self.result = 'Errore sconosciuto (%s)' % code
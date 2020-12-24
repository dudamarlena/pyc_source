# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/errors.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    PDB2PQR exceptions\n\n    This module represents errors specific to PDB2PQR. Exists mainly to allow\n    us to more easily distinguish between code errors and input errors. \n\n    Parsing utilities provided by Nathan A. Baker (Nathan.Baker@pnl.gov)\n    Pacific Northwest National Laboratory\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n    All rights reserved.\n\n    Redistribution and use in source and binary forms, with or without modification, \n    are permitted provided that the following conditions are met:\n\n        * Redistributions of source code must retain the above copyright notice, \n          this list of conditions and the following disclaimer.\n        * Redistributions in binary form must reproduce the above copyright notice, \n          this list of conditions and the following disclaimer in the documentation \n          and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n    IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n    OF THE POSSIBILITY OF SUCH DAMAGE.\n\n'
__date__ = '20 August 2012'
__author__ = 'Kyle Monson'
__version__ = '1.8'
import inspect

class PDB2PQRError(Exception):

    def __init__(self, message):
        self.message = message
        self.line = inspect.currentframe().f_back.f_lineno
        self.filename = inspect.currentframe().f_back.f_code.co_filename

    def __str__(self):
        return ('DEBUG INFO: {errorType} {filename}: {line} \nError encountered: {message}').format(message=self.message, errorType=self.__class__.__name__, line=self.line, filename=self.filename)


class PDBInternalError(PDB2PQRError):
    pass


class PDBInputError(PDB2PQRError):
    pass


class PDB2PKAError(PDB2PQRError):
    pass


class PDBFileParseError(PDB2PQRError):

    def __init__(self, lineno, errorStr):
        self.lineno = lineno
        self.errorStr = errorStr

    def __str__(self):
        return ('PDB file parsing error line {lineno}: {errorStr}').format(lineno=self.lineno, errorStr=self.errorStr)
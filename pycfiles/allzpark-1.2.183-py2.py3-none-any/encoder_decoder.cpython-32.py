# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/encoder_decoder.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 24, 2011\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the configurations for encoders and decoders.\n'
from ..ally_core.encoder_decoder import assemblyParsing, updateAssemblyParsing
from ally.container import ioc
from ally.core.http.impl.processor.parser.formdata import ParseFormDataHandler
from ally.core.http.impl.url_encoded import parseStr
from ally.core.impl.processor.parser.text import ParseTextHandler
from ally.design.processor.handler import Handler
import codecs

@ioc.config
def content_types_urlencoded() -> dict:
    """The URLEncoded content type"""
    return {'application/x-www-form-urlencoded': None}


@ioc.entity
def parseURLEncoded() -> Handler:

    def parseURLEncoded(content, charSet):
        return parseStr(codecs.getreader(charSet)(content).read())

    b = ParseTextHandler()
    yield b
    b.contentTypes = set(content_types_urlencoded())
    b.parser = parseURLEncoded
    b.parserName = 'urlencoded'


@ioc.entity
def parseFormData() -> Handler:
    b = ParseFormDataHandler()
    yield b
    b.contentTypeUrlEncoded = next(iter(content_types_urlencoded()))


@ioc.before(updateAssemblyParsing)
def updateAssemblyParsingFormData():
    assemblyParsing().add(parseFormData())
    assemblyParsing().add(parseURLEncoded())
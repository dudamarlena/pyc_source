# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/processor_babel.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Sep 14, 2012\n\n@package: ally core http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the configurations for the Babel conversion processor.\n'
from ..ally_core.processor import conversion, default_language, normalizer
from ..ally_core_http.processor import assemblyResources, updateAssemblyResources
from ..ally_http.processor import contentTypeResponseEncode
from ally.container import ioc
from ally.design.processor.handler import Handler
import logging
log = logging.getLogger(__name__)
try:
    import babel
except ImportError:
    log.info('No Babel library available, no Babel conversion')
else:
    babel = babel
    from ally.core.http.impl.processor.text_conversion import BabelConversionDecodeHandler, BabelConversionEncodeHandler

    @ioc.config
    def present_formatting():
        """
        If true will place on the response header the used formatting for conversion of data.
        """
        return True


    @ioc.replace(conversion)
    def conversionBabel() -> Handler:
        b = BabelConversionDecodeHandler()
        b.languageDefault = default_language()
        b.normalizer = normalizer()
        return b


    @ioc.entity
    def babelConversionEncode() -> Handler:
        return BabelConversionEncodeHandler()


    @ioc.after(updateAssemblyResources)
    def updateAssemblyResourcesForBabel():
        if present_formatting():
            assemblyResources().add(babelConversionEncode(), after=contentTypeResponseEncode())
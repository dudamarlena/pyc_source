# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/processor_time_zone.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Sep 14, 2012\n\n@package: ally core http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the configurations for the time zone conversion processor.\n'
from ..ally_core.processor import conversion
from ..ally_core_http.processor import assemblyResources, updateAssemblyResources
from ally.container import ioc
from ally.design.processor.handler import Handler
import logging
log = logging.getLogger(__name__)
try:
    import pytz
except ImportError:
    log.info('No pytz library available, no time zone conversion available')
else:
    pytz = pytz
    from ally.core.http.impl.processor.time_zone import TimeZoneHandler

    @ioc.config
    def base_time_zone():
        """
        The base time zone that the server date/time values are provided.
        """
        return 'UTC'


    @ioc.config
    def default_time_zone():
        """
        The default time zone if none is specified.
        """
        return 'UTC'


    @ioc.entity
    def timeZone() -> Handler:
        b = TimeZoneHandler()
        b.baseTimeZone = base_time_zone()
        b.defaultTimeZone = default_time_zone()
        return b


    @ioc.after(updateAssemblyResources)
    def updateAssemblyResourcesForTimeZone():
        assemblyResources().add(timeZone(), after=conversion())
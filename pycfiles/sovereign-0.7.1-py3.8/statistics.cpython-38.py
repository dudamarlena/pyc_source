# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/statistics.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 1937 bytes
import logging
from functools import wraps
from sovereign import config
try:
    from datadog import DogStatsd

    class CustomStatsd(DogStatsd):

        def _report(self, metric, metric_type, value, tags, sample_rate):
            super()._report(metric, metric_type, value, tags, sample_rate)
            stats.emitted[metric] = stats.emitted.setdefault(metric, 0) + 1


    statsd = CustomStatsd()
except ImportError:
    if config.statsd.enabled:
        raise
    statsd = None
else:

    class StatsDProxy:

        def __init__(self, statsd_instance=None):
            self.statsd = statsd_instance
            self.emitted = dict()

        def __getattr__--- This code section failed: ---

 L.  26         0  LOAD_FAST                'self'
                2  LOAD_ATTR                statsd
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L.  27        10  LOAD_GLOBAL              getattr
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                statsd
               16  LOAD_FAST                'item'
               18  CALL_FUNCTION_2       2  ''
               20  RETURN_VALUE     
             22_0  COME_FROM             8  '8'

 L.  28        22  SETUP_FINALLY        30  'to 30'

 L.  29        24  LOAD_GLOBAL              StatsdNoop
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY    22  '22'

 L.  30        30  DUP_TOP          
               32  LOAD_GLOBAL              TypeError
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    54  'to 54'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  31        44  LOAD_FAST                'self'
               46  LOAD_ATTR                do_nothing
               48  ROT_FOUR         
               50  POP_EXCEPT       
               52  RETURN_VALUE     
             54_0  COME_FROM            36  '36'
               54  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 40

        def do_nothing(self, *args, **kwargs):
            k = args[0]
            stats.emitted[k] = stats.emitted.setdefault(k, 0) + 1


    class StatsdNoop:

        def __init__(self, *args, **kwargs):
            k = args[0]
            stats.emitted[k] = stats.emitted.setdefault(k, 0) + 1

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            pass

        def __call__(self, func):

            @wraps(func)
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapped


    def configure_statsd(module):
        if config.statsd.enabled:
            module.host = config.statsd.host
            module.port = config.statsd.port
            module.namespace = config.statsd.namespace
            module.use_ms = config.statsd.use_ms
            for tag, value in config.statsd.loaded_tags.items():
                module.constant_tags.extend([f"{tag}:{value}"])

        else:
            module = None
            statsd_logger = logging.getLogger('datadog.dogstatsd')
            statsd_logger.disabled = True
        return StatsDProxy(module)


    stats = configure_statsd(module=statsd)
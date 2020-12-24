# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opentracing_utils/tracers.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 2178 bytes
import os, logging, opentracing
OPENTRACING_INSTANA = 'instana'
OPENTRACING_LIGHTSTEP = 'lightstep'
OPENTRACING_JAEGER = 'jaeger'
OPENTRACING_BASIC = 'basic'
logger = logging.getLogger(__name__)

def init_opentracing_tracer(tracer, **kwargs):
    if tracer == OPENTRACING_BASIC:
        from basictracer import BasicTracer
        recorder = kwargs.get('recorder')
        sampler = kwargs.get('sampler')
        opentracing.tracer = BasicTracer(recorder=recorder, sampler=sampler)
    else:
        if tracer == OPENTRACING_INSTANA:
            import instana
        else:
            if tracer == OPENTRACING_LIGHTSTEP:
                import lightstep
                component_name = kwargs.pop('component_name', os.environ.get('OPENTRACING_LIGHTSTEP_COMPONENT_NAME'))
                access_token = kwargs.pop('access_token', os.environ.get('OPENTRACING_LIGHTSTEP_ACCESS_TOKEN'))
                collector_host = kwargs.pop('collector_host', os.environ.get('OPENTRACING_LIGHTSTEP_COLLECTOR_HOST', 'collector.lightstep.com'))
                collector_port = kwargs.pop('collector_port', int(os.environ.get('OPENTRACING_LIGHTSTEP_COLLECTOR_PORT', 443)))
                verbosity = kwargs.pop('verbosity', int(os.environ.get('OPENTRACING_LIGHTSTEP_VERBOSITY', 0)))
                if not access_token:
                    logger.warning('Initializing LighStep tracer with no access_token!')
                opentracing.tracer = lightstep.Tracer(component_name=component_name, access_token=access_token, collector_host=collector_host, collector_port=collector_port, verbosity=verbosity, **kwargs)
            else:
                if tracer == OPENTRACING_JAEGER:
                    from jaeger_client import Config
                    service_name = kwargs.pop('service_name', os.environ.get('OPENTRACING_JAEGER_SERVICE_NAME'))
                    config = kwargs.pop('config', {})
                    jaeger_config = Config(config=config, service_name=service_name)
                    opentracing.tracer = jaeger_config.initialize_tracer()
                else:
                    opentracing.tracer = opentracing.Tracer()
    return opentracing.tracer
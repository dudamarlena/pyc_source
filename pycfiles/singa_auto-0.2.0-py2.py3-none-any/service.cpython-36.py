# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/utils/service.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 2386 bytes
import os, signal, traceback, logging
from datetime import datetime
from singa_auto.utils.log import configure_logging
logger = logging.getLogger(__name__)
curr_time = datetime.now().strftime('%d-%m-%Y_%I-%M-%S_%p')

def run_worker(meta_store, start_worker, stop_worker):
    service_id = os.environ['SINGA_AUTO_SERVICE_ID']
    service_type = os.environ['SINGA_AUTO_SERVICE_TYPE']
    container_id = os.environ.get('HOSTNAME', 'localhost')
    configure_logging('{}-ServiceID-{}-ContainerID-{}'.format(curr_time, service_id, container_id))

    def _sigterm_handler(_signo, _stack_frame):
        logger.warn('Terminal signal received: %s, %s' % (_signo, _stack_frame))
        stop_worker()
        exit(0)

    signal.signal(signal.SIGINT, _sigterm_handler)
    signal.signal(signal.SIGTERM, _sigterm_handler)
    with meta_store:
        service = meta_store.get_service(service_id)
        meta_store.mark_service_as_running(service)
    try:
        logger.info('Starting worker "{}" for service of ID "{}"...'.format(container_id, service_id))
        start_worker(service_id, service_type, container_id)
        logger.info('Stopping worker...')
        stop_worker()
    except Exception as e:
        logger.error('Error while running worker:')
        logger.error(traceback.format_exc())
        with meta_store:
            service = meta_store.get_service(service_id)
            meta_store.mark_service_as_errored(service)
        stop_worker()
        raise e
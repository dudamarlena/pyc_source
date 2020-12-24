# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/celery_tasks.py
# Compiled at: 2019-05-09 07:31:36
import ssl, os
from celery import Celery
from six.moves.urllib.parse import urlparse
from odcs.server import conf, db
from odcs.server.backend import generate_compose as backend_generate_compose, ComposerThread, RemoveExpiredComposesThread
from odcs.server.utils import retry
from odcs.server.models import Compose, COMPOSE_STATES
composer_thread = ComposerThread()
remove_expired_compose_thread = RemoveExpiredComposesThread()
if os.environ.get('ODCS_CELERY_BROKER_URL'):
    broker_url = os.environ['ODCS_CELERY_BROKER_URL']
elif conf.celery_broker_url:
    broker_url = conf.celery_broker_url
else:
    broker_url = 'amqp://localhost'
if broker_url.startswith('amqps://'):
    netloc = urlparse(broker_url).netloc
    host_port = netloc.split('@')[(-1)]
    host = host_port.split(':')[0]
    ssl_ctx = {}
    broker_use_ssl = {'server_hostname': host, 
       'context': {'purpose': ssl.Purpose.SERVER_AUTH}}
    conf.celery_config.update({'broker_use_ssl': broker_use_ssl})
    broker_url = broker_url.replace('amqps://', 'amqp://')
celery_app = Celery('backend', broker=broker_url)
celery_app.conf.update(conf.celery_config)
celery_app.conf.update({'task_routes': 'odcs.server.celery_tasks.TaskRouter'})

class TaskRouter:
    """ Custom Celery router """

    def __init__(self):
        self.config = conf.celery_router_config

    def route_for_task(self, task_name, *args, **kwargs):
        """
        Method which celery expects to be defined on a custom router. Returns the payload
        with the queue selected for task
        """
        if task_name == self.config['cleanup_task']:
            return {'queue': conf.celery_cleanup_queue}
        compose_id = args[0][0]
        compose = get_odcs_compose(compose_id)
        compose_md = compose.json()
        queue = self.__get_queue_for_compose(compose_md, task_name)
        return {'queue': queue}

    def __get_queue_for_compose(self, compose_md, task_name):
        """ Goes through routing rules configured for a task returns a queue on the first match. """
        rules = {}
        if self.config['routing_rules'].get(task_name):
            rules.update(self.config['routing_rules'][task_name])
        for queue, rule in rules.items():
            if rule:
                for key, value in rule.items():
                    if not compose_md.get(key):
                        raise ValueError('Task Router: Routing rule for queue %s for task %s contains an invalid property: %s' % (
                         queue, task_name, key))
                    if type(value) is list:
                        if compose_md[key] not in value:
                            break
                    elif compose_md[key] != value:
                        break
                else:
                    return queue

            else:
                return queue

        return self.config['default_queue']


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(600, run_cleanup.s())


@retry(wait_on=RuntimeError)
def get_odcs_compose(compose_id):
    """
    Gets the compose from ODCS DB.
    """
    compose = Compose.query.filter(Compose.id == compose_id).first()
    if not compose:
        raise RuntimeError('No compose with id %d in ODCS DB.' % compose_id)
    return compose


def generate_compose(compose_id):
    """
    Generates the compose with id `compose_id`.
    """
    compose = get_odcs_compose(compose_id)
    compose.transition(COMPOSE_STATES['generating'], 'Compose thread started')
    db.session.commit()
    backend_generate_compose(compose.id)


@celery_app.task
def generate_pungi_compose(compose_id):
    """
    Generates the Pungi based compose.
    """
    generate_compose(compose_id)


@celery_app.task
def generate_pulp_compose(compose_id):
    """
    Generates the Pungi based compose.
    """
    generate_compose(compose_id)


@celery_app.task
def run_cleanup():
    """
    Runs the cleanup.
    """
    remove_expired_compose_thread.do_work()
    composer_thread.fail_lost_generating_composes()
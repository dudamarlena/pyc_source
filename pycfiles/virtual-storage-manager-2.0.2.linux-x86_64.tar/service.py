# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/service.py
# Compiled at: 2016-06-13 14:11:03
"""Generic Node base class for all workers that run on hosts."""
import errno, inspect, os, random, signal, sys, time, eventlet, greenlet
from oslo.config import cfg
from vsm import context
from vsm import db
from vsm import exception
from vsm import flags
from vsm.openstack.common import importutils
from vsm.openstack.common import log as logging
from vsm.openstack.common import rpc
from vsm import utils
from vsm import version
from vsm import wsgi
LOG = logging.getLogger(__name__)
service_opts = [
 cfg.IntOpt('report_interval', default=10, help='seconds between nodes reporting state to datastore'),
 cfg.IntOpt('periodic_interval', default=60, help='seconds between running periodic tasks'),
 cfg.IntOpt('periodic_fuzzy_delay', default=60, help='range of seconds to randomly delay when starting the periodic task scheduler to reduce stampeding. (Disable by setting to 0)'),
 cfg.StrOpt('vsmapi_storage_listen', default='0.0.0.0', help='IP address for OpenStack Energy API to listen'),
 cfg.IntOpt('vsmapi_storage_listen_port', default=8778, help='port for os energy api to listen')]
FLAGS = flags.FLAGS
FLAGS.register_opts(service_opts)

class SignalExit(SystemExit):

    def __init__(self, signo, exccode=1):
        super(SignalExit, self).__init__(exccode)
        self.signo = signo


class Launcher(object):
    """Launch one or more services and wait for them to complete."""

    def __init__(self):
        """Initialize the service launcher.

        :returns: None

        """
        self._services = []

    @staticmethod
    def run_server(server):
        """Start and wait for a server to finish.

        :param service: Server to run and wait for.
        :returns: None

        """
        server.start()
        server.wait()

    def launch_server(self, server):
        """Load and start the given server.

        :param server: The server you would like to start.
        :returns: None

        """
        gt = eventlet.spawn(self.run_server, server)
        self._services.append(gt)

    def stop(self):
        """Stop all services which are currently running.

        :returns: None

        """
        for service in self._services:
            service.kill()

    def wait(self):
        """Waits until all services have been stopped, and then returns.

        :returns: None

        """

        def sigterm(sig, frame):
            LOG.audit(_('SIGTERM received'))
            raise KeyboardInterrupt

        signal.signal(signal.SIGTERM, sigterm)
        for service in self._services:
            try:
                service.wait()
            except greenlet.GreenletExit:
                pass


class ServerWrapper(object):

    def __init__(self, server, workers):
        self.server = server
        self.workers = workers
        self.children = set()
        self.forktimes = []


class ProcessLauncher(object):

    def __init__(self):
        self.children = {}
        self.sigcaught = None
        self.running = True
        rfd, self.writepipe = os.pipe()
        self.readpipe = eventlet.greenio.GreenPipe(rfd, 'r')
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        return

    def _handle_signal(self, signo, frame):
        self.sigcaught = signo
        self.running = False
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def _pipe_watcher(self):
        self.readpipe.read()
        LOG.info(_('Parent process has died unexpectedly, exiting'))
        sys.exit(1)

    def _child_process(self, server):

        def _sigterm(*args):
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            raise SignalExit(signal.SIGTERM)

        signal.signal(signal.SIGTERM, _sigterm)
        signal.signal(signal.SIGINT, _sigterm)
        eventlet.hubs.use_hub()
        os.close(self.writepipe)
        eventlet.spawn(self._pipe_watcher)
        random.seed()
        launcher = Launcher()
        launcher.run_server(server)

    def _start_child(self, wrap):
        if len(wrap.forktimes) > wrap.workers:
            if time.time() - wrap.forktimes[0] < wrap.workers:
                LOG.info(_('Forking too fast, sleeping'))
                time.sleep(1)
            wrap.forktimes.pop(0)
        wrap.forktimes.append(time.time())
        pid = os.fork()
        if pid == 0:
            status = 0
            try:
                try:
                    self._child_process(wrap.server)
                except SignalExit as exc:
                    signame = {signal.SIGTERM: 'SIGTERM', signal.SIGINT: 'SIGINT'}[exc.signo]
                    LOG.info(_('Caught %s, exiting'), signame)
                    status = exc.code
                except SystemExit as exc:
                    status = exc.code
                except BaseException:
                    LOG.exception(_('Unhandled exception'))
                    status = 2

            finally:
                wrap.server.stop()

            os._exit(status)
        LOG.info(_('Started child %d'), pid)
        wrap.children.add(pid)
        self.children[pid] = wrap
        return pid

    def launch_server(self, server, workers=1):
        wrap = ServerWrapper(server, workers)
        LOG.info(_('Starting %d workers'), wrap.workers)
        while self.running and len(wrap.children) < wrap.workers:
            self._start_child(wrap)

    def _wait_child(self):
        try:
            pid, status = os.waitpid(0, os.WNOHANG)
            if not pid:
                return
        except OSError as exc:
            if exc.errno not in (errno.EINTR, errno.ECHILD):
                raise
            return

        if os.WIFSIGNALED(status):
            sig = os.WTERMSIG(status)
            LOG.info(_('Child %(pid)d killed by signal %(sig)d'), locals())
        else:
            code = os.WEXITSTATUS(status)
            LOG.info(_('Child %(pid)d exited with status %(code)d'), locals())
        if pid not in self.children:
            LOG.warning(_('pid %d not in child list'), pid)
            return
        else:
            wrap = self.children.pop(pid)
            wrap.children.remove(pid)
            return wrap

    def wait(self):
        """Loop waiting on children to die and respawning as necessary."""
        while self.running:
            wrap = self._wait_child()
            if not wrap:
                eventlet.greenthread.sleep(0.01)
                continue
            while self.running and len(wrap.children) < wrap.workers:
                self._start_child(wrap)

        if self.sigcaught:
            signame = {signal.SIGTERM: 'SIGTERM', signal.SIGINT: 'SIGINT'}[self.sigcaught]
            LOG.info(_('Caught %s, stopping children'), signame)
        for pid in self.children:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError as exc:
                if exc.errno != errno.ESRCH:
                    raise

        if self.children:
            LOG.info(_('Waiting on %d children to exit'), len(self.children))
            while self.children:
                self._wait_child()


class Service(object):
    """Service object for binaries running on hosts.

    A service takes a manager and enables rpc by listening to queues based
    on topic. It also periodically runs tasks on the manager and reports
    it state to the database services table."""

    def __init__(self, host, binary, topic, manager, report_interval=None, periodic_interval=None, periodic_fuzzy_delay=None, service_name=None, *args, **kwargs):
        self.host = host
        self.binary = binary
        self.topic = topic
        self.manager_class_name = manager
        manager_class = importutils.import_class(self.manager_class_name)
        self.manager = manager_class(host=self.host, service_name=service_name, *args, **kwargs)
        self.report_interval = report_interval
        self.periodic_interval = periodic_interval
        self.periodic_fuzzy_delay = periodic_fuzzy_delay
        super(Service, self).__init__(*args, **kwargs)
        self.saved_args, self.saved_kwargs = args, kwargs
        self.timers = []

    def start(self):
        version_string = version.version_string()
        LOG.audit(_('Starting %(topic)s node (version %(version_string)s)'), {'topic': self.topic, 'version_string': version_string})
        self.manager.init_host()
        self.model_disconnected = False
        ctxt = context.get_admin_context()
        try:
            service_ref = db.service_get_by_args(ctxt, self.host, self.binary)
            self.service_id = service_ref['id']
        except exception.NotFound:
            self._create_service_ref(ctxt)

        self.conn = rpc.create_connection(new=True)
        LOG.debug(_('Creating Consumer connection for Service %s') % self.topic)
        rpc_dispatcher = self.manager.create_rpc_dispatcher()
        self.conn.create_consumer(self.topic, rpc_dispatcher, fanout=False)
        node_topic = '%s.%s' % (self.topic, self.host)
        self.conn.create_consumer(node_topic, rpc_dispatcher, fanout=False)
        self.conn.create_consumer(self.topic, rpc_dispatcher, fanout=True)
        self.conn.consume_in_thread()
        if self.report_interval:
            pulse = utils.LoopingCall(self.report_state)
            pulse.start(interval=self.report_interval, initial_delay=self.report_interval)
            self.timers.append(pulse)
        if self.periodic_interval:
            if self.periodic_fuzzy_delay:
                initial_delay = random.randint(0, self.periodic_fuzzy_delay)
            else:
                initial_delay = None
            periodic = utils.LoopingCall(self.periodic_tasks)
            periodic.start(interval=self.periodic_interval, initial_delay=initial_delay)
            self.timers.append(periodic)
        self.manager.insert_node_info_into_db()
        return

    def _create_service_ref(self, context):
        zone = FLAGS.storage_availability_zone
        service_ref = db.service_create(context, {'host': self.host, 'binary': self.binary, 
           'topic': self.topic, 
           'report_count': 0, 
           'availability_zone': zone})
        self.service_id = service_ref['id']

    def __getattr__(self, key):
        manager = self.__dict__.get('manager', None)
        return getattr(manager, key)

    @classmethod
    def create(cls, host=None, binary=None, topic=None, manager=None, report_interval=None, periodic_interval=None, periodic_fuzzy_delay=None, service_name=None):
        """Instantiates class and passes back application object.

        :param host: defaults to FLAGS.host
        :param binary: defaults to basename of executable
        :param topic: defaults to bin_name - 'vsm-' part
        :param manager: defaults to FLAGS.<topic>_manager
        :param report_interval: defaults to FLAGS.report_interval
        :param periodic_interval: defaults to FLAGS.periodic_interval
        :param periodic_fuzzy_delay: defaults to FLAGS.periodic_fuzzy_delay

        """
        if not host:
            host = FLAGS.host
        if not binary:
            binary = os.path.basename(inspect.stack()[(-1)][1])
        if not topic:
            topic = binary
        if not manager:
            subtopic = topic.rpartition('vsm-')[2]
            manager = FLAGS.get('%s_manager' % subtopic, None)
        if report_interval is None:
            report_interval = FLAGS.report_interval
        if periodic_interval is None:
            periodic_interval = FLAGS.periodic_interval
        if periodic_fuzzy_delay is None:
            periodic_fuzzy_delay = FLAGS.periodic_fuzzy_delay
        service_obj = cls(host, binary, topic, manager, report_interval=report_interval, periodic_interval=periodic_interval, periodic_fuzzy_delay=periodic_fuzzy_delay, service_name=service_name)
        return service_obj

    def kill(self):
        """Destroy the service object in the datastore."""
        self.stop()
        try:
            db.service_destroy(context.get_admin_context(), self.service_id)
        except exception.NotFound:
            LOG.warn(_('Service killed that has no database entry'))

    def stop(self):
        try:
            self.conn.close()
        except Exception:
            pass

        for x in self.timers:
            try:
                x.stop()
            except Exception:
                pass

        self.timers = []

    def wait(self):
        for x in self.timers:
            try:
                x.wait()
            except Exception:
                pass

    def periodic_tasks(self, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        ctxt = context.get_admin_context()
        self.manager.periodic_tasks(ctxt, raise_on_error=raise_on_error)

    def report_state(self):
        """Update the state of this service in the datastore."""
        ctxt = context.get_admin_context()
        zone = FLAGS.storage_availability_zone
        state_catalog = {}
        try:
            try:
                service_ref = db.service_get(ctxt, self.service_id)
            except exception.NotFound:
                LOG.debug(_('The service database object disappeared, Recreating it.'))
                self._create_service_ref(ctxt)
                service_ref = db.service_get(ctxt, self.service_id)

            state_catalog['report_count'] = service_ref['report_count'] + 1
            if zone != service_ref['availability_zone']:
                state_catalog['availability_zone'] = zone
            db.service_update(ctxt, self.service_id, state_catalog)
            if getattr(self, 'model_disconnected', False):
                self.model_disconnected = False
                LOG.error(_('Recovered model server connection!'))
        except Exception:
            if not getattr(self, 'model_disconnected', False):
                self.model_disconnected = True
                LOG.exception(_('model server went away'))


class WSGIService(object):
    """Provides ability to launch API from a 'paste' configuration."""

    def __init__(self, name, loader=None):
        """Initialize, but do not start the WSGI server.

        :param name: The name of the WSGI server given to the loader.
        :param loader: Loads the WSGI application using the given name.
        :returns: None

        """
        self.name = name
        self.manager = self._get_manager()
        self.loader = loader or wsgi.Loader()
        self.app = self.loader.load_app(name)
        self.host = getattr(FLAGS, '%s_listen' % name, '0.0.0.0')
        self.port = getattr(FLAGS, '%s_listen_port' % name, 0)
        self.server = wsgi.Server(name, self.app, host=self.host, port=self.port)

    def _get_manager(self):
        """Initialize a Manager object appropriate for this service.

        Use the service name to look up a Manager subclass from the
        configuration and initialize an instance. If no class name
        is configured, just return None.

        :returns: a Manager instance, or None.

        """
        fl = '%s_manager' % self.name
        if fl not in FLAGS:
            return
        else:
            manager_class_name = FLAGS.get(fl, None)
            if not manager_class_name:
                return
            manager_class = importutils.import_class(manager_class_name)
            return manager_class()

    def start(self):
        """Start serving this service using loaded configuration.

        Also, retrieve updated port number in case '0' was passed in, which
        indicates a random port should be used.

        :returns: None

        """
        if self.manager:
            self.manager.init_host()
        self.server.start()
        self.port = self.server.port

    def stop(self):
        """Stop serving this API.

        :returns: None

        """
        self.server.stop()

    def wait(self):
        """Wait for the service to stop serving this API.

        :returns: None

        """
        self.server.wait()


_launcher = None

def serve(*servers):
    global _launcher
    if not _launcher:
        _launcher = Launcher()
    for server in servers:
        _launcher.launch_server(server)


def wait():
    LOG.debug(_('Full set of FLAGS:'))
    for flag in FLAGS:
        flag_get = FLAGS.get(flag, None)
        if '_password' in flag or '_key' in flag or flag == 'sql_connection' and 'mysql:' in flag_get:
            LOG.debug(_('%(flag)s : FLAG SET ') % locals())
        else:
            LOG.debug('%(flag)s : %(flag_get)s' % locals())

    try:
        _launcher.wait()
    except KeyboardInterrupt:
        _launcher.stop()

    rpc.cleanup()
    return
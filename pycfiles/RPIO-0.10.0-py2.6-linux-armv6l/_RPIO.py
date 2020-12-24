# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/RPIO/_RPIO.py
# Compiled at: 2013-03-14 10:44:22
import socket, select, os.path, time, atexit
from logging import debug, info, warn, error
from threading import Thread
from functools import partial
import RPIO, RPIO._GPIO as _GPIO
_SYS_GPIO_ROOT = '/sys/class/gpio/'
_TCP_SOCKET_HOST = '0.0.0.0'
GPIO_FUNCTIONS = {0: 'OUTPUT', 1: 'INPUT', 4: 'ALT0', 7: '-'}
_PULL_UPDN = ('PUD_OFF', 'PUD_DOWN', 'PUD_UP')

def _threaded_callback(callback, *args):
    """
    Internal wrapper to start a callback in threaded mode. Using the
    daemon mode to not block the main thread from exiting.
    """
    t = Thread(target=callback, args=args)
    t.daemon = True
    t.start()


def exit_handler():
    """ Auto-cleanup on exit """
    RPIO.stop_waiting_for_interrupts()
    RPIO.cleanup_interrupts()


atexit.register(exit_handler)

class Interruptor:
    """
    Object-based wrapper for interrupt management.
    """
    _epoll = select.epoll()
    _show_warnings = True
    _map_fileno_to_file = {}
    _map_fileno_to_gpioid = {}
    _map_fileno_to_options = {}
    _map_gpioid_to_fileno = {}
    _map_gpioid_to_callbacks = {}
    _gpio_kernel_interfaces_created = []
    _tcp_client_sockets = {}
    _tcp_server_sockets = {}
    _is_waiting_for_interrupts = False

    def add_tcp_callback(self, port, callback, threaded_callback=False):
        """
        Adds a unix socket server callback, which will be invoked when values
        arrive from a connected socket client. The callback must accept two
        parameters, eg. ``def callback(socket, msg)``.
        """
        if not callback:
            raise AttributeError('No callback')
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((_TCP_SOCKET_HOST, port))
        serversocket.listen(1)
        serversocket.setblocking(0)
        self._epoll.register(serversocket.fileno(), select.EPOLLIN)
        cb = callback if not threaded_callback else partial(_threaded_callback, callback)
        self._tcp_server_sockets[serversocket.fileno()] = (
         serversocket, cb)
        debug('Socket server started at port %s and callback added.' % port)

    def add_interrupt_callback(self, gpio_id, callback, edge='both', pull_up_down=_GPIO.PUD_OFF, threaded_callback=False, debounce_timeout_ms=None):
        """
        Add a callback to be executed when the value on 'gpio_id' changes to
        the edge specified via the 'edge' parameter (default='both').

        `pull_up_down` can be set to `RPIO.PUD_UP`, `RPIO.PUD_DOWN`, and
        `RPIO.PUD_OFF`.

        If `threaded_callback` is True, the callback will be started
        inside a Thread.
        """
        gpio_id = _GPIO.channel_to_gpio(gpio_id)
        debug('Adding callback for GPIO %s' % gpio_id)
        if edge not in ('falling', 'rising', 'both', 'none'):
            raise AttributeError("'%s' is not a valid edge." % edge)
        if pull_up_down not in [_GPIO.PUD_UP, _GPIO.PUD_DOWN, _GPIO.PUD_OFF]:
            raise AttributeError("'%s' is not a valid pull_up_down." % edge)
        if gpio_id not in (RPIO.GPIO_LIST_R1 if _GPIO.RPI_REVISION == 1 else RPIO.GPIO_LIST_R2):
            raise AttributeError('GPIO %s is not a valid gpio-id.' % gpio_id)
        if RPIO.gpio_function(int(gpio_id)) == RPIO.IN:
            RPIO.set_pullupdn(gpio_id, pull_up_down)
        else:
            debug('- changing gpio function from %s to INPUT' % GPIO_FUNCTIONS[RPIO.gpio_function(int(gpio_id))])
            RPIO.setup(gpio_id, RPIO.IN, pull_up_down)
        cb = callback if not threaded_callback else partial(_threaded_callback, callback)
        path_gpio = '%sgpio%s/' % (_SYS_GPIO_ROOT, gpio_id)
        if gpio_id in self._map_gpioid_to_callbacks:
            with open(path_gpio + 'edge', 'r') as (f):
                e = f.read().strip()
                if e != edge:
                    raise AttributeError("Cannot add callback for gpio %s: edge detection '%s' not compatible with existing edge detection '%s'." % (
                     gpio_id, edge, e))
            debug('- kernel interface already setup for GPIO %s' % gpio_id)
            self._map_gpioid_to_callbacks[gpio_id].append(cb)
        else:
            if os.path.exists(path_gpio):
                if self._show_warnings:
                    warn('Kernel interface for GPIO %s already exists.' % gpio_id)
                debug('- unexporting kernel interface for GPIO %s' % gpio_id)
                with open(_SYS_GPIO_ROOT + 'unexport', 'w') as (f):
                    f.write('%s' % gpio_id)
                time.sleep(0.1)
            with open(_SYS_GPIO_ROOT + 'export', 'w') as (f):
                f.write('%s' % gpio_id)
            self._gpio_kernel_interfaces_created.append(gpio_id)
            debug('- kernel interface exported for GPIO %s' % gpio_id)
            with open(path_gpio + 'direction', 'w') as (f):
                f.write('in')
            with open(path_gpio + 'edge', 'w') as (f):
                f.write(edge)
            debug("- kernel interface configured for GPIO %s (edge='%s', pullupdn=%s)" % (
             gpio_id, edge,
             _PULL_UPDN[pull_up_down]))
            f = open(path_gpio + 'value', 'r')
            val_initial = f.read().strip()
            debug('- inital gpio value: %s' % val_initial)
            f.seek(0)
            self._map_fileno_to_file[f.fileno()] = f
            self._map_fileno_to_gpioid[f.fileno()] = gpio_id
            self._map_fileno_to_options[f.fileno()] = {'debounce_timeout_s': debounce_timeout_ms / 1000.0 if debounce_timeout_ms else 0, 
               'interrupt_last': 0, 
               'edge': edge}
            self._map_gpioid_to_fileno[gpio_id] = f.fileno()
            self._map_gpioid_to_callbacks[gpio_id] = [cb]
            self._epoll.register(f.fileno(), select.EPOLLPRI | select.EPOLLERR)

    def del_interrupt_callback(self, gpio_id):
        """ Delete all interrupt callbacks from a certain gpio """
        debug('- removing interrupts on gpio %s' % gpio_id)
        gpio_id = _GPIO.channel_to_gpio(gpio_id)
        fileno = self._map_gpioid_to_fileno[gpio_id]
        self._epoll.unregister(fileno)
        f = self._map_fileno_to_file[fileno]
        del self._map_fileno_to_file[fileno]
        del self._map_fileno_to_gpioid[fileno]
        del self._map_fileno_to_options[fileno]
        del self._map_gpioid_to_fileno[gpio_id]
        del self._map_gpioid_to_callbacks[gpio_id]
        f.close()

    def _handle_interrupt(self, fileno, val):
        """ Internally distributes interrupts to all attached callbacks """
        val = int(val)
        edge = self._map_fileno_to_options[fileno]['edge']
        if edge == 'rising' and val == 0 or edge == 'falling' and val == 1:
            return
        debounce = self._map_fileno_to_options[fileno]['debounce_timeout_s']
        if debounce:
            t = time.time()
            t_last = self._map_fileno_to_options[fileno]['interrupt_last']
            if t - t_last < debounce:
                debug("- don't start interrupt callback due to debouncing")
                return
            self._map_fileno_to_options[fileno]['interrupt_last'] = t
        gpio_id = self._map_fileno_to_gpioid[fileno]
        if gpio_id in self._map_gpioid_to_callbacks:
            for cb in self._map_gpioid_to_callbacks[gpio_id]:
                cb(gpio_id, val)

    def close_tcp_client(self, fileno):
        debug('closing client socket fd %s' % fileno)
        self._epoll.unregister(fileno)
        (socket, cb) = self._tcp_client_sockets[fileno]
        socket.close()
        del self._tcp_client_sockets[fileno]

    def wait_for_interrupts(self, epoll_timeout=1):
        """
        Blocking loop to listen for GPIO interrupts and distribute them to
        associated callbacks. epoll_timeout is an easy way to shutdown the
        blocking function. Per default the timeout is set to 1 second; if
        `_is_waiting_for_interrupts` is set to False the loop will exit.

        If an exception occurs while waiting for interrupts, the interrupt
        gpio interfaces will be cleaned up (/sys/class/gpio unexports). In
        this case all interrupts will be reset and you'd need to add the
        callbacks again before using `wait_for_interrupts(..)` again.
        """
        self._is_waiting_for_interrupts = True
        while self._is_waiting_for_interrupts:
            events = self._epoll.poll(epoll_timeout)
            for (fileno, event) in events:
                debug('- epoll event on fd %s: %s' % (fileno, event))
                if fileno in self._tcp_server_sockets:
                    (serversocket, cb) = self._tcp_server_sockets[fileno]
                    (connection, address) = serversocket.accept()
                    connection.setblocking(0)
                    f = connection.fileno()
                    self._epoll.register(f, select.EPOLLIN)
                    self._tcp_client_sockets[f] = (connection, cb)
                elif event & select.EPOLLIN:
                    (socket, cb) = self._tcp_client_sockets[fileno]
                    content = socket.recv(1024)
                    if not content or not content.strip():
                        self.close_tcp_client(fileno)
                    else:
                        (sock, cb) = self._tcp_client_sockets[fileno]
                        cb(self._tcp_client_sockets[fileno][0], content.strip())
                elif event & select.EPOLLHUP:
                    self.close_tcp_client(fileno)
                elif event & select.EPOLLPRI:
                    f = self._map_fileno_to_file[fileno]
                    val = f.read().strip()
                    f.seek(0)
                    self._handle_interrupt(fileno, val)

    def stop_waiting_for_interrupts(self):
        """
        Ends the blocking `wait_for_interrupts()` loop the next time it can,
        which depends on the `epoll_timeout` (per default its 1 second).
        """
        self._is_waiting_for_interrupts = False

    def cleanup_interfaces(self):
        """
        Removes all /sys/class/gpio/gpioN interfaces that this script created,
        and deletes callback bindings. Should be used after using interrupts.
        """
        debug('Cleaning up interfaces...')
        for gpio_id in self._gpio_kernel_interfaces_created:
            self.del_interrupt_callback(gpio_id)
            debug('- unexporting GPIO %s' % gpio_id)
            with open(_SYS_GPIO_ROOT + 'unexport', 'w') as (f):
                f.write('%s' % gpio_id)

        self._gpio_kernel_interfaces_created = []

    def cleanup_tcpsockets(self):
        """
        Closes all TCP connections and then the socket servers
        """
        for fileno in self._tcp_client_sockets.keys():
            self.close_tcp_client(fileno)

        for (fileno, items) in self._tcp_server_sockets.items():
            (socket, cb) = items
            debug('- _cleanup server socket connection (fd %s)' % fileno)
            self._epoll.unregister(fileno)
            socket.close()

        self._tcp_server_sockets = {}

    def cleanup_interrupts(self):
        """
        Clean up all interrupt-related sockets and interfaces. Recommended to
        use before exiting your program! After this you'll need to re-add the
        interrupt callbacks before waiting for interrupts again.
        """
        self.cleanup_tcpsockets()
        self.cleanup_interfaces()
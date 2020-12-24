# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/ssh.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 20476 bytes
import weakref, socket, os, os.path, paramiko, paramiko.rsakey, paramiko.ssh_exception, logging, shortuuid, re
from threading import Thread
from .sftp import Sftp
from . import Waitable
from .tunnel import Tunnel

class SshServer(Waitable):
    __doc__ = 'An SSH server using 20ft SDK calls.\n    Username/password are whatever you want.\n    Note that for the purposes of this, tunnels are regarded as processes because it makes loads of things simpler.\n\n    Do not instantiate directly, use container.create_ssh_server'

    def __init__(self, container, port):
        Waitable.__init__(self)
        self.uuid = shortuuid.uuid()
        self.container = weakref.ref(container)
        self.node = weakref.ref(container.parent())
        self.location = weakref.ref(self.node().parent())
        self.port = port
        self.run_thread = None
        self.stopping = False
        self.transports = {}
        host_key_fname = os.path.expanduser('~/.20ft/host_key')
        try:
            self.host_key = paramiko.RSAKey.from_private_key_file(host_key_fname)
        except FileNotFoundError:
            self.host_key = paramiko.rsakey.RSAKey.generate(1024)
            self.host_key.write_private_key_file(host_key_fname)

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.listen()
        logging.info('SSH server listening: ssh -p %s root@localhost' % self.port)

    def start(self):
        self.run_thread = Thread(target=(self.run), name=('SSH server onto: ' + self.container().uuid.decode()))
        self.run_thread.start()
        self.mark_as_ready()

    def stop(self):
        for transport in list(self.transports.values()):
            transport.stop()

        self.stopping = True
        self.run_thread.join()
        self.sock.close()

    def run(self):
        self.sock.settimeout(0.5)
        while not self.stopping:
            try:
                try:
                    client, addr = self.sock.accept()
                except socket.timeout:
                    continue

                transport = SshTransport(self, client, self.host_key)
                self.transports[transport.uuid] = transport
            except EOFError:
                raise ValueError("There was a problem with ssh - Is there an old key in 'known_hosts'?")

        logging.debug('Exiting server accept loop')

    def transport_closed(self, transport):
        logging.debug('SSH server knows transport has closed: ' + transport.uuid)
        del self.transports[transport.uuid]

    def __repr__(self):
        return "<SshServer '%s' container=%s port=%d>" % (
         self.uuid, self.container().uuid.decode(), self.port)


class SshTransport(paramiko.ServerInterface):
    __doc__ = 'A Transport is the per-client abstraction, it will spawn channels.'

    def __init__(self, parent, skt, host_key):
        self.uuid = shortuuid.uuid()
        self.parent = weakref.ref(parent)
        self.container = weakref.ref(parent.container())
        self.lead_channel = None
        self.socket = skt
        self.paramiko_transport = paramiko.Transport(skt)
        self.paramiko_transport.add_server_key(host_key)
        self.paramiko_transport.set_subsystem_handler('sftp', paramiko.SFTPServer, Sftp)
        self.paramiko_transport.start_server(server=self)
        self.channels = {}
        self.reverses = {}
        self.pending_tunnels = {}
        self.pending_reverses = []
        self.accept_thread = Thread(target=(self.channel_accept), name=('SSH transport: ' + self.uuid))
        self.accept_thread.start()

    def channel_accept(self):
        close_callback = self.stop
        while True:
            channel = self.paramiko_transport.accept()
            if channel is None:
                break
            chid = channel.get_id()
            logging.debug('Accepted paramiko channel: ' + str(chid))
            ssh_channel = SshChannel(channel, self.container(), close_callback)
            if close_callback is not None:
                self.lead_channel = ssh_channel
            self.channels[chid] = ssh_channel
            close_callback = None
            if chid in self.pending_tunnels:
                for port in self.pending_tunnels[chid]:
                    logging.debug('Spawning pending forward for port: ' + str(port))
                    ssh_channel.spawn_tunnel(port)

                del self.pending_tunnels[chid]
            for reverse in self.pending_reverses:
                try:
                    logging.debug('Hooking up pending reverse for port: ' + str(reverse.dest_addr[1]))
                    reverse.spawn_channel()
                    self.reverses[reverse.dest_addr[1]] = reverse
                except ValueError as e:
                    try:
                        logging.warning(e)
                    finally:
                        e = None
                        del e

            self.pending_reverses.clear()

        logging.debug('Transport loop exited for: ' + self.uuid)
        self.parent().transport_closed(self)

    def stop(self):
        if self.socket is None:
            return
        for reverse in list(self.reverses.values()):
            reverse.close()

        for channel in list(self.channels.values()):
            channel.close_callback = None
            channel.close()

        self.accept_thread.join()
        self.paramiko_transport.close()
        self.socket = None
        logging.debug('Transport closed for: ' + self.uuid)

    def check_auth_none(self, username):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'none'

    def check_channel_request(self, kind, chanid):
        logging.debug('SSH channel_request (%s): %d' % (kind, chanid))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_direct_tcpip_request(self, chanid, origin, destination):
        if chanid in self.channels:
            logging.info("SSH direct_tcpip_request received on open channel, just returning 'succeeded'")
        else:
            logging.info('SSH direct_tcpip_request waiting on port: ' + str(destination[1]))
            if chanid not in self.pending_tunnels:
                self.pending_tunnels[chanid] = []
            self.pending_tunnels[chanid].append(destination[1])
        return paramiko.OPEN_SUCCEEDED

    def check_port_forward_request(self, address, port):
        logging.info('SSH port_forward_request (reverse): %s:%d' % (address, port))
        self.pending_reverses.append(SshReverse((address, port), self.container(), self))
        return port

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        while channel.get_id() not in self.channels:
            os.sched_yield()

        self.channels[channel.get_id()].set_pty_dimensions(width, height)
        return True

    def check_channel_window_change_request(self, channel, width, height, pixelwidth, pixelheight):
        self.channels[channel.get_id()].set_pty_dimensions(width, height)
        self.channels[channel.get_id()].send_window_change()
        return True

    def check_channel_exec_request(self, channel, command):
        while channel.get_id() not in self.channels:
            os.sched_yield()

        return self.channels[channel.get_id()].spawn_process(command)

    def check_channel_shell_request(self, channel):
        while channel.get_id() not in self.channels:
            os.sched_yield()

        return self.channels[channel.get_id()].spawn_shell()


class SshChannel:
    __doc__ = 'A channel is a single channel through a transport. It can be connected to only one process.'

    def __init__(self, paramiko_channel, container, close_callback=None):
        self.paramiko_channel = paramiko_channel
        self.container = weakref.ref(container)
        self.connection = weakref.ref(container.conn())
        self.node = weakref.ref(container.parent())
        self.location = weakref.ref(self.node().parent())
        self.loop = weakref.ref(self.connection().loop)
        self.width = 80
        self.height = 24
        self.process = None
        self.close_callback = close_callback

    def close(self, obj=None, returncode=0):
        if self.paramiko_channel is None:
            return
        else:
            if self.close_callback is not None:
                logging.debug('Closing lead channel.')
                cc = self.close_callback
                self.close_callback = None
                cc()
                return
            chid = self.paramiko_channel.get_id()
            fd = self.paramiko_channel.fileno()
            logging.debug('[chan %d] closing' % chid)
            self.paramiko_channel.send_exit_status(returncode)
            self.paramiko_channel.shutdown(2)
            self.paramiko_channel.close()
            self.paramiko_channel = None
            if fd in self.loop().exclusive_handlers:
                self.loop().unregister_exclusive(fd)
            if self.process is not None:
                if self.process.uuid in self.location().tunnels:
                    del self.location().tunnels[self.process.uuid]
                if not self.process.dead:
                    self.process.destroy()

    def get_id(self):
        return self.paramiko_channel.get_id()

    def set_pty_dimensions(self, width, height):
        self.width = width
        self.height = height

    def send_window_change(self):
        self.connection().send_cmd(b'tty_window', {'node':self.node().pk,  'container':self.container().uuid, 
         'process':self.process.uuid, 
         'width':self.width, 
         'height':self.height})

    def spawn_process(self, command):
        self.process = self.container().spawn_process((command.decode()), data_callback=(self.data),
          stderr_callback=(self.stderr),
          termination_callback=(self.close))
        self.loop().register_exclusive((self.paramiko_channel.fileno()), (self.event), comment=('SSH Process ' + self.process.uuid.decode()))
        return True

    def spawn_shell(self):
        self.process = self.container().spawn_shell(data_callback=(self.data), termination_callback=(self.close),
          echo=True)
        self.loop().register_exclusive((self.paramiko_channel.fileno()), (self.event), comment=('SSH Shell ' + self.process.uuid.decode()))
        self.send_window_change()
        return True

    def spawn_tunnel(self, port):
        logging.debug('Spawning forwarding tunnel for port: ' + str(port))
        tunnel = Tunnel(self.connection(), self.node(), self.container(), port)
        tunnel.connect_tcpip_direct(self)
        self.process = tunnel
        self.location().tunnels[tunnel.uuid] = tunnel
        self.loop().register_exclusive((self.paramiko_channel.fileno()), (self.event), comment=('SSH Tunnel ' + self.process.uuid.decode()))

    def data(self, obj, data):
        try:
            self.paramiko_channel.sendall(data)
        except OSError:
            logging.debug('[chan %d] Failed to send: %s' % (self.paramiko_channel.get_id(), data.decode()))

    def stderr(self, obj, data):
        logging.debug('[chan %d - stderr] <== %s' % (self.paramiko_channel.get_id(), data.decode()))
        try:
            self.paramiko_channel.sendall_stderr(data)
        except OSError:
            logging.debug('[chan %d - stderr] Failed to send: %s' % (self.paramiko_channel.get_id(), data.decode()))

    def event(self, fd):
        while self.paramiko_channel.recv_ready():
            data = self.paramiko_channel.recv(8192)
            self.process.stdin(data)


class SshReverse:
    socat_re = re.compile(b'^\\d{4}/\\d{2}/\\d{2} \\d{2}:\\d{2}:\\d{2} socat')

    def __init__(self, dest_addr, container, transport):
        self.dest_addr = dest_addr
        self.container = weakref.ref(container)
        self.transport = weakref.ref(transport)
        self.process_channel = {}
        self.listening_process = self.spawn_socat()

    def spawn_socat(self):
        logging.debug('Spawning remote listener process for port: ' + str(self.dest_addr[1]))
        proc = 'socat -ls -d -d TCP4-LISTEN:%d,reuseaddr STDIO' % self.dest_addr[1]
        return self.container().spawn_process(proc, data_callback=(self.data),
          termination_callback=(self.terminated),
          stderr_callback=(self.stderr))

    def spawn_channel(self):
        if self.listening_process in self.process_channel:
            return
        if self.listening_process is None:
            self.fail_words('Cannot spawn channel because port is already being listened: ' + str(self.dest_addr[1]))
            return
        src_addr = (
         '127.0.0.1', self.dest_addr[1])
        try:
            p_channel = self.transport().paramiko_transport.open_forwarded_tcpip_channel(src_addr, self.dest_addr)
        except paramiko.ssh_exception.ChannelException:
            self.fail_words('Failed to connect reverse channel onto port: ' + str(self.dest_addr[1]))
            return
        else:
            channel = SshChannel(p_channel, self.container())
            try:
                channel.loop().register_exclusive((p_channel.fileno()), (channel.event),
                  comment=('SSH Reverse ' + self.listening_process.uuid.decode()))
            except RuntimeError:
                self.fail_words('Tried to register exclusive twice, closing channel: ' + str(p_channel.get_id()))
                channel.close(self, 1)
                return
            else:
                self.process_channel[self.listening_process] = channel
                channel.process = self.listening_process
                logging.debug('[chan %d] opened to port: %d' % (channel.get_id(), self.dest_addr[1]))
                return channel

    def terminated(self, process, returncode):
        logging.debug('SshReverse process terminated: %s (%d)' % (process.uuid.decode(), returncode))
        try:
            channel = self.process_channel[process]
            channel.close(process, returncode)
            del self.process_channel[process]
        except KeyError:
            logging.debug('...did not have an associated channel')

    def close(self):
        logging.debug('Closing processes for SSH reverse tunnel on port: ' + str(self.dest_addr[1]))
        for process in list(self.process_channel.keys()):
            process.destroy()

        if self.listening_process is not None:
            self.listening_process.destroy()

    def data(self, process, data):
        self.process_channel[process].data(process, data)

    def stderr(self, process, data):
        if SshReverse.socat_re.match(data) is None:
            self.process_channel[process].stderr(process, data)
            return
        logging.debug('(socat) ' + data.decode()[:-1])
        if b'accepting connection from' in data:
            self.spawn_channel()
            self.listening_process = self.spawn_socat()
            return
        if b'Address already in use' in data:
            self.fail_words('Cannot open forwarding channel, port is in use: ' + str(self.dest_addr[1]))
            return

    def fail_words(self, words):
        self.transport().lead_channel.stderr(self, words.encode() + b'\r\n')
        logging.warning(words)
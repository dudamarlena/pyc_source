# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nettools/sensor/sensor.py
# Compiled at: 2017-03-31 22:32:41
import datetime, logging, socket, signal, sys, threading, time, SocketServer
from optparse import OptionParser
DUMMY_LEN = 1024
DUMMY = '1' * DUMMY_LEN
KB = 1024
MB = KB * 1024
GB = MB * 1024
INTV = 2.0
OPT = {'server': False, 'client': False, 'port': 5001, 'connect_to': '127.0.0.1'}
latency = 0
latency_history = []
num_threads = 0
c_stat = {}
STOPPED = True

def reporter(tid, duration, bw, last=False):
    global latency
    global latency_history
    global num_threads
    if OPT['server'] == True:
        pass
    c_stat[tid] = [duration, bw]
    keys = c_stat.keys()
    keys.sort()
    if len(keys) == num_threads:
        output = ''
        sum_bw = 0
        for key in keys:
            v = c_stat[key]
            bw = v[1]
            sum_bw = sum_bw + bw
            f_bw, scale = getScaled(bw)
            output = output + ' +[Thread:%s]\t%10.4f %sbps\n' % (key, f_bw, scale)

        f_bw, scale = getScaled(sum_bw)
        dt = datetime.datetime.now()
        if last == True:
            avg_latency = 0
            for i in latency_history:
                avg_latency = avg_latency + i

            latency = avg_latency / len(latency_history)
            clientFooter()
            summary = '%s seconds\t%10.4f %sbps\t%10.4f' % (OPT['time'], f_bw, scale, latency)
        else:
            summary = '%s\t%10.4f %sbps\t%10.4f' % (dt.strftime('%H:%M:%S'), f_bw, scale, latency)
        print summary
        print output
        c_stat.clear()
        latency_history.append(latency)


def clientTitle():
    print '\n#################################################\nTime                Bandwidth       Latency(ms)\n-------------------------------------------------'


def clientFooter():
    print '\n------------ Summary ----------------------------'


def getScaled(bw):
    if bw > GB:
        f_bw = bw / GB
        scale = 'G'
    elif bw > MB:
        f_bw = bw / MB
        scale = 'M'
    elif bw > KB:
        f_bw = bw / KB
        scale = 'K'
    else:
        scale = ''
    return (
     f_bw, scale)


def report(tid, s0, s2, total, last=False):
    duration = s2 - s0
    bandwidth = total * 8 / duration
    reporter(tid, duration, bandwidth, last)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        logger.debug('[From Client]%s' % data)
        cur_thread = threading.current_thread()
        tid = cur_thread.ident
        response = ('{}: {}').format(cur_thread.name, data)
        cmd = self.parseCmd(data)
        cmd0 = cmd[0]
        if cmd0 == 'download':
            s0 = s2 = time.time()
            s1 = s0 + INTV
            s3 = s0 + int(cmd[1])
            total = 0
            prev_total = 0
            while s2 <= s3:
                self.request.sendall(DUMMY)
                s2 = time.time()
                if s2 >= s1:
                    report(tid, 0, INTV, total - prev_total)
                    s1 = s1 + INTV
                    prev_total = total
                total = total + DUMMY_LEN

            self.request.sendall('0')
            report(tid, s0, s2, total)
        elif cmd0 == 'echo':
            while True:
                reply = '%s|%f' % (data, time.time())
                logger.debug('ECHO reply=%s' % reply)
                self.request.sendall(reply)
                data = self.request.recv(128)
                if data[0] == '0':
                    break

            logger.info('End of ECHO Thread')
        else:
            logger.error('wrong request:%s' % cmd)

    def parseCmd(self, cmd):
        idx = cmd.split('|')
        ret = {}
        for i in range(len(idx)):
            ret[i] = idx[i]

        return ret


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def client_exit(thrs):
    global STOPPED
    print '\n'
    logger.critical('******************************')
    logger.critical('Force stop threads')
    logger.critical('******************************')
    print '\n'
    STOPPED = False
    sys.exit()


class ClientManager:

    def __init__(self, args):
        global num_threads
        self.threads = []
        self.num_threads = args['num_threads']
        ip = args['ip']
        port = args['port']
        cmd = args['cmd']
        num_threads = self.num_threads
        exit_handler = lambda signum, frame: client_exit(self.threads)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGQUIT, signal.SIG_IGN)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, exit_handler)
        signal.signal(signal.SIGTERM, exit_handler)
        signal.signal(signal.SIGQUIT, exit_handler)
        signal.signal(signal.SIGHUP, exit_handler)
        for i in range(self.num_threads):
            self.startClient(i, ip, port, cmd)

        t = threading.Thread(target=echoClient, args=(i + 1, ip, port, cmd))
        self.threads.append(t)
        t.start()

    def startClient(self, tid, ip, port, cmd):
        t = threading.Thread(target=tcpClient, args=(tid, ip, port, cmd))
        self.threads.append(t)
        t.start()


def tcpClient(tid, ip, port, cmd):
    logger.debug('TCP Client[%s] started' % tid)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        try:
            sock.sendall('download|%s' % cmd[1])
            CONT = True
            s0 = time.time()
            s1 = s0 + INTV
            total = 0
            prev_total = 0
            while CONT and STOPPED:
                res = sock.recv(1024)
                s2 = time.time()
                if s2 >= s1:
                    report(tid, 0, INTV, total - prev_total)
                    s1 = s1 + INTV
                    prev_total = total
                total = total + DUMMY_LEN
                if res[0] == '0':
                    CONT = False

            logger.debug('END of tcpClient Thread:%s' % tid)
        except:
            pass

    finally:
        s2 = time.time()
        report(tid, s0, s2, total, last=True)
        sock.close()


def echoClient(tid, ip, port, cmd):
    global latency
    logger.debug('TCP Echo Client[%s] stared' % tid)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    s0 = s1 = time.time()
    s3 = s0 + int(cmd[1])
    try:
        while s1 <= s3 and STOPPED:
            s1 = time.time()
            cmd = 'echo|%s' % s1
            sock.send(cmd)
            recv = sock.recv(128)
            s2 = time.time()
            latency = (s2 - s1) * 1000 / 2
            time.sleep(INTV)

    finally:
        sock.send('0')
        sock.close()


def cleanup_and_exit(server):
    logger.debug('Clean Up Thread')
    server.shutdown()
    server.server_close()
    sys.exit()


def runAsServer():
    logger.info('Running Server')
    server = None
    exit_handler = lambda signum, frame: cleanup_and_exit(server)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGQUIT, signal.SIG_IGN)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGQUIT, exit_handler)
    signal.signal(signal.SIGHUP, exit_handler)
    server = ThreadedTCPServer((HOST, OPT['port']), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.debug('Server loop running in thread:', server_thread.name)
    while True:
        time.sleep(5)

    return


def runAsClient():
    logger.debug('Running Client')
    cmd = {0: 'download', 1: OPT['time']}
    cargs = {'num_threads': OPT['parallel'], 'ip': OPT['connect_to'], 
       'port': OPT['port'], 
       'cmd': cmd}
    clientTitle()
    client = ClientManager(cargs)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s', '--server', dest='server', action='store_true', help='run in server mode')
    parser.add_option('-p', '--port', dest='port', default=5001, help='server port to listen on/connect to')
    parser.add_option('-c', '--client', dest='client', metavar='host', help='run in client mode, connect to <host>')
    parser.add_option('-t', '--time', dest='time', metavar='seconds', help='time in seconds to transmit for (default 10 secs)')
    parser.add_option('-P', '--parallel', dest='parallel', metavar='num', help='number of parallel client threads to run')
    parser.add_option('-L', '--logging', dest='logging', help='logging level(DEBUG|INFO|WARNING|ERROR|CRITICAL)')
    try:
        options, args = parser.parse_args()
        if options.logging:
            LEVEL = {}
            LEVEL['DEBUG'] = logging.DEBUG
            LEVEL['WARNING'] = logging.WARNING
            LEVEL['INFO'] = logging.INFO
            LEVEL['ERROR'] = logging.ERROR
            LEVEL['CRITICAL'] = logging.CRITICAL
            logging.basicConfig(format='%(levelname)s %(message)s', level=LEVEL[options.logging])
            logger = logging.getLogger('flywheel')
        else:
            logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)
            logger = logging.getLogger('flywheel')
        if options.server:
            OPT['server'] = True
        if options.client:
            OPT['client'] = True
            OPT['connect_to'] = options.client
        if options.port:
            OPT['port'] = int(options.port)
        if options.parallel:
            OPT['parallel'] = int(options.parallel)
        else:
            OPT['parallel'] = 1
        if options.time:
            OPT['time'] = int(options.time)
        else:
            OPT['time'] = 10
        HOST = ''
        if OPT['server']:
            runAsServer()
        if OPT['client']:
            runAsClient()
    except:
        sys.exit()
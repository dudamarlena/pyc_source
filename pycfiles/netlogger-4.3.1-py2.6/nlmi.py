# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/nlmi.py
# Compiled at: 2011-02-25 15:16:56
"""
NetLogger Machine Info library
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: nlmi.py 27244 2011-02-25 20:16:55Z dang $'
import array, fcntl, hashlib, os, socket, struct, sys, time, uuid, bson
from netlogger.nllog import get_logger, DoesLogging
SIOCGIFCONF = 35090
NLMI_VERSION = (0, 1)
SAMPLES_FLD = '_samples'
VERSION_FLD = 'version'
METAID_FLD = '_mid'
ID_FLD = '_id'
META_SECT = 'meta'
DATA_SECT = 'data'
BASE_ET = 'urn:nlmi'
CPU_ET = 'cpuinfo'

def get_hostname():
    """Get canonical host name.
    """
    return socket.getfqdn()


def get_all_interfaces(max_possible=128):
    max_bytes = max_possible * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd = sock.fileno()
    names = array.array('B', '\x00' * max_bytes)
    names_addr = names.buffer_info()[0]
    addresses = fcntl.ioctl(sockfd, SIOCGIFCONF, struct.pack('iL', max_bytes, names_addr))
    outbytes = struct.unpack('iL', addresses)[0]
    namestr = names.tostring()
    return [ namestr[i:i + 32].split('\x00', 1)[0] for i in range(0, outbytes, 32) ]


def get_net_dev(dirname=None, active=[], **ignore):
    """Input is format of /proc/net/dev on linux.

    Details: Parse second line in header so different fields can be understood:
      "face |bytes    packets errs drop fifo frame compressed multicast|       bytes    packets errs drop fifo colls carrier compressed"

    Args:
        dirname - Parent directory of net/dev (default=/proc)
        active - List of interfaces (usually, active ones) to include in results.
                 If falsy, all interfaces will be included, otherwise
                 only those listed will be included.

    Return: { interface : { event : value, .. } }
    """
    log = get_logger(__file__ + '.get_net_dev')
    log.info('start')
    if dirname is None:
        dirname = '/proc'
    filename = os.path.join(dirname, 'net', 'dev')
    result = {}
    iface_map = {}
    if active:
        iface_filter = dict.fromkeys(active)
    else:
        iface_filter = {}
    f = open(filename, 'r')
    f.readline()
    hdr = f.readline()
    (_, r, x) = hdr.split('|')
    value_fields = (('rcv', r.split()), ('snd', x.split()))
    for line in f:
        (iface, v) = line.split(':')
        iface = iface.strip()
        values = v.strip().split()
        if iface_filter and iface not in iface_filter:
            continue
        valuedict = {}
        now = time.time()
        for (i, (valtype, fields)) in enumerate(value_fields):
            for field in fields:
                strval = values[i]
                try:
                    value = int(strval)
                except ValueError:
                    value = float(strval)

                valuedict[field] = value

        result[iface] = valuedict

    log.info('end', status=0)
    return result


class HostInfo(DoesLogging):

    def __init__(self, dirname=None, **ignore):
        DoesLogging.__init__(self)
        assert dirname, 'Directory name is empty'
        if dirname is None:
            self._dir = '/proc'
        else:
            self._dir = dirname
        assert os.path.exists(dirname), 'Directory does not exist'
        self._prev_cpu_hz = {}
        self._prev_cpu_total_hz = {}
        return

    def get_info(self):
        """Get host information.
        
        Return: dict
        """
        self.log.info('start')
        result = {}
        f = open(os.path.join(self._dir, 'stat'), 'r')
        for line in f:
            fields = line.split()
            key = fields[0]
            v = map(int, fields[1:])
            if key.startswith('cpu'):
                if key == 'cpu':
                    cpu_label = CPU_ET
                else:
                    cpu_label = ('.').join((CPU_ET, key[3:]))
                cpudata = dict(zip(('user', 'nice', 'sys', 'idle'), v[0:4]))
                if len(v) >= 7:
                    cpudata.update(dict(zip(('iowait', 'irq', 'softirq'), v[4:7])))
                prev_values = self._prev_cpu_hz.get(cpu_label, {})
                prev_total = self._prev_cpu_total_hz.get(cpu_label, 0.0)
                total_hz = sum(v)
                total_elapsed_hz = total_hz - prev_total
                for (key, value) in cpudata.items():
                    prev = prev_values.get(key, 0.0)
                    elapsed_hz = value - prev
                    if total_elapsed_hz == 0:
                        cpudata[key] = 0.0
                    else:
                        cpudata[key] = 1.0 * elapsed_hz / total_elapsed_hz
                    prev_values[key] = value

                result[cpu_label] = cpudata
                self._prev_cpu_hz[cpu_label] = prev_values
                self._prev_cpu_total_hz[cpu_label] = total_hz

        self.log.info('end')
        return result


class MetaBlock:

    def __init__(self, parent=None, event_type=None, subject={}, params={}):
        self.ident = str(uuid.uuid1())
        self.parent = parent
        self.event_type = event_type
        self.subject = subject
        self.params = params

    def as_dict(self):
        d = {ID_FLD: self.ident, 'event_type': self.event_type, 
           'subject': self.subject, 
           'params': self.params}
        if self.parent:
            d['_pid'] = self.parent
        return d


class DataBlock:

    def __init__(self, event_type, meta=None):
        self.ident = str(uuid.uuid1())
        self.meta_id = str(meta.ident)
        self.event = event_type
        self.values = {}

    def add_named_values(self, timestamp, values):
        values.update({'_ts': timestamp})
        for key in values.keys():
            if not self.values.has_key(key):
                self.values[key] = []
            self.values[key].append(values[key])

    def as_dict(self):
        d = {ID_FLD: self.ident, METAID_FLD: self.meta_id, 
           'event_type': self.event, 
           'values': self.values}
        return d

    def set_sample_range(self, start, end):
        self.values[SAMPLES_FLD] = (
         start, end)


class Block:
    version = ('.').join(map(str, NLMI_VERSION))

    def __init__(self):
        self.meta = []
        self.data = []

    def clear(self):
        self.meta = []
        self.data = []

    def clear_data(self):
        self.data = []

    def as_dict(self):
        d = {VERSION_FLD: self.version, META_SECT: [ x.as_dict() for x in self.meta ], DATA_SECT: [ x.as_dict() for x in self.data ]}
        return d


def build_iface_meta(block, stats, **params):
    iface_meta = {}
    for iface in stats.keys():
        meta1 = MetaBlock(event_type='nlmi.interface', subject={'interface': iface})
        meta2 = MetaBlock(event_type='nlmi.timeseries', parent=meta1.ident, params=params)
        block.meta.append(meta1)
        block.meta.append(meta2)
        iface_meta[iface] = meta2

    return iface_meta


def __test():
    import pprint
    infile = None
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    t0 = time.time()
    delay = 1.0
    sampnum = 1
    iface_meta = {}
    etype = 'nlmi.net.dev'
    stats = get_net_dev(filename=infile)
    b = Block()
    iface_meta = build_meta(b, stats, ts=t0, dt=delay)
    for i in range(5):
        data = {}
        for j in range(3):
            for (iface, imeta) in iface_meta.iteritems():
                if iface not in data:
                    data[iface] = DataBlock(etype, meta=imeta)
                add_to_block(data[iface], stats[iface], sampnum)

            sampnum += 1

        for d in data.values():
            b.data.append(d)

        buf = pprint.pformat(b.as_dict()) + '\n'
        sys.stdout.write(buf)
        sys.stdout.flush()
        b = Block()

    return


if __name__ == '__main__':
    __test()
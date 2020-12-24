# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/burneronfire/__init__.py
# Compiled at: 2009-12-21 08:37:41
import sys, os, re, time, logging, threading
from optparse import OptionParser
from subprocess import Popen, PIPE
import gobject
from minihallib.HALManager import HALManager
from minihallib.HALDevice import HALDevice
from minihallib.HALWrapper import HALWrapper
from burneronfire.utils import *
BURN_PROCESS_REGEX = re.compile('(\\d+)\\s+of\\s+(\\d+)\\s+MB\\s+written')
try:
    HAS_GTK = True
    from burneronfire.gui import BurnerOnFireGTK
except ImportError:
    HAS_GTK = False

__version__ = 0.1
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
ch = logging.StreamHandler()
if int(os.environ.get('BOF_DEBUG', '0')) == 1:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)

class BurnerOnFire(object):
    """Blank CD poller"""

    def __init__(self, options, gui_app=None, limit=0):
        self.capability = 'volume.disc'
        self.property_modified_cb = self.my_cb
        self.receiver = self.my_receiver
        self.options = options
        self.gui_app = gui_app
        self.limit = limit

    def start(self):
        wrapper = HALWrapper()
        wrapper.register(self)
        log.info('Starting! Begin inserting empty discs.')
        wrapper.start()
        discs = get_hal_devices('volume.disc')
        discs = filter(lambda d: d.get('volume.disc.is_blank'), discs)
        for disc in discs:
            self.start_worker(disc, HALDevice(disc.get_parent()))

        return wrapper

    def start_worker(self, device, burner_device):
        if not device.get('volume.disc.is_blank'):
            return
        else:
            dev_path = burner_device.get('block.device')
            burner_name = burner_device.get('info.product')
            worker = Worker(dev_path, burner_name, options=self.options, limit=self.limit)
            disc_type = device.get('volume.disc.type')
            if disc_type == 'unknown':
                log.info('Media type in burner %(dev_path)s is unknown, proceeding anyway...' % locals())
            else:
                media_type = disc_type_to_media_type(disc_type)
                if media_type is False or not burner_device.get('storage.cdrom.%s' % media_type):
                    log.info('Media type %(disc_type)s is not supported by burner %(dev_path)s' % locals())
                    if self.gui_app is not None:
                        self.gui_app.statusw.alter_status_column(worker, 'Disc type not supported: %s' % disc_type)
                    return
            Worker.num_possible_burned_discs_lock.acquire()
            if self.limit != 0 and Worker.NUM_POSSIBLE_BURNED_DISCS >= self.limit:
                log.info('Burner %(dev_path)s stopped, disc limit already reached.' % locals())
                if self.gui_app is not None:
                    self.gui_app.statusw.alter_status_column(worker, 'Limit reached, burning not started.')
                return
            Worker.NUM_POSSIBLE_BURNED_DISCS += 1
            Worker.num_possible_burned_discs_lock.release()
            if self.gui_app is not None:
                worker.connect('started', self.gui_app.statusw.alter_status_column, 'Burning...')
                worker.connect('ended', self.gui_app.statusw.alter_status_column, 'Idle (100% done)')
                worker.connect('error', self.gui_app.statusw.alter_status_column, 'Error (check error log)')
                worker.connect('warning', self.gui_app.statusw.alter_status_column, 'Idle (100% done with warnings)')
                worker.connect('changed-num-of-burned-discs', self.gui_app.statusw.alter_burned_discs)
                worker.connect('progress-changed', self.gui_app.statusw.update_progressbar)
            log.info('Empty disc inserted in burner %s', burner_name)
            log.debug('dev_path of burner: %s', dev_path)
            worker.start()
            return

    def quit(self):
        pass

    def my_cb(self, hal_device, name, modified):
        log.debug('HALDevice: %s, name: %s, modified: %s', hal_device, name, modified)

    def my_receiver(self, packet):
        """Called when device property is changed, invokes start_worker"""
        (msg, device) = packet
        log.debug('HALDevice: %s, msg: %s', device, msg)
        if msg == 'device added':
            burner = device.get_parent()
            burner_device = HALDevice(burner)
            self.start_worker(device, burner_device)


class Worker(threading.Thread, gobject.GObject):
    __gsignals__ = {'started': (
                 gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()), 
       'error': (
               gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()), 
       'ended': (
               gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()), 
       'warning': (
                 gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()), 
       'changed-num-of-burned-discs': (
                                     gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()), 
       'progress-changed': (
                          gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}
    num_burned_discs_lock = threading.Lock()
    num_possible_burned_discs_lock = threading.Lock()
    NUM_BURNED_DISCS = 0
    NUM_POSSIBLE_BURNED_DISCS = 0

    def __init__(self, dev_path, burner_name, options, limit):
        super(Worker, self).__init__()
        self.__gobject_init__()
        self.dev_path = dev_path
        self.burner_name = burner_name
        self.options = options
        self.limit = limit

    def run(self):
        args = [
         'wodim',
         'dev=%s' % self.dev_path,
         'fs=14M',
         '-eject',
         '-overburn',
         '-v'] + self.options
        self.emit('started')
        log.info('Burning... %s', (' ').join(args))
        p = Popen(args, stdout=PIPE, stderr=PIPE)
        while p.poll() == None:
            output = p.stdout.readline(50)
            hit = BURN_PROCESS_REGEX.search(output)
            if hit:
                (done, total) = hit.groups()
                percent = int(int(done) / float(total) * 100)
                log.debug('Progress of %s is %s%% completed.', self.dev_path, percent)
                self.emit('progress-changed', percent)

        self.emit('progress-changed', 0)
        stdout_filename = get_logfile_from_burner_name(self.burner_name, self.dev_path)
        stderr_filename = get_logfile_from_burner_name(self.burner_name, self.dev_path, err=True)
        self.append_file(stdout_filename, p.stdout.read())
        if p.stderr:
            stderr = p.stderr.read()
            self.append_file(stderr_filename, stderr)
        if p.returncode is not 0:
            Worker.num_possible_burned_discs_lock.acquire()
            Worker.NUM_POSSIBLE_BURNED_DISCS -= 1
            Worker.num_possible_burned_discs_lock.release()
            if p.stderr:
                log.error(stderr)
            self.emit('error')
            log.error('Burner %s emited an error, burning not completed!', self.burner_name)
        else:
            if p.stderr:
                log.warning(stderr)
                self.emit('warning')
                log.info('Burner %s 100%% completed with warnings!', self.burner_name)
            else:
                self.emit('ended')
                log.info('Burner %s 100%% completed!', self.burner_name)
            Worker.num_burned_discs_lock.acquire()
            Worker.NUM_BURNED_DISCS += 1
            if Worker.NUM_BURNED_DISCS == self.limit:
                log.info('%d of %d discs burned. You may now quit BurnerOnFire.' % (
                 Worker.NUM_BURNED_DISCS, self.limit))
            Worker.num_burned_discs_lock.release()
            self.emit('changed-num-of-burned-discs')
        return

    def append_file(self, filename, data):
        f = open(filename, 'w+')
        f.write(data)
        f.close()


gobject.type_register(Worker)

def main():
    usage = '%prog -s [write speed] -f [filename/path to filename] -m [burnmode] -l [limit]\n    \n    If no filename is given, GKT+ GUI will start.\n    '
    parser = OptionParser(usage)
    parser.add_option('-f', '--filename', dest='filename', help='specify which file to burn')
    parser.add_option('-s', '--speed', dest='burnspeed', default='16', type='int', help='specify burning speed (default is 16)')
    parser.add_option('-m', '--mode', dest='burnmode', default='-dao', help='provide write mode (defaults to DAO)')
    parser.add_option('-l', '--limit', dest='limit', default='0', type='int', help='number of discs to burn (defaults to 0, which means unlimited)')
    (options, args) = parser.parse_args()
    if not options.filename:
        if not HAS_GTK:
            raise ImportError('You need to install GTK+ modules')
        base = BurnerOnFireGTK(args)
        return base.main()
    if not os.path.isfile(options.filename):
        parser.error('Specified file (%s) does not exist!' % options.filename)
    args.append(options.burnmode)
    args.append('speed=%d' % options.burnspeed)
    args.append(options.filename)
    bof = BurnerOnFire(args, limit=options.limit)
    wrapper = bof.start()
    try:
        while IS_LOOPING:
            time.sleep(0.5)

        wrapper.stop()
    except KeyboardInterrupt:
        wrapper.stop()


if __name__ == '__main__':
    main()
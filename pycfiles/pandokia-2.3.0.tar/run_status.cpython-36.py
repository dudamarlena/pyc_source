# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/run_status.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 12650 bytes
import ast, datetime, mmap, os, platform, sys, time
mem = None
test_mode = None
if test_mode:
    saw_locked = 0
    saw_changed = 0
if platform.system() == 'Windows':

    def init_status(*l, **kw):
        pass


    def pdkrun_status(*l, **kw):
        pass


    def display(*l, **kw):
        pass


    def display_interactive(*l, **kw):
        pass


else:

    def init_status(filename=None, n_records=10, status_text_size=2000):
        """Create a status file with n_records blank records in it
        """
        valid_flag_size = 1
        if filename is None:
            filename = os.getcwd() + '/pdk_statusfile'
            try:
                os.unlink(filename)
            except:
                pass

        with open(filename, 'w') as (fp):

            def gen_header():
                s = '********PDKRUN status monitor 000\n%08d %d %d %d\n' % (
                 header_size, status_text_size, n_records, valid_flag_size)
                return s

            header_size = 0
            header = gen_header()
            header_size = len(header)
            header = gen_header()
            assert header_size == len(header)
            fp.write(('%08x' % int(time.time()))[0:8])
            fp.write(header[8:])
            for x in range(n_records):
                fp.write(' ' * (valid_flag_size + status_text_size))
                fp.write('\n')

        return filename


    class status_block(object):

        def __init__(self, filename, mode):
            if mode == 'w':
                mode = 'r+b'
                prot = mmap.PROT_READ | mmap.PROT_WRITE
            else:
                mode = 'rb'
                prot = mmap.PROT_READ
            with open(filename, mode) as (fp):
                for lineno, record in enumerate(fp):
                    record = record.decode()
                    if lineno == 0:
                        if record[8:] != 'PDKRUN status monitor 000\n':
                            raise Exception('Not a PDKRUN status monitor file: %s' % filename)
                        else:
                            if lineno == 1:
                                header = record.strip().split(' ')

                self._fd = os.dup(fp.fileno())
            self.header_size = int(header[0])
            self.status_text_size = int(header[1])
            self.n_records = int(header[2])
            self.valid_flag_size = int(header[3])
            self.record_size = self.valid_flag_size + self.status_text_size + 1
            self.status_text_offset = self.valid_flag_size
            self.locked_valid_flag = 'X' * self.valid_flag_size
            self.file_size = self.record_size * self.n_records + self.header_size
            self.mem = mmap.mmap(fileno=(self._fd),
              length=(self.file_size),
              flags=(mmap.MAP_SHARED),
              prot=prot)
            self.header_timestamp = self.mem[0:8]

        def header_changed(self):
            return self.mem[0:8] != self.header_timestamp

        def get_status_text(self, n):
            return self.get_value_at_offset(n, self.status_text_offset, self.status_text_size)

        def get_value_at_offset(self, n, offset, len):
            global saw_changed
            global saw_locked
            start = self.header_size + n * self.record_size
            flag = self.mem[start:start + self.valid_flag_size]
            if flag == self.locked_valid_flag:
                if test_mode:
                    if test_mode == 'L':
                        saw_locked += 1
                        return 'locked'
                return
            else:
                s = self.mem[start + offset:start + offset + len]
                if flag != self.mem[start:start + self.valid_flag_size]:
                    if test_mode and test_mode == 'C':
                        saw_changed += 1
                        return 'changed'
                    else:
                        return
                return s

        def set_my_record(self, n):
            if n >= self.n_records:
                raise Exception('only %d records in file - using #%d\n' % (
                 self.n_records, n))
            self.my_record = n
            self.my_record_offset = self.header_size + n * self.record_size

        def set_status_text(self, value):
            return self.set_value_at_offset(self.status_text_offset, self.status_text_size, value)

        def set_value_at_offset(self, offset, blocklen, value):
            start = self.my_record_offset
            old_valid_flag = self.mem[start:start + self.valid_flag_size]
            try:
                self.mem[start:start + self.valid_flag_size] = self.locked_valid_flag
            except TypeError:
                self.mem[start:start + self.valid_flag_size] = bytes(self.locked_valid_flag, 'ascii')

            if len(value) < blocklen:
                value = value + ' ' * (blocklen - len(value) + 1)
            value = value[0:blocklen]
            try:
                s = self.mem[start + offset:start + offset + blocklen] = value
            except TypeError:
                s = self.mem[start + offset:start + offset + blocklen] = bytes(value, 'ascii')

            try:
                n = int(old_valid_flag) + 1 & 7
            except:
                n = 0

            try:
                self.mem[start:start + self.valid_flag_size] = '%*d' % (self.valid_flag_size, n)
            except TypeError:
                self.mem[start:start + self.valid_flag_size] = bytes('%*d' % (
                 self.valid_flag_size,
                 n), 'ascii')


    if __name__ == '__main__':
        s = sys.stdin.readline().strip()
        if s == 'i':
            init_status('pdk_statusfile', 10)
            s = 'w'
        if s == 's':
            m = status_block('pdk_statusfile')
            m.set_my_record(1)
            for x in range(0, 10000000):
                m.set_status_text('%d' % x)

        else:
            m = status_block('pdk_statusfile')
            m.set_my_record(int(s))
            while 1:
                print('>')
                l = sys.stdin.readline().strip()
                if l[0] in '0123456789':
                    n = int(l.split()[0])
                    m.set_my_record(n)
                else:
                    if l[0] == 's':
                        m.set_status_text(l[1:])
                    else:
                        print('?')

    def pdkrun_status(text, slot=None):
        """A status setting function for use within pdkrun

        You call pdkrun_status( text ) to set your status

        slot is the slot number to note the status in (default is PDK_PROCESS_SLOT environment)
        """
        global mem
        if 'PDK_STATUSFILE' not in os.environ:
            return
        else:
            if os.environ['PDK_STATUSFILE'] == 'none':
                return
            if slot is None:
                if 'PDK_PROCESS_SLOT' in os.environ:
                    slot = int(os.environ['PDK_PROCESS_SLOT'])
                else:
                    slot = 0
            if mem is None:
                mem = status_block(os.environ['PDK_STATUSFILE'], 'w')
                mem.set_my_record(slot)
        mem.set_status_text(repr(text) + ',%d' % time.time())


    def display(visual, waiting_for_start):
        filename = 'pdk_statusfile'
        done_waiting = not waiting_for_start
        if waiting_for_start:
            while not os.path.exists(filename):
                time.sleep(1)

        m = status_block(filename, 'r')
        times = {}
        while True:
            if visual:
                sys.stdout.write('\x1b[H\x1b[J')
            elif m.header_changed():
                m = status_block(filename, 'r')
                done_waiting = not waiting_for_start
            else:
                any = 0
                for x in range(0, m.n_records):
                    s = m.get_status_text(x)
                    if s is None:
                        sys.stdout.write('-')
                    else:
                        try:
                            text, tyme = ast.literal_eval(s)
                        except SyntaxError:
                            text = str(s).strip()
                            tyme = 'None'
                        else:
                            if tyme not in times:
                                times = {}
                                times[tyme] = str(datetime.datetime.fromtimestamp(tyme))
                            tyme = times[tyme]
                            text = str(text).strip()
                            if text != '':
                                any = 1
                                done_waiting = 1
                            sys.stdout.write('%2d %s %s' % (x, tyme, text))
                    if visual:
                        sys.stdout.write('\x1b[K')
                    sys.stdout.write('\n')

                if test_mode:
                    sys.stdout.write('%d %d %d\n' % (
                     time.time(), saw_locked, saw_changed))
                if not visual:
                    break
                if not any:
                    if done_waiting:
                        break
            time.sleep(1)


    def display_interactive(args):
        display(1, 1)
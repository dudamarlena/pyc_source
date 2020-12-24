# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/v9_parser.py
# Compiled at: 2019-08-04 12:24:18
# Size of source mod 2**32: 6822 bytes
import logging, struct, sys
from flowproc import v9_state
logger = logging.getLogger(__name__)
fmt1 = logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)s: %(message)s')
fmt2 = logging.Formatter('%(levelname)-8s %(message)s')
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(fmt2)
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)
LIM = 1800
lim = LIM

def parse_data_flowset(tid, packed):
    """
    Responsibility: parse Data FlowSets

    Args:
        tid         `int`: the setid here IS the tid (aka Template ID)
        packed      `bytes`: data to parse

    Return:
        number of records processed
    """
    record_count = 0
    try:
        template = v9_state.Template.get(tid)
        if isinstance(template, v9_state.OptionsTemplate):
            logger.debug('OT {} {} {}'.format(template.scopelen, template.optionlen, template.types))
        else:
            logger.debug('T  {} {}'.format(tid, template.types))
        reclen = sum(template.lengths)
        record_count = len(packed) // reclen
    except KeyError:
        logger.warning('No template, discarding Data FlowSet ID {:d}'.format(tid))

    return record_count


def parse_options_template_flowset(packed):
    """
    Responsibility: parse Options Template FlowSet

    Args:
        packed      `bytes`: data to parse

    Return:
        number of records processed
    """
    record_count = 1
    start = 0
    stop = 6
    unpacked = struct.unpack('!HHH', packed[start:stop])
    tid, scopelen, optionlen = unpacked
    start = stop
    reclen = scopelen + optionlen
    stop += reclen
    tbytes = packed[start:stop]
    assert reclen % 4 == 0
    tdata = struct.unpack('!' + 'HH' * (reclen // 4), tbytes)
    v9_state.OptionsTemplate(tid, tdata, scopelen, optionlen)
    return record_count


class Zemplate:
    __doc__ = '\n    Responsibility: represent Template Record\n    '
    tdict = {}

    def __init__(self, tid, tdata):
        self.tid = tid
        self.tdata = tdata
        try:
            try:
                template = Zemplate.tdict[tid]
                if self.__repr__() == template.__repr__():
                    logger.info('Renewing template {:d}'.format(tid))
                else:
                    logger.warning('Replacing template {:d}'.format(tid))
            except KeyError:
                logger.info('Creating template {:d}'.format(tid))

        finally:
            Zemplate.tdict[tid] = self

    @classmethod
    def get(cls, tid):
        """
        Return:
            `Template` or raise `KeyError`
        """
        return cls.tdict[tid]

    @classmethod
    def discard_all(cls):
        """
        Discard all templates
        """
        cls.tdict = {}

    @property
    def types(self):
        return self.tdata[0::2]

    @property
    def lengths(self):
        return self.tdata[1::2]

    def __repr__(self):
        return (
         self.tid, self.tdata)


def parse_template_flowset(packed):
    """
    Responsibility: parse Template FlowSet

    Args:
        packed      `bytes`: data to parse

    Return:
        number of records processed
    """
    record_count = 0
    start = 0
    while True:
        stop = start + 4
        try:
            assert len(packed[start:stop]) == 4
        except AssertionError:
            break

        tid, fieldcount = struct.unpack('!HH', packed[start:stop])
        start = stop
        stop += fieldcount * 4
        tbytes = packed[start:stop]
        tdata = struct.unpack('!' + 'HH' * fieldcount, tbytes)
        start = stop
        v9_state.Template(tid, tdata)
        record_count += 1

    return record_count


def dispatch_flowset(setid, packed):
    """
    Responsibility: dispatch FlowSet data to the appropriate parser

    Args:
        setid       `int`: the setid here IS the tid (aka Template ID)
        packed      `bytes`: data to dispatch

    Return:
        number of records processed
    """
    record_count = 0
    if setid == 0:
        record_count += parse_template_flowset(packed)
    else:
        if setid == 1:
            record_count += parse_options_template_flowset(packed)
        else:
            if 255 < setid and setid < 65536:
                record_count += parse_data_flowset(setid, packed)
            else:
                logger.error('No implementation for unknown ID {:3d} - {}'.format(setid, packed))
    return record_count


def parse_file(fh):
    """
    Responsibility: parse raw NetFlow V9 data from disk.
    """
    lastseq = None
    lastup = None
    count = None
    record_count = 0
    while True:
        pos = fh.tell()
        packed = fh.read(4)
        try:
            assert len(packed) == 4
        except AssertionError:
            return

        setid, setlen = struct.unpack('!HH', packed)
        if setid != 9:
            packed = fh.read(setlen - 4)
            assert len(packed) == setlen - 4
            record_count += dispatch_flowset(setid, packed)
        else:
            if count:
                if count != record_count:
                    logger.warning('Record account not balanced {}/{}'.format(count, record_count))
                else:
                    logger.warning('Processed {} records'.format(count))
            fh.seek(pos)
            packed = fh.read(20)
            assert len(packed) == 20
            header = struct.unpack('!HHIIII', packed)
            logger.debug(header)
            up = header[2]
            seq = header[4]
            if lastup and lastseq and seq != lastseq + 1:
                updiff = up - lastup
                logger.warning('Out of seq, lost {}, tdiff {:.1f} s'.format(seq - lastseq, round(updiff / 1000, 1)))
                if updiff > lim * 1000:
                    logger.warning('Discarding templates')
                    v9_state.Template.discard_all()
            lastup = up
            lastseq = seq
            count = header[1]
            record_count = 0
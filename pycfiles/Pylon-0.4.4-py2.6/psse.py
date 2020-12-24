# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\io\psse.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a reader for PSS/E data files.
"""
import os, time, logging
from pylon import Case, Bus, Branch, Generator, PQ, PV, REFERENCE, ISOLATED
from pylon.util import feq
from pylon.io.common import _CaseReader, _CaseWriter
logger = logging.getLogger(__name__)

class PSSEReader(_CaseReader):
    """ Defines a reader for PSS/E(TM) version 30 Raw files.
    """

    def __init__(self):
        self.xtol = 0.0001
        self.init()

    def init(self):
        self.bus_map = {}

    def read(self, file_or_filename):
        """ Returns a case from a version 30 PSS/E raw file.

        @param file_or_filename: File name or file like object with PSS/E data
        @return: Case object
        """
        t0 = time.time()
        self.init()
        if isinstance(file_or_filename, basestring):
            fname = os.path.basename(file_or_filename)
            logger.info('Loading PSS/E Raw file [%s].' % fname)
            file = None
            try:
                try:
                    file = open(file_or_filename, 'rb')
                except:
                    logger.error('Error opening %s.' % fname)
                    return

            finally:
                if file is not None:
                    case = self._parse_file(file)
                    file.close()

        else:
            file = file_or_filename
            case = self._parse_file(file)
        logger.info('PSS/E Raw file parsed in %.2fs.' % (time.time() - t0))
        return case

    def _parse_file(self, file):
        """ Parses the given file.
        """
        case = Case()
        file.seek(0)
        case.base_mva = float(file.next().split(',')[1].split('/')[0])
        case.name = '%s %s' % (file.next().strip(), file.next().strip())
        bustype_map = {1: 'PQ', 2: 'PV', 3: 'ref', 4: 'isolated'}
        bus_data = file.next().split(',')
        while bus_data[0].strip()[0] != '0':
            bus = Bus()
            i = int(bus_data[0].strip())
            self.bus_map[i] = bus
            bus._i = i
            bus.name = bus_data[1].strip("'").strip()
            bus.v_base = float(bus_data[2])
            bus.type = bustype_map[int(bus_data[3])]
            bus.g_shunt = float(bus_data[4])
            bus.b_shunt = float(bus_data[5])
            bus.v_magnitude = float(bus_data[8])
            bus.v_angle = float(bus_data[9])
            case.buses.append(bus)
            bus_data = file.next().split(',')

        load_data = file.next().split(',')
        while load_data[0].strip()[0] != '0':
            bus = self.bus_map[int(load_data[0].strip())]
            bus.p_demand += float(load_data[5])
            bus.q_demand += float(load_data[6])
            load_data = file.next().split(',')

        gen_data = file.next().split(',')
        while gen_data[0].strip()[0] != '0':
            bus = self.bus_map[int(gen_data[0].strip())]
            g = Generator(bus)
            g.p = float(gen_data[2])
            g.q = float(gen_data[3])
            g.q_max = float(gen_data[4])
            g.q_min = float(gen_data[5])
            g.v_magnitude = float(gen_data[6])
            g.base_mva = float(gen_data[8])
            g.online = bool(int(gen_data[14]))
            g.p_max = float(gen_data[16])
            g.p_min = float(gen_data[17])
            case.generators.append(g)
            gen_data = file.next().split(',')

        branch_data = file.next().split(',')
        while branch_data[0].strip()[0] != '0':
            from_bus = self.bus_map[abs(int(branch_data[0]))]
            to_bus = self.bus_map[abs(int(branch_data[1]))]
            l = Branch(from_bus, to_bus)
            l.r = float(branch_data[3])
            l.x = float(branch_data[4])
            l.b = float(branch_data[5])
            l.rate_a = float(branch_data[6])
            l.rate_b = float(branch_data[7])
            l.rate_c = float(branch_data[8])
            case.branches.append(l)
            branch_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            trx_data2 = file.next().split(',')
            trx_data3 = file.next().split(',')
            trx_data4 = file.next().split(',')
            if len(trx_data2) < 5:
                from_bus = self.bus_map[abs(int(trx_data[0]))]
                to_bus = self.bus_map[abs(int(trx_data[1]))]
                l = Branch(from_bus, to_bus)
                l.name = trx_data[10].strip("'").strip()
                l.online = bool(int(trx_data[11]))
                l.b = float(trx_data[8])
                l.r = float(trx_data2[0])
                l.x = float(trx_data2[1])
                l.ratio = float(trx_data3[0])
                l.phase_shift = float(trx_data3[2])
                rate_a = float(trx_data3[3])
                if rate_a != 0.0:
                    l.rate_a = rate_a
                rate_b = float(trx_data3[4])
                if rate_b != 0.0:
                    l.rate_b = rate_b
                rate_c = float(trx_data3[5])
                if rate_c != 0.0:
                    l.rate_c = rate_c
                case.branches.append(l)
                trx_data = file.next().split(',')
            else:
                trx_data5 = file.next().split(',')
                tmp_bus = Bus()
                tmp_bus.name = 'n' + tmp_bus.name
                tmp_bus._i = len(case.buses) + 1
                bus1 = self.bus_map[abs(int(trx_data[0]))]
                bus2 = self.bus_map[abs(int(trx_data[1]))]
                bus3 = self.bus_map[abs(int(trx_data[2]))]
                l1 = Branch(tmp_bus, bus1)
                l2 = Branch(tmp_bus, bus2)
                l3 = Branch(tmp_bus, bus3)
                b = float(trx_data[8])
                l1.b = b
                on = bool(int(trx_data[11]))
                l1.online = on
                l2.online = on
                l3.online = on
                r12 = float(trx_data2[0])
                x12 = float(trx_data2[1])
                r23 = float(trx_data2[3])
                x23 = float(trx_data2[4])
                r31 = float(trx_data2[6])
                x31 = float(trx_data2[7])
                l1.r = 0.5 * (r12 + r31 - r23)
                l1.x = 0.5 * (x12 + x31 - x23)
                l2.r = 0.5 * (r12 + r23 - r31)
                l2.x = 0.5 * (x12 + x23 - x31)
                l3.r = 0.5 * (r23 + r31 - r12)
                l3.x = 0.5 * (x23 + x31 - x12)
                for l in [l1, l2, l3]:
                    if abs(l.x) < 1e-05:
                        logger.warning('Zero branch reactance [%s].' % l.name)
                        l.x = self.xtol
                    if abs(complex(l.r, l.x)) < 1e-05:
                        logger.warning('Zero branch impedance [%s].' % l.name)

                l1.ratio = float(trx_data3[0])
                l1.phase_shift = float(trx_data3[2])
                l2.ratio = float(trx_data4[0])
                l2.phase_shift = float(trx_data4[2])
                l3.ratio = float(trx_data5[0])
                l3.phase_shift = float(trx_data5[2])
                rate_a1 = float(trx_data3[3])
                rate_b1 = float(trx_data3[4])
                rate_c1 = float(trx_data3[5])
                if rate_a1 > 0.0:
                    l1.rate_a = rate_a1
                if rate_b1 > 0.0:
                    l1.rate_b = rate_b1
                if rate_c1 > 0.0:
                    l1.rate_c = rate_c1
                rate_a2 = float(trx_data4[3])
                rate_b2 = float(trx_data4[4])
                rate_c2 = float(trx_data4[5])
                if rate_a2 > 0.0:
                    l2.rate_a = rate_a2
                if rate_b2 > 0.0:
                    l2.rate_b = rate_b2
                if rate_c2 > 0.0:
                    l2.rate_c = rate_c2
                rate_a3 = float(trx_data5[3])
                rate_b3 = float(trx_data5[4])
                rate_c3 = float(trx_data5[5])
                if rate_a3 > 0.0:
                    l3.rate_a = rate_a3
                if rate_b2 > 0.0:
                    l3.rate_b = rate_b3
                if rate_c2 > 0.0:
                    l3.rate_c = rate_c3
                case.buses.append(tmp_bus)
                case.branches.append(l1)
                case.branches.append(l2)
                case.branches.append(l3)
                trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring area interchange data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring two-terminal DC line data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring VSC DC line data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            bus = self.bus_map[abs(int(trx_data[0]))]
            bus.b_shunt += float(trx_data[7])
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring transformer X correction table data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring multi-terminal dc line data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring multisection line data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring zone data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring interarea transfer data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring owner data.')
            trx_data = file.next().split(',')

        trx_data = file.next().split(',')
        while trx_data[0].strip()[0] != '0':
            logger.warning('Ignoring FACTS device data.')
            trx_data = file.next().split(',')

        return case


class PSSEWriter(_CaseWriter):
    """ Defines a class for writing a case in PSS/E format.
    """

    def _write_data(self, file):
        self.write_case_data(file)
        self.write_bus_data(file)
        self.write_generator_data(file)
        self.write_branch_data(file)

    def write_case_data(self, file):
        """ Writes case data to file.
        """
        change_code = 0
        s_base = self.case.base_mva
        timestr = time.strftime('%Y%m%d%H%M', time.gmtime())
        file.write('%d, %8.2f, 30 / PSS(tm)E-30 RAW created by Pylon (%s).\n' % (
         change_code, s_base, timestr))
        file.write(' %s\n' % self.case.name)
        file.write(' %d BUSES, %d BRANCHES\n' % (
         len(self.case.buses), len(self.case.branches)))

    def write_bus_data(self, file):
        """ Writes bus data in MATPOWER format.
        """
        bus_attrs = [
         '_i', 'name', 'v_base', 'type', 'g_shunt', 'b_shunt',
         'area', 'zone',
         'v_magnitude', 'v_angle']
        for bus in self.case.buses:
            vals = [ getattr(bus, a) for a in bus_attrs ]
            d = {PQ: 1, PV: 2, REFERENCE: 3, ISOLATED: 4}
            vals[3] = d[vals[3]]
            vals.append(1)
            file.write("%6d,'%-10s',%10.4f,%d,%10.3f,%10.3f,%4d,%4d,%10.3f,%10.3f%4d\n" % tuple(vals))

        file.write(' 0 / END OF BUS DATA, BEGIN LOAD DATA\n')
        load_attrs = [
         '_i', 'area', 'zone', 'p_demand', 'q_demand']
        for bus in self.case.buses:
            if bus.p_demand > 0.0 or bus.q_demand > 0.0:
                vals = [ getattr(bus, a) for a in load_attrs ]
                vals.insert(1, 1)
                vals.insert(1, '1 ')
                vals.extend([0.0, 0.0, 0.0, 0.0])
                vals.append(1)
                file.write("%6d,'%s',%2d,%2d,%2d,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%4d\n" % tuple(vals))

        file.write(' 0 / END OF LOAD DATA, BEGIN GENERATOR DATA\n')

    def write_generator_data(self, file):
        """ Writes generator data in MATPOWER format.
        """
        for generator in self.case.generators:
            vals = []
            vals.append(generator.bus._i)
            vals.append('1 ')
            vals.append(generator.p)
            vals.append(generator.q)
            vals.append(generator.q_max)
            vals.append(generator.q_min)
            vals.append(generator.v_magnitude)
            vals.append(0)
            vals.append(generator.base_mva)
            vals.extend([0.0, 0.0, 0.0, 0.0, 0.0])
            vals.append(generator.online)
            vals.append(100.0)
            vals.append(generator.p_max)
            vals.append(generator.p_min)
            vals.extend([1, 1.0])
            file.write("%6d,'%s',%10.3f,%10.3f,%10.3f,%10.3f,%10.5f,%6d,%10.3f,%10.5f,%10.5f,%10.5f,%10.5f,%7.5f,%d,%7.1f,%10.3f,%10.3f,%4d,%6.4f\n" % tuple(vals))

        file.write(' 0 / END OF GENERATOR DATA, BEGIN NON-TRANSFORMER BRANCH DATA\n')

    def write_branch_data(self, file):
        """ Writes branch data to file.
        """
        branch_attr = [
         'r', 'x', 'b', 'rate_a', 'rate_b', 'rate_c']
        for branch in self.case.branches:
            if feq(branch.ratio, 0.0):
                vals = [ getattr(branch, a) for a in branch_attr ]
                vals.insert(0, '1 ')
                vals.insert(0, branch.to_bus._i)
                vals.insert(0, branch.from_bus._i)
                vals.extend([0.0, 0.0, 0.0, 0.0])
                vals.append(branch.online)
                vals.extend([0.0, 1, 1.0])
                file.write("%6d,%6d,'%s',%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%10.3f,%d,%10.3f,%4d,%6.4f\n" % tuple(vals))

        file.write(' 0 / END OF NON-TRANSFORMER BRANCH DATA, BEGIN TRANSFORMER DATA\n')
        for branch in self.case.branches:
            if not feq(branch.ratio, 0.0):
                vals = []
                vals.append(branch.from_bus._i)
                vals.append(branch.to_bus._i)
                vals.extend([0, '1 ', 1, 1, 1, 0.0, 0.0, 2])
                vals.append(branch.name)
                vals.append(branch.online)
                vals.extend([1, 1.0])
                file.write("%6d,%6d,%6d,'%2s',%d,%d,%d,%10.3f,%10.3f,%d,'%-12s',%d,%4d,%6.4f\n" % tuple(vals))
                file.write('%8.3f,%8.3f,%10.2f\n' % (branch.r, branch.x,
                 self.case.base_mva))
                line3 = []
                line3.append(branch.from_bus.v_base)
                line3.append(0.0)
                line3.append(branch.phase_shift)
                line3.append(branch.rate_a)
                line3.append(branch.rate_b)
                line3.append(branch.rate_c)
                line3.extend([0, 0, 1.1, 0.9, 1.1, 0.9, 33, 0, 0.0, 0.0])
                file.write('%7.5f,%8.3f,%8.3f,%8.2f,%8.2f,%8.2f,%d,%7d,%8.5f,%8.5f,%8.5f,%8.5f,%4d,%2d,%8.5f,%8.5f\n' % tuple(line3))
                file.write('%7.5f,%8.3f\n' % (branch.to_bus.v_base, 0.0))

        file.write(' 0 / END OF TRANSFORMER DATA, BEGIN AREA INTERCHANGE DATA\n 0 / END OF AREA INTERCHANGE DATA, BEGIN TWO-TERMINAL DC DATA\n 0 / END OF TWO-TERMINAL DC DATA, BEGIN VSC DC LINE DATA\n 0 / END OF VSC DC LINE DATA, BEGIN SWITCHED SHUNT DATA\n 0 / END OF SWITCHED SHUNT DATA, BEGIN TRANS. IMP. CORR. TABLE DATA\n 0 / END OF TRANS. IMP. CORR. TABLE DATA, BEGIN MULTI-TERMINAL DC LINE DATA\n 0 / END OF MULTI-TERMINAL DC LINE DATA, BEGIN MULTI-SECTION LINE DATA\n 0 / END OF MULTI-SECTION LINE DATA, BEGIN ZONE DATA\n 0 / END OF ZONE DATA, BEGIN INTERAREA TRANSFER DATA\n 0 / END OF INTERAREA TRANSFER DATA, BEGIN OWNER DATA\n 0 / END OF OWNER DATA, BEGIN FACTS DEVICE DATA\n 0 / END OF FACTS DEVICE DATA, END OF CASE DATA\n')
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\io\matpower.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a class for reading MATPOWER data files.\n'
import time, logging
from os.path import basename, splitext
from pylon.case import Case, Bus, Branch, PQ, PV, REFERENCE, ISOLATED
from pylon.generator import Generator, PW_LINEAR, POLYNOMIAL
from pylon.io.common import _CaseReader, _CaseWriter
logger = logging.getLogger(__name__)

class MATPOWERReader(_CaseReader):
    """ Defines a reader for MATPOWER case files.
    """

    def __init__(self, version=2):
        self.version = version
        self._bus_map = {}
        self._is_struct = True

    def read(self, file_or_filename):
        """ Returns a Case given a MATPOWER file or file name.
        """
        t0 = time.time()
        self._bus_map = {}
        if isinstance(file_or_filename, basestring):
            fname = basename(file_or_filename)
            logger.info('Loading MATPOWER file [%s].' % fname)
            file = None
            try:
                try:
                    file = open(file_or_filename, 'rb')
                except:
                    logger.error('Error opening: %s' % fname)
                    return

            finally:
                if file is not None:
                    case = self._parse_file(file)
                    file.close()

        else:
            file = file_or_filename
            case = self._parse_file(file)
        case.index_buses()
        logger.info('MATPOWER file parsed in %.2fs.' % (time.time() - t0))
        return case

    def _parse_file(self, file):
        """ Parses the given file-like object.
        """
        case = Case()
        file.seek(0)
        line = file.readline().split()
        if line[0] != 'function':
            logger.error('Invalid data file header.')
            return case
        if line[1] != 'mpc':
            self._is_struct = False
            base = ''
        else:
            base = 'mpc.'
        case.name = line[(-1)]
        for line in file:
            if line.startswith('%sbaseMVA' % base):
                case_data = line.rstrip(';\n').split()
                case.base_mva = float(case_data[(-1)])
            elif line.startswith('%sbus' % base):
                self._parse_buses(case, file)
            elif line.startswith('%sgencost' % base):
                self._parse_gencost(case, file)
            elif line.startswith('%sgen' % base):
                self._parse_generators(case, file)
            elif line.startswith('%sbranch' % base):
                self._parse_branches(case, file)

        return case

    def _parse_buses(self, case, file):
        bustype_map = {1: 'PQ', 2: 'PV', 3: 'ref', 4: 'isolated'}
        for line in file:
            if line.startswith(']'):
                break
            bus_data = line.rstrip(';\n').split()
            bus = Bus()
            i = int(bus_data[0])
            self._bus_map[i] = bus
            bus._i = i
            bus.type = bustype_map[int(bus_data[1])]
            bus.p_demand = float(bus_data[2])
            bus.q_demand = float(bus_data[3])
            bus.g_shunt = float(bus_data[4])
            bus.b_shunt = float(bus_data[5])
            bus.area = int(bus_data[6])
            bus.v_magnitude = float(bus_data[7])
            bus.v_angle = float(bus_data[8])
            bus.v_base = float(bus_data[9])
            bus.zone = int(bus_data[10])
            bus.v_max = float(bus_data[11])
            bus.v_min = float(bus_data[12])
            case.buses.append(bus)

    def _parse_generators(self, case, file):
        for line in file:
            if line.startswith(']'):
                break
            gen_data = line.strip(';\n').split()
            bus = self._bus_map[int(gen_data[0])]
            g = Generator(bus)
            g.p = float(gen_data[1])
            g.q = float(gen_data[2])
            g.q_max = float(gen_data[3])
            g.q_min = float(gen_data[4])
            g.v_magnitude = float(gen_data[5])
            g.base_mva = float(gen_data[6])
            g.online = bool(gen_data[7])
            g.p_max = float(gen_data[8])
            g.p_min = float(gen_data[9])
            case.generators.append(g)

    def _parse_branches(self, case, file):
        for line in file:
            if line.startswith(']'):
                break
            branch_data = line.strip(';\n').split()
            from_bus = self._bus_map[int(branch_data[0])]
            to_bus = self._bus_map[int(branch_data[1])]
            l = Branch(from_bus, to_bus)
            l.r = float(branch_data[2])
            l.x = float(branch_data[3])
            l.b = float(branch_data[4])
            l.rate_a = float(branch_data[5])
            l.rate_b = float(branch_data[6])
            l.rate_c = float(branch_data[7])
            l.ratio = float(branch_data[8])
            l.phase_shift = float(branch_data[9])
            l.online = bool(branch_data[10])
            case.branches.append(l)

    def _parse_gencost(self, case, file):
        for (i, line) in enumerate(file):
            if line.startswith(']'):
                break
            g = case.generators[i]
            (model, c_startup, c_shutdown, cost) = self._parse_gencost_line(line)
            g.pcost_model = model
            g.c_startup = c_startup
            g.c_shutdown = c_shutdown
            g.p_cost = cost

        if line.startswith(']'):
            logger.info('No reactive power cost data.')
            return
        for (i, line) in enumerate(file):
            g = case.generators[i]
            if line.startswith(']'):
                logger.warning('No Q cost data for %s' % g.name)
                continue
            (model, _, _, cost) = self._parse_gencost_line(line)
            g.qcost_model = model
            g.q_cost = cost

        for line in file:
            if not line.startswith(']'):
                logger.info('Superfluous Q cost data [%s].' % line)
            else:
                return

    def _parse_gencost_line(self, line):
        gencost_map = {1: PW_LINEAR, 2: POLYNOMIAL}
        gencost_data = line.replace(';', '').strip('\n').split()
        model = gencost_map[int(gencost_data[0])]
        c_startup = float(gencost_data[1])
        c_shutdown = float(gencost_data[2])
        n = int(gencost_data[3])
        if model == PW_LINEAR:
            d = gencost_data[4:4 + 2 * n]
            cost = []
            for j in range(n):
                cost.append((float(d[(2 * j)]), float(d[(2 * j + 1)])))

        else:
            d = gencost_data[4:4 + n]
            cost = tuple([ float(a) for a in d ])
        return (
         model, c_startup, c_shutdown, cost)


class MATPOWERWriter(_CaseWriter):
    """ Write case data to a file in MATPOWER format.

    Based on savecase.m from MATPOWER by Ray Zimmerman, developed at PSERC
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    """

    def __init__(self, case):
        """ Initialises a new MATPOWERWriter instance.
        """
        super(MATPOWERWriter, self).__init__(case)
        self._fcn_name = case.name
        self._prefix = 'mpc.'

    def write(self, file_or_filename):
        """ Writes case data to file in MATPOWER format.
        """
        if isinstance(file_or_filename, basestring):
            (self._fcn_name, _) = splitext(basename(file_or_filename))
        else:
            self._fcn_name = self.case.name
        self._fcn_name = self._fcn_name.replace(',', '').replace(' ', '_')
        super(MATPOWERWriter, self).write(file_or_filename)

    def write_case_data(self, file):
        """ Writes the case data in MATPOWER format.
        """
        file.write('function mpc = %s\n' % self._fcn_name)
        file.write('\n%%%% MATPOWER Case Format : Version %d\n' % 2)
        file.write("mpc.version = '2';\n")
        file.write('\n%%%%-----  Power Flow Data  -----%%%%\n')
        file.write('%%%% system MVA base\n')
        file.write('%sbaseMVA = %g;\n' % (self._prefix, self.case.base_mva))

    def write_bus_data(self, file):
        """ Writes bus data in MATPOWER format.
        """
        bus_attrs = [
         '_i', 'type', 'p_demand', 'q_demand', 'g_shunt', 'b_shunt',
         'area', 'v_magnitude', 'v_angle', 'v_base', 'zone',
         'v_max', 'v_min', 'p_lmbda', 'q_lmbda', 'mu_vmin', 'mu_vmax']
        file.write('\n%%%% bus data\n')
        file.write('%%\tbus_i\ttype\tPd\tQd\tGs\tBs\tarea\tVm\tVa\tbaseKV\tzone\tVmax\tVmin\tlam_P\tlam_Q\tmu_Vmax\tmu_Vmin')
        file.write('\n%sbus = [\n' % self._prefix)
        for bus in self.case.buses:
            vals = [ getattr(bus, a) for a in bus_attrs ]
            d = {PQ: 1, PV: 2, REFERENCE: 3, ISOLATED: 4}
            vals[1] = d[vals[1]]
            assert len(vals) == 17
            file.write('\t%d\t%d\t%g\t%g\t%g\t%g\t%d\t%.8g\t%.8g\t%g\t%d\t%g\t%g\t%.4f\t%.4f\t%.4f\t%.4f;\n' % tuple(vals[:]))

        file.write('];\n')

    def write_generator_data(self, file):
        """ Writes generator data in MATPOWER format.
        """
        gen_attr = [
         'p', 'q', 'q_max', 'q_min', 'v_magnitude',
         'base_mva', 'online', 'p_max', 'p_min', 'mu_pmax', 'mu_pmin',
         'mu_qmax', 'mu_qmin']
        file.write('\n%%%% generator data\n')
        file.write('%%\tbus\tPg\tQg\tQmax\tQmin\tVg\tmBase\tstatus\tPmax\tPmin')
        file.write('\tmu_Pmax\tmu_Pmin\tmu_Qmax\tmu_Qmin')
        file.write('\n%sgen = [\n' % self._prefix)
        for generator in self.case.generators:
            vals = [ getattr(generator, a) for a in gen_attr ]
            vals.insert(0, generator.bus._i)
            assert len(vals) == 14
            file.write('\t%d\t%g\t%g\t%g\t%g\t%.8g\t%g\t%d\t%g\t%g\t%g\t%g\t%g\t%g;\n' % tuple(vals))

        file.write('];\n')

    def write_branch_data(self, file):
        """ Writes branch data to file.
        """
        branch_attr = [
         'r', 'x', 'b', 'rate_a', 'rate_b', 'rate_c',
         'ratio', 'phase_shift', 'online', 'ang_min', 'ang_max', 'p_from',
         'q_from', 'p_to', 'q_to', 'mu_s_from', 'mu_s_to', 'mu_angmin',
         'mu_angmax']
        file.write('\n%%%% branch data\n')
        file.write('%%\tfbus\ttbus\tr\tx\tb\trateA\trateB\trateC\tratio\tangle\tstatus')
        file.write('\tangmin\tangmax')
        file.write('\tPf\tQf\tPt\tQt')
        file.write('\tmu_Sf\tmu_St')
        file.write('\tmu_angmin\tmu_angmax')
        file.write('\n%sbranch = [\n' % self._prefix)
        for branch in self.case.branches:
            vals = [ getattr(branch, a) for a in branch_attr ]
            vals.insert(0, branch.to_bus._i)
            vals.insert(0, branch.from_bus._i)
            file.write('\t%d\t%d\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%g\t%d\t%g\t%g\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f;\n' % tuple(vals))

        file.write('];\n')

    def write_generator_cost_data(self, file):
        """ Writes generator cost data to file.
        """
        file.write('\n%%%% generator cost data\n')
        file.write('%%\t1\tstartup\tshutdown\tn\tx1\ty1\t...\txn\tyn\n')
        file.write('%%\t2\tstartup\tshutdown\tn\tc(n-1)\t...\tc0\n')
        file.write('%sgencost = [\n' % self._prefix)
        for generator in self.case.generators:
            n = len(generator.p_cost)
            template = '\t%d\t%g\t%g\t%d'
            for _ in range(n):
                template = '%s\t%%g' % template

            template = '%s;\n' % template
            if generator.pcost_model == PW_LINEAR:
                t = 2
                c = [ v for pc in generator.p_cost for v in pc ]
            elif generator.pcost_model == POLYNOMIAL:
                t = 1
                c = list(generator.p_cost)
            else:
                raise
            vals = [
             t, generator.c_startup, generator.c_shutdown, n] + c
            file.write(template % tuple(vals))

        file.write('];\n')

    def write_area_data(self, file):
        """ Writes area data to file.
        """
        file.write('%% area data\n')
        file.write('%\tno.\tprice_ref_bus\n')
        file.write('areas = [\n')
        file.write('\t1\t1;\n')
        file.write('];\n')
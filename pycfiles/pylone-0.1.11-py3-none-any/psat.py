# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\io\psat.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a class for reading PSAT data files.\n'
import time, logging
from os.path import basename, splitext
from parsing_util import integer, boolean, real, scolon, matlab_comment
from pyparsing import Optional, Literal, ZeroOrMore
from pylon import Case, Bus, Branch, Generator
from pylon.io.common import _CaseReader
logger = logging.getLogger(__name__)

class PSATReader(_CaseReader):
    """ Defines a method class for reading PSAT data files and
    returning a Case object.
    """

    def read(self, file_or_filename):
        """ Parses a PSAT data file and returns a case object

            file_or_filename: File object or path to PSAT data file
            return: Case object
        """
        self.file_or_filename = file_or_filename
        logger.info('Parsing PSAT case file [%s].' % file_or_filename)
        t0 = time.time()
        self.case = Case()
        if isinstance(file_or_filename, basestring):
            (name, _) = splitext(basename(file_or_filename))
        else:
            (name, _) = splitext(file_or_filename.name)
        self.case.name = name
        bus_array = self._get_bus_array_construct()
        line_array = self._get_line_array_construct()
        slack_array = self._get_slack_array_construct()
        pv_array = self._get_pv_array_construct()
        pq_array = self._get_pq_array_construct()
        demand_array = self._get_demand_array_construct()
        supply_array = self._get_supply_array_construct()
        case = ZeroOrMore(matlab_comment) + bus_array + ZeroOrMore(matlab_comment) + line_array + ZeroOrMore(matlab_comment) + slack_array + ZeroOrMore(matlab_comment) + pv_array + ZeroOrMore(matlab_comment) + pq_array + ZeroOrMore(matlab_comment) + demand_array + ZeroOrMore(matlab_comment) + supply_array
        case.parseFile(file_or_filename)
        elapsed = time.time() - t0
        logger.info('PSAT case file parsed in %.3fs.' % elapsed)
        return self.case

    def _get_bus_array_construct(self):
        """ Returns a construct for an array of bus data.
        """
        bus_no = integer.setResultsName('bus_no')
        v_base = real.setResultsName('v_base')
        v_magnitude = Optional(real).setResultsName('v_magnitude')
        v_angle = Optional(real).setResultsName('v_angle')
        area = Optional(integer).setResultsName('area')
        region = Optional(integer).setResultsName('region')
        bus_data = bus_no + v_base + v_magnitude + v_angle + area + region + scolon
        bus_data.setParseAction(self.push_bus)
        bus_array = Literal('Bus.con') + '=' + '[' + '...' + ZeroOrMore(bus_data + Optional(']' + scolon))
        bus_array.setParseAction(self.sort_buses)
        return bus_array

    def _get_line_array_construct(self):
        """ Returns a construct for an array of line data.
        """
        from_bus = integer.setResultsName('fbus')
        to_bus = integer.setResultsName('tbus')
        s_rating = real.setResultsName('s_rating')
        v_rating = real.setResultsName('v_rating')
        f_rating = real.setResultsName('f_rating')
        length = real.setResultsName('length')
        v_ratio = real.setResultsName('v_ratio')
        r = real.setResultsName('r')
        x = real.setResultsName('x')
        b = real.setResultsName('b')
        tap_ratio = real.setResultsName('tap')
        phase_shift = real.setResultsName('shift')
        i_limit = Optional(real).setResultsName('i_limit')
        p_limit = Optional(real).setResultsName('p_limit')
        s_limit = Optional(real).setResultsName('s_limit')
        status = Optional(boolean).setResultsName('status')
        line_data = from_bus + to_bus + s_rating + v_rating + f_rating + length + v_ratio + r + x + b + tap_ratio + phase_shift + i_limit + p_limit + s_limit + status + scolon
        line_data.setParseAction(self.push_line)
        line_array = Literal('Line.con') + '=' + '[' + '...' + ZeroOrMore(line_data + Optional(']' + scolon))
        return line_array

    def _get_slack_array_construct(self):
        """ Returns a construct for an array of slack bus data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        v_rating = real.setResultsName('v_rating')
        v_magnitude = real.setResultsName('v_magnitude')
        ref_angle = real.setResultsName('ref_angle')
        q_max = Optional(real).setResultsName('q_max')
        q_min = Optional(real).setResultsName('q_min')
        v_max = Optional(real).setResultsName('v_max')
        v_min = Optional(real).setResultsName('v_min')
        p_guess = Optional(real).setResultsName('p_guess')
        lp_coeff = Optional(real).setResultsName('lp_coeff')
        ref_bus = Optional(boolean).setResultsName('ref_bus')
        status = Optional(boolean).setResultsName('status')
        slack_data = bus_no + s_rating + v_rating + v_magnitude + ref_angle + q_max + q_min + v_max + v_min + p_guess + lp_coeff + ref_bus + status + scolon
        slack_data.setParseAction(self.push_slack)
        slack_array = Literal('SW.con') + '=' + '[' + '...' + ZeroOrMore(slack_data + Optional(']' + scolon))
        return slack_array

    def _get_pv_array_construct(self):
        """ Returns a construct for an array of PV generator data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        v_rating = real.setResultsName('v_rating')
        p = real.setResultsName('p')
        v = real.setResultsName('v')
        q_max = Optional(real).setResultsName('q_max')
        q_min = Optional(real).setResultsName('q_min')
        v_max = Optional(real).setResultsName('v_max')
        v_min = Optional(real).setResultsName('v_min')
        lp_coeff = Optional(real).setResultsName('lp_coeff')
        status = Optional(boolean).setResultsName('status')
        pv_data = bus_no + s_rating + v_rating + p + v + q_max + q_min + v_max + v_min + lp_coeff + status + scolon
        pv_data.setParseAction(self.push_pv)
        pv_array = Literal('PV.con') + '=' + '[' + '...' + ZeroOrMore(pv_data + Optional(']' + scolon))
        return pv_array

    def _get_pq_array_construct(self):
        """ Returns a construct for an array of PQ load data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        v_rating = real.setResultsName('v_rating')
        p = real.setResultsName('p')
        q = real.setResultsName('q')
        v_max = Optional(real).setResultsName('v_max')
        v_min = Optional(real).setResultsName('v_min')
        z_conv = Optional(boolean).setResultsName('z_conv')
        status = Optional(boolean).setResultsName('status')
        pq_data = bus_no + s_rating + v_rating + p + q + v_max + v_min + z_conv + status + scolon
        pq_data.setParseAction(self.push_pq)
        pq_array = Literal('PQ.con') + '=' + '[' + '...' + ZeroOrMore(pq_data + Optional(']' + scolon))
        return pq_array

    def _get_demand_array_construct(self):
        """ Returns a construct for an array of power demand data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        p_direction = real.setResultsName('p_direction')
        q_direction = real.setResultsName('q_direction')
        p_bid_max = real.setResultsName('p_bid_max')
        p_bid_min = real.setResultsName('p_bid_min')
        p_optimal_bid = Optional(real).setResultsName('p_optimal_bid')
        p_fixed = real.setResultsName('p_fixed')
        p_proportional = real.setResultsName('p_proportional')
        p_quadratic = real.setResultsName('p_quadratic')
        q_fixed = real.setResultsName('q_fixed')
        q_proportional = real.setResultsName('q_proportional')
        q_quadratic = real.setResultsName('q_quadratic')
        commitment = boolean.setResultsName('commitment')
        cost_tie_break = real.setResultsName('cost_tie_break')
        cost_cong_up = real.setResultsName('cost_cong_up')
        cost_cong_down = real.setResultsName('cost_cong_down')
        status = Optional(boolean).setResultsName('status')
        demand_data = bus_no + s_rating + p_direction + q_direction + p_bid_max + p_bid_min + p_optimal_bid + p_fixed + p_proportional + p_quadratic + q_fixed + q_proportional + q_quadratic + commitment + cost_tie_break + cost_cong_up + cost_cong_down + status + scolon
        demand_data.setParseAction(self.push_demand)
        demand_array = Literal('Demand.con') + '=' + '[' + '...' + ZeroOrMore(demand_data + Optional(']' + scolon))
        return demand_array

    def _get_supply_array_construct(self):
        """ Returns a construct for an array of power supply data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        p_direction = real.setResultsName('p_direction')
        p_bid_max = real.setResultsName('p_bid_max')
        p_bid_min = real.setResultsName('p_bid_min')
        p_bid_actual = real.setResultsName('p_bid_actual')
        p_fixed = real.setResultsName('p_fixed')
        p_proportional = real.setResultsName('p_proportional')
        p_quadratic = real.setResultsName('p_quadratic')
        q_fixed = real.setResultsName('q_fixed')
        q_proportional = real.setResultsName('q_proportional')
        q_quadratic = real.setResultsName('q_quadratic')
        commitment = boolean.setResultsName('commitment')
        cost_tie_break = real.setResultsName('cost_tie_break')
        lp_factor = real.setResultsName('lp_factor')
        q_max = real.setResultsName('q_max')
        q_min = real.setResultsName('q_min')
        cost_cong_up = real.setResultsName('cost_cong_up')
        cost_cong_down = real.setResultsName('cost_cong_down')
        status = Optional(boolean).setResultsName('status')
        supply_data = bus_no + s_rating + p_direction + p_bid_max + p_bid_min + p_bid_actual + p_fixed + p_proportional + p_quadratic + q_fixed + q_proportional + q_quadratic + commitment + cost_tie_break + lp_factor + q_max + q_min + cost_cong_up + cost_cong_down + status + scolon
        supply_data.setParseAction(self.push_supply)
        supply_array = Literal('Supply.con') + '=' + '[' + '...' + ZeroOrMore(supply_data + Optional(']' + scolon))
        return supply_array

    def _get_generator_ramping_construct(self):
        """ Returns a construct for an array of generator ramping data.
        """
        supply_no = integer.setResultsName('supply_no')
        s_rating = real.setResultsName('s_rating')
        up_rate = real.setResultsName('up_rate')
        down_rate = real.setResultsName('down_rate')
        min_period_up = real.setResultsName('min_period_up')
        min_period_down = real.setResultsName('min_period_down')
        initial_period_up = integer.setResultsName('initial_period_up')
        initial_period_down = integer.setResultsName('initial_period_down')
        c_startup = real.setResultsName('c_startup')
        status = boolean.setResultsName('status')
        g_ramp_data = supply_no + s_rating + up_rate + down_rate + min_period_up + min_period_down + initial_period_up + initial_period_down + c_startup + status + scolon
        g_ramp_array = Literal('Rmpg.con') + '=' + '[' + ZeroOrMore(g_ramp_data + Optional(']' + scolon))
        return g_ramp_array

    def _get_load_ramping_construct(self):
        """ Returns a construct for an array of load ramping data.
        """
        bus_no = integer.setResultsName('bus_no')
        s_rating = real.setResultsName('s_rating')
        up_rate = real.setResultsName('up_rate')
        down_rate = real.setResultsName('down_rate')
        min_up_time = real.setResultsName('min_up_time')
        min_down_time = real.setResultsName('min_down_time')
        n_period_up = integer.setResultsName('n_period_up')
        n_period_down = integer.setResultsName('n_period_down')
        status = boolean.setResultsName('status')
        l_ramp_data = bus_no + s_rating + up_rate + down_rate + min_up_time + min_down_time + n_period_up + n_period_down + status + scolon
        l_ramp_array = Literal('Rmpl.con') + '=' + '[' + ZeroOrMore(l_ramp_data + Optional(']' + scolon))
        return l_ramp_array

    def push_bus(self, tokens):
        """ Adds a Bus object to the case.
        """
        logger.debug('Pushing bus data: %s' % tokens)
        bus = Bus()
        bus.name = tokens['bus_no']
        bus.v_magnitude = tokens['v_magnitude']
        bus.v_angle = tokens['v_angle']
        bus.v_magnitude = tokens['v_magnitude']
        bus.v_angle = tokens['v_angle']
        self.case.buses.append(bus)

    def sort_buses(self, tokens):
        """ Sorts bus list according to name (bus_no).
        """
        self.case.buses.sort(key=lambda obj: obj.name)

    def push_line(self, tokens):
        """ Adds a Branch object to the case.
        """
        logger.debug('Pushing line data: %s' % tokens)
        from_bus = self.case.buses[(tokens['fbus'] - 1)]
        to_bus = self.case.buses[(tokens['tbus'] - 1)]
        e = Branch(from_bus=from_bus, to_bus=to_bus)
        e.r = tokens['r']
        e.x = tokens['x']
        e.b = tokens['b']
        e.rate_a = tokens['s_limit']
        e.rate_b = tokens['p_limit']
        e.rate_c = tokens['i_limit']
        if tokens['tap'] == 0:
            e.ratio = 1.0
        else:
            e.ratio = tokens['tap']
        e.phase_shift = tokens['shift']
        self.case.branches.append(e)

    def push_slack(self, tokens):
        """ Finds the slack bus, adds a Generator with the appropriate data
        and sets the bus type to slack.
        """
        logger.debug('Pushing slack data: %s' % tokens)
        bus = self.case.buses[(tokens['bus_no'] - 1)]
        g = Generator(bus)
        g.q_max = tokens['q_max']
        g.q_min = tokens['q_min']
        self.case.generators.append(g)
        bus.type = 'ref'

    def push_pv(self, tokens):
        """ Creates and Generator object, populates it with data, finds its Bus
        and adds it.
        """
        logger.debug('Pushing PV data: %s' % tokens)
        bus = self.case.buses[(tokens['bus_no'] - 1)]
        g = Generator(bus)
        g.p = tokens['p']
        g.q_max = tokens['q_max']
        g.q_min = tokens['q_min']
        self.case.generators.append(g)

    def push_pq(self, tokens):
        """ Creates and Load object, populates it with data, finds its Bus and
        adds it.
        """
        logger.debug('Pushing PQ data: %s' % tokens)
        bus = self.case.buses[(tokens['bus_no'] - 1)]
        bus.p_demand = tokens['p']
        bus.q_demand = tokens['q']

    def push_demand(self, tokens):
        """ Added OPF and CPF data to an appropriate Load.
        """
        logger.debug('Pushing demand data: %s' % tokens)

    def push_supply(self, tokens):
        """ Adds OPF and CPF data to a Generator.
        """
        logger.debug('Pushing supply data: %s' % tokens)
        bus = self.case.buses[(tokens['bus_no'] - 1)]
        n_generators = len([ g for g in self.case.generators if g.bus == bus ])
        if n_generators == 0:
            logger.error('No generator at bus [%s] for matching supply' % bus)
            return
        if n_generators > 1:
            g = [ g for g in self.case.generators if g.bus == bus ][0]
            logger.warning('More than one generator at bus [%s] for demand. Using the first one [%s].' % (
             bus, g))
        else:
            g = [ g for g in self.case.generators if g.bus == bus ][0]
        g.pcost_model = 'poly'
        g.poly_coeffs = (
         tokens['p_fixed'],
         tokens['p_proportional'],
         tokens['p_quadratic'])
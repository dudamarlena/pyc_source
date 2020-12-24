# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\generator.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a generator as a complex power injection at a bus.
"""
import logging
from numpy import polyval
from util import _Named
GENERATOR = 'generator'
DISPATCHABLE_LOAD = 'vload'
POLYNOMIAL = 'poly'
PW_LINEAR = 'pwl'
logger = logging.getLogger(__name__)

class Generator(_Named):
    """ Generators are defined as a complex power injection at a specific bus.
    """

    def __init__(self, bus, name=None, online=True, base_mva=100.0, p=100.0, p_max=200.0, p_min=0.0, v_magnitude=1.0, q=0.0, q_max=30.0, q_min=-30.0, c_startup=0.0, c_shutdown=0.0, p_cost=None, pcost_model=POLYNOMIAL, q_cost=None, qcost_model=None):
        self.bus = bus
        self.name = name
        self.online = online
        self.base_mva = base_mva
        self.p = p
        self.p_max = p_max
        self.p_min = p_min
        self.v_magnitude = v_magnitude
        self.q = q
        self.q_max = q_max
        self.q_min = q_min
        self.c_startup = c_startup
        self.c_shutdown = c_shutdown
        if isinstance(p_cost, tuple):
            self.pcost_model = POLYNOMIAL
        elif isinstance(p_cost, list):
            self.pcost_model = PW_LINEAR
        else:
            self.pcost_model = pcost_model
        if isinstance(q_cost, tuple):
            self.qcost_model = POLYNOMIAL
        elif isinstance(q_cost, list):
            self.qcost_model = PW_LINEAR
        else:
            self.qcost_model = qcost_model
        if p_cost is not None:
            self.p_cost = p_cost
        elif self.pcost_model == POLYNOMIAL:
            self.p_cost = (0.01, 0.1, 10.0)
        elif self.pcost_model == PW_LINEAR:
            self.p_cost = [
             (0.0, 0.0), (p_max, 10.0)]
        else:
            raise ValueError
        self.q_cost = q_cost
        self.mu_pmin = 0.0
        self.mu_pmax = 0.0
        self.mu_qmin = 0.0
        self.mu_qmax = 0.0
        return

    @property
    def q_limited(self):
        """ Is the machine at it's limit of reactive power?
        """
        if self.q >= self.q_max or self.q <= self.q_min:
            return True
        else:
            return False

    @property
    def is_load(self):
        """ Returns true if the generator if a dispatchable load. This may
        need to be revised to allow sensible specification of both elastic
        demand and pumped storage units.
        """
        return self.p_min < 0.0 and self.p_max == 0.0

    def reset(self):
        """ Resets the result variables.
        """
        self.mu_pmin = 0.0
        self.mu_pmax = 0.0

    def total_cost(self, p=None, p_cost=None, pcost_model=None):
        """ Computes total cost for the generator at the given output level.
        """
        p = self.p if p is None else p
        p_cost = self.p_cost if p_cost is None else p_cost
        pcost_model = self.pcost_model if pcost_model is None else pcost_model
        p = 0.0 if not self.online else p
        if pcost_model == PW_LINEAR:
            n_segments = len(p_cost) - 1
            for i in range(n_segments):
                (x1, y1) = p_cost[i]
                (x2, y2) = p_cost[(i + 1)]
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                if x1 <= p <= x2:
                    result = m * p + c
                    break
            else:
                logger.error('Value [%f] outside pwl cost curve [%s].' % (
                 p, p_cost[(-1)][0]))
                result = m * p + c
        else:
            if pcost_model == POLYNOMIAL:
                result = polyval(p_cost, p)
            else:
                raise ValueError
            if self.is_load:
                return -result
            return result
            return

    def pwl_to_poly(self):
        """ Converts the first segment of the pwl cost to linear quadratic.
        FIXME: Curve-fit for all segments.
        """
        if self.pcost_model == PW_LINEAR:
            x0 = self.p_cost[0][0]
            y0 = self.p_cost[0][1]
            x1 = self.p_cost[1][0]
            y1 = self.p_cost[1][1]
            m = (y1 - y0) / (x1 - x0)
            c = y0 - m * x0
            self.pcost_model = POLYNOMIAL
            self.p_cost = (m, c)
        else:
            return

    def poly_to_pwl(self, n_points=4):
        """ Sets the piece-wise linear cost attribute, converting the
        polynomial cost variable by evaluating at zero and then at n_points
        evenly spaced points between p_min and p_max.
        """
        assert self.pcost_model == POLYNOMIAL
        p_min = self.p_min
        p_max = self.p_max
        p_cost = []
        if p_min > 0.0:
            step = (p_max - p_min) / (n_points - 2)
            y0 = self.total_cost(0.0)
            p_cost.append((0.0, y0))
            x = p_min
            n_points -= 1
        else:
            step = (p_max - p_min) / (n_points - 1)
            x = 0.0
        for _ in range(n_points):
            y = self.total_cost(x)
            p_cost.append((x, y))
            x += step

        self.pcost_model = PW_LINEAR
        self.p_cost = p_cost

    def get_offers(self, n_points=6):
        """ Returns quantity and price offers created from the cost function.
        """
        from pyreto.smart_market import Offer
        qtyprc = self._get_qtyprc(n_points)
        return [ Offer(self, qty, prc) for (qty, prc) in qtyprc ]

    def get_bids(self, n_points=6):
        """ Returns quantity and price bids created from the cost function.
        """
        from pyreto.smart_market import Bid
        qtyprc = self._get_qtyprc(n_points)
        return [ Bid(self, qty, prc) for (qty, prc) in qtyprc ]

    def _get_qtyprc(self, n_points=6):
        """ Returns a list of tuples of the form (qty, prc) created from the
        cost function.  If the cost function is polynomial it will be converted
        to piece-wise linear using poly_to_pwl(n_points).
        """
        if self.pcost_model == POLYNOMIAL:
            self.poly_to_pwl(n_points)
        n_segments = len(self.p_cost) - 1
        qtyprc = []
        for i in range(n_segments):
            (x1, y1) = self.p_cost[i]
            (x2, y2) = self.p_cost[(i + 1)]
            quantity = x2 - x1
            price = (y2 - y1) / quantity
            qtyprc.append((quantity, price))

        return qtyprc

    def offers_to_pwl(self, offers):
        """ Updates the piece-wise linear total cost function using the given
        offer blocks.

        Based on off2case.m from MATPOWER by Ray Zimmerman, developed at PSERC
        Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
        """
        assert not self.is_load
        g_offers = [ offer for offer in offers if offer.generator == self ]
        gt_zero = [ offr for offr in g_offers if round(offr.quantity, 4) > 0.0 ]
        valid = [ offer for offer in gt_zero if not offer.withheld ]
        p_offers = [ v for v in valid if not v.reactive ]
        q_offers = [ v for v in valid if v.reactive ]
        if p_offers:
            self.p_cost = self._offbids_to_points(p_offers)
            self.pcost_model = PW_LINEAR
            self.online = True
        else:
            self.p_cost = [
             (0.0, 0.0), (self.p_max, 0.0)]
            self.pcost_model = PW_LINEAR
            if q_offers:
                self.p_min = 0.0
                self.p_max = 0.0
                self.online = True
            else:
                self.online = False
        if q_offers:
            self.q_cost = self._offbids_to_points(q_offers)
            self.qcost_model = PW_LINEAR
        else:
            self.q_cost = None
            self.qcost_model = PW_LINEAR
        if not len(p_offers) and not len(q_offers):
            logger.info('No valid offers for generator [%s], shutting down.' % self.name)
            self.online = False
        self._adjust_limits()
        return

    def bids_to_pwl(self, bids):
        """ Updates the piece-wise linear total cost function using the given
        bid blocks.

        Based on off2case.m from MATPOWER by Ray Zimmerman, developed at PSERC
        Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
        """
        assert self.is_load
        vl_bids = [ bid for bid in bids if bid.vLoad == self ]
        gt_zero = [ bid for bid in vl_bids if round(bid.quantity, 4) > 0.0 ]
        valid_bids = [ bid for bid in gt_zero if not bid.withheld ]
        p_bids = [ v for v in valid_bids if not v.reactive ]
        q_bids = [ v for v in valid_bids if v.reactive ]
        if p_bids:
            self.p_cost = self._offbids_to_points(p_bids, True)
            self.pcost_model = PW_LINEAR
            self.online = True
        else:
            self.p_cost = [
             (0.0, 0.0), (self.p_max, 0.0)]
            self.pcost_model = PW_LINEAR
            logger.info('No valid active power bids for dispatchable load [%s], shutting down.' % self.name)
            self.online = False
        if q_bids:
            self.q_cost = self._offbids_to_points(q_bids, True)
            self.qcost_model = PW_LINEAR
            self.online = True
        else:
            self.q_cost = [
             (
              self.q_min, 0.0), (0.0, 0.0), (self.q_max, 0.0)]
            self.qcost_model = PW_LINEAR
        self._adjust_limits()

    def _offbids_to_points(self, offbids, arebids=False):
        """ Returns a list of points for a piece-wise linear function from the
        given offer/bid blocks.
        """
        offbids.sort(key=lambda x: x.price, reverse=arebids)
        points = [
         (
          0.0, offbids[0].noLoadCost)]
        for (i, offbid) in enumerate(offbids):
            (x1, y1) = points[i]
            x2 = x1 + offbid.quantity
            m = offbid.price
            y2 = m * (x2 - x1) + y1
            points.append((x2, y2))

        if arebids:
            points = [ (-x, -y) for (x, y) in points ]
            points.reverse()
        return points

    def _adjust_limits(self):
        """ Sets the active power limits, 'p_max' and 'p_min', according to
        the pwl cost function points.
        """
        if not self.is_load:
            self.p_max = max([ point[0] for point in self.p_cost ])
        else:
            p_min = min([ point[0] for point in self.p_cost ])
            self.p_max = 0.0
            self.q_min = self.q_min * p_min / self.p_min
            self.q_max = self.q_max * p_min / self.p_min
            self.p_min = p_min
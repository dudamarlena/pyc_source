# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\util.py
# Compiled at: 2010-12-26 13:36:33
""" Defines various utility functions and classes for Pylon.
"""
from __future__ import with_statement
import os.path, pickle, random
from numpy import ones, array, exp, pi, Inf
from itertools import count, izip
known_extensions = {'m': 'matpower', 
   'pkl': 'pickle', 
   'pickle': 'pickle', 
   'raw': 'psse', 
   'rst': 'rest', 
   'csv': 'csv', 
   'xls': 'excel', 
   'dot': 'dot'}

class _Named(object):
    """ Base class taken from PyBrain for objects guaranteed to have a
        unique name.
    """
    _name_ids = count(0)

    def _get_name(self):
        """ Returns the name, which is generated if it has not been already.
        """
        if self._name is None:
            self._name = self._generate_name()
        return self._name

    def _set_name(self, value):
        """ Changes name to 'value'. Uniquity no longer guaranteed.
        """
        self._name = value

    _name = None
    name = property(_get_name, _set_name)

    def _generate_name(self):
        """ Return a unique name for this object.
        """
        return '%s-%i' % (self.__class__.__name__, self._name_ids.next())


class _Serializable(object):
    """ Defines shortcuts to serialize an object.  Taken from PyBrain.
    """

    def save_to_file_object(self, fd, format=None, **kwargs):
        """ Save the object to a given file like object in the given format.
        """
        format = 'pickle' if format is None else format
        save = getattr(self, 'save_%s' % format, None)
        if save is None:
            raise ValueError("Unknown format '%s'." % format)
        save(fd, **kwargs)
        return

    @classmethod
    def load_from_file_object(cls, fd, format=None):
        """ Load the object from a given file like object in the given format.
        """
        format = 'pickle' if format is None else format
        load = getattr(cls, 'load_%s' % format, None)
        if load is None:
            raise ValueError("Unknown format '%s'." % format)
        return load(fd)

    def save(self, filename, format=None, **kwargs):
        """ Save the object to file given by filename.
        """
        if format is None:
            format = format_from_extension(filename)
        with file(filename, 'wb') as (fp):
            self.save_to_file_object(fp, format, **kwargs)
        return

    @classmethod
    def load(cls, filename, format=None):
        """ Return an instance of the class that is saved in the file with the
            given filename in the specified format.
        """
        if format is None:
            format = format_from_extension(filename)
        with file(filename, 'rbU') as (fp):
            obj = cls.load_from_file_object(fp, format)
            obj.filename = filename
            return obj
        return

    def save_pickle(self, fd, protocol=0):
        """ Create portable serialized representation of the object.
        """
        pickle.dump(self, fd, protocol)

    @classmethod
    def load_pickle(cls, fd):
        """ Load portable serialized representation of the object.
        """
        return pickle.load(fd)


def format_from_extension(fname):
    """ Tries to infer a protocol from the file extension."""
    (_base, ext) = os.path.splitext(fname)
    if not ext:
        return
    else:
        try:
            format = known_extensions[ext.replace('.', '')]
        except KeyError:
            format = None

        return format


def pickle_matpower_cases(case_paths, case_format=2):
    """ Parses the MATPOWER case files at the given paths and pickles the
        resulting Case objects to the same directory.
    """
    import pylon.io
    if isinstance(case_paths, basestring):
        case_paths = [
         case_paths]
    for case_path in case_paths:
        case = pylon.io.MATPOWERReader(case_format).read(case_path)
        dir_path = os.path.dirname(case_path)
        case_basename = os.path.basename(case_path)
        (root, _) = os.path.splitext(case_basename)
        pickled_case_path = os.path.join(dir_path, root + '.pkl')
        pylon.io.PickleWriter(case).write(pickled_case_path)


def feq(a, b, diff=1e-08):
    if abs(a - b) < diff:
        return 1
    else:
        return 0


def mfeq1(a, b, diff=1e-12):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        ai, bi = a[i], b[i]
        if ai == Inf and bi == Inf:
            continue
        elif ai == -Inf and bi == -Inf:
            continue
        else:
            if feq(a[i], b[i], diff) == False:
                return False
            continue

    return True


def mfeq2(a, b, diff=1e-12):
    if a.shape != b.shape:
        return False
    (rows, cols) = a.shape
    for i in range(rows):
        for j in range(cols):
            if feq(a[(i, j)], b[(i, j)], diff) == False:
                return False

    return True


def fair_max(x):
    """ Takes a single iterable as an argument and returns the same output as
    the built-in function max with two output parameters, except that where
    the maximum value occurs at more than one position in the  vector, the
    index is chosen randomly from these positions as opposed to just choosing
    the first occurance.
    """
    value = max(x)
    i = [ x.index(v) for v in x if v == value ]
    idx = random.choice(i)
    return (
     idx, value)


def factorial(n):
    """ Returns the factorial of n.
    """
    f = 1
    while n > 0:
        f = f * n
        n = n - 1

    return f


class CaseReport(object):

    def __init__(self, case):
        self.case = case

    @property
    def n_buses(self):
        return len(self.case.buses)

    @property
    def n_connected_buses(self):
        return len(self.case.connected_buses)

    @property
    def n_generators(self):
        return len([ g for g in self.case.generators if not g.is_load ])

    @property
    def online_generators(self):
        return [ g for g in self.case.generators if not g.is_load if g.online ]

    @property
    def n_online_generators(self):
        return len(self.online_generators)

    @property
    def n_loads(self):
        return self.n_fixed_loads + self.n_online_vloads

    @property
    def n_fixed_loads(self):
        return len([ b for b in self.case.buses if b.p_demand or b.q_demand ])

    @property
    def online_vloads(self):
        return [ g for g in self.case.generators if g.is_load if g.online ]

    @property
    def n_online_vloads(self):
        return len(self.online_vloads)

    @property
    def n_shunts(self):
        return len([ b for b in self.case.buses if b.g_shunt or b.b_shunt ])

    @property
    def interties(self):
        return [ l for l in self.case.branches if l.from_bus.area != l.to_bus.area
               ]

    @property
    def n_interties(self):
        return len(self.interties)

    @property
    def n_areas(self):
        s_areas = set([ b.area for b in self.case.buses ])
        return len(s_areas)

    @property
    def n_branches(self):
        return len(self.case.branches)

    @property
    def n_transformers(self):
        return len([ e for e in self.case.branches if e.ratio != 0.0 ])

    @property
    def total_pgen_capacity(self):
        return sum([ g.p_max for g in self.case.generators ])

    @property
    def total_qgen_capacity(self):
        q_min = sum([ g.q_min for g in self.case.generators ])
        q_max = sum([ g.q_max for g in self.case.generators ])
        return (q_min, q_max)

    @property
    def online_pgen_capacity(self):
        return sum([ g.p_max for g in self.online_generators ])

    @property
    def online_qgen_capacity(self):
        q_min = sum([ g.q_min for g in self.online_generators ])
        q_max = sum([ g.q_max for g in self.online_generators ])
        return (q_min, q_max)

    @property
    def actual_pgen(self):
        return sum([ g.p for g in self.online_generators ])

    @property
    def actual_qgen(self):
        return sum([ g.q for g in self.online_generators ])

    @property
    def fixed_p_demand(self):
        return sum([ bus.p_demand for bus in self.case.buses ])

    @property
    def fixed_q_demand(self):
        return sum([ bus.q_demand for bus in self.case.buses ])

    @property
    def vload_p_demand(self):
        p = -sum([ g.p for g in self.online_vloads ])
        p_min = -sum([ g.p_min for g in self.online_vloads ])
        return (p, p_min)

    @property
    def vload_q_demand(self):
        return -sum([ g.q for g in self.online_vloads ])

    @property
    def p_demand(self):
        return self.fixed_p_demand + self.vload_p_demand[0]

    @property
    def q_demand(self):
        return self.fixed_q_demand + self.vload_q_demand

    @property
    def shunt_pinj(self):
        pinj = 0.0
        for bus in self.case.buses:
            if bus.g_shunt or bus.b_shunt:
                pinj += bus.v_magnitude ** 2 * bus.g_shunt

        return pinj

    @property
    def shunt_qinj(self):
        qinj = 0.0
        for bus in self.case.buses:
            if bus.g_shunt or bus.b_shunt:
                qinj += bus.v_magnitude ** 2 * bus.b_shunt

        return qinj

    def _loss(self):
        base_mva = self.case.base_mva
        buses = self.case.buses
        branches = self.case.branches
        tap = ones(len(branches))
        i_trx = [ l._i for l in branches if l.ratio != 0.0 ]
        if len(i_trx) > 0:
            tap[i_trx] = array([ e.ratio for e in branches ])[i_trx]
        Vm = array([ bus.v_magnitude for bus in buses ])
        Va = array([ bus.v_angle * (pi / 180.0) for bus in buses ])
        V = Vm * exp(complex(0.0, 1.0) * Va)
        loss = array([ abs(V[l.from_bus._i] / tap[l._i] - V[l.to_bus._i]) ** 2 / (l.r - complex(0.0, 1.0) * l.x) * base_mva for l in branches
                     ])
        return loss

    @property
    def losses(self):
        loss = self._loss()
        return (sum(loss.real), sum(loss.imag))

    @property
    def branch_qinj(self):
        base_mva = self.case.base_mva
        buses = self.case.buses
        branches = self.case.branches
        tap = ones(len(branches))
        i_trx = [ l._i for l in branches if l.ratio != 0.0 ]
        if len(i_trx) > 0:
            tap[i_trx] = array([ e.ratio for e in branches ])[i_trx]
        Vm = array([ bus.v_magnitude for bus in buses ])
        Va = array([ bus.v_angle * (pi / 180.0) for bus in buses ])
        V = Vm * exp(complex(0.0, 1.0) * Va)
        fchg = array([ abs(V[l.from_bus._i] / tap[l._i]) ** 2 * l.b * base_mva / 2 for l in branches
                     ])
        tchg = array([ abs(V[l.to_bus._i]) ** 2 * l.b * base_mva / 2 for l in branches
                     ])
        return sum(fchg) + sum(tchg)

    @property
    def total_tie_pflow(self):
        return sum([ abs(t.p_from - t.p_to) for t in self.interties ]) / 2.0

    @property
    def total_tie_qflow(self):
        return sum([ abs(t.q_from - t.q_to) for t in self.interties ]) / 2.0

    @property
    def min_v_magnitude(self):
        Vm = [ bus.v_magnitude for bus in self.case.buses ]
        (min_v, min_i) = min(izip(Vm, count()))
        return (min_v, min_i)

    @property
    def max_v_magnitude(self):
        Vm = [ bus.v_magnitude for bus in self.case.buses ]
        (max_v, max_i) = max(izip(Vm, count()))
        return (max_v, max_i)

    @property
    def min_v_angle(self):
        Va = [ bus.v_angle for bus in self.case.buses ]
        (min_v, min_i) = min(izip(Va, count()))
        return (min_v, min_i)

    @property
    def max_v_angle(self):
        Va = [ bus.v_angle for bus in self.case.buses ]
        (max_v, max_i) = max(izip(Va, count()))
        return (max_v, max_i)

    @property
    def max_p_losses(self):
        branches = self.case.branches
        p_loss = self._loss().real
        (max_v, max_i) = max(izip(p_loss, count()))
        return (max_v, branches[max_i].from_bus._i, branches[max_i].to_bus._i)

    @property
    def max_q_losses(self):
        branches = self.case.branches
        q_loss = self._loss().imag
        (max_v, max_i) = max(izip(q_loss, count()))
        return (max_v, branches[max_i].from_bus._i, branches[max_i].to_bus._i)

    @property
    def min_p_lambda(self):
        p_lmbda = [ bus.p_lmbda for bus in self.case.buses ]
        (min_v, min_i) = min(izip(p_lmbda, count()))
        return (min_v, min_i)

    @property
    def max_p_lmbda(self):
        p_lmbda = [ bus.p_lmbda for bus in self.case.buses ]
        (max_v, max_i) = max(izip(p_lmbda, count()))
        return (max_v, max_i)

    @property
    def min_q_lmbda(self):
        q_lmbda = [ bus.q_lmbda for bus in self.case.buses ]
        (min_v, min_i) = min(izip(q_lmbda, count()))
        return (min_v, min_i)

    @property
    def max_q_lmbda(self):
        q_lmbda = [ bus.q_lmbda for bus in self.case.buses ]
        (max_v, max_i) = max(izip(q_lmbda, count()))
        return (max_v, max_i)
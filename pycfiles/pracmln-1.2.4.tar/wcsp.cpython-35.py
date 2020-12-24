# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/wcsp/wcsp.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 18037 bytes
import sys, os
from subprocess import Popen, PIPE
import bisect, re
from collections import defaultdict
import _thread, platform
from dnutils import logs
from ..utils import locs
from ..mln.errors import NoConstraintsError
import tempfile
from functools import reduce
logger = logs.getlogger(__name__)

class MaxCostExceeded(Exception):
    pass


toulbar_version = '0.9.7.0'

def is_executable_win(program):

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    if not program.endswith('.exe'):
        program += '.exe'
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file


def is_executable_unix(path):
    if os.path.exists(path) and os.access(path, os.X_OK):
        return path
    else:
        return


def is_executable(path):
    return is_executable_unix(path) or is_executable_win(path)


def toulbar2_path():
    osname, _, _, _, arch, _ = platform.uname()
    execname = 'toulbar2'
    en = is_executable(execname)
    if en is not None:
        return en
    if osname == 'Windows':
        execname += '.exe'
    return os.path.join('3rdparty', 'toulbar2-{}'.format(toulbar_version), arch, osname, execname)


_tb2path = os.path.join(locs.app_data, toulbar2_path())
if not is_executable(_tb2path):
    logger.error('toulbar2 was expected to be in {} but cannot be found. WCSP inference will not be possible.\n'.format(_tb2path))

class Constraint(object):
    __doc__ = '\n    Represents a a constraint in WCSP problem consisting of\n    a range of variables (indices), a set tuples with each\n    assigned costs and default costs. Costs are either a real\n    valued non-negative weight or the WCSP.TOP constant\n    indicating global inconsistency.\n    \n    :member tuples:     dictionary mapping a tuple to int (the costs)\n    :member defcost:    the default cost of this constraint\n    :param variables:   list of indices that identify the range of this constraint\n    :param tuples:      (optional) list of tuples, where the last element of each\n                        tuple specifies the costs for this assignment.\n    :param defcost:     the default costs (if none of the tuples apply).\n    '

    def __init__(self, variables, tuples=None, defcost=0):
        self.tuples = dict()
        if tuples is not None:
            for t in tuples:
                self.tuples[tuple(t[:-1])] = t[(-1)]

        self.defcost = defcost
        self.variables = variables

    def tuple(self, t, cost):
        """
        Adds a tuple to the constraint. A value in the tuple corresponds to the
        index of the value in the domain of the respective variable.
        """
        if not len(t) == len(self.variables):
            print('tuple:', t)
            print('vars:', self.variables)
            raise Exception('List of variables and tuples must have the same length.')
        self.tuples[tuple(t)] = cost

    def write(self, stream=sys.stdout.buffer):
        stream.write('{} {} {} {}\n'.format(len(self.variables), ' '.join(map(str, self.variables)), self.defcost, len(self.tuples)).encode())
        for t in list(self.tuples.keys()):
            stream.write('{} {}\n'.format(' '.join(map(str, t)), self.tuples[t]).encode())

    def __eq__(self, other):
        eq = set(self.variables) == set(other.variables)
        eq = eq and self.defcost == other.defcost
        eq = eq and self.tuples == other.tuples
        return eq


class WCSP(object):
    __doc__ = '\n    Represents a WCSP problem.\n    \n    This class implements a wrapper around the `toulbar2` weighted-SAT solver.\n    \n    :member name:        (arbitrary) name of the problem\n    :member domsizes:    list of domain sizes\n    :member top:         maximal costs (entirely inconsistent worlds)\n    :member constraints: list of :class:`Constraint` objects\n    '
    MAX_COST = 1537228672809129301

    def __init__(self, name=None, domsizes=None, top=-1):
        self.name = name
        self.domsizes = domsizes
        self.top = top
        self.constraints = {}

    def constraint(self, constraint):
        """
        Adds the given constraint to the WCSP. If a constraint 
        with the same scope already exists, the tuples of the
        new constraint are merged with the existing ones.
        """
        varindices = constraint.variables
        cold = self.constraints.get(tuple(sorted(varindices)))
        if cold is not None:
            c_ = Constraint(cold.variables, defcost=constraint.defcost)
            for t, cost in constraint.tuples.items():
                t = [t[constraint.variables.index(v)] for v in cold.variables]
                c_.tuple(t, cost)

            constraint = c_
            varindices = constraint.variables
            for t, cost in constraint.tuples.items():
                oldcost = cold.tuples.get(t, None)
                if not oldcost == self.top:
                    if oldcost is None and cold.defcost == self.top:
                        pass
                    else:
                        if oldcost is not None:
                            cold.tuple(t, self.top if cost == self.top else cost + oldcost)
                        else:
                            cold.tuple(t, self.top if cost == self.top else cost + cold.defcost)

            if constraint.defcost != 0:
                for t in [x for x in cold.tuples if x not in constraint.tuples]:
                    oldcost = cold.tuples[t]
                    if oldcost != self.top:
                        cold.tuple(t, self.top if constraint.defcost == self.top else oldcost + constraint.defcost)

                if cold.defcost != self.top:
                    cold.defcost = self.top if constraint.defcost == self.top else cold.defcost + constraint.defcost
            if reduce(lambda x, y: x * y, [self.domsizes[x] for x in varindices]) == len(cold.tuples):
                cost2assignments = defaultdict(list)
                for t, c in cold.tuples.items():
                    cost2assignments[c].append(t)

                defaultCost = max(cost2assignments, key=lambda x: len(cost2assignments[x]))
                del cost2assignments[defaultCost]
                cold.defcost = defaultCost
                cold.tuples = {}
                for cost, tuples in cost2assignments.items():
                    for t in tuples:
                        cold.tuple(t, cost)

        else:
            self.constraints[tuple(sorted(varindices))] = constraint

    def write(self, stream=sys.stdout.buffer):
        """
        Writes the WCSP problem in WCSP format into an arbitrary stream
        providing a write method.
        """
        self._make_integer_cost()
        stream.write('{} {} {} {} {}\n'.format(self.name, len(self.domsizes), max(self.domsizes), len(self.constraints), int(self.top)).encode())
        stream.write('{}\n'.format(' '.join(map(str, self.domsizes))).encode())
        for c in list(self.constraints.values()):
            stream.write('{} {} {} {}\n'.format(len(c.variables), ' '.join(map(str, c.variables)), c.defcost, len(c.tuples)).encode())
            for t in list(c.tuples.keys()):
                stream.write('{} {}\n'.format(' '.join(map(str, t)), int(c.tuples[t])).encode())

    def read(self, stream):
        """
        Loads a WCSP problem from an arbitrary stream. Must be in the WCSP format.
        """
        tuplesToRead = 0
        for i, line in enumerate(stream.readlines()):
            tokens = line.split()
            if i == 0:
                self.name = tokens[0]
                self.top = int(tokens[(-1)])
            elif i == 1:
                self.domsizes = list(map(int, tokens))
            elif tuplesToRead == 0:
                tuplesToRead = int(tokens[(-1)])
                variables = list(map(int, tokens[1:-2]))
                defcost = int(tokens[(-2)])
                constraint = Constraint(variables, defcost=defcost)
                self.constraints.append(constraint)
            else:
                constraint.tuple(list(map(int, tokens[0:-1])), int(tokens[(-1)]))
                tuplesToRead -= 1

    def _compute_divisor(self):
        """
        Computes a divisor for making all constraint costs integers.
        """
        costs = []
        minWeight = None
        if len(self.constraints) == 0:
            raise NoConstraintsError('There are no satisfiable constraints.')
        for constraint in list(self.constraints.values()):
            for value in [constraint.defcost] + list(constraint.tuples.values()):
                if value == self.top:
                    pass
                else:
                    value = eval('{:.6f}'.format(value))
                    if value in costs:
                        pass
                    else:
                        bisect.insort(costs, value)
                        if (minWeight is None or value < minWeight) and value > 0:
                            minWeight = value

        if minWeight is None:
            return
        deltaMin = None
        w1 = costs[0]
        if len(costs) == 1:
            deltaMin = costs[0]
        for w2 in costs[1:]:
            diff = w2 - w1
            if deltaMin is None or diff < deltaMin:
                deltaMin = diff
            w1 = w2

        divisor = 1.0
        if minWeight < 1.0:
            divisor *= minWeight
        if deltaMin < 1.0:
            divisor *= deltaMin
        return divisor

    def _compute_hardcost(self, divisor):
        """
        Computes the costs for hard constraints that determine
        costs for entirely inconsistent worlds (0 probability).
        """
        if divisor is None:
            return 1
        costSum = int(0)
        for constraint in list(self.constraints.values()):
            maxCost = max([constraint.defcost] + list(constraint.tuples.values()))
            if not maxCost == self.top:
                if maxCost == 0.0:
                    pass
                else:
                    cost = abs(int(maxCost / divisor))
                    newSum = costSum + cost
                    if newSum < costSum:
                        raise Exception('Numeric Overflow')
                    costSum = newSum

        top = costSum + 1
        if top < costSum:
            raise Exception('Numeric Overflow')
        if top > WCSP.MAX_COST:
            logger.critical('Maximum costs exceeded: {} > {}'.format(top, WCSP.MAX_COST))
            raise MaxCostExceeded()
        return int(top)

    def _make_integer_cost(self):
        """
        Returns a new WCSP problem instance, which is semantically
        equivalent to the original one, but whose costs have been converted
        to integers.
        """
        if self.top != -1:
            return
        divisor = self._compute_divisor()
        top = self._compute_hardcost(divisor)
        for constraint in list(self.constraints.values()):
            if constraint.defcost == self.top:
                constraint.defcost = top
            else:
                constraint.defcost = 0 if divisor is None else int(float(constraint.defcost) / divisor)
            for tup, cost in constraint.tuples.items():
                if cost == self.top:
                    constraint.tuples[tup] = top
                else:
                    constraint.tuples[tup] = 0 if divisor is None else int(float(cost) / divisor)

        self.top = top

    def itersolutions(self):
        """
        Iterates over all (intermediate) solutions found.
        
        Intermediate solutions are sound variable assignments that may not necessarily
        be gloabally optimal.
        
        :returns:    a generator of (idx, solution) tuples, where idx is the index and solution is a tuple
                     of variable value indices.
        """
        if not is_executable(_tb2path):
            raise Exception('toulbar2 cannot be found.')
        tmpfile = tempfile.NamedTemporaryFile(prefix=os.getpid(), suffix='.wcsp', delete=False)
        wcspfilename = tmpfile.name
        self.write(stream=tmpfile)
        tmpfile.close()
        cmd = '%s -s -a %s' % (_tb2path, wcspfilename)
        logger.debug('solving WCSP...')
        p = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        solution = None
        while 1:
            l = p.stdout.readline().strip()
            if not l:
                break
            m = re.match('(\\d+)\\s+solution:([\\s\\d]+)', l)
            if m is not None:
                num = m.group(1)
                solution = list(map(int, m.group(2).strip().split()))
                yield (num, solution)

        p.wait()
        logger.debug('toulbar2 process returned {}'.format(str(p.returncode)))
        try:
            os.remove(wcspfilename)
        except OSError:
            logger.warning('could not remove temporary file {}'.format(wcspfilename))

        if p.returncode != 0:
            raise Exception('toulbar2 returned a non-zero exit code: {}'.format(p.returncode))

    def solve(self):
        """
        Uses toulbar2 inference. Returns the best solution, i.e. a tuple
        of variable assignments.
        """
        if not is_executable(_tb2path):
            raise Exception('toulbar2 cannot be found.')
        tmpfile = tempfile.NamedTemporaryFile(prefix='{}-{}'.format(os.getpid(), _thread.get_ident()), suffix='.wcsp', delete=False)
        wcspfilename = tmpfile.name
        self.write(stream=tmpfile)
        tmpfile.close()
        cmd = '"%s" -s %s' % (_tb2path, wcspfilename)
        logger.debug('solving WCSP...')
        p = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
        solution = None
        nextLineIsSolution = False
        cost = None
        while 1:
            l = p.stdout.readline()
            if not l:
                break
            if l.startswith(b'New solution'):
                cost = int(l.split()[2])
                nextLineIsSolution = True
                continue
                if nextLineIsSolution:
                    solution = list(map(int, l.split()))
                    nextLineIsSolution = False

        p.wait()
        logger.debug('toulbar2 process returned {}'.format(str(p.returncode)))
        try:
            os.remove(wcspfilename)
        except OSError:
            logger.warning('could not remove temporary file {}'.format(wcspfilename))

        if p.returncode != 0:
            raise Exception('toulbar2 returned a non-zero exit code: {}'.format(p.returncode))
        return (
         solution, cost)


if __name__ == '__main__':
    wcsp = WCSP()
    wcsp.read(open('/home/nyga/code/test/nqueens.wcsp', 'rb'))
    for i, s in wcsp.itersolutions():
        print(i, s)

    print('best solution:', wcsp.solve())
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/mrfvars.py
# Compiled at: 2018-04-24 04:48:32
from dnutils import ifnone
from pracmln.mln.errors import MRFValueException
from pracmln.mln.util import Interval

class MRFVariable(object):
    """
    Represents a (mutually exclusive) block of ground atoms.
    
    This is the base class for different types of variables an MRF
    may consist of, e.g. mutually exclusive ground atoms. The purpose
    of these variables is to provide some convenience methods for 
    easy iteration over their values ("possible worlds") and to ease
    introduction of new types of variables in an MRF.
    
    The values of a variable should have a fixed order, so every value
    must have a fixed index.
    """

    def __init__(self, mrf, name, predicate, *gndatoms):
        """
        :param mrf:         the instance of the MRF that this variable is added to
        :param name:        the readable name of the variable
        :param predicate:   the :class:`mln.base.Predicate` instance of this variable
        :param gndatoms:    the ground atoms constituting this variable
        """
        self.mrf = mrf
        self.gndatoms = list(gndatoms)
        self.idx = len(mrf.variables)
        self.name = name
        self.predicate = predicate

    def atomvalues(self, value):
        """
        Returns a generator of (atom, value) pairs for the given variable value
        
        :param value:     a tuple of truth values
        """
        for atom, val in zip(self.gndatoms, value):
            yield (
             atom, val)

    def iteratoms(self):
        """
        Yields all ground atoms in this variable, sorted by atom index ascending
        """
        for atom in sorted(self.gndatoms, key=lambda a: a.idx):
            yield atom

    def strval(self, value):
        """
        Returns a readable string representation for the value tuple given by `value`.
        """
        return '<%s>' % (', ').join(map(--- This code section failed: ---

 L.  78         0  LOAD_FAST             0  '.0'
                3  UNPACK_SEQUENCE_2     2 
                6  STORE_FAST            1  'a'
                9  STORE_FAST            2  'v'
               12  LOAD_FAST             2  'v'
               15  LOAD_CONST               1
               18  COMPARE_OP            2  ==
               21  POP_JUMP_IF_FALSE    38  'to 38'
               24  LOAD_CONST               '%s'
               27  LOAD_GLOBAL           0  'str'
               30  LOAD_FAST             1  'a'
               33  CALL_FUNCTION_1       1  None
               36  BINARY_MODULO    
               37  RETURN_END_IF_LAMBDA
             38_0  COME_FROM            21  '21'
               38  LOAD_FAST             2  'v'
               41  LOAD_CONST               0
               44  COMPARE_OP            2  ==
               47  POP_JUMP_IF_FALSE    64  'to 64'
               50  LOAD_CONST               '!%s'
               53  LOAD_GLOBAL           0  'str'
               56  LOAD_FAST             1  'a'
               59  CALL_FUNCTION_1       1  None
               62  BINARY_MODULO    
               63  RETURN_END_IF_LAMBDA
             64_0  COME_FROM            47  '47'
               64  LOAD_CONST               '?%s?'
               67  LOAD_GLOBAL           0  'str'
               70  LOAD_FAST             1  'a'
               73  CALL_FUNCTION_1       1  None
               76  BINARY_MODULO    
               77  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
, zip(self.gndatoms, value)))

    def valuecount(self, evidence=None):
        """
        Returns the number of values this variable can take.
        """
        raise Exception('%s does not implement valuecount()' % self.__class__.__name__)

    def _itervalues(self, evidence=None):
        """
        Generates all values of this variable as tuples of truth values.
        
        :param evidence: an optional dictionary mapping ground atoms to truth values.
        
        .. seealso:: values are given in the same format as in :method:`MRFVariable.itervalues()`
        """
        raise Exception('%s does not implement _itervalues()' % self.__class__.__name__)

    def valueidx(self, value):
        """
        Computes the index of the given value.
        
        .. seealso:: values are given in the same format as in :method:`MRFVariable.itervalues()`
        """
        raise Exception('%s does not implement valueidx()' % self.__class__.__name__)

    def evidence_value_index(self, evidence=None):
        """
        Returns the index of this atomic block value for the possible world given in `evidence`.
        
        .. seealso:: `MRFVariable.evidence_value()`
        """
        value = self.evidence_value(evidence)
        if any(map(lambda v: v is None, value)):
            return None
        else:
            return self.valueidx(tuple(value))

    def evidence_value(self, evidence=None):
        """
        Returns the value of this variable as a tuple of truth values
        in the possible world given by `evidence`.
        
        Exp: (0, 1, 0) for a mutex variable containing 3 gnd atoms
        
        :param evidence:   the truth values wrt. the ground atom indices. Can be a 
                           complete assignment of truth values (i.e. a list) or a dict
                           mapping ground atom indices to their truth values. If evidence is `None`,
                           the evidence vector of the MRF is taken.
        """
        if evidence is None:
            evidence = self.mrf.evidence
        value = []
        for gndatom in self.gndatoms:
            value.append(evidence[gndatom.idx])

        return tuple(value)

    def value2dict(self, value):
        """
        Takes a tuple of truth values and transforms it into a dict 
        mapping the respective ground atom indices to their truth values.
        
        :param value: the value tuple to be converted.
        """
        evidence = {}
        for atom, val in zip(self.gndatoms, value):
            evidence[atom.idx] = val

        return evidence

    def setval(self, value, world):
        """
        Sets the value of this variable in the world `world` to the given value.
        
        :param value:    tuple representing the value of the variable.
        :param world:    vector representing the world to be modified:
        :returns:        the modified world.  
        """
        for i, v in self.value2dict(value).iteritems():
            world[i] = v

        return world

    def itervalues(self, evidence=None):
        """
        Iterates over (idx, value) pairs for this variable.
        
        Values are given as tuples of truth values of the respective ground atoms. 
        For a binary variable (a 'normal' ground atom), for example, the two values 
        are represented by (0,) and (1,). If `evidence is` given, only values 
        matching the evidence values are generated.
        
        :param evidence:     an optional dictionary mapping ground atom indices to truth values.
        
                             .. warning:: ground atom indices are with respect to the mrf instance,
                                          not to the index of the gnd atom in the variable
                                           
        .. warning:: The values are not necessarily orderd with respect to their
                     actual index obtained by `MRFVariable.valueidx()`.
        
        """
        if type(evidence) is list:
            evidence = dict([ (i, v) for i, v in enumerate(evidence) ])
        for tup in self._itervalues(evidence):
            yield (
             self.valueidx(tup), tup)

    def values(self, evidence=None):
        """
        Returns a generator of possible values of this variable under consideration of
        the evidence given, if any.
        
        Same as ``itervalues()`` but without value indices.
        """
        for _, val in self.itervalues(evidence):
            yield val

    def iterworlds(self, evidence=None):
        """
        Iterates over possible worlds of evidence which can be generated with this variable.
        
        This does not have side effects on the `evidence`. If no `evidence` is specified,
        the evidence vector of the MRF is taken.
        
        :param evidence:     a possible world of truth values of all ground atoms in the MRF.
        :returns:            
        """
        if type(evidence) is not dict:
            raise Exception('evidence must be of type dict, is %s' % type(evidence))
        if evidence is None:
            evidence = self.mrf.evidence_dicti()
        for i, val in self.itervalues(evidence):
            world = dict(evidence)
            value = self.value2dict(val)
            world.update(value)
            yield (i, world)

        return

    def consistent(self, world, strict=False):
        """
        Checks for this variable if its assignment in the assignment `evidence` is consistent.
        
        :param evidence: the assignment to be checked.
        :param strict:   if True, no unknown assignments are allowed, i.e. there must not be any
                         ground atoms in the variable that do not have a truth value assigned.
        """
        total = 0
        evstr = (',').join([ ifnone(world[atom.idx], '?', str) for atom in self.gndatoms ])
        for gnatom in self.gndatoms:
            val = world[gnatom.idx]
            if strict and val is None:
                raise MRFValueException('Not all values have truth assignments: %s: %s' % (repr(self), evstr))
            total += ifnone(val, 0)

        if not (total == 1 if strict else total in Interval('[0,1]')):
            raise MRFValueException('Invalid value of variable %s: %s' % (repr(self), evstr))
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s "%s": [%s]>' % (self.__class__.__name__, self.name, (',').join(map(str, self.gndatoms)))

    def __contains__(self, element):
        return element in self.gndatoms


class FuzzyVariable(MRFVariable):
    """
    Represents a fuzzy ground atom that can take values of truth in [0,1].
    
    It does not support iteration over values or value indexing.
    """

    def consistent(self, world, strict=False):
        value = self.evidence_value(world)[0]
        if value is not None:
            if value >= 0 and value <= 1:
                return True
            raise MRFValueException('Invalid value of variable %s: %s' % (repr(self), value))
        elif strict:
            raise MRFValueException('Invalid value of variable %s: %s' % (repr(self), value))
        else:
            return True
        return

    def valuecount(self, evidence=None):
        if evidence is None or evidence[self.gndatoms[0].idx] is None:
            raise MRFValueException('Cannot count number of values of an unassigned FuzzyVariable: %s' % str(self))
        else:
            return 1
        return

    def itervalues(self, evidence=None):
        if evidence is None or evidence[self.gndatoms[0].idx] is None:
            raise MRFValueException('Cannot iterate over values of fuzzy variables: %s' % str(self))
        else:
            yield (
             None, (evidence[self.gndatoms[0].idx],))
        return


class BinaryVariable(MRFVariable):
    """
    Represents a binary ("normal") ground atom with the two truth values 1 (true) and 0 (false).
    The first value is always the false one.
    """

    def valuecount(self, evidence=None):
        if evidence is None:
            return 2
        else:
            return len(list(self.itervalues(evidence)))
            return

    def _itervalues(self, evidence=None):
        if evidence is None:
            evidence = {}
        if len(self.gndatoms) != 1:
            raise Exception('Illegal number of ground atoms in the variable %s' % repr(self))
        gndatom = self.gndatoms[0]
        if evidence.get(gndatom.idx) is not None and evidence.get(gndatom.idx) in (0,
                                                                                   1):
            yield (
             evidence[gndatom.idx],)
            return
        else:
            for t in (0, 1):
                yield (
                 t,)

            return

    def valueidx(self, value):
        if value == (0, ):
            return 0
        if value == (1, ):
            return 1
        raise MRFValueException('Invalid world value for binary variable %s: %s' % (str(self), str(value)))

    def consistent(self, world, strict=False):
        val = world[self.gndatoms[0].idx]
        if strict and val is None:
            raise MRFValueException('Invalid value of variable %s: %s' % (repr(self), val))
        return


class MutexVariable(MRFVariable):
    """
    Represents a mutually exclusive block of ground atoms, i.e. a block
    in which exactly one ground atom must be true.
    """

    def valuecount(self, evidence=None):
        if evidence is None:
            return len(self.gndatoms)
        else:
            return len(list(self.itervalues(evidence)))
            return

    def _itervalues(self, evidence=None):
        if evidence is None:
            evidence = {}
        atomindices = map(lambda a: a.idx, self.gndatoms)
        valpattern = []
        for mutexatom in atomindices:
            valpattern.append(evidence.get(mutexatom, None))

        trues = sum(filter(lambda x: x == 1, valpattern))
        if trues > 1:
            raise MRFValueException('More than one ground atom in mutex variable is true: %s' % str(self))
        if trues == 1:
            yield tuple(map(lambda x: 1 if x == 1 else 0, valpattern))
            return
        else:
            if all([ x == 0 for x in valpattern ]):
                raise MRFValueException('Illegal value for a MutexVariable %s: %s' % (self, valpattern))
            for i, val in enumerate(valpattern):
                if val == 0:
                    continue
                elif val is None:
                    values = [
                     0] * len(valpattern)
                    values[i] = 1
                    yield tuple(values)

            return

    def valueidx(self, value):
        if sum(value) != 1:
            raise MRFValueException('Invalid world value for mutex variable %s: %s' % (str(self), str(value)))
        else:
            return value.index(1)


class SoftMutexVariable(MRFVariable):
    """
    Represents a soft mutex block of ground atoms, i.e. a mutex block in which maximally
    one ground atom may be true.
    """

    def valuecount(self, evidence=None):
        if evidence is None:
            return len(self.gndatoms) + 1
        else:
            return len(list(self.itervalues(evidence)))
            return

    def _itervalues(self, evidence=None):
        if evidence is None:
            evidence = {}
        atomindices = map(lambda a: a.idx, self.gndatoms)
        valpattern = []
        for mutexatom in atomindices:
            valpattern.append(evidence.get(mutexatom, None))

        trues = sum(filter(lambda x: x == 1, valpattern))
        if trues > 1:
            raise Exception('More than one ground atom in mutex variable is true: %s' % str(self))
        if trues == 1:
            yield tuple(map(lambda x: 1 if x == 1 else 0, valpattern))
            return
        else:
            for i, val in enumerate(valpattern):
                if val == 0:
                    continue
                elif val is None:
                    values = [
                     0] * len(valpattern)
                    values[i] = 1
                    yield tuple(values)

            yield tuple([0] * len(atomindices))
            return

    def valueidx(self, value):
        if sum(value) > 1:
            raise Exception('Invalid world value for soft mutex block %s: %s' % (str(self), str(value)))
        else:
            if sum(value) == 1:
                return value.index(1) + 1
            else:
                return 0
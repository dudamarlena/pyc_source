# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lancelot/specs/specification_spec.py
# Compiled at: 2009-02-20 10:37:54
""" Specs for core library classes / behaviours """
from lancelot import Spec, verifiable, verify
from lancelot.calling import WrapFunction
from lancelot.comparators import Type, Length
from lancelot.verification import UnmetSpecification
from lancelot.specs.simple_fns import dont_raise_index_error, number_one, raise_index_error, string_abc

@verifiable
def atomic_raise_behaviour():
    """ should_raise() and should_not_raise() are the only 
    "atomic" parts that require test assertions. All other 
    functionality can be bootstrap-specified using these methods. """
    spec1 = Spec(dont_raise_index_error)
    try:
        spec1.dont_raise_index_error().should_raise(IndexError)
        assert False
    except UnmetSpecification:
        pass

    spec2 = Spec(raise_index_error)
    try:
        spec2.raise_index_error().should_not_raise(IndexError)
        assert False
    except UnmetSpecification:
        pass

    spec2 = Spec(raise_index_error)
    try:
        spec2.raise_index_error().should_raise(ValueError)
        assert False
    except IndexError:
        pass


@verifiable
def should_be_value_behaviour():
    """ Basic specification of the Spec.should...() methods"""
    spec = Spec(number_one)
    spec.number_one().should_be(1)
    spec.number_one().should_not_be(2)
    spec.number_one().should_not_be('a')
    spec = Spec(string_abc)
    spec.string_abc().should_be('abc')
    spec.string_abc().should_not_be('a')
    spec.string_abc().should_not_be(2)


@verifiable
def given_when_then_behaviour():
    """ given empty list when item appended then list length should be one """
    spec = Spec([])
    spec.when(spec.append(object())).then(spec.it()).should_be(Length(1))

    def empty_list():
        """ descriptive name for fn returning an empty list """
        return []

    spec = Spec(type([]), given=empty_list)
    spec.when(spec.append('monty')).then(spec.it()).should_be(Length(1))


@verifiable
def given_typechecking_behaviour():
    """ Spec for check that given=... is correct type """

    def spec_for_dict_given_empty_list():
        """ callable method to defer instance creation until within Spec """
        return Spec(type({}), given=lambda : [])

    spec = Spec(spec_for_dict_given_empty_list)
    type_error = TypeError("[] is not instance of <type 'dict'>")
    spec.__call__().should_raise(type_error)


@verifiable
def spec_getattr_behaviour():
    """ getattr from spec should return wrapper for unknown attributes """
    spec = Spec(lambda : getattr(Spec('grail'), 'should'))
    spec.__call__().should_not_be(Type(WrapFunction))
    spec = Spec(lambda : getattr(Spec('life'), 'death'))
    spec.__call__().should_be(Type(WrapFunction))


@verifiable
def external_then_behaviour():
    """ Spec for then()... actions that call outside the spec itself.
    
    Note that the action on the spec is invoked in client code with parens():
        spec.then( * spec.__len__() * ).should_be(1)
        
    but the action outside the spec is NOT:
        spec.then( * 'they called him brian'.__len__ * ).should_be(21) 
    """
    spec = Spec([])
    spec.when(spec.append('brian'))
    spec.then(spec.__len__()).should_be(1)
    spec.then(('they called him brian').__len__).should_be(21)


@verifiable
def should_contain_behaviour():
    """ should_ and should_not_ contain methods delegate to Contain """
    spec = Spec(['brave', 'brave', 'sir robin'])
    spec.it().should_contain('brave')
    spec.it().should_not_contain('bravely ran away')


@verifiable
def should_raise_optional_args():
    """ should_raise and should_not_raise should not require args, and if
    no args are specified then the catch-all value of Exception is assumed """
    Spec(raise_index_error).raise_index_error().should_raise()
    Spec(dont_raise_index_error).dont_raise_index_error().should_not_raise()


if __name__ == '__main__':
    verify()
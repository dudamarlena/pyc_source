# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/wheel/symengine/tests/test_number.py
# Compiled at: 2020-03-16 01:41:57
from symengine.utilities import raises
from symengine import Integer, I, S, pi
from symengine.lib.symengine_wrapper import perfect_power, is_square, integer_nthroot

def test_integer():
    i = Integer(5)
    assert str(i) == '5'
    assert int(i) == 5
    assert float(i) == 5.0
    assert complex(i) == complex(5.0, 0.0)
    assert i.real == i
    assert i.imag == S.Zero


def test_integer_long():
    py_int = 123434444444444444444
    i = Integer(py_int)
    assert str(i) == str(py_int)
    assert int(i) == py_int


def test_integer_string():
    assert Integer('133') == 133


def test_rational():
    i = Integer(5) / 10
    assert str(i) == '1/2'
    assert int(i) == 0
    assert float(i) == 0.5
    assert complex(i) == complex(0.5, 0.0)
    assert i.real == i
    assert i.imag == S.Zero


def test_complex():
    i = Integer(5) / 10 + I
    assert str(i) == '1/2 + I'
    assert complex(i) == complex(0.5, 1.0)
    assert i.real == Integer(1) / 2
    assert i.imag == 1
    i = 0.5 + I
    assert str(i) == '0.5 + 1.0*I'
    assert complex(i) == complex(0.5, 1.0)
    assert i.real == 0.5
    assert i.imag == 1.0


def test_smallfloat_valid():
    i = Integer(7.5)
    assert str(i) == '7'


def test_bigfloat_valid():
    i = Integer(1.3333333333333334e+16)
    assert str(i) == '13333333333333334'


def test_is_conditions():
    i = Integer(-123)
    assert not i.is_zero
    assert not i.is_positive
    assert i.is_negative
    assert i.is_nonzero
    assert i.is_nonpositive
    assert not i.is_nonnegative
    assert not i.is_complex
    i = Integer(123)
    assert not i.is_zero
    assert i.is_positive
    assert not i.is_negative
    assert i.is_nonzero
    assert not i.is_nonpositive
    assert i.is_nonnegative
    assert not i.is_complex
    i = Integer(0)
    assert i.is_zero
    assert not i.is_positive
    assert not i.is_negative
    assert not i.is_nonzero
    assert i.is_nonpositive
    assert i.is_nonnegative
    assert not i.is_complex
    i = Integer(1) + I
    assert not i.is_zero
    assert not i.is_positive
    assert not i.is_negative
    assert not i.is_nonzero
    assert not i.is_nonpositive
    assert not i.is_nonnegative
    assert i.is_complex
    assert pi.is_number


def test_perfect_power():
    assert perfect_power(1) == True
    assert perfect_power(7) == False
    assert perfect_power(8) == True
    assert perfect_power(9) == True
    assert perfect_power(10) == False
    assert perfect_power(1024) == True
    assert perfect_power(1025) == False
    assert perfect_power(279936) == True
    assert perfect_power(-27) == True
    assert perfect_power(-64) == True
    assert perfect_power(-32) == True


def test_perfect_square():
    assert is_square(7) == False
    assert is_square(8) == False
    assert is_square(9) == True
    assert is_square(10) == False
    assert perfect_power(49) == True
    assert perfect_power(50) == False


def test_integer_nthroot():
    assert integer_nthroot(1, 2) == (1, True)
    assert integer_nthroot(1, 5) == (1, True)
    assert integer_nthroot(2, 1) == (2, True)
    assert integer_nthroot(2, 2) == (1, False)
    assert integer_nthroot(2, 5) == (1, False)
    assert integer_nthroot(4, 2) == (2, True)
    assert integer_nthroot(17685925284953355608333258649989090388842388168292443, 25) == (123, True)
    assert integer_nthroot(17685925284953355608333258649989090388842388168292444, 25) == (123, False)
    assert integer_nthroot(17685925284953355608333258649989090388842388168292442, 25) == (122, False)
    assert integer_nthroot(1, 1) == (1, True)
    assert integer_nthroot(0, 1) == (0, True)
    assert integer_nthroot(0, 3) == (0, True)
    assert integer_nthroot(10000, 1) == (10000, True)
    assert integer_nthroot(4, 2) == (2, True)
    assert integer_nthroot(16, 2) == (4, True)
    assert integer_nthroot(26, 2) == (5, False)
    assert integer_nthroot(4371219837658380601508594259852871941768823, 7) == (1234567, True)
    assert integer_nthroot(4371219837658380601508594259852871941768824, 7) == (1234567, False)
    assert integer_nthroot(4371219837658380601508594259852871941768822, 7) == (1234566, False)
    b = 870980981621721667557619549477887229585910374270538861664349322949828885340626741378473875079978788106556408717745512063620430237198833632508279082452303686110151064231029731844770912338990942384805856374197234719063103709717102341338066824141470072823629277351483947365609114807773659084382927185815811948911134617256915670416545076575696978688296466624839314010926757566865640829864607020478209736583890745367167211108478699317026667107461706636187594713500639193851672095206666878678364305056913162755577282544319220234472829986232534712298259962687261646269421115058998416069587800908920579349669236736913827347448298397172895803277667115579753494052712115087421629797155964976280104903975345046567785695453426825434185295645428424293462112053395137460028538491546496267026898886434214356481725450758426045441108355790758165263762707637097797493609152464857349232178547471268908595592165403420696716220544097087042534305174783814271995118445411602119001993267698963158366035219345898069254813486663593971465352723605221893603623162344963023226799889023333175534301945815013863127729744770005798281812992166753266441172395445809353443716569909308297494243007169052124052051599106448566000604029261487881100463610822941645972134518552644715890683789506575861017698385432029210038002794322539542020752022213866641380472576754542153919782083275936648524549223149282539679916226305067539215087890625
    assert integer_nthroot(b, 1000) == (25, True)
    assert integer_nthroot(b + 1, 1000) == (25, False)
    assert integer_nthroot(b - 1, 1000) == (24, False)
    c = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    c2 = c ** 2
    assert integer_nthroot(c2, 2) == (c, True)
    assert integer_nthroot(c2 + 1, 2) == (c, False)
    assert integer_nthroot(c2 - 1, 2) == (c - 1, False)
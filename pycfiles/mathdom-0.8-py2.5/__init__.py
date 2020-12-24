# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/__init__.py
# Compiled at: 2005-10-21 11:29:12
MATHML_NAMESPACE_URI = 'http://www.w3.org/1998/Math/MathML'
UNARY_ARITHMETIC_FUNCTIONS = '\nfactorial minus abs conjugate arg real imaginary floor ceiling\n'
UNARY_LOGICAL_FUNCTIONS = '\nnot\n'
UNARY_ELEMENTARY_CLASSICAL_FUNCTIONS = '\nsin cos tan sec csc cot sinh cosh tanh sech csch coth\narcsin arccos arctan arccosh arccot arccoth arccsc arccsch\narcsec arcsech arcsinh arctanh exp ln log\n'
BINARY_ARITHMETIC_FUNCTIONS = '\nquotient divide minus power rem\n'
NARY_ARITHMETIC_FUNCTIONS = '\nplus times max min gcd lcm\n'
NARY_STATISTICAL_FUNCTIONS = '\nmean sdev variance median mode\n'
NARY_LOGICAL_FUNCTIONS = '\nand or xor\n'
NARY_FUNCTIONAL_FUNCTION = '\ncompose\n'
BINARY_SET_CONTAINMENT = '\nin notin\n'
BINARY_RELATIONS = '\nneq equivalent approx factorof\n'
NARY_RELATIONS = '\neq leq lt geq gt\n'
CONSTANTS = '\npi ExponentialE ee ImaginaryI ii gamma infin infty true false NotANumber NaN\n'
UNARY_FUNCTIONS = UNARY_ELEMENTARY_CLASSICAL_FUNCTIONS + UNARY_ARITHMETIC_FUNCTIONS + UNARY_LOGICAL_FUNCTIONS
BINARY_FUNCTIONS = BINARY_ARITHMETIC_FUNCTIONS + BINARY_SET_CONTAINMENT
NARY_FUNCTIONS = NARY_ARITHMETIC_FUNCTIONS + NARY_STATISTICAL_FUNCTIONS + NARY_LOGICAL_FUNCTIONS + NARY_FUNCTIONAL_FUNCTION
FUNCTIONS = UNARY_FUNCTIONS + BINARY_FUNCTIONS + NARY_FUNCTIONS
RELATIONS = BINARY_RELATIONS + NARY_RELATIONS + BINARY_SET_CONTAINMENT
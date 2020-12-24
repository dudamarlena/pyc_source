# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukas/work/development/gridcells/external/numpydoc/numpydoc/tests/test_docscrape.py
# Compiled at: 2014-03-29 16:39:55
# Size of source mod 2**32: 18326 bytes
from __future__ import division, absolute_import, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, textwrap
from numpydoc.docscrape import NumpyDocString, FunctionDoc, ClassDoc
from numpydoc.docscrape_sphinx import SphinxDocString, SphinxClassDoc
from nose.tools import *
if sys.version_info[0] >= 3:
    sixu = lambda s: s
else:
    sixu = lambda s: unicode(s, 'unicode_escape')
doc_txt = '  numpy.multivariate_normal(mean, cov, shape=None, spam=None)\n\n  Draw values from a multivariate normal distribution with specified\n  mean and covariance.\n\n  The multivariate normal or Gaussian distribution is a generalisation\n  of the one-dimensional normal distribution to higher dimensions.\n\n  Parameters\n  ----------\n  mean : (N,) ndarray\n      Mean of the N-dimensional distribution.\n\n      .. math::\n\n         (1+2+3)/3\n\n  cov : (N, N) ndarray\n      Covariance matrix of the distribution.\n  shape : tuple of ints\n      Given a shape of, for example, (m,n,k), m*n*k samples are\n      generated, and packed in an m-by-n-by-k arrangement.  Because\n      each sample is N-dimensional, the output shape is (m,n,k,N).\n\n  Returns\n  -------\n  out : ndarray\n      The drawn samples, arranged according to `shape`.  If the\n      shape given is (m,n,...), then the shape of `out` is is\n      (m,n,...,N).\n\n      In other words, each entry ``out[i,j,...,:]`` is an N-dimensional\n      value drawn from the distribution.\n  list of str\n      This is not a real return value.  It exists to test\n      anonymous return values.\n\n  Other Parameters\n  ----------------\n  spam : parrot\n      A parrot off its mortal coil.\n\n  Raises\n  ------\n  RuntimeError\n      Some error\n\n  Warns\n  -----\n  RuntimeWarning\n      Some warning\n\n  Warnings\n  --------\n  Certain warnings apply.\n\n  Notes\n  -----\n  Instead of specifying the full covariance matrix, popular\n  approximations include:\n\n    - Spherical covariance (`cov` is a multiple of the identity matrix)\n    - Diagonal covariance (`cov` has non-negative elements only on the diagonal)\n\n  This geometrical property can be seen in two dimensions by plotting\n  generated data-points:\n\n  >>> mean = [0,0]\n  >>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis\n\n  >>> x,y = multivariate_normal(mean,cov,5000).T\n  >>> plt.plot(x,y,\'x\'); plt.axis(\'equal\'); plt.show()\n\n  Note that the covariance matrix must be symmetric and non-negative\n  definite.\n\n  References\n  ----------\n  .. [1] A. Papoulis, "Probability, Random Variables, and Stochastic\n         Processes," 3rd ed., McGraw-Hill Companies, 1991\n  .. [2] R.O. Duda, P.E. Hart, and D.G. Stork, "Pattern Classification,"\n         2nd ed., Wiley, 2001.\n\n  See Also\n  --------\n  some, other, funcs\n  otherfunc : relationship\n\n  Examples\n  --------\n  >>> mean = (1,2)\n  >>> cov = [[1,0],[1,0]]\n  >>> x = multivariate_normal(mean,cov,(3,3))\n  >>> print x.shape\n  (3, 3, 2)\n\n  The following is probably true, given that 0.6 is roughly twice the\n  standard deviation:\n\n  >>> print list( (x[0,0,:] - mean) < 0.6 )\n  [True, True]\n\n  .. index:: random\n     :refguide: random;distributions, random;gauss\n\n  '
doc = NumpyDocString(doc_txt)

def test_signature():
    @py_assert0 = doc['Signature']
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'numpy.multivariate_normal('
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['Signature']
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'spam=None)'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_summary():
    @py_assert0 = doc['Summary'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Draw values'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['Summary'][(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'covariance.'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_extended_summary():
    @py_assert0 = doc['Extended Summary'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'The multivariate normal'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_parameters():
    assert_equal(len(doc['Parameters']), 3)
    assert_equal([n for n, _, _ in doc['Parameters']], ['mean', 'cov', 'shape'])
    arg, arg_type, desc = doc['Parameters'][1]
    assert_equal(arg_type, '(N, N) ndarray')
    @py_assert0 = desc[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Covariance matrix'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['Parameters'][0][(-1)][(-2)]
    @py_assert3 = '   (1+2+3)/3'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_other_parameters():
    assert_equal(len(doc['Other Parameters']), 1)
    assert_equal([n for n, _, _ in doc['Other Parameters']], ['spam'])
    arg, arg_type, desc = doc['Other Parameters'][0]
    assert_equal(arg_type, 'parrot')
    @py_assert0 = desc[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'A parrot off its mortal coil'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_returns():
    assert_equal(len(doc['Returns']), 2)
    arg, arg_type, desc = doc['Returns'][0]
    assert_equal(arg, 'out')
    assert_equal(arg_type, 'ndarray')
    @py_assert0 = desc[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'The drawn samples'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = desc[(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'distribution.'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    arg, arg_type, desc = doc['Returns'][1]
    assert_equal(arg, 'list of str')
    assert_equal(arg_type, '')
    @py_assert0 = desc[0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'This is not a real'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = desc[(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'anonymous return values.'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_notes():
    @py_assert0 = doc['Notes'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Instead'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['Notes'][(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'definite.'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    assert_equal(len(doc['Notes']), 17)
    return


def test_references():
    @py_assert0 = doc['References'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = '..'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['References'][(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = '2001.'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_examples():
    @py_assert0 = doc['Examples'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = '>>>'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = doc['Examples'][(-1)]
    @py_assert2 = @py_assert0.endswith
    @py_assert4 = 'True]'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.endswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_index():
    assert_equal(doc['index']['default'], 'random')
    assert_equal(len(doc['index']), 2)
    assert_equal(len(doc['index']['refguide']), 2)


def non_blank_line_by_line_compare(a, b):
    a = textwrap.dedent(a)
    b = textwrap.dedent(b)
    a = [l.rstrip() for l in a.split('\n') if l.strip()]
    b = [l.rstrip() for l in b.split('\n') if l.strip()]
    for n, line in enumerate(a):
        if not line == b[n]:
            raise AssertionError('Lines %s of a and b differ: \n>>> %s\n<<< %s\n' % (
             n, line, b[n]))
            continue


def test_str():
    non_blank_line_by_line_compare(str(doc), 'numpy.multivariate_normal(mean, cov, shape=None, spam=None)\n\nDraw values from a multivariate normal distribution with specified\nmean and covariance.\n\nThe multivariate normal or Gaussian distribution is a generalisation\nof the one-dimensional normal distribution to higher dimensions.\n\nParameters\n----------\nmean : (N,) ndarray\n    Mean of the N-dimensional distribution.\n\n    .. math::\n\n       (1+2+3)/3\n\ncov : (N, N) ndarray\n    Covariance matrix of the distribution.\nshape : tuple of ints\n    Given a shape of, for example, (m,n,k), m*n*k samples are\n    generated, and packed in an m-by-n-by-k arrangement.  Because\n    each sample is N-dimensional, the output shape is (m,n,k,N).\n\nReturns\n-------\nout : ndarray\n    The drawn samples, arranged according to `shape`.  If the\n    shape given is (m,n,...), then the shape of `out` is is\n    (m,n,...,N).\n\n    In other words, each entry ``out[i,j,...,:]`` is an N-dimensional\n    value drawn from the distribution.\nlist of str\n    This is not a real return value.  It exists to test\n    anonymous return values.\n\nOther Parameters\n----------------\nspam : parrot\n    A parrot off its mortal coil.\n\nRaises\n------\nRuntimeError\n    Some error\n\nWarns\n-----\nRuntimeWarning\n    Some warning\n\nWarnings\n--------\nCertain warnings apply.\n\nSee Also\n--------\n`some`_, `other`_, `funcs`_\n\n`otherfunc`_\n    relationship\n\nNotes\n-----\nInstead of specifying the full covariance matrix, popular\napproximations include:\n\n  - Spherical covariance (`cov` is a multiple of the identity matrix)\n  - Diagonal covariance (`cov` has non-negative elements only on the diagonal)\n\nThis geometrical property can be seen in two dimensions by plotting\ngenerated data-points:\n\n>>> mean = [0,0]\n>>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis\n\n>>> x,y = multivariate_normal(mean,cov,5000).T\n>>> plt.plot(x,y,\'x\'); plt.axis(\'equal\'); plt.show()\n\nNote that the covariance matrix must be symmetric and non-negative\ndefinite.\n\nReferences\n----------\n.. [1] A. Papoulis, "Probability, Random Variables, and Stochastic\n       Processes," 3rd ed., McGraw-Hill Companies, 1991\n.. [2] R.O. Duda, P.E. Hart, and D.G. Stork, "Pattern Classification,"\n       2nd ed., Wiley, 2001.\n\nExamples\n--------\n>>> mean = (1,2)\n>>> cov = [[1,0],[1,0]]\n>>> x = multivariate_normal(mean,cov,(3,3))\n>>> print x.shape\n(3, 3, 2)\n\nThe following is probably true, given that 0.6 is roughly twice the\nstandard deviation:\n\n>>> print list( (x[0,0,:] - mean) < 0.6 )\n[True, True]\n\n.. index:: random\n   :refguide: random;distributions, random;gauss')


def test_sphinx_str():
    sphinx_doc = SphinxDocString(doc_txt)
    non_blank_line_by_line_compare(str(sphinx_doc), '\n.. index:: random\n   single: random;distributions, random;gauss\n\nDraw values from a multivariate normal distribution with specified\nmean and covariance.\n\nThe multivariate normal or Gaussian distribution is a generalisation\nof the one-dimensional normal distribution to higher dimensions.\n\n:Parameters:\n\n    **mean** : (N,) ndarray\n\n        Mean of the N-dimensional distribution.\n\n        .. math::\n\n           (1+2+3)/3\n\n    **cov** : (N, N) ndarray\n\n        Covariance matrix of the distribution.\n\n    **shape** : tuple of ints\n\n        Given a shape of, for example, (m,n,k), m*n*k samples are\n        generated, and packed in an m-by-n-by-k arrangement.  Because\n        each sample is N-dimensional, the output shape is (m,n,k,N).\n\n:Returns:\n\n    **out** : ndarray\n\n        The drawn samples, arranged according to `shape`.  If the\n        shape given is (m,n,...), then the shape of `out` is is\n        (m,n,...,N).\n\n        In other words, each entry ``out[i,j,...,:]`` is an N-dimensional\n        value drawn from the distribution.\n\n    list of str\n\n        This is not a real return value.  It exists to test\n        anonymous return values.\n\n:Other Parameters:\n\n    **spam** : parrot\n\n        A parrot off its mortal coil.\n\n:Raises:\n\n    **RuntimeError**\n\n        Some error\n\n:Warns:\n\n    **RuntimeWarning**\n\n        Some warning\n\n.. warning::\n\n    Certain warnings apply.\n\n.. seealso::\n\n    :obj:`some`, :obj:`other`, :obj:`funcs`\n\n    :obj:`otherfunc`\n        relationship\n\n.. rubric:: Notes\n\nInstead of specifying the full covariance matrix, popular\napproximations include:\n\n  - Spherical covariance (`cov` is a multiple of the identity matrix)\n  - Diagonal covariance (`cov` has non-negative elements only on the diagonal)\n\nThis geometrical property can be seen in two dimensions by plotting\ngenerated data-points:\n\n>>> mean = [0,0]\n>>> cov = [[1,0],[0,100]] # diagonal covariance, points lie on x or y-axis\n\n>>> x,y = multivariate_normal(mean,cov,5000).T\n>>> plt.plot(x,y,\'x\'); plt.axis(\'equal\'); plt.show()\n\nNote that the covariance matrix must be symmetric and non-negative\ndefinite.\n\n.. rubric:: References\n\n.. [1] A. Papoulis, "Probability, Random Variables, and Stochastic\n       Processes," 3rd ed., McGraw-Hill Companies, 1991\n.. [2] R.O. Duda, P.E. Hart, and D.G. Stork, "Pattern Classification,"\n       2nd ed., Wiley, 2001.\n\n.. only:: latex\n\n   [1]_, [2]_\n\n.. rubric:: Examples\n\n>>> mean = (1,2)\n>>> cov = [[1,0],[1,0]]\n>>> x = multivariate_normal(mean,cov,(3,3))\n>>> print x.shape\n(3, 3, 2)\n\nThe following is probably true, given that 0.6 is roughly twice the\nstandard deviation:\n\n>>> print list( (x[0,0,:] - mean) < 0.6 )\n[True, True]\n')


doc2 = NumpyDocString('\n    Returns array of indices of the maximum values of along the given axis.\n\n    Parameters\n    ----------\n    a : {array_like}\n        Array to look in.\n    axis : {None, integer}\n        If None, the index is into the flattened array, otherwise along\n        the specified axis')

def test_parameters_without_extended_description():
    assert_equal(len(doc2['Parameters']), 2)


doc3 = NumpyDocString('\n    my_signature(*params, **kwds)\n\n    Return this and that.\n    ')

def test_escape_stars():
    signature = str(doc3).split('\n')[0]
    assert_equal(signature, 'my_signature(\\*params, \\*\\*kwds)')


doc4 = NumpyDocString('a.conj()\n\n    Return an array with all complex-valued elements conjugated.')

def test_empty_extended_summary():
    assert_equal(doc4['Extended Summary'], [])


doc5 = NumpyDocString('\n    a.something()\n\n    Raises\n    ------\n    LinAlgException\n        If array is singular.\n\n    Warns\n    -----\n    SomeWarning\n        If needed\n    ')

def test_raises():
    assert_equal(len(doc5['Raises']), 1)
    name, _, desc = doc5['Raises'][0]
    assert_equal(name, 'LinAlgException')
    assert_equal(desc, ['If array is singular.'])


def test_warns():
    assert_equal(len(doc5['Warns']), 1)
    name, _, desc = doc5['Warns'][0]
    assert_equal(name, 'SomeWarning')
    assert_equal(desc, ['If needed'])


def test_see_also():
    doc6 = NumpyDocString('\n    z(x,theta)\n\n    See Also\n    --------\n    func_a, func_b, func_c\n    func_d : some equivalent func\n    foo.func_e : some other func over\n             multiple lines\n    func_f, func_g, :meth:`func_h`, func_j,\n    func_k\n    :obj:`baz.obj_q`\n    :class:`class_j`: fubar\n        foobar\n    ')
    @py_assert1 = doc6['See Also']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 12
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py4': @pytest_ar._saferepr(@py_assert3),  'py7': @pytest_ar._saferepr(@py_assert6),  'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    for func, desc, role in doc6['See Also']:
        if func in ('func_a', 'func_b', 'func_c', 'func_f', 'func_g', 'func_h', 'func_j',
                    'func_k', 'baz.obj_q'):
            @py_assert1 = not desc
            if not @py_assert1:
                @py_format2 = 'assert not %(py0)s' % {'py0': @pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format2))
            @py_assert1 = None
        else:
            if not desc:
                @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format1))
            if func == 'func_h':
                @py_assert2 = 'meth'
                @py_assert1 = role == @py_assert2
                if not @py_assert1:
                    @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (role, @py_assert2)) % {'py0': @pytest_ar._saferepr(role) if 'role' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(role) else 'role',  'py3': @pytest_ar._saferepr(@py_assert2)}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert1 = @py_assert2 = None
            else:
                if func == 'baz.obj_q':
                    @py_assert2 = 'obj'
                    @py_assert1 = role == @py_assert2
                    if not @py_assert1:
                        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (role, @py_assert2)) % {'py0': @pytest_ar._saferepr(role) if 'role' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(role) else 'role',  'py3': @pytest_ar._saferepr(@py_assert2)}
                        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                    @py_assert1 = @py_assert2 = None
                else:
                    if func == 'class_j':
                        @py_assert2 = 'class'
                        @py_assert1 = role == @py_assert2
                        if not @py_assert1:
                            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (role, @py_assert2)) % {'py0': @pytest_ar._saferepr(role) if 'role' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(role) else 'role',  'py3': @pytest_ar._saferepr(@py_assert2)}
                            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                        @py_assert1 = @py_assert2 = None
                    else:
                        @py_assert2 = None
                        @py_assert1 = role is @py_assert2
                        if not @py_assert1:
                            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (role, @py_assert2)) % {'py0': @pytest_ar._saferepr(role) if 'role' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(role) else 'role',  'py3': @pytest_ar._saferepr(@py_assert2)}
                            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                        @py_assert1 = @py_assert2 = None
        if func == 'func_d':
            @py_assert2 = [
             'some equivalent func']
            @py_assert1 = desc == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (desc, @py_assert2)) % {'py0': @pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc',  'py3': @pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None
        elif func == 'foo.func_e':
            @py_assert2 = [
             'some other func over', 'multiple lines']
            @py_assert1 = desc == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (desc, @py_assert2)) % {'py0': @pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc',  'py3': @pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None
        elif func == 'class_j':
            @py_assert2 = [
             'fubar', 'foobar']
            @py_assert1 = desc == @py_assert2
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (desc, @py_assert2)) % {'py0': @pytest_ar._saferepr(desc) if 'desc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(desc) else 'desc',  'py3': @pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None
            continue

    return


def test_see_also_print():

    class Dummy(object):
        __doc__ = '\n        See Also\n        --------\n        func_a, func_b\n        func_c : some relationship\n                 goes here\n        func_d\n        '

    obj = Dummy()
    s = str(FunctionDoc(obj, role='func'))
    @py_assert0 = ':func:`func_a`, :func:`func_b`'
    @py_assert2 = @py_assert0 in s
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, s)) % {'py3': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = '    some relationship'
    @py_assert2 = @py_assert0 in s
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, s)) % {'py3': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = ':func:`func_d`'
    @py_assert2 = @py_assert0 in s
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, s)) % {'py3': @pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


doc7 = NumpyDocString('\n\n        Doc starts on second line.\n\n        ')

def test_empty_first_line():
    @py_assert0 = doc7['Summary'][0]
    @py_assert2 = @py_assert0.startswith
    @py_assert4 = 'Doc starts'
    @py_assert6 = @py_assert2(@py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_no_summary():
    str(SphinxDocString('\n    Parameters\n    ----------'))


def test_unicode():
    doc = SphinxDocString('\n    öäöäöäöäöåååå\n\n    öäöäöäööäååå\n\n    Parameters\n    ----------\n    ååå : äää\n        ööö\n\n    Returns\n    -------\n    ååå : ööö\n        äää\n\n    ')
    @py_assert1 = doc['Summary'][0]
    @py_assert4 = isinstance(@py_assert1, str)
    if not @py_assert4:
        @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    @py_assert0 = doc['Summary'][0]
    @py_assert3 = 'öäöäöäöäöåååå'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_plot_examples():
    cfg = dict(use_plots=True)
    doc = SphinxDocString('\n    Examples\n    --------\n    >>> import matplotlib.pyplot as plt\n    >>> plt.plot([1,2,3],[4,5,6])\n    >>> plt.show()\n    ', config=cfg)
    @py_assert0 = 'plot::'
    @py_assert5 = str(doc)
    @py_assert2 = @py_assert0 in @py_assert5
    if not @py_assert2:
        @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = (@pytest_ar._format_assertmsg(str(doc)) + '\n>assert %(py8)s') % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert5 = None
    doc = SphinxDocString('\n    Examples\n    --------\n    .. plot::\n\n       import matplotlib.pyplot as plt\n       plt.plot([1,2,3],[4,5,6])\n       plt.show()\n    ', config=cfg)
    @py_assert2 = str(doc)
    @py_assert4 = @py_assert2.count
    @py_assert6 = 'plot::'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert11 = 1
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}.count\n}(%(py7)s)\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py9': @pytest_ar._saferepr(@py_assert8),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py12': @pytest_ar._saferepr(@py_assert11)}
        @py_format15 = (@pytest_ar._format_assertmsg(str(doc)) + '\n>assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    return


def test_class_members():

    class Dummy(object):
        __doc__ = '\n        Dummy class.\n\n        '

        def spam(self, a, b):
            """Spam

Spam spam."""
            pass

        def ham(self, c, d):
            """Cheese

No cheese."""
            pass

        @property
        def spammity(self):
            """Spammity index"""
            return 0.95

        class Ignorable(object):
            __doc__ = 'local class, to be ignored'

    for cls in (ClassDoc, SphinxClassDoc):
        doc = cls(Dummy, config=dict(show_class_members=False))
        @py_assert0 = 'Methods'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'spam'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'ham'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'spammity'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'Spammity index'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 not in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        doc = cls(Dummy, config=dict(show_class_members=True))
        @py_assert0 = 'Methods'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'spam'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'ham'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        @py_assert0 = 'spammity'
        @py_assert5 = str(doc)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = (@pytest_ar._format_assertmsg((cls, str(doc))) + '\n>assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
        if cls is SphinxClassDoc:
            @py_assert0 = '.. autosummary::'
            @py_assert5 = str(doc)
            @py_assert2 = @py_assert0 in @py_assert5
            if not @py_assert2:
                @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
                @py_format9 = (@pytest_ar._format_assertmsg(str(doc)) + '\n>assert %(py8)s') % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert0 = @py_assert2 = @py_assert5 = None
        else:
            @py_assert0 = 'Spammity index'
            @py_assert5 = str(doc)
            @py_assert2 = @py_assert0 in @py_assert5
            if not @py_assert2:
                @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0),  'py4': @pytest_ar._saferepr(doc) if 'doc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(doc) else 'doc',  'py6': @pytest_ar._saferepr(@py_assert5)}
                @py_format9 = (@pytest_ar._format_assertmsg(str(doc)) + '\n>assert %(py8)s') % {'py8': @py_format7}
                raise AssertionError(@pytest_ar._format_explanation(@py_format9))
            @py_assert0 = @py_assert2 = @py_assert5 = None

    return


def test_duplicate_signature():
    doc = NumpyDocString('\n    z(x1, x2)\n\n    z(a, theta)\n    ')
    @py_assert0 = doc['Signature']
    @py_assert2 = @py_assert0.strip
    @py_assert4 = @py_assert2()
    @py_assert7 = 'z(a, theta)'
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.strip\n}()\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0),  'py8': @pytest_ar._saferepr(@py_assert7),  'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


class_doc_txt = '\n    Foo\n\n    Parameters\n    ----------\n    f : callable ``f(t, y, *f_args)``\n        Aaa.\n    jac : callable ``jac(t, y, *jac_args)``\n        Bbb.\n\n    Attributes\n    ----------\n    t : float\n        Current time.\n    y : ndarray\n        Current variable values.\n\n    Methods\n    -------\n    a\n    b\n    c\n\n    Examples\n    --------\n    For usage examples, see `ode`.\n'

def test_class_members_doc():
    doc = ClassDoc(None, class_doc_txt)
    non_blank_line_by_line_compare(str(doc), '\n    Foo\n\n    Parameters\n    ----------\n    f : callable ``f(t, y, *f_args)``\n        Aaa.\n    jac : callable ``jac(t, y, *jac_args)``\n        Bbb.\n\n    Examples\n    --------\n    For usage examples, see `ode`.\n\n    Attributes\n    ----------\n    t : float\n        Current time.\n    y : ndarray\n        Current variable values.\n\n    Methods\n    -------\n    a\n\n    b\n\n    c\n\n    .. index::\n\n    ')


def test_class_members_doc_sphinx():
    doc = SphinxClassDoc(None, class_doc_txt)
    non_blank_line_by_line_compare(str(doc), '\n    Foo\n\n    :Parameters:\n\n        **f** : callable ``f(t, y, *f_args)``\n\n            Aaa.\n\n        **jac** : callable ``jac(t, y, *jac_args)``\n\n            Bbb.\n\n    .. rubric:: Examples\n\n    For usage examples, see `ode`.\n\n    .. rubric:: Attributes\n\n    ===  ==========\n      t  (float) Current time.\n      y  (ndarray) Current variable values.\n    ===  ==========\n\n    .. rubric:: Methods\n\n    ===  ==========\n      a\n      b\n      c\n    ===  ==========\n\n    ')


if __name__ == '__main__':
    import nose
    nose.run()
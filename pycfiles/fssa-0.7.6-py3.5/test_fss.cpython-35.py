# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fssa/test/test_fss.py
# Compiled at: 2015-12-12 16:19:49
# Size of source mod 2**32: 31790 bytes
import copy, inspect, unittest, warnings, fssa, numpy as np, numpy.ma as ma

class TestScaleData(unittest.TestCase):
    __doc__ = 'Test data scaling function.'

    def setUp(self):
        rho = np.linspace(-1, 1, num=11)
        l = np.logspace(1, 3, num=3)
        l_mesh, rho_mesh = np.meshgrid(l, rho, indexing='ij')
        a = 1.0 / (1.0 + np.exp(-np.log10(l_mesh) * rho_mesh))
        da = np.ones_like(a) * 0.01
        self.default_params = {'rho': rho, 
         'l': l, 
         'a': a, 
         'da': da, 
         'rho_c': 0.0, 
         'nu': 1.0, 
         'zeta': 0.0}

    def tearDown(self):
        pass

    def test_call(self):
        """
        Test function call
        """
        self.assertTrue(hasattr(fssa, 'scaledata'), msg='No such function: fssa.scaledata')

    def test_signature(self):
        """
        Test scaledata function signature
        """
        try:
            args = inspect.signature(fssa.scaledata).parameters
        except:
            args = inspect.getargspec(fssa.scaledata).args

        self.assertIn('rho', args)
        self.assertIn('l', args)
        self.assertIn('a', args)
        self.assertIn('da', args)
        self.assertIn('rho_c', args)
        self.assertIn('nu', args)
        self.assertIn('zeta', args)

    def test_rho_1d_array_like(self):
        """
        Test that function raises ValueError when rho is not 1-D array_like
        """
        self._test_for_1d_array_like(fssa.scaledata, 'rho', self.default_params)

    def test_l_1d_array_like(self):
        """
        Test that function raises ValueError when l is not 1-D array_like
        """
        self._test_for_1d_array_like(fssa.scaledata, 'l', self.default_params)

    def test_a_2d_array_like(self):
        """
        Test that function raises ValueError when a is not 2-D array_like
        """
        self._test_for_2d_array_like(fssa.scaledata, 'a', self.default_params)

    def test_a_has_l_rho_shape(self):
        """
        Test that function raises ValueError when a does not have the correct
        shape
        """
        args = copy.deepcopy(self.default_params)
        args['a'] = np.ones(shape=(3, args['rho'].size - 1))
        self.assertRaises(ValueError, fssa.scaledata, **args)

    def test_da_2d_array_like(self):
        """
        Test that function raises ValueError when da is not 2-D array_like
        """
        self._test_for_2d_array_like(fssa.scaledata, 'da', self.default_params)

    def test_da_has_l_rho_shape(self):
        """
        Test that function raises ValueError when da does not have the correct
        shape
        """
        args = copy.deepcopy(self.default_params)
        args['da'] = np.ones(shape=(3, args['rho'].size - 1))
        self.assertRaises(ValueError, fssa.scaledata, **args)

    def test_no_error_if_not_da_all_positive(self):
        """
        Test that function does not raise ValueError if any da is not positive
        """
        args = copy.deepcopy(self.default_params)
        args['da'][(1, 1)] = 0.0
        fssa.scaledata(**args)
        args = copy.deepcopy(self.default_params)
        args['da'][(1, 0)] = -1.0
        fssa.scaledata(**args)

    def test_rho_c_float(self):
        """
        Test that function raises TypeError when rho_c is not a float
        """
        self._test_for_float(fssa.scaledata, 'rho_c', self.default_params)

    def test_rho_c_in_range(self):
        """
        Test that function issues warning when rho_c is out of range
        """
        args = copy.deepcopy(self.default_params)
        args['rho_c'] = args['rho'].max() + 1.0
        with warnings.catch_warnings(record=True) as (w):
            warnings.simplefilter('always')
            fssa.scaledata(**args)
            assert len(w) == 1
            assert issubclass(w[(-1)].category, RuntimeWarning)
            assert 'out of range' in str(w[(-1)].message)

    def test_nu_float(self):
        """
        Test that function raises TypeError when nu is not a float
        """
        self._test_for_float(fssa.scaledata, 'nu', self.default_params)

    def test_zeta_float(self):
        """
        Test that function raises TypeError when zeta is not a float
        """
        self._test_for_float(fssa.scaledata, 'zeta', self.default_params)

    def test_output_len(self):
        """
        Test that function returns at least three items
        """
        result = fssa.scaledata(**self.default_params)
        self.assertGreaterEqual(len(result), 3)

    def test_output_shape(self):
        """
        Test that function returns three ndarrays of correct shape
        """
        correct_shape = (
         self.default_params['l'].size,
         self.default_params['rho'].size)
        result = fssa.scaledata(**self.default_params)
        for i in range(3):
            try:
                with self.subTest(i=i):
                    self.assertTupleEqual(np.asarray(result[i]).shape, correct_shape)
            except AttributeError:
                self.assertTupleEqual(np.asarray(result[i]).shape, correct_shape)

    def test_output_namedtuple(self):
        """
        Test that function returns namedtuple with correct field names
        """
        result = fssa.scaledata(**self.default_params)
        fields = ['x', 'y', 'dy']
        for i in range(len(fields)):
            try:
                with self.subTest(i=i):
                    self.assertTrue(hasattr(result, fields[i]))
                    self.assertIs(getattr(result, fields[i]), result[i])
            except AttributeError:
                self.assertTrue(hasattr(result, fields[i]))
                self.assertIs(getattr(result, fields[i]), result[i])

    def test_zero_zeta_keeps_y_values(self):
        r"""
        Check that $\zeta = 0$ does not affect the y values
        """
        args = copy.deepcopy(self.default_params)
        args['zeta'] = 0.0
        result = fssa.scaledata(**self.default_params)
        self.assertTrue(np.all(args['a'] == result.y))

    def test_values(self):
        """
        Check some arbitrary value
        """
        l = self.default_params['l'][2]
        rho = self.default_params['rho'][3]
        rho_c = self.default_params['rho_c']
        nu = self.default_params['nu']
        zeta = self.default_params['zeta']
        a = self.default_params['a'][(2, 3)]
        da = self.default_params['da'][(2, 3)]
        result = fssa.scaledata(**self.default_params)
        self.assertAlmostEqual(result.x[(2, 3)], l ** (1.0 / nu) * (rho - rho_c))
        self.assertAlmostEqual(result.y[(2, 3)], l ** (-zeta / nu) * a)
        self.assertAlmostEqual(result.dy[(2, 3)], l ** (-zeta / nu) * da)

    def _test_for_float(self, callable, param, default_args):
        """
        Test that callable raises TypeError when param is not float
        """
        args = copy.deepcopy(default_args)
        args[param] = np.array([1.0, 2.0])
        self.assertRaises(TypeError, callable, **args)

    def _test_for_1d_array_like(self, callable, param, default_args):
        """
        Test that callable raises ValueError when param is not 1-D array_like
        """
        args = copy.deepcopy(default_args)
        args[param] = 0.0
        self.assertRaises(ValueError, callable, **args)
        args = copy.deepcopy(default_args)
        args[param] = np.zeros(shape=(2, 3))
        self.assertRaises(ValueError, callable, **args)

    def _test_for_2d_array_like(self, callable, param, default_args):
        """
        Test that callable raises ValueError when param is not 2-D array_like
        """
        args = copy.deepcopy(default_args)
        args[param] = 0.0
        self.assertRaises(ValueError, callable, **args)
        args = copy.deepcopy(default_args)
        args[param] = np.zeros(2)
        self.assertRaises(ValueError, callable, **args)
        args = copy.deepcopy(default_args)
        args[param] = np.zeros(shape=(2, 3, 4))
        self.assertRaises(ValueError, callable, **args)


class TestJPrimes(unittest.TestCase):
    __doc__ = '\n    Test the j_primes helper function\n    '

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_existence(self):
        """
        Test for function existence
        """
        self.assertTrue(hasattr(fssa.fssa, '_jprimes'), msg='No such function: fssa.fssa.._jprimes')

    def test_signature(self):
        """
        Test function signature
        """
        try:
            args = inspect.signature(fssa.fssa._jprimes).parameters
        except:
            args = inspect.getargspec(fssa.fssa._jprimes).args

        fields = ['x', 'i', 'x_bounds']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_return_type(self):
        """
        Test that the function returns an array of the same shape as x
        """
        x = np.sort(np.random.rand(4, 3))
        ret = fssa.fssa._jprimes(x, 2)
        self.assertTupleEqual(ret.shape, x.shape)

    def test_never_select_from_i(self):
        """
        Test that the mask never selects from the i row
        """
        x = np.sort(np.random.rand(4, 3))
        ret = fssa.fssa._jprimes(x, 2)
        self.assertTrue(np.isnan(ret[2, :]).all())

    def test_jprime_nan_if_xij_doesnt_fit(self):
        """
        Test that there is no j' if and only if the xij does not fit into
        the i' row of x values
        """
        x = np.sort(np.random.rand(4, 3))
        x[3, :] = x[2, :]
        ret = fssa.fssa._jprimes(x, 2)
        for iprime in range(x.shape[0]):
            if iprime == 2:
                pass
            else:
                for j in range(x.shape[1]):
                    xij = x[(2, j)]
                    jprime = ret[(iprime, j)]
                    self.assertTrue(np.isnan(jprime) == (xij < x[iprime, :].min() or xij >= x[iprime, :].max()))

    def test_xiprimejprime_lessequal_xij(self):
        r"""
        Test that :math:`x_{i'j'} \leq x_{ij}`
        """
        x = np.sort(np.random.rand(4, 3))
        x[3, :] = x[2, :]
        ret = fssa.fssa._jprimes(x, 2)
        for iprime in range(x.shape[0]):
            if iprime == 2:
                pass
            else:
                for j in range(x.shape[1]):
                    xij = x[(2, j)]
                    jprime = ret[(iprime, j)]
                    if np.isnan(jprime):
                        pass
                    else:
                        jprime = int(jprime)
                        self.assertLessEqual(x[(iprime, jprime)], xij)

    def test_xiprimejprime1_greater_xij(self):
        """
        Test that :math:`x_{i'(j'+1)} > x_{ij}`
        """
        x = np.sort(np.random.rand(4, 3))
        x[3, :] = x[2, :]
        ret = fssa.fssa._jprimes(x, 2)
        for iprime in range(x.shape[0]):
            if iprime == 2:
                pass
            else:
                for j in range(x.shape[1]):
                    xij = x[(2, j)]
                    jprime = ret[(iprime, j)]
                    if np.isnan(jprime):
                        pass
                    else:
                        jprime = int(jprime)
                        self.assertGreater(x[(iprime, jprime + 1)], xij)

    def test_jprimes(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        jprimes = list()
        jprimes.append(np.array([
         [
          np.nan, np.nan, np.nan],
         [
          np.nan, 0.0, 1.0],
         [
          0.0, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          0.0, 1.0, np.nan],
         [
          np.nan, np.nan, np.nan],
         [
          1.0, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          np.nan, 0.0, 0.0],
         [
          np.nan, np.nan, 0.0],
         [
          np.nan, np.nan, np.nan]]))
        for i in range(3):
            ret = fssa.fssa._jprimes(x=x, i=i)
            try:
                with self.subTest(i):
                    np.testing.assert_allclose(ret, jprimes[i])
            except AttributeError:
                np.testing.assert_allclose(ret, jprimes[i])

    def test_mask(self):
        x = ma.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        jprimes = list()
        jprimes.append(np.array([
         [
          np.nan, np.nan, np.nan],
         [
          np.nan, 0.0, 1.0],
         [
          0.0, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          0.0, 1.0, np.nan],
         [
          np.nan, np.nan, np.nan],
         [
          1.0, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          np.nan, 0.0, 0.0],
         [
          np.nan, np.nan, 0.0],
         [
          np.nan, np.nan, np.nan]]))
        for i in range(3):
            ret = fssa.fssa._jprimes(x=x, i=i)
            try:
                with self.subTest(i):
                    np.testing.assert_allclose(ret, jprimes[i])
            except AttributeError:
                np.testing.assert_allclose(ret, jprimes[i])

    def test_xbounds(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        jprimes = list()
        jprimes.append(np.array([
         [
          np.nan, np.nan, np.nan],
         [
          np.nan, 0.0, np.nan],
         [
          np.nan, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          np.nan, 1.0, np.nan],
         [
          np.nan, np.nan, np.nan],
         [
          np.nan, np.nan, np.nan]]))
        jprimes.append(np.array([
         [
          np.nan, np.nan, np.nan],
         [
          np.nan, np.nan, 0.0],
         [
          np.nan, np.nan, np.nan]]))
        for i in range(3):
            ret = fssa.fssa._jprimes(x=x, i=i, x_bounds=(0.3, 2.3))
            try:
                with self.subTest(i):
                    np.testing.assert_allclose(ret, jprimes[i])
            except AttributeError:
                np.testing.assert_allclose(ret, jprimes[i])


class TestSelectMask(unittest.TestCase):
    __doc__ = '\n    Test the select mask helper function\n    '

    def setUp(self):
        self.i = 1
        self.j = 2
        self.j_primes = np.asfarray(np.random.randint(-1, 2, size=(4, 3)))
        self.j_primes[self.j_primes == -1] = np.nan
        self.default_args = {'j': self.j, 
         'j_primes': self.j_primes}

    def tearDown(self):
        pass

    def test_existence(self):
        """
        Test for function existence
        """
        self.assertTrue(hasattr(fssa.fssa, '_select_mask'), msg='No such function: fssa.fssa._select_mask')

    def test_signature(self):
        """
        Test function signature
        """
        try:
            args = inspect.signature(fssa.fssa._select_mask).parameters
        except:
            args = inspect.getargspec(fssa.fssa._select_mask).args

        fields = ['j', 'j_primes']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_return_type(self):
        """
        Test that the function returns an array of the same shape as
        j_primes
        """
        ret = fssa.fssa._select_mask(**self.default_args)
        self.assertTupleEqual(ret.shape, self.default_args['j_primes'].shape)

    def test_jprime_selection(self):
        """
        Test that the function selects element (i', j') if and only if
        j_primes[i', j] == j' or j_primes[i', j] == j' - 1
        """
        ret = fssa.fssa._select_mask(**self.default_args)
        for iprime in range(self.j_primes.shape[0]):
            for jprime in range(self.j_primes.shape[1]):
                self.assertTrue(ret[(iprime, jprime)] == (self.j_primes[(iprime, self.j)] == jprime or self.j_primes[(iprime, self.j)] == jprime - 1))


class TestWLSPredict(unittest.TestCase):
    __doc__ = '\n    Test the Weighted Least Squares Prediction Function\n    '

    def setUp(self):
        x = np.array([-2, 0, -10, 10], dtype=float)
        y = np.array([-4, 0, -100, 100], dtype=float)
        dy = np.array([0.2, 0.1, 1, 1])
        w = dy ** (-2)
        wx = w * x
        wy = w * y
        wxx = w * x * x
        wxy = w * x * y
        select = np.ones_like(x, dtype=bool)
        x = 1.0
        self.default_args = {'x': x, 
         'w': w, 
         'wx': wx, 
         'wy': wy, 
         'wxx': wxx, 
         'wxy': wxy, 
         'select': select}

    def tearDown(self):
        pass

    def test_existence(self):
        """
        Test for function existence
        """
        self.assertTrue(hasattr(fssa.fssa, '_wls_linearfit_predict'), msg='No such function: fssa.fssa._wls_linearfit_predict')

    def test_signature(self):
        """
        Test wls function signature
        """
        try:
            args = inspect.signature(fssa.fssa._wls_linearfit_predict).parameters
        except:
            args = inspect.getargspec(fssa.fssa._wls_linearfit_predict).args

        fields = ['x', 'w', 'wx', 'wy', 'wxx', 'wxy', 'select']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_return_type(self):
        """
        Tests for correct return
        """
        ret = fssa.fssa._wls_linearfit_predict(**self.default_args)
        y = float(ret[0])
        dy = float(ret[1])
        y, dy = fssa.fssa._wls_linearfit_predict(**self.default_args)
        (float(y), float(dy))

    def test_function_value(self):
        """
        Test for a concrete function value
        """
        y, dy2 = fssa.fssa._wls_linearfit_predict(**self.default_args)
        self.assertAlmostEqual(y, float(9.95505617977528))
        self.assertAlmostEqual(dy2, 0.014803370786516853)


class TestQuality(unittest.TestCase):
    __doc__ = '\n    Test the quality function\n    '

    def setUp(self):
        rho = np.linspace(-1, 1, num=11)
        l = np.logspace(1, 3, num=3)
        l_mesh, rho_mesh = np.meshgrid(l, rho, indexing='ij')
        a = 1.0 / (1.0 + np.exp(-np.log10(l_mesh) * rho_mesh))
        da = np.ones_like(a) * 0.01
        self.scaled_data = fssa.scaledata(l, rho, a, da, 0, 1, 0)

    def tearDown(self):
        pass

    def test_call(self):
        """
        Test function call
        """
        self.assertTrue(hasattr(fssa, 'quality'), msg='No such function: fssa.quality')

    def test_signature(self):
        """
        Test quality function signature
        """
        try:
            args = inspect.signature(fssa.quality).parameters
        except:
            args = inspect.getargspec(fssa.quality).args

        fields = ['x', 'y', 'dy', 'x_bounds']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_args_2d_array_like(self):
        """
        Test that function raises ValueError when one of the arguments is not
        2-D array_like
        """
        args = [
         'x', 'y', 'dy']
        for i in range(len(args)):
            try:
                with self.subTest(i=i):
                    self._test_for_2d_array_like(fssa.quality, i, self.scaled_data)
            except:
                self._test_for_2d_array_like(fssa.quality, i, self.scaled_data)

    def test_args_of_same_shape(self):
        """
        Test that function raises ValueError if the shapes of the arguments
        differ
        """
        args = list(self.scaled_data)
        for i in range(len(args)):
            args = list(self.scaled_data)
            args[i] = np.zeros(shape=(134, 23))
            try:
                with self.subTest(i=i):
                    self.assertRaises(ValueError, fssa.quality, *args)
            except AttributeError:
                self.assertRaises(ValueError, fssa.quality, *args)

    def test_x_sorted(self):
        """
        Test that function raises ValueError if x is not sorted in the second
        dimension (parameter values)
        """
        args = list(self.scaled_data)
        args[0][(1, 3)] = args[0][(1, 1)]
        self.assertRaises(ValueError, fssa.quality, *args)

    def test_dy_all_positive(self):
        """
        Test that function raises ValueError if any dy is not positive
        """
        orig_args = list(self.scaled_data)
        args = copy.deepcopy(orig_args)
        args[2][(1, 1)] = 0.0
        self.assertRaises(ValueError, fssa.quality, *args)
        args = copy.deepcopy(orig_args)
        assert args[2][(1, 1)] != 0
        args[2][(1, 0)] = -1.0
        self.assertRaises(ValueError, fssa.quality, *args)

    def test_zero_quality(self):
        """
        Test that function returns close to zero value if fed with the same x
        and y values
        """

        def master_curve(x):
            return 1.0 / (1.0 + np.exp(5 * (1.0 - x)))

        x = np.linspace(0, 2)
        x_array = np.row_stack([x for i in range(10)])
        y_array = master_curve(x_array)
        dy = 0.05
        dy_array = dy * np.ones_like(y_array)
        ret = fssa.quality(x_array, y_array, dy_array)
        self.assertGreaterEqual(ret, 0.0)
        self.assertLess(ret, 0.1)

    def test_standard_quality(self):
        """
        Test that function returns close to one value if fed with the same x
        and y values with some standard error applied
        """

        def master_curve(x):
            return 1.0 / (1.0 + np.exp(5 * (1.0 - x)))

        x = np.linspace(0, 2)
        x_array = np.row_stack([x for i in range(10)])
        y_array = master_curve(x_array)
        dy = 0.05
        dy_array = dy * np.ones_like(y_array)
        y_array += dy * np.random.randn(*y_array.shape)
        ret = fssa.quality(x_array, y_array, dy_array)
        self.assertGreater(ret, np.power(10, -0.5))
        self.assertLess(ret, np.power(10, 0.5))

    def _test_for_2d_array_like(self, callable, param, default_args):
        """
        Test that callable raises ValueError when param is not 2-D array_like
        """
        args = list(default_args)
        args[param] = 0.0
        self.assertRaises(ValueError, callable, *args)
        args = list(default_args)
        args[param] = np.zeros(2)
        self.assertRaises(ValueError, callable, *args)
        args = list(default_args)
        args[param] = np.zeros(shape=(2, 3, 4))
        self.assertRaises(ValueError, callable, *args)

    def test_linear_quality(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        y = x.copy()
        dy = 0.05 * np.ones_like(y)
        ret = fssa.quality(x, y, dy)
        self.assertEqual(ret, 0.0)

    def test_linear_quality_fail(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        y = x.copy()
        y[(1, 1)] = 1.0
        dy = 0.05 * np.ones_like(y)
        ret = fssa.quality(x, y, dy)
        self.assertGreater(ret, 0.0)

    def test_linear_quality_x_bounds(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        y = x.copy()
        dy = 0.05 * np.ones_like(y)
        ret = fssa.quality(x, y, dy, x_bounds=(0.3, 2.3))
        self.assertEqual(ret, 0.0)

    def test_linear_quality_x_bounds_omits(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        y = x.copy()
        y[(2, 1)] = 0.0
        dy = 0.05 * np.ones_like(y)
        ret = fssa.quality(x, y, dy, x_bounds=(0.3, 2.3))
        self.assertEqual(ret, 0.0)

    def test_linear_quality_fails_x_bounds(self):
        x = np.array([
         [
          0.0, 1.0, 2.0],
         [
          0.5, 1.5, 2.5],
         [
          -0.25, 0.25, 0.75]])
        y = x.copy()
        y[(1, 1)] = 1.0
        dy = 0.05 * np.ones_like(y)
        ret = fssa.quality(x, y, dy, x_bounds=(0.3, 2.3))
        self.assertGreater(ret, 0.0)


class TestNelderMeadErrors(unittest.TestCase):
    __doc__ = '\n    Test the Nelder Mead errors helper function\n    '

    def setUp(self):
        self.n = 2
        self.sim = np.array([[0, 0], [1, 0], [0, 1]])
        self.ymin = 1.42

        def identity_curvature(x):
            return self.ymin + (0.5 * np.sum(x ** 2) if x.ndim == 1 else 0.5 * np.sum(x ** 2, axis=1))

        self.fun = identity_curvature
        self.fsim = self.fun(self.sim)
        self.default_args = {'sim': self.sim, 
         'fun': self.fun, 
         'fsim': self.fsim}

    def tearDown(self):
        pass

    def test_call(self):
        """
        Test function call
        """
        self.assertTrue(hasattr(fssa.fssa, '_neldermead_errors'), msg='No such function: fssa.fssa._neldermead_errors')

    def test_signature(self):
        """
        Test function signature
        """
        try:
            args = inspect.signature(fssa.fssa._neldermead_errors).parameters
        except:
            args = inspect.getargspec(fssa.fssa._neldermead_errors).args

        fields = ['sim', 'fsim', 'fun']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_return_errors_and_varco_matrix(self):
        """
        Test that the function returns the standard errors and the whole
        variance--covariance matrix
        """
        errors, varco = fssa.fssa._neldermead_errors(**self.default_args)
        self.assertTupleEqual(errors.shape, (self.n,))
        self.assertTupleEqual(varco.shape, (self.n, self.n))

    def test_identity_hessian(self):
        """
        Test function returns correct errors and variance--covariance matrix
        for identity hessian (curvature)
        """
        errors, varco = fssa.fssa._neldermead_errors(**self.default_args)
        self.assertTrue(np.allclose(errors, np.sqrt(2.0 * self.ymin)))
        self.assertTrue(np.allclose(varco, 2.0 * self.ymin * np.eye(self.n)))

    def test_ellipsoidal_hessian(self):
        """
        Test function returns correct errors and variance--covariance matrix
        for ellipsoidal hessian (curvature)
        """
        args = copy.deepcopy(self.default_args)

        def ellipsoidal_curvature(x):
            return self.ymin + (0.5 * np.sum(x ** 2) - 0.5 * np.prod(x) if x.ndim == 1 else 0.5 * np.sum(x ** 2, axis=1) - 0.5 * np.prod(x, axis=1))

        args['fun'] = ellipsoidal_curvature
        errors, varco = fssa.fssa._neldermead_errors(**args)
        self.assertTrue(np.allclose(errors, np.sqrt(2.0 * self.ymin * 4.0 / 3.0)))
        self.assertTrue(np.allclose(varco, 2.0 * self.ymin * np.eye(self.n) * 4.0 / 3.0 + (np.ones((self.n, self.n)) - np.eye(self.n)) * 2.0 * self.ymin * 2.0 / 3.0))


class TestAutoscale(unittest.TestCase):
    __doc__ = '\n    Test the autoscale function\n    '

    def setUp(self):
        self.l = [
         10, 100, 1000]
        self.rho = np.linspace(0.9, 1.1)
        l_mesh, rho_mesh = np.meshgrid(self.l, self.rho, indexing='ij')
        self.x = np.power(l_mesh, 0.5) * (rho_mesh - 1.0)

        def master_curve(x):
            return 1.0 / (1.0 + np.exp(-x))

        self.master_curve = master_curve
        self.y = self.master_curve(self.x)
        self.y += np.random.randn(*self.y.shape) * self.y / 100.0
        self.dy = self.y / 100.0
        self.a = self.y
        self.da = self.dy
        self.rho_c0 = 0.95
        self.nu0 = 2.0
        self.zeta0 = 0.0
        self.rho_c = 1.0
        self.nu = 2.0
        self.zeta = 0.0
        self.default_args = {'l': self.l, 
         'rho': self.rho, 
         'a': self.a, 
         'da': self.da, 
         'rho_c0': self.rho_c0, 
         'nu0': self.nu0, 
         'zeta0': self.zeta0}

    def tearDown(self):
        pass

    def test_call(self):
        """
        Test function call
        """
        self.assertTrue(hasattr(fssa, 'autoscale'), msg='No such function: fssa.autoscale')

    def test_signature(self):
        """
        Test function signature
        """
        try:
            args = inspect.signature(fssa.autoscale).parameters
        except:
            args = inspect.getargspec(fssa.autoscale).args

        fields = ['l', 'rho', 'a', 'da', 'rho_c0', 'nu0', 'zeta0']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, args)
            except AttributeError:
                self.assertIn(field, args)

    def test_return_type(self):
        """
        Test that function returns correct type
        """
        res = fssa.autoscale(**self.default_args)
        fields = [
         'success', 'x', 'rho', 'nu', 'zeta', 'drho', 'dnu', 'dzeta',
         'errors', 'varco']
        for field in fields:
            try:
                with self.subTest(i=field):
                    self.assertIn(field, res)
            except AttributeError:
                self.assertIn(field, res)


if __name__ == '__main__':
    unittest.main()
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/matrixtest.py
# Compiled at: 2015-05-28 03:50:17
import unittest, random
from copy import copy
from pycast.common.matrix import Matrix
from pycast.common.matrix import Vector
from pycast.common.matrix import sign, pythag
from pycast.common.timeseries import TimeSeries
from pycast.common.timeseries import MultiDimensionalTimeSeries as MDTS
PRECISION = 4

class MatrixTest(unittest.TestCase):
    """Test class for the matrix"""

    def init_test(self):
        """Test the initialization of a matrix."""
        rows = random.randint(1, 1000)
        cols = random.randint(1, 1000)
        matrix = Matrix(cols, rows)
        assert matrix.get_height() == rows
        assert matrix.get_width() == cols

    def init_negative_number_of_columns_test(self):
        """Test for ValueError, if columns is less then 1."""
        rows = random.randint(1, 1000)
        cols = random.randint(-1000, 0)
        self.assertRaises(ValueError, Matrix, cols, rows)

    def init_negative_number_of_rows_test(self):
        """Test for ValueError, if columns is less then 1."""
        cols = random.randint(1, 1000)
        rows = random.randint(-1000, 0)
        self.assertRaises(ValueError, Matrix, cols, rows)

    def init_with_one_dimensional_column_based_array_test(self):
        """Test the initialization with a one dimensional column based array."""
        data = [
         1, 2, 3, 4]
        mtrx = Matrix(2, 2, data, rowBased=False)
        exRes = [[1, 2], [3, 4]]
        res = mtrx.matrix
        self.assertEqual(exRes, res)

    def init_with_one_dimensional_row_based_array_test(self):
        """Test the initialization with a one dimensional row based array."""
        data = [
         1, 2, 3, 4]
        mtrx = Matrix(2, 2, data, rowBased=True)
        exRes = [[1, 3], [2, 4]]
        res = mtrx.matrix
        self.assertEqual(exRes, res)

    def init_with_one_dimensional_array_value_error_test(self):
        """Test for ValueError, if length of one dimensional array does not fit."""
        data = [
         1, 2, 3, 4, 5]
        self.assertRaises(ValueError, Matrix, 2, 2, data)

    def init_with_tow_dimensional_row_based_array_test(self):
        """Test the initialization with a two dimensional row based array"""
        rows = 4
        cols = 5
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6],
         [
          1, 6, 4, 3, 9]]
        exRes = [
         [
          1, 4, 3, 1],
         [
          2, 5, 5, 6],
         [
          3, 6, 4, 4],
         [
          4, 7, 8, 3],
         [
          5, 8, 6, 9]]
        matrix = Matrix(cols, rows, oneDimArray=data, rowBased=True, isOneDimArray=False)
        dstArr = matrix.matrix
        self.assertEqual(exRes, dstArr)

    def initialization_with_row_based_list_test(self):
        """Test setting the matrix values using a row based list."""
        rows = 4
        cols = 5
        matrix = Matrix(cols, rows)
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6],
         [
          1, 6, 4, 3, 9]]
        matrix.initialize(data, rowBased=True)
        exRes = [
         [
          1, 4, 3, 1],
         [
          2, 5, 5, 6],
         [
          3, 6, 4, 4],
         [
          4, 7, 8, 3],
         [
          5, 8, 6, 9]]
        dstArr = matrix.matrix
        self.assertEqual(exRes, dstArr)

    def initialization_with_column_based_list_test(self):
        """Test setting the matrix values using a row based list."""
        rows = 5
        cols = 4
        mtrx = Matrix(cols, rows)
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6],
         [
          1, 6, 4, 3, 9]]
        mtrx.initialize(data, rowBased=False)
        self.assertEqual(data, mtrx.matrix)

    def row_based_initialization_wrong_rows_test(self):
        """Test for :py:exc:`ValueError` if datalist has less rows than the Matrix."""
        rows = 4
        cols = 5
        matrix = Matrix(cols, rows)
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6]]
        self.assertRaises(ValueError, matrix.initialize, data, True)

    def column_based_initialization_with_wrong_rows_test(self):
        """Test for ValueError if number of rows does not match."""
        rows = 4
        cols = 3
        mtrx = Matrix(cols, rows)
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6]]
        self.assertRaises(ValueError, mtrx.initialize, data, False)

    def column_based_initialization_with_wrong_columns_test(self):
        """Test for ValueError in initialize() if number of columns does not match."""
        rows = 2
        cols = 3
        mtrx = Matrix(cols, rows)
        data = [
         [
          1, 2],
         [
          3, 4],
         [
          5, 6],
         [
          7, 9]]
        self.assertRaises(ValueError, mtrx.initialize, data, False)

    def initialization_wrong_cols_test(self):
        """Test for :py:exc:`ValueError` in initialize() if data array has different number of columns."""
        rows = 2
        cols = 3
        data = [
         [
          2, 3],
         [
          1, 2, 4]]
        matrix = Matrix(cols, rows)
        self.assertRaises(ValueError, matrix.initialize, data, True)

    def create_from_timeseries_test(self):
        """Test to create a Matrix from a one dimensional Timeseries."""
        dataOne = [
         [
          0.0, 0.0],
         [
          0.1, 0.1],
         [
          0.2, 0.2],
         [
          0.3, 0.3],
         [
          0.4, 0.4],
         [
          0.5, 0.5]]
        tsOne = TimeSeries.from_twodim_list(dataOne)
        mtrx = Matrix.from_timeseries(tsOne)
        exRes = [[ entry[1] for entry in dataOne ]]
        self.assertEqual(mtrx.matrix, exRes)

    def create_from_multi_dimensional_timeseries_test(self):
        """Test to cretae a Matrix from a multi dimensional Timeseries."""
        dataOne = [
         [
          0.0, [0.0, 1.3]],
         [
          0.1, [0.5, 3.5]],
         [
          0.2, [0.2, 4.7]]]
        tsOne = MDTS.from_twodim_list(dataOne, dimensions=2)
        mtrx = Matrix.from_timeseries(tsOne)
        exRes = [
         [
          0.0, 0.5, 0.2],
         [
          1.3, 3.5, 4.7]]
        self.assertEqual(mtrx.matrix, exRes)

    def create_from_empty_timeseries_test(self):
        """Test for :py:exc:`ValueError` when creating a Matrix from an empty Timeseries."""
        ts = TimeSeries()
        self.assertRaises(ValueError, Matrix.from_timeseries, ts)

    def create_from_two_dim_array_test(self):
        rows = 5
        cols = 4
        data = [
         [
          1, 2, 3, 4, 5],
         [
          4, 5, 6, 7, 8],
         [
          3, 5, 4, 8, 6],
         [
          1, 6, 4, 3, 9]]
        matrix = Matrix.from_two_dim_array(cols, rows, data)
        self.assertEqual(data, matrix.matrix)

    def matrix_to_multi_dim_timeseries_test(self):
        """Test to create a Timeseries from a Matrix."""
        rows = 5
        cols = 3
        data = [
         [
          2.4, 4.5, 6.1],
         [
          3.6, 3.2, 9.4],
         [
          5.6, 3.2, 8.7],
         [
          4.3, 7.1, 3.3],
         [
          7.2, 9.6, 0.3]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, True)
        ts = mtrx.to_multi_dim_timeseries()
        tsData = [
         [
          0, [2.4, 4.5, 6.1]],
         [
          1, [3.6, 3.2, 9.4]],
         [
          2, [5.6, 3.2, 8.7]],
         [
          3, [4.3, 7.1, 3.3]],
         [
          4, [7.2, 9.6, 0.3]]]
        exTs = MDTS.from_twodim_list(tsData, dimensions=3)
        self.assertEqual(ts, exTs)
        row = 3
        ts[row] = [row, 4, 3, 1]
        for col in xrange(cols):
            self.assertEqual(mtrx.get_value(col, row), data[row][col])

    def matrix_string_representation_test(self):
        """Test the String representation of a Matrix instance."""
        matrix = Matrix(2, 2)
        a = [[1, 2], [-3, 4]]
        matrix.initialize(a, rowBased=True)
        rep = matrix.__str__()
        self.assertTrue(rep.find('  1.0') >= 0)
        self.assertTrue(rep.find(' -3.0') >= 0)
        self.assertFalse(rep.find('  -3.0') >= 0)
        self.assertTrue(rep.find('Matrix') >= 0)

    def matrix_string_representation_with_precision_test(self):
        """Test if the precision is set correctly and used when printing a Matrix.
        """
        size = 2
        data = [
         [
          1.0123343, -2.012341234123],
         [
          3.04674567566, 4.01234123412]]
        mtrx = Matrix(size, size)
        mtrx.initialize(data, rowBased=True)
        mtrx.set_string_precision(4)
        rep = mtrx.__str__()
        self.assertTrue(rep.find(' 3.0467 ') >= 0)
        self.assertTrue(rep.find(' -2.0123') >= 0)
        self.assertFalse(rep.find(' 3.04674567566') >= 0)
        self.assertFalse(rep.find(' -2.012341234123 ') >= 0)
        mtrx.set_string_precision(2)
        rep = mtrx.__str__()
        print mtrx
        self.assertTrue(rep.find(' 3.05 ') >= 0)
        self.assertTrue(rep.find(' -2.01') >= 0)

    def equality_test(self):
        """Test the == operator for Matrix instances."""
        rows = 3
        cols = 2
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        mtrx1 = Matrix(cols, rows)
        mtrx2 = Matrix(cols, rows)
        mtrx3 = Matrix(cols, rows)
        mtrx1.initialize(data, rowBased=False)
        mtrx2.initialize(data, rowBased=False)
        mtrx3.initialize(data, rowBased=False)
        mtrx2.set_value(1, 2, 4)
        mtrx3.set_value(0, 1, 2.0)
        self.assertTrue(mtrx1 == mtrx3)
        self.assertTrue(mtrx1 != mtrx2)
        self.assertTrue(mtrx2 != mtrx3)

    def get_array_test(self):
        """Test if get_array method returns an array with the correct values."""
        rows = 2
        cols = 3
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        for row in xrange(rows):
            for col in xrange(cols):
                self.assertEqual(matrix.get_value(col, row), data[row][col])

    def get_matrix_from_list_test(self):
        """Test to create a Matrix from a one dimensional list."""
        rows = 2
        cols = 3
        mtrx = Matrix(cols, rows)
        data = [1, 2, 3, 4, 5, 6]
        exRes = [[1, 2, 3], [4, 5, 6]]
        newMtrx = mtrx.get_matrix_from_list(rows, cols, data, rowBased=True)
        self.assertEqual(newMtrx.get_array(rowBased=True), exRes)

    def get_value_test(self):
        """Test if the correct value of the Matrix is returned."""
        rows = 2
        cols = 3
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        val1 = matrix.get_value(1, 0)
        val2 = matrix.get_value(2, 1)
        self.assertEqual(val1, 2)
        self.assertEqual(val2, 6)

    def set_value_test(self):
        """Test if the new value is correctly set in the matrix."""
        rows = 2
        cols = 3
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        matrix.set_value(1, 0, 10)
        matrix.set_value(2, 1, 9)
        self.assertEqual(matrix.matrix[1][0], 10)
        self.assertEqual(matrix.matrix[2][1], 9)

    def set_string_precision_error_value_test(self):
        """Test for :py:exc:`ValueError` when trying to set the precision to a negative value."""
        size = 2
        data = [[1, 2], [3, 4]]
        mtrx = Matrix(size, size)
        mtrx.initialize(data, rowBased=True)
        self.assertRaises(ValueError, mtrx.set_string_precision, -2)

    def copy_test(self):
        """Test to clone the Matrix."""
        rows = 2
        cols = 3
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        mtrx.optimizationEnabled = True
        cp = copy(mtrx)
        self.assertEqual(cp, mtrx)
        mtrx.set_value(2, 0, 10)
        mtrx.optimizationEnabled = False
        self.assertNotEqual(cp, mtrx)
        self.assertNotEqual(mtrx.get_value(2, 0), cp.get_value(2, 0))
        self.assertTrue(cp.optimizationEnabled)

    def invers_test(self):
        """Test the calculation of the inverse."""
        size = 2
        data = [
         [
          1.0, 2.0],
         [
          3.0, 4.0]]
        exRes = [
         [
          -2.0, 1.5],
         [
          1.0, -0.5]]
        matrix = Matrix(size, size)
        matrix.initialize(data, rowBased=True)
        res = matrix.invers()
        self.assertEqual(res.matrix, exRes)

    def invers_value_error_test(self):
        """Test if a :py:exc:`ValueError` is raised if Matrix is not regular"""
        rows = 2
        cols = 3
        data = [
         [
          1, 2, 3],
         [
          4, 5, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        self.assertRaises(ValueError, matrix.invers)

    def matrix_multiplication_test(self):
        """Test the matrixmultplication of two matrices."""
        rows1 = 2
        cols1 = 3
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          3, 4],
         [
          5, -6],
         [
          7, 8]]
        exRes = [
         [
          14.0, 55.0],
         [
          40.0, 2.0]]
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(rows1, cols1)
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        res = mtrx1.matrix_multiplication(mtrx2)
        self.assertEqual(res.matrix, exRes)

    def is_matrix_mult_possible_false_test(self):
        """Test if matrix_mult_possible() returns False, if matrices cannot be multiplied."""
        rows1 = 2
        cols1 = 3
        rows2 = 4
        cols2 = 2
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(cols2, rows2)
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          3, 4],
         [
          5, -6],
         [
          7, 8],
         [
          2, 4]]
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        res = mtrx1.is_matrix_mult_possible(mtrx2)
        self.assertFalse(res)

    def is_matrix_mult_possible_true_test(self):
        """Test if matrix_mult_possible() returns True, if matrices can be multiplied."""
        rows1 = 2
        cols1 = 3
        rows2 = 3
        cols2 = 2
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(cols2, rows2)
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          3, 4],
         [
          5, -6],
         [
          7, 8]]
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        res = mtrx1.is_matrix_mult_possible(mtrx2)
        self.assertTrue(res)

    def matrix_multiplication_square_test(self):
        """Test the matrix_multiplication with a square matrix"""
        size = 33
        array = [ [ 1.0 for i in range(size) ] for j in range(size) ]
        matrix = Matrix(size, size)
        matrix2 = Matrix(size, size)
        matrix.initialize(array, rowBased=True)
        matrix2.initialize(array, rowBased=True)
        result = matrix * matrix2
        expRes = [ [ size for i in range(size) ] for j in range(size) ]
        self.assertEqual(expRes, result.matrix)

    def mul_type_error_test(self):
        """Test for TypeError, if Matrix is multiplied with a String

        or a String is multiplied with a Matrix."""
        rows = 3
        cols = 2
        data = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        try:
            mtrx * 'Test'
        except TypeError:
            pass
        else:
            raise AssertionError

        try:
            'Test' * mtrx
        except TypeError:
            pass
        else:
            raise AssertionError

    def mul_matrix_test(self):
        """Test numeric multiplication on Matrices."""
        rows1 = 3
        cols1 = 2
        rows2 = 2
        cols2 = 4
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(cols2, rows2)
        data1 = [
         [
          1, -2],
         [
          -4, 5],
         [
          3, 6]]
        data2 = [
         [
          3, 4, 5, 6],
         [
          5, -6, 4, 5]]
        exRes = [
         [
          -7, 13, 39],
         [
          16, -46, -24],
         [
          -3, 0, 39],
         [
          -4, 1, 48]]
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        res = mtrx1 * mtrx2
        self.assertEqual(res.matrix, exRes)

    def mul_with_number_test(self):
        """Test the multiplication with an integer."""
        rows = 3
        cols = 2
        data = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        multi = 2
        expRes = [ [ col * multi for col in row ] for row in data ]
        res = multi * mtrx
        self.assertEqual(res.matrix, expRes)

    def mult_associative_test(self):
        """Test if the multiplication with an integer is associative."""
        rows = 3
        cols = 2
        data = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        multi = 2
        res1 = multi * mtrx
        res2 = mtrx * multi
        self.assertEqual(res1.matrix, res2.matrix)

    def transform_test(self):
        """Test matrix transformation."""
        rows = 3
        cols = 2
        data = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        exRes = [
         [
          1, -4],
         [
          -2, 5],
         [
          3, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        res = mtrx.transform()
        self.assertEqual(res.matrix, exRes)

    def gauss_jordan_test(self):
        """Test gauss_jordan algorithm for the calculation of the inverse."""
        rows = 3
        cols = 6
        data = [
         [
          1, 2, 0, 1, 0, 0],
         [
          2, 3, 0, 0, 1, 0],
         [
          3, 4, 1, 0, 0, 1]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        exRes = [
         [
          1, 0, 0],
         [
          0, 1, 0],
         [
          0, 0, 1],
         [
          -3, 2, 1],
         [
          2, -1, -2],
         [
          0, 0, 1]]
        res = mtrx.gauss_jordan()
        self.assertEqual(res.matrix, exRes)

    def gauss_jordan_switch_column_test(self):
        """Test the gauss jordan algorithm if the first values is zero.

        This test checks, if the lines are switched correctly.
        """
        rows = 3
        cols = 6
        data = [
         [
          0, 2, 0, 1, 0, 0],
         [
          2, 3, 0, 0, 1, 0],
         [
          3, 4, 1, 0, 0, 1]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        exRes = [
         [
          1.0, 0.0, 0.0],
         [
          0.0, 1.0, 0.0],
         [
          0.0, 0.0, 1.0],
         [
          -0.75, 0.5, 0.25],
         [
          0.5, 0.0, -1.5],
         [
          0.0, 0.0, 1.0]]
        res = mtrx.gauss_jordan()
        self.assertEqual(res.matrix, exRes)

    def gauss_jordan_value_error_test(self):
        """Test for ValueError in gauss_jordan(), if matrix has wrong size."""
        rows = 3
        cols = 3
        data = [
         [
          0, 2, 0],
         [
          2, 3, 0],
         [
          3, 4, 1]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        self.assertRaises(ValueError, mtrx.gauss_jordan)

    def gauss_jordan_linear_equation_system_test(self):
        """Test gauss_jordan algorithm to solve a linear equation system."""
        rows = 3
        cols = 4
        data = [
         [
          1, 1, 1, 0],
         [
          4, 2, 1, 1],
         [
          9, 3, 1, 3]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        exRes = [
         [
          1.0, 0.0, 0.0],
         [
          0.0, 1.0, 0.0],
         [
          0.0, 0.0, 1.0],
         [
          0.5, -0.5, 0]]
        res = mtrx.gauss_jordan()
        self.assertEqual(res.matrix, exRes)

    def gauss_jordan_non_singular_matrix_test(self):
        """Test for ValueError, if the Matrix is not invertible."""
        rows = 3
        cols = 6
        data = [
         [
          0, 2, 0, 1, 0, 0],
         [
          0, 3, 0, 0, 1, 0],
         [
          3, 4, 1, 0, 0, 1]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        self.assertRaises(ValueError, mtrx.gauss_jordan)

    def add_matrix_test(self):
        """Test addition of two matrices."""
        rows = 2
        cols = 3
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          2, 4, -3],
         [
          5, -7, 3]]
        mtrx1 = Matrix(cols, rows)
        mtrx2 = Matrix(cols, rows)
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        expRes = [[3, 1], [2, -2], [0, 9]]
        res = mtrx1 + mtrx2
        self.assertEqual(res.matrix, expRes)

    def add_matrix_value_error_test(self):
        """Test for ValueError, when adding matrices of different size."""
        rows1 = 2
        cols1 = 3
        rows2 = 3
        cols2 = 3
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          2, 4, -3],
         [
          5, -7, 3],
         [
          5, -7, 3]]
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(cols2, rows2)
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        try:
            mtrx1 + mtrx2
        except ValueError:
            pass
        else:
            raise AssertionError

    def sub_matrix_test(self):
        """Test subtraction of two matrices."""
        rows = 2
        cols = 3
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          2, 4, -3],
         [
          5, -7, 3]]
        mtrx1 = Matrix(cols, rows)
        mtrx2 = Matrix(cols, rows)
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        expRes = [[-1, -9], [-6, 12], [6, 3]]
        res = mtrx1 - mtrx2
        self.assertEqual(res.matrix, expRes)

    def sub_matrix_value_error_test(self):
        """Test for ValueError, when subtracting matrices of different size."""
        rows1 = 2
        cols1 = 3
        rows2 = 3
        cols2 = 3
        data1 = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        data2 = [
         [
          2, 4, -3],
         [
          5, -7, 3],
         [
          5, -7, 3]]
        mtrx1 = Matrix(cols1, rows1)
        mtrx2 = Matrix(cols2, rows2)
        mtrx1.initialize(data1, rowBased=True)
        mtrx2.initialize(data2, rowBased=True)
        try:
            mtrx1 - mtrx2
        except ValueError:
            pass
        else:
            raise AssertionError

    def div_matrix_test(self):
        """Test the division of a matrix by a number."""
        rows = 3
        cols = 2
        data = [
         [
          1, -2, 3],
         [
          -4, 5, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=False)
        divider = 2
        expRes = [ [ col / float(divider) for col in row ] for row in data ]
        res = mtrx / divider
        self.assertEqual(res.matrix, expRes)

    def householder_with_zero_column_test(self):
        """Test the householder transformation of a Matrix with a 0 column

        All values of the 2nd column are 0."""
        c = [
         [
          3, 0, 3, 2],
         [
          0, 0, 5, 6],
         [
          4, 0, 4, 7],
         [
          8, 0, 3, 9]]
        matrix = Matrix(4, 4)
        matrix.initialize(c, rowBased=True)
        u, bidiag, v = matrix.householder()
        res = u * bidiag * v
        for row in range(res.get_height()):
            for col in range(res.get_width()):
                self.assertAlmostEqual(res.get_value(col, row), c[row][col], PRECISION)

    def householder_test(self):
        """Test the householder transformation to get a matrix in bidiagonalization."""
        c = [
         [
          4, 3, 0],
         [
          2, 1, 2],
         [
          4, 4, 0]]
        matrix = Matrix(3, 3)
        matrix.initialize(c, rowBased=True)
        u, bidiag, v = matrix.householder()
        res = u * bidiag * v
        for row in range(res.get_height()):
            for col in range(res.get_width()):
                self.assertAlmostEqual(res.get_value(col, row), c[row][col], PRECISION)

        self.assertAlmostEqual(bidiag.get_value(0, 1), 0, PRECISION)
        self.assertAlmostEqual(bidiag.get_value(0, 2), 0, PRECISION)
        self.assertAlmostEqual(bidiag.get_value(1, 2), 0, PRECISION)
        self.assertAlmostEqual(bidiag.get_value(2, 0), 0, PRECISION)

    def svd_test(self):
        """Test the Singular Value Decomposition."""
        a = [
         [
          22.0, 10.0, 2.0, 3.0, 7.0],
         [
          14.0, 7.0, 10.0, 0.0, 8.0],
         [
          -1.0, 13.0, -1.0, -11.0, 3.0],
         [
          -3.0, -2.0, 13.0, -2.0, 4.0],
         [
          9.0, 8.0, 1.0, -2.0, 4.0],
         [
          9.0, 1.0, -7.0, 5.0, -1.0],
         [
          2.0, -6.0, 6.0, 5.0, 1.0],
         [
          4.0, 5.0, 0.0, -2.0, 2.0]]
        matrix = Matrix(5, 8)
        matrix.initialize(a, rowBased=True)
        u, diag, v = matrix.svd()
        res = u * diag * v.transform()
        for row in range(res.get_height()):
            for col in range(res.get_width()):
                self.assertAlmostEqual(res.get_value(col, row), a[row][col], PRECISION)

    def svd_diagional_test(self):
        """Test if the one Matrix of svd() is in diagonal form."""
        a = [[22.0, 10.0, 2.0, 3.0, 7.0],
         [
          14.0, 7.0, 10.0, 0.0, 8.0],
         [
          -1.0, 13.0, -1.0, -11.0, 3.0],
         [
          -3.0, -2.0, 13.0, -2.0, 4.0],
         [
          9.0, 8.0, 1.0, -2.0, 4.0],
         [
          9.0, 1.0, -7.0, 5.0, -1.0],
         [
          2.0, -6.0, 6.0, 5.0, 1.0],
         [
          4.0, 5.0, 0.0, -2.0, 2.0]]
        matrix = Matrix(5, 8)
        matrix.initialize(a, rowBased=True)
        u, diag, v = matrix.svd()
        for row in range(diag.get_height()):
            for col in range(diag.get_width()):
                if row != col:
                    self.assertEqual(diag.get_value(col, row), 0.0)

    def svd_unitary_test(self):
        """Test if matrices u and v are unitary."""
        a = [
         [
          22.0, 10.0, 2.0, 3.0, 7.0],
         [
          14.0, 7.0, 10.0, 0.0, 8.0],
         [
          -1.0, 13.0, -1.0, -11.0, 3.0],
         [
          -3.0, -2.0, 13.0, -2.0, 4.0],
         [
          9.0, 8.0, 1.0, -2.0, 4.0],
         [
          9.0, 1.0, -7.0, 5.0, -1.0],
         [
          2.0, -6.0, 6.0, 5.0, 1.0],
         [
          4.0, 5.0, 0.0, -2.0, 2.0]]
        matrix = Matrix(5, 8)
        matrix.initialize(a, rowBased=True)
        u, diag, v = matrix.svd()
        res = u.transform() * u
        res1 = v * v.transform()
        for row in range(res.get_height()):
            for col in range(res.get_width()):
                if row == col:
                    self.assertAlmostEqual(res.get_value(col, row), 1, PRECISION)
                    self.assertAlmostEqual(res1.get_value(col, row), 1, PRECISION)
                else:
                    self.assertAlmostEqual(res.get_value(col, row), 0, PRECISION)
                    self.assertAlmostEqual(res1.get_value(col, row), 0, PRECISION)

    def svd_value_error_test(self):
        """Test for ValueError in svd(), if Matrix has more columns than rows.

        May be removed if algorithm also works with these matrices.
        """
        rows = 2
        cols = 4
        data = [
         [
          -11, 2, -5.0, 7.0],
         [
          2, -4, 3.4, 5.4]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        self.assertRaises(ValueError, mtrx.svd)

    def pseudoinverse_test(self):
        """Test that the pseudoinverse is calculated correctly."""
        rows = 3
        cols = 2
        data = [
         [
          1, 2],
         [
          2, 4],
         [
          3, 6]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        exRes = [
         [
          0.01428571, 0.02857143, 0.04285714],
         [
          0.02857143, 0.05714286, 0.08571429]]
        res = mtrx.pseudoinverse()
        self.assertEqual(res.get_width(), rows)
        self.assertEqual(res.get_height(), cols)
        for row in range(cols):
            for col in range(rows):
                self.assertAlmostEqual(exRes[row][col], res.get_value(col, row))

    def pseudoinverse_with_more_columns_test(self):
        """Test to calculate the pseudoinverse of a Matrix with more columns than rows."""
        rows = 2
        cols = 4
        data = [
         [
          -11, 2, -5.0, 7.0],
         [
          2, -4, 3.4, 5.4]]
        mtrx = Matrix(cols, rows)
        mtrx.initialize(data, rowBased=True)
        exRes = [
         [
          -0.0541328, 0.02473614],
         [
          0.00705413, -0.06480734],
         [
          -0.02269591, 0.05255596],
         [
          0.03956448, 0.09492743]]
        res = mtrx.pseudoinverse()
        self.assertEqual(res.get_width(), rows)
        self.assertEqual(res.get_height(), cols)
        for row in range(cols):
            for col in range(rows):
                self.assertAlmostEqual(exRes[row][col], res.get_value(col, row))

    def blockwise_multiplication_test(self):
        data = range(1, 33)
        a = Matrix(4, 2, data[:8])
        b = Matrix(6, 4, data[8:])
        result = [
         210.0, 220.0, 230.0, 240.0, 250.0, 260.0,
         498.0, 524.0, 550.0, 576.0, 602.0, 628.0]
        resultMatrix = Matrix(6, 2, result)
        calculated = a.matrix_multiplication_blockwise(b, 2)
        self.assertEqual(resultMatrix, calculated)

    def blockwise_with_zero_expansion_test(self):
        a = Matrix(4, 4, [1, 2, 3, 0, 4, 5, 6, 0, 7, 8, 9, 0, 0, 0, 0, 0])
        b = Matrix(4, 4, [1, 2, 3, 0, 4, 5, 6, 0, 7, 8, 9, 0, 0, 0, 0, 0])
        calculated = a.matrix_multiplication_blockwise(b, 2)
        result = Matrix(4, 4, [
         30.0, 36.0, 42.0, 0, 66.0, 81.0, 96.0, 0,
         102.0, 126.0, 150.0, 0, 0, 0, 0, 0])
        self.assertEqual(result, calculated)

    def flatten_test(self):
        a = Matrix(2, 2, [2, 2, 2, 2])
        b = Matrix(2, 2, [a, a, a, a])
        result = Matrix(4, 4, [2] * 16)
        calculated = b.flatten()
        self.assertTrue(calculated, result)

    def matrix_to_blockmatrix_test(self):
        data = range(16)
        calculated = Matrix(4, 4, data).matrix_to_blockmatrix(2)
        a1 = Matrix(2, 2, [0, 1, 4, 5])
        a2 = Matrix(2, 2, [2, 3, 6, 7])
        a3 = Matrix(2, 2, [8, 9, 12, 13])
        a4 = Matrix(2, 2, [10, 11, 14, 15])
        result = Matrix(2, 2, [a1, a2, a3, a4])
        self.assertEqual(result, calculated)
        self.assertRaises(ValueError, Matrix(4, 4, data).matrix_to_blockmatrix, 3)


class VectorTest(unittest.TestCase):
    """Test class for the Vector"""

    def init_test(self):
        """Test the initialization of a Vector."""
        rows = random.randint(1, 1000)
        vector = Vector(rows)
        self.assertEqual(vector.get_height(), rows)

    def norm_test(self):
        """Test the length calculation of a Vector."""
        rows = 3
        data = [[6], [4], [5]]
        vector = Vector(rows)
        vector.initialize(data, rowBased=True)
        exRes = 8.774964387392123
        res = vector.norm()
        self.assertEqual(res, exRes)

    def unify_test(self):
        """Test if the matrix is unified correctly."""
        rows = 3
        data = [[0], [4], [3]]
        vector = Vector(rows)
        vector.initialize(data, rowBased=True)
        exRes = [[0, 4 / 5.0, 3 / 5.0]]
        res = vector.unify()
        self.assertEqual(res.matrix, exRes)

    def initialize_from_matrix_test(self):
        """Test to create a Vector from a specified column of a Matrix."""
        rows = 3
        cols = 2
        data = [
         [
          1, -4],
         [
          -2, 5],
         [
          3, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        vector = Vector.initialize_from_matrix(matrix, 1)
        exRes = [[-4, 5, 6]]
        self.assertEqual(vector.matrix, exRes)

    def initialize_from_matrix_value_error_test(self):
        """Test for IndexError when creating a Vector from a Matrix,
        which does not have the specified column.
        """
        rows = 3
        cols = 2
        data = [
         [
          1, -4],
         [
          -2, 5],
         [
          3, 6]]
        matrix = Matrix(cols, rows)
        matrix.initialize(data, rowBased=True)
        self.assertRaises(IndexError, Vector.initialize_from_matrix, matrix, 3)


class MatrixHelperTest(unittest.TestCase):
    """Test helper methods used in Matrix class."""

    def pythag_test(self):
        """Test the pythag method."""
        a = 4
        b = 3
        res = pythag(a, b)
        self.assertEqual(res, 5)
        res = pythag(b, a)
        self.assertEqual(res, 5)
        res = pythag(0, 0)
        self.assertEqual(res, 0)

    def sign_test(self):
        """Test if the sign method return a with th algebraic sign of b."""
        a = 2
        b = -3
        res = sign(a, b)
        self.assertEqual(res, -2)
        a = -2
        b = -3
        res = sign(a, b)
        self.assertEqual(res, -2)
        a = -2
        b = 3
        res = sign(a, b)
        self.assertEqual(res, 2)
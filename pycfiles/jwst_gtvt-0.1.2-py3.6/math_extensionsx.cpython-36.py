# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/jwst_gtvt/math_extensionsx.py
# Compiled at: 2020-02-10 11:10:52
# Size of source mod 2**32: 26272 bytes
from __future__ import print_function
from math import *
import copy
R2D = 180.0 / pi
D2R = 1 / R2D
EPSILON = 1e-10
OBLIQUITY = 23.43929 * D2R

def really_less_than(x, y):
    """Safe less-than function that returns true if and only if x is "significantly" less than y."""
    return x < y - EPSILON


def really_greater_than(x, y):
    """Safe greater-than function that returns true if and only if x is "significantly" greater than y."""
    return x > y + EPSILON


def asin2(val):
    """Safe version of asin that handles invalid arguments.
        
        Arguments greater than 1 are truncated to 1; arguments less than -1 are set to -1."""
    return asin(max(-1.0, min(1.0, val)))


def acos2(val):
    """Safe version of acos that handles invalid arguments in the same way as asin2."""
    return acos(max(-1.0, min(1.0, val)))


def avg(l):
    """Returns the average of a list of numbers."""
    return sum(l) / float(len(l))


def avg2(num1, num2):
    """Returns the average of two numbers."""
    return (num1 + num2) / 2.0


def output_as_percentage(num, fractional_digits=1):
    """Output a percentage neatly.
    
    fractional_digits = number of digits to output as fractions of a percent.
    If None is supplied, there is no reduction in precision."""
    if fractional_digits is not None:
        format_str = '%%.%.df' % fractional_digits
    else:
        format_str = '%f'
    return '%s%%' % (format_str % num)


def percent_str(num, fractional_digits=1):
    """Output a number as a percentage.
    
    fractional_digits = number of digits to output as fractions of a percent.
    If not supplied, there is no reduction in precision."""
    return output_as_percentage(100 * num, fractional_digits)


def variance(l):
    """Variance of a list of numbers that represent sample values."""
    mean = avg(l)
    sumsq = sum(map(lambda i: (i - mean) ** 2, l))
    return sumsq / float(len(l) - 1)


def stdev(l):
    """Standard deviation of a list of numbers that represent sample values."""
    return sqrt(variance(l))


def factorial(num):
    """Returns the factorial of a nonnegative integer.
    
    This function is provided in math module starting with Python 2.6,
    but implement anyway for compatibility with older systems."""
    result = 1
    for i in range(2, num + 1):
        result = result * i

    return result


def conditional_probability(p_joint, p_B):
    """Returns probability of event A given event B.
    
    p_joint = P(A,B)
    p_B = probability of event B."""
    return p_joint / p_B


class Polynomial(object):
    __doc__ = 'Class to represent a polynomial.'

    def __init__(self, coefficients):
        """Constructor for a polynomial.
        
        Coefficients = a list of coefficients, starting with order 0 and increasing."""
        self.coefficients = coefficients

    def __str__(self):
        """Returns a string representation of a polynomial."""
        order = len(self.coefficients) - 1
        return_string = 'Polynomial: order %d' % order
        for index in range(order + 1):
            return_string = return_string + '\nCoefficient %d = %.3f' % (index, self.coefficients[index])

        return return_string

    def apply(self, value):
        """Returns the result of applying a polynomial to an input value."""
        result = 0
        for index in range(len(self.coefficients)):
            result = result + self.coefficients[index] * value ** index

        return result


class LinearEquation(Polynomial):
    __doc__ = 'Subclass of Polynomial for linear equations.\n    \n    This implementation is three times faster, so Polynomial should be reserved for higher orders.'

    def __init__(self, coeff0, coeff1):
        """Constructor for a linear equation to provide a more 'natural' interface without using a list.
        
        Coeff0 = additive constant
        Coeff1 = multiplicative coefficient
        Coeff0 is first for consistency with list order in Polynomial coefficient list."""
        self.coefficients = [
         coeff0, coeff1]

    def apply(self, value):
        """Applies a linear equation to an input value.
        
        This is intended to be faster than the more general method with Polynomial."""
        return value * self.coefficients[1] + self.coefficients[0]


class HistogramBin(object):
    __doc__ = 'Class to represent a bin within a histogram.'

    def store_items(self, num_items=1):
        """Stores a given number of items in the bin.
        
        num_items = number of items to store (default 1)."""
        self.count += num_items


class DiscreteBin(HistogramBin):
    __doc__ = 'Class to represent a bin with a fixed value.'

    def __init__(self, bin_value):
        """Constructor for a fixed-value bin."""
        self.bin_value = bin_value
        self.count = 0

    def __str__(self):
        """Returns a printed representation of the bin."""
        return '%s: %s items' % (self.bin_value, self.count)

    def ismatch(self, value):
        """Returns True if the value matches the bin, False otherwise."""
        return value == self.bin_value


class RangeBin(HistogramBin):
    __doc__ = 'Class to represent a bin with a range.'

    def __init__(self, min_value=None, max_value=None, lower_inclusive=False, upper_inclusive=True):
        """Constructor for a range bin.
        
        min_value = minimum value for the bin.
        max_value = maximum value for the bin
        lower_inclusive = True if min_value is inclusive, False (default) otherwise.
        upper_inclusive = True (default) if max_value is inclusive, False otherwise."""
        self.min_value = min_value
        self.max_value = max_value
        self.lower_inclusive = lower_inclusive
        self.upper_inclusive = upper_inclusive
        self.count = 0

    def describe_limits(self, precision=2):
        """Returns a printed representation of the limits of the bin.
        
        precision = number of digits to print after the decimal point."""
        if self.min_value is None:
            if self.upper_inclusive:
                result = '<= %.*f:' % (precision, self.max_value)
            else:
                result = '< %.*f:' % (precision, self.max_value)
        else:
            if self.max_value is None:
                if self.lower_inclusive:
                    result = '>= %.*f:' % (precision, self.min_value)
                else:
                    result = '> %.*f:' % (precision, self.min_value)
            else:
                result = '%.*f to %.*f:' % (precision, self.min_value, precision, self.max_value)
        return result

    def __str__(self):
        """Returns a printed representation of the bin."""
        return '%s %s items' % (self.describe_limits(), self.count)

    def istoo_high(self, value):
        """Returns True if the specified value is too high for the bin.
        
        Assumes the bin has an upper limit."""
        if self.upper_inclusive:
            result = value > self.max_value
        else:
            result = value >= self.max_value
        return result

    def ismatch(self, value):
        """Indicates whether the bin matches the value."""
        return False


class Histogram(object):
    __doc__ = 'Class to represent a histogram.'

    def retrieve_count(self, bin_index):
        """Returns the number of items stored in a given bin of the histogram.
        
        Bin_index starts with 1."""
        return self.bins[(bin_index - 1)].count

    def num_items(self):
        """Returns the total number of items stored in the histogram."""
        return sum(map(lambda bin: bin.count, self.bins))

    def __str__(self):
        """Returns a printed representation of the histogram."""
        result = 'Histogram: %d bins, %s items\n' % (len(self.bins), self.num_items())
        for bin in self.bins:
            result = result + '%s\n' % bin.__str__()

        return result

    def normalize(self, total=None):
        """Takes a histogram and returns a new histogram that normalizes all its values.
        
        total = number of items to divide each bin by for the normalization.
        If not supplied, it defaults to the total in the histogram."""
        if total is None:
            total = self.num_items()
        new_histogram = copy.deepcopy(self)
        for bin in new_histogram.bins:
            bin.count = float(bin.count) / total

        return new_histogram


class DiscreteHistogram(Histogram):
    __doc__ = 'Class to represent a histogram with discrete values.'

    def __init__(self, values):
        """Initializes a histogram with discrete values.
        
        values = list of the discrete values."""
        self.bins = []
        for value in values:
            self.bins.append(DiscreteBin(value))

    def retrieve_values(self):
        """Returns the list of bin values of a discrete histogram."""
        return map(lambda bin: bin.bin_value, self.bins)

    def retrieve_count_by_value(self, value):
        """Returns the count matching a certain value.  If not found, return None."""
        bin_index = 0
        result = None
        while not result and bin_index < len(self.bins):
            bin = self.bins[bin_index]
            if bin.ismatch(value):
                result = bin.count
            bin_index += 1

        return result

    def store_items(self, value, count=1):
        """Stores a value in the discrete histogram if it matches one of the bin values.
        
        Count = number of items with that value to store (default 1).
        
        Returns True if a match was found and the value could be stored, False otherwise."""
        bin_index = 0
        found = False
        while not found and bin_index < len(self.bins):
            bin = self.bins[bin_index]
            if bin.ismatch(value):
                bin.store_items(count)
                found = True
            bin_index += 1

        return found


class ContinuousHistogram(Histogram):
    __doc__ = 'Class to represent a histogram with continuous values.'

    def __init__(self, boundaries, highest_inclusive=False):
        """Initializes a continuous histogram.
        
        boundaries = list of numbers that separate the bins, in increasing order.
        highest_inclusive = True if highest bin includes the last boundary, False (default) otherwise.
        Number of boundaries must be at least 2 if highest_inclusive = True, at least 1 otherwise.
        
        Default behavior with highest_inclusive = False:
           Bin 0 is defined by x <= boundaries[0].
           For i > 0, bin i is defined by boundaries[i-1] < x <= boundaries[i].
           Bin n+1 is defined by x > boundaries[n-1].
           
        Behavior with highest_exclusive = True:
           Bins below n are defined in the same way as above.
           Bin n is defined by boundaries[n-2] < x < boundaries[n-1].
           Bin n+1 is defined by x >= boundaries[n-1]."""
        self.bins = []
        self.highest_inclusive = highest_inclusive
        lower_limit = None
        for index in range(len(boundaries)):
            upper_limit = boundaries[index]
            self.bins.append(RangeBin(min_value=lower_limit, max_value=upper_limit))
            lower_limit = upper_limit

        self.bins.append(RangeBin(min_value=lower_limit))
        if highest_inclusive:
            self.bins[(-2)].upper_inclusive = False
            self.bins[(-1)].lower_inclusive = True

    def retrieve_boundaries(self):
        """Returns the list of boundaries of a continuous histogram."""
        return map(lambda bin: bin.max_value, self.bins[:-1])

    def store_items(self, value, count=1):
        """Stores a value in the continuous histogram.
        
        Count = number of items with that value to store (default 1)."""
        bin_index = 0
        found = False
        while not found and bin_index < len(self.bins) - 1:
            bin = self.bins[bin_index]
            if not bin.istoo_high(value):
                found = True
                bin.store_items(count)
            bin_index += 1

        if not found:
            self.bins[(-1)].store_items(count)


def combine_histograms(histograms):
    """Takes a list of histograms and returns a new Histogram object that sums the values in each bin.
    
    All histograms in the list must be identical except for the count."""
    if isinstance(histograms[0], ContinuousHistogram):
        new_histogram = ContinuousHistogram(histograms[0].retrieve_boundaries(), histograms[0].highest_inclusive)
    else:
        new_histogram = DiscreteHistogram(histograms[0].retrieve_values())
    for bin_index in range(len(new_histogram.bins)):
        total_items = sum(map(lambda hist: hist.bins[bin_index].count, histograms))
        new_histogram.bins[bin_index].store_items(total_items)

    return new_histogram


def average_histograms(histograms):
    """Takes a list of histogram objects and simply averages all the bin values.
    
    All histograms in the list must be identical except for the count."""
    new_histogram = copy.deepcopy(histograms[0])
    for bin_index in range(len(new_histogram.bins)):
        new_histogram.bins[bin_index].count = avg(map(lambda hist: hist.bins[bin_index].count, histograms))

    return new_histogram


class PoissonDistribution(DiscreteHistogram):
    __doc__ = 'Class to represent a Poisson distribution.'

    def probability(self, k):
        """Computes the probability that the Poisson distribution takes on the value k.
        
        Value must be a nonnegative integer."""
        u = self.mean
        return u ** k * exp(-u) / factorial(k)

    def generate_distribution(self):
        """Populates a Poisson distribution up to the maximum bin."""
        cum = 0
        for value in range(len(self.bins) - 1):
            self.bins[value].count = p = self.probability(value)
            cum += p

        self.bins[(-1)].count = 1.0 - cum

    def __init__(self, mean, max_boundary):
        """Constructor function for the Poisson distribution.
        
        Mean = mean parameter for the Poisson distribution.
        max_boundary = the largest parameter for which the probability is to be computed.
        All values larger than max_boundary will be lumped into the highest bin."""
        self.mean = mean
        self.bins = []
        for value in range(max_boundary + 1):
            self.bins.append(DiscreteBin(value))

        self.bins.append(RangeBin(min_value=max_boundary))
        self.generate_distribution()

    def __str__(self):
        poisson_info = 'PoissonDistribution: Mean: %.2f\n' % self.mean
        generic_info = super(self.__class__, self).__str__()
        return poisson_info + generic_info

    def retrieve_values(self):
        """Returns the list of bin values for the Poisson distribution."""
        return range(len(self.bins) - 1)

    def retrieve_count_by_value(self, value):
        """Returns the number of items in the histogram that have the designated value.
        
        Value must be an integer between 0 and max_boundary."""
        if value > len(self.bins) - 2:
            result = None
        else:
            result = self.bins[value].count
        return result

    def cumulative_probability(self, value):
        """Returns the probability that a random variable will have a value no greater than the one specified.
        
        value = integer (must be between 0 and the max_boundary of the distribution)."""
        return sum(map(lambda i: self.bins[i].count, range(value + 1)))


class StatisticalList(list):
    __doc__ = 'Numeric list class with statistical attributes.'

    def __init__(self, data=None):
        """Initializes a statistical list.
        
        data = list of inputs to list."""
        if data is not None:
            for i in range(len(data)):
                self.append(data[i])

    def compute_variance(self):
        """Computes the variance of a statistical list."""
        mean = self.mean
        return sum(map(lambda n: (n - mean) ** 2, self)) / (len(self) - 1)

    def compute_rms(self):
        """Computes the rms value of a statistical list."""
        return sqrt(avg(map(lambda n: n ** 2, self)))

    def compute_statistics(self, min_value=None, max_value=None, max_bins=None):
        """Computes statistics for a StatisticalList object; must contain at least one element.
        
        min_value = minimum value for cutoff of histogram (defaults to minimum in list).
        max_value = maximum value for cutoff of histogram (defaults to maximum in list).
        max_bins = maximum number of bins in histogram."""
        self.sort()
        num_elements = len(self)
        self.min = self[0]
        self.max = self[(-1)]
        self.mean = avg(self)
        self.median = self[(num_elements / 2)]
        self.variance = self.compute_variance()
        self.stdev = sqrt(self.variance)
        self.rms_value = self.compute_rms()
        self.percentiles = []
        for i in range(51):
            index = int(round((num_elements - 1) * (i / 50.0)))
            self.percentiles.append((i * 2, self[index]))

        num_bins = max(3, int(ceil(num_elements / 4.0)))
        if max_bins is not None:
            num_bins = min(num_bins, max_bins)
        bin_step = (self.max - self.min) / float(num_bins)
        min_bin_value = self.min + bin_step
        max_bin_value = self.max - bin_step
        if min_value is not None:
            min_bin_value = min_value
        if max_value is not None:
            max_bin_value = max_value
        bin_step = (max_bin_value - min_bin_value) / float(num_bins - 2)
        boundary_value = min_bin_value
        boundaries = []
        for i in range(num_bins - 1):
            boundaries.append(boundary_value)
            boundary_value = boundary_value + bin_step

        self.histogram = ContinuousHistogram(boundaries, highest_inclusive=False)
        for value in self:
            self.histogram.store_items(value)

    def __str__(self):
        """Prints data on a statistical list after statistics are generated."""
        return 'StatisticalList: %d elements, min = %.4f, max = %.4f, mean = %.4f, median = %.4f, variance = %.4f, stdev = %.4f, rms = %.4f' % (
         len(self), self.min, self.max, self.mean, self.median, self.variance, self.stdev, self.rms_value)


class Circle(object):
    __doc__ = 'Class to represent a circle.'

    def __init__(self, radius):
        """Initialize a circle with a specified radius."""
        self.radius = radius

    def __str__(self):
        """Inspector method for the circle."""
        return 'Circle: radius = %.2f' % self.radius

    def area(self):
        """Returns the area of the circle."""
        return pi * self.radius ** 2


class Rectangle(object):
    __doc__ = 'Class to represent a rectangle.'

    def __init__(self, length, width):
        """Initialize a rectangle with a specified length and width."""
        self.length = length
        self.width = width

    def __str__(self):
        """Inspector method for the rectangle."""
        return 'Rectangle: length = %.2f, width = %.2f' % (self.length, self.width)

    def area(self):
        """Returns the area of the rectangle."""
        return self.length * self.width

    def motion_tolerant_area(self, motion_length, motion_angle):
        """Returns the area within a rectangle that can tolerate a motion in a known direction
        while remaining within the rectangle. 
        
        length = distance of motion (same units as rectangle length and width).
        angle = angle in radians between the direction of motion and long direction of rectangle."""
        delta_x = motion_length * cos(motion_angle)
        delta_y = motion_length * sin(motion_angle)
        return (self.length - delta_x) * (self.width - delta_y)


class Square(Rectangle):
    __doc__ = 'Class to represent a square.'

    def __init__(self, side):
        self.side = side
        super(self.__class__, self).__init__(side, side)

    def __str__(self):
        """Inspector method for the square."""
        return 'Square: side = %.2f' % self.side

    def inner_area(self, excluded_width):
        """Returns the area of the square after removing a strip of specified width along each edge."""
        return Square(self.side - 2 * excluded_width).area()
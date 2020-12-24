# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\squeak\main.py
# Compiled at: 2015-05-11 12:28:50
import os, pandas as pd, numpy as np
from scipy import interpolate, interp, stats
from math import sqrt
import math, warnings

def even_time_steps(x, y, t, length=101):
    """Interpolates x/y coordinates and t to 101 even time steps, returns x and y TimeSeries
        
        Parameters
        ----------
        x, y : array-like
                Coordinates to be interpolated
        t : array-like
                Associated time stamps
        length : int, optional
                Number of time steps to interpolate to. Default 101
                
        Returns
        ---------
        TimeSeries(nx, nt) : Pandas.TimeSeries object
                x coordinates intepolated to 101 even time steps
        TimeSeries(ny, nt) : Pandas.TimeSeries object
                y coordinates intepolated to 101 even time steps
        """
    nt = np.arange(min(t), max(t), float(max(t) - min(t)) / length)
    nx = interp(nt, t, x)[:101]
    ny = interp(nt, t, y)[:101]
    return (pd.TimeSeries(nx, range(len(nx))), pd.TimeSeries(ny, range(len(ny))))


def normalize_space(array, start=0, end=1, preserve_direction=False):
    """Interpolates array of 1-d coordinates to given start and end value.
         
        Parameters
        ----------
        array : array-like
                array of coordinates to interpolate
        start : numeric
                Default: 0
                Value to interpolate first coordinate to
        end : numeric
                Default: 1
                Value to interpolate last coordinate to         
        preserve_direction : boolean
                Default: False
                If False, decrasing coordinates (i.e. where the
                last value is less than the first) will remain decreasing
                in the output. If start=0, and end=1, increasing coordinates will output [0, ..., 1],
                while decreasing coordinates will output [0, ..., -1].
                If False, all output will run [0, ..., 1].
        
        TODO: Might not work on decreasing arrays. Test this"""
    if type(array) != np.ndarray:
        if type(array) == list:
            array = np.array(array)
        else:
            raise TypeError("You've used an input of type %s.\nPlease input either a Numpy array or a list.\nThe value you used was:\n%s" % (type(array), repr(array)))
    reverse_when_done = False
    old_delta = array[(-1)] - array[0]
    if old_delta < 0:
        array = array * -1
        old_delta = array[(-1)] - array[0]
        if preserve_direction:
            reverse_when_done = True
    new_delta = end - start
    array = array.astype('float')
    if max(array) > array[(-1)] + 2 * old_delta or min(array) < array[0] - 2 * old_delta:
        raise ValueError("Input included values way outside of the range\t\tof your data, given the start and end coordinates.\n\t\tThis shouldn't happen.")
    old_range = np.array([array[0] - 2 * old_delta, array[(-1)] + 2 * old_delta])
    new_range = np.array([start - 2 * new_delta, end + 2 * new_delta])
    normal = np.interp(array, old_range, new_range)
    if reverse_when_done:
        return normal * -1
    else:
        return normal


def remap_right(array):
    """Flips decreasing coordinates horizontally on their origin
        
        >>> remap_right([10,11,12])
        array([10, 11, 12])

        >>> remap_right([10, 9, 8])
        array([10, 11, 12])
        
        Parameters
        ----------
        array : array-like
                array of coordinates to remap
        """
    array = np.array(array)
    if array[(-1)] - array[0] < 0:
        array_start = array[0]
        return (array - array_start) * -1 + array_start
    else:
        return array


def uniform_time(coordinates, timepoints, desired_interval=20, max_duration=3000):
    """Extend coordinates to desired duration by repeating the final value
        
        Parameters
        ----------
        coordinates : array-like
                1D x or y coordinates to extend
        timepoitns : array-like
                timestamps corresponding to each coordinate
        desired_interval : int, optional
                frequency of timepoints in output, in ms
                Default 10
        max_duration : int, optional
                Length to extend to.
                Note: Currently crashes if max(timepoints) > max_duration
                Default 3000
                
        Returns
        ---------
        uniform_time_coordinates : coordinates extended up to max_duration"""
    regular_timepoints = np.arange(0, timepoints[(-1)] + 0.1, desired_interval)
    regular_coordinates = interp(regular_timepoints, timepoints, coordinates)
    required_length = int(max_duration / desired_interval)
    extra_values = np.array([regular_coordinates[(-1)]] * (required_length - len(regular_coordinates) + 1))
    extended_coordinates = np.concatenate([regular_coordinates, extra_values])
    extended_timepoints = np.arange(0, max_duration + 0.1, desired_interval)
    return pd.TimeSeries(extended_coordinates, extended_timepoints)


def list_from_string(string_list):
    """Parses string represation of list '[1,2,3]' to an actual pythonic list [1,2,3]
        
        A rough and ready function"""
    try:
        first = string_list.strip('[]')
        then = np.array(first.split(','))
        lastly = then.astype(float)
        return lastly
    except:
        warnings.warn('There was an error parsing one of your strings to a list.\n\t\t`None` value used instead', UserWarning)
        return

    return


def distance_from_response(x, y, from_foil=False):
    """Calculate distance from the ultimate response for each step of a trajectory.
        If `from_foil` is True, shows distance from the foil response,
        assuming the foil is located on the opposite side of the x axis to the
        response.
        
        Parameters
        x, y: array-like
                Coordinates of trajectory
        from_foil: boolean, optional, default False
                If `True`, return distance to the non-chosen response.
        """
    response_x, response_y = x[(-1)], y[(-1)]
    if from_foil:
        response_x *= -1
    distance = np.sqrt((x - response_x) ** 2 + (y - response_y) ** 2)
    return distance


def get_init_time(t, y, y_threshold=0.01, ascending=True):
    """Returns time  from t of point where y exceeds y_threshold.
         TODO - Replace this with faster code using generators
        init_time = next(time for (time, location) in zip(tList, yList) if location < (h-30)) # More than 30 pixels from bottom

        
        Parameters
        ----------
        y, t : array-like
                y coordinates, and associated timestamps
        y_threshold : int, optional
                Value beyond which y is said to be in motion
                Default is .01
        ascending : bool, optional
                If True (default) return first value where y > threshold.
                Otherwise, return first where y < threshold (y decreases).
        
        Returns
        -------
        init_time : Timestamp of first y value to exceed y_threshold.
        """
    init_step = get_init_step(y, y_threshold, ascending)
    return t[init_step]


def get_init_step(y, y_threshold=0.01, ascending=True):
    """Return index of point where y exceeds y_threshold
        
        Parameters
        ----------
        y : array-like
        y_threshold : int, optional
                Value beyond which y is said to be in motion
                Default is .01
        ascending : bool, optional
                If True (default) return first value where y > threshold.
                Otherwise, return first where y < threshold (y decreases).
        
        Returns
        -------
        step: index of y which first exceeds y_threshold
        """
    if ascending:
        started = np.array(y) > y_threshold
    else:
        started = np.array(y) < y_threshold
    step = np.argmax(started)
    return step


def rotate(x, y, rad):
    """Rotate counter-clockwise around origin by `rad` radians.
        """
    s, c = [ f(rad) for f in (math.sin, math.cos) ]
    x, y = c * x - s * y, s * x + c * y
    return (x, y)


def get_deviation(x, y):
    """Returns the deviation away from a straight line over the course of a path.
        Calculated by rotating the trajectory so that it starts at (0, 0),
        and ends at (0, 1), so that the x-axis coordinates represent the deviation
        
        Parameters
        ----------
        x, y : array-like
                x and y coordinates of the path.
                
        Returns
        ----------
        deviation : np.array
                Distance between observed and straight line at every step
        
        
        """
    path = np.array(zip(x, y)).T
    radians_to_rotate = math.atan(float(x[(len(x) - 1)]) / y[(len(y) - 1)])
    rotMatrix = np.array([[np.cos(radians_to_rotate), -np.sin(radians_to_rotate)],
     [
      np.sin(radians_to_rotate), np.cos(radians_to_rotate)]])
    deviation, deviation_y = rotMatrix.dot(path)
    return -1 * deviation


def max_deviation(x, y, allow_negative=True):
    """Caluclate furthest distance between observed path and ideal straight one.
        
        Parameters
        ----------
        x, y : array-like
                x and y coordinates of the path.
        allow_negative : boolean, optional, default True
                If False, ignore deviation AWAY from foil response.
                
        Returns
        ----------
        max_dev : Greatest distance between observed and straight line.
        
        As with the rest of Squeak, this assumes a line running from bottom center
        (0, 0) to top right (1, 1), or (1, 1.5), as it relies on rotating the
        line 45 degrees anticlockwise and comparing it to the y axis.
        
        Will return negative values in cases where the greatest distance
        is to the right (i.e. AWAY from the alternative response).
        """
    deviation = get_deviation(x, y)
    max_positive = abs(max(deviation))
    max_negative = abs(min(deviation))
    if allow_negative:
        if max_positive > max_negative:
            return max_positive
        else:
            return -1 * max_negative

    else:
        return max_positive


def auc(x, y, method='polygon'):
    """Calculates area between observed path and idea straight line.
        
        An alternative to max_deviation
        
        Parameters
        ----------
        x, y : array-like
                x and y coordinates of the path.
        method : string, optional, default 'polygon'
                Method used to calculate area under curve.
                Options are:
                        - 'polygon' - Using formula for area of irregular polygon,
                        - 'even-odd' - Slower, using the even-odd rule on each pixel
                                        to see if if falls within the curve
                                        
        Returns
        ----------
        area : Total area enclosed by the curve and line together
        """
    if method == 'polygon':
        return polygon_auc(x, y)
    if method == 'even-odd':
        return even_odd_auc(x, y)
    raise ValueError("AUC method must be either 'polygon' or 'even-odd'.\n\t\tYou entered '%s'" % method)


def polygon_auc(x, y):
    areas = []
    j = len(x) - 1
    for i in range(len(x)):
        x1y2 = y[i] * x[j]
        x2y1 = x[i] * y[j]
        area = x2y1 - x1y2
        areas.append(area)
        j = i

    return float(sum(areas)) / 2


def even_odd_auc(x, y, resolution=0.05, debug=False):
    x, y = np.array(x), np.array(y)
    start_x, end_x, start_y, end_y = (x[0], x[(-1)], y[0], y[(-1)])
    if debug:
        plt.plot(x, y, '-ob')
        points_under_curve = []
        for px in np.arange(-end_x * 1.51, end_x * 1.51, resolution):
            for py in np.arange(start_y - 0.2, end_y + 0.3, resolution):
                test = even_odd_rule(px, py, x, y)
                if test:
                    plt.plot(px, py, 'or')
                points_under_curve.append(test)

    else:
        points_under_curve = [ even_odd_rule(px, py, x, y) for px in np.arange(-end_x * 1.51, end_x * 1.51, resolution) for py in np.arange(start_y - 0.2, end_y + 0.3, resolution)
                             ]
    auc = float(sum(points_under_curve)) / len(points_under_curve)
    return auc


def even_odd_rule(point_x, point_y, line_x, line_y, resample=5):
    line_x, line_y = line_x[::resample], line_y[::resample]
    line_x = np.append(line_x, [line_x[(-1)], line_x[0]])
    line_y = np.append(line_y, [line_y[0]] * 2)
    poly = zip(line_x, line_y)
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if (poly[i][1] > point_y) != (poly[j][1] > point_y) and point_x < (poly[j][0] - poly[i][0]) * (point_y - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0]:
            c = not c
        j = i

    return c


def pythag(o, a):
    return np.sqrt(o ** 2 + a ** 2)


def velocity(x, y):
    """Returns array of velocity at each time step"""
    if isinstance(x, pd.Series):
        x = x.values
        y = y.values
    vx = np.ediff1d(x)
    vy = np.ediff1d(y)
    vel = np.sqrt(vx ** 2 + vy ** 2)
    return vel


def bimodality_coef(samp):
    """Checks sample for bimodality (values > .555)
        
        See `Freeman, J.B. & Dale, R. (2013). Assessing bimodality to detect 
        the presence of a dual cognitive process. Behavior Research Methods.` 
        """
    n = len(samp)
    m3 = stats.skew(samp)
    m4 = stats.kurtosis(samp, fisher=True)
    b = (m3 ** 2 + 1) / (m4 + 3 * ((n - 1) ** 2 / ((n - 2) * (n - 3))))
    return b


def angular_deviation(x, y, t=None, response_x=1, response_y=1, alt_x=-1, alt_y=1, normalized=False):
    """
        Shows how far, in degrees, the path deviated from going straight to the response,
        at every step along the way.
        
        Parameters
        ----------
        x, y : Pandas Series objects (including TimeSeries)
                The mouse coordinates
        response_x, response_y, alt_x, alt_y : int
                The locations of the responses
        normalized : Bool
                Not implemented: Normalize the result, so that straight towards
                the response returns 0, and straight towards the alternative
                returns 1.
        """
    dx, dy = x.diff(), y.diff()
    response_dx = response_x - x
    response_dy = response_y - y
    alt_dx = alt_x - x
    alt_dy = alt_y - y
    actual_angle = np.arctan2(dy, dx)
    angle_to_response = np.arctan2(response_dy, response_dx)
    angle_to_alt = np.arctan2(alt_dy, alt_dx)
    velocity = np.sqrt(dx ** 2 + dy ** 2)
    actual_angle *= velocity > 0.05
    angle_to_alt *= velocity > 0.05
    angle_to_response *= velocity > 0.05
    deviation_angle = actual_angle - angle_to_response
    if t == None:
        t = range(len(dx))
    if normalized:
        raise Exception("normalization isn't implemented yet for angular_deviation")
        normal = (deviation_angle - angle_to_response) / (angle_to_alt - angle_to_response)
        return normal
    else:
        return deviation_angle
        return


def movement_angle(x, y, step_by=5):
    original_index = x.index
    x, y = (x[::step_by], y[::step_by])
    try:
        dx, dy = (x.diff(), y.diff())
    except AttributeError:
        dx, dy = (
         np.ediff1d(x), np.ediff1d(y))

    angle = np.arctan2(dx, dy)
    velocity = np.sqrt(dx ** 2 + dy ** 2)
    angle *= velocity > 0.05
    angle = np.nan_to_num(angle)
    return angle.reindex(index=original_index).interpolate()
    print end_x, end_y,
    print


def smooth_gaussian(array, degree=5):
    """
        Smoothes jagged, oversampled time series data.
        
        Parameters
        ----------
        array : 
                TimeSeries to smooth
        degree : int, optional, default=5
                window over which to smooth
                
        Code from http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/
        With thanks to  Scott W Harden
        """
    window = degree * 2 - 1
    weight = np.array([1.0] * window)
    weightGauss = []
    for i in range(window):
        i = i - degree + 1
        frac = i / float(window)
        gauss = 1 / np.exp((4 * frac) ** 2)
        weightGauss.append(gauss)

    weight = np.array(weightGauss) * weight
    smoothed = [0.0] * (len(array) - window)
    for i in range(len(smoothed)):
        smoothed[i] = sum(np.array(array[i:i + window]) * weight) / sum(weight)

    return smoothed


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.
        
        http://wiki.scipy.org/Cookbook/SignalSmooth
   """
    if x.ndim != 1:
        raise ValueError, 'smooth only accepts 1 dimension arrays.'
    if x.size < window_len:
        raise ValueError, 'Input vector needs to be bigger than window size.'
    if window_len < 3:
        return x
    if window not in ('flat', 'hanning', 'hamming', 'bartlett', 'blackman'):
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    s = np.r_[(x[window_len - 1:0:-1], x, x[-1:-window_len:-1])]
    if window == 'flat':
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')
    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def smooth_timeseries(series, window_len=11, window='hanning'):
    original_index = series.index
    smoothed = smooth(series, window_len, window)
    interpolated = np.interp(np.linspace(0, len(smoothed), len(original_index)), range(len(smoothed)), smoothed)
    return pd.TimeSeries(interpolated, original_index)


def jitter(array, scale=0.1):
    return array + np.random.normal(scale=scale * np.std(array), size=len(array))


def acceleration_components(velocity):
    if isinstance(velocity, pd.Series):
        velocity = velocity.values
    acc = np.ediff1d(velocity)
    c = acc[:-1] * acc[1:]
    components = c < -1e-06
    return np.array(components)


def x_flips(x):
    if isinstance(x, pd.Series):
        x = x.values
    dx = np.ediff1d(x)
    changes = dx[:-1] * dx[1:]
    flips = changes < -1e-05
    return np.array(flips)


def count_x_flips(x):
    return sum(x_flips(x))


def sample_entropy(ts, edim=2, tau=1):
    """
        ts - a time series.
        edim - the embedding dimension, as for chaotic time series; a preferred value is 2.
        r - filter factor; work on heart rate variability has suggested setting r to be 0.2
            times the standard deviation of the data.
        elag - embedding lag; defaults to 1, more appropriately it
            should be set to the smallest lag at which the autocorrelation
            function of the time series is close to zero. (At the moment
            it cannot be changed by the user.)
        tau - delay time for subsampling, similar to elag.
        """
    r = 0.2 * np.std(ts, ddof=1)
    N = len(ts)
    correl = []
    datamat = np.zeros((edim + 1, N - edim))
    for i in range(1, edim + 1 + 1):
        datamat[i - 1] = ts[i - 1:N - edim + i - 1]

    for m in [edim, edim + 1]:
        count = np.zeros((1, N - edim))
        tempmat = datamat[:m,]
        for i in range(1, N - m):
            a = tempmat[..., i:N - edim]
            b = np.transpose([tempmat[(..., i - 1)]] * (N - edim - i))
            X = np.abs(a - b)
            dst = np.max(X, axis=0)
            d = dst < r
            count[(..., i)] = float(sum(d)) / (N - edim)

        correl.append(np.sum(count) / (N - edim))

    return np.log(correl[0] / correl[1])


def ballistic_direction(x):
    dx = x.diff()
    side_of_screen = np.sign(x)
    direction = np.sign(dx)
    direction.iloc[0] = 0
    sizable = dx.abs() > 0.01
    direction *= sizable
    for i in range(1, len(direction)):
        if direction.iloc[i] == 0 and direction.iloc[(i - 1)] != 0:
            direction.iloc[i] = side_of_screen[(i - 1)]

    return direction
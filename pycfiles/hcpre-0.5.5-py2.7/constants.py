# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hcpre/duke_siemens/constants.py
# Compiled at: 2014-05-12 17:01:30
"""A home for constants."""
from __future__ import division
from collections import OrderedDict as ordered_dict
DEGREES_TO_RADIANS = 0.017453292519943295
RADIANS_TO_DEGREES = 57.29577951308232

class PaneNames(object):
    """ A container that allows me to represent wxWidgets pane names (which
    are strings) in a way that Python will complain loudly about if I mistype
    one of them (e.g. psuedo instead of pseudo). A pane's name is its unique
    handle. They are not exposed to the user and they are not magic. (i.e.
    the name "baseline" could just as well be "shrubbery".)
    """
    BASELINE = 'baseline'
    XYZ_BROWSER = 'xyz_browser'
    SUM_SPECTRA = 'sum_spectra'
    TIME_SERIES = 'time_series'
    KORNAK = 'kornak'
    LORENTZ_GAUSS = 'lorentz_gauss'
    PSEUDO_2D = 'pseudo_2d'
    HEADER = 'header'
    SPECTRAL = 'spectral'
    SPATIAL = 'spatial'
    FILEBAR = 'filebar'
    SVD = 'svd'
    FITTING = 'fitting'
    PROCESSING = 'processing'
    TOOLS = (
     FILEBAR, SPATIAL, BASELINE, XYZ_BROWSER, SUM_SPECTRA,
     TIME_SERIES, KORNAK, LORENTZ_GAUSS, PSEUDO_2D)


class AmplitudeMultiplier(object):
    """ Amplitude multiplier constants """
    MIN = 0
    MAX = 1000000000000.0


class Apodization(object):
    """ Apodization constants """
    MIN_WIDTH = 0
    MAX_WIDTH = 100
    NONE = 0
    GAUSSIAN = 1
    LORENTZIAN = 2
    choices = ordered_dict(((NONE, 'None'),
     (
      GAUSSIAN, 'Gaussian'),
     (
      LORENTZIAN, 'Lorentzian')))


class AreaFrom(object):
    """ Contains constants for area calculation options. """
    PLOT_1 = 1
    PLOT_2 = 2
    PLOT_3 = 3


class BaselineFilterMethod(object):
    """ Baseline Filter Method """
    NONE = 0
    LOWESS = 1
    BSPLINE = 2
    choices = ordered_dict(((NONE, 'None'),
     (
      LOWESS, 'Lowess'),
     (
      BSPLINE, 'B-Spline')))


class BaselineFilterRange(object):
    """ Baseline Filter Range """
    WHOLE_SPECTRUM = 0
    BETWEEN_CURSORS = 1
    choices = ordered_dict(((WHOLE_SPECTRUM, 'Whole Spectrum'),
     (
      BETWEEN_CURSORS, 'Between Cursors')))


class DcOffset(object):
    """ DC offset constants """
    MIN = -100000.0
    MAX = 100000.0


class EddyCurrentCorrection(object):
    """ Eddy current correction constants """
    NONE = 0
    SIMPLE = 1
    MIN_NOISE_FILTER = 0.1
    MAX_NOISE_FILTER = 100.0
    choices = ordered_dict(((NONE, 'Off'),
     (
      SIMPLE, 'Simple')))


class FittingLineshapeModel(object):
    """ Lineshape model """
    VOIGT = 0
    LORENTZ = 1
    GAUSS = 2
    choices = ordered_dict(((VOIGT, 'Voigt'),
     (
      LORENTZ, 'Lorentz'),
     (
      GAUSS, 'Gauss')))


class FittingBaselineAlgorithm(object):
    """ Baseline Algorithm """
    NONE = 0
    VARIABLE_KNOT_SPLINE = 1
    FIXED_KNOT_SPLINE = 2
    WAVELET_FILTER = 3
    choices = ordered_dict(((NONE, 'None'),
     (
      VARIABLE_KNOT_SPLINE, 'Variable Knot Spline'),
     (
      FIXED_KNOT_SPLINE, 'Fixed Knot Spline'),
     (
      WAVELET_FILTER, 'Wavelet Filter')))


class FittingMacromoleculePeak(object):
    """ Macromolecular Peak Method """
    GROUPED_PEAKS = 0
    INDIVIDUAL_PEAKS = 1
    choices = ordered_dict(((GROUPED_PEAKS, 'Grouped Peaks'),
     (
      INDIVIDUAL_PEAKS, 'Individual Peaks')))


class FittingMacromoleculeLinewidths(object):
    """ Macromolecular Linewidths Method """
    LUMPED = 0
    INDEPENDENT = 1
    choices = ordered_dict(((LUMPED, 'Lumped'),
     (
      INDEPENDENT, 'Independent')))


class FittingOptimizeAlgorithm(object):
    """ Optimization Algorithm """
    NONE = 0
    CONSTRAINED_LEVENBERG_MARQUARDT = 1
    choices = ordered_dict(((NONE, 'None'),
     (
      CONSTRAINED_LEVENBERG_MARQUARDT, 'ccfit')))


class FittingOptimizeWeights(object):
    """ Macromolecular Linewidths Method """
    EVEN_WEIGHTING = 0
    LOCAL_WEIGHTING = 1
    choices = ordered_dict(((EVEN_WEIGHTING, 'Even Weighting'),
     (
      LOCAL_WEIGHTING, 'Local Weighting')))


class FittingAmplitudeMultiplier(object):
    """ Metabolites amplitude multiplier constants """
    MIN = 0.001
    MAX = 1000.0


class FittingBaselineBsplineOrder(object):
    """ Baseline B-Spline order constants """
    MIN = 1.0
    MAX = 5.0


class FittingBaselineLowessWindowSize(object):
    """ Baseline metabolites region Lowess window size (Hz) constants """
    MIN = 1e-05
    MAX = 5000.0


class FittingBaselineUnderestimation(object):
    """ Baseline first pass underestimation constants """
    MIN = -50.0
    MAX = 100.0


class FittingLineWidth(object):
    """ Metabolites line width constants """
    MIN = 0.001
    MAX = 1000.0


class FittingMacroMoleculeLines(object):
    """ Metabolites Lorentz-Gauss macro molecule model lines constants """
    MIN = 1
    MAX = 50


class FittingMacroMoleculeAdjustment(object):
    """ Metabolites Lorentz-Gauss macro molecule adjustment (spinner) constants """
    MIN = 0
    MAX = 100


class FittingOptimizationAmplitude(object):
    """ Fitting Lorentz-Gauss optimization metabolite amplitude constants """
    MIN = 1
    MAX = 10000


class FittingOptimizationAreaWeight(object):
    """ Fitting Lorentz-Gauss optimization area weight constants """
    MIN = 0.0001
    MAX = 1000000.0


class FittingOptimizationAlgorithmIterations(object):
    """ Fitting Lorentz-Gauss optimization algorithm max iterations constants """
    MIN = 1
    MAX = 10000


class FittingOptimizationConfidenceAlpha(object):
    """ Fitting Lorentz-Gauss optimization algorithm confidence alpha constants """
    MIN = 0.05
    MAX = 0.9999


class FittingOptimizationFrequency(object):
    """ Fitting Lorentz-Gauss optimization metabolite frequency constants """
    MIN = 1
    MAX = 10000


class FittingOptimizationGlobalIterations(object):
    """ Fitting Lorentz-Gauss optimization global iterations constants """
    MIN = 1
    MAX = 1000


class FittingOptimizationLocalMultiplier(object):
    """ Fitting Lorentz-Gauss optimization "LW Local Mult" (???) constants """
    MIN = 1.0
    MAX = 100.0


class FittingOptimizationPhase1(object):
    """ Fitting Lorentz-Gauss optimization metabolite phase 1 constants """
    MIN = 1
    MAX = 5000


class FittingOptimizationStopTolerance(object):
    """ Fitting Lorentz-Gauss optimization algorithm stop tolerance constants """
    MIN = 1e-09
    MAX = 100000.0


class FittingOptimizationTaTb(object):
    """ Fitting Lorentz-Gauss optimization Ta=Tb constants """
    MIN = 0.001
    MAX = 200.0


class FittingPeakPpm(object):
    """ Metabolites peak PPM constants """
    MIN = -5000.0
    MAX = 5000.0


class FittingPeakSearchRange(object):
    """ Metabolites peak search range constants """
    MIN = 0.001
    MAX = 10.0


class FrequencyShift(object):
    """ Frequency shift constants """
    MIN = -10000.0
    MAX = 10000.0


class Phase_1(object):
    """ First order phase constants """
    MIN = -10000.0
    MAX = 10000.0
    MIN_PIVOT = -1000
    MAX_PIVOT = 1000


class Plot3Function(object):
    """ Contains constants for plot 3 function options. """
    NONE = 0
    RESIDUAL_1_MINUS_2 = 1
    RESIDUAL_2_MINUS_1 = 2
    TIME_SERIES_SUM_1 = 3
    TIME_SERIES_SUM_2 = 4


class SpatialFilter(object):
    """ Spatial filter constants """
    NONE = 0
    HAMMING = 1
    EXPONENTIAL = 2
    GAUSSIAN = 3
    choices = ordered_dict(((NONE, 'None'),
     (
      HAMMING, 'Hamming'),
     (
      EXPONENTIAL, 'Exponential'),
     (
      GAUSSIAN, 'Gaussian')))


class SpatialTranspose(object):
    """ Spatial transposition constants """
    NONE = 0
    TRANSPOSE_XY = 1
    TRANSPOSE_XZ = 2
    TRANSPOSE_YZ = 3
    TRANSPOSE_XYZ = 4
    choices = ordered_dict(((NONE, 'None'),
     (
      TRANSPOSE_XY, 'Transpose_XY'),
     (
      TRANSPOSE_XZ, 'Transpose_XZ'),
     (
      TRANSPOSE_YZ, 'Transpose_YZ'),
     (
      TRANSPOSE_XYZ, 'Transpose_XYZ')))


class WaterExtrapolation(object):
    """ Water extrapolation constants """
    NONE = 0
    LINEAR = 1
    AR_MODEL = 2
    MIN_POINTS = 1
    MAX_POINTS = 1000
    choices = ordered_dict(((NONE, 'None'),
     (
      LINEAR, 'Linear'),
     (
      AR_MODEL, 'AR Model')))


class WaterFilter(object):
    """ Water filter constants """
    NONE = 0
    HAMMING = 1
    FIR = 2
    HLSVD = 3
    choices = ordered_dict(((NONE, 'None'),
     (
      HAMMING, 'Hamming'),
     (
      FIR, 'FIR'),
     (
      HLSVD, 'HLSVD')))
    MIN_FIR_RIPPLE = 0
    MAX_FIR_RIPPLE = 500
    MIN_FIR_HALF_WIDTH = 0
    MAX_FIR_HALF_WIDTH = 500
    MIN_HLSVD_DATA_POINTS = 1
    MAX_HLSVD_DATA_POINTS = 2048
    MIN_HLSVD_SINGULAR_VALUES = 1
    MAX_HLSVD_SINGULAR_VALUES = 50
    MIN_HLSVD_MATRIX_POINTS = 1
    MAX_HLSVD_MATRIX_POINTS = 1024
    MIN_HLSVD_ITERATIONS = 1
    MAX_HLSVD_ITERATIONS = 2000


class XYZImageType(object):
    """ XYZ Image Type constants """
    MAGNITUDE = 0
    REAL = 1
    IMAGINARY = 2
    MAGNITUDE_PLUS_MASK = 3
    B0_MAP = 4
    choices = ordered_dict(((MAGNITUDE, 'Magnitude'),
     (
      REAL, 'Real'),
     (
      IMAGINARY, 'Imaginary'),
     (
      MAGNITUDE_PLUS_MASK, 'Magnitude plus Mask'),
     (
      B0_MAP, 'B0 Map')))


class XYZOrientation(object):
    """ XYZ Orientation constants """
    XY_ORIENTATION = 0
    YZ_ORIENTATION = 1
    XZ_ORIENTATION = 2
    choices = ordered_dict(((XY_ORIENTATION, 'XY_Orientation'),
     (
      YZ_ORIENTATION, 'YZ_Orientation'),
     (
      XZ_ORIENTATION, 'XZ_Orientation')))


class ZeroFillMultiplier(object):
    """ Zero fill multiplier constants. The zero fill is not only limited
    to a specific range, but it must also be an integral power of 2.
    """
    _EXPONENT = 5
    MIN = 1
    MAX = 2 ** _EXPONENT
    choices = [ (2 ** i, str(2 ** i)) for i in range(0, _EXPONENT + 1) ]
    choices = ordered_dict(choices)
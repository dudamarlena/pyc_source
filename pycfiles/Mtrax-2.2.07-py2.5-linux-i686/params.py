# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/params.py
# Compiled at: 2008-08-09 08:49:07
from version import DEBUG, __version__
import numpy as num, copy
try:
    raise ImportError
except ImportError:
    from about import AboutDialogInfo

class ShapeParams():

    def __init__(self, major=0, minor=0, area=0, ecc=0):
        self.major = major
        self.minor = minor
        self.area = area
        self.ecc = ecc

    def copy(self):
        return ShapeParams(self.major, self.minor, self.area, self.ecc)

    def __print__(self):
        return 'major = %.2f, minor = %.2f, area = %.2f, ecc = %.2f' % (self.major, self.minor, self.area, self.ecc)

    def __repr__(self):
        return self.__print__()

    def __str__(self):
        return self.__print__()

    def __eq__(self, other):
        for (i, j) in self.__dict__.iteritems():
            if not hasattr(other, i):
                return False
            if not j == other.__dict__[i]:
                return False

        for (i, j) in other.__dict__.iteritems():
            if not hasattr(self, i):
                return False
            if not j == self.__dict__[i]:
                return False

        return True


def averageshape(shape1, shape2):
    shape3 = ShapeParams()
    shape3.major = (shape1.major + shape2.major) / 2.0
    shape3.minor = (shape1.minor + shape2.minor) / 2.0
    shape3.area = (shape1.area + shape2.area) / 2.0
    shape3.ecc = (shape1.ecc + shape2.ecc) / 2.0
    return shape3


class Grid():

    def __init__(self):
        self.X = None
        self.Y = None
        self.X2 = None
        self.Y2 = None
        self.XY = None
        return

    def setsize(self, sz):
        (self.Y, self.X) = num.mgrid[0:sz[0], 0:sz[1]]
        self.Y2 = self.Y ** 2
        self.X2 = self.X ** 2
        self.XY = self.X * self.Y

    def __eq__(self, other):
        return True


class Parameters():

    def __init__(self):
        self.DOBREAK = False
        self.last_time = 0
        self.DEFAULT_FRAME_RATE = 25.0
        self.GRID = Grid()
        self.max_n_points_ratio = 1.0 / 250.0
        self.max_n_clusters = 100
        self.empty_val = -1
        self.dummy_val = -2
        self.zoom_window_pix = 20
        self.id_spinner_width = 40
        self.normal_palette = [
         [
          255, 0, 0],
         [
          0, 255, 0],
         [
          0, 0, 255],
         [
          255, 0, 255],
         [
          255, 255, 0],
         [
          0, 255, 255],
         [
          255, 127, 127],
         [
          127, 255, 127],
         [
          127, 127, 255],
         [
          255, 127, 255],
         [
          255, 255, 127],
         [
          127, 255, 255]]
        self.colorblind_palette = [
         [
          230, 159, 0],
         [
          86, 180, 233],
         [
          0, 158, 115],
         [
          240, 228, 66],
         [
          0, 114, 178],
         [
          213, 94, 0],
         [
          204, 121, 167]]
        self.SHOW_BACKGROUND = 0
        self.SHOW_DISTANCE = 1
        self.SHOW_THRESH = 2
        self.SHOW_NONFORE = 3
        self.SHOW_DEV = 4
        self.SHOW_CC = 5
        self.SHOW_ELLIPSES = 6
        self.BG_TYPE_LIGHTONDARK = 0
        self.BG_TYPE_DARKONLIGHT = 1
        self.BG_TYPE_OTHER = 2
        self.BG_NORM_STD = 0
        self.BG_NORM_INTENSITY = 1
        self.BG_NORM_HOMOMORPHIC = 2
        self.ALGORITHM_MEDIAN = 0
        self.ALGORITHM_MEAN = 1
        self.print_crap = False
        self.watch_threads = True
        self.watch_locks = False
        self.count_time = True
        if not DEBUG:
            self.print_crap = False
            self.watch_threads = False
            self.watch_locks = False
            self.count_time = False
        self.status_green = '#66FF66'
        self.status_blue = '#AAAAFF'
        self.status_red = '#FF6666'
        self.status_yellow = '#FFFF66'
        self.wxvt_bg = '#DDFFDD'
        self.MAXDSHOWINFO = 10
        self.DRAW_MOTION_SCALE = 10.0
        self.start_frame = 0
        self.nids = 0
        self.interactive = True
        self.version = 0
        self.min_ntargets = 0
        self.max_ntargets = 100
        self.n_frames = 0
        self.movie_size = (0, 0)
        self.npixels = 0
        self.movie = None
        self.movie_name = ''
        self.annotation_movie_name = ''
        self.n_bg_frames = 100
        self.use_median = True
        self.bg_firstframe = 0
        self.bg_lastframe = 99999
        self.bg_type = self.BG_TYPE_LIGHTONDARK
        self.bg_norm_type = self.BG_NORM_STD
        self.hm_cutoff = 0.35
        self.hm_boost = 2
        self.hm_order = 2
        self.n_bg_std_thresh = 20.0
        self.n_bg_std_thresh_low = 10.0
        self.bg_std_min = 1.0
        self.bg_std_max = 10.0
        self.min_nonarena = 256.0
        self.max_nonarena = -1.0
        self.arena_center_x = None
        self.arena_center_y = None
        self.arena_radius = None
        self.arena_edgethresh = None
        self.do_set_circular_arena = True
        self.batch_autodetect_arena = True
        self.batch_autodetect_shape = True
        self.batch_autodetect_bg_model = True
        self.maxshape = ShapeParams(10000, 10000, 10000, 1.0)
        self.minshape = ShapeParams(1.0, 1.0, 1.0, 0.0)
        self.meanshape = ShapeParams(2.64, 3.56, 40.25, 1.98)
        self.have_computed_shape = False
        self.minbackthresh = 1.0
        self.maxpenaltymerge = 40
        self.maxareadelete = 5
        self.n_frames_size = 50
        self.n_std_thresh = 3.0
        self.ang_dist_wt = 100.0
        self.max_jump = 100.0
        self.dampen = 0.0
        self.angle_dampen = 0.5
        self.velocity_angle_weight = 0.05
        self.max_velocity_angle_weight = 0.25
        self.do_fix_split = True
        self.do_fix_merged = True
        self.do_fix_spurious = True
        self.do_fix_lost = True
        self.lostdetection_length = 50
        self.lostdetection_distance = 100.0
        self.spuriousdetection_length = 50
        self.mergeddetection_distance = 20.0
        self.mergeddetection_length = 50
        self.splitdetection_cost = 40.0
        self.splitdetection_length = 50
        self.ellipse_thickness = 2
        self.use_colorblind_palette = False
        self.colors = self.normal_palette
        self.sliderres = 255.0
        self.tail_length = 10
        self.status_box = 0
        self.file_box = 1
        self.file_box_max_width = 40
        self.request_refresh = False
        self.do_refresh = True
        self.framesbetweenrefresh = 1
        self.bg_est_threads = 1
        self.max_median_frames = 100
        self.max_n_obj = 500
        return

    def __print__(self):
        s = ''
        for (i, j) in self.__dict__.iteritems():
            if j is None:
                s += i + ': None\n'
            else:
                s += i + ': ' + str(j) + '\n'

        return s

    def __repr__(self):
        return self.__print__()

    def __str__(self):
        return self.__print__()

    def copy(self):
        v = Parameters()
        for (i, j) in self.__dict__.iteritems():
            try:
                v.__dict__[i] = copy.deepcopy(j)
            except:
                v.__dict__[i] = j

        return v

    def __eq__(self, other):
        for (i, j) in self.__dict__.iteritems():
            if not hasattr(other, i):
                return False
            if not j == other.__dict__[i]:
                return False

        for (i, j) in other.__dict__.iteritems():
            if not hasattr(self, i):
                return False
            if not j == self.__dict__[i]:
                return False

        return True


params = Parameters()

class GUIConstants():

    def __init__(self):
        self.info = AboutDialogInfo()
        self.info.SetName('Mtrax')
        self.info.SetVersion(__version__)
        self.info.SetCopyright('2007, Caltech ethomics project')
        self.info.SetDescription('Multiple fly tracker.\n\nhttp://www.dickinson.caltech.edu/Research/Mtrax\n\nDistributed under the GNU General Public License\n(http://www.gnu.org/licenses/gpl.html) with\nABSOLUTELY NO WARRANTY.\n\nThis project is supported by grant R01 DA022777-01 from\nthe National Institute on Drug Abuse at the US NIH.')
        self.TRACK_START = 'Start Tracking'
        self.TRACK_STOP = 'Stop Tracking'
        self.TRACK_PLAY = 'Start Playback'
        self.TRACK_PAUSE = 'Stop Playback'
        params.version = __version__


const = GUIConstants()
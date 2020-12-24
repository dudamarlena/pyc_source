# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/ellipsesk.py
# Compiled at: 2008-08-05 03:42:32
USEGL = False
import numpy as num, time
from warnings import warn
import wx
from wx import xrc
from params import params
import imagesk, matchidentities as m_id
if USEGL:
    import motmot.wxglvideo.simple_overlay as wxvideo
else:
    import motmot.wxvideo.wxvideo as wxvideo
import scipy.ndimage as meas
from version import DEBUG
import pkg_resources
ZOOM_RSRC_FILE = pkg_resources.resource_filename(__name__, 'ellipses_zoom.xrc')
SETTINGS_RSRC_FILE = pkg_resources.resource_filename(__name__, 'ellipses_settings.xrc')

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == params.empty_val:
            if self.x == params.empty_val and self.y == params.empty_val:
                return True
            else:
                return False
        elif type(other) != type(self):
            raise TypeError('must compare points to points')
        elif self.x == other.x and self.y == other.y:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __print__(self):
        return '(%.1f, %.1f)' % (self.x, self.y)

    def __repr__(self):
        return self.__print__()

    def __str__(self):
        return self.__print__()


class Size:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __eq__(self, other):
        if other == params.empty_val:
            if self.width == params.empty_val and self.height == params.empty_val:
                return True
            else:
                return False
        elif type(other) != type(self):
            raise TypeError('must compare sizes to sizes')
        elif self.width == other.width and self.height == other.height:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __print__(self):
        return '(%.1f, %.1f)' % (self.width, self.height)

    def __repr__(self):
        return self.__print__()

    def __str__(self):
        return self.__print__()


class Ellipse:

    def __init__(self, centerX=params.empty_val, centerY=params.empty_val, sizeW=params.empty_val, sizeH=params.empty_val, angle=params.empty_val, area=params.empty_val, identity=-1):
        self.center = Point(centerX, centerY)
        self.size = Size(sizeW, sizeH)
        self.angle = angle
        self.area = area
        self.identity = identity

    def make_dummy(self):
        """A dummy ellipse has its area (only) set to params.dummy_val ."""
        self.area = params.dummy_val

    def __eq__(self, other):
        if other == params.empty_val:
            if not self.isDummy() and self.center == params.empty_val and self.size == params.empty_val:
                return True
            else:
                return False
        elif other == params.dummy_val:
            if self.area == params.dummy_val:
                return True
            else:
                return False
        elif type(other) != type(self):
            raise TypeError('must compare ellipses to ellipses')
        elif self.center == other.center and self.size == other.size and num.mod(self.angle - other.angle, TWOPI) == 0 and self.identity == other.identity:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def isEmpty(self):
        return self.__eq__(params.empty_val)

    def isDummy(self):
        return self.__eq__(params.dummy_val)

    def __nonzero__(self):
        return not self.isEmpty()

    def __setattr__(self, name, value):
        if name == 'major':
            self.size.height = value
        elif name == 'minor':
            self.size.width = value
        elif name == 'x':
            self.center.x = value
        elif name == 'y':
            self.center.y = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if name == 'width':
            return self.size.width
        elif name == 'minor':
            return self.size.width
        elif name == 'height':
            return self.size.height
        elif name == 'major':
            return self.size.height
        elif name == 'x':
            return self.center.x
        elif name == 'y':
            return self.center.y
        elif name == 'identity':
            return self.identity
        raise AttributeError('Ellipse has no attribute %s' % name)

    def __print__(self, verbose=False):
        if self.isEmpty():
            s = '[]'
        else:
            s = '[id=%d: center=' % self.identity + self.center.__print__()
            s += ', axis lengths=' + self.size.__print__()
            s += ', angle=%.3f, area=%.1f]' % (self.angle, self.area)
        return s

    def __str__(self):
        return self.__print__(False)

    def __repr__(self):
        return self.__print__(True)

    def copy(self):
        other = Ellipse(self.center.x, self.center.y, self.size.width, self.size.height, self.angle, self.area, self.identity)
        return other

    def Euc_dist(self, other):
        """Euclidean distance between two ellipse centers."""
        return float((self.center.x - other.center.x) ** 2 + (self.center.y - other.center.y) ** 2)

    def dist(self, other):
        """Calculates distance between ellipses, using some metric."""
        ang_dist = ((self.angle - other.angle + num.pi / 2.0) % num.pi - num.pi / 2.0) ** 2
        center_dist = self.Euc_dist(other)
        return num.sqrt(center_dist + params.ang_dist_wt * ang_dist)

    def compute_area(self):
        self.area = self.size.width * self.size.height * num.pi * 4.0


class TargetList:

    def __init__(self):
        self.list = {}

    def __len__(self):
        return len(self.list)

    def __setitem__(self, i, val):
        self.list[i] = val

    def __getitem__(self, i):
        if self.hasItem(i):
            return self.list[i]
        else:
            return params.empty_val

    def __eq__(self, val):
        """Test equality, either with another list of targets or with a single
        target. Returns a list of truth values."""
        if type(val) == type(params.empty_val):
            rtn = []
            for target in self.itervalues():
                if target == val:
                    rtn.append(True)
                else:
                    rtn.append(False)

        elif len(val) == len(self.list):
            rtn = []
            for (i, target) in self.iteritems():
                if val.hasItem(i) and target == val[i]:
                    rtn.append(True)
                else:
                    rtn.append(False)

        else:
            raise TypeError('must compare with a list of equal length')
        return rtn

    def __ne__(self, other):
        return not self.__eq__(other)

    def hasItem(self, i):
        return self.list.has_key(i)

    def isEmpty(self):
        return self.__eq__(params.empty_val)

    def __nonzero__(self):
        return not self.isEmpty()

    def __print__(self, verbose=False):
        s = '{'
        for target in self.itervalues():
            s += target.__print__(verbose) + '; '

        s += '\x08\x08}\n'
        return s

    def __str__(self):
        return self.__print__(False)

    def __repr__(self):
        return self.__print__(True)

    def append(self, target):
        self.list[target.identity] = target

    def pop(self, i):
        return self.list.pop(i)

    def copy(self):
        other = TargetList()
        for target in self.itervalues():
            other.append(target.copy())

        return other

    def itervalues(self):
        return self.list.itervalues()

    def iterkeys(self):
        return self.list.iterkeys()

    def iteritems(self):
        return self.list.iteritems()

    def keys(self):
        return self.list.keys()


import estconncomps as est

def find_ellipses(dfore, bw, dofix=True):
    """Fits ellipses to connected components in image.
    Returns an EllipseList, each member representing
    the x,y position and orientation of a single fly."""
    (rows, cols) = num.nonzero(bw)
    last_time = time.time()
    (L, ncc) = meas.label(bw)
    if ncc > params.max_n_clusters:
        warn('too many objects found (>%d); truncating object search' % params.max_n_clusters)
        ncc = params.max_n_clusters
        L[L >= ncc] = 0
    last_time = time.time()
    ellipses = est.weightedregionprops(L, ncc, dfore)
    if dofix:
        last_time = time.time()
        est.fixsmall(ellipses, L, dfore)
        last_time = time.time()
        est.fixlarge(ellipses, L, dfore)
    return ellipses


def find_ellipses2(dfore, bw, dofix=True):
    """Fits ellipses to connected components in image.
    Returns an EllipseList, each member representing
    the x,y position and orientation of a single fly."""
    (rows, cols) = num.nonzero(bw)
    (L, ncc) = meas.label(bw)
    if ncc > params.max_n_clusters:
        warn('too many objects found (>%d); truncating object search' % params.max_n_clusters)
        ncc = params.max_n_clusters
        L[L >= ncc] = 0
    ellipses = est.weightedregionprops(L, ncc, dfore)
    if dofix:
        est.fixsmall(ellipses, L, dfore)
        est.fixlarge(ellipses, L, dfore)
    return (ellipses, L)


def est_shape(bg):
    """Estimate fly shape from a bunch of sample frames."""
    framelist = num.round(num.linspace(0, params.n_frames - 1, params.n_frames_size)).astype(num.int)
    ellipses = []
    for frame in framelist:
        (dfore, bw) = bg.sub_bg(frame)
        (L, ncc) = meas.label(bw)
        ellipsescurr = est.weightedregionprops(L, ncc, dfore)
        ellipses += ellipsescurr

    n_ell = len(ellipses)
    if n_ell == 0:
        return
    major = num.zeros(n_ell)
    minor = num.zeros(n_ell)
    area = num.zeros(n_ell)
    for i in range(len(ellipses)):
        major[i] = ellipses[i].size.height
        minor[i] = ellipses[i].size.width
        area[i] = ellipses[i].area

    eccen = minor / major
    iseven = num.mod(n_ell, 2) == 0
    middle1 = num.floor(n_ell / 2)
    middle2 = middle1 - 1
    major.sort()
    minor.sort()
    area.sort()
    eccen.sort()
    mu_maj = major[middle1]
    mu_min = minor[middle1]
    mu_area = area[middle1]
    mu_ecc = eccen[middle1]
    if iseven:
        mu_maj = (mu_maj + major[middle2]) / 2.0
        mu_min = (mu_min + minor[middle2]) / 2.0
        mu_area = (mu_area + area[middle2]) / 2.0
        mu_ecc = (mu_ecc + eccen[middle2]) / 2.0
    major = num.abs(major - mu_maj)
    minor = num.abs(minor - mu_min)
    area = num.abs(area - mu_area)
    eccen = num.abs(eccen - mu_ecc)
    major.sort()
    minor.sort()
    area.sort()
    eccen.sort()
    sigma_maj = major[middle1]
    sigma_min = minor[middle1]
    sigma_area = area[middle1]
    sigma_ecc = eccen[middle1]
    if iseven:
        sigma_maj = (sigma_maj + major[middle2]) / 2.0
        sigma_min = (sigma_min + minor[middle2]) / 2.0
        sigma_area = (sigma_area + area[middle2]) / 2.0
        sigma_ecc = (sigma_ecc + eccen[middle2]) / 2.0
    MADTOSTDFACTOR = 1.482602
    sigma_maj *= MADTOSTDFACTOR
    sigma_min *= MADTOSTDFACTOR
    sigma_area *= MADTOSTDFACTOR
    sigma_ecc *= MADTOSTDFACTOR
    params.maxshape.major = mu_maj + params.n_std_thresh * sigma_maj
    params.minshape.major = mu_maj - params.n_std_thresh * sigma_maj
    if params.minshape.major < 0:
        params.minshape.major = 0
    params.maxshape.minor = mu_min + params.n_std_thresh * sigma_min
    params.minshape.minor = mu_min - params.n_std_thresh * sigma_min
    if params.minshape.minor < 0:
        params.minshape.minor = 0
    params.maxshape.ecc = mu_ecc + params.n_std_thresh * sigma_ecc
    params.minshape.ecc = mu_ecc - params.n_std_thresh * sigma_ecc
    if params.minshape.ecc < 0:
        params.minshape.ecc = 0
    if params.maxshape.ecc > 1:
        params.maxshape.ecc = 1
    params.maxshape.area = mu_area + params.n_std_thresh * sigma_area
    params.minshape.area = mu_area - params.n_std_thresh * sigma_area
    if params.minshape.area < 0:
        params.minshape.area = 0
    params.meanshape.major = mu_maj
    params.meanshape.minor = mu_min
    params.meanshape.ecc = mu_ecc
    params.meanshape.area = mu_area
    params.have_computed_shape = True


class EllipseWindow:
    """Container class for each ellipse drawing window."""

    def __init__(self, img_panel, ell_id=0):
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.window = wxvideo.DynamicImageCanvas(img_panel, -1)
        self.window.set_resize(True)
        self.box.Add(self.window, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        inbox = wx.BoxSizer(wx.HORIZONTAL)
        self.stext = wx.StaticText(img_panel, -1, 'ID')
        inbox.Add(self.stext, 0, wx.ALIGN_CENTER_VERTICAL)
        self.spinner = wx.SpinCtrl(img_panel, -1, min=0, max=params.nids, size=(
         params.id_spinner_width, -1), style=wx.SP_ARROW_KEYS | wx.SP_WRAP)
        self.spinner.SetValue(ell_id)
        inbox.Add(self.spinner, 0, wx.ALIGN_CENTER_VERTICAL)
        img_panel.Bind(wx.EVT_SPINCTRL, self.OnSpinner, self.spinner)
        self.box.Add(inbox, 0, wx.ALIGN_TOP)
        self.data = num.ones((params.zoom_window_pix, params.zoom_window_pix), num.uint8) * 127
        self.offset = (0, 0)
        self.ellipse = Ellipse()
        self.color = [0, 0, 0]
        self.name = 'ellipse_%d' % ell_id

    def SetData(self, ellipses, img):
        self.ellipse = ellipses
        self.data = img
        self.spinner.SetRange(0, params.nids - 1)

    def __del__(self):
        try:
            self.window.Destroy()
            self.spinner.Destroy()
            self.stext.Destroy()
        except wx._core.PyDeadObjectError:
            pass

    def OnSpinner(self, evt):
        self.redraw()

    def redraw(self, eraseBackground=False):
        """Scale data and draw on window."""
        if not hasattr(self, 'ellipse') or not hasattr(self.ellipse, 'hasItem'):
            return
        ind = self.spinner.GetValue()
        if not self.ellipse.hasItem(ind):
            blank = num.ones((params.zoom_window_pix,
             params.zoom_window_pix), num.uint8) * 127
            self.window.update_image_and_drawings(self.name, blank, format='MONO8')
        else:
            valx = self.ellipse[ind].center.x - params.zoom_window_pix / 2
            valx = max(valx, 0)
            valx = min(valx, self.data.shape[1] - params.zoom_window_pix)
            valy = self.ellipse[ind].center.y - params.zoom_window_pix / 2
            valy = max(valy, 0)
            valy = min(valy, self.data.shape[0] - params.zoom_window_pix)
            self.offset = (valx, valy)
            zoomaxes = [self.offset[0], self.offset[0] + params.zoom_window_pix - 1,
             self.offset[1], self.offset[1] + params.zoom_window_pix - 1]
            linesegs = draw_ellipses([self.ellipse[ind]], colors=[
             params.colors[(ind % len(params.colors))]])
            im = imagesk.double2mono8(self.data, donormalize=False)
            (linesegs, im) = imagesk.zoom_linesegs_and_image(linesegs, im, zoomaxes)
            (linesegs, linecolors) = imagesk.separate_linesegs_colors(linesegs)
            self.window.update_image_and_drawings(self.name, im, format='MONO8', linesegs=linesegs, lineseg_colors=linecolors)
            self.window.Refresh(eraseBackground=eraseBackground)


class EllipseFrame:
    """Window to show zoomed objects with their fit ellipses."""

    def __init__(self, parent):
        rsrc = xrc.XmlResource(ZOOM_RSRC_FILE)
        self.frame = rsrc.LoadFrame(parent, 'frame_ellipses')
        self.n_ell_spinner = xrc.XRCCTRL(self.frame, 'spin_n_ellipses')
        self.frame.Bind(wx.EVT_SPINCTRL, self.OnNEllSpinner, id=xrc.XRCID('spin_n_ellipses'))
        self.img_panel = xrc.XRCCTRL(self.frame, 'panel_show')
        self.img_box = wx.BoxSizer(wx.VERTICAL)
        self.img_panel.SetSizer(self.img_box)
        self.ellipse_windows = [
         EllipseWindow(self.img_panel, 0)]
        self.n_ell = 1
        self.img_box.Add(self.ellipse_windows[0].box, 1, wx.EXPAND)
        self.img_panel.SetAutoLayout(True)
        self.img_panel.Layout()
        self.frame.Show()

    def SetData(self, ellipses, img):
        self.ellipses = ellipses
        self.img = img
        for window in self.ellipse_windows:
            window.SetData(ellipses, img)

    def AddEllipseWindow(self, id):
        id_list = []
        for window in self.ellipse_windows:
            id_list.append(window.spinner.GetValue())

        id_list.append(id)
        self.SetEllipseWindows(id_list)
        self.n_ell += 1
        self.n_ell_spinner.SetValue(self.n_ell)

    def OnNEllSpinner(self, evt):
        """Remove or add a window."""
        id_list = []
        for window in self.ellipse_windows:
            id_list.append(window.spinner.GetValue())

        new_n_ell = self.n_ell_spinner.GetValue()
        if new_n_ell > self.n_ell:
            max_id = params.nids
            use_id = max_id - 1
            while use_id in id_list and use_id >= 0:
                use_id -= 1

            id_list.append(use_id)
        elif new_n_ell < self.n_ell:
            id_list.pop()
        self.SetEllipseWindows(id_list)
        self.n_ell = new_n_ell

    def SetEllipseWindows(self, id_list):
        self.img_box.DeleteWindows()
        self.ellipse_windows = []
        for id in id_list:
            self.ellipse_windows.append(EllipseWindow(self.img_panel, id))
            self.ellipse_windows[(-1)].SetData(self.ellipses, self.img)
            self.img_box.Add(self.ellipse_windows[(-1)].box, 1, wx.EXPAND)

        self.img_box.Layout()
        self.img_panel.Layout()
        self.Redraw(True)

    def Redraw(self, eraseBackground=False):
        """Scale images and display."""
        for window in self.ellipse_windows:
            window.redraw(eraseBackground=eraseBackground)


def find_ellipses_display(dfore, bw):
    """Fits ellipses to connected components in image.
    Returns an EllipseList, each member representing
    the x,y position and orientation of a single fly."""
    (rows, cols) = num.nonzero(bw)
    (L, ncc) = meas.label(bw)
    if ncc > params.max_n_clusters:
        warn('too many objects found (>%d); truncating object search' % params.max_n_clusters)
        ncc = params.max_n_clusters
        L[L >= ncc] = 0
    ellipses = est.weightedregionprops(L, ncc, dfore)
    (issmall, didlowerthresh, didmerge, diddelete) = est.fixsmalldisplay(ellipses, L, dfore)
    (islarge, didsplit) = est.fixlargedisplay(ellipses, L, dfore)
    return (
     ellipses, issmall, islarge, didlowerthresh, didmerge, diddelete, didsplit)


def draw_ellipses(targets, thickness=1, step=10 * num.pi / 180.0, colors=params.colors):
    """Draw ellipses on a color image (MxNx3 numpy array).
    Refuses to draw empty ellipses (center==size==area==0)."""
    if hasattr(targets, 'iteritems'):
        targetiterator = targets.iteritems()
    else:
        targetiterator = enumerate(targets)
    lines = []
    for (i, target) in targetiterator:
        if target.isEmpty():
            continue
        color = colors[(i % len(colors))]
        points = []
        alpha = num.sin(target.angle)
        beta = num.cos(target.angle)
        aa = 0.0
        ax = 2.0 * target.size.width * num.cos(aa)
        ay = 2.0 * target.size.height * num.sin(aa)
        xx = target.center.x + ax * alpha - ay * beta
        yy = target.center.y - ax * beta - ay * alpha
        for aa in num.arange(step, 2.0 * num.pi + step, step):
            xprev = xx
            yprev = yy
            ax = 2.0 * target.size.width * num.cos(aa)
            ay = 2.0 * target.size.height * num.sin(aa)
            xx = target.center.x + ax * alpha - ay * beta
            yy = target.center.y - ax * beta - ay * alpha
            lines.append([xprev + 1, yprev + 1, xx + 1, yy + 1, color])

    return lines


def draw_ellipses_bmp(img, targets, thickness=1, step=10 * num.pi / 180.0, colors=params.colors, windowsize=None, zoomaxes=None):
    """Draw ellipses on a color image (MxNx3 numpy array).
    Refuses to draw empty ellipses (center==size==area==0)."""
    if zoomaxes is None:
        zoomaxes = [
         0, img.shape[1] - 1, 0, img.shape[0] - 1]
    if hasattr(targets, 'iteritems'):
        targetiterator = targets.iteritems()
    else:
        targetiterator = enumerate(targets)
    linecolors = []
    for (i, target) in targetiterator:
        if target.isEmpty():
            continue
        linecolors.append(colors[(i % len(colors))])

    if hasattr(targets, 'iteritems'):
        targetiterator = targets.iteritems()
    else:
        targetiterator = enumerate(targets)
    linelists = []
    for (i, target) in targetiterator:
        if target.isEmpty():
            continue
        points = []
        alpha = num.sin(target.angle)
        beta = num.cos(target.angle)
        for aa in num.arange(0.0, 2.0 * num.pi + step, step):
            ax = 2.0 * target.size.width * num.cos(aa)
            ay = 2.0 * target.size.height * num.sin(aa)
            xx = target.center.x + ax * alpha - ay * beta
            yy = target.center.y - ax * beta - ay * alpha
            if xx < zoomaxes[0] or xx > zoomaxes[1] or yy < zoomaxes[2] or yy > zoomaxes[3]:
                continue
            points.append([xx + 1, yy + 1])

        linelists.append(points)

    bmp = imagesk.draw_annotated_image(img, linelists=linelists, windowsize=windowsize, zoomaxes=zoomaxes, linecolors=linecolors)
    return bmp


def find_flies(old0, old1, obs):
    """All arguments are EllipseLists. Returns an EllipseList."""
    if len(obs) == 0:
        flies = TargetList()
        return flies
    targ = m_id.cvpred(old0, old1)
    if params.print_crap:
        print 'targ (%d)' % len(targ), targ
        print 'obs (%d)' % len(obs), obs
    ids = []
    for i in targ.iterkeys():
        ids.append(i)

    vals = []
    for i in targ.itervalues():
        vals.append(i)

    cost = num.zeros((len(obs), len(targ)))
    for (i, observation) in enumerate(obs):
        for (j, target) in enumerate(vals):
            if target.isDummy():
                cost[(i, j)] = params.max_jump + eps
            else:
                cost[(i, j)] = observation.dist(target)

    (obs_for_target, unass_obs) = m_id.matchidentities(cost)
    if params.print_crap:
        print 'best matches:', obs_for_target
    flies = TargetList()
    for tt in range(len(targ)):
        if obs_for_target[tt] >= 0:
            obs[obs_for_target[tt]].identity = ids[tt]
            flies.append(obs[obs_for_target[tt]])

    for oo in range(len(obs)):
        if unass_obs[oo]:
            obs[oo].identity = params.nids
            params.nids += 1
            flies.append(obs[oo])

    if params.print_crap:
        print 'returning', flies
    return flies
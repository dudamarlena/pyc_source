# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/bg.py
# Compiled at: 2008-08-09 09:12:58
import numpy as num
from numpy import fft
from numpy import random
from scipy.interpolate import interpolate
from scipy.linalg.basic import eps
import scipy.io.mio, sys, threading, time, wx
from wx import xrc
from colormapk import colormap_image
import scipy.ndimage.measurements as meas, scipy.ndimage.morphology as morph
from ellipsesk import find_ellipses
from ellipsesk import draw_ellipses
import imagesk
from params import params
import setarena, motmot.wxvideo.wxvideo as wxvideo, motmot.wxvalidatedtext.wxvalidatedtext as wxvt, highboostfilter
from version import DEBUG
import pkg_resources
THRESH_RSRC_FILE = pkg_resources.resource_filename(__name__, 'bg_thresh.xrc')
SETTINGS_RSRC_FILE = pkg_resources.resource_filename(__name__, 'bg_settings.xrc')
HF_RSRC_FILE = pkg_resources.resource_filename(__name__, 'homomorphic.xrc')
SAVE_STUFF = False
USE_SAVED = False

class NoMoreFramesException(Exception):
    pass


class HomoFilt():
    """Implements a homomorphic filter and uses it to retrieve filtered
    movie frames."""

    def __init__(self, movie_size):
        self.movie_size = movie_size
        self.hbf = highboostfilter.highboostfilter(self.movie_size, params.hm_cutoff, params.hm_order, params.hm_boost)
        self.frame = None
        return

    def SetFrame(self, parent):
        rsrc = xrc.XmlResource(HF_RSRC_FILE)
        self.frame = rsrc.LoadFrame(parent, 'homomorphic_settings_frame')
        self.hm_cutoff_box = xrc.XRCCTRL(self.frame, 'hm_cutoff_input')
        self.hm_boost_box = xrc.XRCCTRL(self.frame, 'hm_boost_input')
        self.hm_order_box = xrc.XRCCTRL(self.frame, 'hm_order_input')
        self.hm_cutoff_box.SetValue(str(params.hm_cutoff))
        self.hm_boost_box.SetValue(str(params.hm_boost))
        self.hm_order_box.SetValue(str(params.hm_order))
        wxvt.setup_validated_float_callback(self.hm_cutoff_box, xrc.XRCID('hm_cutoff_input'), self.OnTextValidated, pending_color=params.wxvt_bg)
        wxvt.setup_validated_integer_callback(self.hm_boost_box, xrc.XRCID('hm_boost_input'), self.OnTextValidated, pending_color=params.wxvt_bg)
        wxvt.setup_validated_integer_callback(self.hm_order_box, xrc.XRCID('hm_order_input'), self.OnTextValidated, pending_color=params.wxvt_bg)

    def OnTextValidated(self, evt):
        """Set global constants based on input settings."""
        new_cutoff = float(self.hm_cutoff_box.GetValue())
        new_boost = float(self.hm_boost_box.GetValue())
        new_order = int(self.hm_order_box.GetValue())
        if new_cutoff >= 0.1 and new_cutoff <= 0.5 and new_boost >= 1.0 and new_boost <= 10.0 and new_order >= 2 and new_order <= 10:
            params.hm_cutoff = new_cutoff
            params.hm_boost = new_boost
            params.hm_order = new_order
            self.changed = True
        else:
            self.hm_cutoff_box.SetValue(str(params.hm_cutoff))
            self.hm_boost_box.SetValue(str(params.hm_boost))
            self.hm_order_box.SetValue(str(params.hm_order))

    def apply(self, I):
        Ifloat = I.astype(num.float)
        FFTlogI = num.fft.fft2(num.log(Ifloat + 1.0))
        img = num.exp(num.real(num.fft.ifft2(FFTlogI * self.hbf)))
        img[img > 255.0] = 255.0
        img[img < 0.0] = 0.0
        return img


class BackgroundCalculator():

    def __init__(self, movie, hm_cutoff=None, hm_boost=None, hm_order=None, use_thresh=None, use_median=False):
        """Initialize background subtractor."""
        params.movie = movie
        params.n_frames = params.movie.get_n_frames()
        params.bg_firstframe = max(min(params.bg_firstframe, params.n_frames - 1), 0)
        params.bg_lastframe = max(params.bg_firstframe, params.bg_lastframe)
        params.movie_size = (
         params.movie.get_height(), params.movie.get_width())
        params.GRID.setsize(params.movie_size)
        params.npixels = params.movie_size[0] * params.movie_size[1]
        self.show_img_type = params.SHOW_THRESH
        params.bg_type = params.BG_TYPE_LIGHTONDARK
        params.bg_norm_type = params.BG_NORM_STD
        self.hf = HomoFilt(params.movie_size)
        self.isnotarena = num.zeros(params.movie_size, num.bool)
        if params.movie.type == 'sbfmf':
            self.center = params.movie.h_mov.bgcenter.copy()
            self.center.shape = params.movie.h_mov.framesize
            self.dev = params.movie.h_mov.bgstd.copy()
            self.dev.shape = params.movie.h_mov.framesize
            self.med = params.movie.h_mov.bgcenter.copy()
            self.med.shape = params.movie.h_mov.framesize
            self.mad = params.movie.h_mov.bgstd.copy()
            self.mad.shape = params.movie.h_mov.framesize
            self.mean = params.movie.h_mov.bgcenter.copy()
            self.mean.shape = params.movie.h_mov.framesize
            self.std = params.movie.h_mov.bgstd.copy()
            self.std.shape = params.movie.h_mov.framesize

    def updateParameters(self):
        if params.use_median:
            self.center = self.med.copy()
        else:
            self.center = self.mean.copy()
        if params.bg_norm_type == params.BG_NORM_STD:
            if params.use_median:
                self.dev = self.mad.copy()
            else:
                self.dev = self.std.copy()
            self.dev[self.dev < params.bg_std_min] = params.bg_std_min
            self.dev[self.dev > params.bg_std_max] = params.bg_std_max
        elif params.bg_norm_type == params.BG_NORM_INTENSITY:
            self.dev = self.center.copy()
        elif params.bg_norm_type == params.BG_NORM_HOMOMORPHIC:
            self.dev = self.hfnorm.copy()
        self.hf = HomoFilt(params.movie_size)
        self.UpdateIsNotArena()

    def meanstd(self):
        bg_lastframe = min(params.bg_lastframe, params.n_frames - 1)
        nframes = params.bg_lastframe - bg_lastframe + 1
        n_bg_frames = min(nframes, params.n_bg_frames)
        nr = params.movie_size[0]
        nc = params.movie_size[1]
        nframesskip = int(num.floor(nframes / n_bg_frames))
        self.mean = num.zeros((nr, nc))
        self.std = num.zeros((nr, nc))
        nframesused = 0
        for i in range(params.bg_firstframe, bg_lastframe + 1, nframesskip):
            (im, stamp) = params.movie.get_frame(int(i))
            im = im.astype(num.float)
            self.mean += im
            self.std += im ** 2
            nframesused += 1

        self.mean /= num.double(nframesused)
        self.std /= num.double(nframesused)
        self.std = num.sqrt(self.std - self.mean ** 2)

    def flexmedmad(self):
        bg_lastframe = min(params.bg_lastframe, params.n_frames - 1)
        nframesmovie = bg_lastframe - params.bg_firstframe + 1
        nframes = min(params.n_bg_frames, nframesmovie)
        nr = params.movie_size[0]
        nc = params.movie_size[1]
        framesize = nr * nc
        nframesskip = int(num.floor(nframesmovie / nframes))
        iseven = num.mod(nframes, 2) == 0
        middle1 = num.floor(nframes / 2)
        middle2 = middle1 - 1
        nrsmall = num.int(num.floor(16000000.0 / num.double(nc) / num.double(nframes)))
        if nrsmall < 1:
            nrsmall = 1
        if nrsmall > nr:
            nrsmall = nr
        nrsmalllast = num.mod(nr, nrsmall)
        if nrsmalllast == 0:
            nrsmalllast = nrsmall
        buffersize = nrsmall * nc * nframes
        self.med = num.zeros((nr, nc))
        self.mad = num.zeros((nr, nc))
        for rowoffset in range(0, nr, nrsmall):
            print 'row offset = %d.' % rowoffset
            rowoffsetnext = int(min(rowoffset + nrsmall, nr))
            nrowscurr = rowoffsetnext - rowoffset
            buf = num.zeros((nframes, nrowscurr, nc), dtype=num.uint8)
            print 'Reading ...'
            frame = params.bg_firstframe
            for i in range(nframes):
                (data, stamp) = params.movie.get_frame(frame)
                buf[i, :, :] = data[rowoffset:rowoffsetnext, :]
                frame = frame + nframesskip

            print 'Computing ...'
            buf = num.rollaxis(num.rollaxis(buf, 2, 0), 2, 0)
            buf.sort(axis=2, kind='mergesort')
            self.med[rowoffset:rowoffsetnext, :] = buf[:, :, middle1]
            if iseven:
                self.med[rowoffset:rowoffsetnext, :] += buf[:, :, middle2]
                self.med[rowoffset:rowoffsetnext, :] /= 2.0
            buf = num.double(buf)
            for j in range(nframes):
                buf[:, :, j] = num.abs(buf[:, :, j] - self.med[rowoffset:rowoffsetnext, :])

            buf.sort(axis=2, kind='mergesort')
            self.mad[rowoffset:rowoffsetnext, :] = buf[:, :, middle1]
            if iseven:
                self.mad[rowoffset:rowoffsetnext, :] += buf[:, :, middle2]
                self.mad[rowoffset:rowoffsetnext, :] /= 2.0

        MADTOSTDFACTOR = 1.482602
        self.mad *= MADTOSTDFACTOR

    def medmad(self):
        fp = params.movie.h_mov.file
        nr = params.movie_size[0]
        nc = params.movie_size[1]
        bg_lastframe = min(params.bg_lastframe, params.n_frames - 1)
        nframesmovie = bg_lastframe - params.bg_firstframe + 1
        nframes = min(params.n_bg_frames, nframesmovie)
        print 'firstframe = %d, lastframe = %d' % (params.bg_firstframe, bg_lastframe)
        nframesskip = int(num.floor(nframesmovie / nframes))
        bytesperchunk = params.movie.h_mov.bytes_per_chunk
        if num.mod(params.movie.h_mov.bits_per_pixel, 8) != 0:
            print 'Not sure what will happen if bytesperpixel is non-integer!!'
        bytesperpixel = params.movie.h_mov.bits_per_pixel / 8.0
        headersize = params.movie.h_mov.chunk_start + params.bg_firstframe * bytesperchunk + params.movie.h_mov.timestamp_len
        framesize = nr * nc
        nbytes = num.int(nr * nc * bytesperpixel)
        iseven = num.mod(nframes, 2) == 0
        middle1 = num.floor(nframes / 2)
        middle2 = middle1 - 1
        nrsmall = num.int(num.floor(16000000.0 / num.double(nc) / num.double(nframes)))
        if nrsmall < 1:
            nrsmall = 1
        if nrsmall > nr:
            nrsmall = nr
        nrsmalllast = num.mod(nr, nrsmall)
        if nrsmalllast == 0:
            nrsmalllast = nrsmall
        nbytessmall = num.int(nrsmall * nc * bytesperpixel)
        nbytessmalllast = num.int(nrsmalllast * nc * bytesperpixel)
        buffersize = nbytessmall * nframes
        seekperframe = bytesperchunk * nframesskip - nbytessmall
        seekperframelast = bytesperchunk * nframesskip - nbytessmalllast
        self.med = num.zeros(framesize)
        self.mad = num.zeros(framesize)
        for imageoffset in range(0, nbytes, nbytessmall):
            print 'image offset = %d.' % imageoffset
            imageoffsetnext = imageoffset + nbytessmall
            if imageoffsetnext > nbytes:
                nbytescurr = nbytessmalllast
                seekperframecurr = seekperframelast
                imageoffsetnext = nbytes
            else:
                nbytescurr = nbytessmall
                seekperframecurr = seekperframe
            buf = num.zeros((nframes, nbytescurr), dtype=num.uint8)
            fp.seek(imageoffset + headersize, 0)
            print 'Reading ...'
            for i in range(nframes):
                if i > 0:
                    fp.seek(seekperframecurr, 1)
                data = fp.read(nbytescurr)
                if data == '':
                    raise NoMoreFramesException('EOF')
                buf[i, :] = num.fromstring(data, num.uint8)

            print 'Computing ...'
            buf = buf.transpose()
            buf.sort(axis=1, kind='mergesort')
            self.med[imageoffset:imageoffsetnext] = buf[:, middle1]
            if iseven:
                self.med[imageoffset:imageoffsetnext] += buf[:, middle2]
                self.med[imageoffset:imageoffsetnext] /= 2.0
            buf = num.double(buf)
            for j in range(nframes):
                buf[:, j] = num.abs(buf[:, j] - self.med[imageoffset:imageoffsetnext])

            buf.sort(axis=1, kind='mergesort')
            self.mad[imageoffset:imageoffsetnext] = buf[:, middle1]
            if iseven:
                self.mad[imageoffset:imageoffsetnext] += buf[:, middle2]
                self.mad[imageoffset:imageoffsetnext] /= 2.0

        MADTOSTDFACTOR = 1.482602
        self.mad *= MADTOSTDFACTOR
        self.mad.shape = params.movie_size
        self.med.shape = params.movie_size

    def est_bg(self):
        if params.n_bg_frames > params.n_frames:
            params.n_bg_frames = params.n_frames
        if params.use_median:
            print 'params.movie.type = ' + str(params.movie.type)
            if params.movie.type == 'fmf' or params.movie.type == 'avi' and params.movie.h_mov.bits_per_pixel == 8:
                self.medmad()
                self.center = self.med.copy()
                self.dev = self.mad.copy()
            elif params.movie.type == 'sbfmf':
                self.center = params.movie.h_mov.bgcenter.copy()
                self.dev = params.movie.h_mov.bgstd.copy()
                self.center.shape = params.movie.h_mov.framesize
                self.dev.shape = params.movie.h_mov.framesize
                print 'center.shape = ' + str(self.center.shape)
                print 'dev.shape = ' + str(self.dev.shape)
            else:
                self.flexmedmad()
                self.center = self.med.copy()
                self.dev = self.mad.copy()
        elif params.movie.type == 'fmf' or params.movie.type == 'avi':
            self.meanstd()
            self.center = self.mean.copy()
            self.dev = self.std.copy()
        elif params.movie.type == 'sbfmf':
            self.center = params.movie.h_mov.bgcenter.copy()
            self.dev = params.movie.h_mov.bgstd.copy()
            self.center.shape = params.movie.h_mov.framesize
            self.dev.shape = params.movie.h_mov.framesize
            print 'center.shape = ' + str(self.center.shape)
            print 'dev.shape = ' + str(self.dev.shape)
        else:
            wx.MessageBox('Invalid movie type', 'Error', wx.ICON_ERROR)
        self.dev[self.dev < params.bg_std_min] = params.bg_std_min
        self.dev[self.dev > params.bg_std_max] = params.bg_std_max
        self.thresh = self.dev * params.n_bg_std_thresh
        self.thresh_low = self.dev * params.n_bg_std_thresh_low
        self.UpdateIsNotArena()
        tmp = self.center.copy()
        issmall = tmp < 1.0
        tmp[issmall] = 1.0
        self.hfnorm = self.hf.apply(self.center) / tmp
        self.hfnorm[issmall & (self.hfnorm < 1.0)] = 1.0

    def sub_bg(self, framenumber):
        """Reads image, subtracts background, then thresholds."""
        (self.curr_im, stamp) = params.movie.get_frame(int(framenumber))
        im = self.curr_im.astype(num.float)
        self.curr_stamp = stamp
        if params.bg_type == params.BG_TYPE_LIGHTONDARK:
            dfore = im - self.center
            dfore[dfore < 0] = 0
        elif params.bg_type == params.BG_TYPE_DARKONLIGHT:
            dfore = self.center - im
            dfore[dfore < 0] = 0
        else:
            dfore = num.abs(im - self.center)
        dfore[self.isnotarena] = 0.0
        dfore /= self.dev
        if params.n_bg_std_thresh > params.n_bg_std_thresh_low:
            bwhigh = dfore > params.n_bg_std_thresh
            bwlow = dfore > params.n_bg_std_thresh_low
            bw = morph.binary_propagation(bwhigh, mask=bwlow)
        else:
            bw = dfore > params.n_bg_std_thresh
        return (dfore, bw)

    def ShowBG(self, parent, framenumber, old_thresh):
        if not hasattr(self, 'center'):
            wx.BeginBusyCursor()
            wx.Yield()
            self.est_bg()
            wx.EndBusyCursor()
        self.old_thresh = params.n_bg_std_thresh
        self.show_frame = framenumber
        rsrc = xrc.XmlResource(THRESH_RSRC_FILE)
        self.frame = rsrc.LoadFrame(parent, 'frame_mtrax_bg')
        self.hf.SetFrame(self.frame)
        self.hf.frame.Bind(wx.EVT_BUTTON, self.OnQuitHF, id=xrc.XRCID('hm_done_button'))
        self.hf.frame.Bind(wx.EVT_CLOSE, self.OnQuitHF)
        self.menu = self.frame.GetMenuBar()
        self.frame_text = xrc.XRCCTRL(self.frame, 'text_frame')
        self.thresh_slider = xrc.XRCCTRL(self.frame, 'slider_thresh')
        self.thresh_slider.SetScrollbar(self.GetThresholdScrollbar(), 0, params.sliderres, 25)
        self.thresh_low_slider = xrc.XRCCTRL(self.frame, 'slider_low_thresh')
        self.thresh_low_slider.SetScrollbar(self.GetThresholdLowScrollbar(), 0, params.sliderres, 25)
        self.SetThreshBounds()
        self.thresh_textinput = xrc.XRCCTRL(self.frame, 'threshold_text_input')
        self.frame.Bind(wx.EVT_SCROLL, self.OnThreshSlider, self.thresh_slider)
        wxvt.setup_validated_float_callback(self.thresh_textinput, xrc.XRCID('threshold_text_input'), self.OnThreshTextEnter, pending_color=params.wxvt_bg)
        self.thresh_low_textinput = xrc.XRCCTRL(self.frame, 'low_threshold_text_input')
        self.frame.Bind(wx.EVT_SCROLL, self.OnThreshSlider, self.thresh_low_slider)
        wxvt.setup_validated_float_callback(self.thresh_low_textinput, xrc.XRCID('low_threshold_text_input'), self.OnThreshTextEnter, pending_color=params.wxvt_bg)
        self.SetThreshold()
        self.frame_slider = xrc.XRCCTRL(self.frame, 'slider_frame')
        self.frame.Bind(wx.EVT_SCROLL, self.OnFrameSlider, self.frame_slider)
        self.frame_slider.SetScrollbar(self.show_frame, 0, params.n_frames - 1, params.n_frames / 10)
        self.bg_img_chooser = xrc.XRCCTRL(self.frame, 'view_type_input')
        self.bg_img_chooser.SetSelection(self.show_img_type)
        self.frame.Bind(wx.EVT_CHOICE, self.OnImgChoice, self.bg_img_chooser)
        self.bg_type_chooser = xrc.XRCCTRL(self.frame, 'bg_type_input')
        self.bg_type_chooser.SetSelection(params.bg_type)
        self.frame.Bind(wx.EVT_CHOICE, self.OnBgTypeChoice, self.bg_type_chooser)
        self.bg_minstd_textinput = xrc.XRCCTRL(self.frame, 'bg_min_std_input')
        wxvt.setup_validated_float_callback(self.bg_minstd_textinput, xrc.XRCID('bg_min_std_input'), self.OnMinStdTextEnter, pending_color=params.wxvt_bg)
        self.bg_minstd_textinput.SetValue('%.2f' % params.bg_std_min)
        self.bg_maxstd_textinput = xrc.XRCCTRL(self.frame, 'bg_max_std_input')
        wxvt.setup_validated_float_callback(self.bg_maxstd_textinput, xrc.XRCID('bg_max_std_input'), self.OnMinStdTextEnter, pending_color=params.wxvt_bg)
        self.bg_maxstd_textinput.SetValue('%.2f' % params.bg_std_max)
        self.bg_norm_chooser = xrc.XRCCTRL(self.frame, 'bg_normalization_input')
        self.bg_norm_chooser.SetSelection(params.bg_norm_type)
        self.frame.Bind(wx.EVT_CHOICE, self.OnNormChoice, self.bg_norm_chooser)
        self.hf_button = xrc.XRCCTRL(self.frame, 'homomorphic_settings')
        self.hf_button.Enable(False)
        self.frame.Bind(wx.EVT_BUTTON, self.OnHFClick, self.hf_button)
        self.hf_window_open = False
        self.detect_arena_button = xrc.XRCCTRL(self.frame, 'detect_arena_button')
        self.detect_arena_checkbox = xrc.XRCCTRL(self.frame, 'detect_arena_checkbox')
        self.detect_arena_button.Enable(params.do_set_circular_arena)
        self.detect_arena_checkbox.SetValue(params.do_set_circular_arena)
        self.frame.Bind(wx.EVT_BUTTON, self.OnDetectArenaClick, self.detect_arena_button)
        self.frame.Bind(wx.EVT_CHECKBOX, self.OnDetectArenaCheck, self.detect_arena_checkbox)
        self.detect_arena_window_open = False
        self.min_nonarena_textinput = xrc.XRCCTRL(self.frame, 'min_nonfore_intensity_input')
        wxvt.setup_validated_float_callback(self.min_nonarena_textinput, xrc.XRCID('min_nonfore_intensity_input'), self.OnMinNonArenaTextEnter, pending_color=params.wxvt_bg)
        self.min_nonarena_textinput.SetValue('%.1f' % params.min_nonarena)
        self.max_nonarena_textinput = xrc.XRCCTRL(self.frame, 'max_nonfore_intensity_input')
        wxvt.setup_validated_float_callback(self.max_nonarena_textinput, xrc.XRCID('max_nonfore_intensity_input'), self.OnMaxNonArenaTextEnter, pending_color=params.wxvt_bg)
        self.max_nonarena_textinput.SetValue('%.1f' % params.max_nonarena)
        self.img_panel = xrc.XRCCTRL(self.frame, 'panel_img')
        box = wx.BoxSizer(wx.VERTICAL)
        self.img_panel.SetSizer(box)
        self.img_wind = wxvideo.DynamicImageCanvas(self.img_panel, -1)
        self.img_wind.set_resize(True)
        box.Add(self.img_wind, 1, wx.EXPAND)
        self.img_panel.SetAutoLayout(True)
        self.img_panel.Layout()

    def SetThreshBounds(self, maxv=None):
        if maxv is not None:
            self.scrollbar2thresh = float(maxv) / float(params.sliderres)
            return
        (self.dfore, self.bw) = self.sub_bg(self.show_frame)
        self.max_slider = num.max(self.dfore)
        self.scrollbar2thresh = float(self.max_slider) / float(params.sliderres)
        return

    def SetThreshold(self):
        if params.n_bg_std_thresh < params.n_bg_std_thresh_low:
            params.n_bg_std_thresh_low = params.n_bg_std_thresh
        self.thresh_slider.SetThumbPosition(self.GetThresholdScrollbar())
        self.thresh_low_slider.SetThumbPosition(self.GetThresholdLowScrollbar())
        self.thresh_textinput.SetValue('%.1f' % params.n_bg_std_thresh)
        self.thresh_low_textinput.SetValue('%.1f' % params.n_bg_std_thresh_low)

    def GetThresholdScrollbar(self):
        if not hasattr(self, 'scrollbar2thresh'):
            self.SetThreshBounds()
        return params.n_bg_std_thresh / self.scrollbar2thresh

    def GetThresholdLowScrollbar(self):
        if not hasattr(self, 'scrollbar2thresh'):
            self.SetThreshBounds()
        return params.n_bg_std_thresh_low / self.scrollbar2thresh

    def ReadScrollbar(self):
        return self.thresh_slider.GetThumbPosition() * self.scrollbar2thresh

    def ReadScrollbarLow(self):
        return self.thresh_low_slider.GetThumbPosition() * self.scrollbar2thresh

    def OnShowBG(self, evt):
        self.frame_slider.Enable(False)
        self.DoSub()

    def OnShowThresh(self, evt):
        self.frame_slider.Enable(True)
        self.DoSub()

    def OnImgChoice(self, evt):
        new_img_type = self.bg_img_chooser.GetSelection()
        if new_img_type is not wx.NOT_FOUND:
            self.show_img_type = new_img_type
            self.DoSub()

    def OnBgTypeChoice(self, evt):
        new_bg_type = self.bg_type_chooser.GetSelection()
        if new_bg_type is not wx.NOT_FOUND:
            params.bg_type = new_bg_type
            self.DoSub()
            self.SetThreshBounds()
            if params.n_bg_std_thresh > self.max_slider:
                params.n_bg_std_thresh = self.max_slider
                self.SetThreshold()
                self.DoSub()

    def OnNormChoice(self, evt):
        new_norm_type = self.bg_norm_chooser.GetSelection()
        if new_norm_type is not wx.NOT_FOUND:
            params.bg_norm_type = new_norm_type
            if evt is not None:
                if params.bg_norm_type == params.BG_NORM_STD:
                    if params.use_median:
                        self.dev[:] = self.mad
                        self.dev[self.dev < params.bg_std_min] = params.bg_std_min
                        self.dev[self.dev > params.bg_std_max] = params.bg_std_max
                    else:
                        self.dev[:] = self.std
                        self.dev[self.dev < params.bg_std_min] = params.bg_std_min
                        self.dev[self.dev > params.bg_std_max] = params.bg_std_max
                    self.hf_button.Enable(False)
                elif params.bg_norm_type == params.BG_NORM_INTENSITY:
                    self.dev[:] = self.center
                    self.hf_button.Enable(False)
                elif params.bg_norm_type == params.BG_NORM_HOMOMORPHIC:
                    self.dev[:] = self.hfnorm
                    self.hf_button.Enable(True)
                if hasattr(self, 'dfore'):
                    oldmaxdfore = num.max(self.dfore)
                    donormalize = True
                else:
                    donormalize = False
                (self.dfore, self.bw) = self.sub_bg(self.show_frame)
                self.SetThreshBounds()
                if donormalize:
                    params.n_bg_std_thresh *= self.max_slider / oldmaxdfore
                    params.n_bg_std_thresh_low *= self.max_slider / oldmaxdfore
                self.SetThreshold()
                self.DoSub()
        return

    def OnHFClick(self, evt):
        if self.hf_window_open:
            self.hf.frame.Raise()
            return
        self.hf_window_open = True
        self.hf.frame.Show()

    def OnDetectArenaCheck(self, evt):
        if evt is None:
            return
        params.do_set_circular_arena = self.detect_arena_checkbox.GetValue()
        self.detect_arena_button.Enable(params.do_set_circular_arena)
        self.UpdateIsNotArena()
        self.DoSub()
        return

    def UpdateIsNotArena(self):
        self.isnotarena = num.zeros(params.movie_size, num.bool)
        if hasattr(params, 'max_nonarena'):
            self.isnotarena = self.center <= params.max_nonarena
        if hasattr(params, 'min_nonarena'):
            self.isnotarena = self.isnotarena | (self.center >= params.min_nonarena)
        if params.do_set_circular_arena and hasattr(params, 'arena_center_x') and params.arena_center_x is not None:
            self.isnotarena = self.isnotarena | ((params.GRID.X - params.arena_center_x) ** 2.0 + (params.GRID.Y - params.arena_center_y) ** 2 > params.arena_radius ** 2.0)
        return

    def OnDetectArenaClick(self, evt):
        if self.detect_arena_window_open:
            self.detect_arena.frame.Raise()
            return
        self.detect_arena_window_open = True
        self.detect_arena = setarena.SetArena(self.frame, self.center)
        self.detect_arena.frame.Bind(wx.EVT_BUTTON, self.OnQuitDetectArena, id=xrc.XRCID('done_button'))
        self.detect_arena.frame.Bind(wx.EVT_CLOSE, self.OnQuitDetectArena)
        self.detect_arena.frame.Show()

    def OnQuitDetectArena(self, evt):
        (params.arena_center_x, params.arena_center_y, params.arena_radius) = self.detect_arena.GetArenaParameters()
        self.UpdateIsNotArena()
        self.detect_arena_window_open = False
        self.detect_arena.frame.Destroy()
        delattr(self, 'detect_arena')
        self.DoSub()

    def OnQuitHF(self, evt):
        self.hf_window_open = False
        self.hf.frame.Hide()
        self.DoSub()

    def OnThreshSlider(self, evt):
        params.n_bg_std_thresh = self.ReadScrollbar()
        params.n_bg_std_thresh_low = self.ReadScrollbarLow()
        if params.n_bg_std_thresh_low > params.n_bg_std_thresh:
            params.n_bg_std_thresh_low = params.n_bg_std_thresh
        self.thresh_textinput.SetValue('%.1f' % params.n_bg_std_thresh)
        self.thresh_low_textinput.SetValue('%.1f' % params.n_bg_std_thresh_low)
        if evt is not None:
            self.DoSub()
        return

    def OnThreshTextEnter(self, evt):
        params.n_bg_std_thresh = float(self.thresh_textinput.GetValue())
        params.n_bg_std_thresh_low = float(self.thresh_low_textinput.GetValue())
        if params.n_bg_std_thresh < 0:
            params.n_bg_std_thresh = 0
        if params.n_bg_std_thresh_low < 0:
            params.n_bg_std_thresh_low = 0
        if params.n_bg_std_thresh_low > params.n_bg_std_thresh:
            params.n_bg_std_thresh_low = params.n_bg_std_thresh
        self.thresh_slider.SetThumbPosition(self.GetThresholdScrollbar())
        self.thresh_low_slider.SetThumbPosition(self.GetThresholdLowScrollbar())
        if evt is not None:
            self.DoSub()
        return

    def OnMinStdTextEnter(self, evt):
        textentered = self.bg_minstd_textinput.GetValue()
        maxtextentered = self.bg_maxstd_textinput.GetValue()
        try:
            numentered = float(textentered)
            maxnumentered = float(maxtextentered)
            if numentered > maxnumentered:
                self.bg_minstd_textinput.SetValue('%.2f' % params.bg_std_min)
                self.bg_maxstd_textinput.SetValue('%.2f' % params.bg_std_max)
                return
            if numentered < 0:
                numentered = 0
            if maxnumentered < 0:
                maxnumentered = 0
            if numentered > 255:
                maxnumentered = 255
            params.bg_std_min = numentered
            params.bg_std_max = maxnumentered
            self.bg_minstd_textinput.SetValue('%.2f' % params.bg_std_min)
            self.bg_maxstd_textinput.SetValue('%.2f' % params.bg_std_max)
            if params.use_median:
                self.dev[:] = self.mad
            else:
                self.dev[:] = self.std
            self.dev[self.dev < params.bg_std_min] = params.bg_std_min
            self.dev[self.dev > params.bg_std_max] = params.bg_std_max
        except ValueError:
            self.bg_minstd_textinput.SetValue('%.2f' % params.bg_std_min)
            self.bg_maxstd_textinput.SetValue('%.2f' % params.bg_std_max)
            return

        if evt is not None:
            self.DoSub()
            self.SetThreshBounds()
            if params.n_bg_std_thresh > self.max_slider:
                params.n_bg_std_thresh = self.max_slider
                self.SetThreshold()
                self.DoSub()
        return

    def OnMinNonArenaTextEnter(self, evt):
        textentered = self.min_nonarena_textinput.GetValue()
        try:
            params.min_nonarena = float(textentered)
        except ValueError:
            self.min_nonarena_textinput.SetValue('%.1f' % params.min_nonarena)
            return

        if evt is not None:
            self.UpdateIsNotArena()
            self.DoSub()
        return

    def OnMaxNonArenaTextEnter(self, evt):
        textentered = self.max_nonarena_textinput.GetValue()
        try:
            params.max_nonarena = float(textentered)
        except ValueError:
            self.max_nonarena_textinput.SetValue('%.1f' % params.max_nonarena)
            return

        if evt is not None:
            self.UpdateIsNotArena()
            self.DoSub()
        return

    def OnFrameSlider(self, evt):
        self.show_frame = self.frame_slider.GetThumbPosition()
        self.frame_text.SetLabel('frame %d' % self.show_frame)
        if evt is not None:
            self.DoSub()
            self.SetThreshBounds()
        return

    def DoSub(self):
        """Do background subtraction."""
        wx.BeginBusyCursor()
        wx.Yield()
        (self.dfore, self.bw) = self.sub_bg(self.show_frame)
        self.windowsize = [self.img_panel.GetRect().GetHeight(), self.img_panel.GetRect().GetWidth()]
        if self.show_img_type == params.SHOW_BACKGROUND:
            img_8 = imagesk.double2mono8(self.center, donormalize=False)
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8')
        elif self.show_img_type == params.SHOW_DISTANCE:
            img_8 = imagesk.double2mono8(self.dfore)
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8')
        elif self.show_img_type == params.SHOW_THRESH:
            img_8 = imagesk.double2mono8(self.bw.astype(float))
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8')
        elif self.show_img_type == params.SHOW_NONFORE:
            img_8 = imagesk.double2mono8(self.isnotarena.astype(float))
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8')
        elif self.show_img_type == params.SHOW_DEV:
            mu = num.mean(self.dev)
            sig = num.std(self.dev)
            if sig == 0:
                print 'dev is uniformly ' + str(mu)
                img_8 = imagesk.double2mono8(self.dev)
            else:
                n1 = mu - 3.0 * sig
                n2 = mu + 3.0 * sig
                img_8 = imagesk.double2mono8(self.dev.clip(n1, n2))
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8')
        elif self.show_img_type == params.SHOW_CC:
            (L, ncc) = meas.label(self.bw)
            img_8 = colormap_image(L)
            self.img_wind.update_image_and_drawings('bg', img_8, format='RGB8')
        elif self.show_img_type == params.SHOW_ELLIPSES:
            obs = find_ellipses(self.dfore, self.bw, False)
            (im, stamp) = params.movie.get_frame(int(self.show_frame))
            img_8 = imagesk.double2mono8(im, donormalize=False)
            plot_linesegs = draw_ellipses(obs)
            (linesegs, linecolors) = imagesk.separate_linesegs_colors(plot_linesegs)
            img_8 = imagesk.double2mono8(im, donormalize=False)
            self.img_wind.update_image_and_drawings('bg', img_8, format='MONO8', linesegs=linesegs, lineseg_colors=linecolors)
        self.img_wind.Refresh(eraseBackground=False)
        wx.EndBusyCursor()


class BgSettingsDialog():

    def __init__(self, parent, bg):
        self.bg = bg
        rsrc = xrc.XmlResource(SETTINGS_RSRC_FILE)
        self.frame = rsrc.LoadFrame(parent, 'bg_settings')
        self.algorithm = xrc.XRCCTRL(self.frame, 'algorithm')
        self.nframes = xrc.XRCCTRL(self.frame, 'nframes')
        self.bg_firstframe = xrc.XRCCTRL(self.frame, 'bg_firstframe')
        self.bg_lastframe = xrc.XRCCTRL(self.frame, 'bg_lastframe')
        self.calculate = xrc.XRCCTRL(self.frame, 'calculate_button')
        if params.use_median:
            self.algorithm.SetSelection(params.ALGORITHM_MEDIAN)
        else:
            self.algorithm.SetSelection(params.ALGORITHM_MEAN)
        self.nframes.SetValue(str(params.n_bg_frames))
        wxvt.setup_validated_integer_callback(self.nframes, xrc.XRCID('nframes'), self.OnTextValidated, pending_color=params.wxvt_bg)
        self.bg_firstframe.SetValue(str(params.bg_firstframe))
        wxvt.setup_validated_integer_callback(self.bg_firstframe, xrc.XRCID('bg_firstframe'), self.OnTextValidatedFirstframe, pending_color=params.wxvt_bg)
        self.bg_lastframe.SetValue(str(params.bg_lastframe))
        wxvt.setup_validated_integer_callback(self.bg_lastframe, xrc.XRCID('bg_lastframe'), self.OnTextValidatedLastframe, pending_color=params.wxvt_bg)
        self.frame.Bind(wx.EVT_CHOICE, self.OnAlgorithmChoice, self.algorithm)
        self.frame.Bind(wx.EVT_BUTTON, self.OnCalculate, self.calculate)
        self.frame.Show()

    def OnCalculate(self, evt):
        wx.BeginBusyCursor()
        wx.Yield()
        self.bg.est_bg()
        wx.EndBusyCursor()

    def OnTextValidated(self, evt):
        tmp = int(self.nframes.GetValue())
        if tmp > 0:
            params.n_bg_frames = tmp
            if params.n_bg_frames > params.n_frames:
                params.n_bg_frames = params.n_frames
            self.nframes.SetValue(str(params.n_bg_frames))

    def OnTextValidatedFirstframe(self, evt):
        tmp0 = int(self.bg_firstframe.GetValue())
        tmp = tmp0
        tmp = max(tmp, 0)
        tmp = min(tmp, params.bg_lastframe)
        tmp = min(tmp, params.n_frames - 1)
        params.bg_firstframe = tmp
        if not tmp == tmp0:
            self.bg_firstframe.SetValue(str(params.bg_firstframe))

    def OnTextValidatedLastframe(self, evt):
        tmp0 = int(self.bg_lastframe.GetValue())
        tmp = tmp0
        tmp = max(tmp, params.bg_firstframe)
        params.bg_lastframe = tmp
        if not tmp == tmp0:
            self.bg_lastframe.SetValue(str(params.bg_lastframe))

    def OnAlgorithmChoice(self, evt):
        new_alg_type = self.algorithm.GetSelection()
        if new_alg_type is not wx.NOT_FOUND:
            if new_alg_type == params.ALGORITHM_MEDIAN:
                params.use_median = True
            else:
                params.use_median = False


def save_image(filename, img):
    """Saves an image as a MATLAB array."""
    scipy.io.mio.savemat(filename + '.mat', {filename: img})
    print 'saved', filename, '.mat'


def read_image(filename):
    """Reads an image from a mat-file."""
    new_dict = scipy.io.mio.loadmat(filename)
    print 'loaded', filename, '.mat'
    return new_dict[filename]


def write_img_text(img, filename):
    fp = open(filename, 'w')
    for r in img:
        for c in r:
            fp.write('%f\t' % c)

        fp.write('\n')

    fp.close()
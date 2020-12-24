# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/algorithm.py
# Compiled at: 2008-08-14 20:11:43
import numpy as num
from scipy.linalg.basic import eps
import time, wx
from wx import xrc
import setarena, chooseorientations, os, motmot.wxvalidatedtext as wxvt
from version import DEBUG
import annfiles as annot, ellipsesk as ell, settings, hindsight, sys
from params import params
import pkg_resources
SETTINGS_RSRC_FILE = pkg_resources.resource_filename(__name__, 'track_settings.xrc')

class MtraxAlgorithm(settings.AppWithSettings):
    """Cannot be used alone -- this class only exists
    to keep algorithm code together in one file."""

    def Track(self):
        """Run the m-tracker."""
        self.maxlookback = max(params.lostdetection_length, params.spuriousdetection_length, params.mergeddetection_length, params.splitdetection_length)
        self.ann_file = annot.AnnotationFile(self.ann_filename, params.version, True)
        self.ann_file.WriteAnnHeader(params.start_frame, self.bg_imgs)
        if self.ann_data is None or len(self.ann_data) == 0:
            self.ann_data = []
            params.nids = 0
        for ff in range(len(self.ann_data) - self.maxlookback):
            self.ann_file.write_ellipses(self.ann_data[ff])

        self.lastframewritten = max(-1, len(self.ann_data) - self.maxlookback - 1)
        wx.Yield()
        self.hindsight = hindsight.Hindsight(self.ann_data, self.bg_imgs)
        self.hindsight.initialize_milestones()
        self.break_flag = False
        for self.start_frame in range(self.start_frame, self.n_frames):
            if self.break_flag:
                break
            last_time = time.time()
            (self.dfore, self.isfore) = self.bg_imgs.sub_bg(self.start_frame)
            if self.dowritesbfmf:
                self.movie.writesbfmf_writeframe(self.isfore, self.bg_imgs.curr_im, self.bg_imgs.curr_stamp, self.start_frame)
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break
            self.ellipses = ell.find_ellipses(self.dfore, self.isfore)
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break
            if len(self.ann_data) > 1:
                flies = ell.find_flies(self.ann_data[(-2)], self.ann_data[(-1)], self.ellipses)
            if len(self.ann_data) == 1:
                flies = ell.find_flies(self.ann_data[0], self.ann_data[0], self.ellipses)
            flies = ell.TargetList()
            for (i, obs) in enumerate(self.ellipses):
                if obs.isEmpty():
                    print 'empty observation'
                else:
                    obs.identity = params.nids
                    flies.append(obs)
                    params.nids += 1

            self.ann_data.append(flies)
            self.hindsight.fixerrors()
            if self.ann_data is not None and len(self.ann_data) > self.maxlookback + self.lastframewritten:
                self.lastframewritten = self.lastframewritten + 1
                self.ann_file.write_ellipses(self.ann_data[self.lastframewritten])
            if params.request_refresh or params.do_refresh and self.start_frame % params.framesbetweenrefresh == 0:
                if params.interactive:
                    if self.start_frame:
                        self.ShowCurrentFrame()
                else:
                    sys.stderr.write('Frame %d / %d\n' % (self.start_frame, self.n_frames))
                params.request_refresh = False
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break

        print 'out of loop'
        self.Finish()
        return

    def Finish(self):
        for ff in range(self.lastframewritten + 1, len(self.ann_data)):
            self.ann_file.write_ellipses(self.ann_data[ff])

        self.lastframewritten = len(self.ann_data) - 1
        self.ann_file.file.close()

    def StopThreads(self):
        print 'in stopthreads, setting break_flag to true'
        self.break_flag = True

    def InitTrackingState(self):
        self.tracking = True
        self.ann_data = []
        params.nids = 0
        params.start_frame = 0
        self.start_frame = 0

    def DoAllPreprocessing(self):
        if not self.IsBGModel() or params.batch_autodetect_bg_model:
            print 'Estimating background model'
            self.bg_imgs.est_bg()
        else:
            print 'Not estimating background model'
        if params.do_set_circular_arena and params.batch_autodetect_arena:
            print 'Auto-detecting circular arena'
            setarena.doall(self.bg_imgs.center)
        else:
            print 'Not detecting arena'
        self.bg_imgs.UpdateIsNotArena()
        if params.batch_autodetect_shape:
            print 'Estimating shape model'
            ell.est_shape(self.bg_imgs)
        else:
            print 'Not estimating shape model'

    def DoAll(self):
        if not params.interactive:
            self.RestoreStdio()
        sys.stderr.write('Performing preprocessing...\n')
        self.DoAllPreprocessing()
        sys.stderr.write('Done preprocessing, beginning tracking...\n')
        if params.interactive:
            self.UpdateToolBar('started')
        sys.stderr.write('Tracking...\n')
        self.Track()
        sys.stderr.write('Choosing Orientations...\n')
        self.choose_orientations = chooseorientations.ChooseOrientations(self.frame, self.ann_data, interactive=False)
        self.choose_orientations.ChooseOrientations()
        (basename, ext) = os.path.splitext(self.filename)
        if self.matfilename is None:
            savename = basename + '.mat'
        else:
            savename = self.matfilename
        sys.stderr.write('Saving to mat file ' + savename + '...\n')
        self.ann_file.WriteMAT(savename, self.ann_data)
        sys.stderr.write('Done\n')
        return
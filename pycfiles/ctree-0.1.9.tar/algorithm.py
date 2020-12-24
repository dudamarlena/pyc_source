# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/algorithm.py
# Compiled at: 2016-03-19 20:20:50
import multiprocessing, os
from Queue import Empty as QueueEmpty
import sys
from threading import Timer
import time, traceback, numpy as num, wx
from wx import xrc
from version import DEBUG, DEBUG_TRACKINGSETTINGS
import annfiles as annot, codedir, ellipsesk as ell, hindsight, setarena, chooseorientations
from params import params
import setarena, settings
from version import DEBUG
SETTINGS_RSRC_FILE = os.path.join(codedir.codedir, 'xrc', 'tracking_settings.xrc')
if SETTINGS_RSRC_FILE is None:
    SETTINGS_RSRC_FILE = os.path.join('xrc', 'tracking_settings.xrc')
if DEBUG:
    import pdb
DEBUG_LEVEL = 2
if not DEBUG:
    DEBUG_LEVEL = 0
PRINT_COUNTS = False

class CtraxAlgorithm(settings.AppWithSettings):
    """Cannot be used alone -- this class only exists
    to keep algorithm code together in one file."""

    def Track(self):
        """Run the tracker."""
        if DEBUG:
            print 'Tracking from frame %d...' % self.start_frame
        if DEBUG:
            print 'Last frame tracked = %d' % self.ann_file.lastframetracked
        self.maxlookback = max(params.lostdetection_length, params.spuriousdetection_length, params.mergeddetection_length, params.splitdetection_length)
        if params.interactive:
            wx.Yield()
        self.hindsight = hindsight.Hindsight(self.ann_file, self.bg_imgs)
        self.bg_imgs.set_buffer_maxnframes()
        self.track_timer_start_time = time.time()
        self.update_track_time()
        self.break_flag = False
        for self.start_frame in range(self.start_frame, self.movie.get_n_frames()):
            if DEBUG or DEBUG_TRACKINGSETTINGS:
                print 'frame', self.start_frame
            if self.start_frame >= self.last_frame:
                break
            if DEBUG_LEVEL > 0:
                print 'Tracking frame %d / %d' % (self.start_frame, self.movie.get_n_frames() - 1)
            if self.break_flag:
                break
            last_time = time.time()
            try:
                dfore, isfore, cc, ncc = self.bg_imgs.sub_bg(self.start_frame)
            except IOError:
                if self.movie.type == 'cavi' and self.start_frame >= self.movie.get_n_frames() - 2:
                    print 'ignoring compressed AVI IOError reading last frame'
                else:
                    traceback.print_exc()
                break
            except:
                traceback.print_exc()
                break

            if DEBUG_LEVEL > 1:
                print ncc, 'connected components'
            if self.dowritesbfmf:
                self.movie.writesbfmf_writeframe(isfore, self.bg_imgs.curr_im, self.bg_imgs.curr_stamp, self.start_frame)
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break
            ellipses = ell.find_ellipses(dfore, cc, ncc)
            if DEBUG_LEVEL > 1:
                print len(ellipses), 'ellipses'
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break
            if DEBUG_LEVEL > 0:
                print 'matching identities'
            if len(self.ann_file) > 1:
                flies = ell.find_flies(self.ann_file[(-2)], self.ann_file[(-1)], ellipses, self.ann_file)
            elif len(self.ann_file) == 1:
                flies = ell.find_flies(self.ann_file[(-1)], self.ann_file[(-1)], ellipses, self.ann_file)
            else:
                flies = ell.TargetList()
                for i, obs in enumerate(ellipses):
                    if obs.isEmpty():
                        if DEBUG:
                            print 'empty observation'
                    else:
                        newid = self.ann_file.GetNewId()
                        obs.identity = newid
                        flies.append(obs)

            if DEBUG_LEVEL > 1:
                print len(flies), 'flies'
            if DEBUG_LEVEL > 0:
                print 'Done with frame %d, appending to ann_file' % self.start_frame
            self.ann_file.append(flies)
            if DEBUG_LEVEL > 0:
                print 'Added to ann_file, now running fixerrors'
            self.hindsight.fixerrors()
            if self.request_refresh or self.do_refresh and self.start_frame % self.framesbetweenrefresh == 0:
                if params.interactive:
                    if self.start_frame:
                        self.ShowCurrentFrame()
                else:
                    print '    Frame %d / %d' % (self.start_frame, self.movie.get_n_frames() - 1)
                self.request_refresh = False
            if DEBUG_LEVEL > 1:
                print len(self.ann_file[(-1)]), 'flies in last frame'
            if params.interactive:
                wx.Yield()
            if self.break_flag:
                break
            if self.start_frame % 100 == 0 and self.has('diagnostics_filename'):
                self.write_diagnostics()

        if hasattr(self, 'timer'):
            self.timer.cancel()
            self.track_timer_cancel = True
        self.Finish()

    def write_diagnostics(self):
        """Safely write diagnostics file."""
        if not self.has('diagnostics_filename'):
            self.diagnostics_filename = self.get_filename_with_extension('_ctraxdiagnostics.txt')
        annot.WriteDiagnostics(self.diagnostics_filename)

    def update_track_time(self):
        """Update the time shown in the timer box."""
        if hasattr(self, 'track_timer_cancel'):
            delattr(self, 'track_timer_cancel')
            return
        elapsed = time.time() - self.track_timer_start_time
        h = int((elapsed - elapsed % 3600.0) / 60.0 / 60.0)
        elapsed -= h * 60.0 * 60.0
        m = int((elapsed - elapsed % 60.0) / 60.0)
        elapsed -= m * 60.0
        s = int(round(elapsed))
        if h == 0:
            time_str = '%02d:%02d' % (m, s)
        else:
            if h == 1 and m < 40:
                time_str = '%02d:%02d' % (m + 60, s)
            elif s % 2 == 0:
                time_str = '%02d:%02d' % (h, m)
            else:
                time_str = '%02d %02d' % (h, m)
            try:
                self.time_text.SetValue(time_str)
            except wx.PyDeadObjectError:
                return
            except AttributeError:
                return
            except wx._core.PyAssertionError:
                pass

        self.timer = Timer(1.0, self.update_track_time)
        self.timer.start()

    def Finish(self):
        self.ann_file.write_all_frames_to_disk()
        if self.has('diagnostics_filename'):
            self.write_diagnostics()

    def StopThreads(self):
        self.break_flag = True

    def DoAllPreprocessing(self):
        if not self.IsBGModel() or params.batch_autodetect_bg_model:
            print 'Estimating background model'
            if not params.batch_autodetect_bg_model:
                print '**autodetecting background because no existing model is loaded'
            print 'BG Modeling parameters:'
            print 'n_bg_frames = ' + str(self.bg_imgs.n_bg_frames)
            print 'use_median = ' + str(self.bg_imgs.use_median)
            print 'bg_firstframe = ' + str(self.bg_imgs.bg_firstframe)
            print 'bg_lastframe = ' + str(self.bg_imgs.bg_lastframe)
            if not self.OnComputeBg():
                return
            self.bg_imgs.updateParameters()
        else:
            print 'Not estimating background model'
        if params.do_set_circular_arena and params.batch_autodetect_arena:
            print 'Auto-detecting circular arena'
            setarena.doall(self.bg_imgs.center)
        else:
            print 'Not detecting arena'
        self.bg_imgs.UpdateIsArena()
        if params.batch_autodetect_shape and params.enforce_minmax_shape:
            print 'Estimating shape model'
            self.OnComputeShape()
        else:
            print 'Not estimating shape model'

    def DoAll(self):
        if not params.interactive:
            self.RestoreStdio()
        print 'Performing preprocessing...\n'
        self.DoAllPreprocessing()
        if params.noninteractive_resume_tracking and self.ann_file.lastframetracked > 0:
            print 'resuming at', self.ann_file.lastframetracked
            self.start_frame = self.ann_file.lastframetracked
            if DEBUG_LEVEL > 0:
                print 'start_frame = ' + str(self.start_frame)
            if DEBUG_LEVEL > 0:
                print 'cropping annotation file to frames %d through %d' % (self.ann_file.firstframetracked, self.ann_file.lastframetracked - 1)
            self.ann_file.InitializeData(self.ann_file.firstframetracked, self.ann_file.lastframetracked - 1, bg_model=self.bg_imgs)
            print 'initialized...', self.ann_file.lastframetracked
        else:
            print 'Initializing annotation file...\n'
            self.ann_file.InitializeData(self.start_frame, bg_model=self.bg_imgs)
        print 'Done preprocessing, beginning tracking...\n'
        if params.interactive:
            self.UpdateToolBar('started')
        if self.dowritesbfmf:
            self.movie.writesbfmf_start(self.bg_imgs, self.writesbfmf_filename)
        print 'Tracking...'
        try:
            self.Track()
        except:
            print 'Error during Track'
            raise

        print 'Done tracking'
        if self.dowritesbfmf and self.movie.writesbfmf_isopen():
            self.movie.writesbfmf_close(self.start_frame)
        print 'Choosing Orientations...'
        choose_orientations = chooseorientations.ChooseOrientations(self.frame, interactive=False)
        self.ann_file = choose_orientations.ChooseOrientations(self.ann_file, bg_model=self.bg_imgs)
        if self.has('matfilename'):
            savename = self.matfilename
        else:
            savename = self.get_filename_with_extension('.mat')
        print 'Saving to MAT file', savename
        self.ann_file.WriteMAT(self.movie, savename)
        if self.has('csvfilename'):
            print 'Saving to CSV file', self.csvfilename
            self.ann_file.WriteCSV(self.csvfilename)
        print 'Done\n'
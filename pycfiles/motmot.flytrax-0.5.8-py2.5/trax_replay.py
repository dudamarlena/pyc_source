# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/flytrax/trax_replay.py
# Compiled at: 2009-04-14 12:30:53
import pkg_resources, flytrax
try:
    import flytrax.traxio as traxio
except ImportError:
    import traxio

import motmot.FlyMovieFormat.FlyMovieFormat as FlyMovieFormat, numpy, motmot.FastImage.FastImage as FastImage, wx, wx.xrc as xrc, time, Queue, threading, os, sys, motmot.fview.fview_video as video_module
RESFILE = pkg_resources.resource_filename(__name__, 'trax_replay.xrc')
RES = xrc.EmptyXmlResource()
RES.LoadFromString(open(RESFILE).read())

class ReplayApp(wx.App):

    def OnInit(self, *args, **kw):
        wx.InitAllImageHandlers()
        self.frame = RES.LoadFrame(None, 'TRAX_REPLAY_FRAME')
        self.frame.Show()
        widget = xrc.XRCCTRL(self.frame, 'LOAD_TRX_BUTTON')
        wx.EVT_BUTTON(widget, widget.GetId(), self.OnLoadTrx)
        widget = xrc.XRCCTRL(self.frame, 'PLAY_FRAMES')
        wx.EVT_BUTTON(widget, widget.GetId(), self.OnPlayFrames)
        self.loaded_trx = None
        main_display_panel = xrc.XRCCTRL(self.frame, 'MAIN_DISPLAY_PANEL')
        box = wx.BoxSizer(wx.VERTICAL)
        main_display_panel.SetSizer(box)
        self.cam_image_canvas = video_module.DynamicImageCanvas(main_display_panel, -1)
        box.Add(self.cam_image_canvas, 1, wx.EXPAND)
        main_display_panel.SetAutoLayout(True)
        main_display_panel.Layout()
        self.inq = Queue.Queue()
        self.playing = threading.Event()
        ID_Timer = wx.NewId()
        self.timer = wx.Timer(self, ID_Timer)
        wx.EVT_TIMER(self, ID_Timer, self.OnTimer)
        self.timer.Start(100)
        self.statusbar = self.frame.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusText('no .trx file loaded', 0)
        return True

    def OnTimer(self, event):
        tup = None
        if not self.playing.isSet():
            if self.loaded_trx is None:
                return
            self.statusbar.SetStatusText('showing background', 1)
            tracker = self.loaded_trx['tracker']
            bg_image = self.loaded_trx['bg_image']
            cam_id = self.loaded_trx['cam_id']
            buf_offset = (0, 0)
            timestamp = 0.0
            framenumber = 0
            (points, linesegs) = tracker.process_frame(cam_id, bg_image, buf_offset, timestamp, framenumber)
            tup = (bg_image, points, linesegs)
        try:
            while 1:
                tup = self.inq.get(0)
                self.statusbar.SetStatusText('playing', 1)

        except Queue.Empty:
            pass

        if tup is not None:
            (im, points, linesegs) = tup
            self.cam_image_canvas.update_image_and_drawings('camera', im, format=self.loaded_trx['format'], points=points, linesegs=linesegs)
        return

    def OnLoadTrx(self, event):
        doit = False
        dlg = wx.FileDialog(self.frame, 'Select .trx file', style=wx.OPEN, wildcard='*.trx')
        try:
            if dlg.ShowModal() == wx.ID_OK:
                trx_filename = dlg.GetPath()
                doit = True
        finally:
            dlg.Destroy()

        if not doit:
            return
        self.load_trx(trx_filename)

    def load_trx(self, trx_filename):
        if self.loaded_trx is not None:
            tracker = self.loaded_trx['tracker']
            tracker.get_frame().Destroy()
            self.loaded_trx = None
            self.inq = Queue.Queue()
        fmf_filename = os.path.splitext(trx_filename)[0] + '.fmf'
        (bg_image, all_vals) = traxio.readtrax(trx_filename)
        all_vals = numpy.asarray(all_vals)
        fmf = FlyMovieFormat.FlyMovie(fmf_filename)
        assert len(all_vals) == fmf.get_n_frames()
        n_frames = len(all_vals)
        cam_id = 'fake_camera'
        format = 'MONO8'
        tracker = flytrax.Tracker(self.frame)
        tracker.get_frame().Show()
        wx.EVT_CLOSE(tracker.get_frame(), self.OnTrackerWindowClose)
        tracker.camera_starting_notification(cam_id, pixel_format=format, max_width=bg_image.shape[1], max_height=bg_image.shape[0])
        self.loaded_trx = dict(bg_image=bg_image, all_vals=all_vals, fmf=fmf, n_frames=n_frames, cam_id=cam_id, format=format, tracker=tracker)
        self.inq = Queue.Queue()
        self.cam_image_canvas.update_image_and_drawings('camera', bg_image, format=format)
        self.statusbar.SetStatusText('%s loaded' % (os.path.split(trx_filename)[1],), 0)
        return

    def OnTrackerWindowClose(self, event):
        pass

    def OnPlayFrames(self, event):
        if self.loaded_trx is None:
            print 'no .trx file loaded'
            return
        self.play_thread = threading.Thread(target=play_func, args=(self.loaded_trx,
         self.inq,
         self.playing))
        self.play_thread.setDaemon(True)
        self.play_thread.start()
        return


def play_func(loaded_trx, im_pts_segs_q, playing):
    playing.set()
    try:
        n_frames = loaded_trx['n_frames']
        all_vals = loaded_trx['all_vals']
        fmf = loaded_trx['fmf']
        bg_image = loaded_trx['bg_image']
        tracker = loaded_trx['tracker']
        cam_id = loaded_trx['cam_id']
        format = loaded_trx['format']
        fibg = FastImage.asfastimage(bg_image)
        smallframe_size = None
        fmf.seek(0)
        for fno in range(n_frames):
            (posx, posy, orientation, windowx, windowy, data_timestamp) = all_vals[fno][:6]
            (smallframe, fmf_timestamp) = fmf.get_frame(fno)
            fismall = FastImage.asfastimage(smallframe)
            assert fmf_timestamp == data_timestamp
            timestamp = fmf_timestamp
            fullsize_image = bg_image.copy()
            fullsize_image[windowy:windowy + smallframe.shape[0], windowx:windowx + smallframe.shape[1]] = smallframe
            fullsize_image = FastImage.asfastimage(fullsize_image)
            buf_offset = (0, 0)
            framenumber = fno
            (points, linesegs) = tracker.process_frame(cam_id, fullsize_image, buf_offset, timestamp, framenumber)
            tup = (fullsize_image, points, linesegs)
            im_pts_segs_q.put(tup)

    finally:
        playing.clear()

    return


def main():
    app = ReplayApp(0)
    if len(sys.argv) > 1:
        trx_filename = sys.argv[1]
        app.load_trx(trx_filename)
    app.MainLoop()
    if app.loaded_trx is not None:
        tracker = app.loaded_trx['tracker']
        tracker.quit()
    return


if __name__ == '__main__':
    main()
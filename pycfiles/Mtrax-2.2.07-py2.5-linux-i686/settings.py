# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mtrax/settings.py
# Compiled at: 2008-08-08 12:34:44
import os, sys, wx
from wx import xrc
from params import params
import tracking_settings, chooseorientations, numpy as num, motmot.wxglvideo.simple_overlay as wxvideo, motmot.wxvalidatedtext.wxvalidatedtext as wxvt
from version import __version__, DEBUG
import pkg_resources
RSRC_FILE = pkg_resources.resource_filename(__name__, 'mtrax.xrc')
import algorithm as alg, bg, draw, ellipsesk as ell

class AppWithSettings(wx.App):
    """Cannot be used alone -- this class only exists
    to keep settings GUI code together in one file."""

    def InitGUI(self):
        """Load XML resources, create handles, bind callbacks."""
        rsrc = xrc.XmlResource(RSRC_FILE)
        self.frame = rsrc.LoadFrame(None, 'frame_mtrax')
        plat = sys.platform
        if not plat.startswith('win'):
            self.frame.SetIcon(wx.Icon(pkg_resources.resource_filename(__name__, 'mtraxicon.ico'), wx.BITMAP_TYPE_ICO))
        self.menu = self.frame.GetMenuBar()
        if DEBUG:
            self.menu.Append(wx.Menu(), 'DEBUG')
        self.status = xrc.XRCCTRL(self.frame, 'bar_status')
        self.framenumber_text = xrc.XRCCTRL(self.frame, 'text_framenumber')
        self.num_flies_text = xrc.XRCCTRL(self.frame, 'text_num_flies')
        self.rate_text = xrc.XRCCTRL(self.frame, 'text_refresh_rate')
        self.slider = xrc.XRCCTRL(self.frame, 'slider_frame')
        self.slider.Enable(False)
        self.img_panel = xrc.XRCCTRL(self.frame, 'panel_img')
        box = wx.BoxSizer(wx.VERTICAL)
        self.img_panel.SetSizer(box)
        self.img_wind = wxvideo.DynamicImageCanvas(self.img_panel, -1)
        box.Add(self.img_wind, 1, wx.EXPAND)
        self.img_panel.SetAutoLayout(True)
        self.img_panel.Layout()
        self.zoommode = False
        self.toolbar = xrc.XRCCTRL(self.frame, 'toolbar')
        self.zoom_id = xrc.XRCID('zoom')
        self.play_id = xrc.XRCID('play')
        self.stop_id = xrc.XRCID('stop')
        self.speedup_id = xrc.XRCID('speed_up')
        self.slowdown_id = xrc.XRCID('slow_down')
        self.refresh_id = xrc.XRCID('refresh')
        self.toolbar.SetToggle(self.zoommode, self.zoom_id)
        self.stop_tracking_tooltip = 'Stop Tracking'
        self.stop_playback_tooltip = 'Stop Video Playback'
        self.start_playback_tooltip = 'Start Video Playback'
        self.speedup_tracking_tooltip = 'Increase Refresh Rate'
        self.speedup_playback_tooltip = 'Increase Playback Speed'
        self.slowdown_tracking_tooltip = 'Decrease Refresh Rate'
        self.slowdown_playback_tooltip = 'Decrease Playback Speed'
        self.play_speed = 1.0
        self.UpdateToolBar('stopped')
        self.frame.Bind(wx.EVT_MENU, self.OnOpen, id=xrc.XRCID('menu_file_open'))
        self.frame.Bind(wx.EVT_MENU, self.OnLoadSettings, id=xrc.XRCID('menu_load_settings'))
        self.frame.Bind(wx.EVT_MENU, self.OnBatch, id=xrc.XRCID('menu_file_batch'))
        self.frame.Bind(wx.EVT_MENU, self.OnSave, id=xrc.XRCID('menu_file_export'))
        self.frame.Bind(wx.EVT_MENU, self.OnSaveTimestamps, id=xrc.XRCID('menu_file_write_timestamps'))
        self.frame.Bind(wx.EVT_MENU, self.OnSaveAvi, id=xrc.XRCID('menu_file_save_avi'))
        self.frame.Bind(wx.EVT_MENU, self.OnQuit, id=xrc.XRCID('menu_file_quit'))
        self.frame.Bind(wx.EVT_MENU, self.OnHelp, id=xrc.XRCID('menu_help_help'))
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id=xrc.XRCID('menu_help_about'))
        self.frame.Bind(wx.EVT_MENU, self.OnStartTrackingMenu, id=xrc.XRCID('menu_track_start'))
        self.frame.Bind(wx.EVT_MENU, self.OnStartTrackingMenu, id=xrc.XRCID('menu_track_resume'))
        self.frame.Bind(wx.EVT_MENU, self.OnStartTrackingMenu, id=xrc.XRCID('menu_track_resume_here'))
        self.frame.Bind(wx.EVT_MENU, self.OnWriteSBFMF, id=xrc.XRCID('menu_track_writesbfmf'))
        self.frame.Bind(wx.EVT_MENU, self.OnComputeBg, id=xrc.XRCID('menu_compute_background'))
        self.frame.Bind(wx.EVT_MENU, self.OnComputeShape, id=xrc.XRCID('menu_compute_shape'))
        self.frame.Bind(wx.EVT_MENU, self.OnSettingsBGModel, id=xrc.XRCID('menu_settings_bg_model'))
        self.frame.Bind(wx.EVT_MENU, self.OnSettingsBG, id=xrc.XRCID('menu_settings_bg'))
        self.frame.Bind(wx.EVT_MENU, self.OnSettingsTracking, id=xrc.XRCID('menu_settings_tracking'))
        self.frame.Bind(wx.EVT_MENU, self.OnChooseOrientations, id=xrc.XRCID('menu_choose_orientations'))
        self.frame.Bind(wx.EVT_MENU, self.OnCheckShowAnn, id=xrc.XRCID('menu_playback_show_ann'))
        self.frame.Bind(wx.EVT_MENU, self.OnCheckRefresh, id=xrc.XRCID('menu_do_refresh'))
        self.frame.Bind(wx.EVT_MENU, self.OnTailLength, id=xrc.XRCID('menu_playback_tails'))
        self.frame.Bind(wx.EVT_MENU, self.OnCheckDim, id=xrc.XRCID('menu_playback_dim'))
        self.frame.Bind(wx.EVT_MENU, self.OnCheckZoom, id=xrc.XRCID('menu_settings_zoom'))
        self.frame.Bind(wx.EVT_MENU, self.OnStats, id=xrc.XRCID('menu_stats_vel'))
        self.frame.Bind(wx.EVT_MENU, self.OnStats, id=xrc.XRCID('menu_stats_orn'))
        self.frame.Bind(wx.EVT_MENU, self.OnStats, id=xrc.XRCID('menu_stats_space'))
        self.frame.Bind(wx.EVT_MENU, self.OnStats, id=xrc.XRCID('menu_stats_pos'))
        self.frame.Bind(wx.EVT_MENU, self.OnSettingsStats, id=xrc.XRCID('menu_stats_settings'))
        self.frame.Bind(wx.EVT_MENU, self.OnCheckBatchStats, id=xrc.XRCID('menu_stats_batch'))
        self.frame.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.frame.Bind(wx.EVT_SCROLL, self.OnSlider, self.slider)
        self.frame.Bind(wx.EVT_SIZE, self.OnResize)
        self.frame.Bind(wx.EVT_MAXIMIZE, self.OnResize)
        self.frame.Bind(wx.EVT_TOOL, self.ZoomToggle, id=self.zoom_id)
        self.frame.Bind(wx.EVT_TOOL, self.OnPlayButton, id=self.play_id)
        self.frame.Bind(wx.EVT_TOOL, self.OnStopButton, id=self.stop_id)
        self.frame.Bind(wx.EVT_TOOL, self.OnSpeedUpButton, id=self.speedup_id)
        self.frame.Bind(wx.EVT_TOOL, self.OnSlowDownButton, id=self.slowdown_id)
        self.frame.Bind(wx.EVT_TOOL, self.OnRefreshButton, id=self.refresh_id)
        wxvt.setup_validated_integer_callback(self.framenumber_text, xrc.XRCID('text_framenumber'), self.OnFrameNumberValidated, pending_color=params.status_blue)
        if sys.platform == 'win32':
            homedir = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
        else:
            homedir = os.environ['HOME']
        self.dir = homedir
        self.ellipse_thickness = params.ellipse_thickness
        self.ReadUserfile()
        self.OnResize(None)
        return

    def InitState(self):
        self.start_frame = 0
        self.tracking = False
        self.batch = None
        self.batch_data = None
        self.bg_window_open = False
        params.batch_executing = False
        params.framesbetweenrefresh = 1
        self.dowritesbfmf = False
        return

    def SetPlayToolTip(self, s):
        self.toolbar.SetToolShortHelp(self.play_id, s)

    def SetStopToolTip(self, s):
        self.toolbar.SetToolShortHelp(self.stop_id, s)

    def SetSpeedUpToolTip(self, s):
        self.toolbar.SetToolShortHelp(self.speedup_id, s)

    def SetSlowDownToolTip(self, s):
        self.toolbar.SetToolShortHelp(self.slowdown_id, s)

    def EnableRefreshBitmap(self, state):
        self.toolbar.EnableTool(self.refresh_id, state)

    def EnablePlayBitmap(self, state):
        self.toolbar.EnableTool(self.play_id, state)

    def EnableStopBitmap(self, state):
        self.toolbar.EnableTool(self.stop_id, state)

    def UpdateToolBar(self, state):
        if state == 'stopped':
            self.EnablePlayBitmap(True)
            self.SetPlayToolTip(self.start_playback_tooltip)
            self.EnableStopBitmap(False)
            self.SetSpeedUpToolTip(self.speedup_playback_tooltip)
            self.SetSlowDownToolTip(self.slowdown_playback_tooltip)
            self.EnableRefreshBitmap(False)
            self.rate_text.SetValue('Play Speed: %.1f fps' % self.play_speed)
        else:
            self.EnableStopBitmap(True)
            self.EnablePlayBitmap(False)
            if self.tracking:
                self.SetStopToolTip(self.stop_tracking_tooltip)
                self.SetSpeedUpToolTip(self.speedup_tracking_tooltip)
                self.SetSlowDownToolTip(self.slowdown_tracking_tooltip)
                self.EnableRefreshBitmap(True)
                if params.do_refresh:
                    self.rate_text.SetValue('Refresh Period: %02d fr' % params.framesbetweenrefresh)
                else:
                    self.rate_text.SetValue('Refresh Rate: Never')
            else:
                self.SetStopToolTip(self.stop_playback_tooltip)
                self.SetSpeedUpToolTip(self.speedup_playback_tooltip)
                self.SetSlowDownToolTip(self.slowdown_playback_tooltip)
                self.EnableRefreshBitmap(False)
                self.rate_text.SetValue('Play Speed: %.1f fps' % self.play_speed)

    def ReadUserfile(self):
        """Read user settings from file. Set window size, location.
        Called on startup."""
        try:
            if sys.platform[:3] == 'win':
                homedir = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
            else:
                homedir = os.environ['HOME']
            self.userfile_name = os.path.join(homedir, '.mtraxrc')
            userfile = open(self.userfile_name, 'r')
            last_version = userfile.readline().rstrip()
            if last_version != __version__:
                wx.MessageBox('Welcome to Mtrax version %s' % __version__, 'Mtrax updated', wx.ICON_INFORMATION)
            self.dir = userfile.readline().rstrip()
            (last_pos, last_size) = str222tuples(userfile.readline().rstrip())
            self.frame.SetPosition(last_pos)
            self.frame.SetSize(last_size)
            try:
                (self.last_bg_pos, self.last_bg_size) = str222tuples(userfile.readline().rstrip())
            except (ValueError, IndexError):
                self.last_bg_pos = None
                self.last_bg_size = None

            try:
                (self.last_batch_pos, self.last_batch_size) = str222tuples(userfile.readline().rstrip())
            except (ValueError, IndexError):
                self.last_batch_pos = None
                self.last_batch_size = None

            use_cb = userfile.readline().rstrip()
            use_et = userfile.readline().rstrip()
            if use_et.isdigit():
                self.ellipse_thickness = int(use_et)
            use_tl = userfile.readline().rstrip()
            if use_tl.isdigit():
                params.tail_length = int(use_tl)
            use_di = userfile.readline().rstrip()
            if use_di == 'True':
                self.menu.Check(xrc.XRCID('menu_playback_dim'), True)
            self.save_dir = userfile.readline().rstrip()
            draw.const.save_dir = self.save_dir
            try:
                (self.last_zoom_pos, self.last_zoom_size) = str222tuples(userfile.readline().rstrip())
            except (ValueError, IndexError):
                self.last_zoom_pos = None
                self.last_zoom_size = None

            userfile.close()
        except:
            if not hasattr(self, 'last_bg_pos'):
                self.last_bg_pos = None
                self.last_bg_size = None
            if not hasattr(self, 'last_batch_pos'):
                self.last_batch_pos = None
                self.last_batch_size = None
            if not hasattr(self, 'save_dir'):
                if hasattr(self, 'dir'):
                    self.save_dir = self.dir
                else:
                    self.save_dir = os.environ['HOME']
            if not hasattr(self, 'last_zoom_pos'):
                self.last_zoom_pos = None
                self.last_zoom_size = None

        return

    def WriteUserfile(self):
        """Write current user settings to file. Called on quit."""
        try:
            userfile = open(self.userfile_name, 'w')
        except IOError:
            pass
        else:
            print >> userfile, __version__
            print >> userfile, self.dir
            print >> userfile, self.frame.GetPosition(), self.frame.GetSize()
            if self.last_bg_pos is not None:
                print >> userfile, self.last_bg_pos, self.last_bg_size
            else:
                print >> userfile, ''
            if self.last_batch_pos is not None:
                print >> userfile, self.last_batch_pos, self.last_batch_size
            else:
                print >> userfile, ''
            print >> userfile, False
            print >> userfile, self.ellipse_thickness
            print >> userfile, params.tail_length
            print >> userfile, self.menu.IsChecked(xrc.XRCID('menu_playback_dim'))
            print >> userfile, self.save_dir
            if self.last_zoom_pos is not None:
                print >> userfile, self.last_zoom_pos, self.last_zoom_size
            else:
                print >> userfile, ''
            userfile.close()

        return

    def OnFrameNumberValidated(self, evt):
        new_frame = int(self.framenumber_text.GetValue())
        if new_frame < 0:
            new_frame = 0
        elif new_frame >= self.n_frames:
            new_frame = self.n_frames - 1
        self.start_frame = new_frame
        self.ShowCurrentFrame()

    def OnSettingsBG(self, evt):
        """Open window for bg threshold settings."""
        if self.bg_window_open:
            self.bg_imgs.frame.Raise()
            return
        if self.ann_file is not None:
            old_thresh = params.n_bg_std_thresh
        else:
            old_thresh = None
        isbgmodel = self.CheckForBGModel()
        if isbgmodel == False:
            return
        self.bg_imgs.ShowBG(self.frame, self.start_frame, old_thresh)
        self.bg_imgs.frame.Bind(wx.EVT_SIZE, self.OnResizeBG)
        self.bg_imgs.frame.Bind(wx.EVT_MOVE, self.OnResizeBG)
        self.bg_imgs.frame.Bind(wx.EVT_MENU, self.OnQuitBG, id=xrc.XRCID('menu_window_close'))
        self.bg_imgs.frame.Bind(wx.EVT_CLOSE, self.OnQuitBG)
        self.bg_imgs.frame.Bind(wx.EVT_BUTTON, self.OnQuitBG, id=xrc.XRCID('done_button'))
        if self.last_bg_pos is not None:
            self.bg_imgs.frame.SetPosition(self.last_bg_pos)
            self.bg_imgs.frame.SetSize(self.last_bg_size)
        self.bg_imgs.OnThreshSlider(None)
        self.bg_imgs.OnFrameSlider(None)
        self.bg_imgs.frame.Show()
        self.bg_window_open = True
        self.bg_imgs.DoSub()
        self.bg_imgs.frame_slider.SetMinSize(wx.Size(self.bg_imgs.img_panel.GetRect().GetWidth(), self.bg_imgs.frame_slider.GetRect().GetHeight()))
        return

    def OnSettingsBGModel(self, evt):
        """Open window for bg model settings."""
        if not hasattr(self.bg_imgs, 'modeldlg'):
            self.bg_imgs.modeldlg = bg.BgSettingsDialog(self.frame, self.bg_imgs)
            self.bg_imgs.modeldlg.frame.Bind(wx.EVT_CLOSE, self.OnQuitBGModel)
            self.bg_imgs.modeldlg.frame.Bind(wx.EVT_BUTTON, self.OnQuitBGModel, id=xrc.XRCID('done_button'))
        else:
            self.bg_imgs.modeldlg.frame.Raise()

    def OnSettingsTracking(self, evt):
        """Open window for bg model settings."""
        if hasattr(self, 'tracking_settings_window_open') and self.tracking_settings_window_open:
            self.tracking_settings.frame.Raise()
            return
        isbgmodel = self.CheckForBGModel()
        if isbgmodel == False:
            return
        self.tracking_settings = tracking_settings.TrackingSettings(self.frame, self.bg_imgs, self.start_frame)
        self.tracking_settings.frame.Bind(wx.EVT_CLOSE, self.OnQuitTrackingSettings)
        self.tracking_settings.frame.Bind(wx.EVT_BUTTON, self.OnQuitTrackingSettings, id=xrc.XRCID('done'))
        self.tracking_settings.frame.Show()
        self.tracking_settings_window_open = True

    def OnChooseOrientations(self, evt):
        """Open window for bg model settings."""
        if hasattr(self, 'choose_orientations_window_open') and self.choose_orientations_window_open:
            self.choose_orientations.frame.Raise()
            return
        self.choose_orientations = chooseorientations.ChooseOrientations(self.frame, self.ann_data)
        self.choose_orientations.frame.Bind(wx.EVT_CLOSE, self.OnQuitChooseOrientations)
        self.choose_orientations.frame.Bind(wx.EVT_BUTTON, self.OnQuitChooseOrientations, id=xrc.XRCID('ID_CANCEL'))
        self.choose_orientations.frame.Bind(wx.EVT_BUTTON, self.ChooseOrientations, id=xrc.XRCID('ID_OK'))
        self.choose_orientations.frame.Show()
        self.choose_orientations_window_open = True

    def OnQuitBGModel(self, evt):
        self.bg_imgs.modeldlg.frame.Destroy()
        delattr(self.bg_imgs, 'modeldlg')

    def OnQuitTrackingSettings(self, evt):
        print 'in OnQuitTrackingSettings'
        self.tracking_settings.frame.Destroy()
        print 'destroyed frame'
        delattr(self, 'tracking_settings')
        self.tracking_settings_window_open = False
        print 'done'

    def OnQuitChooseOrientations(self, evt):
        self.choose_orientations.frame.Destroy()
        delattr(self, 'choose_orientations')
        self.choose_orientations_window_open = False
        self.RewriteTracks()

    def ChooseOrientations(self, evt):
        self.choose_orientations.ChooseOrientations()
        self.OnQuitChooseOrientations(evt)

    def OnResizeBG(self, evt):
        """BG window was moved or resized. Rescale image and slider,
        and remember new location."""
        if evt is not None:
            evt.Skip()
        self.bg_imgs.frame.Layout()
        try:
            self.bg_imgs.DoDraw()
            self.bg_imgs.frame_slider.SetMinSize(wx.Size(self.bg_imgs.img_panel.GetRect().GetWidth(), self.bg_imgs.frame_slider.GetRect().GetHeight()))
            self.last_bg_size = self.bg_imgs.frame.GetSize()
            self.last_bg_pos = self.bg_imgs.frame.GetPosition()
        except AttributeError:
            pass

        return

    def OnQuitBG(self, evt):
        """Take data from bg threshold window and close it."""
        self.bg_window_open = False
        self.bg_imgs.hf.frame.Destroy()
        self.bg_imgs.frame.Destroy()

    def OnCheckZoom(self, evt):
        """Open ellipse zoom window."""
        if self.menu.IsChecked(xrc.XRCID('menu_settings_zoom')):
            self.zoom_window = ell.EllipseFrame(self.frame)
            self.zoom_window.frame.Bind(wx.EVT_CLOSE, self.OnCloseZoom)
            self.zoom_window.frame.Bind(wx.EVT_SIZE, self.OnZoomResize)
            self.zoom_window.frame.Bind(wx.EVT_MOVE, self.OnZoomMove)
            if self.last_zoom_pos is not None:
                self.zoom_window.frame.SetPosition(self.last_zoom_pos)
                self.zoom_window.frame.SetSize(self.last_zoom_size)
            if evt is not None:
                self.ShowCurrentFrame()
        else:
            self.OnCloseZoom(None)
        return

    def OnZoomResize(self, evt):
        """Zoom window was resized; remember position and redraw."""
        evt.Skip()
        self.zoom_window.Redraw()
        try:
            self.last_zoom_size = self.zoom_window.frame.GetSize()
            self.last_zoom_pos = self.zoom_window.frame.GetPosition()
        except AttributeError:
            pass

    def OnZoomMove(self, evt):
        """Zoom window moved; remember position."""
        evt.Skip()
        try:
            self.last_zoom_size = self.zoom_window.frame.GetSize()
            self.last_zoom_pos = self.zoom_window.frame.GetPosition()
        except AttributeError:
            pass

    def OnCloseZoom(self, evt):
        """Close ellipse zoom window."""
        self.menu.Check(xrc.XRCID('menu_settings_zoom'), False)
        self.zoom_window.frame.Destroy()

    def ZoomToggle(self, evt):
        self.zoommode = self.zoommode == False

    def MouseClick(self, evt):
        if not self.zoommode:
            return
        if self.ann_data is None:
            return
        windowheight = self.img_wind_child.GetRect().GetHeight()
        windowwidth = self.img_wind_child.GetRect().GetWidth()
        x = evt.GetX() * self.img_size[1] / windowwidth
        y = self.img_size[0] - evt.GetY() * self.img_size[0] / windowheight
        if x > self.img_size[1] or y > self.img_size[0]:
            return
        mind = num.inf
        drawframe = self.start_frame - params.start_frame
        if drawframe >= len(self.ann_data):
            drawframe = -1
        for (i, v) in self.ann_data[drawframe].iteritems():
            d = (v.center.x - x) ** 2 + (v.center.y - y) ** 2
            if d <= mind:
                mini = i
                mind = d

        maxdshowinfo = (num.maximum(params.movie_size[0], params.movie_size[1]) / params.MAXDSHOWINFO) ** 2
        if mind < maxdshowinfo:
            window = None
            if not self.menu.IsChecked(xrc.XRCID('menu_settings_zoom')):
                self.menu.Check(xrc.XRCID('menu_settings_zoom'), True)
                self.OnCheckZoom(evt)
                window = 0
            self.ZoomTarget(self.ann_data[drawframe][mini], window)
        return

    def ZoomTarget(self, targ, window):
        nwindows = self.zoom_window.n_ell
        for i in range(nwindows):
            if targ.identity == self.zoom_window.ellipse_windows[i].spinner.GetValue():
                return

        maxnwindows = self.zoom_window.n_ell_spinner.GetMax()
        if window is None:
            if nwindows < maxnwindows:
                self.zoom_window.AddEllipseWindow(targ.identity)
            else:
                if hasattr(self, 'firstzoomwindowcreated'):
                    window = self.firstzoomwindowcreated
                    self.firstzoomwindowcreated = (self.firstzoomwindowcreated + 1) % maxnwindows
                else:
                    window = 0
                    self.firstzoomwindowcreated = 1 % maxnwindows
                self.zoom_window.ellipse_windows[window].spinner.SetValue(targ.identity)
                self.zoom_window.ellipse_windows[window].redraw()
        else:
            self.zoom_window.ellipse_windows[window].spinner.SetValue(targ.identity)
            self.zoom_window.ellipse_windows[window].redraw()
        return

    def OnSettingsStats(self, evt):
        """Open statistics settings dialog."""
        if not hasattr(self, 'draw_dialog'):
            self.draw_dialog = draw.DrawSettingsDialog(self.frame)
            self.draw_dialog.frame.Bind(wx.EVT_CLOSE, self.OnQuitSettings)
        else:
            self.draw_dialog.frame.Raise()

    def OnQuitSettings(self, evt):
        """Close stats settings dialog and enable a new one to be opened."""
        self.draw_dialog.frame.Destroy()
        delattr(self, 'draw_dialog')

    def OnCheckDim(self, evt):
        self.ShowCurrentFrame()

    def OnTailLength(self, evt):
        try:
            dlg = wx.NumberEntryDialog(self.frame, 'Enter new tail length', '(0-200 frames)', 'Tail Length', value=params.tail_length, min=0, max=200)
            if dlg.ShowModal() == wx.ID_OK:
                params.tail_length = dlg.GetValue()
            dlg.Destroy()
        except AttributeError:
            import warnings
            warnings.filterwarnings('ignore', '', DeprecationWarning)
            new_num = wx.GetNumberFromUser('Enter new tail length', '(0-200 frames)', 'Tail Length', params.tail_length, min=0, max=200, parent=self.frame)
            warnings.resetwarnings()
            if new_num >= 0:
                params.tail_length = new_num

        self.ShowCurrentFrame()

    def IsBGModel(self):
        return hasattr(self.bg_imgs, 'center')

    def CheckForBGModel(self):
        if hasattr(self.bg_imgs, 'center'):
            return True
        if params.interactive == False:
            self.bg_imgs.est_bg()
            return True
        if params.use_median:
            algtxt = 'Median'
        else:
            algtxt = 'Mean'
        msgtxt = 'Background model has not been calculated.\nCalculate now using the following parameters?\n\nAlgorithm: %s\nNumber of Frames: %d' % (algtxt, params.n_bg_frames)
        if wx.MessageBox(msgtxt, 'Calculate?', wx.OK | wx.CANCEL) == wx.CANCEL:
            return False
        if self.status is not None:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_green)
            self.status.SetStatusText('calculating background', params.status_box)
        wx.BeginBusyCursor()
        wx.Yield()
        self.bg_imgs.est_bg()
        if self.status is not None:
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
        wx.EndBusyCursor()
        return True

    def CheckForShapeModel(self):
        if params.have_computed_shape:
            return True
        haveshape = num.isinf(params.maxshape.area) == False
        if params.movie_name == params.annotation_movie_name and haveshape:
            return True
        if params.interactive == False:
            ell.est_shape(self.bg_imgs)
            return True
        if haveshape:
            msgtxt = 'Shape model has not been automatically computed for this movie. Currently:\n\nMin Area = %.2f\nMax Area = %.2f\n\nDo you want to automatically compute now with the following parameters?\n\nNumber of Frames: %d\nNumber of Standard Deviations: %.2f' % (params.minshape.area, params.maxshape.area, params.n_frames_size, params.n_std_thresh)
        else:
            msgtxt = 'Shape is currently unbounded. Do you want to automatically compute now with the following parameters?\n\nNumber of Frames: %d\nNumber of Standard Deviations: %.2f' % (params.n_frames_size, params.n_std_thresh)
        resp = wx.MessageBox(msgtxt, 'Calculate?', wx.YES_NO | wx.CANCEL)
        if resp == wx.NO:
            return True
        elif resp == wx.CANCEL:
            return False
        if self.status is not None:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_blue)
            self.status.SetStatusText('calculating shape', params.status_box)
        wx.BeginBusyCursor()
        wx.Yield()
        ell.est_shape(self.bg_imgs)
        if self.status is not None:
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
        wx.EndBusyCursor()
        return True


def str222tuples(string):
    """Converts string into two 2-tuples."""
    vals = string.split()
    for vv in range(len(vals)):
        vals[vv] = int(vals[vv].strip('(), '))

    return (
     (
      vals[0], vals[1]), (vals[2], vals[3]))


def str22tuple(string):
    """Converts string into a 2-tuple."""
    vals = string.split()
    for vv in range(len(vals)):
        vals[vv] = int(vals[vv].strip('(), '))

    return (
     vals[0], vals[1])
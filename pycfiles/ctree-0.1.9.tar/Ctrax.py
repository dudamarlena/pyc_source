# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/Ctrax.py
# Compiled at: 2016-09-17 17:03:38
import os, platform, sys, time, wx
from wx import xrc
import numpy as num
num.seterr(invalid='raise')
num.seterr(divide='raise')
num.seterr(over='warn')
num.seterr(under='ignore')
from scipy.misc import imresize
from matplotlib import __version__ as mpl_version
try:
    from psutil import __version__ as psutil_version
except ImportError:
    psutil_version = '-not found-'

from cv2 import __version__ as opencv_version
from version import __version__, DEBUG, DEBUG_REPEATABLE_BEHAVIOR
import annfiles as annot, batch, bg, algorithm, draw, imagesk, movies, ellipsesk as ell
from params import params, const
if DEBUG:
    import pdb

class CtraxApp(algorithm.CtraxAlgorithm):

    def has(self, attr):
        return hasattr(self, attr) and getattr(self, attr) is not None

    def OnInit(self):
        """
        Start up the Ctrax GUI
        """
        self.InitState()
        self.ParseCommandLine()
        self.InitGUI()
        self.ReadUserfile()
        self.frame.Show()
        self.alive = True
        params.app_instance = self
        if params.interactive:
            print '********** Ctrax Warning and Error Messages **********'
            print 'Error and warning messages will appear in this window.'
            print 'If you have trouble and are contacting the Ctrax mailing'
            print 'list (see http://groups.google.com/group/ctrax ), be'
            print 'sure to copy and paste the relevant messages from this'
            print 'window into your email.'
            print '*********************** Ctrax ************************\n'
            print 'system version', platform.platform()
            print 'Python version', sys.version
            print 'Wx version', wx.__version__
            print 'OpenCV version', opencv_version
            print 'Matplotlib version', mpl_version
            print 'psutil version', psutil_version
            print 'Ctrax version', __version__
        self.OpenMovie(new_movie=False)
        return True

    def PrintUsage(self):
        """
        Print command line arguments for Ctrax.
        """
        self.RestoreStdio()
        print 'Ctrax:\nOptional Command Line Arguments:\n--Interactive={True,False}\n--Output=<movie.fmf.ann>\n--Input=<movie.fmf>\n--SettingsFile=<settings.ann>\n--AutoEstimateBackground={True,False}\n--AutoEstimateShape={True,False}\n--AutoDetectCircularArena={True,False}\n--CompressMovie=<movie.sbfmf>\n--MatFile=<movie.mat>\n--CsvFile=<movie.csv>\n--DiagnosticsFile=<movie_ctraxdiagnostics.txt>\n--FirstFrameTrack={0,1,...}\n--LastFrameTrack={-1,0,1,...}\n--ResumeTracking={False,True}\n--FlipMovieUD={False,True}\n--EnforceShapeBounds={True,False}\n\nExample:\nCtrax --Interactive=True --Input=movie1.fmf \\\n  --Output=movie1.fmf.ann \\\n  --SettingsFile=exp1.ann \\\n  --MatFile=movie1.mat \\\n  --DiagnosticsFile=movie1_ctraxdiagnostics.txt\n\nBy default, Interactive=True, AutoEstimateBackground=True,\nAutoEstimateShape=True, AutoDetectCircularArena=True,\nFirstFrameTrack=0, LastFrameTrack=-1\n(meaning to track until the end of the video),\nResumeTracking=False, FlipMovieUD=False\n\nIf not in interactive mode, then Input must be defined.\n\nIf Input is movie1.fmf and Output is not defined, then output\nand settings will go to movie1.fmf.ann in non-interactive mode.\n\nExisting annotation files are always backed up before being\noverwritten, as long as the user has the appropriate\npermissions to the output directory.\n\nIf CompressMovie is not set, then a compressed SBFMF will not\nbe created.\n\nIf MatFile is not set, then <basename>.mat will be used,\nwhere <basename> is the base name of the movie.\n\nIf CsvFile is not set, no CSV output will be exported.\n\nIf DiagnosticsFile is not set, then\n<basename>_ctraxdiagnostics.txt will be used.\n'

    def ParseCommandLine(self):
        """
        Interpret command line arguments.
        """
        args = sys.argv[1:]
        self.movie = None
        self.ann_filename = None
        self.start_frame = 0
        self.last_frame = num.inf
        self.dowritesbfmf = False
        self.input_file_was_specified = False
        self.output_file_was_specified = False
        if len(args) == 1:
            if args[0] == '--help':
                self.PrintUsage()
                sys.exit(1)
            elif args[0].startswith('-psn_'):
                args = []
            elif '=' not in args[0]:
                args = ['--input=%s' % args[0]]
        for arg in args:
            if arg.lower() == '--interactive=false':
                params.interactive = False
                params.enable_feedback(False)
                self.RestoreStdio()

        for i in range(len(args)):
            try:
                name, value = args[i].split('=', 1)
            except:
                print 'Error parsing command line arguments. No equals sign found. Usage: '
                self.PrintUsage()
                raise NotImplementedError

            if name.lower() == '--interactive':
                continue
            elif name.lower() == '--input':
                if hasattr(self, 'frame'):
                    openframe = self.frame
                else:
                    openframe = None
                self.movie = movies.Movie(value, interactive=params.interactive, parentframe=openframe, open_now=True)
                self.input_file_was_specified = True
            elif name.lower() == '--output':
                self.ann_filename = value
                self.output_file_was_specified = True
            elif name.lower() == '--settingsfile':
                self.settingsfilename = value
                print 'settingsfile = ' + str(self.settingsfilename)
            elif name.lower() == '--autoestimatebackground':
                if value.lower() == 'false':
                    params.batch_autodetect_bg_model = False
            elif name.lower() == '--autoestimateshape':
                if value.lower() == 'false':
                    params.batch_autodetect_shape = False
            elif name.lower() == '--autodetectcirculararena':
                if value.lower() == 'false':
                    params.batch_autodetect_arena = False
                elif value.lower() == 'none':
                    params.batch_autodetect_arena = None
            elif name.lower() == '--compressmovie':
                self.writesbfmf_filename = value
                self.dowritesbfmf = True
            elif name.lower() == '--matfile':
                self.matfilename = value
            elif name.lower() == '--csvfile':
                self.csvfilename = value
            elif name.lower() == '--diagnosticsfile':
                self.diagnostics_filename = value
            elif name.lower() == '--firstframetrack':
                try:
                    start_frame = float(value)
                    if start_frame < 0 or round(start_frame) != start_frame:
                        raise NotImplementedError
                except:
                    print 'FirstFrameTrack must be an integer greater than or equal to 0'
                    self.PrintUsage()
                    raise

                self.start_frame = int(start_frame)
                print 'setting params.start_frame = ' + str(int(start_frame))
                params.start_frame = int(start_frame)
            elif name.lower() == '--lastframetrack':
                try:
                    last_frame = float(value)
                    if round(last_frame) != last_frame:
                        raise NotImplementedError
                    if last_frame < 0:
                        last_frame = num.inf
                except:
                    print 'LastFrameTrack must be an integer'
                    self.PrintUsage()
                    raise

                self.last_frame = last_frame
            elif name.lower() == '--resumetracking':
                if value.lower() == 'true':
                    params.noninteractive_resume_tracking = True
            elif name.lower() == '--flipmovieud':
                if value.lower() == 'true':
                    params.movie_flipud = True
            elif name.lower() == '--enforceshapebounds':
                if value.lower() == 'false':
                    params.enforce_minmax_shape = False
            else:
                print 'Error parsing command line arguments. Unknown parameter name "%s". Usage: ' % name
                self.PrintUsage()
                raise NotImplementedError

        if self.start_frame > self.last_frame:
            print 'FirstFrameTrack must be <= LastFrameTrack'
            self.PrintUsage()
            raise NotImplementedError
        if params.noninteractive_resume_tracking:
            if not self.output_file_was_specified or self.ann_filename is None or not os.path.isfile(self.ann_filename):
                print 'To resume tracking, an existing output file must be specified.'
                raise NotImplementedError
        if params.interactive == False:
            self.run_noninteractive()
            sys.exit(0)
        return

    def run_noninteractive(self):
        """
        Run Ctrax in non-interactive mode.
        """
        starttime = time.time()
        self.frame = None
        if not self.has('movie'):
            print 'Error parsing command line arguments.\n            Input file must be specified in non-interactive mode.\n            Usage: '
            self.PrintUsage()
            raise NotImplementedError
        if not self.has('ann_filename'):
            self.ann_filename = self.get_filename_with_extension('+.ann')
        if self.has('ann_filename'):
            print 'ann_filename = ' + str(self.ann_filename)
        if not self.has('settingsfilename'):
            self.settingsfilename = self.ann_filename
        print 'Opening movie ' + self.movie.filename
        self.OpenMovie(new_movie=False)
        if not self.has('movie'):
            print 'failed opening movie!'
            sys.exit(1)
        params.start_frame = self.start_frame
        self.do_refresh = True
        if not self.has('diagnostics_filename'):
            self.diagnostics_filename = self.get_filename_with_extension('_ctraxdiagnostics.txt')
        print 'Diagnostics info will be written to ' + self.diagnostics_filename
        print 'DoAll...'
        self.DoAll()
        print 'process completed in', time.time() - starttime, 's'
        return

    def LoadSettings(self):
        """
        Load parameter values from another annotation file.
        """
        doreadbgmodel = not (params.interactive or self.IsBGModel())
        if doreadbgmodel and self.has('movie'):
            bg_img_shape = (
             self.movie.get_height(), self.movie.get_width())
        else:
            bg_img_shape = None
        print 'loading settings from file ' + self.settingsfilename
        print 'reading bg?', doreadbgmodel, '-',
        if not doreadbgmodel:
            if params.interactive:
                print 'in interactive mode'
            elif self.IsBGModel():
                print 'bg model exists'
            else:
                print '??'
        try:
            annot.LoadSettings(self.settingsfilename, self.bg_imgs, bg_img_shape=bg_img_shape, readbgmodel=doreadbgmodel)
        except:
            print 'Could not read annotation file ' + self.settingsfilename
            raise

        return

    def MacOpenFile(self, filename):
        """Fires when a compatible file is dropped onto the app on Mac."""
        self.movie = movies.Movie(filename, interactive=params.interactive, parentframe=self.frame, open_now=True)
        self.OpenMovie(new_movie=False)

    def OpenMovie(self, new_movie=True):
        """Attempt to open a movie given the current filename."""
        if new_movie:
            try:
                self.movie = movies.Movie(self.dir, params.interactive, default_extension=self.last_movie_ext)
                if DEBUG:
                    print 'Opened movie ' + str(self.movie.filename)
            except ImportError:
                return
            except Exception as details:
                raise
                if self.has('movie'):
                    if params.interactive:
                        wx.MessageBox('Could not open the movie ' + self.movie.filename, 'Error', wx.ICON_ERROR | wx.OK)
                    else:
                        print 'Could not open the movie ' + self.movie.filename
                    print details
                    self.movie = None
                    self.ShowCurrentFrame()
                self.start_frame = 0
                return

        if not self.has('movie'):
            return
        else:
            if new_movie:
                self.start_frame = 0
            if self.has('bg_imgs'):
                self.OnQuitBGModel(None)
            if self.bg_window_open:
                self.OnQuitBG(None)
            if self.tracking_settings_window_open:
                self.OnQuitTrackingSettings(None)
            if self.choose_orientations_window_open:
                self.OnQuitChooseOrientations(None)
            if self.has('wizard'):
                self.OnQuitTrackingWizard(None)
            params.movie_name = self.movie.filename
            self.dir = self.movie.dirname
            draw.const.filepath = self.movie.fullpath
            base, self.last_movie_ext = os.path.splitext(self.movie.filename)
            self.img_size = [
             self.movie.get_height(), self.movie.get_width()]
            if params.interactive:
                self.reset_img_wind()
                img = num.zeros((self.img_size[0], self.img_size[1]), dtype=num.uint8)
                sys.stdout.flush()
                self.img_wind.update_image_and_drawings('Ctraxmain', img, format='MONO8')
                sys.stdout.flush()
                self.img_wind_child = self.img_wind.get_child_canvas('Ctraxmain')
                self.img_wind_child.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
                self.img_wind_child.Bind(wx.EVT_MOTION, self.OnMouseMoved)
                self.img_wind_child.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
                self.img_wind_child.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDoubleClick)
            self.bg_imgs = bg.BackgroundCalculator(self.movie)
            if DEBUG:
                print 'initialized backsub data structure'
            if self.has('settingsfilename'):
                try:
                    self.LoadSettings()
                except:
                    pass

            if params.interactive:
                start_color = self.status.GetBackgroundColour()
                self.status.SetBackgroundColour(params.status_blue)
                self.status.SetStatusText('Reading annotation from file', params.status_box)
                wx.BeginBusyCursor()
                try:
                    wx.Yield()
                except:
                    pass

            if DEBUG:
                print 'creating/reading annotation file'
            if self.has('ann_filename'):
                new_ann_filename = self.ann_filename
            else:
                if self.menu.IsChecked(xrc.XRCID('menu_settings_annprompt')):
                    prompt_title = 'Choose annotation file'
                else:
                    prompt_title = None
                new_ann_filename = self.get_filename_with_extension('+.ann', prompt_title=prompt_title)
                if new_ann_filename is None:
                    self.OnQuit(None)
                    sys.exit(2)
            self.close_annfile()
            try:
                self.ann_file = annot.AnnotationFile(new_ann_filename, self.bg_imgs, justreadheader=not (params.interactive or params.noninteractive_resume_tracking), bg_img_shape=(self.movie.get_height(), self.movie.get_width()))
            except ValueError:
                s = 'Could not read annotation header, not reading in %s.' % new_ann_filename
                if params.feedback_enabled:
                    wx.MessageBox(s, 'Warning', wx.ICON_WARNING | wx.OK)
                else:
                    print s
                try:
                    os.remove(new_ann_filename)
                except Exception as details:
                    s = 'Could not delete unreadable annotation file %s:\n  %s.' % (new_ann_filename, str(details))
                    if params.feedback_enabled:
                        wx.MessageBox(s, 'Error', wx.ICON_ERROR | wx.OK)
                    else:
                        print s
                    self.movie = None
                    if params.interactive:
                        self.status.SetBackgroundColour(start_color)
                        self.status.SetStatusText('', params.status_box)
                        self.EnableControls()
                        self.UpdateStatusMovie()
                        wx.EndBusyCursor()
                    return

                self.ann_file = annot.AnnotationFile(new_ann_filename)

            if self.has('menu'):
                self.menu.Check(xrc.XRCID('menu_playback_flipud'), params.movie_flipud)
            if DEBUG:
                print 'done reading annotation file'
            if params.interactive:
                self.status.SetBackgroundColour(start_color)
                self.status.SetStatusText('', params.status_box)
                wx.EndBusyCursor()
                try:
                    wx.Yield()
                except:
                    pass

            if params.interactive and len(self.ann_file) > 0:
                self.menu.Check(xrc.XRCID('menu_playback_show_ann'), True)
            if self.has('update_alert_string'):
                if params.interactive and self.menu.IsChecked(xrc.XRCID('menu_help_updates')):
                    wx.MessageBox(self.update_alert_string, 'Ctrax can be updated', wx.OK)
                elif not params.interactive:
                    print '============================================'
                    print self.update_alert_string
                    print '============================================'
                delattr(self, 'update_alert_string')
                if self.has('newer_ctrax_avail'):
                    self.newest_ctrax_notified = self.newer_ctrax_avail
                if self.has('newer_matlab_avail'):
                    self.newest_matlab_notified = self.newer_matlab_avail
            if params.interactive:
                self.OnMouseDoubleClick(None)
                self.ShowCurrentFrame()
                self.EnableControls()
                self.UpdateStatusMovie()
                self.InitializeFrameSlider()
                self.OnResize()
            return

    def OnOpen(self, evt):
        """Movie file selection dialog."""
        old_mov = self.movie
        self.OpenMovie(new_movie=True)
        if self.movie is not old_mov:
            if self.menu.GetLabel(xrc.XRCID('menu_track_start')) == const.TRACK_STOP:
                self.OnStopTracking(None)
            self.play_break = True
            self.start_frame = 0
        return

    def OnLoadSettings(self, evt):
        settings_file = self.get_filename_with_extension('+.ann', 'Load Settings from File')
        if settings_file is not None:
            if self.menu.GetLabel(xrc.XRCID('menu_track_start')) == const.TRACK_STOP:
                self.OnStopTracking(None)
            self.play_break = True
            self.settingsfilename = settings_file
            self.start_frame = 0
            self.LoadSettings()
        return

    def OnSaveSettings(self, evt):
        settings_filename = self.get_filename_with_extension('+.ann', 'Save Settings to File')
        if settings_filename is not None:
            if params.feedback_enabled and os.access(settings_filename, os.F_OK):
                if wx.MessageBox('This will destroy any existing annotation data in the file. The file may have been automatically backed up, but you should verify. Continue saving settings to this file anyway?', 'Overwrite Data?', wx.YES_NO) == wx.NO:
                    return
            if os.path.exists(settings_filename):
                try:
                    os.remove(settings_filename)
                except WindowsError as details:
                    wx.MessageBox('Failed saving settings file: ' + str(details), 'Save Error', wx.OK)
                    return

            outfile = annot.AnnotationFile(settings_filename)
            outfile.InitializeData(bg_model=self.bg_imgs)
        return

    def get_filename_with_extension(self, new_ext, prompt_title=None):
        """Prompt user for a new filename, based on the movie filename but with a new extension.
Setting '+' as the first character of new_ext indicates that the new extension
should be appended rather than altered/replaced. If prompt_title is None, then
the new name is created and returned without user input."""
        if not self.has('movie'):
            return
        else:
            if new_ext[0] == '+':
                new_ext = new_ext[1:]
                replace_ext = False
            else:
                replace_ext = True
            if prompt_title is not None and params.feedback_enabled and not DEBUG:
                if replace_ext:
                    basename, ext = os.path.splitext(self.movie.filename)
                else:
                    basename = self.movie.filename
                new_name = basename + new_ext
                prompt_base, prompt_ext = os.path.splitext(new_ext)
                if prompt_ext == '':
                    prompt_ext = prompt_base
                dlg = wx.FileDialog(self.frame, prompt_title, self.movie.dirname, new_name, '*' + prompt_ext, wx.SAVE)
                if dlg.ShowModal() == wx.ID_OK:
                    save_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
                else:
                    save_path = None
                dlg.Destroy()
            else:
                if replace_ext:
                    basename, ext = os.path.splitext(self.movie.fullpath)
                else:
                    basename = self.movie.fullpath
                save_path = basename + new_ext
            return save_path

    def OnSave(self, evt):
        """Choose filename to save annotation data as MAT-file."""
        if len(self.ann_file) <= 0:
            if params.interactive:
                wx.MessageBox('No valid annotation\nexists for this movie\nor no movie is loaded.', 'Error', wx.ICON_ERROR | wx.OK)
            else:
                print 'Not saving -- no data'
            return
        if not self.ann_file.orientations_chosen:
            if params.interactive:
                if wx.MessageBox('Fly orientations have not been disambiguated yet. Do it now?', 'Choose orientations?', wx.YES_NO) == wx.YES:
                    self.OnChooseOrientations()
                    while hasattr(self, 'choose_orientations'):
                        self.choose_orientations.frame.Raise()
                        wx.Yield()
                        time.sleep(0.1)

            else:
                choose_orientations = chooseorientations.ChooseOrientations(self.frame, interactive=False)
                self.ann_file = choose_orientations.ChooseOrientations(self.ann_file, bg_model=self.bg_imgs)
        mat_name = self.get_filename_with_extension('.mat', 'Save as MAT-file')
        if mat_name is not None:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_blue)
            self.status.SetStatusText('writing annotation data to file', params.status_box)
            wx.BeginBusyCursor()
            wx.Yield()
            self.ann_file.WriteMAT(self.movie, mat_name)
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
            wx.EndBusyCursor()
            wx.Yield()
        return

    def OnSaveAvi(self, evt):
        """Choose filename to save tracks as AVI-file."""
        if len(self.ann_file) <= 0:
            if params.interactive:
                wx.MessageBox('No valid annotation\nexists for this movie\nor no movie is loaded.', 'Error', wx.ICON_ERROR | wx.OK)
            else:
                print 'Not saving -- no data'
            return
        dlg = wx.TextEntryDialog(self.frame, 'Frames to output to AVI file: (startframe:endframe): ', 'Save as AVI-file', '%d:%d' % (self.ann_file.firstframetracked, self.ann_file.lastframetracked))
        isgood = False
        while isgood == False:
            if dlg.ShowModal() == wx.ID_OK:
                isgood = True
                s = dlg.GetValue()
                s = s.rsplit(':')
            else:
                break
            if len(s) == 2:
                if s[0].isdigit() and s[1].isdigit():
                    framestart = int(s[0])
                    frameend = int(s[1])
                else:
                    isgood = False
                    continue
            else:
                isgood = False
                continue

        dlg.Destroy()
        if isgood == False:
            return
        else:
            avi_name = self.get_filename_with_extension('_annot.avi', 'Save as AVI file')
            if avi_name is not None:
                if params.interactive:
                    start_color = self.status.GetBackgroundColour()
                    self.status.SetBackgroundColour(params.status_blue)
                    self.status.SetStatusText('writing movie of results', params.status_box)
                    wx.BeginBusyCursor()
                    wx.Yield()
                movies.write_results_to_avi(self.movie, self.ann_file, avi_name, framestart, frameend)
                if self.alive and params.interactive:
                    self.status.SetBackgroundColour(start_color)
                    self.status.SetStatusText('', params.status_box)
                    wx.EndBusyCursor()
                    wx.Yield()
                print 'movie exported successfully'
            return

    def OnSaveCsv(self, evt):
        """Choose filename to save tracks as CSV-file."""
        if len(self.ann_file) <= 0:
            if params.interactive:
                wx.MessageBox('No valid annotation\nexists for this movie\nor no movie is loaded.', 'Error', wx.ICON_ERROR | wx.OK)
            else:
                print 'Not saving -- no data'
            return
        csv_name = self.get_filename_with_extension('.csv', 'Save as CSV file')
        if csv_name is not None:
            if params.interactive:
                start_color = self.status.GetBackgroundColour()
                self.status.SetBackgroundColour(params.status_blue)
                self.status.SetStatusText('writing plaintext results', params.status_box)
                wx.BeginBusyCursor()
                wx.Yield()
            self.ann_file.WriteCSV(csv_name)
            if self.alive and params.interactive:
                self.status.SetBackgroundColour(start_color)
                self.status.SetStatusText('', params.status_box)
                wx.EndBusyCursor()
                wx.Yield()
        return

    def OnSaveDiagnostics(self, evt):
        """Choose filename to save diagnostics to."""
        diag_name = self.get_filename_with_extension('_ctraxdiagnostics.txt', 'Save diagnostics to text file')
        if diag_name is not None:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_blue)
            self.status.SetStatusText('writing diagnostics to file', params.status_box)
            wx.BeginBusyCursor()
            wx.Yield()
            annot.WriteDiagnostics(diag_name)
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
            wx.EndBusyCursor()
            wx.Yield()
        return

    def EnableControls(self):
        """Enable or disable GUI controls based on current state of tracker."""
        if not params.interactive:
            return
        if self.has('batch'):
            self.batch.EnableControls()
        twiddling_enabled = params.feedback_enabled and not self.tracking
        movieready = self.has('movie')
        if movieready:
            issbfmf = hasattr(self.movie, 'type') and self.movie.type == 'sbfmf'
        else:
            issbfmf = False
        annready = movieready and self.has('ann_file') and len(self.ann_file) > 0
        isplaying = hasattr(self, 'play_break') and not self.play_break
        self.menu.Enable(xrc.XRCID('menu_track_start'), movieready and not isplaying)
        settings_enabled = movieready and twiddling_enabled
        self.menu.Enable(xrc.XRCID('menu_track_writesbfmf'), settings_enabled and not issbfmf)
        self.dowritesbfmf = self.dowritesbfmf and not issbfmf
        self.menu.Check(xrc.XRCID('menu_track_writesbfmf'), self.dowritesbfmf)
        self.menu.Enable(xrc.XRCID('menu_track_resume'), settings_enabled and not isplaying and annready and len(self.ann_file) < self.movie.get_n_frames())
        self.menu.Enable(xrc.XRCID('menu_track_resume_here'), settings_enabled and not isplaying and annready)
        self.menu.Enable(xrc.XRCID('menu_load_settings'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_save_settings'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_settings_bg'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_settings_bg_model'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_settings_tracking'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_playback_flipud'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_playback_transpose'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_tracking_wizard'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_compute_background'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_compute_shape'), settings_enabled)
        self.menu.Enable(xrc.XRCID('menu_file_save_diagnostics'), settings_enabled)
        self.framenumber_text.Enable(settings_enabled)
        self.slider.Enable(settings_enabled)
        self.frameinc_button.Enable(settings_enabled)
        self.framedec_button.Enable(settings_enabled)
        saving_enabled = annready and twiddling_enabled
        self.menu.Enable(xrc.XRCID('menu_playback_show_ann'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_file_export'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_file_save_avi'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_choose_orientations'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_analyze_plottraj'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_analyze_plotvel'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_analyze_histpos'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_analyze_histspeed'), saving_enabled)
        self.menu.Enable(xrc.XRCID('menu_analyze_histdtheta'), saving_enabled)

    def InitializeFrameSlider(self):
        self.slider.SetThumbPosition(self.start_frame)
        self.slider.SetScrollbar(self.start_frame, 1, self.movie.get_n_frames() - 1, 100)
        self.framenumber_text.SetValue('%06d' % self.movie.get_n_frames())

    def UpdateStatusMovie(self):
        """Update status bar with movie filename."""
        try:
            if not self.has('movie') or len(self.movie.filename) == 0:
                self.status.SetStatusText('[no file loaded]', params.file_box)
            elif len(self.movie.filename) < params.file_box_max_width:
                self.status.SetStatusText(self.movie.filename, params.file_box)
            else:
                self.status.SetStatusText('...' + os.sep + self.movie.filename, params.file_box)
        except (TypeError, AttributeError):
            pass

    def ShowCurrentFrame(self):
        """Grab current frame, draw on it, and display in GUI.
        Also update zoom-ellipse windows, if present."""
        if not params.interactive:
            return
        if not self.alive:
            return
        if not self.has('movie'):
            return
        if self.start_frame < 0:
            return
        try:
            st = time.time()
            frame, self.last_timestamp = self.movie.get_frame(self.start_frame)
            if num.isnan(self.last_timestamp):
                self.last_timestamp = float(self.start_frame) / float(params.DEFAULT_FRAME_RATE)
        except movies.NoMoreFramesException:
            self.start_frame = min(self.start_frame, self.movie.get_n_frames() - 1)
            self.slider.SetScrollbar(self.start_frame, 1, self.movie.get_n_frames() - 1, 100)
            return
        except IndexError:
            return

        self.framenumber_text.SetValue('%06d' % self.start_frame)
        if self.menu.IsChecked(xrc.XRCID('menu_playback_dim')):
            frame = frame / 2
        dodrawann = len(self.ann_file) > 0 and self.start_frame >= self.ann_file.firstframetracked and self.start_frame <= self.ann_file.lastframetracked
        frame8 = imagesk.double2mono8(frame, donormalize=False)
        height, width = frame8.shape
        if self.has('zoom_drag_roi'):
            left = int(round(width * self.zoom_drag_roi[0]))
            top = int(round(height * self.zoom_drag_roi[1]))
            right = int(round(width * self.zoom_drag_roi[2]))
            bottom = int(round(height * self.zoom_drag_roi[3]))
            frame8 = frame8[top:bottom, left:right]
            resizew = float(width) / max(float(frame8.shape[1]), 0.1)
            resizeh = float(height) / max(float(frame8.shape[0]), 0.1)
            self.zoom_drag_roi_scale = min(resizew, resizeh)
            try:
                new_frame8 = imresize(frame8, self.zoom_drag_roi_scale)
            except ValueError:
                return

            frame8 = num.ones(frame.shape, dtype=num.uint8) * 127
            frame8[:new_frame8.shape[0], :new_frame8.shape[1]] = new_frame8
        lines_to_draw = []
        line_colors = []
        if self.zoom_dragging:
            lines_to_draw.extend([
             (width * self.zoom_drag_origin[0],
              height * self.zoom_drag_origin[1],
              width * self.zoom_drag_origin[0],
              height * self.zoom_drag_current[1]),
             (
              width * self.zoom_drag_origin[0],
              height * self.zoom_drag_current[1],
              width * self.zoom_drag_current[0],
              height * self.zoom_drag_current[1]),
             (
              width * self.zoom_drag_current[0],
              height * self.zoom_drag_current[1],
              width * self.zoom_drag_current[0],
              height * self.zoom_drag_origin[1]),
             (
              width * self.zoom_drag_current[0],
              height * self.zoom_drag_origin[1],
              width * self.zoom_drag_origin[0],
              height * self.zoom_drag_origin[1])])
            line_colors.extend([params.zoom_drag_rectangle_color,
             params.zoom_drag_rectangle_color,
             params.zoom_drag_rectangle_color,
             params.zoom_drag_rectangle_color])
        if self.menu.IsChecked(xrc.XRCID('menu_playback_show_ann')) and dodrawann:
            tailframe = max(self.ann_file.firstframetracked, self.start_frame - params.tail_length)
            dataframes = self.ann_file[tailframe:self.start_frame + 1]
            if self.menu.IsChecked(xrc.XRCID('menu_settings_zoom')):
                self.zoom_window.SetData(dataframes[(-1)], frame)
                self.zoom_window.Redraw()
            ellipses = dataframes[(-1)]
            old_pts = []
            for dataframe in dataframes:
                these_pts = []
                for ellipse in dataframe.itervalues():
                    these_pts.append((ellipse.center.x, ellipse.center.y, ellipse.identity))

                old_pts.append(these_pts)

            linesegs = ell.annotate_image(ellipses, old_pts)
            linesegs, linecolors = imagesk.separate_linesegs_colors(linesegs)
            lines_to_draw.extend(linesegs)
            line_colors.extend(linecolors)
            self.num_flies_text.SetValue('N. Flies: %02d' % len(ellipses))
        else:
            self.num_flies_text.SetValue('')
        if self.has('zoom_drag_roi'):
            for si in range(len(lines_to_draw)):
                orig_seg = lines_to_draw[si]
                new_seg = ((orig_seg[0] - left) * self.zoom_drag_roi_scale,
                 (orig_seg[1] - top) * self.zoom_drag_roi_scale,
                 (orig_seg[2] - left) * self.zoom_drag_roi_scale,
                 (orig_seg[3] - top) * self.zoom_drag_roi_scale)
                lines_to_draw[si] = new_seg

        self.img_wind.update_image_and_drawings('Ctraxmain', frame8, format='MONO8', linesegs=lines_to_draw, lineseg_colors=line_colors, lineseg_widths=[
         params.ellipse_thickness] * len(lines_to_draw))
        self.img_wind.Refresh(eraseBackground=False)
        self.slider.SetThumbPosition(self.start_frame)
        self.frameinc_button.Enable(self.start_frame < self.movie.get_n_frames() - 1)
        self.framedec_button.Enable(self.start_frame > 0)

    def OnSlider(self, evt):
        """Frame slider callback. Display new frame."""
        new_fr = self.slider.GetThumbPosition()
        if new_fr != self.start_frame:
            try:
                try:
                    wx.Yield()
                except:
                    pass
                else:
                    self.play_break = True
                    self.start_frame = new_fr
                    self.ShowCurrentFrame()

            finally:
                evt.Skip()

    def OnResize(self, evt=None):
        """Window resized. Repaint in new window size."""
        if hasattr(self, 'img_size'):
            top_sizer = self.frame.GetSizer()
            panel_item = top_sizer.GetItem(self.img_panel)
            panel_item.SetFlag(panel_item.GetFlag() | wx.SHAPED)
            panel_item.SetRatio(float(self.img_size[1]) / self.img_size[0])
        self.frame.Layout()
        try:
            self.ShowCurrentFrame()
            button_size = self.frameinc_button.GetRect().GetWidth()
            new_size = wx.Size(self.img_wind.GetRect().GetWidth() - 2 * button_size, self.slider.GetRect().GetHeight())
            self.slider.SetMinSize(new_size)
            self.slider.SetSize(new_size)
            new_pos = wx.Point(self.img_panel.GetPosition().x + button_size, self.slider.GetPosition().y)
            self.slider.SetPosition(new_pos)
            new_pos = wx.Point(self.img_panel.GetPosition().x, self.framedec_button.GetPosition().y)
            self.framedec_button.SetPosition(new_pos)
            new_pos.x = self.img_panel.GetPosition().x + new_size.width + button_size
            self.frameinc_button.SetPosition(new_pos)
            const.file_box_max_width = int(float(self.img_wind.GetRect().GetWidth()) / 11.0)
            self.UpdateStatusMovie()
        except AttributeError:
            pass

    def close_annfile(self):
        """Close annotation file, as when opening a new movie or quitting."""
        if self.has('ann_file'):
            self.ann_file.close()
            if self.dowritesbfmf:
                self.ann_file.CopyToSBFMF()

    def OnQuit(self, evt):
        """Quit selected (or window closing). Stop threads and close window."""
        if self.menu.GetLabel(xrc.XRCID('menu_track_start')) == const.TRACK_STOP:
            self.OnStopTracking(None)
        self.play_break = True
        try:
            self.close_annfile()
        except Exception as details:
            print 'error closing annotation: %s' % details

        self.WriteUserfile()
        self.alive = False
        self.frame.Destroy()
        return

    def OnStopTracking(self, evt=None):
        """Stop button pressed. Stop threads."""
        self.StopThreads()
        params.enable_feedback(True)
        if self.has('batch'):
            self.batch.executing = False
        if self.dowritesbfmf and self.movie.writesbfmf_isopen():
            self.movie.writesbfmf_close(self.start_frame)
        self.tracking = False

    def OnStartTrackingMenu(self, evt):
        """Start button pressed. Begin tracking."""
        if self.menu.GetLabel(xrc.XRCID('menu_track_start')) == const.TRACK_STOP:
            self.OnStopTracking()
        else:
            self.OnStartTracking(evt)

    def OnWriteSBFMF(self, evt=None):
        """Set SBFMF filename. Use user input if running interactively."""
        self.dowritesbfmf = False
        if self.has('movie') and self.menu.IsChecked(xrc.XRCID('menu_track_writesbfmf')):
            self.writesbfmf_filename = self.get_filename_with_extension('.sbfmf')
            self.dowritesbfmf = True

    def OnPlayButton(self, evt):
        self.OnStartPlayback()

    def OnStopButton(self, evt):
        if self.tracking:
            self.OnStopTracking()
        else:
            self.OnStopPlayback()

    def OnStartTracking(self, evt=None):
        if not self.CheckForBGModel():
            return
        else:
            if params.enforce_minmax_shape and not self.CheckForShapeModel():
                return
            if evt is not None and params.interactive and self.has('ann_file') and len(self.ann_file) > 0 and not DEBUG:
                if evt.GetId() == xrc.XRCID('menu_track_start'):
                    msgtxt = 'Frames %d to %d have been tracked.\nErase these results and start tracking over?' % (self.ann_file.firstframetracked, self.ann_file.lastframetracked)
                    if wx.MessageBox(msgtxt, 'Erase trajectories and start tracking?', wx.OK | wx.CANCEL) == wx.CANCEL:
                        return
                elif evt.GetId() == xrc.XRCID('menu_track_resume_here'):
                    if self.ann_file.lastframetracked >= self.start_frame:
                        msgtxt = 'Frames %d to %d have been tracked.\nRestarting tracking at frame %d will cause old trajectories from %d to %d to be erased.\nErase these results and restart tracking in the current frame?' % (self.ann_file.firstframetracked, self.ann_file.lastframetracked, self.start_frame, self.start_frame, self.ann_file.lastframetracked)
                        if wx.MessageBox(msgtxt, 'Erase trajectories and start tracking?', wx.OK | wx.CANCEL) == wx.CANCEL:
                            return
            self.tracking = True
            self.UpdateToolBar('started')
            self.menu.SetLabel(xrc.XRCID('menu_track_start'), const.TRACK_STOP)
            self.menu.Check(xrc.XRCID('menu_playback_show_ann'), True)
            self.EnableControls()
            wx.Yield()
            if evt is not None and evt.GetId() == xrc.XRCID('menu_track_resume'):
                self.start_frame = self.ann_file.lastframetracked
                if DEBUG:
                    print 'start_frame = ' + str(self.start_frame)
                if DEBUG:
                    print 'cropping annotation file to frames %d through %d' % (self.ann_file.firstframetracked, self.ann_file.lastframetracked - 1)
                self.ann_file.InitializeData(self.ann_file.firstframetracked, self.ann_file.lastframetracked - 1, bg_model=self.bg_imgs)
                if self.dowritesbfmf:
                    try:
                        self.movie.writesbfmf_restart(self.start_frame, self.bg_imgs, self.writesbfmf_filename)
                    except Exception as details:
                        self.abort_sbfmf_writing(details)

            elif evt is not None and evt.GetId() == xrc.XRCID('menu_track_resume_here'):
                if self.start_frame > self.ann_file.lastframetracked:
                    print 'Restarting tracking at frame %d (current frame > last frame tracked)' % self.ann_file.lastframetracked
                    self.start_frame = self.ann_file.lastframetracked
                self.ann_file.InitializeData(self.ann_file.firstframetracked, self.start_frame - 1, bg_model=self.bg_imgs)
                if self.dowritesbfmf:
                    try:
                        self.movie.writesbfmf_restart(self.start_frame, self.bg_imgs, self.writesbfmf_filename)
                    except Exception as details:
                        self.abort_sbfmf_writing(details)

            else:
                self.start_frame = 0
                params.start_frame = self.start_frame
                self.ann_file.InitializeData(self.start_frame, bg_model=self.bg_imgs)
                if self.dowritesbfmf:
                    self.movie.writesbfmf_start(self.bg_imgs, self.writesbfmf_filename)
            self.Track()
            if self.alive:
                self.OnStopTracking()
                self.UpdateToolBar('stopped')
                self.menu.SetLabel(xrc.XRCID('menu_track_start'), const.TRACK_START)
                self.EnableControls()
            return

    def abort_sbfmf_writing(self, exception):
        msgtxt = 'Could not restart writing sbfmf; file %s was unreadable. Not writing sbfmf.' % self.writesbfmf_filename
        if params.interactive:
            wx.MessageBox(msgtxt, 'Warning', wx.ICON_WARNING | wx.OK)
        else:
            print msgtxt
        print 'SBFMF restart error was:', str(exception)
        self.dowritesbfmf = False
        self.menu.Check(xrc.XRCID('menu_track_writesbfmf'), False)
        self.movie.writesbfmf_close(self.start_frame)

    def OnComputeBg(self, evt=None):
        if params.interactive:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_green)
            self.status.SetStatusText('calculating background', params.status_box)
            success = self.bg_imgs.OnCalculate(parent=self.frame)
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
        else:
            success = self.bg_imgs.OnCalculate()
        return success

    def OnComputeShape(self, evt=None):
        if not self.CheckForBGModel():
            return
        if params.interactive:
            start_color = self.status.GetBackgroundColour()
            self.status.SetBackgroundColour(params.status_red)
            self.status.SetStatusText('calculating shape', params.status_box)
            wx.BeginBusyCursor()
            wx.Yield()
            success = ell.est_shape(self.bg_imgs, self.frame)
            wx.EndBusyCursor()
            self.status.SetBackgroundColour(start_color)
            self.status.SetStatusText('', params.status_box)
        else:
            success = ell.est_shape(self.bg_imgs)
        return success

    def OnStopPlayback(self, evt=None):
        self.play_break = True
        self.UpdateToolBar('stopped')
        self.EnableControls()

    def OnStartPlayback(self, evt=None):
        """Begin playback."""
        if not self.has('movie'):
            return
        self.UpdateToolBar('started')
        self.play_break = False
        self.EnableControls()
        self.start_frame += 1
        if self.start_frame >= self.movie.get_n_frames():
            self.start_frame = 0
            self.last_timestamp = self.movie.get_some_timestamps(0, 1)[0]
        self.play_start_stamp = self.last_timestamp
        self.play_start_time = time.time()
        while self.start_frame < self.movie.get_n_frames():
            self.slider.SetThumbPosition(self.start_frame)
            self.ShowCurrentFrame()
            wx.Yield()
            if self.play_break:
                break
            actual_time = max(time.time() - self.play_start_time, 0.05)
            movie_time = max(self.last_timestamp - self.play_start_stamp, 0.05)
            if movie_time / actual_time > self.play_speed:
                time.sleep(movie_time - actual_time * self.play_speed)
                self.start_frame += 1
            else:
                self.start_frame += int(round(actual_time * self.play_speed / movie_time))

        if self.start_frame >= self.movie.get_n_frames():
            self.start_frame = self.movie.get_n_frames() - 1
            self.slider.SetScrollbar(self.start_frame, 1, self.movie.get_n_frames() - 1, 100)
        if self.alive:
            self.OnStopPlayback()

    def OnSpeedUpButton(self, evt):
        if self.tracking:
            self.OnSpeedUpTracking()
        else:
            self.OnChangePlaybackSpeed(evt)

    def OnSlowDownButton(self, evt):
        if self.tracking:
            self.OnSlowDownTracking()
        else:
            self.OnChangePlaybackSpeed(evt)

    def OnRefreshButton(self, evt):
        self.request_refresh = True

    def OnSpeedUpTracking(self):
        self.framesbetweenrefresh = max(1, self.framesbetweenrefresh - 1)
        self.set_rate_text(use_refresh=True)

    def OnSlowDownTracking(self):
        self.framesbetweenrefresh += 1
        self.set_rate_text(use_refresh=True)

    def OnChangePlaybackSpeed(self, evt=None):
        """Change playback speed."""
        if evt.GetId() == self.speedup_id:
            self.play_speed *= 2
        elif evt.GetId() == self.slowdown_id:
            self.play_speed /= 2
        self.play_speed = min(self.play_speed, 32.0)
        self.play_speed = max(self.play_speed, 1 / 32.0)
        self.set_rate_text(use_refresh=False)
        if self.has('movie'):
            self.play_start_stamp = self.last_timestamp
            self.play_start_time = time.time()

    def OnBatch(self, evt):
        """Open batch processing window."""
        if self.batch is not None and self.batch.is_showing:
            self.batch.frame.Raise()
            return
        else:
            if self.batch is None:
                if self.has('movie'):
                    self.batch = batch.BatchWindow(self.frame, self.dir, self.last_movie_ext, self.movie)
                else:
                    self.batch = batch.BatchWindow(self.frame, self.dir, self.last_movie_ext)
            else:
                self.batch.ShowWindow(self.frame)
            self.batch.frame.Bind(wx.EVT_SIZE, self.OnBatchResize)
            self.batch.frame.Bind(wx.EVT_MOVE, self.OnBatchResize)
            self.batch.frame.Bind(wx.EVT_BUTTON, self.OnBatchExecute, id=xrc.XRCID('button_execute'))
            if self.last_batch_pos is not None:
                batch_pos = self.constrain_window_to_screen(self.last_batch_pos, self.last_batch_size)
                self.batch.frame.SetPosition(batch_pos)
                self.batch.frame.SetSize(self.last_batch_size)
            self.batch.sbfmf_checkbox.SetValue(self.menu.IsChecked(xrc.XRCID('menu_track_writesbfmf')))
            self.batch.flipud_checkbox.SetValue(self.menu.IsChecked(xrc.XRCID('menu_playback_flipud')))
            return

    def OnBatchResize(self, evt):
        """Batch window was moved or resized, remember new location."""
        evt.Skip()
        try:
            self.last_batch_size = self.batch.frame.GetSize()
            self.last_batch_pos = self.batch.frame.GetPosition()
        except AttributeError:
            pass

    def OnBatchExecute(self, evt):
        """Begin executing batch processing."""
        if len(self.batch.file_list) == 0:
            return
        else:
            if params.interactive and wx.MessageBox('Execute batch processing now?', 'Execute?', wx.YES_NO) == wx.NO:
                return
            if self.batch.should_load_settings():
                if not self.has('movie'):
                    self.movie = movies.Movie(self.batch.file_list[0]['filename'], interactive=False, open_now=False)
                settings_file = self.get_filename_with_extension('+.ann', 'Load Settings from File')
                if settings_file is None:
                    return
            else:
                settings_file = None
            params.enable_feedback(False)
            self.menu.SetLabel(xrc.XRCID('menu_track_start'), const.TRACK_STOP)
            self.EnableControls()
            if not self.menu.IsEnabled(xrc.XRCID('menu_playback_show_ann')):
                self.menu.Check(xrc.XRCID('menu_playback_show_ann'), True)
            wx.Yield()
            write_sbfmfs_init = self.dowritesbfmf
            write_sbfmfs = self.batch.sbfmf_checkbox.IsChecked()
            write_csvs = self.batch.csv_checkbox.IsChecked()
            movie_flipud = self.batch.flipud_checkbox.IsChecked()
            if params.batch_autodetect_arena is None:
                params.do_set_circular_arena = False
            else:
                params.do_set_circular_arena = params.batch_autodetect_arena
            self.batch.executing = True
            batch_list = self.batch.file_list[:]
            for movie_data in batch_list:
                params.movie_flipud = movie_flipud
                self.movie = movies.Movie(movie_data['filename'], interactive=False)
                self.start_frame = movie_data['startframe']
                self.last_frame = movie_data['endframe']
                self.OpenMovie(new_movie=False)
                if write_sbfmfs and self.movie.type != 'sbfmf':
                    self.dowritesbfmf = True
                    self.writesbfmf_filename = self.get_filename_with_extension('.sbfmf')
                else:
                    self.dowritesbfmf = False
                if write_csvs:
                    self.csvfilename = self.get_filename_with_extension('.csv')
                if settings_file is not None:
                    try:
                        annot.LoadSettings(settings_file, self.bg_imgs, bg_img_shape=(
                         self.movie.get_height(),
                         self.movie.get_width()), readbgmodel=True)
                    except:
                        print 'Could not read settings file', settings_file
                        raise

                    if params.batch_autodetect_arena == True and params.do_set_circular_arena == False:
                        params.do_set_circular_arena = True
                if self.menu.IsEnabled(xrc.XRCID('menu_track_start')):
                    self.tracking = True
                    self.UpdateToolBar('started')
                    wx.Yield()
                    self.DoAll()
                    if self.dowritesbfmf:
                        self.ann_file.CopyToSBFMF()
                    if self.alive:
                        self.UpdateToolBar('stopped')
                        wx.Yield()
                    self.tracking = False
                    self.last_frame = num.inf
                if not self.batch.executing:
                    break
                if len(self.batch.file_list) > 0:
                    self.batch.file_list.pop(0)
                    if self.batch.is_showing:
                        self.batch.list_box.Set(self.batch.file_list)

            self.batch.executing = False
            self.dowritesbfmf = write_sbfmfs_init
            if self.alive:
                params.enable_feedback(True)
                self.menu.SetLabel(xrc.XRCID('menu_track_start'), const.TRACK_START)
                self.EnableControls()
            return

    def OnCheckBatchStats(self, evt):
        """Batch statistics box checked. Force re-read of annotation data."""
        self.batch_data = None
        return

    def OnHelp(self, evt):
        """Help requested. Popup box with website."""
        wx.MessageBox('Documentation available at\nhttp://ctrax.sourceforge.net', 'Help', wx.OK)

    def OnAbout(self, evt):
        """About box requested."""
        wx.AboutBox(const.info)


def main():
    args = (0, )
    kw = {}
    if not int(os.environ.get('CTRAX_NO_REDIRECT', '0')):
        args = ()
        kw = dict(redirect=True)
    if DEBUG_REPEATABLE_BEHAVIOR:
        num.random.seed(0)
    app = CtraxApp(*args, **kw)
    app.MainLoop()


if __name__ == '__main__':
    main()
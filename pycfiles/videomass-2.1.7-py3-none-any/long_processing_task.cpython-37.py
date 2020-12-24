# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_panels/long_processing_task.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 19183 bytes
from __future__ import unicode_literals
import wx, os
from pubsub import pub
from videomass3.vdms_io.make_filelog import write_log
from videomass3.vdms_threads.ydl_pylibdownloader import Ydl_DL_Pylib
from videomass3.vdms_threads.ydl_executable import Ydl_DL_Exec
from videomass3.vdms_threads.one_pass import OnePass
from videomass3.vdms_threads.two_pass import TwoPass
from videomass3.vdms_threads.two_pass_EBU import Loudnorm
from videomass3.vdms_threads.picture_exporting import PicturesFromVideo
from videomass3.vdms_utils.utils import time_human
YELLOW = (200, 183, 47)
RED = (210, 24, 20)
VIOLET = (164, 30, 164)
GREEN = (30, 164, 30)
AZURE = (30, 62, 164)
get = wx.GetApp()
OS = get.OS
LOGDIR = get.LOGdir

def pairwise(iterable):
    """
    Return a zip object from iterable.
    This function is used by the update_display method.
    ----
    USE:

    after splitting ffmpeg's progress strings such as:
    output = "frame= 1178 fps=155 q=29.0 size=    2072kB time=00:00:39.02
              bitrate= 435.0kbits/s speed=5.15x  "
    in a list as:
    iterable = ['frame', '1178', 'fps', '155', 'q', '29.0', 'size', '2072kB',
                'time', '00:00:39.02', 'bitrate', '435.0kbits/s', s'peed',
                '5.15x']
    for x, y in pairwise(iterable):
        print(x,y)

    <https://stackoverflow.com/questions/5389507/iterating-over-every-
    two-elements-in-a-list>

    """
    a = iter(iterable)
    return zip(a, a)


class Logging_Console(wx.Panel):
    __doc__ = '\n    displays a text control for the output logging, a progress bar\n    and a progressive percentage text label. This panel is used\n    in combination with separated threads for long processing tasks.\n    It also implements stop and close buttons to stop the current\n    process and close the panel at the end.\n\n    '

    def __init__(self, parent):
        """
        In the 'previous' attribute is stored an ID string used to
        recover the previous panel from which the process is started.
        The 'logname' attribute is the name_of_panel.log file in which
        log messages will be written

        """
        self.parent = parent
        self.PARENT_THREAD = None
        self.ABORT = False
        self.ERROR = False
        self.previus = None
        self.logname = None
        wx.Panel.__init__(self, parent=parent)
        lbl = wx.StaticText(self, label=(_('Log viewing console:')))
        self.OutText = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2))
        self.ckbx_text = wx.CheckBox(self, wx.ID_ANY, _('Suppress excess output'))
        self.barProg = wx.Gauge(self, (wx.ID_ANY), range=0)
        self.labPerc = wx.StaticText(self, label='')
        self.button_stop = wx.Button(self, wx.ID_STOP, _('Abort'))
        self.button_close = wx.Button(self, wx.ID_CLOSE, '')
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridSizer(1, 2, 5, 5)
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(self.OutText, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.ckbx_text, 0, wx.ALL, 5)
        sizer.Add(self.barProg, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.labPerc, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer.Add(grid, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=5)
        grid.Add(self.button_stop, 0, wx.ALL, 5)
        grid.Add(self.button_close, 1, wx.ALL, 5)
        if OS == 'Darwin':
            self.OutText.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        else:
            self.OutText.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.ckbx_text.SetToolTip(_('If activated, hides some output messages.'))
        self.button_stop.SetToolTip(_('Stops current process'))
        self.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.button_stop)
        self.Bind(wx.EVT_BUTTON, self.on_close, self.button_close)
        self.button_stop.Enable(True)
        self.button_close.Enable(False)
        pub.subscribe(self.youtubedl_from_import, 'UPDATE_YDL_FROM_IMPORT_EVT')
        pub.subscribe(self.youtubedl_exec, 'UPDATE_YDL_EXECUTABLE_EVT')
        pub.subscribe(self.update_display, 'UPDATE_EVT')
        pub.subscribe(self.update_count, 'COUNT_EVT')
        pub.subscribe(self.end_proc, 'END_EVT')

    def topic_thread(self, panel, varargs, duration):
        """
        Thread redirection
        varargs: type tuple data object
        duration: total duration or partial if set timeseq
        """
        self.previus = panel
        if varargs[0] == 'console view only':
            self.button_stop.Enable(False)
            self.button_close.Enable(True)
            return
            (
             self.OutText.Clear(), self.labPerc.SetLabel(''))
            self.logname = varargs[8]
            time_seq = self.parent.time_seq
            write_log(self.logname, LOGDIR)
            if varargs[0] == 'onepass':
                self.PARENT_THREAD = OnePass(varargs, duration, self.logname, time_seq)
        elif varargs[0] == 'twopass':
            self.PARENT_THREAD = TwoPass(varargs, duration, self.logname, time_seq)
        else:
            if varargs[0] == 'two pass EBU':
                self.PARENT_THREAD = Loudnorm(varargs, duration, self.logname, time_seq)
            else:
                if varargs[0] == 'savepictures':
                    self.PARENT_THREAD = PicturesFromVideo(varargs, duration, self.logname, time_seq)
                else:
                    if varargs[0] == 'youtube_dl python package':
                        self.ckbx_text.Hide()
                        self.PARENT_THREAD = Ydl_DL_Pylib(varargs, self.logname)
                    else:
                        if varargs[0] == 'youtube-dl executable':
                            self.ckbx_text.Hide()
                            self.PARENT_THREAD = Ydl_DL_Exec(varargs, self.logname)

    def youtubedl_from_import(self, output, duration, status):
        """
        Receiving output messages from youtube_dl library via
        pubsub "UPDATE_YDL_FROM_IMPORT_EVT" .
        """
        if status == 'ERROR':
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
            self.OutText.AppendText('%s\n' % output)
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(RED)))
            self.OutText.AppendText(_(' ...Failed\n'))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
        else:
            if status == 'WARNING':
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                self.OutText.AppendText('%s\n' % output)
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            else:
                if status == 'DEBUG':
                    if '[download] Destination' in output:
                        self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                        self.OutText.AppendText('%s\n' % output)
                        self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
                    else:
                        if '[download]' not in output:
                            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                            self.OutText.AppendText('%s\n' % output)
                            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
                            with open(os.path.join(LOGDIR, self.logname), 'a') as (logerr):
                                logerr.write('[YOUTUBE_DL]: %s > %s\n' % (status,
                                 output))
                else:
                    if status == 'DOWNLOAD':
                        self.labPerc.SetLabel('%s' % duration[0])
                        self.barProg.SetValue(duration[1])
                    else:
                        if status == 'FINISHED':
                            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                            self.OutText.AppendText('%s\n' % duration)
                            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
                        if status in ('ERROR', 'WARNING'):
                            with open(os.path.join(LOGDIR, self.logname), 'a') as (logerr):
                                logerr.write('[YOUTUBE_DL]: %s\n' % output)

    def youtubedl_exec(self, output, duration, status):
        """
        Receiving output messages from youtube-dl command line execution
        via pubsub "UPDATE_YDL_EXECUTABLE_EVT" .

        """
        if not status == 0:
            if output:
                self.OutText.AppendText('%s\n' % output)
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(RED)))
            self.OutText.AppendText(_(' ...Failed\n'))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            return
        if '[download]' in output:
            if 'Destination' not in output:
                try:
                    i = float(output.split()[1].split('%')[0])
                except ValueError:
                    self.OutText.AppendText(' %s' % output)
                else:
                    self.barProg.SetValue(i)
                    self.labPerc.SetLabel('%s' % output)
                    del output
                    del duration
        else:
            if not self.ckbx_text.IsChecked():
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                self.OutText.AppendText(' %s' % output)
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            with open(os.path.join(LOGDIR, self.logname), 'a') as (logerr):
                logerr.write('[YOUTUBE-DL]: %s' % output)

    def update_display(self, output, duration, status):
        """
        Receive message from thread of the second loops process
        by wxCallafter and pubsub UPDATE_EVT.
        The received 'output' is parsed for calculate the bar
        progress value, percentage label and errors management.
        This method can be used even for non-loop threads.

        NOTE: During conversion the ffmpeg errors do not stop all
              others tasks, if an error occurred it will be marked
              with 'failed' but continue; if it has finished without
              errors it will be marked with 'completed' on update_count
              method. Since not all ffmpeg messages are errors, sometimes
              it happens to see more output marked with yellow color.

        This strategy consists first of capturing all the output and
        marking it in yellow, then in capturing the error if present,
        but exiting immediately after the function.

        """
        if not status == 0:
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(RED)))
            self.OutText.AppendText(_(' ...Failed\n'))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            return
        if 'time=' in output:
            i = output.index('time=') + 5
            pos = output[i:i + 8].split(':')
            hours, minutes, seconds = pos[0], pos[1], pos[2]
            timesum = (int(hours) * 3600 + int(minutes)) * 60 + int(seconds)
            self.barProg.SetValue(timesum)
            percentage = timesum / duration * 100
            out = [a for a in '='.join(output.split()).split('=') if a]
            ffprog = []
            for x, y in pairwise(out):
                ffprog.append('%s: %s | ' % (x, y))

            remaining = time_human(duration - timesum)
            self.labPerc.SetLabel('Processing... %s%% | %sTime Remaining: %s' % (
             str(int(percentage)), ''.join(ffprog),
             remaining))
            del output
            del duration
        else:
            if not self.ckbx_text.IsChecked():
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
                self.OutText.AppendText('%s' % output)
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            with open(os.path.join(LOGDIR, self.logname), 'a') as (logerr):
                logerr.write('[FFMPEG]: %s' % output)

    def update_count(self, count, duration, fname, end):
        """
        Receive message from first 'for' loop in the thread process.
        This method can be used even for non-loop threads.

        """
        if end == 'ok':
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(GREEN)))
            self.OutText.AppendText(_(' ...Completed\n'))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            lab = '%s' % self.labPerc.GetLabel()
            if lab.split('|')[0] == 'Processing... 99% ':
                relab = lab.replace('Processing... 99%', 'Processing... 100%')
                self.labPerc.SetLabel(relab)
            return
        if end == 'error':
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(YELLOW)))
            self.OutText.AppendText('\n%s\n' % count)
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            self.ERROR = True
        else:
            self.barProg.SetRange(duration)
            self.barProg.SetValue(0)
            self.OutText.AppendText('\n%s : "%s"\n' % (count, fname))

    def end_proc(self):
        """
        At the end of the process
        """
        if self.ERROR is True:
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(RED)))
            self.OutText.AppendText(_('\n Sorry, task failed !\n'))
            self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
        else:
            if self.ABORT is True:
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(VIOLET)))
                self.OutText.AppendText(_('\n Interrupted Process !\n'))
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
            else:
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.Colour(AZURE)))
                self.OutText.AppendText(_('\n All finished !\n'))
                self.OutText.SetDefaultStyle(wx.TextAttr(wx.NullColour))
                self.barProg.SetValue(0)
        self.button_stop.Enable(False)
        self.button_close.Enable(True)
        self.PARENT_THREAD = None

    def on_stop(self, event):
        """
        The user change idea and was stop process
        """
        self.PARENT_THREAD.stop()
        self.parent.statusbar_msg(_("wait... I'm aborting"), 'GOLDENROD')
        self.PARENT_THREAD.join()
        self.parent.statusbar_msg(_('Status: Interrupted'), None)
        self.ABORT = True
        event.Skip()

    def on_close(self, event):
        """
        close dialog and retrieve at previusly panel

        """
        if not self.logname:
            self.ckbx_text.Show()
            self.button_stop.Enable(True)
            self.button_close.Enable(False)
            self.parent.panelShown(self.previus)
        if self.PARENT_THREAD is not None:
            if wx.MessageBox(_('There are still processes running.. if you want to stop them, use the "Abort" button.\n\nDo you want to kill application?'), _('Please confirm'), wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return
            self.parent.on_Kill()
        self.ckbx_text.Show()
        self.button_stop.Enable(True)
        self.button_close.Enable(False)
        self.PARENT_THREAD = None
        self.ABORT = False
        self.ERROR = False
        self.logname = None
        self.parent.panelShown(self.previus)
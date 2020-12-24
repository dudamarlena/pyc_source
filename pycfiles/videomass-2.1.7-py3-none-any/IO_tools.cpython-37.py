# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_io/IO_tools.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 12849 bytes
import wx, os, shutil, stat, tarfile
from videomass3.vdms_threads.mpv_url import Url_Play
from videomass3.vdms_threads.ffplay_file import File_Play
from videomass3.vdms_threads.ffprobe_parser import FFProbe
from videomass3.vdms_threads.volumedetect import VolumeDetectThread
from videomass3.vdms_threads.check_bin import ff_conf
from videomass3.vdms_threads.check_bin import ff_formats
from videomass3.vdms_threads.check_bin import ff_codecs
from videomass3.vdms_threads.check_bin import ff_topics
from videomass3.vdms_threads.opendir import browse
from videomass3.vdms_threads.ydl_pylibextractinfo import Ydl_EI_Pylib
from videomass3.vdms_threads.ydl_executable import Ydl_EI_Exec
from videomass3.vdms_threads import youtubedlupdater
from videomass3.vdms_frames import ffmpeg_conf
from videomass3.vdms_frames import ffmpeg_formats
from videomass3.vdms_frames import ffmpeg_codecs
from videomass3.vdms_dialogs.popup import PopupDialog
get = wx.GetApp()
OS = get.OS
DIR_CONF = get.DIRconf
FFPROBE_URL = get.FFPROBE_url
FFMPEG_URL = get.FFMPEG_url
FFPLAY_URL = get.FFPLAY_url

def stream_info(title, filepath):
    """
    Show media information of the streams content.
    This function make a bit control of file existance.
    """
    try:
        with open(filepath):
            miniframe = Mediainfo(title, filepath, FFPROBE_URL, OS)
            miniframe.Show()
    except IOError:
        wx.MessageBox(_('File does not exist or not a valid file:  %s') % filepath, 'Videomass: warning', wx.ICON_EXCLAMATION, None)


def stream_play(filepath, timeseq, param):
    """
    Thread for media reproduction with ffplay
    """
    try:
        with open(filepath):
            thread = File_Play(filepath, timeseq, param)
    except IOError:
        wx.MessageBox(_('File does not exist or not a valid file:  %s') % filepath, 'Videomass: warning', wx.ICON_EXCLAMATION, None)
        return


def url_play(url, quality):
    """
    Thread for urls reproduction with mpv player
    """
    thread = Url_Play(url, quality)


def probeInfo(filename):
    """
    Get data stream informations during dragNdrop action.
    It is called by MyListCtrl(wx.ListCtrl) only.
    Return tuple object with two items: (data, None) or (None, error).
    """
    metadata = FFProbe(FFPROBE_URL, filename, parse=False, writer='json')
    if metadata.ERROR():
        err = metadata.error
        print('[FFprobe] Error:  %s' % err)
        return (None, err)
    data = metadata.custom_output()
    return (
     data, None)


def volumeDetectProcess(filelist, time_seq, audiomap):
    """
    Run thread to get audio peak level data and show a
    pop-up dialog with message.
    """
    thread = VolumeDetectThread(time_seq, filelist, audiomap, OS)
    loadDlg = PopupDialog(None, _('Videomass - Loading...'), _('\nWait....\nAudio peak analysis.\n'))
    loadDlg.ShowModal()
    data = thread.data
    loadDlg.Destroy()
    return data


def test_conf():
    """
    Call *check_bin.ffmpeg_conf* to get data to test the building
    configurations of the installed or imported FFmpeg executable
    and send it to dialog box.

    """
    out = ff_conf(FFMPEG_URL, OS)
    if 'Not found' in out[0]:
        wx.MessageBox('\n{0}'.format(out[1]), 'Videomass: error', wx.ICON_ERROR, None)
        return
    miniframe = ffmpeg_conf.Checkconf(out, FFMPEG_URL, FFPROBE_URL, FFPLAY_URL, OS)
    miniframe.Show()


def test_formats():
    """
    Call *check_bin.ff_formats* to get available formats by
    imported FFmpeg executable and send it to dialog box.

    """
    diction = ff_formats(FFMPEG_URL, OS)
    if 'Not found' in diction.keys():
        wx.MessageBox('\n{0}'.format(diction['Not found']), 'Videomass: error', wx.ICON_ERROR, None)
        return
    miniframe = ffmpeg_formats.FFmpeg_formats(diction, OS)
    miniframe.Show()


def test_codecs(type_opt):
    """
    Call *check_bin.ff_codecs* to get available encoders
    and decoders by FFmpeg executable and send it to
    corresponding dialog box.

    """
    diction = ff_codecs(FFMPEG_URL, type_opt, OS)
    if 'Not found' in diction.keys():
        wx.MessageBox('\n{0}'.format(diction['Not found']), 'Videomass: error', wx.ICON_ERROR, None)
        return
    miniframe = ffmpeg_codecs.FFmpeg_Codecs(diction, OS, type_opt)
    miniframe.Show()


def findtopic(topic):
    """
    Call * check_bin.ff_topic * to run the ffmpeg command to search
    a certain topic. The FFMPEG_URL is given by ffmpeg-search dialog.

    """
    retcod = ff_topics(FFMPEG_URL, topic, OS)
    if 'Not found' in retcod[0]:
        s = '\n{0}'.format(retcod[1])
        return s
    return retcod[1]


def openpath(where):
    """
    Call vdms_threads.opendir.browse to open file browser into
    configuration directory or log directory.

    """
    ret = browse(OS, where)
    if ret:
        wx.MessageBox(ret, 'Videomass Error', wx.ICON_ERROR, None)


def youtube_info(url):
    """
    Call the thread to get extract info data object with
    youtube_dl python package and show a wait pop-up dialog .
    youtube_dl module.
    example without pop-up dialog:
    thread = Ydl_EI_Pylib(url)
    thread.join()
    data = thread.data
    yield data
    """
    thread = Ydl_EI_Pylib(url)
    loadDlg = PopupDialog(None, _('Videomass - Loading...'), _('\nWait....\nRetrieving required data.\n'))
    loadDlg.ShowModal()
    data = thread.data
    loadDlg.Destroy()
    yield data


def youtube_getformatcode_exec(url):
    """
    Call the thread to get format code data object with youtube-dl
    executable, (e.g. `youtube-dl -F url`) .
    While waiting, a pop-up dialog is shown.
    """
    thread = Ydl_EI_Exec(url)
    loadDlg = PopupDialog(None, _('Videomass - Loading...'), _('\nWait....\nRetrieving required data.\n'))
    loadDlg.ShowModal()
    data = thread.data
    loadDlg.Destroy()
    yield data


def youtubedl_latest(url):
    """
    Call the thread to read the latest version of youtube-dl via the web.
    While waiting, a pop-up dialog is shown.
    """
    thread = youtubedlupdater.CheckNewRelease(url)
    loadDlg = PopupDialog(None, _('Videomass - Reading...'), _('\nWait....\nCheck for update.\n'))
    loadDlg.ShowModal()
    latest = thread.data
    loadDlg.Destroy()
    return latest


def youtubedl_update(cmd, waitmsg):
    """
    Call thread to execute generic tasks as updates youtube-dl executable
    or read the installed version. All these tasks are intended only for
    the local copy (not installed by the package manager) of youtube-dl.
    While waiting, a pop-up dialog is shown.
    """
    thread = youtubedlupdater.Command_Execution(cmd)
    loadDlg = PopupDialog(None, _('Videomass - Loading...'), waitmsg)
    loadDlg.ShowModal()
    update = thread.data
    loadDlg.Destroy()
    return update


def youtubedl_upgrade(latest, executable, upgrade=False):
    """
    Run thread to download locally the latest version of youtube-dl
    or youtube-dl.exe . While waiting, a pop-up dialog is shown.
    """
    if upgrade:
        msg = _('\nWait....\nUpgrading youtube-dl.\n')
    else:
        msg = _('\nWait....\nDownloading youtube-dl.\n')
    if os.path.basename(executable) == 'youtube-dl.exe':
        name = os.path.basename(executable)
        url = 'https://github.com/ytdl-org/youtube-dl/releases/download/%s/%s' % (
         latest, name)
        dest = executable
    else:
        name = os.path.basename(executable)
        url = 'https://github.com/ytdl-org/youtube-dl/releases/download/%s/%s-%s.tar.gz' % (
         latest, name, latest)
        dest = '%s-%s.tar.gz' % (executable, latest)
    if os.path.exists(executable):
        try:
            os.rename(executable, '%s_OLD' % executable)
        except FileNotFoundError as err:
            try:
                return (
                 None, err)
            finally:
                err = None
                del err

    else:
        if not os.path.exists(os.path.dirname(executable)):
            try:
                os.makedirs((os.path.dirname(executable)), mode=511)
            except OSError as err:
                try:
                    return (
                     None, err)
                finally:
                    err = None
                    del err

            thread = youtubedlupdater.Upgrade_Latest(url, dest)
            loadDlg = PopupDialog(None, _('Videomass - Downloading...'), msg)
            loadDlg.ShowModal()
            status = thread.data
            loadDlg.Destroy()
            if os.path.splitext(dest)[1] == '.gz':
                if os.path.exists(dest):
                    try:
                        with tarfile.open(dest) as (tar):
                            tar.extractall(os.path.dirname(dest))
                            tar.close()
                    except:
                        print('error when opening tarfile')
                        return
                    else:
                        os.remove(dest)
            if os.path.exists('%s_OLD' % executable):
                if not status[1]:
                    if os.path.isfile('%s_OLD' % executable):
                        os.remove('%s_OLD' % executable)
                    else:
                        if os.path.isdir('%s_OLD' % executable):
                            shutil.rmtree('%s_OLD' % executable)
                else:
                    os.rename('%s_OLD' % executable, executable)
        elif os.path.isfile(executable):
            if name != 'youtube-dl.exe' and os.path.isfile(executable):
                st = os.stat(executable)
                os.chmod(executable, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return status
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/Videomass3.py
# Compiled at: 2020-05-11 08:15:23
# Size of source mod 2**32: 8816 bytes
import wx, os, sys, shutil
from videomass3.vdms_sys.ctrl_run import system_check
from videomass3.vdms_sys.appearance import Appearance
import builtins
builtins.__dict__['_'] = wx.GetTranslation
import videomass3.vdms_sys as appC

class Videomass(wx.App):
    __doc__ = '\n    Check for the essentials Before starting the Videomass main frame\n\n    '

    def __init__(self, redirect=True, filename=None):
        """
        The following attributes will be used in some class
        with wx.GetApp()
        -------
        attribute definition:
        self.DIRconf > location of the configuration directory
        self.FILEconf > location videomass.conf (Windows or Unix?)
        self.WORKdir > (PWD) location of the current program directory
        self.OS > operating system name
        self.pylibYdl > if None youtube-dl is used as library
        self.execYdl > if False is not used a local executable
        self.USERfilesave > set user path folder for file destination

        """
        self.DIRconf = None
        self.FILEconf = None
        self.WORKdir = None
        self.OS = None
        self.FFMPEG_url = None
        self.FFPLAY_url = None
        self.FFPROBE_url = None
        self.FFMPEG_loglev = None
        self.FFPLAY_loglev = None
        self.pylibYdl = None
        self.execYdl = False
        self.USERfilesave = None
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        """
        This is bootstrap interface. ``setui`` get data
        of the file configuration and set the environment.

        """
        setui = system_check()
        lang = ''
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(setui[5])
        self.updateLanguage(lang)
        if setui[2]:
            wx.MessageBox(_('{0}\n\nSorry, cannot continue..'.format(setui[2])), 'Videomass: Fatal Error', wx.ICON_STOP)
            return False
        icons = Appearance(setui[3], setui[4][13])
        pathicons = icons.icons_set()
        self.OS = setui[0]
        self.FILEconf = setui[6]
        self.WORKdir = setui[7]
        self.DIRconf = setui[8]
        self.FFMPEG_loglev = setui[4][4]
        self.FFPLAY_loglev = setui[4][3]
        self.FFMPEG_check = setui[4][5]
        self.FFPROBE_check = setui[4][7]
        self.FFPLAY_check = setui[4][9]
        self.MPV_check = setui[4][11]
        self.MPV_url = setui[4][12]
        self.FFthreads = setui[4][2]
        self.USERfilesave = None if setui[4][1] == 'none' else setui[4][1]
        self.LOGdir = setui[9]
        self.CACHEdir = setui[10]
        if self.OS == 'Windows':
            try:
                from youtube_dl import YoutubeDL
                self.execYdl = False
            except (ModuleNotFoundError, ImportError) as nomodule:
                try:
                    self.pylibYdl = nomodule
                    self.execYdl = os.path.join(self.CACHEdir, 'youtube-dl.exe')
                finally:
                    nomodule = None
                    del nomodule

        else:
            try:
                from youtube_dl import YoutubeDL
                self.execYdl = False
            except (ModuleNotFoundError, ImportError) as nomodule:
                try:
                    src = os.path.join(self.CACHEdir, 'youtube-dl')
                    sys.path.append(src)
                    try:
                        from youtube_dl import YoutubeDL
                        self.execYdl = False
                    except (ModuleNotFoundError, ImportError) as nomodule:
                        try:
                            self.pylibYdl = nomodule
                            self.execYdl = src
                        finally:
                            nomodule = None
                            del nomodule

                finally:
                    nomodule = None
                    del nomodule

            if setui[0] == 'Darwin':
                for link in [setui[4][6], setui[4][8], setui[4][10]]:
                    if os.path.isfile('%s' % link):
                        binaries = False
                    else:
                        binaries = True
                        break

                if binaries:
                    self.firstrun(pathicons[16])
                    return True
                self.FFMPEG_url = setui[4][6]
                self.FFPROBE_url = setui[4][8]
                self.FFPLAY_url = setui[4][10]
            else:
                if setui[0] == 'Windows':
                    for link in [setui[4][6], setui[4][8], setui[4][10]]:
                        if os.path.isfile('%s' % link):
                            binaries = False
                        else:
                            binaries = True
                            break

                    if binaries:
                        self.firstrun(pathicons[16])
                        return True
                    self.FFMPEG_url = setui[4][6]
                    self.FFPROBE_url = setui[4][8]
                    self.FFPLAY_url = setui[4][10]
                else:
                    self.FFMPEG_url = setui[4][6]
                    self.FFPROBE_url = setui[4][8]
                    self.FFPLAY_url = setui[4][10]
            from videomass3.vdms_main.main_frame import MainFrame
            main_frame = MainFrame(setui, pathicons)
            main_frame.Show()
            self.SetTopWindow(main_frame)
            return True

    def firstrun(self, icon):
        """
        Start a temporary dialog: this is showing during first time
        start of the Videomass application on MacOS and Windows.
        """
        from videomass3.vdms_dialogs.first_time_start import FirstStart
        main_frame = FirstStart(icon)
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True

    def updateLanguage(self, lang):
        """
        Update the language to the requested one.
        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param string `lang`: one of the supported language codes

        """
        if lang in appC.supLang:
            selLang = appC.supLang[lang]
        else:
            selLang = wx.LANGUAGE_DEFAULT
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        else:
            self.locale = wx.Locale(selLang)
            if self.locale.IsOk():
                self.locale.AddCatalog(appC.langDomain)
            else:
                self.locale = None

    def OnExit(self):
        """
        OnExit provides an interface for exiting the application
        """
        return True


def main():
    """
    Starts the wx.App mainloop
    """
    app = Videomass(False)
    fred = app.MainLoop()
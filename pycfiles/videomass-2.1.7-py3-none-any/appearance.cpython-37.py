# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_sys/appearance.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 8040 bytes
import os

class Appearance(object):
    __doc__ = '\n    This class determines the paths to use to set icons\n    on the graphic appearance of the Videomass program.\n    '

    def __init__(self, IS_LOCAL, iconset):
        """
        The paths where the icon sets are located depend where
        the program is run and on which operating system.
        Each icons set is defined by the name of the folder that
        contains it.
        """
        if IS_LOCAL:
            url = '%s/art/icons' % os.getcwd()
            self.videomass_icon = '%s/videomass.png' % url
            self.wizard_icon = '%s/videomass_wizard.png' % url
        else:
            import sys, platform
            OS = platform.system()
            if OS == 'Windows':
                pythonpath = os.path.dirname(sys.executable)
                url = pythonpath + '\\share\\videomass\\icons'
                self.videomass_icon = url + '\\videomass.png'
                self.wizard_icon = url + '\\videomass_wizard.png'
            else:
                from shutil import which
                binarypath = which('videomass')
                if binarypath == '/usr/local/bin/videomass':
                    url = '/usr/local/share/videomass/icons'
                    share = '/usr/local/share/pixmaps'
                    self.videomass_icon = share + '/videomass.png'
                    self.wizard_icon = url + '/videomass_wizard.png'
                else:
                    if binarypath == '/usr/bin/videomass':
                        url = '/usr/share/videomass/icons'
                        share = '/usr/share/pixmaps'
                        self.videomass_icon = share + '/videomass.png'
                        self.wizard_icon = url + '/videomass_wizard.png'
                    else:
                        import site
                        userbase = site.getuserbase()
                        url = userbase + '/share/videomass/icons'
                        share = '/share/pixmaps'
                        self.videomass_icon = userbase + share + '/videomass.png'
                        self.wizard_icon = url + '/videomass_wizard.png'
        if iconset == 'Videomass_Sign_Icons':
            self.x48 = '%s/Videomass_Sign_Icons/48x48' % url
            self.x32 = '%s/Videomass_Sign_Icons/32x32' % url
            self.x24 = '%s/Videomass_Sign_Icons/24x24' % url
            self.x18 = '%s/Videomass_Sign_Icons/18x18' % url
        elif iconset == 'Material_Design_Icons_black':
            self.x48 = '%s/Videomass_Sign_Icons/48x48' % url
            self.x32 = '%s/Material_Design_Icons_black/32x32' % url
            self.x24 = '%s/Material_Design_Icons_black/24x24' % url
            self.x18 = '%s/Material_Design_Icons_black/18x18' % url
            self.icons_set()
        else:
            if iconset == 'Flat_Color_Icons':
                self.x48 = '%s/Videomass_Sign_Icons/48x48' % url
                self.x32 = '%s/Flat_Color_Icons/32x32' % url
                self.x24 = '%s/Flat_Color_Icons/24x24' % url
                self.x18 = '%s/Flat_Color_Icons/18x18' % url
                self.icons_set()

    def icons_set(self):
        """
        assignment path at the used icons in according to configuration file.
        """
        icon_switchvideomass = '%s/icon_videoconversions.png' % self.x48
        icon_youtube = '%s/icon_youtube.png' % self.x48
        icon_prst_mng = '%s/icon_prst_mng.png' % self.x48
        icon_process = '%s/icon_process.png' % self.x32
        icon_toolback = '%s/icon_mainback.png' % self.x32
        icon_toolforward = '%s/icon_mainforward.png' % self.x32
        icon_ydl = '%s/youtubeDL.png' % self.x32
        icn_infosource = '%s/infosource.png' % self.x24
        icn_preview = '%s/preview.png' % self.x24
        icn_cut = '%s/cut.png' % self.x24
        icn_saveprf = '%s/saveprf.png' % self.x24
        icn_newprf = '%s/newprf.png' % self.x24
        icn_delprf = '%s/delprf.png' % self.x24
        icn_editprf = '%s/editprf.png' % self.x24
        icn_playfilters = '%s/playfilters.png' % self.x24
        icn_resetfilters = '%s/resetfilters.png' % self.x24
        ic_resize = '%s/resize.png' % self.x18
        ic_crop = '%s/crop.png' % self.x18
        ic_rotate = '%s/rotate.png' % self.x18
        ic_deinterlace = '%s/deinterlace.png' % self.x18
        ic_denoiser = '%s/denoiser.png' % self.x18
        ic_analyzes = '%s/analyzes.png' % self.x18
        ic_settings = '%s/settings.png' % self.x18
        ic_peaklevel = '%s/peaklevel.png' % self.x18
        return [os.path.join(norm) for norm in [self.videomass_icon,
         icon_switchvideomass,
         icon_process,
         icn_infosource,
         icn_preview,
         icn_cut,
         icn_playfilters,
         icn_resetfilters,
         icn_saveprf,
         ic_resize,
         ic_crop,
         ic_rotate,
         ic_deinterlace,
         ic_denoiser,
         ic_analyzes,
         ic_settings,
         self.wizard_icon,
         ic_peaklevel,
         icon_youtube,
         icon_prst_mng,
         icn_newprf,
         icn_delprf,
         icn_editprf,
         icon_toolback,
         icon_toolforward,
         icon_ydl]]
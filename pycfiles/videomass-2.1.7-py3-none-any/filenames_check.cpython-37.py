# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_io/filenames_check.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 4466 bytes
import wx, os

def inspect(file_sources, dir_destin, extoutput):
    """
    La funzione offre un controllo per gestire l'overwriting demandando
    all'utente la scelta se sovrascrive o meno file già esistenti, e
    un'altro controllo per la verifica dell'esistenza reale di files
    e cartelle e un ultimo controllo per la modalità batch o single process.

    The function return following values:
    typeproc: if one singol file is alone, if multiple file is batch.
    file_sources: a file list filtered by checking.
    outputdir: contains output paths as many as the file sources
    filename: file names without path and extension
    base_name: file names without path but with extensions
    lenghmax: lengh list useful for count the loop index on the batch process.

    """
    if not file_sources:
        return (False, None, None, None, None)
    else:
        exclude = []
        outputdir = []
        base_name = []
        for path in file_sources:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            filename = os.path.splitext(basename)[0]
            if not extoutput:
                pathname = '%s/%s' % (dir_destin, basename)
                outputdir.append(dir_destin)
                base_name.append(basename)
                if os.path.exists(pathname):
                    exclude.append(pathname)
                else:
                    pathname = '%s/%s.%s' % (dir_destin, filename, extoutput)
                    outputdir.append(dir_destin)
                    if os.path.exists(pathname):
                        exclude.append(pathname)

        if exclude:
            if wx.MessageBox(_('Already exist: \n\n- %s\n\nDo you want to overwrite? ') % '\n- '.join(exclude), _('Videomass: Please Confirm'), wx.ICON_QUESTION | wx.YES_NO, None) == wx.NO:
                return (False, None, None, None, None)
        for f in file_sources:
            if not os.path.isfile(os.path.abspath(f)):
                wx.MessageBox(_('The file does not exist:\n\n"%s"\n') % f, _('Videomass: Input file error'), wx.ICON_ERROR)
                return (False, None, None, None, None)

        for d in outputdir:
            if not os.path.isdir(os.path.abspath(d)):
                wx.MessageBox(_('The folder does not exist:\n\n"%s"\n') % d, _('Videomass: Output folder error'), wx.ICON_ERROR)
                return (False, None, None, None, None)

        if len(file_sources) > 1:
            typeproc = 'batch'
        else:
            typeproc = 'alone'
    lenghmax = len(file_sources)
    return (
     typeproc, file_sources, outputdir, filename, base_name, lenghmax)
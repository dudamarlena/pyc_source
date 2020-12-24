# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_io/presets_manager_properties.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 4424 bytes
import wx, os, json

def supported_formats(supp, file_sources):
    """
    check for supported formats from selected profile in the
    presets manager panel
    """
    items = ''.join(supp.split()).split(',')
    exclude = []
    if not items == ['']:
        for src in file_sources:
            if os.path.splitext(src)[1].split('.')[1] not in items:
                exclude.append(src)

        if exclude:
            for x in exclude:
                file_sources.remove(x)

            if not file_sources:
                wx.MessageBox(_('The selected profile is not suitable to convert the following file formats:\n\n%s\n\n') % '\n'.join(exclude), 'Videomass', wx.ICON_INFORMATION | wx.OK)
                return
    return file_sources


def json_data(arg):
    """
    Used by presets_mng_panel.py to get JSON data from `*.vip` files.
    The `arg` parameter refer to each file name to parse. Return a list
    type object from getting data using `json` module in the following
    form:

    [{"Name": "",
      "Descritpion": "",
      "First_pass": "",
      "Second_pass": "",
      "Supported_list": "",
      "Output_extension": ""
    }]

    """
    try:
        with open(arg, 'r', encoding='utf-8') as (f):
            data = json.load(f)
    except json.decoder.JSONDecodeError as err:
        try:
            msg = _('Is not a compatible Videomass presets. It is recommended removing it or rewrite it with a compatible JSON data structure.\n\nPossible solution: open Presets Manager panel, then use menu "File" > "Reset all presets" to safe repair all presets. Remember, those that are not compatible you have to manually remove them.')
            wx.MessageBox('\nERROR: {1}\n\nFile: "{0}"\n{2}'.format(arg, err, msg), 'Videomass', wx.ICON_ERROR | wx.OK, None)
            return 'error'
        finally:
            err = None
            del err

    except FileNotFoundError as err:
        try:
            msg = _('The presets folder is empty, or there are invalid files. Open the Presets Manager panel, then Perform a repair in the "File" > "Reset all presets" menu.')
            wx.MessageBox('\nERROR: {1}\n\nFile: "{0}"\n{2}'.format(arg, err, msg), 'Videomass', wx.ICON_ERROR | wx.OK, None)
            return 'error'
        finally:
            err = None
            del err

    return data


def delete_profiles(path, name):
    """
    Profile deletion from Presets manager panel
    """
    with open(path, 'r', encoding='utf-8') as (f):
        data = json.load(f)
    new_data = [obj for obj in data if not obj['Name'] == name]
    with open(path, 'w', encoding='utf-8') as (outfile):
        json.dump(new_data, outfile, ensure_ascii=False, indent=4)
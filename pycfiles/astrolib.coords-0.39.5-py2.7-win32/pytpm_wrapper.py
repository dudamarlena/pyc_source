# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\astrolib\coords\pytpm_wrapper.py
# Compiled at: 2014-01-13 11:58:06
"""
This routine wraps the `pytpm.blackbox` routine in order to apply
the longitude convention preferred in coords. All `astrolib.coords`
routines should call `~astrolib.coords.pytpm_wrapper.blackbox`
instead of `pytpm.blackbox`.

Since pytpm is itself a wrapper for the TPM library, the change
could have been made there; but the modulo operator in C only
works on integers, so it was simpler to do it in python. Also,
this leaves pytpm itself as a more transparent wrapper for TPM.

"""
import pytpm, astrodate, datetime

def blackbox(x, y, instate, outstate, epoch, equinox, timetag=None):
    """
    Parameters
    ----------
    x, y : float
        Position in decimal degrees.

    instate, outstate : int
        The TPM states of the position.

    epoch : float
        Epoch of the position.

    equinox : float
        Equinox of the position.

    timetag : `~astrolib.coords.astrodate.AstroDate`
        Timetag of returned coordinate.

    Returns
    -------
    r, d : float
        Converted coordinate.

    """
    if timetag == None:
        timetag = astrodate.AstroDate()
    try:
        r, d = pytpm.blackbox(x, y, instate, outstate, epoch, equinox, timetag.jd)
    except AttributeError:
        astrotag = astrodate.AstroDate(timetag)
        r, d = pytpm.blackbox(x, y, instate, outstate, epoch, equinox, astrotag.jd)

    r = r % 360.0
    return (r, d)
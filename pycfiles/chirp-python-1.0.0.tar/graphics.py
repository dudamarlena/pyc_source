# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\graphics.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nPlotting utilities\n\nCopyright (C) 2011 Dan Meliza <dan // meliza.org>\nCreated 2011-08-10\n'

def axgriditer(gridfun=None, figfun=None, **figparams):
    """
    Generates axes for multiple gridded plots.  Initial call
    to generator specifies plot grid (default 1x1).  Yields axes
    on the grid; when the grid is full, opens a new figure and starts
    filling that.

    Arguments:
    gridfun - function to open figure and specify subplots. Needs to to return
              fig, axes. Default function creates one subplot in a figure.

    figfun - called when the figure is full or the generator is
             closed.  Can be used for final figure cleanup or to save
             the figure.  Can be callable, in which case the
             signature is figfun(fig); or it can be a generator, in
             which case its send() method is called.

    additional arguments are passed to the figure() function
    """
    if gridfun is None:
        from matplotlib.pyplot import subplots
        gridfun = lambda : subplots(1, 1)
    fig, axg = gridfun(**figparams)
    try:
        while 1:
            for ax in axg.flat:
                yield ax

            if callable(figfun):
                figfun(fig)
            elif hasattr(figfun, 'send'):
                figfun.send(fig)
            fig, axg = gridfun(**figparams)

    except:
        if callable(figfun):
            figfun(fig)
        elif hasattr(figfun, 'send'):
            figfun.send(fig)
        raise

    return
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/plot_top_down_view.py
# Compiled at: 2020-02-02 11:10:42
# Size of source mod 2**32: 17197 bytes
"""
Created on Sat Feb  2 16:06:09 2019

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Circle
import matplotlib.ticker as plticker
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import random, warnings
try:
    import rebound
    from rebound.particle import Particle
except:
    warnings.warn('Module "rebound" could not be imported. Orbital plots are not available.')

from itertools import cycle
from allesfitter import config
from allesfitter.exoworlds_rdx.lightcurves.index_transits import get_first_epoch
from allesfitter.exoworlds_rdx.lightcurves.lightcurve_tools import calc_phase

def OrbitPlot(sim, figsize=None, lim=None, limz=None, Narc=100, xlabel='x', ylabel='y', zlabel='z', color=False, periastron=False, trails=True, show_orbit=True, lw=1.0, glow=False, slices=False, plotparticles=[], primary=None, fancy=False, ax=None):
    """
    Convenience function for plotting instantaneous orbits.

    Parameters
    ----------
    slices          : bool, optional
        Plot all three slices if set to True. Default is False and plots orbits only in the xy plane.
    figsize         : tuple of float, optional
        Tuple defining the figure size (default: (5,5))
    lim             : float, optional           
        Limit for axes (default: None = automatically determined)
    limz            : float, optional           
        Limit for z axis, only used if slices=True (default: None = automatically determined)
    unitlabel       : str, optional          
        String describing the units, shown on axis labels (default: None)
    color           : bool, str or list, optional            
        By default plots in black. If set to True, plots using REBOUND color cycle. If a string or list of strings, e.g. ['red', 'cyan'], will cycle between passed colors.
    periastron  : bool, optional            
        Draw a marker at periastron (default: False)
    trails          : bool, optional            
        Draw trails instead of solid lines (default: False)
    show_orbit      : bool, optional
        Draw orbit trails/lines (default: True)
    lw              : float, optional           
        Linewidth (default: 1.)
    glow            : bool (default: False)
        Make lines glow
    fancy           : bool (default: False)
        Changes various settings to create a fancy looking plot
    plotparticles   : list, optional
        List of particles to plot. Can be a list of any valid keys for accessing sim.particles, i.e., integer indices or hashes (default: plot all particles)
    primary         : rebound.Particle, optional
        Pimrary to use for the osculating orbit (default: Jacobi center of mass)

    Returns
    -------
    fig
        A matplotlib figure

    Examples
    --------
    The following example illustrates a typical use case.

    >>> sim = rebound.Simulation()
    >>> sim.add(m=1)
    >>> sim.add(a=1)
    >>> fig = rebound.OrbitPlot(sim)
    >>> fig.savefig("image.png") # save figure to file
    >>> fig.show() # show figure on screen

    """
    if slices:
        if figsize is None:
            figsize = (8, 8)
        if ax is None:
            fig, ax = plt.subplots(2, 2, figsize=figsize)
        gs = gridspec.GridSpec(2, 2, width_ratios=[3.0, 2.0], height_ratios=[2.0, 3.0], wspace=0.0, hspace=0.0)
        OrbitPlotOneSlice(sim, (plt.subplot(gs[2])), lim=lim, Narc=Narc, color=color, periastron=periastron, trails=trails, show_orbit=show_orbit, lw=lw, axes='xy', fancy=fancy, plotparticles=plotparticles, primary=primary, glow=glow)
        OrbitPlotOneSlice(sim, (plt.subplot(gs[3])), lim=lim, limz=limz, Narc=Narc, color=color, periastron=periastron, trails=trails, show_orbit=show_orbit, lw=lw, fancy=fancy, axes='zy', plotparticles=plotparticles, primary=primary, glow=glow)
        OrbitPlotOneSlice(sim, (plt.subplot(gs[0])), lim=lim, limz=limz, Narc=Narc, color=color, periastron=periastron, trails=trails, show_orbit=show_orbit, lw=lw, fancy=fancy, axes='xz', plotparticles=plotparticles, primary=primary, glow=glow)
        plt.subplot(gs[2]).set_xlabel(xlabel)
        plt.subplot(gs[2]).set_ylabel(ylabel)
        plt.setp((plt.subplot(gs[0]).get_xticklabels()), visible=False)
        plt.subplot(gs[0]).set_ylabel(zlabel)
        plt.subplot(gs[3]).set_xlabel(zlabel)
        plt.setp((plt.subplot(gs[3]).get_yticklabels()), visible=False)
    else:
        if figsize is None:
            figsize = (5, 5)
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        OrbitPlotOneSlice(sim, ax, lim=lim, Narc=Narc, color=color, periastron=periastron, trails=trails, show_orbit=show_orbit, lw=lw, fancy=fancy, plotparticles=plotparticles, primary=primary, glow=glow)
    return (
     plt.gcf(), ax)


def get_color(color):
    """
    Takes a string for a color name defined in matplotlib and returns of a 3-tuple of RGB values.
    Will simply return passed value if it's a tuple of length three.

    Parameters
    ----------
    color   : str
        Name of matplotlib color to calculate RGB values for.
    """
    if isinstance(color, tuple):
        if len(color) == 3:
            return color
    hexcolor = sns.colors.xkcd_rgb[color]
    hexcolor = hexcolor.lstrip('#')
    lv = len(hexcolor)
    return tuple((int(hexcolor[i:i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3)))


def fading_line(x, y, color='black', alpha_initial=1.0, alpha_final=0.0, glow=False, **kwargs):
    """
    Returns a matplotlib LineCollection connecting the points in the x and y lists, with a single color and alpha varying from alpha_initial to alpha_final along the line.
    Can pass any kwargs you can pass to LineCollection, like linewidgth.

    Parameters
    ----------
    x       : list or array of floats for the positions on the (plot's) x axis
    y       : list or array of floats for the positions on the (plot's) y axis
    color   : matplotlib color for the line. Can also pass a 3-tuple of RGB values (default: 'black')
    alpha_initial:  Limiting value of alpha to use at the beginning of the arrays.
    alpha_final:    Limiting value of alpha to use at the end of the arrays.
    """
    if glow:
        glow = False
        kwargs['lw'] = 1
        fl1 = fading_line(x, y, color, alpha_initial, alpha_final, glow=False, **kwargs)
        kwargs['lw'] = 2
        alpha_initial *= 0.5
        alpha_final *= 0.5
        fl2 = fading_line(x, y, color, alpha_initial, alpha_final, glow=False, **kwargs)
        kwargs['lw'] = 6
        alpha_initial *= 0.5
        alpha_final *= 0.5
        fl3 = fading_line(x, y, color, alpha_initial, alpha_final, glow=False, **kwargs)
        return [fl3, fl2, fl1]
    color = get_color(color)
    cdict = {'red':((0.0, color[0], color[0]), (1.0, color[0], color[0])),  'green':(
      (
       0.0, color[1], color[1]), (1.0, color[1], color[1])), 
     'blue':(
      (
       0.0, color[2], color[2]), (1.0, color[2], color[2])), 
     'alpha':(
      (
       0.0, alpha_initial, alpha_initial), (1.0, alpha_final, alpha_final))}
    Npts = len(x)
    if len(y) != Npts:
        raise AttributeError('x and y must have same dimension.')
    segments = np.zeros((Npts - 1, 2, 2))
    segments[0][0] = [x[0], y[0]]
    for i in range(1, Npts - 1):
        pt = [
         x[i], y[i]]
        segments[(i - 1)][1] = pt
        segments[i][0] = pt

    segments[(-1)][1] = [
     x[(-1)], y[(-1)]]
    individual_cm = LinearSegmentedColormap('indv1', cdict)
    lc = LineCollection(segments, cmap=individual_cm, **kwargs)
    lc.set_array(np.linspace(0.0, 1.0, len(segments)))
    return lc


def OrbitPlotOneSlice--- This code section failed: ---

 L. 209         0  BUILD_LIST_0          0 
                2  STORE_FAST               'p_orb_pairs'

 L. 210         4  LOAD_FAST                'plotparticles'
                6  POP_JUMP_IF_TRUE     20  'to 20'

 L. 211         8  LOAD_GLOBAL              range
               10  LOAD_CONST               1
               12  LOAD_FAST                'sim'
               14  LOAD_ATTR                N_real
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  STORE_FAST               'plotparticles'
             20_0  COME_FROM             6  '6'

 L. 212        20  SETUP_LOOP           66  'to 66'
               22  LOAD_FAST                'plotparticles'
               24  GET_ITER         
               26  FOR_ITER             64  'to 64'
               28  STORE_FAST               'i'

 L. 213        30  LOAD_FAST                'sim'
               32  LOAD_ATTR                particles
               34  LOAD_FAST                'i'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'p'

 L. 214        40  LOAD_FAST                'p_orb_pairs'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'p'
               46  LOAD_FAST                'p'
               48  LOAD_ATTR                calculate_orbit
               50  LOAD_FAST                'primary'
               52  LOAD_CONST               ('primary',)
               54  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               56  BUILD_TUPLE_2         2 
               58  CALL_METHOD_1         1  '1 positional argument'
               60  POP_TOP          
               62  JUMP_BACK            26  'to 26'
               64  POP_BLOCK        
             66_0  COME_FROM_LOOP       20  '20'

 L. 216        66  LOAD_FAST                'lim'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE   150  'to 150'

 L. 217        74  LOAD_CONST               0.0
               76  STORE_FAST               'lim'

 L. 218        78  SETUP_LOOP          142  'to 142'
               80  LOAD_FAST                'p_orb_pairs'
               82  GET_ITER         
             84_0  COME_FROM           132  '132'
               84  FOR_ITER            140  'to 140'
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'p'
               90  STORE_FAST               'o'

 L. 219        92  LOAD_FAST                'o'
               94  LOAD_ATTR                a
               96  LOAD_CONST               0.0
               98  COMPARE_OP               >
              100  POP_JUMP_IF_FALSE   120  'to 120'

 L. 220       102  LOAD_CONST               1.0
              104  LOAD_FAST                'o'
              106  LOAD_ATTR                e
              108  BINARY_ADD       
              110  LOAD_FAST                'o'
              112  LOAD_ATTR                a
              114  BINARY_MULTIPLY  
              116  STORE_FAST               'r'
              118  JUMP_FORWARD        126  'to 126'
            120_0  COME_FROM           100  '100'

 L. 222       120  LOAD_FAST                'o'
              122  LOAD_ATTR                d
              124  STORE_FAST               'r'
            126_0  COME_FROM           118  '118'

 L. 223       126  LOAD_FAST                'r'
              128  LOAD_FAST                'lim'
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE    84  'to 84'

 L. 224       134  LOAD_FAST                'r'
              136  STORE_FAST               'lim'
              138  JUMP_BACK            84  'to 84'
              140  POP_BLOCK        
            142_0  COME_FROM_LOOP       78  '78'

 L. 225       142  LOAD_FAST                'lim'
              144  LOAD_CONST               1.15
              146  INPLACE_MULTIPLY 
              148  STORE_FAST               'lim'
            150_0  COME_FROM            72  '72'

 L. 226       150  LOAD_FAST                'limz'
              152  LOAD_CONST               None
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   208  'to 208'

 L. 227       158  LOAD_LISTCOMP            '<code_object <listcomp>>'
              160  LOAD_STR                 'OrbitPlotOneSlice.<locals>.<listcomp>'
              162  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              164  LOAD_FAST                'p_orb_pairs'
              166  GET_ITER         
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  STORE_FAST               'z'

 L. 228       172  LOAD_CONST               2.0
              174  LOAD_GLOBAL              max
              176  LOAD_FAST                'z'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  BINARY_MULTIPLY  
              182  STORE_FAST               'limz'

 L. 229       184  LOAD_FAST                'limz'
              186  LOAD_FAST                'lim'
              188  COMPARE_OP               >
              190  POP_JUMP_IF_FALSE   196  'to 196'

 L. 230       192  LOAD_FAST                'lim'
              194  STORE_FAST               'limz'
            196_0  COME_FROM           190  '190'

 L. 231       196  LOAD_FAST                'limz'
              198  LOAD_CONST               0.0
              200  COMPARE_OP               <=
              202  POP_JUMP_IF_FALSE   208  'to 208'

 L. 232       204  LOAD_FAST                'lim'
              206  STORE_FAST               'limz'
            208_0  COME_FROM           202  '202'
            208_1  COME_FROM           156  '156'

 L. 234       208  LOAD_FAST                'axes'
              210  LOAD_CONST               0
              212  BINARY_SUBSCR    
              214  LOAD_STR                 'z'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   238  'to 238'

 L. 235       220  LOAD_FAST                'ax'
              222  LOAD_METHOD              set_xlim
              224  LOAD_FAST                'limz'
              226  UNARY_NEGATIVE   
              228  LOAD_FAST                'limz'
              230  BUILD_LIST_2          2 
              232  CALL_METHOD_1         1  '1 positional argument'
              234  POP_TOP          
              236  JUMP_FORWARD        254  'to 254'
            238_0  COME_FROM           218  '218'

 L. 237       238  LOAD_FAST                'ax'
              240  LOAD_METHOD              set_xlim
              242  LOAD_FAST                'lim'
              244  UNARY_NEGATIVE   
              246  LOAD_FAST                'lim'
              248  BUILD_LIST_2          2 
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
            254_0  COME_FROM           236  '236'

 L. 238       254  LOAD_FAST                'axes'
              256  LOAD_CONST               1
              258  BINARY_SUBSCR    
              260  LOAD_STR                 'z'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   286  'to 286'

 L. 239       268  LOAD_FAST                'ax'
              270  LOAD_METHOD              set_ylim
              272  LOAD_FAST                'limz'
              274  UNARY_NEGATIVE   
              276  LOAD_FAST                'limz'
              278  BUILD_LIST_2          2 
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
              284  JUMP_FORWARD        302  'to 302'
            286_0  COME_FROM           264  '264'

 L. 241       286  LOAD_FAST                'ax'
              288  LOAD_METHOD              set_ylim
              290  LOAD_FAST                'lim'
              292  UNARY_NEGATIVE   
              294  LOAD_FAST                'lim'
              296  BUILD_LIST_2          2 
              298  CALL_METHOD_1         1  '1 positional argument'
              300  POP_TOP          
            302_0  COME_FROM           284  '284'

 L. 243       302  LOAD_FAST                'fancy'
          304_306  POP_JUMP_IF_FALSE   350  'to 350'

 L. 244       308  LOAD_FAST                'ax'
              310  LOAD_METHOD              set_facecolor
              312  LOAD_CONST               (0.0, 0.0, 0.0)
              314  CALL_METHOD_1         1  '1 positional argument'
              316  POP_TOP          

 L. 245       318  SETUP_LOOP          350  'to 350'
              320  LOAD_CONST               ('top', 'bottom', 'right', 'left')
              322  GET_ITER         
              324  FOR_ITER            348  'to 348'
              326  STORE_FAST               'pos'

 L. 246       328  LOAD_FAST                'ax'
              330  LOAD_ATTR                spines
              332  LOAD_FAST                'pos'
              334  BINARY_SUBSCR    
              336  LOAD_METHOD              set_edgecolor
              338  LOAD_CONST               (0.3, 0.3, 0.3)
              340  CALL_METHOD_1         1  '1 positional argument'
              342  POP_TOP          
          344_346  JUMP_BACK           324  'to 324'
              348  POP_BLOCK        
            350_0  COME_FROM_LOOP      318  '318'
            350_1  COME_FROM           304  '304'

 L. 248       350  LOAD_FAST                'color'
              352  LOAD_CONST               False
              354  COMPARE_OP               is-not
          356_358  POP_JUMP_IF_FALSE   462  'to 462'

 L. 249       360  LOAD_GLOBAL              isinstance
              362  LOAD_FAST                'color'
              364  LOAD_GLOBAL              list
              366  CALL_FUNCTION_2       2  '2 positional arguments'
          368_370  POP_JUMP_IF_FALSE   408  'to 408'

 L. 250       372  BUILD_LIST_0          0 
              374  STORE_FAST               'colors'

 L. 251       376  SETUP_LOOP          460  'to 460'
              378  LOAD_FAST                'color'
              380  GET_ITER         
              382  FOR_ITER            404  'to 404'
              384  STORE_FAST               'c'

 L. 252       386  LOAD_FAST                'colors'
              388  LOAD_METHOD              append
              390  LOAD_GLOBAL              get_color
              392  LOAD_FAST                'c'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  CALL_METHOD_1         1  '1 positional argument'
              398  POP_TOP          
          400_402  JUMP_BACK           382  'to 382'
              404  POP_BLOCK        
              406  JUMP_FORWARD        460  'to 460'
            408_0  COME_FROM           368  '368'

 L. 253       408  LOAD_GLOBAL              isinstance
              410  LOAD_FAST                'color'
              412  LOAD_GLOBAL              str
              414  CALL_FUNCTION_2       2  '2 positional arguments'
          416_418  POP_JUMP_IF_FALSE   432  'to 432'

 L. 254       420  LOAD_GLOBAL              get_color
              422  LOAD_FAST                'color'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  BUILD_LIST_1          1 
              428  STORE_FAST               'colors'
              430  JUMP_FORWARD        460  'to 460'
            432_0  COME_FROM           416  '416'

 L. 255       432  LOAD_FAST                'color'
              434  LOAD_CONST               True
              436  COMPARE_OP               ==
          438_440  POP_JUMP_IF_FALSE   486  'to 486'

 L. 256       442  LOAD_CONST               (1.0, 0.0, 0.0)
              444  LOAD_CONST               (0.0, 0.75, 0.75)
              446  LOAD_CONST               (0.75, 0.0, 0.75)
              448  LOAD_CONST               (0.75, 0.75, 0)
              450  LOAD_CONST               (0.0, 0.0, 0.0)
              452  LOAD_CONST               (0.0, 0.0, 1.0)
              454  LOAD_CONST               (0.0, 0.5, 0.0)
              456  BUILD_LIST_7          7 
              458  STORE_FAST               'colors'
            460_0  COME_FROM           430  '430'
            460_1  COME_FROM           406  '406'
            460_2  COME_FROM_LOOP      376  '376'
              460  JUMP_FORWARD        486  'to 486'
            462_0  COME_FROM           356  '356'

 L. 258       462  LOAD_FAST                'fancy'
          464_466  POP_JUMP_IF_FALSE   480  'to 480'

 L. 259       468  LOAD_CONST               (0.8786407766990292, 0.32038834951456313, 0.9271844660194175)
              470  BUILD_LIST_1          1 
              472  STORE_FAST               'colors'

 L. 260       474  LOAD_CONST               True
              476  STORE_FAST               'glow'
              478  JUMP_FORWARD        486  'to 486'
            480_0  COME_FROM           464  '464'

 L. 262       480  LOAD_STR                 'black'
              482  BUILD_LIST_1          1 
              484  STORE_FAST               'colors'
            486_0  COME_FROM           478  '478'
            486_1  COME_FROM           460  '460'
            486_2  COME_FROM           438  '438'

 L. 263       486  LOAD_GLOBAL              cycle
              488  LOAD_FAST                'colors'
              490  CALL_FUNCTION_1       1  '1 positional argument'
              492  STORE_FAST               'coloriterator'

 L. 269       494  LOAD_FAST                'primary'
              496  LOAD_CONST               None
              498  COMPARE_OP               is
          500_502  POP_JUMP_IF_FALSE   514  'to 514'
              504  LOAD_FAST                'sim'
              506  LOAD_ATTR                particles
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  JUMP_FORWARD        516  'to 516'
            514_0  COME_FROM           500  '500'
              514  LOAD_FAST                'primary'
            516_0  COME_FROM           512  '512'
              516  STORE_FAST               'prim'

 L. 270       518  LOAD_FAST                'fancy'
          520_522  POP_JUMP_IF_FALSE   958  'to 958'

 L. 271       524  LOAD_CONST               (1.0, 1.0, 0.7421875)
              526  STORE_FAST               'sun'

 L. 272       528  LOAD_CONST               0.02
              530  STORE_FAST               'opa'

 L. 273       532  LOAD_CONST               6000.0
              534  STORE_FAST               'size'

 L. 274       536  SETUP_LOOP          612  'to 612'
              538  LOAD_GLOBAL              range
              540  LOAD_CONST               256
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  GET_ITER         
              546  FOR_ITER            610  'to 610'
              548  STORE_FAST               'i'

 L. 275       550  LOAD_FAST                'ax'
              552  LOAD_ATTR                scatter
              554  LOAD_GLOBAL              getattr
              556  LOAD_FAST                'prim'
              558  LOAD_FAST                'axes'
              560  LOAD_CONST               0
              562  BINARY_SUBSCR    
              564  CALL_FUNCTION_2       2  '2 positional arguments'
              566  LOAD_GLOBAL              getattr
              568  LOAD_FAST                'prim'
              570  LOAD_FAST                'axes'
              572  LOAD_CONST               1
              574  BINARY_SUBSCR    
              576  CALL_FUNCTION_2       2  '2 positional arguments'
              578  LOAD_FAST                'opa'
              580  LOAD_FAST                'size'
              582  LOAD_FAST                'lw'
              584  BINARY_MULTIPLY  
              586  LOAD_FAST                'sun'
              588  LOAD_CONST               None
              590  LOAD_CONST               3
              592  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              594  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              596  POP_TOP          

 L. 276       598  LOAD_FAST                'size'
              600  LOAD_CONST               0.95
              602  INPLACE_MULTIPLY 
              604  STORE_FAST               'size'
          606_608  JUMP_BACK           546  'to 546'
              610  POP_BLOCK        
            612_0  COME_FROM_LOOP      536  '536'

 L. 278       612  LOAD_CONST               (1.0, 1.0, 1.0)
              614  STORE_FAST               'starcolor'

 L. 279       616  LOAD_FAST                'ax'
              618  LOAD_METHOD              get_xlim
              620  CALL_METHOD_0         0  '0 positional arguments'
              622  UNPACK_SEQUENCE_2     2 
              624  STORE_FAST               'mi'
              626  STORE_FAST               'ma'

 L. 280       628  LOAD_GLOBAL              random
              630  LOAD_METHOD              getstate
              632  CALL_METHOD_0         0  '0 positional arguments'
              634  STORE_FAST               'prestate'

 L. 281       636  LOAD_GLOBAL              random
              638  LOAD_METHOD              seed
              640  LOAD_CONST               1
              642  CALL_METHOD_1         1  '1 positional argument'
              644  POP_TOP          

 L. 282       646  BUILD_LIST_0          0 
              648  BUILD_LIST_0          0 
              650  ROT_TWO          
              652  STORE_FAST               'x'
              654  STORE_FAST               'y'

 L. 284       656  SETUP_LOOP          712  'to 712'
              658  LOAD_GLOBAL              range
              660  LOAD_CONST               64
              662  CALL_FUNCTION_1       1  '1 positional argument'
              664  GET_ITER         
              666  FOR_ITER            710  'to 710'
              668  STORE_FAST               'i'

 L. 285       670  LOAD_FAST                'x'
              672  LOAD_METHOD              append
              674  LOAD_GLOBAL              random
              676  LOAD_METHOD              uniform
              678  LOAD_FAST                'mi'
              680  LOAD_FAST                'ma'
              682  CALL_METHOD_2         2  '2 positional arguments'
              684  CALL_METHOD_1         1  '1 positional argument'
              686  POP_TOP          

 L. 286       688  LOAD_FAST                'y'
              690  LOAD_METHOD              append
              692  LOAD_GLOBAL              random
              694  LOAD_METHOD              uniform
              696  LOAD_FAST                'mi'
              698  LOAD_FAST                'ma'
              700  CALL_METHOD_2         2  '2 positional arguments'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  POP_TOP          
          706_708  JUMP_BACK           666  'to 666'
              710  POP_BLOCK        
            712_0  COME_FROM_LOOP      656  '656'

 L. 287       712  LOAD_FAST                'ax'
              714  LOAD_ATTR                scatter
              716  LOAD_FAST                'x'
              718  LOAD_FAST                'y'
              720  LOAD_CONST               0.05
              722  LOAD_CONST               8
              724  LOAD_FAST                'lw'
              726  BINARY_MULTIPLY  
              728  LOAD_FAST                'starcolor'
              730  LOAD_CONST               None
              732  LOAD_CONST               3
              734  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              736  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              738  POP_TOP          

 L. 288       740  LOAD_FAST                'ax'
              742  LOAD_ATTR                scatter
              744  LOAD_FAST                'x'
              746  LOAD_FAST                'y'
              748  LOAD_CONST               0.1
              750  LOAD_CONST               4
              752  LOAD_FAST                'lw'
              754  BINARY_MULTIPLY  
              756  LOAD_FAST                'starcolor'
              758  LOAD_CONST               None
              760  LOAD_CONST               3
              762  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              764  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              766  POP_TOP          

 L. 289       768  LOAD_FAST                'ax'
              770  LOAD_ATTR                scatter
              772  LOAD_FAST                'x'
              774  LOAD_FAST                'y'
              776  LOAD_CONST               0.2
              778  LOAD_CONST               0.5
              780  LOAD_FAST                'lw'
              782  BINARY_MULTIPLY  
              784  LOAD_FAST                'starcolor'
              786  LOAD_CONST               None
              788  LOAD_CONST               3
              790  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              792  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              794  POP_TOP          

 L. 291       796  BUILD_LIST_0          0 
              798  BUILD_LIST_0          0 
              800  ROT_TWO          
              802  STORE_FAST               'x'
              804  STORE_FAST               'y'

 L. 292       806  SETUP_LOOP          862  'to 862'
              808  LOAD_GLOBAL              range
              810  LOAD_CONST               16
              812  CALL_FUNCTION_1       1  '1 positional argument'
              814  GET_ITER         
              816  FOR_ITER            860  'to 860'
              818  STORE_FAST               'i'

 L. 293       820  LOAD_FAST                'x'
              822  LOAD_METHOD              append
              824  LOAD_GLOBAL              random
              826  LOAD_METHOD              uniform
              828  LOAD_FAST                'mi'
              830  LOAD_FAST                'ma'
              832  CALL_METHOD_2         2  '2 positional arguments'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  POP_TOP          

 L. 294       838  LOAD_FAST                'y'
              840  LOAD_METHOD              append
              842  LOAD_GLOBAL              random
              844  LOAD_METHOD              uniform
              846  LOAD_FAST                'mi'
              848  LOAD_FAST                'ma'
              850  CALL_METHOD_2         2  '2 positional arguments'
              852  CALL_METHOD_1         1  '1 positional argument'
              854  POP_TOP          
          856_858  JUMP_BACK           816  'to 816'
              860  POP_BLOCK        
            862_0  COME_FROM_LOOP      806  '806'

 L. 295       862  LOAD_FAST                'ax'
              864  LOAD_ATTR                scatter
              866  LOAD_FAST                'x'
              868  LOAD_FAST                'y'
              870  LOAD_CONST               0.1
              872  LOAD_CONST               15
              874  LOAD_FAST                'lw'
              876  BINARY_MULTIPLY  
              878  LOAD_FAST                'starcolor'
              880  LOAD_CONST               None
              882  LOAD_CONST               3
              884  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              886  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              888  POP_TOP          

 L. 296       890  LOAD_FAST                'ax'
              892  LOAD_ATTR                scatter
              894  LOAD_FAST                'x'
              896  LOAD_FAST                'y'
              898  LOAD_CONST               0.1
              900  LOAD_CONST               5
              902  LOAD_FAST                'lw'
              904  BINARY_MULTIPLY  
              906  LOAD_FAST                'starcolor'
              908  LOAD_CONST               None
              910  LOAD_CONST               3
              912  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              914  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              916  POP_TOP          

 L. 297       918  LOAD_FAST                'ax'
              920  LOAD_ATTR                scatter
              922  LOAD_FAST                'x'
              924  LOAD_FAST                'y'
              926  LOAD_CONST               0.5
              928  LOAD_CONST               2
              930  LOAD_FAST                'lw'
              932  BINARY_MULTIPLY  
              934  LOAD_FAST                'starcolor'
              936  LOAD_CONST               None
              938  LOAD_CONST               3
              940  LOAD_CONST               ('alpha', 's', 'facecolor', 'edgecolor', 'zorder')
              942  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              944  POP_TOP          

 L. 298       946  LOAD_GLOBAL              random
              948  LOAD_METHOD              setstate
              950  LOAD_FAST                'prestate'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  POP_TOP          
              956  JUMP_FORWARD       1006  'to 1006'
            958_0  COME_FROM           520  '520'

 L. 301       958  LOAD_FAST                'ax'
              960  LOAD_ATTR                scatter
              962  LOAD_GLOBAL              getattr
              964  LOAD_FAST                'prim'
              966  LOAD_FAST                'axes'
              968  LOAD_CONST               0
              970  BINARY_SUBSCR    
              972  CALL_FUNCTION_2       2  '2 positional arguments'
              974  LOAD_GLOBAL              getattr
              976  LOAD_FAST                'prim'
              978  LOAD_FAST                'axes'
              980  LOAD_CONST               1
              982  BINARY_SUBSCR    
              984  CALL_FUNCTION_2       2  '2 positional arguments'
              986  LOAD_STR                 '*'
              988  LOAD_CONST               35
              990  LOAD_FAST                'lw'
              992  BINARY_MULTIPLY  
              994  LOAD_STR                 'black'
              996  LOAD_CONST               None
              998  LOAD_CONST               3
             1000  LOAD_CONST               ('marker', 's', 'facecolor', 'edgecolor', 'zorder')
             1002  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1004  POP_TOP          
           1006_0  COME_FROM           956  '956'

 L. 303      1006  BUILD_MAP_0           0 
             1008  STORE_FAST               'proj'

 L. 304  1010_1012  SETUP_LOOP         1816  'to 1816'
             1014  LOAD_FAST                'p_orb_pairs'
             1016  GET_ITER         
           1018_0  COME_FROM          1646  '1646'
         1018_1020  FOR_ITER           1814  'to 1814'
             1022  UNPACK_SEQUENCE_2     2 
             1024  STORE_FAST               'p'
             1026  STORE_FAST               'o'

 L. 305      1028  LOAD_GLOBAL              next
             1030  LOAD_FAST                'coloriterator'
             1032  CALL_FUNCTION_1       1  '1 positional argument'
             1034  STORE_FAST               'colori'

 L. 307      1036  LOAD_FAST                'primary'
             1038  LOAD_CONST               None
             1040  COMPARE_OP               is
         1042_1044  POP_JUMP_IF_FALSE  1052  'to 1052'
             1046  LOAD_FAST                'p'
             1048  LOAD_ATTR                jacobi_com
             1050  JUMP_FORWARD       1054  'to 1054'
           1052_0  COME_FROM          1042  '1042'
             1052  LOAD_FAST                'primary'
           1054_0  COME_FROM          1050  '1050'
             1054  STORE_FAST               'prim'

 L. 308      1056  LOAD_FAST                'fancy'
         1058_1060  POP_JUMP_IF_FALSE  1110  'to 1110'

 L. 309      1062  LOAD_FAST                'ax'
             1064  LOAD_ATTR                scatter
             1066  LOAD_GLOBAL              getattr
             1068  LOAD_FAST                'p'
             1070  LOAD_FAST                'axes'
             1072  LOAD_CONST               0
             1074  BINARY_SUBSCR    
             1076  CALL_FUNCTION_2       2  '2 positional arguments'
             1078  LOAD_GLOBAL              getattr
             1080  LOAD_FAST                'p'
             1082  LOAD_FAST                'axes'
             1084  LOAD_CONST               1
             1086  BINARY_SUBSCR    
             1088  CALL_FUNCTION_2       2  '2 positional arguments'
             1090  LOAD_CONST               25
             1092  LOAD_FAST                'lw'
             1094  BINARY_MULTIPLY  
             1096  LOAD_FAST                'colors'
             1098  LOAD_CONST               None
             1100  LOAD_CONST               3
             1102  LOAD_CONST               ('s', 'facecolor', 'edgecolor', 'zorder')
             1104  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1106  POP_TOP          
             1108  JUMP_FORWARD       1110  'to 1110'
           1110_0  COME_FROM          1108  '1108'
           1110_1  COME_FROM          1058  '1058'

 L. 320      1110  LOAD_FAST                'show_orbit'
             1112  LOAD_CONST               True
             1114  COMPARE_OP               is
         1116_1118  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 321      1120  LOAD_FAST                'trails'
             1122  LOAD_CONST               True
             1124  COMPARE_OP               is
         1126_1128  POP_JUMP_IF_FALSE  1134  'to 1134'
             1130  LOAD_CONST               0.0
             1132  JUMP_FORWARD       1136  'to 1136'
           1134_0  COME_FROM          1126  '1126'
             1134  LOAD_CONST               1.0
           1136_0  COME_FROM          1132  '1132'
             1136  STORE_FAST               'alpha_final'

 L. 323      1138  LOAD_FAST                'o'
             1140  LOAD_ATTR                a
             1142  LOAD_CONST               0.0
             1144  COMPARE_OP               <
             1146  STORE_FAST               'hyperbolic'

 L. 324      1148  LOAD_FAST                'hyperbolic'
             1150  LOAD_CONST               False
             1152  COMPARE_OP               is
         1154_1156  POP_JUMP_IF_FALSE  1314  'to 1314'

 L. 325      1158  LOAD_GLOBAL              np
             1160  LOAD_METHOD              array
             1162  LOAD_FAST                'p'
             1164  LOAD_ATTR                sample_orbit
             1166  LOAD_FAST                'Narc'
             1168  LOAD_CONST               1
             1170  BINARY_ADD       
             1172  LOAD_FAST                'prim'
             1174  LOAD_CONST               ('Npts', 'primary')
             1176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1178  CALL_METHOD_1         1  '1 positional argument'
             1180  STORE_DEREF              'pts'

 L. 326      1182  LOAD_CLOSURE             'pts'
             1184  BUILD_TUPLE_1         1 
             1186  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1188  LOAD_STR                 'OrbitPlotOneSlice.<locals>.<listcomp>'
             1190  MAKE_FUNCTION_8          'closure'
             1192  LOAD_GLOBAL              range
             1194  LOAD_CONST               3
             1196  CALL_FUNCTION_1       1  '1 positional argument'
             1198  GET_ITER         
             1200  CALL_FUNCTION_1       1  '1 positional argument'
             1202  UNPACK_SEQUENCE_3     3 
             1204  LOAD_FAST                'proj'
             1206  LOAD_STR                 'x'
             1208  STORE_SUBSCR     
             1210  LOAD_FAST                'proj'
             1212  LOAD_STR                 'y'
             1214  STORE_SUBSCR     
             1216  LOAD_FAST                'proj'
             1218  LOAD_STR                 'z'
             1220  STORE_SUBSCR     

 L. 327      1222  LOAD_GLOBAL              fading_line
             1224  LOAD_FAST                'proj'
             1226  LOAD_FAST                'axes'
             1228  LOAD_CONST               0
             1230  BINARY_SUBSCR    
             1232  BINARY_SUBSCR    
             1234  LOAD_FAST                'proj'
             1236  LOAD_FAST                'axes'
             1238  LOAD_CONST               1
             1240  BINARY_SUBSCR    
             1242  BINARY_SUBSCR    
             1244  LOAD_FAST                'colori'
             1246  LOAD_FAST                'alpha_final'
             1248  LOAD_FAST                'lw'
             1250  LOAD_FAST                'glow'
             1252  LOAD_CONST               ('alpha_final', 'lw', 'glow')
             1254  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1256  STORE_FAST               'lc'

 L. 328      1258  LOAD_GLOBAL              type
             1260  LOAD_FAST                'lc'
             1262  CALL_FUNCTION_1       1  '1 positional argument'
             1264  LOAD_GLOBAL              list
             1266  COMPARE_OP               is
         1268_1270  POP_JUMP_IF_FALSE  1300  'to 1300'

 L. 329      1272  SETUP_LOOP         1310  'to 1310'
             1274  LOAD_FAST                'lc'
             1276  GET_ITER         
             1278  FOR_ITER           1296  'to 1296'
             1280  STORE_FAST               'l'

 L. 330      1282  LOAD_FAST                'ax'
             1284  LOAD_METHOD              add_collection
             1286  LOAD_FAST                'l'
             1288  CALL_METHOD_1         1  '1 positional argument'
             1290  POP_TOP          
         1292_1294  JUMP_BACK          1278  'to 1278'
             1296  POP_BLOCK        
             1298  JUMP_FORWARD       1644  'to 1644'
           1300_0  COME_FROM          1268  '1268'

 L. 332      1300  LOAD_FAST                'ax'
             1302  LOAD_METHOD              add_collection
             1304  LOAD_FAST                'lc'
             1306  CALL_METHOD_1         1  '1 positional argument'
             1308  POP_TOP          
           1310_0  COME_FROM_LOOP     1272  '1272'
         1310_1312  JUMP_FORWARD       1644  'to 1644'
           1314_0  COME_FROM          1154  '1154'

 L. 335      1314  LOAD_GLOBAL              np
             1316  LOAD_METHOD              array
             1318  LOAD_FAST                'p'
             1320  LOAD_ATTR                sample_orbit
             1322  LOAD_FAST                'Narc'
             1324  LOAD_CONST               1
             1326  BINARY_ADD       
             1328  LOAD_FAST                'prim'
             1330  LOAD_CONST               False
             1332  LOAD_CONST               ('Npts', 'primary', 'useTrueAnomaly')
             1334  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  STORE_DEREF              'pts'

 L. 337      1340  LOAD_CLOSURE             'pts'
             1342  BUILD_TUPLE_1         1 
             1344  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1346  LOAD_STR                 'OrbitPlotOneSlice.<locals>.<listcomp>'
             1348  MAKE_FUNCTION_8          'closure'
             1350  LOAD_GLOBAL              range
             1352  LOAD_CONST               3
             1354  CALL_FUNCTION_1       1  '1 positional argument'
             1356  GET_ITER         
             1358  CALL_FUNCTION_1       1  '1 positional argument'
             1360  UNPACK_SEQUENCE_3     3 
             1362  LOAD_FAST                'proj'
             1364  LOAD_STR                 'x'
             1366  STORE_SUBSCR     
             1368  LOAD_FAST                'proj'
             1370  LOAD_STR                 'y'
             1372  STORE_SUBSCR     
             1374  LOAD_FAST                'proj'
             1376  LOAD_STR                 'z'
             1378  STORE_SUBSCR     

 L. 338      1380  LOAD_GLOBAL              fading_line
             1382  LOAD_FAST                'proj'
             1384  LOAD_FAST                'axes'
             1386  LOAD_CONST               0
             1388  BINARY_SUBSCR    
             1390  BINARY_SUBSCR    
             1392  LOAD_FAST                'proj'
             1394  LOAD_FAST                'axes'
             1396  LOAD_CONST               1
             1398  BINARY_SUBSCR    
             1400  BINARY_SUBSCR    
             1402  LOAD_FAST                'colori'
             1404  LOAD_FAST                'alpha_final'
             1406  LOAD_FAST                'lw'
             1408  LOAD_FAST                'glow'
             1410  LOAD_CONST               ('alpha_final', 'lw', 'glow')
             1412  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1414  STORE_FAST               'lc'

 L. 339      1416  LOAD_GLOBAL              type
             1418  LOAD_FAST                'lc'
             1420  CALL_FUNCTION_1       1  '1 positional argument'
             1422  LOAD_GLOBAL              list
             1424  COMPARE_OP               is
         1426_1428  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 340      1430  SETUP_LOOP         1468  'to 1468'
             1432  LOAD_FAST                'lc'
             1434  GET_ITER         
             1436  FOR_ITER           1454  'to 1454'
             1438  STORE_FAST               'l'

 L. 341      1440  LOAD_FAST                'ax'
             1442  LOAD_METHOD              add_collection
             1444  LOAD_FAST                'l'
             1446  CALL_METHOD_1         1  '1 positional argument'
             1448  POP_TOP          
         1450_1452  JUMP_BACK          1436  'to 1436'
             1454  POP_BLOCK        
             1456  JUMP_FORWARD       1468  'to 1468'
           1458_0  COME_FROM          1426  '1426'

 L. 343      1458  LOAD_FAST                'ax'
             1460  LOAD_METHOD              add_collection
             1462  LOAD_FAST                'lc'
             1464  CALL_METHOD_1         1  '1 positional argument'
             1466  POP_TOP          
           1468_0  COME_FROM          1456  '1456'
           1468_1  COME_FROM_LOOP     1430  '1430'

 L. 345      1468  LOAD_FAST                'trails'
             1470  LOAD_CONST               True
             1472  COMPARE_OP               is
         1474_1476  POP_JUMP_IF_FALSE  1482  'to 1482'
             1478  LOAD_CONST               0.2
             1480  JUMP_FORWARD       1484  'to 1484'
           1482_0  COME_FROM          1474  '1474'
             1482  LOAD_CONST               1.0
           1484_0  COME_FROM          1480  '1480'
             1484  STORE_FAST               'alpha'

 L. 346      1486  LOAD_GLOBAL              np
             1488  LOAD_METHOD              array
             1490  LOAD_FAST                'p'
             1492  LOAD_ATTR                sample_orbit
             1494  LOAD_FAST                'Narc'
             1496  LOAD_CONST               1
             1498  BINARY_ADD       
             1500  LOAD_FAST                'prim'
             1502  LOAD_CONST               False
             1504  LOAD_CONST               False
             1506  LOAD_CONST               ('Npts', 'primary', 'trailing', 'useTrueAnomaly')
             1508  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1510  CALL_METHOD_1         1  '1 positional argument'
             1512  STORE_DEREF              'pts'

 L. 347      1514  LOAD_CLOSURE             'pts'
             1516  BUILD_TUPLE_1         1 
             1518  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1520  LOAD_STR                 'OrbitPlotOneSlice.<locals>.<listcomp>'
             1522  MAKE_FUNCTION_8          'closure'
             1524  LOAD_GLOBAL              range
             1526  LOAD_CONST               3
             1528  CALL_FUNCTION_1       1  '1 positional argument'
             1530  GET_ITER         
             1532  CALL_FUNCTION_1       1  '1 positional argument'
             1534  UNPACK_SEQUENCE_3     3 
             1536  LOAD_FAST                'proj'
             1538  LOAD_STR                 'x'
             1540  STORE_SUBSCR     
             1542  LOAD_FAST                'proj'
             1544  LOAD_STR                 'y'
             1546  STORE_SUBSCR     
             1548  LOAD_FAST                'proj'
             1550  LOAD_STR                 'z'
             1552  STORE_SUBSCR     

 L. 348      1554  LOAD_GLOBAL              fading_line
             1556  LOAD_FAST                'proj'
             1558  LOAD_FAST                'axes'
             1560  LOAD_CONST               0
             1562  BINARY_SUBSCR    
             1564  BINARY_SUBSCR    
             1566  LOAD_FAST                'proj'
             1568  LOAD_FAST                'axes'
             1570  LOAD_CONST               1
             1572  BINARY_SUBSCR    
             1574  BINARY_SUBSCR    
             1576  LOAD_FAST                'colori'
             1578  LOAD_FAST                'alpha'
             1580  LOAD_FAST                'alpha'
             1582  LOAD_FAST                'lw'
             1584  LOAD_FAST                'glow'
             1586  LOAD_CONST               ('alpha_initial', 'alpha_final', 'lw', 'glow')
             1588  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1590  STORE_FAST               'lc'

 L. 349      1592  LOAD_GLOBAL              type
             1594  LOAD_FAST                'lc'
             1596  CALL_FUNCTION_1       1  '1 positional argument'
             1598  LOAD_GLOBAL              list
             1600  COMPARE_OP               is
         1602_1604  POP_JUMP_IF_FALSE  1634  'to 1634'

 L. 350      1606  SETUP_LOOP         1644  'to 1644'
             1608  LOAD_FAST                'lc'
             1610  GET_ITER         
             1612  FOR_ITER           1630  'to 1630'
             1614  STORE_FAST               'l'

 L. 351      1616  LOAD_FAST                'ax'
             1618  LOAD_METHOD              add_collection
             1620  LOAD_FAST                'l'
             1622  CALL_METHOD_1         1  '1 positional argument'
             1624  POP_TOP          
         1626_1628  JUMP_BACK          1612  'to 1612'
           1630_0  COME_FROM          1298  '1298'
             1630  POP_BLOCK        
             1632  JUMP_FORWARD       1644  'to 1644'
           1634_0  COME_FROM          1602  '1602'

 L. 353      1634  LOAD_FAST                'ax'
             1636  LOAD_METHOD              add_collection
             1638  LOAD_FAST                'lc'
             1640  CALL_METHOD_1         1  '1 positional argument'
             1642  POP_TOP          
           1644_0  COME_FROM          1632  '1632'
           1644_1  COME_FROM_LOOP     1606  '1606'
           1644_2  COME_FROM          1310  '1310'
           1644_3  COME_FROM          1116  '1116'

 L. 355      1644  LOAD_FAST                'periastron'
         1646_1648  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 356      1650  LOAD_GLOBAL              Particle
             1652  LOAD_FAST                'o'
             1654  LOAD_ATTR                a
             1656  LOAD_CONST               0.0
             1658  LOAD_FAST                'o'
             1660  LOAD_ATTR                inc
             1662  LOAD_FAST                'o'
             1664  LOAD_ATTR                omega
             1666  LOAD_FAST                'o'
             1668  LOAD_ATTR                Omega
             1670  LOAD_FAST                'o'
             1672  LOAD_ATTR                e
             1674  LOAD_FAST                'p'
             1676  LOAD_ATTR                m
             1678  LOAD_FAST                'prim'
             1680  LOAD_FAST                'sim'
             1682  LOAD_CONST               ('a', 'f', 'inc', 'omega', 'Omega', 'e', 'm', 'primary', 'simulation')
             1684  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1686  STORE_FAST               'newp'

 L. 357      1688  LOAD_FAST                'ax'
             1690  LOAD_ATTR                plot
             1692  LOAD_GLOBAL              getattr
             1694  LOAD_FAST                'prim'
             1696  LOAD_FAST                'axes'
             1698  LOAD_CONST               0
             1700  BINARY_SUBSCR    
             1702  CALL_FUNCTION_2       2  '2 positional arguments'
             1704  LOAD_GLOBAL              getattr
             1706  LOAD_FAST                'newp'
             1708  LOAD_FAST                'axes'
             1710  LOAD_CONST               0
             1712  BINARY_SUBSCR    
             1714  CALL_FUNCTION_2       2  '2 positional arguments'
             1716  BUILD_LIST_2          2 
             1718  LOAD_GLOBAL              getattr
             1720  LOAD_FAST                'prim'
             1722  LOAD_FAST                'axes'
             1724  LOAD_CONST               1
             1726  BINARY_SUBSCR    
             1728  CALL_FUNCTION_2       2  '2 positional arguments'
             1730  LOAD_GLOBAL              getattr
             1732  LOAD_FAST                'newp'
             1734  LOAD_FAST                'axes'
             1736  LOAD_CONST               1
             1738  BINARY_SUBSCR    
             1740  CALL_FUNCTION_2       2  '2 positional arguments'
             1742  BUILD_LIST_2          2 
             1744  LOAD_STR                 'dotted'
             1746  LOAD_FAST                'colori'
             1748  LOAD_CONST               1
             1750  LOAD_FAST                'lw'
             1752  LOAD_CONST               ('linestyle', 'c', 'zorder', 'lw')
             1754  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1756  POP_TOP          

 L. 358      1758  LOAD_FAST                'ax'
             1760  LOAD_ATTR                scatter
             1762  LOAD_GLOBAL              getattr
             1764  LOAD_FAST                'newp'
             1766  LOAD_FAST                'axes'
             1768  LOAD_CONST               0
             1770  BINARY_SUBSCR    
             1772  CALL_FUNCTION_2       2  '2 positional arguments'
             1774  BUILD_LIST_1          1 
             1776  LOAD_GLOBAL              getattr
             1778  LOAD_FAST                'newp'
             1780  LOAD_FAST                'axes'
             1782  LOAD_CONST               1
             1784  BINARY_SUBSCR    
             1786  CALL_FUNCTION_2       2  '2 positional arguments'
             1788  BUILD_LIST_1          1 
             1790  LOAD_STR                 'o'
             1792  LOAD_CONST               5.0
             1794  LOAD_FAST                'lw'
             1796  BINARY_MULTIPLY  
             1798  LOAD_STR                 'none'
             1800  LOAD_FAST                'colori'
             1802  LOAD_CONST               1
             1804  LOAD_CONST               ('marker', 's', 'facecolor', 'edgecolor', 'zorder')
             1806  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1808  POP_TOP          
         1810_1812  JUMP_BACK          1018  'to 1018'
             1814  POP_BLOCK        
           1816_0  COME_FROM_LOOP     1010  '1010'

Parse error at or near `COME_FROM_LOOP' instruction at offset 460_2


def plot_top_down_view(params_median, params_star, a=None, timestep=None, scaling=5.0, colors=sns.color_palette('deep'), linewidth=2, plot_arrow=False, ax=None):
    sim = rebound.Simulation()
    sim.add(m=1)
    for i, companion in enumerate(config.BASEMENT.settings['companions_all']):
        if i == 0:
            if timestep is None:
                timestep = params_median[(companion + '_epoch')]
            else:
                first_epoch = get_first_epoch(timestep, params_median[(companion + '_epoch')], params_median[(companion + '_period')])
                phase = calc_phase(timestep, params_median[(companion + '_period')], first_epoch)
                ecc = params_median[(companion + '_f_s')] ** 2 + params_median[(companion + '_f_c')] ** 2
                w = np.arccos(params_median[(companion + '_f_c')] / np.sqrt(ecc))
                inc = params_median[(companion + '_incl')] / 180.0 * np.pi
                if a is None:
                    a1 = params_star['R_star'] / params_median[(companion + '_radius_1')]
                    a1 *= 0.004650467260962157
                else:
                    a1 = a[i]
            if ecc > 0:
                sim.add(a=a1, inc=(inc - np.pi / 2.0), e=ecc, omega=w, f=(phase * 2 * np.pi))
        else:
            sim.add(a=a1, inc=(inc - -np.pi / 2.0), f=(phase * 2 * np.pi))

    fig, ax = OrbitPlot(sim, xlabel='AU', ylabel='AU', color=colors, lw=linewidth, ax=ax)
    for i, companion in enumerate(config.BASEMENT.settings['companions_all']):
        R_companion = params_star['R_star'] * params_median[(companion + '_rr')]
        R_companion *= 0.004650467260962157
        R_companion *= scaling
        x = sim.particles.get(i + 1).x
        y = sim.particles.get(i + 1).y
        p = Circle((x, y), R_companion, color=(colors[i]))
        ax.add_artist(p)

    if plot_arrow:
        x0, x1 = ax.get_xlim()
        plt.arrow((0.1 * x1), 0, (0.7 * x1), 0, color='silver', zorder=1)
    plt.axis('equal')
    return (
     fig, ax)
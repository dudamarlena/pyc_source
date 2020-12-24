# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/Logo.py
# Compiled at: 2019-05-09 13:29:43
# Size of source mod 2**32: 38046 bytes
from __future__ import division
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.axes import Axes
from logomaker.src.Glyph import Glyph
from logomaker.src.validate import validate_matrix
from logomaker.src.error_handling import check, handle_errors
from logomaker.src.colors import get_color_dict, get_rgb
from logomaker.src.matrix import transform_matrix

class Logo:
    __doc__ = "\n    Logo represents a basic logo, drawn on a specified axes object\n    using a specified matrix, which is supplied as a pandas dataframe.\n\n    attributes\n    ----------\n\n    df: (pd.DataFrame)\n        A matrix specifying character heights and positions. Rows correspond\n        to positions while columns correspond to characters. Column names\n        must be single characters and row indices must be integers.\n\n    color_scheme: (str, dict, or array with length 3)\n        Specification of logo colors. Default is 'gray'. Can take a variety of\n        forms.\n         - (str) A built-in Logomaker color scheme in which the color of each\n         character is determined that character's identity. Options are,\n             + For DNA/RNA: 'classic', 'grays', or 'base_paring'.\n             + For protein: 'hydrophobicity', 'chemistry', or 'charge'.\n         - (str) A built-in matplotlib color name such as 'k' or 'tomato'\n         - (list) An RGB array, i.e., 3 floats with values in the interval [0,1]\n         - (dict) A dictionary that maps characters to colors, E.g.,\n            {'A': 'blue',\n             'C': 'yellow',\n             'G': 'green',\n             'T': 'red'}\n\n    font_name: (str)\n        The character font to use when rendering the logo. For a list of\n        valid font names, run logomaker.list_font_names().\n\n    stack_order: (str)\n        Must be 'big_on_top', 'small_on_top', or 'fixed'. If 'big_on_top',\n        stack characters away from x-axis in order of increasing absolute value.\n        If 'small_on_top', stack glyphs away from x-axis in order of\n        decreasing absolute value. If 'fixed', stack glyphs from top to bottom\n        in the order that characters appear in the data frame.\n\n    center_values: (bool)\n        If True, the stack of characters at each position will be centered\n        around zero. This is accomplished by subtracting the mean value\n        in each row of the matrix from each element in that row.\n\n    baseline_width: (float >= 0.0)\n        Width of the logo baseline, drawn at value 0.0 on the y-axis.\n\n    flip_below: (bool)\n        If True, characters below the x-axis (which correspond to negative\n        values in the matrix) will be flipped upside down.\n\n    shade_below: (float in [0,1])\n        The amount of shading to use for characters drawn below the x-axis.\n        Larger numbers correspond to more shading (i.e., darker characters).\n\n    fade_below: (float in [0,1])\n        The amount of fading to use for characters drawn below the x-axis.\n        Larger numbers correspond to more fading (i.e., more transparent\n        characters).\n\n    fade_probabilities: (bool)\n        If True, the characters in each stack will be assigned an alpha value\n        equal to their height. This option only makes sense if df is a\n        probability matrix. For additional customization, use\n        Logo.fade_glyphs_in_probability_logo().\n\n    vpad: (float in [0,1])\n        The whitespace to leave above and below each character within that\n        character's bounding box. Note that, if vpad > 0, the height of the\n        character's bounding box (and not of the character itself) will\n        correspond to values in df.\n\n    vsep: (float >= 0)\n        Amount of whitespace to leave between the bounding boxes of rendered\n        characters. Unlike vpad, vsep is NOT relative to character height.\n\n    alpha: (float in [0,1])\n        Opacity to use when rendering characters. Note that, if this is used\n        together with fade_below or fade_probabilities, alpha will multiply\n        existing opacity values.\n\n    show_spines: (None or bool)\n        Whether a box should be drawn around the logo.  For additional\n        customization of spines, use Logo.style_spines().\n\n    ax: (matplotlib Axes object)\n        The matplotlb Axes object on which the logo is drawn.\n\n    zorder: (int >=0)\n        This governs what other objects drawn on ax will appear in front or\n        behind the rendered logo.\n\n    figsize: ([float, float]):\n        The default figure size for the rendered logo; only used if ax is\n        not supplied by the user.\n\n    **kwargs:\n        Additional key word arguments to send to the Glyph constructor.\n    "

    @handle_errors
    def __init__(self, df, color_scheme=None, font_name='sans', stack_order='big_on_top', center_values=False, baseline_width=0.5, flip_below=True, shade_below=0.0, fade_below=0.0, fade_probabilities=False, vpad=0.0, vsep=0.0, alpha=1.0, show_spines=None, ax=None, zorder=0, figsize=(10, 2.5), **kwargs):
        self.df = df
        self.color_scheme = color_scheme
        self.font_name = font_name
        self.stack_order = stack_order
        self.center_values = center_values
        self.baseline_width = baseline_width
        self.flip_below = flip_below
        self.shade_below = shade_below
        self.fade_below = fade_below
        self.fade_probabilities = fade_probabilities
        self.vpad = vpad
        self.vsep = vsep
        self.alpha = alpha
        self.show_spines = show_spines
        self.zorder = zorder
        self.figsize = figsize
        self.ax = ax
        self.glyph_kwargs = kwargs
        self.has_been_drawn = False
        self._input_checks()
        self.L = len(self.df)
        self.cs = np.array([c for c in self.df.columns])
        self.C = len(self.cs)
        self.rgb_dict = get_color_dict(self.color_scheme, self.cs)
        self.ps = np.array([p for p in self.df.index])
        if self.center_values:
            self.df = transform_matrix((self.df), center_values=True)
        if self.ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(self.figsize))
            self.ax = ax
        self._compute_glyphs()
        self.style_glyphs_below(shade=(self.shade_below), fade=(self.fade_below),
          flip=(self.flip_below))
        if self.fade_probabilities:
            self.fade_glyphs_in_probability_logo(v_alpha0=0, v_alpha1=1)
        self.draw()

    def _input_checks(self):
        """
        Validate parameters passed to the Logo constructor EXCEPT for
        color_scheme; that is validated in the Logo constructor
        """
        self.df = validate_matrix(self.df)
        check(isinstance(self.font_name, str), 'type(font_name) = %s must be of type str' % type(self.font_name))
        valid_stack_orders = {
         'big_on_top', 'small_on_top', 'fixed'}
        check(self.stack_order in valid_stack_orders, 'stack_order = %s; must be in %s.' % (
         self.stack_order, valid_stack_orders))
        check(isinstance(self.center_values, bool), 'type(center_values) = %s; must be of type bool.' % type(self.center_values))
        check(isinstance(self.baseline_width, (int, float)), 'type(baseline_width) = %s must be of type number' % type(self.baseline_width))
        check(self.baseline_width >= 0.0, 'baseline_width = %s must be >= 0.0' % self.baseline_width)
        check(isinstance(self.flip_below, bool), 'type(flip_below) = %s; must be of type bool ' % type(self.flip_below))
        check(isinstance(self.shade_below, (float, int)), 'type(shade_below) = %s must be of type float' % type(self.shade_below))
        check(0.0 <= self.shade_below <= 1.0, 'shade_below must be between 0 and 1')
        check(isinstance(self.fade_below, (float, int)), 'type(fade_below) = %s must be of type float' % type(self.fade_below))
        check(0.0 <= self.fade_below <= 1.0, 'fade_below must be between 0 and 1')
        check(isinstance(self.fade_probabilities, bool), 'type(fade_probabilities) = %s; must be of type bool ' % type(self.fade_probabilities))
        check(isinstance(self.vpad, (float, int)), 'type(vpad) = %s must be of type float' % type(self.vpad))
        check(0.0 <= self.vpad <= 1.0, 'vpad must be between 0 and 1')
        check(isinstance(self.vsep, (float, int)), 'type(vsep) = %s; must be of type float or int ' % type(self.vsep))
        check(self.vsep >= 0, 'vsep = %d must be greater than 0 ' % self.vsep)
        check(isinstance(self.alpha, (float, int)), 'type(alpha) = %s must be of type float' % type(self.alpha))
        check(0.0 <= self.alpha <= 1.0, 'alpha must be between 0 and 1')
        check(isinstance(self.show_spines, bool) or self.show_spines is None, 'show_spines = %s; show_spines must be None or boolean.' % repr(self.show_spines))
        check(isinstance(self.ax, Axes) or self.ax is None, 'ax = %s; ax must be None or a matplotlib.Axes object.' % repr(self.ax))
        check(isinstance(self.zorder, (float, int)), 'type(zorder) = %s; zorder must be a number.' % type(self.zorder))
        check(isinstance(self.figsize, (tuple, list, np.ndarray)), 'type(figsize) = %s; figsize must be array-like.' % type(self.figsize))
        self.figsize = tuple(self.figsize)
        check(len(self.figsize) == 2, 'figsize must have length two.')
        check(all([isinstance(n, (int, float)) and n > 0 for n in self.figsize]), 'all elements of figsize array must be numbers > 0.')

    @handle_errors
    def style_glyphs(self, color_scheme=None, **kwargs):
        """
        Modifies the properties of all characters in a Logo.

        parameters
        ----------

        color_scheme: (str, dict, or array with length 3)
            Specification of logo colors. Default is 'gray'. Can take a variety of
            forms.
             - (str) A built-in Logomaker color scheme in which the color of each
             character is determined that character's identity. Options are,
                 + For DNA/RNA: 'classic', 'grays', or 'base_paring'.
                 + For protein: 'hydrophobicity', 'chemistry', or 'charge'.
             - (str) A built-in matplotlib color name such as 'k' or 'tomato'
             - (list) An RGB array, i.e., 3 floats with values in the interval [0,1]
             - (dict) A dictionary that maps characters to colors, E.g.,
                {'A': 'blue',
                 'C': 'yellow',
                 'G': 'green',
                 'T': 'red'}

        **kwargs:
            Keyword arguments to pass to Glyph.set_attributes()

        returns
        -------
        None
        """
        if color_scheme is not None:
            self.color_scheme = color_scheme
            self.rgb_dict = get_color_dict(self.color_scheme, self.cs)
        for key in ('zorder', 'vpad', 'font_name'):
            if key in kwargs.keys():
                self.__dict__[key] = kwargs[key]

        for g in self.glyph_list:
            if color_scheme is not None:
                kwargs['color'] = self.rgb_dict[g.c]
            (g.set_attributes)(**kwargs)

    @handle_errors
    def fade_glyphs_in_probability_logo(self, v_alpha0=0.0, v_alpha1=1.0):
        """
        Fades glyphs in probability logo according to value.

        parameters
        ----------

        v_alpha0, v_alpha1: (number in [0,1])
            Matrix values marking values that are rendered using
            alpha=0 and alpha=1, respectively. These values must satisfy
            v_alpha0 < v_alpha1.

        returns
        -------
        None
         """
        check(isinstance(v_alpha0, (float, int)), 'type(v_alpha0) = %s must be a number' % type(v_alpha0))
        check(0.0 <= v_alpha0 <= 1.0, 'v_alpha0 must be between 0 and 1; value is %f.' % v_alpha0)
        check(isinstance(v_alpha1, (float, int)), 'type(v_alpha1) = %s must be a number' % type(v_alpha1))
        check(0.0 <= v_alpha1 <= 1.0, 'v_alpha1 must be between 0 and 1; value is %f' % v_alpha1)
        check(v_alpha0 < v_alpha1, 'must have v_alpha0 < v_alpha1;here, v_alpha0 = %f and v_alpha1 = %f' % (
         v_alpha0, v_alpha1))
        self.df = validate_matrix((self.df), matrix_type='probability')
        for p in self.ps:
            for c in self.cs:
                v = self.df.loc[(p, c)]
                g = self.glyph_df.loc[(p, c)]
                if v <= v_alpha0:
                    alpha = 0
                else:
                    if v >= v_alpha1:
                        alpha = 1
                    else:
                        alpha = (v - v_alpha0) / (v_alpha1 - v_alpha0)
                g.set_attributes(alpha=alpha)

    @handle_errors
    def style_glyphs_below(self, color=None, alpha=None, shade=0.0, fade=0.0, flip=None, **kwargs):
        """
        Modifies the properties of all characters drawn below the x-axis.

        parameters
        ----------

        color: (color specification)
            Color to use before shade is applied.

        alpha: (number in [0,1])
            Opacity to use when rendering characters, before fade is applied.

        shade: (number in [0,1])
            The amount to shade characters below the x-axis.

        fade: (number in [0,1])
            The amount to fade characters below the x-axis.

        flip: (bool)
            If True, characters below the x-axis will be flipped upside down.

        **kwargs:
            Keyword arguments to pass to Glyph.set_attributes(), but only
            for characters below the x-axis.

        returns
        -------
        None
        """
        if color is not None:
            color = get_rgb(color)
        else:
            if alpha is not None:
                check(isinstance(alpha, (float, int)), 'type(alpha) = %s must be a float or int' % type(alpha))
                self.alpha = float(alpha)
                check(0 <= alpha <= 1.0, 'alpha must be between 0.0 and 1.0 (inclusive)')
            check(isinstance(shade, (float, int)), 'type(shade) = %s must be a number' % type(shade))
            check(0.0 <= shade <= 1.0, 'shade must be between 0 and 1; value is %f.' % shade)
            check(isinstance(fade, (float, int)), 'type(fade) = %s must be a number' % type(fade))
            check(0.0 <= fade <= 1.0, 'fade must be between 0 and 1; value is %f' % fade)
            if flip is not None:
                check(isinstance(flip, bool), 'type(flip) = %s; must be of type bool ' % type(flip))
        for p in self.ps:
            for c in self.cs:
                v = self.df.loc[(p, c)]
                if v < 0:
                    g = self.glyph_df.loc[(p, c)]
                    if color is None:
                        this_color = get_rgb(g.color)
                    else:
                        this_color = color
                    if alpha is None:
                        this_alpha = g.alpha
                    else:
                        this_alpha = alpha
                    (g.set_attributes)(color=this_color * (1.0 - shade), alpha=this_alpha * (1.0 - fade), 
                     flip=flip, **kwargs)

    @handle_errors
    def style_single_glyph(self, p, c, **kwargs):
        """
        Modifies the properties of a single character in Logo.

        parameters
        ----------

        p: (int)
            Position of modified glyph. Must index a row in the matrix df passed
            to the Logo constructor.

        c: (str of length 1)
            Character to modify. Must be the name of a column in the matrix df
            passed to the Logo constructor.

        **kwargs:
            Keyword arguments to pass to Glyph.set_attributes()

        returns
        -------
        None
        """
        check(isinstance(p, int), 'type(p) = %s must be of type int' % type(p))
        check(p in self.glyph_df.index, 'p=%s is not a valid position' % p)
        check(isinstance(c, str), 'type(c) = %s must be of type str' % type(c))
        check(len(c) == 1, 'c = %s; must have length 1.' % repr(c))
        check(c in self.glyph_df.columns, 'c=%s is not a valid character' % c)
        g = self.glyph_df.loc[(p, c)]
        (g.set_attributes)(**kwargs)

    @handle_errors
    def style_glyphs_in_sequence(self, sequence, **kwargs):
        """
        Restyles the glyphs in a specific sequence.

        parameters
        ----------
        sequence: (str)
            A string the same length as the logo, specifying which character
            to restyle at each position. Characters in sequence that are not
            in the columns of the Logo's df are ignored.

        **kwargs:
            Keyword arguments to pass to Glyph.set_attributes()

        returns
        -------
        None
        """
        check(isinstance(sequence, str), 'type(sequence) = %s must be of type str' % type(sequence))
        check(len(sequence) == self.L, 'sequence to restyle (length %d) ' % len(sequence) + 'must have same length as logo (length %d).' % self.L)
        for i, p in enumerate(self.glyph_df.index):
            c = sequence[i]
            if c in self.cs:
                (self.style_single_glyph)(p, c, **kwargs)

    @handle_errors
    def highlight_position(self, p, **kwargs):
        """
        Draws a rectangular box highlighting a specific position.

        parameters
        ----------
        p: (int)
            Single position to highlight.

        **kwargs:
            Other parameters to pass to highlight_position_range()

        returns
        -------
        None
        """
        check(isinstance(p, int), 'type(p) = %s must be of type int' % type(p))
        (self.highlight_position_range)(pmin=p, pmax=p, **kwargs)

    @handle_errors
    def highlight_position_range(self, pmin, pmax, padding=0.0, color='yellow', edgecolor=None, floor=None, ceiling=None, zorder=-2, **kwargs):
        """
        Draws a rectangular box highlighting multiple positions within the Logo

        parameters
        ----------
        pmin: (int)
            Lowest position to highlight.
            
        pmax: (int)
            Highest position to highlight.
            
        padding: (number >= -0.5)
            Amount of padding to add on the left and right sides of highlight.
            
        color: (None or matplotlib color)
            Color to use for highlight. Can be a named matplotlib color or
            an RGB array.

        edgecolor: (None or matplotlib color)
            Color to use for highlight box edges. Can be a named matplotlib
            color or an RGB array.
            
        floor: (None number)
            Lowest y-axis extent of highlight box. If None, is set to
            ymin of the Axes object.
            
        ceiling: (None or number)
            Highest y-axis extent of highlight box. If None, is set to
            ymax of the Axes object.
            
        zorder: (number)
            This governs which other objects drawn on ax will appear in front or
            behind of the highlight. Logo characters are, by default, drawn in
            front of the highlight box.

        returns
        -------
        None
        """
        ymin, ymax = self.ax.get_ylim()
        check(isinstance(pmin, (float, int)), 'type(pmin) = %s must be a number' % type(pmin))
        check(isinstance(pmax, (float, int)), 'type(pmax) = %s must be a number' % type(pmax))
        check(pmin <= pmax, 'pmin <= pmax not satisfied.')
        check(isinstance(padding, (float, int)) and padding >= -0.5, 'padding = %s must be a number >= -0.5' % repr(padding))
        if color is not None:
            color = get_rgb(color)
        else:
            if edgecolor is not None:
                edgecolor = get_rgb(edgecolor)
            else:
                if floor is None:
                    floor = ymin
                else:
                    check(isinstance(floor, (float, int)), 'type(floor) = %s must be a number' % type(floor))
            if ceiling is None:
                ceiling = ymax
            else:
                check(isinstance(ceiling, (float, int)), 'type(ceiling) = %s must be a number' % type(ceiling))
        check(floor <= ceiling, 'must have floor <= ceiling; as is, floor = %f, ceiling = %s' % (
         floor, ceiling))
        check(isinstance(zorder, (float, int)), 'type(zorder) = %s; must a float or int.' % type(zorder))
        x = pmin - 0.5 - padding
        y = floor
        width = pmax - pmin + 1 + 2 * padding
        height = ceiling - floor
        patch = Rectangle(xy=(x, y), width=width, 
         height=height, 
         facecolor=color, 
         edgecolor=edgecolor, 
         zorder=zorder, **kwargs)
        self.ax.add_patch(patch)

    @handle_errors
    def draw_baseline(self, zorder=-1, color='black', linewidth=0.5, **kwargs):
        """
        Draws a horizontal line along the x-axis.

        parameters
        ----------

        zorder: (number)
            This governs what other objects drawn on ax will appear in front or
            behind the baseline. Logo characters are, by default, drawn in front
            of the baseline.

        color: (matplotlib color)
            Color to use for the baseline. Can be a named matplotlib color or an
            RGB array.

        linewidth: (number >= 0)
            Width of the baseline.

        **kwargs:
            Additional keyword arguments to be passed to ax.axhline()

        returns
        -------
        None
        """
        check(isinstance(zorder, (float, int)), 'type(zorder) = %s; must a float or int.' % type(zorder))
        color = get_rgb(color)
        check(isinstance(linewidth, (float, int)), 'type(linewidth) = %s; must be a number ' % type(linewidth))
        check(linewidth >= 0, 'linewidth must be >= 0')
        (self.ax.axhline)(zorder=zorder, color=color, 
         linewidth=linewidth, **kwargs)

    @handle_errors
    def style_xticks(self, anchor=0, spacing=1, fmt='%d', rotation=0.0, **kwargs):
        """
        Formats and styles tick marks along the x-axis.

        parameters
        ----------

        anchor: (int)
            Anchors tick marks at a specific number. Even if this number
            is not within the x-axis limits, it fixes the register for
            tick marks.

        spacing: (int > 0)
            The spacing between adjacent tick marks

        fmt: (str)
            String used to format tick labels.

        rotation: (number)
            Angle, in degrees, with which to draw tick mark labels.

        **kwargs:
            Additional keyword arguments to be passed to ax.set_xticklabels()

        returns
        -------
        None
        """
        check(isinstance(anchor, int), 'type(anchor) = %s must be of type int' % type(anchor))
        check(isinstance(spacing, int) and spacing > 0, 'spacing = %s must be an int > 0' % repr(spacing))
        check(isinstance(fmt, str), 'type(fmt) = %s must be of type str' % type(fmt))
        check(isinstance(rotation, (float, int)), 'type(rotation) = %s; must be of type float or int ' % type(rotation))
        p_min = min(self.ps)
        p_max = max(self.ps)
        ps = np.arange(p_min, p_max + 1)
        xticks = ps[((ps - anchor) % spacing == 0)]
        self.ax.set_xticks(xticks)
        xticklabels = [fmt % p for p in xticks]
        (self.ax.set_xticklabels)(xticklabels, rotation=rotation, **kwargs)

    @handle_errors
    def style_spines(self, spines=('top', 'bottom', 'left', 'right'), visible=True, color='black', linewidth=1.0, bounds=None):
        """
        Styles the spines of the Axes object in which the logo is drawn.
        Note: "spines" refers to the edges of the Axes bounding box.

        parameters
        ----------

        spines: (tuple of str)
            Specifies which of the four spines to modify. The default value
            for this parameter lists all four spines.

        visible: (bool)
            Whether to show or not show the spines listed in the parameter
            spines.

        color: (matplotlib color)
            Color of the spines. Can be a named matplotlib color or an
            RGB array.

        linewidth: (float >= 0)
            Width of lines used to draw the spines.

        bounds: (None or [float, float])
            If not None, specifies the values between which a spine (or spines)
            will be drawn.

        returns
        -------
        None
        """
        self.show_spines = None
        check(isinstance(spines, (tuple, list, set)), 'type(spines) = %s; must be of type (tuple, list, set) ' % type(spines))
        spines = set(spines)
        valid_spines = {
         'top', 'bottom', 'left', 'right'}
        check(spines <= valid_spines, 'spines has invalid entry; valid entries are: %s' % repr(valid_spines))
        check(isinstance(visible, bool), 'type(visible) = %s; must be of type bool ' % type(visible))
        check(isinstance(linewidth, (float, int)), 'type(linewidth) = %s; must be a number ' % type(linewidth))
        check(linewidth >= 0, 'linewidth must be >= 0')
        color = get_rgb(color)
        if bounds is not None:
            bounds_types = (
             list, tuple, np.ndarray)
            check(isinstance(bounds, bounds_types), 'type(bounds) = %s; must be one of %s' % (
             type(bounds), bounds_types))
            check(len(bounds) == 2, 'len(bounds) = %d; must be %d' % (len(bounds), 2))
            check(all([isinstance(bound, (float, int)) for bound in bounds]), 'bounds = %s; all entries must be numbers' % repr(bounds))
            check(bounds[0] < bounds[1], 'bounds = %s; must have bounds[0] < bounds[1]' % repr(bounds))
        for name, spine in self.ax.spines.items():
            if name in spines:
                spine.set_visible(visible)
                spine.set_color(color)
                spine.set_linewidth(linewidth)
                if bounds is not None:
                    spine.set_bounds(bounds[0], bounds[1])

    def draw(self, clear=False):
        """
        Draws characters in Logo.

        parameters
        ----------

        clear: (bool)
            If True, Axes will be cleared before logo is drawn.

        returns
        -------
        None
        """
        check(isinstance(clear, bool), 'type(clear) = %s; must be of type bool ' % type(clear))
        if clear:
            self.ax.clear()
            for g in self.glyph_list:
                g.draw()

        self.draw_baseline(linewidth=(self.baseline_width))
        xmin = min([g.p - 0.5 * g.width for g in self.glyph_list])
        xmax = max([g.p + 0.5 * g.width for g in self.glyph_list])
        self.ax.set_xlim([xmin, xmax])
        ymin = min([g.floor for g in self.glyph_list])
        ymax = max([g.ceiling for g in self.glyph_list])
        self.ax.set_ylim([ymin, ymax])
        if self.show_spines is not None:
            self.style_spines(visible=(self.show_spines))

    def _compute_glyphs(self):
        """
        Specifies the placement and styling of all glyphs within the logo.
        """
        glyph_df = pd.DataFrame()
        for p in self.ps:
            vs = np.array(self.df.loc[p, :])
            if self.stack_order == 'big_on_top':
                ordered_indices = np.argsort(vs)
            else:
                if self.stack_order == 'small_on_top':
                    tmp_vs = np.zeros(len(vs))
                    indices = vs != 0
                    tmp_vs[indices] = 1.0 / vs[indices]
                    ordered_indices = np.argsort(tmp_vs)
                else:
                    if self.stack_order == 'fixed':
                        ordered_indices = np.array(range(len(vs)))[::-1]
                    else:
                        assert False, 'This line of code should never be called.'
            vs = vs[ordered_indices]
            cs = [str(c) for c in self.cs[ordered_indices]]
            floor = sum((vs - self.vsep) * (vs < 0)) + self.vsep / 2.0
            for v, c in zip(vs, cs):
                ceiling = floor + abs(v)
                this_color = self.rgb_dict[c]
                flip = v < 0 and self.flip_below
                glyph = Glyph(p, c, ax=self.ax, 
                 floor=floor, 
                 ceiling=ceiling, 
                 color=this_color, 
                 flip=flip, 
                 zorder=self.zorder, 
                 font_name=self.font_name, 
                 alpha=self.alpha, 
                 vpad=self.vpad, **self.glyph_kwargs)
                glyph_df.loc[(p, c)] = glyph
                floor = ceiling + self.vsep

        self.glyph_df = glyph_df
        self.glyph_list = [g for g in self.glyph_df.values.ravel() if isinstance(g, Glyph)]
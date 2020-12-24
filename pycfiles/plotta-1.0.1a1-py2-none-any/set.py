# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/gdelraye/Documents/workspace/plotsettings/build/lib/plotsettings/set.py
# Compiled at: 2014-10-20 14:55:56
__doc__ = "\nEasily format figures to match the publication requirements of an academic journal. \nFigure settings can be determined using the defaults provided in the 'journals' module,\nwhich currently supports the following journals: \n\n    * Cell (use argument 'Cell')\n    * Copeia (use argument 'Copeia')\n    * Deep Sea Research II (use argument 'DSRII')\n    * Ecology Letters (use argument 'EcolLett')\n    * Global Change Biology (use argument 'GlobChangeBio')\n    * Global Environmental Change (use argument 'GlobEnvChange')\n    * Integrative and Comparative Biology (use argument 'IntCompBiol')\n    * Journal of Experimental Biology (use argument 'JEB')\n    * Limnology and Oceanography (use argument 'LimnolOcean')\n    * Marine Ecology Progress Series (use argument 'MEPS')\n    * Nature magazine (use argument 'Nature')\n    * Proceedings of the National Academy of Sciences, USA (use argument 'PNAS')\n    * Proceedings of the Royal Society B (use argument 'ProcRoySocB')\n    * Public Library of Science One (use argument 'PLOSOne')\n    * Public Library of Science Biology (use argument 'PLOSBio')\n    * Science magazine (use argument 'Science')\n    * Presentation (okay, this is not a journal but it's still useful for outputting \n      figures to presentation slides; access with the argument 'Presentation')\n    \nFor journals not in the above list, custom settings can be provided by creating a module \non the python path containing a dictionary named 'journals' with the following structure::\n\n    journals = {'journal1':      {'rcParams':     {'param1': value1,\n                                                   'param2': value2 ...}, \n                                  'figsize':      {'param1': value1,\n                                                   'param2': value2 ...},\n                                  'panel_labels': {'param1': value1,\n                                                   'param2': value2 ...},\n                'journal2':      {'rcParams':     {'param1': value1,\n                                                   'param2': value2 ...}, \n                                  'figsize':      {'param1': value1,\n                                                   'param2': value2 ...},\n                                  'panel_labels': {'param1': value1,\n                                                   'param2': value2 ...},\n                'journal3'...\n                }\n                \nwhere 'journalx' are the identifying names of academic journals (e.g. 'Nature'), with\nthe specifications for each journal being divided into 3 dictionaries:\n\n    * rcParams: All parameters are optional. Any valid input to pyplot.rcParams (for\n      example font name and sizes, default linewidths) is accepted. Definitions of valid \n      keys to rcParams can be found `here <http://matplotlib.org/users/customizing.html>`_.\n    * figsize: Set figure dimension calculations. Requires the parameters column_width, \n      gutter_width, and units. The parameter max_height is optional. See below for details.\n    * panel_labels: Set default panel labels (i.e. the text that identifies each subplot in\n      a figure as A, B, C, etc.). All parameters are optional. See below for details.\n  \nThe possible non-rcParams parameters are:\n    \n    * figsize:\n    \n        * column_width (required) - the maximum width a figure is allowed to be while still \n          fitting withing a single column.\n        * gutter_width (required) - the width of the gutter (space between columns). This can \n          usually be found by comparing the maximum width that a journal allows for a single-\n          column figure with the maximum width of a 2-column figure. For example, PLOS One\n          allows a 1-column figure to be 83 mm in width and a 2-column figure to be 173.5 mm,\n          meaning that the gutter width (173.5 - 83*2) must be 7.5 mm wide.\n        * max_height (optional) - the maximum height a figure is allowed to be while fitting \n          on a single page (i.e. the page height).\n        * units (required) - the units in which the above are reported. Can be one of 'mm', \n          'cm', 'inch', or 'pts'\n    \n    * panel_labels:\n    \n        * fontweight (optional) - the font weight of panel annotations (e.g. A, B, C etc.).\n          Default is 'bold'\n        * case (optional) - whether to capitalize ('upper') or not capitalize\n          ('lower') the panel labels.\n        * prefix (optional) - characters to prepend to panel label (e.g. if the desired\n          label style is (A), (B), etc., set label_prefix to ')').\n        * suffix (optional) - characters to append to panel label (e.g. if the desired\n          label style is a., b., etc., set label_suffix = '.')\n        * fontsize (optional) - font size in pts of the label. Defaults to rcParams['font.size']\n\nCreated on Oct 10, 2014\n\n@author: gdelraye\n"
from matplotlib import pyplot
import importlib, warnings, copy, string

class Set:
    """Set matplotlib figure parameters to conform to academic journal requirements, and
    easily specify figure dimensions.
    
    Usage example:
    
    First set the journal you want to submit to::
    
            publishable = Set('MEPS') # Lets publish in the Marine Ecology Progress Series!
            
    Then set the dimensions of a particular figure with the line::
    
        publishable.set_figsize(n_columns = 1, n_rows = 1)
        
    This will cause the next figure that is drawn to be 1 column wide (81 mm for MEPS) x 1 
    row high (the concept of 'rows' is a little made up, but the default is that one row is
    equal to one column width multiplied by the golden ratio, so in this case 50.1 mm). Once 
    the first figure is drawn, we can set the next figure to be 2 columns wide and 1 row 
    tall and this time set the row height to be equal to the column width::
    
        publishable.set_figsize(2, 1, aspect_ratio = 1)
        
    Importantly, plotsettings doesn't just calculate the width of a 2-column figure as two
    times the width of one column, but includes the width of the gutter (the space between
    columns on a page) as well. Therefore, the figure that follows the above line will end
    up being 169 mm wide (2 columns of 81 mm each plus a 7 mm gutter) and 81 mm tall (row
    height = 1*column width).
    """

    def __init__(self, journal_name, module='plotsettings.journals'):
        """Import a dictionary containing default plot settings for each journal, and
        set them to values appropriate for the indicated journal.
        
        Inputs:
        
            * journal_name (str) - identifying name of a journal. Must be a valid key 
              for the dictionary 'journals' contained in 'module'
            * module (str) - name of a module in the pythonpath containing the settings
              for each journal. Defaults to the 'journals' module in this package. To
              use an external module (e.g. 'my_journal_settings.py'), input the module
              name without extensions
              
        Example:
        
        # Using the default journal settings:
        >>> from matplotlib import rcParams
        >>> publishable = Set('DSRII') # Settings for the journal Deep Sea Research II
        >>> rcParams['font.sans-serif'] # Check that rcparams has been changed
        ['Arial']
        
        # Import journal settings from a user-defined file:
        >>> user_module = 'plotsettings.test.custom_journals' # A module on the Pythonpath
        >>> publishable = Set('Journal of Irreproducible Results', user_module)
        >>> rcParams['font.sans-serif'] # Check that rcparams has been changed
        ['Comic Sans MS']
        """
        self.journals = importlib.import_module(module).journals
        params = copy.deepcopy(self.journals[journal_name])
        pyplot.rcParams.update(params['rcParams'])
        self.size_dict = params['figsize']
        self.size_dict['column_width'] = self._inches(self.size_dict['column_width'], self.size_dict['units'])
        self.size_dict['gutter_width'] = self._inches(self.size_dict['gutter_width'], self.size_dict['units'])
        self.size_dict['max_height'] = self._inches(self.size_dict.get('max_height', float('inf')), self.size_dict['units'])
        self.label_dict = params['panel_labels']
        self.label_dict['fontsize'] = self.label_dict.get('fontsize', params['rcParams']['font.size'])

    def set_figsize(self, n_columns, n_rows=1, aspect_ratio=0.618):
        """Set the figure size according to the number of columns and rows that
        the figure should cover. By default, the 'rows' are calculated as a height
        equal to the width of a column times the golden ratio.
        
        Inputs:
        
            * n_columns (scalar) - number of columns that the figure should cover
            * n_rows (scalar) - number of rows that the figure should cover. The row
              height is defined as the column height multiplied by the aspect
              ratio.
            * aspect_ratio (scalar) - ratio of row height to column width. Defaults
              to the golden ratio (0.618).
              
        Example:
        
        >>> from matplotlib import rcParams
        >>> publishable = Set('DSRII') # Settings for the journal Deep Sea Research II
        >>> publishable.set_figsize(1, 1, aspect_ratio = 1) # Figure dimensions = column_width x column_width
        >>> height, width = rcParams['figure.figsize'] # Check the figure dimensions
        >>> print '%.3f, %.3f' %(height, width) # Check the figure dimensions
        3.543, 3.543
        >>> publishable.set_figsize(2, 1, 0.5) # Two-columned figure width = 2*column_width + 1*gutter_width
        >>> height, width = rcParams['figure.figsize'] # Check the figure dimensions
        >>> print '%.3f, %.3f' %(height, width) # Check the figure dimensions
        7.480, 1.772
        >>> publishable.set_figsize(2, 3, 1) # This figure is too tall to fit in one page
        Traceback (most recent call last):
        UserWarning: Specified figure height exceeds maximum height. Setting to maximum height instead
        """
        row_height = self.size_dict['column_width'] * aspect_ratio
        figure_height = row_height * n_rows
        if figure_height > self.size_dict['max_height']:
            warnings.warn('Specified figure height exceeds maximum height. Setting to maximum height instead')
            figure_height = self.size_dict['max_height']
        pyplot.rcParams['figure.figsize'] = (
         self._calc_width(n_columns), figure_height)

    def panel_labels(self, fig=None, **kwargs):
        """Annotate the subplots as panels (e.g. with letter A, B, C etc.) according to the journal defaults.
        
        Inputs:
        
            * fig (object) - a matplotlib figure object. Defaults to the currently opened figure.
            * kwargs - see function panel_labels for a description of valid kwargs
        
        Usage::
        
            from matplotlib import pyplot
            fig, ax = pyplot.subplots(1, 1)
            publishable = Set('Copeia')
            publishable.set_figsize(1, 1)
            ax.plot(numpy.arange(10), 'b-')
            publishable.panel_labels(fig)
            fig.savefig('myfigure.png')
        """
        label_dict = copy.deepcopy(self.label_dict)
        label_dict.update(kwargs)
        panel_labels(fig=fig, **label_dict)

    def list_journals(self):
        """Return a list of all supported journals
        """
        return self.journals.keys()

    def _calc_width(self, n_columns):
        """Calculate the width of a figure taking into account the number of columns
        and the width of the gutter between them.
        
        Inputs:
        
            * n_columns (int) - number of columns that the figure should cover
            
        Returns:
        
            * The figure width 
        """
        return n_columns * self.size_dict['column_width'] + (n_columns - 1) * self.size_dict['gutter_width']

    @staticmethod
    def _inches(length, units='mm'):
        """Convert measurements to inches
        
        Inputs:
        
            * length (scalar) - dimension to be converted into units
            * units (str) - the units of the dimension. Must be one of mm, cm, inch, or pts
            
        Returns:
        
            * length in inches
            
        Example:
        
        >>> converted = Set._inches(10, 'cm') # Convert 10cm to inches
        >>> print '%.3f' %(converted) # Check the result
        3.937
        """
        unitconverter = {'pts': 1.0 / 72.0, 'mm': 0.039370079, 
           'cm': 0.39370079, 
           'inch': 1.0}
        inches = length * unitconverter[units]
        return inches


def label_generator(case='lower', prefix='', suffix='.'):
    """Create a generator that iterates through panel labels (e.g. (A), (B), (C) or a., b., c.)
    
    Inputs:
    
        * case (str) - 'upper' for capitalized labels and 'lower' for uncapitalized
        * prefix (str) - characters to prepend to the label (e.g. to generate labels such as 
          (A) and (B), set prefix to '(' ).
        * suffix (str) - characters to append to the label (e.g. ')' or '.').
    
    Returns
    
        * A generator object
    
    Examples:
    
    >>> capitals = label_generator('upper')
    >>> print capitals.next()
    A.
    >>> print capitals.next()
    B.
    >>> lowercase = label_generator('lower', '(', ')')
    >>> print lowercase.next()
    (a)
    """
    choose_type = {'lower': string.ascii_lowercase, 'upper': string.ascii_uppercase}
    label_generator = ('%s%s%s' % (prefix, letter, suffix) for letter in choose_type[case])
    return label_generator


def label_offsetter(ax, xoffset_axis):
    """Convert an offset in x axis coordinates (e.g. 0 is left side of x axis, 1 is right side)
    to x and y axis offsets in axis coordinates, where both x and y offsets are the same when
    expressed in display (i.e. pixels) coordinates.
    
    Inputs:
        * ax (object) - a matplotlib axis object
        * xoffset_axis (scalar) - how much to offset the label from the x axis in axis coordinates
          (e.g. 1 is the length of the entire x axis).
    
    Examples:
    
    >>> from matplotlib import pyplot
    >>> import numpy
    >>> fig, ax = pyplot.subplots(1, 1) # Create an empty axis
    >>> axis_pixels = ax.transAxes.transform(numpy.array([[0,0], [1, 1]]))
    >>> xpixels, ypixels = axis_pixels[1] - axis_pixels[0]
    >>> xoffset, yoffset = label_offsetter(ax, xoffset_axis = 0.1) # Offset by 10% of x axis dimensions
    >>> yoffset_true = xoffset*(xpixels/ypixels) # expected yoffset
    >>> numpy.allclose(xoffset, 0.1) # xoffset is unchanged from input
    True
    >>> numpy.allclose(yoffset, yoffset_true) # yoffset is 0.129
    True
    """
    x_origin, y_origin = ax.transAxes.transform((0, 0))
    x_display = ax.transAxes.transform((xoffset_axis, y_origin))[0]
    offset = x_display - x_origin
    xoffset_axis, yoffset_axis = ax.transAxes.inverted().transform((offset + x_origin, offset + y_origin))
    return (
     xoffset_axis, yoffset_axis)


def is_colorbar(ax):
    """Detect whether a matplotlib axis contains a colorbar
    Depends on the assumption that colorbar axes are not navigable (i.e. cannot be panned or zoomed in the
    interactive figure).
    
    Inputs:
        * ax (object) - matplotlib axis object 
    """
    not_colorbar = ax.get_navigate()
    return not not_colorbar


def panel_labels(fig=None, position='outside', case='lower', prefix='', suffix='.', fontweight='bold', detect_colorbars=True, xy=(0.03, ), fontsize=None):
    """Label figure subplots as panels (e.g. A., B., C. or (a), (b), (c)) while ignoring
    subplot axes that contain only colorbars.
    
    Inputs:
        * fig (object) - a matplotlib figure object. If None, defaults to the currently 
          opened figure
        * position (str) - 'outside' for labels outside of the top left corner of the 
          axes area and 'inside' for labels inside of it. Defaults to outside.
        * case (str) - 'upper' for capitalized labels and 'lower' for 
          uncapitalized.
        * prefix (str) - characters to be prepended to the label (e.g. '(' )
        * suffix (str) - characters to be appended to the label (e.g. ')' or '.')
        * fontweight (str) - any valid argument to matplotlib.text.Text.set_weight.
          Use 'normal' for plaintext, 'bold' for boldface.
        * detect_colorbars (bool) - if True, will attempt to detect axes that only contain
          colorbars. This does not appear to work with AxesGrid objects, for which colorbar
          detection does not seem to be necessary. Optional, defaults to True.
        * xy (tuple) - set location of labels in axis coordinates. If len(xy) is one, both
          x and y offsets will be set according to the distance in display coordinates (i.e.
          pixels) of the x offset. If len(xy) is two, x and y offsets will be set
          independently.
        * fontsize (scalar) - font size in pts of the label. Defaults to None
    
    Usage::
    
        fig, (ax) = pyplot.subplots(1, 1) # Create plot
        ax.plot(range(3)) # Plot some stuff
        panel_labels(fig) # Create the lettering
        pyplot.show()
    """
    if fig == None:
        fig = pyplot.gcf()
    axis_list = fig.get_axes()
    generate_labels = label_generator(case=case, prefix=prefix, suffix=suffix)
    choose_position = {'outside': {'va': 'bottom', 'ha': 'right'}, 'inside': {'va': 'top', 'ha': 'left'}}
    create_offset = {'outside': lambda x, y: (
                 -x, 1 + y), 
       'inside': lambda x, y: (x, 1 - y)}
    offsetter = create_offset[position]
    text_kwargs = choose_position[position]
    if len(xy) == 1:
        x_offset = xy[0]
        equaloffsets = True
    if len(xy) == 2:
        x_offset, y_offset = xy
        x, y = offsetter(x_offset, y_offset)
        equaloffsets = False
    choose_colorbardetector = {True: is_colorbar, False: lambda ax: False}
    colorbar_detector = choose_colorbardetector[detect_colorbars]
    for ax in axis_list:
        if colorbar_detector(ax) == False:
            label = generate_labels.next()
            if equaloffsets:
                x_axis, y_axis = label_offsetter(ax, x_offset)
                x, y = offsetter(x_axis, y_axis)
            ax.text(x, y, s=label, transform=ax.transAxes, fontweight=fontweight, fontsize=fontsize, **text_kwargs)

    return


def dummy_figure(color='Coral'):
    import numpy
    x = numpy.linspace(1, 10, 20)
    ys = (numpy.log(x), 0.05 * x ** 2)
    fig, axes = pyplot.subplots(1, 2, sharey=True, sharex=False)
    titles = ('just matplotlib', 'with plotsettings')
    ylabels = ('progress', '')
    xlabels = ('number of matplotlib tweaks', 'lines of code')
    xticklabels = (('0', 'way too many'), ('0', '3 or 4'))
    for ax, title, y, ylabel, xticklabel, xlabel in zip(axes, titles, ys, ylabels, xticklabels, xlabels):
        ax.plot(x, y, linestyle='-', color=color, linewidth=2)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.set_xticks((1, 10))
        ax.set_yticks((4.5, ))
        ax.set_yticklabels(('done!', ))
        ax.set_ylabel(ylabel)
        ax.set_xticklabels(xticklabel, ha='right')

    return fig


def demonstrate():
    colors = ('DeepSkyBlue', 'Coral')
    fig = dummy_figure(colors[0])
    fig.tight_layout()
    fig.savefig('./test/default.pdf')
    publishable = Set('ProcRoySocB')
    publishable.set_figsize(1, 1)
    fig = dummy_figure(colors[1])
    publishable.panel_labels(fig)
    fig.tight_layout()
    fig.savefig('./test/fixed.pdf')


if __name__ == '__main__':
    demonstrate()
    import doctest
    with warnings.catch_warnings(record=True) as (w):
        warnings.simplefilter('error', UserWarning)
        doctest.testmod()
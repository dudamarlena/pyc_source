# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpl_tune/text.py
# Compiled at: 2019-12-02 13:27:14
# Size of source mod 2**32: 4399 bytes


class FigText(object):
    __doc__ = 'Helper to set the main foreground color and text size.\n\n\tAlso provides a method to prepare text to be analysed by LaTeX or mathtext.\n\t'

    def __init__(self, size=None, color=None, fontproperties=None, tex=False):
        self.size = size
        self.color = color
        self.fontproperties = fontproperties
        self.tex = tex

    def get_size(self):
        """Retrieve the default font size of the text items."""
        return self.size

    def set_size(self, size):
        """Set the default font size of the text items."""
        self.size = size

    def get_color(self):
        """Retrieve the default color of the text items."""
        return self.color

    def set_color(self, color):
        """Set the default color of the text items."""
        self.color = color

    def get_fontproperties(self):
        """Retrieve the default FontProperties object."""
        return self.fontproperties

    def set_fontproperties(self, fontproperties):
        """Set the default FontProperties object for text elements."""
        self.fontproperties = fontproperties

    def set_tex(self, tex):
        """Set whether the text should be analysed through LaTeX."""
        self.tex = tex

    def conv(self, text, math=True):
        """Add needed escaping sequences to run the text through LaTeX (or mathtext) processor.

                Parameters
                ----------
                text : The text to transform
                math : Flag that indicates whether the text contains mathematical notation

                Returns
                -------
                str
                        The transformed text.
                """
        if self.tex:
            if math:
                return '$\\mathrm{' + text.replace(' ', '~') + '}$'
            return text.replace('_', '\\_').replace('^', '\\^')
        else:
            if math:
                if '^' in text or '_' in text or '\\' in text:
                    return '$\\mathdefault{' + text.replace(' ', '\\ ') + '}$'
            return text

    def get_text_args(self, color=None, size=None):
        """Prepare additional arguments to a call that sets text.

                Parameters
                ----------
                color : Override for the text's color
                size : Override for the text's size

                Returns
                -------
                dict
                        Arguments that can be passed to various matplotlib calls that set text.
                """
        ret = {'usetex': self.tex}
        if color is not None:
            ret['color'] = color
        else:
            if self.color is not None:
                ret['color'] = self.color
            elif self.fontproperties is None:
                if size is not None:
                    ret['fontsize'] = size
                elif self.size is not None:
                    ret['fontsize'] = self.size
            else:
                ret['fontproperties'] = self.fontproperties.copy()
                if size is not None:
                    ret['fontproperties'].set_size(size)
            return ret

    def set_axes(self, ax):
        """Update the properties of a Axes object.

                Parameters
                ----------
                ax : matplotlib.axes.Axes object
                        Axes object to work on.
                """
        ax.set_facecolor('none')
        ax.tick_params(axis='both', which='both', color=(self.color))
        for key in ax.spines:
            ax.spines[key].set_color(self.color)
        else:
            for t in ax.get_xticklabels() + ax.get_yticklabels():
                self.set_text(t)

    def set_cbar(self, cbar):
        """Update the properties of a Colobar object.

                Parameters
                ----------
                cbar : matplotlib.colorbar.Colobar object
                        Colobar object to work on.
                """
        self.set_axes(cbar.ax)
        cbar.outline.set_edgecolor(self.color)

    def set_legend(self, legend):
        """Update the properties of a Legend object.

                Parameters
                ----------
                legend : matplotlib.legend.Legend object
                        Legend object to work on.
                """
        for t in legend.get_texts():
            self.set_text(t)

    def set_text(self, text):
        """Update the properties of a Text object.

                Parameters
                ----------
                text : matplotlib.text.Text object
                        Text object to work on.
                """
        text.set_usetex(self.tex)
        text.set_color(self.color)
        if self.fontproperties is None:
            text.set_fontsize(self.size)
        else:
            text.set_fontproperties(self.fontproperties)
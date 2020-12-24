# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/mtoken.py
# Compiled at: 2006-04-25 13:06:37
from element import *
import warnings, opdict, re
MI_FONT_REGULAR = ('Sans', 'Regular')
MI_FONT_ITALIC = ('Sans', 'Italic')
MO_FONT_REGULAR = ('Sans', 'Regular')
MO_FONT_ITALIC = ('Sans', 'Italic')
MN_FONT = ('Sans', 'Regular')
MTEXT_FONT = ('Sans', 'Regular')
MERROR_FONT = ('Monospace', 'Regular')

class _StretchyParts(object):
    __slots__ = ('upper', 'lower', 'middle', 'bar')

    def __init__(self, upper, lower, bar, middle=None):
        self.upper = upper
        self.lower = lower
        self.middle = middle
        self.bar = bar


_stretchy_parenthesis = {'(': _StretchyParts(upper=unichr(9115), bar=unichr(9116), lower=unichr(9117)), 
   '[': _StretchyParts(upper=unichr(9121), bar=unichr(9122), lower=unichr(9123)), 
   '{': _StretchyParts(upper=unichr(9127), middle=unichr(9128), lower=unichr(9129), bar=unichr(9130)), 
   ')': _StretchyParts(upper=unichr(9118), bar=unichr(9119), lower=unichr(9120)), 
   ']': _StretchyParts(upper=unichr(9124), bar=unichr(9125), lower=unichr(9126)), 
   '}': _StretchyParts(upper=unichr(9131), middle=unichr(9132), lower=unichr(9133), bar=unichr(9130)), 
   unichr(8747): _StretchyParts(upper=unichr(8992), lower=unichr(8993), bar=unichr(9134)), 
   '|': _StretchyParts(upper=None, lower=None, bar=unichr(9134))}
content_substitutions = {unichr(8517): 'D', 
   unichr(8518): 'd', 
   unichr(8519): 'e', 
   unichr(8520): 'i', 
   '-': '−', 
   unichr(10913): '≪', 
   unichr(10914): '≫', 
   unichr(8788): '≔'}
_content_substitutions_rx = re.compile(('|').join(map(re.escape, content_substitutions.keys())))

class MToken(Element):

    def __init__(self, plotter, content):
        Element.__init__(self, plotter)
        self.content = content
        self.descender = 0
        self.__stretch_height = None
        self.__stretch_depth = None
        self.__stretch_width = None
        self.__parts = None
        self.__stretchy_font_family = 'FreeSerif'
        self.__stretchy_font_style = 'Regular'
        if self.content == unichr(8290) or self.content == unichr(8289):
            self.setAttributeWeak('lspace', 0.0)
            self.setAttributeWeak('rspace', 0.0)
        self._applySubstitutions()
        return

    def _applySubstitutions(self):
        self.subst_content = _content_substitutions_rx.sub(lambda match: content_substitutions[match.group(0)], self.content)

    def _update_stretchy(self):
        pl = self.plotter
        pl.setfont(self.__stretchy_font_family, self.__stretchy_font_style, self.font_size)
        default_min_height = 0
        for part in (self.__parts.lower,
         self.__parts.middle,
         self.__parts.upper):
            if part is None:
                continue
            (_, _, height, _) = pl.labelmetrics(part)
            default_min_height += height

        if default_min_height * 0.5 > self.__stretch_depth + self.__stretch_height:
            self.height = default_min_height * 0.5
            k = self.__stretch_depth / (self.__stretch_depth + self.__stretch_height)
            self.__stretch_depth = self.height * k
            self.__stretch_height = self.height - self.__stretch_depth
            self.__stretched_font_size = self.font_size * 0.5
        else:
            self.height = self.__stretch_depth + self.__stretch_height
            if default_min_height > self.height:
                self.__stretched_font_size = self.height / default_min_height * self.font_size
            else:
                self.__stretched_font_size = self.font_size
        pl.setfont(self.__stretchy_font_family, self.__stretchy_font_style, self.__stretched_font_size)
        self.width = 0
        for part in (self.__parts.lower,
         self.__parts.middle,
         self.__parts.upper,
         self.__parts.bar):
            if part is not None:
                (_, width, _, _) = pl.labelmetrics(part, logicalw=True)
                self.width = max(self.width, width)

        self.axis = self.__stretch_depth
        return

    def update(self):
        if self.__stretch_width:
            return self._update_hstretchy()
        elif self.__parts is not None:
            return self._update_stretchy()
        if self.content == unichr(8290) or self.content == unichr(8289):
            self.width = self.Attribute(self, 'verythinmathspace').length
            self.height = 0
            return
        pl = self.plotter
        pl.setfont(self.font_family, self.font_style, self.font_size)
        (self.__layout_cache, self.width, self.height, self.axis) = pl.labelmetrics(self.subst_content)
        self.unstretched_width = self.width
        self.unstretched_height = self.height
        return

    def setVStretch(self, height, depth):
        self.__stretch_height = height
        self.__stretch_depth = depth
        try:
            self.__parts = _stretchy_parenthesis[self.content]
        except KeyError:
            self.__parts = None
            warnings.warn("Cannot stretch '%s'" % (',').join([ hex(ord(c)) for c in self.content ]))

        return

    def setHStretch(self, width):
        self.__stretch_width = width

    def _draw_non_stretchy(self):
        pl = self.plotter
        pl.setfont(self.font_family, self.font_style, self.font_size)
        pl.moveto(0, 0)
        pl.label(self.subst_content, self.__layout_cache)

    def _close_gap(self, gap_start, gap_end, bar, x0):
        if gap_start >= gap_end:
            return
        pl = self.plotter
        (layout, width, height, _) = pl.labelmetrics(bar, logicalw=True)
        if height <= 0:
            return
        overlap = height / 20
        jump = height - overlap
        gap_start -= overlap
        gap_end += overlap
        y = gap_start
        while y < gap_end:
            if y + height > gap_end:
                pl.savestate()
                pl.setcliprect(-width, y, width * 2, gap_end)
                pl.moveto(x0, y)
                pl.label(bar, layout, logicalw=True)
                pl.restorestate()
            else:
                pl.moveto(x0, y)
                pl.label(bar, layout, logicalw=True)
            y += jump

    def _draw_stretchy(self):
        pl = self.plotter
        pl.setfont(self.__stretchy_font_family, self.__stretchy_font_style, self.__stretched_font_size)
        if self.__parts.lower is not None:
            (layout, width, lower_gap_start, _) = pl.labelmetrics(self.__parts.lower, logicalw=True)
            pl.moveto(0, 0)
            pl.label(self.__parts.lower, layout, logicalw=True)
        else:
            lower_gap_start = 0
        if self.__parts.upper is not None:
            (layout, width, height, _) = pl.labelmetrics(self.__parts.upper)
            upper_gap_end = self.height - height
            pl.moveto(0, upper_gap_end)
            pl.label(self.__parts.upper, layout, logicalw=True)
        else:
            upper_gap_end = self.height
        if self.__parts.middle is None:
            self._close_gap(lower_gap_start, upper_gap_end, self.__parts.bar, 0)
        else:
            (layout, _, height, _) = pl.labelmetrics(self.__parts.middle, logicalw=True)
            lower_gap_end = self.__stretch_depth - height / 2
            pl.moveto(0, lower_gap_end)
            pl.label(self.__parts.middle, layout, logicalw=True)
            upper_gap_start = lower_gap_end + height
            self._close_gap(lower_gap_start, lower_gap_end, self.__parts.bar, 0)
            self._close_gap(upper_gap_start, upper_gap_end, self.__parts.bar, 0)
        return

    def draw(self):
        if self.content == unichr(8290) or self.content == unichr(8289):
            return
        if self.__stretch_width is not None:
            self._draw_hstretchy()
        elif self.__parts is not None:
            self._draw_stretchy()
        else:
            self._draw_non_stretchy()
        return

    def _update_hstretchy(self):
        pl = self.plotter
        pl.setfont(self.font_family, self.font_style, self.font_size)
        (_, width, height, axis) = pl.labelmetrics(self.subst_content)
        scaling = self.__stretch_width / width
        self.__stretched_font_size = self.font_size * scaling
        pl.setfont(self.font_family, self.font_style, self.__stretched_font_size)
        (_, self.width, self.height, self.axis) = pl.labelmetrics(self.subst_content)

    def _draw_hstretchy(self):
        pl = self.plotter
        pl.setfont(self.font_family, self.font_style, self.__stretched_font_size)
        pl.moveto(0, 0)
        pl.label(self.subst_content, self.__layout_cache)

    def __str__(self):
        return str(self.__class__) + "('" + self.content + "')"


class MText(MToken):

    def __init__(self, plotter, content):
        MToken.__init__(self, plotter, content)
        self.font_family = MTEXT_FONT[0]
        self.font_style = MTEXT_FONT[1]


class MError(MToken):

    def __init__(self, plotter, content):
        MToken.__init__(self, plotter, content)
        self.font_family = MERROR_FONT[0]
        self.font_style = MERROR_FONT[1]


class MOperator(MToken):

    def __init__(self, plotter, content):
        MToken.__init__(self, plotter, content)
        self.__original_content = content
        self.font_family = MO_FONT_REGULAR[0]
        self.font_style = MO_FONT_REGULAR[1]

    def update(self):
        form = self.getAttribute('form', recursive=0, default='infix').str
        try:
            attrs = opdict.lookup(self.__original_content, form)
            for (key, value) in attrs.items():
                self.setAttributeWeak(key, value)

        except KeyError:
            warnings.warn("Couldn't find operator '%s' in operator dictionary" % (self.content,))

        MToken.update(self)

    def embellished_p(self):
        return self


class MNumber(MToken):

    def __init__(self, plotter, content):
        MToken.__init__(self, plotter, content)
        self.font_family = MN_FONT[0]
        self.font_style = MN_FONT[1]


class MIdentifier(MToken):

    def __init__(self, plotter, content):
        MToken.__init__(self, plotter, content)
        if len(content) > 1:
            self.font_family = MI_FONT_REGULAR[0]
            self.font_style = MI_FONT_REGULAR[1]
        else:
            self.font_family = MI_FONT_ITALIC[0]
            self.font_style = MI_FONT_ITALIC[1]


xml_mapping['mtext'] = MText
xml_mapping['merror'] = MError
xml_mapping['mo'] = MOperator
xml_mapping['mi'] = MIdentifier
xml_mapping['mn'] = MNumber
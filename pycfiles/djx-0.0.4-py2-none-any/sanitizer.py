# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/filters/sanitizer.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
import re
from xml.sax.saxutils import escape, unescape
from pip._vendor.six.moves import urllib_parse as urlparse
from . import base
from ..constants import namespaces, prefixes
__all__ = [
 b'Filter']
allowed_elements = frozenset((
 (
  namespaces[b'html'], b'a'),
 (
  namespaces[b'html'], b'abbr'),
 (
  namespaces[b'html'], b'acronym'),
 (
  namespaces[b'html'], b'address'),
 (
  namespaces[b'html'], b'area'),
 (
  namespaces[b'html'], b'article'),
 (
  namespaces[b'html'], b'aside'),
 (
  namespaces[b'html'], b'audio'),
 (
  namespaces[b'html'], b'b'),
 (
  namespaces[b'html'], b'big'),
 (
  namespaces[b'html'], b'blockquote'),
 (
  namespaces[b'html'], b'br'),
 (
  namespaces[b'html'], b'button'),
 (
  namespaces[b'html'], b'canvas'),
 (
  namespaces[b'html'], b'caption'),
 (
  namespaces[b'html'], b'center'),
 (
  namespaces[b'html'], b'cite'),
 (
  namespaces[b'html'], b'code'),
 (
  namespaces[b'html'], b'col'),
 (
  namespaces[b'html'], b'colgroup'),
 (
  namespaces[b'html'], b'command'),
 (
  namespaces[b'html'], b'datagrid'),
 (
  namespaces[b'html'], b'datalist'),
 (
  namespaces[b'html'], b'dd'),
 (
  namespaces[b'html'], b'del'),
 (
  namespaces[b'html'], b'details'),
 (
  namespaces[b'html'], b'dfn'),
 (
  namespaces[b'html'], b'dialog'),
 (
  namespaces[b'html'], b'dir'),
 (
  namespaces[b'html'], b'div'),
 (
  namespaces[b'html'], b'dl'),
 (
  namespaces[b'html'], b'dt'),
 (
  namespaces[b'html'], b'em'),
 (
  namespaces[b'html'], b'event-source'),
 (
  namespaces[b'html'], b'fieldset'),
 (
  namespaces[b'html'], b'figcaption'),
 (
  namespaces[b'html'], b'figure'),
 (
  namespaces[b'html'], b'footer'),
 (
  namespaces[b'html'], b'font'),
 (
  namespaces[b'html'], b'form'),
 (
  namespaces[b'html'], b'header'),
 (
  namespaces[b'html'], b'h1'),
 (
  namespaces[b'html'], b'h2'),
 (
  namespaces[b'html'], b'h3'),
 (
  namespaces[b'html'], b'h4'),
 (
  namespaces[b'html'], b'h5'),
 (
  namespaces[b'html'], b'h6'),
 (
  namespaces[b'html'], b'hr'),
 (
  namespaces[b'html'], b'i'),
 (
  namespaces[b'html'], b'img'),
 (
  namespaces[b'html'], b'input'),
 (
  namespaces[b'html'], b'ins'),
 (
  namespaces[b'html'], b'keygen'),
 (
  namespaces[b'html'], b'kbd'),
 (
  namespaces[b'html'], b'label'),
 (
  namespaces[b'html'], b'legend'),
 (
  namespaces[b'html'], b'li'),
 (
  namespaces[b'html'], b'm'),
 (
  namespaces[b'html'], b'map'),
 (
  namespaces[b'html'], b'menu'),
 (
  namespaces[b'html'], b'meter'),
 (
  namespaces[b'html'], b'multicol'),
 (
  namespaces[b'html'], b'nav'),
 (
  namespaces[b'html'], b'nextid'),
 (
  namespaces[b'html'], b'ol'),
 (
  namespaces[b'html'], b'output'),
 (
  namespaces[b'html'], b'optgroup'),
 (
  namespaces[b'html'], b'option'),
 (
  namespaces[b'html'], b'p'),
 (
  namespaces[b'html'], b'pre'),
 (
  namespaces[b'html'], b'progress'),
 (
  namespaces[b'html'], b'q'),
 (
  namespaces[b'html'], b's'),
 (
  namespaces[b'html'], b'samp'),
 (
  namespaces[b'html'], b'section'),
 (
  namespaces[b'html'], b'select'),
 (
  namespaces[b'html'], b'small'),
 (
  namespaces[b'html'], b'sound'),
 (
  namespaces[b'html'], b'source'),
 (
  namespaces[b'html'], b'spacer'),
 (
  namespaces[b'html'], b'span'),
 (
  namespaces[b'html'], b'strike'),
 (
  namespaces[b'html'], b'strong'),
 (
  namespaces[b'html'], b'sub'),
 (
  namespaces[b'html'], b'sup'),
 (
  namespaces[b'html'], b'table'),
 (
  namespaces[b'html'], b'tbody'),
 (
  namespaces[b'html'], b'td'),
 (
  namespaces[b'html'], b'textarea'),
 (
  namespaces[b'html'], b'time'),
 (
  namespaces[b'html'], b'tfoot'),
 (
  namespaces[b'html'], b'th'),
 (
  namespaces[b'html'], b'thead'),
 (
  namespaces[b'html'], b'tr'),
 (
  namespaces[b'html'], b'tt'),
 (
  namespaces[b'html'], b'u'),
 (
  namespaces[b'html'], b'ul'),
 (
  namespaces[b'html'], b'var'),
 (
  namespaces[b'html'], b'video'),
 (
  namespaces[b'mathml'], b'maction'),
 (
  namespaces[b'mathml'], b'math'),
 (
  namespaces[b'mathml'], b'merror'),
 (
  namespaces[b'mathml'], b'mfrac'),
 (
  namespaces[b'mathml'], b'mi'),
 (
  namespaces[b'mathml'], b'mmultiscripts'),
 (
  namespaces[b'mathml'], b'mn'),
 (
  namespaces[b'mathml'], b'mo'),
 (
  namespaces[b'mathml'], b'mover'),
 (
  namespaces[b'mathml'], b'mpadded'),
 (
  namespaces[b'mathml'], b'mphantom'),
 (
  namespaces[b'mathml'], b'mprescripts'),
 (
  namespaces[b'mathml'], b'mroot'),
 (
  namespaces[b'mathml'], b'mrow'),
 (
  namespaces[b'mathml'], b'mspace'),
 (
  namespaces[b'mathml'], b'msqrt'),
 (
  namespaces[b'mathml'], b'mstyle'),
 (
  namespaces[b'mathml'], b'msub'),
 (
  namespaces[b'mathml'], b'msubsup'),
 (
  namespaces[b'mathml'], b'msup'),
 (
  namespaces[b'mathml'], b'mtable'),
 (
  namespaces[b'mathml'], b'mtd'),
 (
  namespaces[b'mathml'], b'mtext'),
 (
  namespaces[b'mathml'], b'mtr'),
 (
  namespaces[b'mathml'], b'munder'),
 (
  namespaces[b'mathml'], b'munderover'),
 (
  namespaces[b'mathml'], b'none'),
 (
  namespaces[b'svg'], b'a'),
 (
  namespaces[b'svg'], b'animate'),
 (
  namespaces[b'svg'], b'animateColor'),
 (
  namespaces[b'svg'], b'animateMotion'),
 (
  namespaces[b'svg'], b'animateTransform'),
 (
  namespaces[b'svg'], b'clipPath'),
 (
  namespaces[b'svg'], b'circle'),
 (
  namespaces[b'svg'], b'defs'),
 (
  namespaces[b'svg'], b'desc'),
 (
  namespaces[b'svg'], b'ellipse'),
 (
  namespaces[b'svg'], b'font-face'),
 (
  namespaces[b'svg'], b'font-face-name'),
 (
  namespaces[b'svg'], b'font-face-src'),
 (
  namespaces[b'svg'], b'g'),
 (
  namespaces[b'svg'], b'glyph'),
 (
  namespaces[b'svg'], b'hkern'),
 (
  namespaces[b'svg'], b'linearGradient'),
 (
  namespaces[b'svg'], b'line'),
 (
  namespaces[b'svg'], b'marker'),
 (
  namespaces[b'svg'], b'metadata'),
 (
  namespaces[b'svg'], b'missing-glyph'),
 (
  namespaces[b'svg'], b'mpath'),
 (
  namespaces[b'svg'], b'path'),
 (
  namespaces[b'svg'], b'polygon'),
 (
  namespaces[b'svg'], b'polyline'),
 (
  namespaces[b'svg'], b'radialGradient'),
 (
  namespaces[b'svg'], b'rect'),
 (
  namespaces[b'svg'], b'set'),
 (
  namespaces[b'svg'], b'stop'),
 (
  namespaces[b'svg'], b'svg'),
 (
  namespaces[b'svg'], b'switch'),
 (
  namespaces[b'svg'], b'text'),
 (
  namespaces[b'svg'], b'title'),
 (
  namespaces[b'svg'], b'tspan'),
 (
  namespaces[b'svg'], b'use')))
allowed_attributes = frozenset((
 (None, 'abbr'),
 (None, 'accept'),
 (None, 'accept-charset'),
 (None, 'accesskey'),
 (None, 'action'),
 (None, 'align'),
 (None, 'alt'),
 (None, 'autocomplete'),
 (None, 'autofocus'),
 (None, 'axis'),
 (None, 'background'),
 (None, 'balance'),
 (None, 'bgcolor'),
 (None, 'bgproperties'),
 (None, 'border'),
 (None, 'bordercolor'),
 (None, 'bordercolordark'),
 (None, 'bordercolorlight'),
 (None, 'bottompadding'),
 (None, 'cellpadding'),
 (None, 'cellspacing'),
 (None, 'ch'),
 (None, 'challenge'),
 (None, 'char'),
 (None, 'charoff'),
 (None, 'choff'),
 (None, 'charset'),
 (None, 'checked'),
 (None, 'cite'),
 (None, 'class'),
 (None, 'clear'),
 (None, 'color'),
 (None, 'cols'),
 (None, 'colspan'),
 (None, 'compact'),
 (None, 'contenteditable'),
 (None, 'controls'),
 (None, 'coords'),
 (None, 'data'),
 (None, 'datafld'),
 (None, 'datapagesize'),
 (None, 'datasrc'),
 (None, 'datetime'),
 (None, 'default'),
 (None, 'delay'),
 (None, 'dir'),
 (None, 'disabled'),
 (None, 'draggable'),
 (None, 'dynsrc'),
 (None, 'enctype'),
 (None, 'end'),
 (None, 'face'),
 (None, 'for'),
 (None, 'form'),
 (None, 'frame'),
 (None, 'galleryimg'),
 (None, 'gutter'),
 (None, 'headers'),
 (None, 'height'),
 (None, 'hidefocus'),
 (None, 'hidden'),
 (None, 'high'),
 (None, 'href'),
 (None, 'hreflang'),
 (None, 'hspace'),
 (None, 'icon'),
 (None, 'id'),
 (None, 'inputmode'),
 (None, 'ismap'),
 (None, 'keytype'),
 (None, 'label'),
 (None, 'leftspacing'),
 (None, 'lang'),
 (None, 'list'),
 (None, 'longdesc'),
 (None, 'loop'),
 (None, 'loopcount'),
 (None, 'loopend'),
 (None, 'loopstart'),
 (None, 'low'),
 (None, 'lowsrc'),
 (None, 'max'),
 (None, 'maxlength'),
 (None, 'media'),
 (None, 'method'),
 (None, 'min'),
 (None, 'multiple'),
 (None, 'name'),
 (None, 'nohref'),
 (None, 'noshade'),
 (None, 'nowrap'),
 (None, 'open'),
 (None, 'optimum'),
 (None, 'pattern'),
 (None, 'ping'),
 (None, 'point-size'),
 (None, 'poster'),
 (None, 'pqg'),
 (None, 'preload'),
 (None, 'prompt'),
 (None, 'radiogroup'),
 (None, 'readonly'),
 (None, 'rel'),
 (None, 'repeat-max'),
 (None, 'repeat-min'),
 (None, 'replace'),
 (None, 'required'),
 (None, 'rev'),
 (None, 'rightspacing'),
 (None, 'rows'),
 (None, 'rowspan'),
 (None, 'rules'),
 (None, 'scope'),
 (None, 'selected'),
 (None, 'shape'),
 (None, 'size'),
 (None, 'span'),
 (None, 'src'),
 (None, 'start'),
 (None, 'step'),
 (None, 'style'),
 (None, 'summary'),
 (None, 'suppress'),
 (None, 'tabindex'),
 (None, 'target'),
 (None, 'template'),
 (None, 'title'),
 (None, 'toppadding'),
 (None, 'type'),
 (None, 'unselectable'),
 (None, 'usemap'),
 (None, 'urn'),
 (None, 'valign'),
 (None, 'value'),
 (None, 'variable'),
 (None, 'volume'),
 (None, 'vspace'),
 (None, 'vrml'),
 (None, 'width'),
 (None, 'wrap'),
 (
  namespaces[b'xml'], b'lang'),
 (None, 'actiontype'),
 (None, 'align'),
 (None, 'columnalign'),
 (None, 'columnalign'),
 (None, 'columnalign'),
 (None, 'columnlines'),
 (None, 'columnspacing'),
 (None, 'columnspan'),
 (None, 'depth'),
 (None, 'display'),
 (None, 'displaystyle'),
 (None, 'equalcolumns'),
 (None, 'equalrows'),
 (None, 'fence'),
 (None, 'fontstyle'),
 (None, 'fontweight'),
 (None, 'frame'),
 (None, 'height'),
 (None, 'linethickness'),
 (None, 'lspace'),
 (None, 'mathbackground'),
 (None, 'mathcolor'),
 (None, 'mathvariant'),
 (None, 'mathvariant'),
 (None, 'maxsize'),
 (None, 'minsize'),
 (None, 'other'),
 (None, 'rowalign'),
 (None, 'rowalign'),
 (None, 'rowalign'),
 (None, 'rowlines'),
 (None, 'rowspacing'),
 (None, 'rowspan'),
 (None, 'rspace'),
 (None, 'scriptlevel'),
 (None, 'selection'),
 (None, 'separator'),
 (None, 'stretchy'),
 (None, 'width'),
 (None, 'width'),
 (
  namespaces[b'xlink'], b'href'),
 (
  namespaces[b'xlink'], b'show'),
 (
  namespaces[b'xlink'], b'type'),
 (None, 'accent-height'),
 (None, 'accumulate'),
 (None, 'additive'),
 (None, 'alphabetic'),
 (None, 'arabic-form'),
 (None, 'ascent'),
 (None, 'attributeName'),
 (None, 'attributeType'),
 (None, 'baseProfile'),
 (None, 'bbox'),
 (None, 'begin'),
 (None, 'by'),
 (None, 'calcMode'),
 (None, 'cap-height'),
 (None, 'class'),
 (None, 'clip-path'),
 (None, 'color'),
 (None, 'color-rendering'),
 (None, 'content'),
 (None, 'cx'),
 (None, 'cy'),
 (None, 'd'),
 (None, 'dx'),
 (None, 'dy'),
 (None, 'descent'),
 (None, 'display'),
 (None, 'dur'),
 (None, 'end'),
 (None, 'fill'),
 (None, 'fill-opacity'),
 (None, 'fill-rule'),
 (None, 'font-family'),
 (None, 'font-size'),
 (None, 'font-stretch'),
 (None, 'font-style'),
 (None, 'font-variant'),
 (None, 'font-weight'),
 (None, 'from'),
 (None, 'fx'),
 (None, 'fy'),
 (None, 'g1'),
 (None, 'g2'),
 (None, 'glyph-name'),
 (None, 'gradientUnits'),
 (None, 'hanging'),
 (None, 'height'),
 (None, 'horiz-adv-x'),
 (None, 'horiz-origin-x'),
 (None, 'id'),
 (None, 'ideographic'),
 (None, 'k'),
 (None, 'keyPoints'),
 (None, 'keySplines'),
 (None, 'keyTimes'),
 (None, 'lang'),
 (None, 'marker-end'),
 (None, 'marker-mid'),
 (None, 'marker-start'),
 (None, 'markerHeight'),
 (None, 'markerUnits'),
 (None, 'markerWidth'),
 (None, 'mathematical'),
 (None, 'max'),
 (None, 'min'),
 (None, 'name'),
 (None, 'offset'),
 (None, 'opacity'),
 (None, 'orient'),
 (None, 'origin'),
 (None, 'overline-position'),
 (None, 'overline-thickness'),
 (None, 'panose-1'),
 (None, 'path'),
 (None, 'pathLength'),
 (None, 'points'),
 (None, 'preserveAspectRatio'),
 (None, 'r'),
 (None, 'refX'),
 (None, 'refY'),
 (None, 'repeatCount'),
 (None, 'repeatDur'),
 (None, 'requiredExtensions'),
 (None, 'requiredFeatures'),
 (None, 'restart'),
 (None, 'rotate'),
 (None, 'rx'),
 (None, 'ry'),
 (None, 'slope'),
 (None, 'stemh'),
 (None, 'stemv'),
 (None, 'stop-color'),
 (None, 'stop-opacity'),
 (None, 'strikethrough-position'),
 (None, 'strikethrough-thickness'),
 (None, 'stroke'),
 (None, 'stroke-dasharray'),
 (None, 'stroke-dashoffset'),
 (None, 'stroke-linecap'),
 (None, 'stroke-linejoin'),
 (None, 'stroke-miterlimit'),
 (None, 'stroke-opacity'),
 (None, 'stroke-width'),
 (None, 'systemLanguage'),
 (None, 'target'),
 (None, 'text-anchor'),
 (None, 'to'),
 (None, 'transform'),
 (None, 'type'),
 (None, 'u1'),
 (None, 'u2'),
 (None, 'underline-position'),
 (None, 'underline-thickness'),
 (None, 'unicode'),
 (None, 'unicode-range'),
 (None, 'units-per-em'),
 (None, 'values'),
 (None, 'version'),
 (None, 'viewBox'),
 (None, 'visibility'),
 (None, 'width'),
 (None, 'widths'),
 (None, 'x'),
 (None, 'x-height'),
 (None, 'x1'),
 (None, 'x2'),
 (
  namespaces[b'xlink'], b'actuate'),
 (
  namespaces[b'xlink'], b'arcrole'),
 (
  namespaces[b'xlink'], b'href'),
 (
  namespaces[b'xlink'], b'role'),
 (
  namespaces[b'xlink'], b'show'),
 (
  namespaces[b'xlink'], b'title'),
 (
  namespaces[b'xlink'], b'type'),
 (
  namespaces[b'xml'], b'base'),
 (
  namespaces[b'xml'], b'lang'),
 (
  namespaces[b'xml'], b'space'),
 (None, 'y'),
 (None, 'y1'),
 (None, 'y2'),
 (None, 'zoomAndPan')))
attr_val_is_uri = frozenset((
 (None, 'href'),
 (None, 'src'),
 (None, 'cite'),
 (None, 'action'),
 (None, 'longdesc'),
 (None, 'poster'),
 (None, 'background'),
 (None, 'datasrc'),
 (None, 'dynsrc'),
 (None, 'lowsrc'),
 (None, 'ping'),
 (
  namespaces[b'xlink'], b'href'),
 (
  namespaces[b'xml'], b'base')))
svg_attr_val_allows_ref = frozenset((
 (None, 'clip-path'),
 (None, 'color-profile'),
 (None, 'cursor'),
 (None, 'fill'),
 (None, 'filter'),
 (None, 'marker'),
 (None, 'marker-start'),
 (None, 'marker-mid'),
 (None, 'marker-end'),
 (None, 'mask'),
 (None, 'stroke')))
svg_allow_local_href = frozenset((
 (None, 'altGlyph'),
 (None, 'animate'),
 (None, 'animateColor'),
 (None, 'animateMotion'),
 (None, 'animateTransform'),
 (None, 'cursor'),
 (None, 'feImage'),
 (None, 'filter'),
 (None, 'linearGradient'),
 (None, 'pattern'),
 (None, 'radialGradient'),
 (None, 'textpath'),
 (None, 'tref'),
 (None, 'set'),
 (None, 'use')))
allowed_css_properties = frozenset(('azimuth', 'background-color', 'border-bottom-color',
                                    'border-collapse', 'border-color', 'border-left-color',
                                    'border-right-color', 'border-top-color', 'clear',
                                    'color', 'cursor', 'direction', 'display', 'elevation',
                                    'float', 'font', 'font-family', 'font-size',
                                    'font-style', 'font-variant', 'font-weight',
                                    'height', 'letter-spacing', 'line-height', 'overflow',
                                    'pause', 'pause-after', 'pause-before', 'pitch',
                                    'pitch-range', 'richness', 'speak', 'speak-header',
                                    'speak-numeral', 'speak-punctuation', 'speech-rate',
                                    'stress', 'text-align', 'text-decoration', 'text-indent',
                                    'unicode-bidi', 'vertical-align', 'voice-family',
                                    'volume', 'white-space', 'width'))
allowed_css_keywords = frozenset(('auto', 'aqua', 'black', 'block', 'blue', 'bold',
                                  'both', 'bottom', 'brown', 'center', 'collapse',
                                  'dashed', 'dotted', 'fuchsia', 'gray', 'green',
                                  '!important', 'italic', 'left', 'lime', 'maroon',
                                  'medium', 'none', 'navy', 'normal', 'nowrap', 'olive',
                                  'pointer', 'purple', 'red', 'right', 'solid', 'silver',
                                  'teal', 'top', 'transparent', 'underline', 'white',
                                  'yellow'))
allowed_svg_properties = frozenset(('fill', 'fill-opacity', 'fill-rule', 'stroke',
                                    'stroke-width', 'stroke-linecap', 'stroke-linejoin',
                                    'stroke-opacity'))
allowed_protocols = frozenset(('ed2k', 'ftp', 'http', 'https', 'irc', 'mailto', 'news',
                               'gopher', 'nntp', 'telnet', 'webcal', 'xmpp', 'callto',
                               'feed', 'urn', 'aim', 'rsync', 'tag', 'ssh', 'sftp',
                               'rtsp', 'afs', 'data'))
allowed_content_types = frozenset(('image/png', 'image/jpeg', 'image/gif', 'image/webp',
                                   'image/bmp', 'text/plain'))
data_content_type = re.compile(b'\n                                ^\n                                # Match a content type <application>/<type>\n                                (?P<content_type>[-a-zA-Z0-9.]+/[-a-zA-Z0-9.]+)\n                                # Match any character set and encoding\n                                (?:(?:;charset=(?:[-a-zA-Z0-9]+)(?:;(?:base64))?)\n                                  |(?:;(?:base64))?(?:;charset=(?:[-a-zA-Z0-9]+))?)\n                                # Assume the rest is data\n                                ,.*\n                                $\n                                ', re.VERBOSE)

class Filter(base.Filter):
    """Sanitizes token stream of XHTML+MathML+SVG and of inline style attributes"""

    def __init__(self, source, allowed_elements=allowed_elements, allowed_attributes=allowed_attributes, allowed_css_properties=allowed_css_properties, allowed_css_keywords=allowed_css_keywords, allowed_svg_properties=allowed_svg_properties, allowed_protocols=allowed_protocols, allowed_content_types=allowed_content_types, attr_val_is_uri=attr_val_is_uri, svg_attr_val_allows_ref=svg_attr_val_allows_ref, svg_allow_local_href=svg_allow_local_href):
        """Creates a Filter

        :arg allowed_elements: set of elements to allow--everything else will
            be escaped

        :arg allowed_attributes: set of attributes to allow in
            elements--everything else will be stripped

        :arg allowed_css_properties: set of CSS properties to allow--everything
            else will be stripped

        :arg allowed_css_keywords: set of CSS keywords to allow--everything
            else will be stripped

        :arg allowed_svg_properties: set of SVG properties to allow--everything
            else will be removed

        :arg allowed_protocols: set of allowed protocols for URIs

        :arg allowed_content_types: set of allowed content types for ``data`` URIs.

        :arg attr_val_is_uri: set of attributes that have URI values--values
            that have a scheme not listed in ``allowed_protocols`` are removed

        :arg svg_attr_val_allows_ref: set of SVG attributes that can have
            references

        :arg svg_allow_local_href: set of SVG elements that can have local
            hrefs--these are removed

        """
        super(Filter, self).__init__(source)
        self.allowed_elements = allowed_elements
        self.allowed_attributes = allowed_attributes
        self.allowed_css_properties = allowed_css_properties
        self.allowed_css_keywords = allowed_css_keywords
        self.allowed_svg_properties = allowed_svg_properties
        self.allowed_protocols = allowed_protocols
        self.allowed_content_types = allowed_content_types
        self.attr_val_is_uri = attr_val_is_uri
        self.svg_attr_val_allows_ref = svg_attr_val_allows_ref
        self.svg_allow_local_href = svg_allow_local_href

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            token = self.sanitize_token(token)
            if token:
                yield token

    def sanitize_token(self, token):
        token_type = token[b'type']
        if token_type in ('StartTag', 'EndTag', 'EmptyTag'):
            name = token[b'name']
            namespace = token[b'namespace']
            if (namespace, name) in self.allowed_elements or namespace is None and (
             namespaces[b'html'], name) in self.allowed_elements:
                return self.allowed_token(token)
            return self.disallowed_token(token)
        elif token_type == b'Comment':
            pass
        else:
            return token
        return

    def allowed_token(self, token):
        if b'data' in token:
            attrs = token[b'data']
            attr_names = set(attrs.keys())
            for to_remove in attr_names - self.allowed_attributes:
                del token[b'data'][to_remove]
                attr_names.remove(to_remove)

            for attr in attr_names & self.attr_val_is_uri:
                assert attr in attrs
                val_unescaped = re.sub(b'[`\x00- \x7f-\xa0\\s]+', b'', unescape(attrs[attr])).lower()
                val_unescaped = val_unescaped.replace(b'�', b'')
                try:
                    uri = urlparse.urlparse(val_unescaped)
                except ValueError:
                    uri = None
                    del attrs[attr]

                if uri and uri.scheme:
                    if uri.scheme not in self.allowed_protocols:
                        del attrs[attr]
                    if uri.scheme == b'data':
                        m = data_content_type.match(uri.path)
                        if not m:
                            del attrs[attr]
                        elif m.group(b'content_type') not in self.allowed_content_types:
                            del attrs[attr]

            for attr in self.svg_attr_val_allows_ref:
                if attr in attrs:
                    attrs[attr] = re.sub(b'url\\s*\\(\\s*[^#\\s][^)]+?\\)', b' ', unescape(attrs[attr]))

            if token[b'name'] in self.svg_allow_local_href and (
             namespaces[b'xlink'], b'href') in attrs and re.search(b'^\\s*[^#\\s].*', attrs[(namespaces[b'xlink'], b'href')]):
                del attrs[(namespaces[b'xlink'], b'href')]
            if (None, 'style') in attrs:
                attrs[(None, 'style')] = self.sanitize_css(attrs[(None, 'style')])
            token[b'data'] = attrs
        return token

    def disallowed_token(self, token):
        token_type = token[b'type']
        if token_type == b'EndTag':
            token[b'data'] = b'</%s>' % token[b'name']
        elif token[b'data']:
            assert token_type in ('StartTag', 'EmptyTag')
            attrs = []
            for (ns, name), v in token[b'data'].items():
                attrs.append(b' %s="%s"' % (name if ns is None else b'%s:%s' % (prefixes[ns], name), escape(v)))

            token[b'data'] = b'<%s%s>' % (token[b'name'], (b'').join(attrs))
        else:
            token[b'data'] = b'<%s>' % token[b'name']
        if token.get(b'selfClosing'):
            token[b'data'] = token[b'data'][:-1] + b'/>'
        token[b'type'] = b'Characters'
        del token[b'name']
        return token

    def sanitize_css(self, style):
        style = re.compile(b'url\\s*\\(\\s*[^\\s)]+?\\s*\\)\\s*').sub(b' ', style)
        if not re.match(b'^([:,;#%.\\sa-zA-Z0-9!]|\\w-\\w|\'[\\s\\w]+\'|"[\\s\\w]+"|\\([\\d,\\s]+\\))*$', style):
            return b''
        if not re.match(b'^\\s*([-\\w]+\\s*:[^:;]*(;\\s*|$))*$', style):
            return b''
        clean = []
        for prop, value in re.findall(b'([-\\w]+)\\s*:\\s*([^:;]*)', style):
            if not value:
                continue
            if prop.lower() in self.allowed_css_properties:
                clean.append(prop + b': ' + value + b';')
            elif prop.split(b'-')[0].lower() in ('background', 'border', 'margin',
                                                 'padding'):
                for keyword in value.split():
                    if keyword not in self.allowed_css_keywords and not re.match(b'^(#[0-9a-fA-F]+|rgb\\(\\d+%?,\\d*%?,?\\d*%?\\)?|\\d{0,2}\\.?\\d{0,2}(cm|em|ex|in|mm|pc|pt|px|%|,|\\))?)$', keyword):
                        break
                else:
                    clean.append(prop + b': ' + value + b';')

            elif prop.lower() in self.allowed_svg_properties:
                clean.append(prop + b': ' + value + b';')

        return (b' ').join(clean)
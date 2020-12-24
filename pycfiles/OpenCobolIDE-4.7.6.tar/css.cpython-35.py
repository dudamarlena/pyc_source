# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/css.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 24707 bytes
"""
    pygments.lexers.css
    ~~~~~~~~~~~~~~~~~~~

    Lexers for CSS and related stylesheet formats.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re, copy
from pygments.lexer import ExtendedRegexLexer, RegexLexer, include, bygroups, default, words, inherit
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
from pygments.util import iteritems
__all__ = [
 'CssLexer', 'SassLexer', 'ScssLexer', 'LessCssLexer']

class CssLexer(RegexLexer):
    __doc__ = '\n    For CSS (Cascading Style Sheets).\n    '
    name = 'CSS'
    aliases = ['css']
    filenames = ['*.css']
    mimetypes = ['text/css']
    tokens = {'root': [
              include('basics')], 
     
     'basics': [
                (
                 '\\s+', Text),
                (
                 '/\\*(?:.|\\n)*?\\*/', Comment),
                (
                 '\\{', Punctuation, 'content'),
                (
                 '\\:[\\w-]+', Name.Decorator),
                (
                 '\\.[\\w-]+', Name.Class),
                (
                 '\\#[\\w-]+', Name.Namespace),
                (
                 '@[\\w-]+', Keyword, 'atrule'),
                (
                 '[\\w-]+', Name.Tag),
                (
                 '[~^*!%&$\\[\\]()<>|+=@:;,./?-]', Operator),
                (
                 '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                (
                 "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)], 
     
     'atrule': [
                (
                 '\\{', Punctuation, 'atcontent'),
                (
                 ';', Punctuation, '#pop'),
                include('basics')], 
     
     'atcontent': [
                   include('basics'),
                   (
                    '\\}', Punctuation, '#pop:2')], 
     
     'content': [
                 (
                  '\\s+', Text),
                 (
                  '\\}', Punctuation, '#pop'),
                 (
                  'url\\(.*?\\)', String.Other),
                 (
                  '^@.*?$', Comment.Preproc),
                 (
                  words(('azimuth', 'background-attachment', 'background-color', 'background-image',
       'background-position', 'background-repeat', 'background', 'border-bottom-color',
       'border-bottom-style', 'border-bottom-width', 'border-left-color', 'border-left-style',
       'border-left-width', 'border-right', 'border-right-color', 'border-right-style',
       'border-right-width', 'border-top-color', 'border-top-style', 'border-top-width',
       'border-bottom', 'border-collapse', 'border-left', 'border-width', 'border-color',
       'border-spacing', 'border-style', 'border-top', 'border', 'caption-side',
       'clear', 'clip', 'color', 'content', 'counter-increment', 'counter-reset',
       'cue-after', 'cue-before', 'cue', 'cursor', 'direction', 'display', 'elevation',
       'empty-cells', 'float', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch',
       'font-style', 'font-variant', 'font-weight', 'font', 'height', 'letter-spacing',
       'line-height', 'list-style-type', 'list-style-image', 'list-style-position',
       'list-style', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top',
       'margin', 'marker-offset', 'marks', 'max-height', 'max-width', 'min-height',
       'min-width', 'opacity', 'orphans', 'outline-color', 'outline-style', 'outline-width',
       'outline', 'overflow', 'overflow-x', 'overflow-y', 'padding-bottom', 'padding-left',
       'padding-right', 'padding-top', 'padding', 'page', 'page-break-after', 'page-break-before',
       'page-break-inside', 'pause-after', 'pause-before', 'pause', 'pitch-range',
       'pitch', 'play-during', 'position', 'quotes', 'richness', 'right', 'size',
       'speak-header', 'speak-numeral', 'speak-punctuation', 'speak', 'speech-rate',
       'stress', 'table-layout', 'text-align', 'text-decoration', 'text-indent',
       'text-shadow', 'text-transform', 'top', 'unicode-bidi', 'vertical-align',
       'visibility', 'voice-family', 'volume', 'white-space', 'widows', 'width',
       'word-spacing', 'z-index', 'bottom', 'above', 'absolute', 'always', 'armenian',
       'aural', 'auto', 'avoid', 'baseline', 'behind', 'below', 'bidi-override',
       'blink', 'block', 'bolder', 'bold', 'both', 'capitalize', 'center-left', 'center-right',
       'center', 'circle', 'cjk-ideographic', 'close-quote', 'collapse', 'condensed',
       'continuous', 'crop', 'crosshair', 'cross', 'cursive', 'dashed', 'decimal-leading-zero',
       'decimal', 'default', 'digits', 'disc', 'dotted', 'double', 'e-resize', 'embed',
       'extra-condensed', 'extra-expanded', 'expanded', 'fantasy', 'far-left', 'far-right',
       'faster', 'fast', 'fixed', 'georgian', 'groove', 'hebrew', 'help', 'hidden',
       'hide', 'higher', 'high', 'hiragana-iroha', 'hiragana', 'icon', 'inherit',
       'inline-table', 'inline', 'inset', 'inside', 'invert', 'italic', 'justify',
       'katakana-iroha', 'katakana', 'landscape', 'larger', 'large', 'left-side',
       'leftwards', 'left', 'level', 'lighter', 'line-through', 'list-item', 'loud',
       'lower-alpha', 'lower-greek', 'lower-roman', 'lowercase', 'ltr', 'lower',
       'low', 'medium', 'message-box', 'middle', 'mix', 'monospace', 'n-resize',
       'narrower', 'ne-resize', 'no-close-quote', 'no-open-quote', 'no-repeat', 'none',
       'normal', 'nowrap', 'nw-resize', 'oblique', 'once', 'open-quote', 'outset',
       'outside', 'overline', 'pointer', 'portrait', 'px', 'relative', 'repeat-x',
       'repeat-y', 'repeat', 'rgb', 'ridge', 'right-side', 'rightwards', 's-resize',
       'sans-serif', 'scroll', 'se-resize', 'semi-condensed', 'semi-expanded', 'separate',
       'serif', 'show', 'silent', 'slower', 'slow', 'small-caps', 'small-caption',
       'smaller', 'soft', 'solid', 'spell-out', 'square', 'static', 'status-bar',
       'super', 'sw-resize', 'table-caption', 'table-cell', 'table-column', 'table-column-group',
       'table-footer-group', 'table-header-group', 'table-row', 'table-row-group',
       'text-bottom', 'text-top', 'text', 'thick', 'thin', 'transparent', 'ultra-condensed',
       'ultra-expanded', 'underline', 'upper-alpha', 'upper-latin', 'upper-roman',
       'uppercase', 'url', 'visible', 'w-resize', 'wait', 'wider', 'x-fast', 'x-high',
       'x-large', 'x-loud', 'x-low', 'x-small', 'x-soft', 'xx-large', 'xx-small',
       'yes'), suffix='\\b'),
                  Name.Builtin),
                 (
                  words(('indigo', 'gold', 'firebrick', 'indianred', 'yellow', 'darkolivegreen', 'darkseagreen',
       'mediumvioletred', 'mediumorchid', 'chartreuse', 'mediumslateblue', 'black',
       'springgreen', 'crimson', 'lightsalmon', 'brown', 'turquoise', 'olivedrab',
       'cyan', 'silver', 'skyblue', 'gray', 'darkturquoise', 'goldenrod', 'darkgreen',
       'darkviolet', 'darkgray', 'lightpink', 'teal', 'darkmagenta', 'lightgoldenrodyellow',
       'lavender', 'yellowgreen', 'thistle', 'violet', 'navy', 'orchid', 'blue',
       'ghostwhite', 'honeydew', 'cornflowerblue', 'darkblue', 'darkkhaki', 'mediumpurple',
       'cornsilk', 'red', 'bisque', 'slategray', 'darkcyan', 'khaki', 'wheat', 'deepskyblue',
       'darkred', 'steelblue', 'aliceblue', 'gainsboro', 'mediumturquoise', 'floralwhite',
       'coral', 'purple', 'lightgrey', 'lightcyan', 'darksalmon', 'beige', 'azure',
       'lightsteelblue', 'oldlace', 'greenyellow', 'royalblue', 'lightseagreen',
       'mistyrose', 'sienna', 'lightcoral', 'orangered', 'navajowhite', 'lime', 'palegreen',
       'burlywood', 'seashell', 'mediumspringgreen', 'fuchsia', 'papayawhip', 'blanchedalmond',
       'peru', 'aquamarine', 'white', 'darkslategray', 'ivory', 'dodgerblue', 'lemonchiffon',
       'chocolate', 'orange', 'forestgreen', 'slateblue', 'olive', 'mintcream', 'antiquewhite',
       'darkorange', 'cadetblue', 'moccasin', 'limegreen', 'saddlebrown', 'darkslateblue',
       'lightskyblue', 'deeppink', 'plum', 'aqua', 'darkgoldenrod', 'maroon', 'sandybrown',
       'magenta', 'tan', 'rosybrown', 'pink', 'lightblue', 'palevioletred', 'mediumseagreen',
       'dimgray', 'powderblue', 'seagreen', 'snow', 'mediumblue', 'midnightblue',
       'paleturquoise', 'palegoldenrod', 'whitesmoke', 'darkorchid', 'salmon', 'lightslategray',
       'lawngreen', 'lightgreen', 'tomato', 'hotpink', 'lightyellow', 'lavenderblush',
       'linen', 'mediumaquamarine', 'green', 'blueviolet', 'peachpuff'), suffix='\\b'),
                  Name.Builtin),
                 (
                  '\\!important', Comment.Preproc),
                 (
                  '/\\*(?:.|\\n)*?\\*/', Comment),
                 (
                  '\\#[a-zA-Z0-9]{1,6}', Number),
                 (
                  '[.-]?[0-9]*[.]?[0-9]+(em|px|pt|pc|in|mm|cm|ex|s)\\b', Number),
                 (
                  '[.-]?[0-9]*[.]?[0-9]+%', Number),
                 (
                  '-?[0-9]+', Number),
                 (
                  '[~^*!%&<>|+=@:,./?-]+', Operator),
                 (
                  '[\\[\\]();]+', Punctuation),
                 (
                  '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                 (
                  "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
                 (
                  '[a-zA-Z_]\\w*', Name)]}


common_sass_tokens = {'value': [
           (
            '[ \\t]+', Text),
           (
            '[!$][\\w-]+', Name.Variable),
           (
            'url\\(', String.Other, 'string-url'),
           (
            '[a-z_-][\\w-]*(?=\\()', Name.Function),
           (
            words(('azimuth', 'background-attachment', 'background-color', 'background-image',
       'background-position', 'background-repeat', 'background', 'border-bottom-color',
       'border-bottom-style', 'border-bottom-width', 'border-left-color', 'border-left-style',
       'border-left-width', 'border-right', 'border-right-color', 'border-right-style',
       'border-right-width', 'border-top-color', 'border-top-style', 'border-top-width',
       'border-bottom', 'border-collapse', 'border-left', 'border-width', 'border-color',
       'border-spacing', 'border-style', 'border-top', 'border', 'caption-side',
       'clear', 'clip', 'color', 'content', 'counter-increment', 'counter-reset',
       'cue-after', 'cue-before', 'cue', 'cursor', 'direction', 'display', 'elevation',
       'empty-cells', 'float', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch',
       'font-style', 'font-variant', 'font-weight', 'font', 'height', 'letter-spacing',
       'line-height', 'list-style-type', 'list-style-image', 'list-style-position',
       'list-style', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top',
       'margin', 'marker-offset', 'marks', 'max-height', 'max-width', 'min-height',
       'min-width', 'opacity', 'orphans', 'outline', 'outline-color', 'outline-style',
       'outline-width', 'overflow', 'padding-bottom', 'padding-left', 'padding-right',
       'padding-top', 'padding', 'page', 'page-break-after', 'page-break-before',
       'page-break-inside', 'pause-after', 'pause-before', 'pause', 'pitch', 'pitch-range',
       'play-during', 'position', 'quotes', 'richness', 'right', 'size', 'speak-header',
       'speak-numeral', 'speak-punctuation', 'speak', 'speech-rate', 'stress', 'table-layout',
       'text-align', 'text-decoration', 'text-indent', 'text-shadow', 'text-transform',
       'top', 'unicode-bidi', 'vertical-align', 'visibility', 'voice-family', 'volume',
       'white-space', 'widows', 'width', 'word-spacing', 'z-index', 'bottom', 'left',
       'above', 'absolute', 'always', 'armenian', 'aural', 'auto', 'avoid', 'baseline',
       'behind', 'below', 'bidi-override', 'blink', 'block', 'bold', 'bolder', 'both',
       'capitalize', 'center-left', 'center-right', 'center', 'circle', 'cjk-ideographic',
       'close-quote', 'collapse', 'condensed', 'continuous', 'crop', 'crosshair',
       'cross', 'cursive', 'dashed', 'decimal-leading-zero', 'decimal', 'default',
       'digits', 'disc', 'dotted', 'double', 'e-resize', 'embed', 'extra-condensed',
       'extra-expanded', 'expanded', 'fantasy', 'far-left', 'far-right', 'faster',
       'fast', 'fixed', 'georgian', 'groove', 'hebrew', 'help', 'hidden', 'hide',
       'higher', 'high', 'hiragana-iroha', 'hiragana', 'icon', 'inherit', 'inline-table',
       'inline', 'inset', 'inside', 'invert', 'italic', 'justify', 'katakana-iroha',
       'katakana', 'landscape', 'larger', 'large', 'left-side', 'leftwards', 'level',
       'lighter', 'line-through', 'list-item', 'loud', 'lower-alpha', 'lower-greek',
       'lower-roman', 'lowercase', 'ltr', 'lower', 'low', 'medium', 'message-box',
       'middle', 'mix', 'monospace', 'n-resize', 'narrower', 'ne-resize', 'no-close-quote',
       'no-open-quote', 'no-repeat', 'none', 'normal', 'nowrap', 'nw-resize', 'oblique',
       'once', 'open-quote', 'outset', 'outside', 'overline', 'pointer', 'portrait',
       'px', 'relative', 'repeat-x', 'repeat-y', 'repeat', 'rgb', 'ridge', 'right-side',
       'rightwards', 's-resize', 'sans-serif', 'scroll', 'se-resize', 'semi-condensed',
       'semi-expanded', 'separate', 'serif', 'show', 'silent', 'slow', 'slower',
       'small-caps', 'small-caption', 'smaller', 'soft', 'solid', 'spell-out', 'square',
       'static', 'status-bar', 'super', 'sw-resize', 'table-caption', 'table-cell',
       'table-column', 'table-column-group', 'table-footer-group', 'table-header-group',
       'table-row', 'table-row-group', 'text', 'text-bottom', 'text-top', 'thick',
       'thin', 'transparent', 'ultra-condensed', 'ultra-expanded', 'underline', 'upper-alpha',
       'upper-latin', 'upper-roman', 'uppercase', 'url', 'visible', 'w-resize', 'wait',
       'wider', 'x-fast', 'x-high', 'x-large', 'x-loud', 'x-low', 'x-small', 'x-soft',
       'xx-large', 'xx-small', 'yes'), suffix='\\b'),
            Name.Constant),
           (
            words(('indigo', 'gold', 'firebrick', 'indianred', 'darkolivegreen', 'darkseagreen',
       'mediumvioletred', 'mediumorchid', 'chartreuse', 'mediumslateblue', 'springgreen',
       'crimson', 'lightsalmon', 'brown', 'turquoise', 'olivedrab', 'cyan', 'skyblue',
       'darkturquoise', 'goldenrod', 'darkgreen', 'darkviolet', 'darkgray', 'lightpink',
       'darkmagenta', 'lightgoldenrodyellow', 'lavender', 'yellowgreen', 'thistle',
       'violet', 'orchid', 'ghostwhite', 'honeydew', 'cornflowerblue', 'darkblue',
       'darkkhaki', 'mediumpurple', 'cornsilk', 'bisque', 'slategray', 'darkcyan',
       'khaki', 'wheat', 'deepskyblue', 'darkred', 'steelblue', 'aliceblue', 'gainsboro',
       'mediumturquoise', 'floralwhite', 'coral', 'lightgrey', 'lightcyan', 'darksalmon',
       'beige', 'azure', 'lightsteelblue', 'oldlace', 'greenyellow', 'royalblue',
       'lightseagreen', 'mistyrose', 'sienna', 'lightcoral', 'orangered', 'navajowhite',
       'palegreen', 'burlywood', 'seashell', 'mediumspringgreen', 'papayawhip', 'blanchedalmond',
       'peru', 'aquamarine', 'darkslategray', 'ivory', 'dodgerblue', 'lemonchiffon',
       'chocolate', 'orange', 'forestgreen', 'slateblue', 'mintcream', 'antiquewhite',
       'darkorange', 'cadetblue', 'moccasin', 'limegreen', 'saddlebrown', 'darkslateblue',
       'lightskyblue', 'deeppink', 'plum', 'darkgoldenrod', 'sandybrown', 'magenta',
       'tan', 'rosybrown', 'pink', 'lightblue', 'palevioletred', 'mediumseagreen',
       'dimgray', 'powderblue', 'seagreen', 'snow', 'mediumblue', 'midnightblue',
       'paleturquoise', 'palegoldenrod', 'whitesmoke', 'darkorchid', 'salmon', 'lightslategray',
       'lawngreen', 'lightgreen', 'tomato', 'hotpink', 'lightyellow', 'lavenderblush',
       'linen', 'mediumaquamarine', 'blueviolet', 'peachpuff'), suffix='\\b'),
            Name.Entity),
           (
            words(('black', 'silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green',
       'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua'), suffix='\\b'),
            Name.Builtin),
           (
            '\\!(important|default)', Name.Exception),
           (
            '(true|false)', Name.Pseudo),
           (
            '(and|or|not)', Operator.Word),
           (
            '/\\*', Comment.Multiline, 'inline-comment'),
           (
            '//[^\\n]*', Comment.Single),
           (
            '\\#[a-z0-9]{1,6}', Number.Hex),
           (
            '(-?\\d+)(\\%|[a-z]+)?', bygroups(Number.Integer, Keyword.Type)),
           (
            '(-?\\d*\\.\\d+)(\\%|[a-z]+)?', bygroups(Number.Float, Keyword.Type)),
           (
            '#\\{', String.Interpol, 'interpolation'),
           (
            '[~^*!&%<>|+=@:,./?-]+', Operator),
           (
            '[\\[\\]()]+', Punctuation),
           (
            '"', String.Double, 'string-double'),
           (
            "'", String.Single, 'string-single'),
           (
            '[a-z_-][\\w-]*', Name)], 
 
 'interpolation': [
                   (
                    '\\}', String.Interpol, '#pop'),
                   include('value')], 
 
 'selector': [
              (
               '[ \\t]+', Text),
              (
               '\\:', Name.Decorator, 'pseudo-class'),
              (
               '\\.', Name.Class, 'class'),
              (
               '\\#', Name.Namespace, 'id'),
              (
               '[\\w-]+', Name.Tag),
              (
               '#\\{', String.Interpol, 'interpolation'),
              (
               '&', Keyword),
              (
               '[~^*!&\\[\\]()<>|+=@:;,./?-]', Operator),
              (
               '"', String.Double, 'string-double'),
              (
               "'", String.Single, 'string-single')], 
 
 'string-double': [
                   (
                    '(\\\\.|#(?=[^\\n{])|[^\\n"#])+', String.Double),
                   (
                    '#\\{', String.Interpol, 'interpolation'),
                   (
                    '"', String.Double, '#pop')], 
 
 'string-single': [
                   (
                    "(\\\\.|#(?=[^\\n{])|[^\\n'#])+", String.Double),
                   (
                    '#\\{', String.Interpol, 'interpolation'),
                   (
                    "'", String.Double, '#pop')], 
 
 'string-url': [
                (
                 '(\\\\#|#(?=[^\\n{])|[^\\n#)])+', String.Other),
                (
                 '#\\{', String.Interpol, 'interpolation'),
                (
                 '\\)', String.Other, '#pop')], 
 
 'pseudo-class': [
                  (
                   '[\\w-]+', Name.Decorator),
                  (
                   '#\\{', String.Interpol, 'interpolation'),
                  default('#pop')], 
 
 'class': [
           (
            '[\\w-]+', Name.Class),
           (
            '#\\{', String.Interpol, 'interpolation'),
           default('#pop')], 
 
 'id': [
        (
         '[\\w-]+', Name.Namespace),
        (
         '#\\{', String.Interpol, 'interpolation'),
        default('#pop')], 
 
 'for': [
         (
          '(from|to|through)', Operator.Word),
         include('value')]}

def _indentation(lexer, match, ctx):
    indentation = match.group(0)
    yield (match.start(), Text, indentation)
    ctx.last_indentation = indentation
    ctx.pos = match.end()
    if hasattr(ctx, 'block_state') and ctx.block_state and indentation.startswith(ctx.block_indentation) and indentation != ctx.block_indentation:
        ctx.stack.append(ctx.block_state)
    else:
        ctx.block_state = None
        ctx.block_indentation = None
        ctx.stack.append('content')


def _starts_block(token, state):

    def callback(lexer, match, ctx):
        yield (
         match.start(), token, match.group(0))
        if hasattr(ctx, 'last_indentation'):
            ctx.block_indentation = ctx.last_indentation
        else:
            ctx.block_indentation = ''
        ctx.block_state = state
        ctx.pos = match.end()

    return callback


class SassLexer(ExtendedRegexLexer):
    __doc__ = '\n    For Sass stylesheets.\n\n    .. versionadded:: 1.3\n    '
    name = 'Sass'
    aliases = ['sass']
    filenames = ['*.sass']
    mimetypes = ['text/x-sass']
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              (
               '[ \\t]*\\n', Text),
              (
               '[ \\t]*', _indentation)], 
     
     'content': [
                 (
                  '//[^\\n]*', _starts_block(Comment.Single, 'single-comment'),
                  'root'),
                 (
                  '/\\*[^\\n]*', _starts_block(Comment.Multiline, 'multi-comment'),
                  'root'),
                 (
                  '@import', Keyword, 'import'),
                 (
                  '@for', Keyword, 'for'),
                 (
                  '@(debug|warn|if|while)', Keyword, 'value'),
                 (
                  '(@mixin)( [\\w-]+)', bygroups(Keyword, Name.Function), 'value'),
                 (
                  '(@include)( [\\w-]+)', bygroups(Keyword, Name.Decorator), 'value'),
                 (
                  '@extend', Keyword, 'selector'),
                 (
                  '@[\\w-]+', Keyword, 'selector'),
                 (
                  '=[\\w-]+', Name.Function, 'value'),
                 (
                  '\\+[\\w-]+', Name.Decorator, 'value'),
                 (
                  '([!$][\\w-]\\w*)([ \\t]*(?:(?:\\|\\|)?=|:))',
                  bygroups(Name.Variable, Operator), 'value'),
                 (
                  ':', Name.Attribute, 'old-style-attr'),
                 (
                  '(?=.+?[=:]([^a-z]|$))', Name.Attribute, 'new-style-attr'),
                 default('selector')], 
     
     'single-comment': [
                        (
                         '.+', Comment.Single),
                        (
                         '\\n', Text, 'root')], 
     
     'multi-comment': [
                       (
                        '.+', Comment.Multiline),
                       (
                        '\\n', Text, 'root')], 
     
     'import': [
                (
                 '[ \\t]+', Text),
                (
                 '\\S+', String),
                (
                 '\\n', Text, 'root')], 
     
     'old-style-attr': [
                        (
                         '[^\\s:="\\[]+', Name.Attribute),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '[ \\t]*=', Operator, 'value'),
                        default('value')], 
     
     'new-style-attr': [
                        (
                         '[^\\s:="\\[]+', Name.Attribute),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '[ \\t]*[=:]', Operator, 'value')], 
     
     'inline-comment': [
                        (
                         '(\\\\#|#(?=[^\\n{])|\\*(?=[^\\n/])|[^\\n#*])+', Comment.Multiline),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '\\*/', Comment, '#pop')]}
    for group, common in iteritems(common_sass_tokens):
        tokens[group] = copy.copy(common)

    tokens['value'].append(('\\n', Text, 'root'))
    tokens['selector'].append(('\\n', Text, 'root'))


class ScssLexer(RegexLexer):
    __doc__ = '\n    For SCSS stylesheets.\n    '
    name = 'SCSS'
    aliases = ['scss']
    filenames = ['*.scss']
    mimetypes = ['text/x-scss']
    flags = re.IGNORECASE | re.DOTALL
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               '@import', Keyword, 'value'),
              (
               '@for', Keyword, 'for'),
              (
               '@(debug|warn|if|while)', Keyword, 'value'),
              (
               '(@mixin)( [\\w-]+)', bygroups(Keyword, Name.Function), 'value'),
              (
               '(@include)( [\\w-]+)', bygroups(Keyword, Name.Decorator), 'value'),
              (
               '@extend', Keyword, 'selector'),
              (
               '(@media)(\\s+)', bygroups(Keyword, Text), 'value'),
              (
               '@[\\w-]+', Keyword, 'selector'),
              (
               '(\\$[\\w-]*\\w)([ \\t]*:)', bygroups(Name.Variable, Operator), 'value'),
              default('selector')], 
     
     'attr': [
              (
               '[^\\s:="\\[]+', Name.Attribute),
              (
               '#\\{', String.Interpol, 'interpolation'),
              (
               '[ \\t]*:', Operator, 'value'),
              default('#pop')], 
     
     'inline-comment': [
                        (
                         '(\\\\#|#(?=[^{])|\\*(?=[^/])|[^#*])+', Comment.Multiline),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '\\*/', Comment, '#pop')]}
    for group, common in iteritems(common_sass_tokens):
        tokens[group] = copy.copy(common)

    tokens['value'].extend([('\\n', Text), ('[;{}]', Punctuation, '#pop')])
    tokens['selector'].extend([('\\n', Text), ('[;{}]', Punctuation, '#pop')])


class LessCssLexer(CssLexer):
    __doc__ = '\n    For `LESS <http://lesscss.org/>`_ styleshets.\n\n    .. versionadded:: 2.1\n    '
    name = 'LessCss'
    aliases = ['less']
    filenames = ['*.less']
    mimetypes = ['text/x-less-css']
    tokens = {'root': [
              (
               '@\\w+', Name.Variable),
              inherit], 
     
     'content': [
                 (
                  '{', Punctuation, '#push'),
                 inherit]}
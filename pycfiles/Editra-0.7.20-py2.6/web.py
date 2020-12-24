# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/lexers/web.py
# Compiled at: 2011-04-22 17:53:26
"""
    pygments.lexers.web
    ~~~~~~~~~~~~~~~~~~~

    Lexers for web-related languages and markup.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re, copy
from pygments.lexer import RegexLexer, ExtendedRegexLexer, bygroups, using, include, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Other, Punctuation, Literal
from pygments.util import get_bool_opt, get_list_opt, looks_like_xml, html_doctype_matches
from pygments.lexers.agile import RubyLexer
from pygments.lexers.compiled import ScalaLexer
__all__ = [
 'HtmlLexer', 'XmlLexer', 'JavascriptLexer', 'CssLexer',
 'PhpLexer', 'ActionScriptLexer', 'XsltLexer', 'ActionScript3Lexer',
 'MxmlLexer', 'HaxeLexer', 'HamlLexer', 'SassLexer', 'ScssLexer',
 'ObjectiveJLexer', 'CoffeeScriptLexer', 'DuelLexer', 'ScamlLexer',
 'JadeLexer', 'XQueryLexer']

class JavascriptLexer(RegexLexer):
    """
    For JavaScript source code.
    """
    name = 'JavaScript'
    aliases = ['js', 'javascript']
    filenames = ['*.js']
    mimetypes = ['application/javascript', 'application/x-javascript',
     'text/x-javascript', 'text/javascript']
    flags = re.DOTALL
    tokens = {'commentsandwhitespace': [
                               (
                                '\\s+', Text),
                               (
                                '<!--', Comment),
                               (
                                '//.*?\\n', Comment.Single),
                               (
                                '/\\*.*?\\*/', Comment.Multiline)], 
       'slashstartsregex': [
                          include('commentsandwhitespace'),
                          (
                           '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
                           String.Regex, '#pop'),
                          (
                           '(?=/)', Text, ('#pop', 'badregex')),
                          (
                           '', Text, '#pop')], 
       'badregex': [
                  (
                   '\n', Text, '#pop')], 
       'root': [
              (
               '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
              include('commentsandwhitespace'),
              (
               '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&\\|\\^/])=?',
               Operator, 'slashstartsregex'),
              (
               '[{(\\[;,]', Punctuation, 'slashstartsregex'),
              (
               '[})\\].]', Punctuation),
              (
               '(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|this)\\b',
               Keyword, 'slashstartsregex'),
              (
               '(var|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
              (
               '(abstract|boolean|byte|char|class|const|debugger|double|enum|export|extends|final|float|goto|implements|import|int|interface|long|native|package|private|protected|public|short|static|super|synchronized|throws|transient|volatile)\\b',
               Keyword.Reserved),
              (
               '(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant),
              (
               '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|window)\\b',
               Name.Builtin),
              (
               '[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-fA-F]+', Number.Hex),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}


class ActionScriptLexer(RegexLexer):
    """
    For ActionScript source code.

    *New in Pygments 0.9.*
    """
    name = 'ActionScript'
    aliases = ['as', 'actionscript']
    filenames = ['*.as']
    mimetypes = ['application/x-actionscript', 'text/x-actionscript',
     'text/actionscript']
    flags = re.DOTALL
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               '/(\\\\\\\\|\\\\/|[^/\\n])*/[gim]*', String.Regex),
              (
               '[~\\^\\*!%&<>\\|+=:;,/?\\\\-]+', Operator),
              (
               '[{}\\[\\]();.]+', Punctuation),
              (
               '(case|default|for|each|in|while|do|break|return|continue|if|else|throw|try|catch|var|with|new|typeof|arguments|instanceof|this|switch)\\b',
               Keyword),
              (
               '(class|public|final|internal|native|override|private|protected|static|import|extends|implements|interface|intrinsic|return|super|dynamic|function|const|get|namespace|package|set)\\b',
               Keyword.Declaration),
              (
               '(true|false|null|NaN|Infinity|-Infinity|undefined|Void)\\b',
               Keyword.Constant),
              (
               '(Accessibility|AccessibilityProperties|ActionScriptVersion|ActivityEvent|AntiAliasType|ApplicationDomain|AsBroadcaster|Array|AsyncErrorEvent|AVM1Movie|BevelFilter|Bitmap|BitmapData|BitmapDataChannel|BitmapFilter|BitmapFilterQuality|BitmapFilterType|BlendMode|BlurFilter|Boolean|ByteArray|Camera|Capabilities|CapsStyle|Class|Color|ColorMatrixFilter|ColorTransform|ContextMenu|ContextMenuBuiltInItems|ContextMenuEvent|ContextMenuItem|ConvultionFilter|CSMSettings|DataEvent|Date|DefinitionError|DeleteObjectSample|Dictionary|DisplacmentMapFilter|DisplayObject|DisplacmentMapFilterMode|DisplayObjectContainer|DropShadowFilter|Endian|EOFError|Error|ErrorEvent|EvalError|Event|EventDispatcher|EventPhase|ExternalInterface|FileFilter|FileReference|FileReferenceList|FocusDirection|FocusEvent|Font|FontStyle|FontType|FrameLabel|FullScreenEvent|Function|GlowFilter|GradientBevelFilter|GradientGlowFilter|GradientType|Graphics|GridFitType|HTTPStatusEvent|IBitmapDrawable|ID3Info|IDataInput|IDataOutput|IDynamicPropertyOutputIDynamicPropertyWriter|IEventDispatcher|IExternalizable|IllegalOperationError|IME|IMEConversionMode|IMEEvent|int|InteractiveObject|InterpolationMethod|InvalidSWFError|InvokeEvent|IOError|IOErrorEvent|JointStyle|Key|Keyboard|KeyboardEvent|KeyLocation|LineScaleMode|Loader|LoaderContext|LoaderInfo|LoadVars|LocalConnection|Locale|Math|Matrix|MemoryError|Microphone|MorphShape|Mouse|MouseEvent|MovieClip|MovieClipLoader|Namespace|NetConnection|NetStatusEvent|NetStream|NewObjectSample|Number|Object|ObjectEncoding|PixelSnapping|Point|PrintJob|PrintJobOptions|PrintJobOrientation|ProgressEvent|Proxy|QName|RangeError|Rectangle|ReferenceError|RegExp|Responder|Sample|Scene|ScriptTimeoutError|Security|SecurityDomain|SecurityError|SecurityErrorEvent|SecurityPanel|Selection|Shape|SharedObject|SharedObjectFlushStatus|SimpleButton|Socket|Sound|SoundChannel|SoundLoaderContext|SoundMixer|SoundTransform|SpreadMethod|Sprite|StackFrame|StackOverflowError|Stage|StageAlign|StageDisplayState|StageQuality|StageScaleMode|StaticText|StatusEvent|String|StyleSheet|SWFVersion|SyncEvent|SyntaxError|System|TextColorType|TextField|TextFieldAutoSize|TextFieldType|TextFormat|TextFormatAlign|TextLineMetrics|TextRenderer|TextSnapshot|Timer|TimerEvent|Transform|TypeError|uint|URIError|URLLoader|URLLoaderDataFormat|URLRequest|URLRequestHeader|URLRequestMethod|URLStream|URLVariabeles|VerifyError|Video|XML|XMLDocument|XMLList|XMLNode|XMLNodeType|XMLSocket|XMLUI)\\b',
               Name.Builtin),
              (
               '(decodeURI|decodeURIComponent|encodeURI|escape|eval|isFinite|isNaN|isXMLName|clearInterval|fscommand|getTimer|getURL|getVersion|isFinite|parseFloat|parseInt|setInterval|trace|updateAfterEvent|unescape)\\b',
               Name.Function),
              (
               '[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-f]+', Number.Hex),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}

    def analyse_text(text):
        return 0.05


class ActionScript3Lexer(RegexLexer):
    """
    For ActionScript 3 source code.

    *New in Pygments 0.11.*
    """
    name = 'ActionScript 3'
    aliases = ['as3', 'actionscript3']
    filenames = ['*.as']
    mimetypes = ['application/x-actionscript', 'text/x-actionscript',
     'text/actionscript']
    identifier = '[$a-zA-Z_][a-zA-Z0-9_]*'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(function\\s+)(' + identifier + ')(\\s*)(\\()',
               bygroups(Keyword.Declaration, Name.Function, Text, Operator),
               'funcparams'),
              (
               '(var|const)(\\s+)(' + identifier + ')(\\s*)(:)(\\s*)(' + identifier + ')',
               bygroups(Keyword.Declaration, Text, Name, Text, Punctuation, Text, Keyword.Type)),
              (
               '(import|package)(\\s+)((?:' + identifier + '|\\.)+)(\\s*)',
               bygroups(Keyword, Text, Name.Namespace, Text)),
              (
               '(new)(\\s+)(' + identifier + ')(\\s*)(\\()',
               bygroups(Keyword, Text, Keyword.Type, Text, Operator)),
              (
               '//.*?\\n', Comment.Single),
              (
               '/\\*.*?\\*/', Comment.Multiline),
              (
               '/(\\\\\\\\|\\\\/|[^\\n])*/[gisx]*', String.Regex),
              (
               '(\\.)(' + identifier + ')', bygroups(Operator, Name.Attribute)),
              (
               '(case|default|for|each|in|while|do|break|return|continue|if|else|throw|try|catch|with|new|typeof|arguments|instanceof|this|switch|import|include|as|is)\\b',
               Keyword),
              (
               '(class|public|final|internal|native|override|private|protected|static|import|extends|implements|interface|intrinsic|return|super|dynamic|function|const|get|namespace|package|set)\\b',
               Keyword.Declaration),
              (
               '(true|false|null|NaN|Infinity|-Infinity|undefined|void)\\b',
               Keyword.Constant),
              (
               '(decodeURI|decodeURIComponent|encodeURI|escape|eval|isFinite|isNaN|isXMLName|clearInterval|fscommand|getTimer|getURL|getVersion|isFinite|parseFloat|parseInt|setInterval|trace|updateAfterEvent|unescape)\\b',
               Name.Function),
              (
               identifier, Name),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-f]+', Number.Hex),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
              (
               '[~\\^\\*!%&<>\\|+=:;,/?\\\\{}\\[\\]();.-]+', Operator)], 
       'funcparams': [
                    (
                     '\\s+', Text),
                    (
                     '(\\s*)(\\.\\.\\.)?(' + identifier + ')(\\s*)(:)(\\s*)(' + identifier + '|\\*)(\\s*)',
                     bygroups(Text, Punctuation, Name, Text, Operator, Text, Keyword.Type, Text), 'defval'),
                    (
                     '\\)', Operator, 'type')], 
       'type': [
              (
               '(\\s*)(:)(\\s*)(' + identifier + '|\\*)',
               bygroups(Text, Operator, Text, Keyword.Type), '#pop:2'),
              (
               '\\s*', Text, '#pop:2')], 
       'defval': [
                (
                 '(=)(\\s*)([^(),]+)(\\s*)(,?)',
                 bygroups(Operator, Text, using(this), Text, Operator), '#pop'),
                (
                 ',?', Operator, '#pop')]}

    def analyse_text(text):
        if re.match('\\w+\\s*:\\s*\\w', text):
            return 0.3
        return 0.1


class CssLexer(RegexLexer):
    """
    For CSS (Cascading Style Sheets).
    """
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
                 '{', Punctuation, 'content'),
                (
                 '\\:[a-zA-Z0-9_-]+', Name.Decorator),
                (
                 '\\.[a-zA-Z0-9_-]+', Name.Class),
                (
                 '\\#[a-zA-Z0-9_-]+', Name.Function),
                (
                 '@[a-zA-Z0-9_-]+', Keyword, 'atrule'),
                (
                 '[a-zA-Z0-9_-]+', Name.Tag),
                (
                 '[~\\^\\*!%&\\[\\]\\(\\)<>\\|+=@:;,./?-]', Operator),
                (
                 '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                (
                 "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)], 
       'atrule': [
                (
                 '{', Punctuation, 'atcontent'),
                (
                 ';', Punctuation, '#pop'),
                include('basics')], 
       'atcontent': [
                   include('basics'),
                   (
                    '}', Punctuation, '#pop:2')], 
       'content': [
                 (
                  '\\s+', Text),
                 (
                  '}', Punctuation, '#pop'),
                 (
                  'url\\(.*?\\)', String.Other),
                 (
                  '^@.*?$', Comment.Preproc),
                 (
                  '(azimuth|background-attachment|background-color|background-image|background-position|background-repeat|background|border-bottom-color|border-bottom-style|border-bottom-width|border-left-color|border-left-style|border-left-width|border-right|border-right-color|border-right-style|border-right-width|border-top-color|border-top-style|border-top-width|border-bottom|border-collapse|border-left|border-width|border-color|border-spacing|border-style|border-top|border|caption-side|clear|clip|color|content|counter-increment|counter-reset|cue-after|cue-before|cue|cursor|direction|display|elevation|empty-cells|float|font-family|font-size|font-size-adjust|font-stretch|font-style|font-variant|font-weight|font|height|letter-spacing|line-height|list-style-type|list-style-image|list-style-position|list-style|margin-bottom|margin-left|margin-right|margin-top|margin|marker-offset|marks|max-height|max-width|min-height|min-width|opacity|orphans|outline|outline-color|outline-style|outline-width|overflow(?:-x|-y|)|padding-bottom|padding-left|padding-right|padding-top|padding|page|page-break-after|page-break-before|page-break-inside|pause-after|pause-before|pause|pitch|pitch-range|play-during|position|quotes|richness|right|size|speak-header|speak-numeral|speak-punctuation|speak|speech-rate|stress|table-layout|text-align|text-decoration|text-indent|text-shadow|text-transform|top|unicode-bidi|vertical-align|visibility|voice-family|volume|white-space|widows|width|word-spacing|z-index|bottom|left|above|absolute|always|armenian|aural|auto|avoid|baseline|behind|below|bidi-override|blink|block|bold|bolder|both|capitalize|center-left|center-right|center|circle|cjk-ideographic|close-quote|collapse|condensed|continuous|crop|crosshair|cross|cursive|dashed|decimal-leading-zero|decimal|default|digits|disc|dotted|double|e-resize|embed|extra-condensed|extra-expanded|expanded|fantasy|far-left|far-right|faster|fast|fixed|georgian|groove|hebrew|help|hidden|hide|higher|high|hiragana-iroha|hiragana|icon|inherit|inline-table|inline|inset|inside|invert|italic|justify|katakana-iroha|katakana|landscape|larger|large|left-side|leftwards|level|lighter|line-through|list-item|loud|lower-alpha|lower-greek|lower-roman|lowercase|ltr|lower|low|medium|message-box|middle|mix|monospace|n-resize|narrower|ne-resize|no-close-quote|no-open-quote|no-repeat|none|normal|nowrap|nw-resize|oblique|once|open-quote|outset|outside|overline|pointer|portrait|px|relative|repeat-x|repeat-y|repeat|rgb|ridge|right-side|rightwards|s-resize|sans-serif|scroll|se-resize|semi-condensed|semi-expanded|separate|serif|show|silent|slow|slower|small-caps|small-caption|smaller|soft|solid|spell-out|square|static|status-bar|super|sw-resize|table-caption|table-cell|table-column|table-column-group|table-footer-group|table-header-group|table-row|table-row-group|text|text-bottom|text-top|thick|thin|transparent|ultra-condensed|ultra-expanded|underline|upper-alpha|upper-latin|upper-roman|uppercase|url|visible|w-resize|wait|wider|x-fast|x-high|x-large|x-loud|x-low|x-small|x-soft|xx-large|xx-small|yes)\\b',
                  Keyword),
                 (
                  '(indigo|gold|firebrick|indianred|yellow|darkolivegreen|darkseagreen|mediumvioletred|mediumorchid|chartreuse|mediumslateblue|black|springgreen|crimson|lightsalmon|brown|turquoise|olivedrab|cyan|silver|skyblue|gray|darkturquoise|goldenrod|darkgreen|darkviolet|darkgray|lightpink|teal|darkmagenta|lightgoldenrodyellow|lavender|yellowgreen|thistle|violet|navy|orchid|blue|ghostwhite|honeydew|cornflowerblue|darkblue|darkkhaki|mediumpurple|cornsilk|red|bisque|slategray|darkcyan|khaki|wheat|deepskyblue|darkred|steelblue|aliceblue|gainsboro|mediumturquoise|floralwhite|coral|purple|lightgrey|lightcyan|darksalmon|beige|azure|lightsteelblue|oldlace|greenyellow|royalblue|lightseagreen|mistyrose|sienna|lightcoral|orangered|navajowhite|lime|palegreen|burlywood|seashell|mediumspringgreen|fuchsia|papayawhip|blanchedalmond|peru|aquamarine|white|darkslategray|ivory|dodgerblue|lemonchiffon|chocolate|orange|forestgreen|slateblue|olive|mintcream|antiquewhite|darkorange|cadetblue|moccasin|limegreen|saddlebrown|darkslateblue|lightskyblue|deeppink|plum|aqua|darkgoldenrod|maroon|sandybrown|magenta|tan|rosybrown|pink|lightblue|palevioletred|mediumseagreen|dimgray|powderblue|seagreen|snow|mediumblue|midnightblue|paleturquoise|palegoldenrod|whitesmoke|darkorchid|salmon|lightslategray|lawngreen|lightgreen|tomato|hotpink|lightyellow|lavenderblush|linen|mediumaquamarine|green|blueviolet|peachpuff)\\b',
                  Name.Builtin),
                 (
                  '\\!important', Comment.Preproc),
                 (
                  '/\\*(?:.|\\n)*?\\*/', Comment),
                 (
                  '\\#[a-zA-Z0-9]{1,6}', Number),
                 (
                  '[\\.-]?[0-9]*[\\.]?[0-9]+(em|px|\\%|pt|pc|in|mm|cm|ex|s)\\b', Number),
                 (
                  '-?[0-9]+', Number),
                 (
                  '[~\\^\\*!%&<>\\|+=@:,./?-]+', Operator),
                 (
                  '[\\[\\]();]+', Punctuation),
                 (
                  '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                 (
                  "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
                 (
                  '[a-zA-Z][a-zA-Z0-9]+', Name)]}


class ObjectiveJLexer(RegexLexer):
    """
    For Objective-J source code with preprocessor directives.

    *New in Pygments 1.3.*
    """
    name = 'Objective-J'
    aliases = ['objective-j', 'objectivej', 'obj-j', 'objj']
    filenames = ['*.j']
    mimetypes = ['text/x-objective-j']
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)*'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root': [
              include('whitespace'),
              (
               '^(' + _ws + '[\\+-]' + _ws + ')([\\(a-zA-Z_].*?[^\\(])(' + _ws + '{)',
               bygroups(using(this), using(this, state='function_signature'), using(this))),
              (
               '(@interface|@implementation)(\\s+)', bygroups(Keyword, Text),
               'classname'),
              (
               '(@class|@protocol)(\\s*)', bygroups(Keyword, Text),
               'forward_classname'),
              (
               '(\\s*)(@end)(\\s*)', bygroups(Text, Keyword, Text)),
              include('statements'),
              (
               '[{\\(\\)}]', Punctuation),
              (
               ';', Punctuation)], 
       'whitespace': [
                    (
                     '(@import)(\\s+)("(\\\\\\\\|\\\\"|[^"])*")',
                     bygroups(Comment.Preproc, Text, String.Double)),
                    (
                     '(@import)(\\s+)(<(\\\\\\\\|\\\\>|[^>])*>)',
                     bygroups(Comment.Preproc, Text, String.Double)),
                    (
                     '(#(?:include|import))(\\s+)("(\\\\\\\\|\\\\"|[^"])*")',
                     bygroups(Comment.Preproc, Text, String.Double)),
                    (
                     '(#(?:include|import))(\\s+)(<(\\\\\\\\|\\\\>|[^>])*>)',
                     bygroups(Comment.Preproc, Text, String.Double)),
                    (
                     '#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '#', Comment.Preproc, 'macro'),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
                    (
                     '<!--', Comment)], 
       'slashstartsregex': [
                          include('whitespace'),
                          (
                           '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
                           String.Regex, '#pop'),
                          (
                           '(?=/)', Text, ('#pop', 'badregex')),
                          (
                           '', Text, '#pop')], 
       'badregex': [
                  (
                   '\n', Text, '#pop')], 
       'statements': [
                    (
                     '(L|@)?"', String, 'string'),
                    (
                     "(L|@)?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
                     String.Char),
                    (
                     '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                    (
                     "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
                    (
                     '0[0-7]+[Ll]?', Number.Oct),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
                    (
                     '\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&\\|\\^/])=?',
                     Operator, 'slashstartsregex'),
                    (
                     '[{(\\[;,]', Punctuation, 'slashstartsregex'),
                    (
                     '[})\\].]', Punctuation),
                    (
                     '(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|prototype|__proto__)\\b',
                     Keyword, 'slashstartsregex'),
                    (
                     '(var|with|function)\\b', Keyword.Declaration, 'slashstartsregex'),
                    (
                     '(@selector|@private|@protected|@public|@encode|@synchronized|@try|@throw|@catch|@finally|@end|@property|@synthesize|@dynamic|@for|@accessors|new)\\b',
                     Keyword),
                    (
                     '(int|long|float|short|double|char|unsigned|signed|void|id|BOOL|bool|boolean|IBOutlet|IBAction|SEL|@outlet|@action)\\b',
                     Keyword.Type),
                    (
                     '(self|super)\\b', Name.Builtin),
                    (
                     '(TRUE|YES|FALSE|NO|Nil|nil|NULL)\\b', Keyword.Constant),
                    (
                     '(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant),
                    (
                     '(ABS|ASIN|ACOS|ATAN|ATAN2|SIN|COS|TAN|EXP|POW|CEIL|FLOOR|ROUND|MIN|MAX|RAND|SQRT|E|LN2|LN10|LOG2E|LOG10E|PI|PI2|PI_2|SQRT1_2|SQRT2)\\b',
                     Keyword.Constant),
                    (
                     '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|window)\\b',
                     Name.Builtin),
                    (
                     '([$a-zA-Z_][a-zA-Z0-9_]*)(' + _ws + ')(?=\\()',
                     bygroups(Name.Function, using(this))),
                    (
                     '[$a-zA-Z_][a-zA-Z0-9_]*', Name)], 
       'classname': [
                   (
                    '([a-zA-Z_][a-zA-Z0-9_]*)(' + _ws + ':' + _ws + ')([a-zA-Z_][a-zA-Z0-9_]*)?',
                    bygroups(Name.Class, using(this), Name.Class), '#pop'),
                   (
                    '([a-zA-Z_][a-zA-Z0-9_]*)(' + _ws + '\\()([a-zA-Z_][a-zA-Z0-9_]*)(\\))',
                    bygroups(Name.Class, using(this), Name.Label, Text), '#pop'),
                   (
                    '([a-zA-Z_][a-zA-Z0-9_]*)', Name.Class, '#pop')], 
       'forward_classname': [
                           (
                            '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*,\\s*)',
                            bygroups(Name.Class, Text), '#push'),
                           (
                            '([a-zA-Z_][a-zA-Z0-9_]*)(\\s*;?)',
                            bygroups(Name.Class, Text), '#pop')], 
       'function_signature': [
                            include('whitespace'),
                            (
                             '(\\(' + _ws + ')([a-zA-Z_][a-zA-Z0-9_]+)(' + _ws + '\\)' + _ws + ')([$a-zA-Z_][a-zA-Z0-9_]+' + _ws + ':)',
                             bygroups(using(this), Keyword.Type, using(this), Name.Function), 'function_parameters'),
                            (
                             '(\\(' + _ws + ')([a-zA-Z_][a-zA-Z0-9_]+)(' + _ws + '\\)' + _ws + ')([$a-zA-Z_][a-zA-Z0-9_]+)',
                             bygroups(using(this), Keyword.Type, using(this), Name.Function), '#pop'),
                            (
                             '([$a-zA-Z_][a-zA-Z0-9_]+' + _ws + ':)',
                             bygroups(Name.Function), 'function_parameters'),
                            (
                             '([$a-zA-Z_][a-zA-Z0-9_]+)',
                             bygroups(Name.Function), '#pop'),
                            (
                             '', Text, '#pop')], 
       'function_parameters': [
                             include('whitespace'),
                             (
                              '(\\(' + _ws + ')([^\\)]+)(' + _ws + '\\)' + _ws + ')+([$a-zA-Z_][a-zA-Z0-9_]+)',
                              bygroups(using(this), Keyword.Type, using(this), Text)),
                             (
                              '([$a-zA-Z_][a-zA-Z0-9_]+' + _ws + ':)',
                              Name.Function),
                             (
                              '(:)', Name.Function),
                             (
                              '(,' + _ws + '...)', using(this)),
                             (
                              '([$a-zA-Z_][a-zA-Z0-9_]+)', Text)], 
       'expression': [
                    (
                     '([$a-zA-Z_][a-zA-Z0-9_]*)(\\()',
                     bygroups(Name.Function, Punctuation)),
                    (
                     '(\\))', Punctuation, '#pop')], 
       'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
       'macro': [
               (
                '[^/\\n]+', Comment.Preproc),
               (
                '/[*](.|\\n)*?[*]/', Comment.Multiline),
               (
                '//.*?\\n', Comment.Single, '#pop'),
               (
                '/', Comment.Preproc),
               (
                '(?<=\\\\)\\n', Comment.Preproc),
               (
                '\\n', Comment.Preproc, '#pop')], 
       'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)]}

    def analyse_text(text):
        if re.search('^\\s*@import\\s+[<"]', text, re.MULTILINE):
            return True
        return False


class HtmlLexer(RegexLexer):
    """
    For HTML 4 and XHTML 1 markup. Nested JavaScript and CSS is highlighted
    by the appropriate lexer.
    """
    name = 'HTML'
    aliases = ['html']
    filenames = ['*.html', '*.htm', '*.xhtml', '*.xslt']
    mimetypes = ['text/html', 'application/xhtml+xml']
    flags = re.IGNORECASE | re.DOTALL
    tokens = {'root': [
              (
               '[^<&]+', Text),
              (
               '&\\S*?;', Name.Entity),
              (
               '\\<\\!\\[CDATA\\[.*?\\]\\]\\>', Comment.Preproc),
              (
               '<!--', Comment, 'comment'),
              (
               '<\\?.*?\\?>', Comment.Preproc),
              (
               '<![^>]*>', Comment.Preproc),
              (
               '<\\s*script\\s*', Name.Tag, ('script-content', 'tag')),
              (
               '<\\s*style\\s*', Name.Tag, ('style-content', 'tag')),
              (
               '<\\s*[a-zA-Z0-9:]+', Name.Tag, 'tag'),
              (
               '<\\s*/\\s*[a-zA-Z0-9:]+\\s*>', Name.Tag)], 
       'comment': [
                 (
                  '[^-]+', Comment),
                 (
                  '-->', Comment, '#pop'),
                 (
                  '-', Comment)], 
       'tag': [
             (
              '\\s+', Text),
             (
              '[a-zA-Z0-9_:-]+\\s*=', Name.Attribute, 'attr'),
             (
              '[a-zA-Z0-9_:-]+', Name.Attribute),
             (
              '/?\\s*>', Name.Tag, '#pop')], 
       'script-content': [
                        (
                         '<\\s*/\\s*script\\s*>', Name.Tag, '#pop'),
                        (
                         '.+?(?=<\\s*/\\s*script\\s*>)', using(JavascriptLexer))], 
       'style-content': [
                       (
                        '<\\s*/\\s*style\\s*>', Name.Tag, '#pop'),
                       (
                        '.+?(?=<\\s*/\\s*style\\s*>)', using(CssLexer))], 
       'attr': [
              (
               '".*?"', String, '#pop'),
              (
               "'.*?'", String, '#pop'),
              (
               '[^\\s>]+', String, '#pop')]}

    def analyse_text(text):
        if html_doctype_matches(text):
            return 0.5


class PhpLexer(RegexLexer):
    """
    For `PHP <http://www.php.net/>`_ source code.
    For PHP embedded in HTML, use the `HtmlPhpLexer`.

    Additional options accepted:

    `startinline`
        If given and ``True`` the lexer starts highlighting with
        php code (i.e.: no starting ``<?php`` required).  The default
        is ``False``.
    `funcnamehighlighting`
        If given and ``True``, highlight builtin function names
        (default: ``True``).
    `disabledmodules`
        If given, must be a list of module names whose function names
        should not be highlighted. By default all modules are highlighted
        except the special ``'unknown'`` module that includes functions
        that are known to php but are undocumented.

        To get a list of allowed modules have a look into the
        `_phpbuiltins` module:

        .. sourcecode:: pycon

            >>> from pygments.lexers._phpbuiltins import MODULES
            >>> MODULES.keys()
            ['PHP Options/Info', 'Zip', 'dba', ...]

        In fact the names of those modules match the module names from
        the php documentation.
    """
    name = 'PHP'
    aliases = ['php', 'php3', 'php4', 'php5']
    filenames = ['*.php', '*.php[345]']
    mimetypes = ['text/x-php']
    flags = re.IGNORECASE | re.DOTALL | re.MULTILINE
    tokens = {'root': [
              (
               '<\\?(php)?', Comment.Preproc, 'php'),
              (
               '[^<]+', Other),
              (
               '<', Other)], 
       'php': [
             (
              '\\?>', Comment.Preproc, '#pop'),
             (
              "<<<(\\'?)([a-zA-Z_][a-zA-Z0-9_]*)\\1\\n.*?\\n\\2\\;?\\n", String),
             (
              '\\s+', Text),
             (
              '#.*?\\n', Comment.Single),
             (
              '//.*?\\n', Comment.Single),
             (
              '/\\*\\*/', Comment.Multiline),
             (
              '/\\*\\*.*?\\*/', String.Doc),
             (
              '/\\*.*?\\*/', Comment.Multiline),
             (
              '(->|::)(\\s*)([a-zA-Z_][a-zA-Z0-9_]*)',
              bygroups(Operator, Text, Name.Attribute)),
             (
              '[~!%^&*+=|:.<>/?@-]+', Operator),
             (
              '[\\[\\]{}();,]+', Punctuation),
             (
              '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
             (
              '(function)(\\s*)(?=\\()', bygroups(Keyword, Text)),
             (
              '(function)(\\s+)(&?)(\\s*)',
              bygroups(Keyword, Text, Operator, Text), 'functionname'),
             (
              '(const)(\\s+)([a-zA-Z_][a-zA-Z0-9_]*)',
              bygroups(Keyword, Text, Name.Constant)),
             (
              '(and|E_PARSE|old_function|E_ERROR|or|as|E_WARNING|parent|eval|PHP_OS|break|exit|case|extends|PHP_VERSION|cfunction|FALSE|print|for|require|continue|foreach|require_once|declare|return|default|static|do|switch|die|stdClass|echo|else|TRUE|elseif|var|empty|if|xor|enddeclare|include|virtual|endfor|include_once|while|endforeach|global|__FILE__|endif|list|__LINE__|endswitch|new|__sleep|endwhile|not|array|__wakeup|E_ALL|NULL|final|php_user_filter|interface|implements|public|private|protected|abstract|clone|try|catch|throw|this|use|namespace)\\b',
              Keyword),
             (
              '(true|false|null)\x08', Keyword.Constant),
             (
              '\\$\\{\\$+[a-zA-Z_][a-zA-Z0-9_]*\\}', Name.Variable),
             (
              '\\$+[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable),
             (
              '[\\\\a-zA-Z_][\\\\a-zA-Z0-9_]*', Name.Other),
             (
              '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
             (
              '\\d+[eE][+-]?[0-9]+', Number.Float),
             (
              '0[0-7]+', Number.Oct),
             (
              '0[xX][a-fA-F0-9]+', Number.Hex),
             (
              '\\d+', Number.Integer),
             (
              "'([^'\\\\]*(?:\\\\.[^'\\\\]*)*)'", String.Single),
             (
              '`([^`\\\\]*(?:\\\\.[^`\\\\]*)*)`', String.Backtick),
             (
              '"', String.Double, 'string')], 
       'classname': [
                   (
                    '[a-zA-Z_][\\\\a-zA-Z0-9_]*', Name.Class, '#pop')], 
       'functionname': [
                      (
                       '[a-zA-Z_][a-zA-Z0-9_]*', Name.Function, '#pop')], 
       'string': [
                (
                 '"', String.Double, '#pop'),
                (
                 '[^{$"\\\\]+', String.Double),
                (
                 '\\\\([nrt\\"$\\\\]|[0-7]{1,3}|x[0-9A-Fa-f]{1,2})', String.Escape),
                (
                 '\\$[a-zA-Z_][a-zA-Z0-9_]*(\\[\\S+\\]|->[a-zA-Z_][a-zA-Z0-9_]*)?',
                 String.Interpol),
                (
                 '(\\{\\$\\{)(.*?)(\\}\\})',
                 bygroups(String.Interpol, using(this, _startinline=True), String.Interpol)),
                (
                 '(\\{)(\\$.*?)(\\})',
                 bygroups(String.Interpol, using(this, _startinline=True), String.Interpol)),
                (
                 '(\\$\\{)(\\S+)(\\})',
                 bygroups(String.Interpol, Name.Variable, String.Interpol)),
                (
                 '[${\\\\]+', String.Double)]}

    def __init__(self, **options):
        self.funcnamehighlighting = get_bool_opt(options, 'funcnamehighlighting', True)
        self.disabledmodules = get_list_opt(options, 'disabledmodules', ['unknown'])
        self.startinline = get_bool_opt(options, 'startinline', False)
        if '_startinline' in options:
            self.startinline = options.pop('_startinline')
        self._functions = set()
        if self.funcnamehighlighting:
            from pygments.lexers._phpbuiltins import MODULES
            for (key, value) in MODULES.iteritems():
                if key not in self.disabledmodules:
                    self._functions.update(value)

        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        stack = [
         'root']
        if self.startinline:
            stack.append('php')
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Other:
                if value in self._functions:
                    yield (
                     index, Name.Builtin, value)
                    continue
            yield (
             index, token, value)

    def analyse_text(text):
        rv = 0.0
        if re.search('<\\?(?!xml)', text):
            rv += 0.3
        if '?>' in text:
            rv += 0.1
        return rv


class XmlLexer(RegexLexer):
    """
    Generic lexer for XML (eXtensible Markup Language).
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'XML'
    aliases = ['xml']
    filenames = ['*.xml', '*.xsl', '*.rss', '*.xslt', '*.xsd', '*.wsdl']
    mimetypes = ['text/xml', 'application/xml', 'image/svg+xml',
     'application/rss+xml', 'application/atom+xml',
     'application/xsl+xml', 'application/xslt+xml']
    tokens = {'root': [
              (
               '[^<&]+', Text),
              (
               '&\\S*?;', Name.Entity),
              (
               '\\<\\!\\[CDATA\\[.*?\\]\\]\\>', Comment.Preproc),
              (
               '<!--', Comment, 'comment'),
              (
               '<\\?.*?\\?>', Comment.Preproc),
              (
               '<![^>]*>', Comment.Preproc),
              (
               '<\\s*[a-zA-Z0-9:._-]+', Name.Tag, 'tag'),
              (
               '<\\s*/\\s*[a-zA-Z0-9:._-]+\\s*>', Name.Tag)], 
       'comment': [
                 (
                  '[^-]+', Comment),
                 (
                  '-->', Comment, '#pop'),
                 (
                  '-', Comment)], 
       'tag': [
             (
              '\\s+', Text),
             (
              '[a-zA-Z0-9_.:-]+\\s*=', Name.Attribute, 'attr'),
             (
              '/?\\s*>', Name.Tag, '#pop')], 
       'attr': [
              (
               '\\s+', Text),
              (
               '".*?"', String, '#pop'),
              (
               "'.*?'", String, '#pop'),
              (
               '[^\\s>]+', String, '#pop')]}

    def analyse_text(text):
        if looks_like_xml(text):
            return 0.5


class XsltLexer(XmlLexer):
    """
    A lexer for XSLT.

    *New in Pygments 0.10.*
    """
    name = 'XSLT'
    aliases = ['xslt']
    filenames = ['*.xsl', '*.xslt']
    EXTRA_KEYWORDS = set([
     'apply-imports', 'apply-templates', 'attribute',
     'attribute-set', 'call-template', 'choose', 'comment',
     'copy', 'copy-of', 'decimal-format', 'element', 'fallback',
     'for-each', 'if', 'import', 'include', 'key', 'message',
     'namespace-alias', 'number', 'otherwise', 'output', 'param',
     'preserve-space', 'processing-instruction', 'sort',
     'strip-space', 'stylesheet', 'template', 'text', 'transform',
     'value-of', 'variable', 'when', 'with-param'])

    def get_tokens_unprocessed(self, text):
        for (index, token, value) in XmlLexer.get_tokens_unprocessed(self, text):
            m = re.match('</?xsl:([^>]*)/?>?', value)
            if token is Name.Tag and m and m.group(1) in self.EXTRA_KEYWORDS:
                yield (
                 index, Keyword, value)
            else:
                yield (
                 index, token, value)

    def analyse_text(text):
        if looks_like_xml(text) and '<xsl' in text:
            return 0.8


class MxmlLexer(RegexLexer):
    """
    For MXML markup.
    Nested AS3 in <script> tags is highlighted by the appropriate lexer.
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'MXML'
    aliases = ['mxml']
    filenames = ['*.mxml']
    mimetimes = ['text/xml', 'application/xml']
    tokens = {'root': [
              (
               '[^<&]+', Text),
              (
               '&\\S*?;', Name.Entity),
              (
               '(\\<\\!\\[CDATA\\[)(.*?)(\\]\\]\\>)',
               bygroups(String, using(ActionScript3Lexer), String)),
              (
               '<!--', Comment, 'comment'),
              (
               '<\\?.*?\\?>', Comment.Preproc),
              (
               '<![^>]*>', Comment.Preproc),
              (
               '<\\s*[a-zA-Z0-9:._-]+', Name.Tag, 'tag'),
              (
               '<\\s*/\\s*[a-zA-Z0-9:._-]+\\s*>', Name.Tag)], 
       'comment': [
                 (
                  '[^-]+', Comment),
                 (
                  '-->', Comment, '#pop'),
                 (
                  '-', Comment)], 
       'tag': [
             (
              '\\s+', Text),
             (
              '[a-zA-Z0-9_.:-]+\\s*=', Name.Attribute, 'attr'),
             (
              '/?\\s*>', Name.Tag, '#pop')], 
       'attr': [
              (
               '\\s+', Text),
              (
               '".*?"', String, '#pop'),
              (
               "'.*?'", String, '#pop'),
              (
               '[^\\s>]+', String, '#pop')]}


class HaxeLexer(RegexLexer):
    """
    For haXe source code (http://haxe.org/).
    """
    name = 'haXe'
    aliases = ['hx', 'haXe']
    filenames = ['*.hx']
    mimetypes = ['text/haxe']
    ident = '(?:[a-zA-Z_][a-zA-Z0-9_]*)'
    typeid = '(?:(?:[a-z0-9_\\.])*[A-Z_][A-Za-z0-9_]*)'
    key_prop = '(?:default|null|never)'
    key_decl_mod = '(?:public|private|override|static|inline|extern|dynamic)'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root': [
              include('whitespace'),
              include('comments'),
              (
               key_decl_mod, Keyword.Declaration),
              include('enumdef'),
              include('typedef'),
              include('classdef'),
              include('imports')], 
       'comments': [
                  (
                   '//.*?\\n', Comment.Single),
                  (
                   '/\\*.*?\\*/', Comment.Multiline),
                  (
                   '#[^\\n]*', Comment.Preproc)], 
       'whitespace': [
                    include('comments'),
                    (
                     '\\s+', Text)], 
       'codekeywords': [
                      (
                       '\\b(if|else|while|do|for|in|break|continue|return|switch|case|try|catch|throw|null|trace|new|this|super|untyped|cast|callback|here)\\b',
                       Keyword.Reserved)], 
       'literals': [
                  (
                   '0[xX][0-9a-fA-F]+', Number.Hex),
                  (
                   '[0-9]+', Number.Integer),
                  (
                   '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
                  (
                   "'(\\\\\\\\|\\\\'|[^'])*'", String.Single),
                  (
                   '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
                  (
                   '~/([^\\n])*?/[gisx]*', String.Regex),
                  (
                   '\\b(true|false|null)\\b', Keyword.Constant)], 
       'codeblock': [
                   include('whitespace'),
                   include('new'),
                   include('case'),
                   include('anonfundef'),
                   include('literals'),
                   include('vardef'),
                   include('codekeywords'),
                   (
                    '[();,\\[\\]]', Punctuation),
                   (
                    '(?:=|\\+=|-=|\\*=|/=|%=|&=|\\|=|\\^=|<<=|>>=|>>>=|\\|\\||&&|\\.\\.\\.|==|!=|>|<|>=|<=|\\||&|\\^|<<|>>|>>>|\\+|\\-|\\*|/|%|!|\\+\\+|\\-\\-|~|\\.|\\?|\\:)',
                    Operator),
                   (
                    ident, Name),
                   (
                    '}', Punctuation, '#pop'),
                   (
                    '{', Punctuation, '#push')], 
       'propertydef': [
                     (
                      '(\\()(' + key_prop + ')(,)(' + key_prop + ')(\\))',
                      bygroups(Punctuation, Keyword.Reserved, Punctuation, Keyword.Reserved, Punctuation))], 
       'new': [
             (
              '\\bnew\\b', Keyword, 'typedecl')], 
       'case': [
              (
               '\\b(case)(\\s+)(' + ident + ')(\\s*)(\\()',
               bygroups(Keyword.Reserved, Text, Name, Text, Punctuation),
               'funargdecl')], 
       'vardef': [
                (
                 '\\b(var)(\\s+)(' + ident + ')',
                 bygroups(Keyword.Declaration, Text, Name.Variable), 'vardecl')], 
       'vardecl': [
                 include('whitespace'),
                 include('typelabel'),
                 (
                  '=', Operator, '#pop'),
                 (
                  ';', Punctuation, '#pop')], 
       'instancevardef': [
                        (
                         key_decl_mod, Keyword.Declaration),
                        (
                         '\\b(var)(\\s+)(' + ident + ')',
                         bygroups(Keyword.Declaration, Text, Name.Variable.Instance),
                         'instancevardecl')], 
       'instancevardecl': [
                         include('vardecl'),
                         include('propertydef')], 
       'anonfundef': [
                    (
                     '\\bfunction\\b', Keyword.Declaration, 'fundecl')], 
       'instancefundef': [
                        (
                         key_decl_mod, Keyword.Declaration),
                        (
                         '\\b(function)(\\s+)(' + ident + ')',
                         bygroups(Keyword.Declaration, Text, Name.Function), 'fundecl')], 
       'fundecl': [
                 include('whitespace'),
                 include('typelabel'),
                 include('generictypedecl'),
                 (
                  '\\(', Punctuation, 'funargdecl'),
                 (
                  '(?=[a-zA-Z0-9_])', Text, '#pop'),
                 (
                  '{', Punctuation, ('#pop', 'codeblock')),
                 (
                  ';', Punctuation, '#pop')], 
       'funargdecl': [
                    include('whitespace'),
                    (
                     ident, Name.Variable),
                    include('typelabel'),
                    include('literals'),
                    (
                     '=', Operator),
                    (
                     ',', Punctuation),
                    (
                     '\\?', Punctuation),
                    (
                     '\\)', Punctuation, '#pop')], 
       'typelabel': [
                   (
                    ':', Punctuation, 'type')], 
       'typedecl': [
                  include('whitespace'),
                  (
                   typeid, Name.Class),
                  (
                   '<', Punctuation, 'generictypedecl'),
                  (
                   '(?=[{}()=,a-z])', Text, '#pop')], 
       'type': [
              include('whitespace'),
              (
               typeid, Name.Class),
              (
               '<', Punctuation, 'generictypedecl'),
              (
               '->', Keyword.Type),
              (
               '(?=[{}(),;=])', Text, '#pop')], 
       'generictypedecl': [
                         include('whitespace'),
                         (
                          typeid, Name.Class),
                         (
                          '<', Punctuation, '#push'),
                         (
                          '>', Punctuation, '#pop'),
                         (
                          ',', Punctuation)], 
       'imports': [
                 (
                  '(package|import|using)(\\s+)([^;]+)(;)',
                  bygroups(Keyword.Namespace, Text, Name.Namespace, Punctuation))], 
       'typedef': [
                 (
                  'typedef', Keyword.Declaration, ('typedefprebody', 'typedecl'))], 
       'typedefprebody': [
                        include('whitespace'),
                        (
                         '(=)(\\s*)({)', bygroups(Punctuation, Text, Punctuation),
                         ('#pop', 'typedefbody'))], 
       'enumdef': [
                 (
                  'enum', Keyword.Declaration, ('enumdefprebody', 'typedecl'))], 
       'enumdefprebody': [
                        include('whitespace'),
                        (
                         '{', Punctuation, ('#pop', 'enumdefbody'))], 
       'classdef': [
                  (
                   'class', Keyword.Declaration, ('classdefprebody', 'typedecl'))], 
       'classdefprebody': [
                         include('whitespace'),
                         (
                          '(extends|implements)', Keyword.Declaration, 'typedecl'),
                         (
                          '{', Punctuation, ('#pop', 'classdefbody'))], 
       'interfacedef': [
                      (
                       'interface', Keyword.Declaration,
                       ('interfacedefprebody', 'typedecl'))], 
       'interfacedefprebody': [
                             include('whitespace'),
                             (
                              '(extends)', Keyword.Declaration, 'typedecl'),
                             (
                              '{', Punctuation, ('#pop', 'classdefbody'))], 
       'typedefbody': [
                     include('whitespace'),
                     include('instancevardef'),
                     include('instancefundef'),
                     (
                      '>', Punctuation, 'typedecl'),
                     (
                      ',', Punctuation),
                     (
                      '}', Punctuation, '#pop')], 
       'enumdefbody': [
                     include('whitespace'),
                     (
                      ident, Name.Variable.Instance),
                     (
                      '\\(', Punctuation, 'funargdecl'),
                     (
                      ';', Punctuation),
                     (
                      '}', Punctuation, '#pop')], 
       'classdefbody': [
                      include('whitespace'),
                      include('instancevardef'),
                      include('instancefundef'),
                      (
                       '}', Punctuation, '#pop'),
                      include('codeblock')]}

    def analyse_text(text):
        if re.match('\\w+\\s*:\\s*\\w', text):
            return 0.3


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
    return


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


class HamlLexer(ExtendedRegexLexer):
    """
    For Haml markup.

    *New in Pygments 1.3.*
    """
    name = 'Haml'
    aliases = ['haml', 'HAML']
    filenames = ['*.haml']
    mimetypes = ['text/x-haml']
    flags = re.IGNORECASE
    _dot = '(?: \\|\\n(?=.* \\|)|.)'
    _comma_dot = '(?:,\\s*\\n|' + _dot + ')'
    tokens = {'root': [
              (
               '[ \\t]*\\n', Text),
              (
               '[ \\t]*', _indentation)], 
       'css': [
             (
              '\\.[a-z0-9_:-]+', Name.Class, 'tag'),
             (
              '\\#[a-z0-9_:-]+', Name.Function, 'tag')], 
       'eval-or-plain': [
                       (
                        '[&!]?==', Punctuation, 'plain'),
                       (
                        '([&!]?[=~])(' + _comma_dot + '*\n)',
                        bygroups(Punctuation, using(RubyLexer)),
                        'root'),
                       (
                        '', Text, 'plain')], 
       'content': [
                 include('css'),
                 (
                  '%[a-z0-9_:-]+', Name.Tag, 'tag'),
                 (
                  '!!!' + _dot + '*\n', Name.Namespace, '#pop'),
                 (
                  '(/)(\\[' + _dot + '*?\\])(' + _dot + '*\n)',
                  bygroups(Comment, Comment.Special, Comment),
                  '#pop'),
                 (
                  '/' + _dot + '*\n', _starts_block(Comment, 'html-comment-block'),
                  '#pop'),
                 (
                  '-#' + _dot + '*\n',
                  _starts_block(Comment.Preproc, 'haml-comment-block'), '#pop'),
                 (
                  '(-)(' + _comma_dot + '*\n)',
                  bygroups(Punctuation, using(RubyLexer)),
                  '#pop'),
                 (
                  ':' + _dot + '*\n', _starts_block(Name.Decorator, 'filter-block'),
                  '#pop'),
                 include('eval-or-plain')], 
       'tag': [
             include('css'),
             (
              '\\{(,\\n|' + _dot + ')*?\\}', using(RubyLexer)),
             (
              '\\[' + _dot + '*?\\]', using(RubyLexer)),
             (
              '\\(', Text, 'html-attributes'),
             (
              '/[ \\t]*\\n', Punctuation, '#pop:2'),
             (
              '[<>]{1,2}(?=[ \\t=])', Punctuation),
             include('eval-or-plain')], 
       'plain': [
               (
                '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text),
               (
                '(#\\{)(' + _dot + '*?)(\\})',
                bygroups(String.Interpol, using(RubyLexer), String.Interpol)),
               (
                '\\n', Text, 'root')], 
       'html-attributes': [
                         (
                          '\\s+', Text),
                         (
                          '[a-z0-9_:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'),
                         (
                          '[a-z0-9_:-]+', Name.Attribute),
                         (
                          '\\)', Text, '#pop')], 
       'html-attribute-value': [
                              (
                               '[ \\t]+', Text),
                              (
                               '[a-z0-9_]+', Name.Variable, '#pop'),
                              (
                               '@[a-z0-9_]+', Name.Variable.Instance, '#pop'),
                              (
                               '\\$[a-z0-9_]+', Name.Variable.Global, '#pop'),
                              (
                               "'(\\\\\\\\|\\\\'|[^'\\n])*'", String, '#pop'),
                              (
                               '"(\\\\\\\\|\\\\"|[^"\\n])*"', String, '#pop')], 
       'html-comment-block': [
                            (
                             _dot + '+', Comment),
                            (
                             '\\n', Text, 'root')], 
       'haml-comment-block': [
                            (
                             _dot + '+', Comment.Preproc),
                            (
                             '\\n', Text, 'root')], 
       'filter-block': [
                      (
                       '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator),
                      (
                       '(#\\{)(' + _dot + '*?)(\\})',
                       bygroups(String.Interpol, using(RubyLexer), String.Interpol)),
                      (
                       '\\n', Text, 'root')]}


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
            '(azimuth|background-attachment|background-color|background-image|background-position|background-repeat|background|border-bottom-color|border-bottom-style|border-bottom-width|border-left-color|border-left-style|border-left-width|border-right|border-right-color|border-right-style|border-right-width|border-top-color|border-top-style|border-top-width|border-bottom|border-collapse|border-left|border-width|border-color|border-spacing|border-style|border-top|border|caption-side|clear|clip|color|content|counter-increment|counter-reset|cue-after|cue-before|cue|cursor|direction|display|elevation|empty-cells|float|font-family|font-size|font-size-adjust|font-stretch|font-style|font-variant|font-weight|font|height|letter-spacing|line-height|list-style-type|list-style-image|list-style-position|list-style|margin-bottom|margin-left|margin-right|margin-top|margin|marker-offset|marks|max-height|max-width|min-height|min-width|opacity|orphans|outline|outline-color|outline-style|outline-width|overflow|padding-bottom|padding-left|padding-right|padding-top|padding|page|page-break-after|page-break-before|page-break-inside|pause-after|pause-before|pause|pitch|pitch-range|play-during|position|quotes|richness|right|size|speak-header|speak-numeral|speak-punctuation|speak|speech-rate|stress|table-layout|text-align|text-decoration|text-indent|text-shadow|text-transform|top|unicode-bidi|vertical-align|visibility|voice-family|volume|white-space|widows|width|word-spacing|z-index|bottom|left|above|absolute|always|armenian|aural|auto|avoid|baseline|behind|below|bidi-override|blink|block|bold|bolder|both|capitalize|center-left|center-right|center|circle|cjk-ideographic|close-quote|collapse|condensed|continuous|crop|crosshair|cross|cursive|dashed|decimal-leading-zero|decimal|default|digits|disc|dotted|double|e-resize|embed|extra-condensed|extra-expanded|expanded|fantasy|far-left|far-right|faster|fast|fixed|georgian|groove|hebrew|help|hidden|hide|higher|high|hiragana-iroha|hiragana|icon|inherit|inline-table|inline|inset|inside|invert|italic|justify|katakana-iroha|katakana|landscape|larger|large|left-side|leftwards|level|lighter|line-through|list-item|loud|lower-alpha|lower-greek|lower-roman|lowercase|ltr|lower|low|medium|message-box|middle|mix|monospace|n-resize|narrower|ne-resize|no-close-quote|no-open-quote|no-repeat|none|normal|nowrap|nw-resize|oblique|once|open-quote|outset|outside|overline|pointer|portrait|px|relative|repeat-x|repeat-y|repeat|rgb|ridge|right-side|rightwards|s-resize|sans-serif|scroll|se-resize|semi-condensed|semi-expanded|separate|serif|show|silent|slow|slower|small-caps|small-caption|smaller|soft|solid|spell-out|square|static|status-bar|super|sw-resize|table-caption|table-cell|table-column|table-column-group|table-footer-group|table-header-group|table-row|table-row-group|text|text-bottom|text-top|thick|thin|transparent|ultra-condensed|ultra-expanded|underline|upper-alpha|upper-latin|upper-roman|uppercase|url|visible|w-resize|wait|wider|x-fast|x-high|x-large|x-loud|x-low|x-small|x-soft|xx-large|xx-small|yes)\\b',
            Name.Constant),
           (
            '(indigo|gold|firebrick|indianred|darkolivegreen|darkseagreen|mediumvioletred|mediumorchid|chartreuse|mediumslateblue|springgreen|crimson|lightsalmon|brown|turquoise|olivedrab|cyan|skyblue|darkturquoise|goldenrod|darkgreen|darkviolet|darkgray|lightpink|darkmagenta|lightgoldenrodyellow|lavender|yellowgreen|thistle|violet|orchid|ghostwhite|honeydew|cornflowerblue|darkblue|darkkhaki|mediumpurple|cornsilk|bisque|slategray|darkcyan|khaki|wheat|deepskyblue|darkred|steelblue|aliceblue|gainsboro|mediumturquoise|floralwhite|coral|lightgrey|lightcyan|darksalmon|beige|azure|lightsteelblue|oldlace|greenyellow|royalblue|lightseagreen|mistyrose|sienna|lightcoral|orangered|navajowhite|palegreen|burlywood|seashell|mediumspringgreen|papayawhip|blanchedalmond|peru|aquamarine|darkslategray|ivory|dodgerblue|lemonchiffon|chocolate|orange|forestgreen|slateblue|mintcream|antiquewhite|darkorange|cadetblue|moccasin|limegreen|saddlebrown|darkslateblue|lightskyblue|deeppink|plum|darkgoldenrod|sandybrown|magenta|tan|rosybrown|pink|lightblue|palevioletred|mediumseagreen|dimgray|powderblue|seagreen|snow|mediumblue|midnightblue|paleturquoise|palegoldenrod|whitesmoke|darkorchid|salmon|lightslategray|lawngreen|lightgreen|tomato|hotpink|lightyellow|lavenderblush|linen|mediumaquamarine|blueviolet|peachpuff)\\b',
            Name.Entity),
           (
            '(black|silver|gray|white|maroon|red|purple|fuchsia|green|lime|olive|yellow|navy|blue|teal|aqua)\\b',
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
            '#{', String.Interpol, 'interpolation'),
           (
            '[~\\^\\*!&%<>\\|+=@:,./?-]+', Operator),
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
               '[a-zA-Z0-9_-]+', Name.Tag),
              (
               '#\\{', String.Interpol, 'interpolation'),
              (
               '&', Keyword),
              (
               '[~\\^\\*!&\\[\\]\\(\\)<>\\|+=@:;,./?-]', Operator),
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
                  (
                   '', Text, '#pop')], 
   'class': [
           (
            '[\\w-]+', Name.Class),
           (
            '#\\{', String.Interpol, 'interpolation'),
           (
            '', Text, '#pop')], 
   'id': [
        (
         '[\\w-]+', Name.Namespace),
        (
         '#\\{', String.Interpol, 'interpolation'),
        (
         '', Text, '#pop')], 
   'for': [
         (
          '(from|to|through)', Operator.Word),
         include('value')]}

class SassLexer(ExtendedRegexLexer):
    """
    For Sass stylesheets.

    *New in Pygments 1.3.*
    """
    name = 'Sass'
    aliases = ['sass', 'SASS']
    filenames = ['*.sass']
    mimetypes = ['text/x-sass']
    flags = re.IGNORECASE
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
                  '@[a-z0-9_-]+', Keyword, 'selector'),
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
                 (
                  '', Text, 'selector')], 
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
                 '[^\\s]+', String),
                (
                 '\\n', Text, 'root')], 
       'old-style-attr': [
                        (
                         '[^\\s:="\\[]+', Name.Attribute),
                        (
                         '#{', String.Interpol, 'interpolation'),
                        (
                         '[ \\t]*=', Operator, 'value'),
                        (
                         '', Text, 'value')], 
       'new-style-attr': [
                        (
                         '[^\\s:="\\[]+', Name.Attribute),
                        (
                         '#{', String.Interpol, 'interpolation'),
                        (
                         '[ \\t]*[=:]', Operator, 'value')], 
       'inline-comment': [
                        (
                         '(\\\\#|#(?=[^\\n{])|\\*(?=[^\\n/])|[^\\n#*])+', Comment.Multiline),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '\\*/', Comment, '#pop')]}
    for (group, common) in common_sass_tokens.iteritems():
        tokens[group] = copy.copy(common)

    tokens['value'].append(('\\n', Text, 'root'))
    tokens['selector'].append(('\\n', Text, 'root'))


class ScssLexer(RegexLexer):
    """
    For SCSS stylesheets.
    """
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
               '@[a-z0-9_-]+', Keyword, 'selector'),
              (
               '(\\$[\\w-]\\w*)([ \\t]*:)', bygroups(Name.Variable, Operator), 'value'),
              (
               '(?=[^;{}][;}])', Name.Attribute, 'attr'),
              (
               '(?=[^;{}:]+:[^a-z])', Name.Attribute, 'attr'),
              (
               '', Text, 'selector')], 
       'attr': [
              (
               '[^\\s:="\\[]+', Name.Attribute),
              (
               '#{', String.Interpol, 'interpolation'),
              (
               '[ \\t]*:', Operator, 'value')], 
       'inline-comment': [
                        (
                         '(\\\\#|#(?=[^{])|\\*(?=[^/])|[^#*])+', Comment.Multiline),
                        (
                         '#\\{', String.Interpol, 'interpolation'),
                        (
                         '\\*/', Comment, '#pop')]}
    for (group, common) in common_sass_tokens.iteritems():
        tokens[group] = copy.copy(common)

    tokens['value'].extend([('\\n', Text), ('[;{}]', Punctuation, 'root')])
    tokens['selector'].extend([('\\n', Text), ('[;{}]', Punctuation, 'root')])


class CoffeeScriptLexer(RegexLexer):
    """
    For `CoffeeScript`_ source code.

    .. _CoffeeScript: http://coffeescript.org

    *New in Pygments 1.3.*
    """
    name = 'CoffeeScript'
    aliases = ['coffee-script', 'coffeescript']
    filenames = ['*.coffee']
    mimetypes = ['text/coffeescript']
    flags = re.DOTALL
    tokens = {'commentsandwhitespace': [
                               (
                                '\\s+', Text),
                               (
                                '#.*?\\n', Comment.Single)], 
       'slashstartsregex': [
                          include('commentsandwhitespace'),
                          (
                           '/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)',
                           String.Regex, '#pop'),
                          (
                           '(?=/)', Text, ('#pop', 'badregex')),
                          (
                           '', Text, '#pop')], 
       'badregex': [
                  (
                   '\n', Text, '#pop')], 
       'root': [
              (
               '^(?=\\s|/|<!--)', Text, 'slashstartsregex'),
              include('commentsandwhitespace'),
              (
               '\\+\\+|--|~|&&|\\band\\b|\\bor\\b|\\bis\\b|\\bisnt\\b|\\bnot\\b|\\?|:|=|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*`%&\\|\\^/])=?',
               Operator, 'slashstartsregex'),
              (
               '\\([^()]*\\)\\s*->', Name.Function),
              (
               '[{(\\[;,]', Punctuation, 'slashstartsregex'),
              (
               '[})\\].]', Punctuation),
              (
               '(for|in|of|while|break|return|continue|switch|when|then|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|super|extends|this|class|by)\\b',
               Keyword, 'slashstartsregex'),
              (
               '(true|false|yes|no|on|off|null|NaN|Infinity|undefined)\\b',
               Keyword.Constant),
              (
               '(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|eval|isFinite|isNaN|parseFloat|parseInt|document|window)\\b',
               Name.Builtin),
              (
               '[$a-zA-Z_][a-zA-Z0-9_\\.:]*\\s*[:=]\\s', Name.Variable,
               'slashstartsregex'),
              (
               '@[$a-zA-Z_][a-zA-Z0-9_\\.:]*\\s*[:=]\\s', Name.Variable.Instance,
               'slashstartsregex'),
              (
               '@?[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other, 'slashstartsregex'),
              (
               '[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
              (
               '0x[0-9a-fA-F]+', Number.Hex),
              (
               '[0-9]+', Number.Integer),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String.Double),
              (
               "'(\\\\\\\\|\\\\'|[^'])*'", String.Single)]}


class DuelLexer(RegexLexer):
    """
    Lexer for Duel Views Engine (formerly JBST) markup with JavaScript code blocks.
    See http://duelengine.org/.
    See http://jsonml.org/jbst/.

    *New in Pygments 1.4.*
    """
    name = 'Duel'
    aliases = ['duel', 'Duel Engine', 'Duel View', 'JBST', 'jbst', 'JsonML+BST']
    filenames = ['*.duel', '*.jbst']
    mimetypes = ['text/x-duel', 'text/x-jbst']
    flags = re.DOTALL
    tokens = {'root': [
              (
               '(<%[@=#!:]?)(.*?)(%>)',
               bygroups(Name.Tag, using(JavascriptLexer), Name.Tag)),
              (
               '(<%\\$)(.*?)(:)(.*?)(%>)',
               bygroups(Name.Tag, Name.Function, Punctuation, String, Name.Tag)),
              (
               '(<%--)(.*?)(--%>)',
               bygroups(Name.Tag, Comment.Multiline, Name.Tag)),
              (
               '(<script.*?>)(.*?)(</script>)',
               bygroups(using(HtmlLexer), using(JavascriptLexer), using(HtmlLexer))),
              (
               '(.+?)(?=<)', using(HtmlLexer)),
              (
               '.+', using(HtmlLexer))]}


class ScamlLexer(ExtendedRegexLexer):
    """
    For `Scaml markup <http://scalate.fusesource.org/>`_.  Scaml is Haml for Scala.

    *New in Pygments 1.4.*
    """
    name = 'Scaml'
    aliases = ['scaml', 'SCAML']
    filenames = ['*.scaml']
    mimetypes = ['text/x-scaml']
    flags = re.IGNORECASE
    _dot = '.'
    tokens = {'root': [
              (
               '[ \\t]*\\n', Text),
              (
               '[ \\t]*', _indentation)], 
       'css': [
             (
              '\\.[a-z0-9_:-]+', Name.Class, 'tag'),
             (
              '\\#[a-z0-9_:-]+', Name.Function, 'tag')], 
       'eval-or-plain': [
                       (
                        '[&!]?==', Punctuation, 'plain'),
                       (
                        '([&!]?[=~])(' + _dot + '*\n)',
                        bygroups(Punctuation, using(ScalaLexer)),
                        'root'),
                       (
                        '', Text, 'plain')], 
       'content': [
                 include('css'),
                 (
                  '%[a-z0-9_:-]+', Name.Tag, 'tag'),
                 (
                  '!!!' + _dot + '*\n', Name.Namespace, '#pop'),
                 (
                  '(/)(\\[' + _dot + '*?\\])(' + _dot + '*\n)',
                  bygroups(Comment, Comment.Special, Comment),
                  '#pop'),
                 (
                  '/' + _dot + '*\n', _starts_block(Comment, 'html-comment-block'),
                  '#pop'),
                 (
                  '-#' + _dot + '*\n',
                  _starts_block(Comment.Preproc, 'scaml-comment-block'), '#pop'),
                 (
                  '(-@\\s*)(import)?(' + _dot + '*\n)',
                  bygroups(Punctuation, Keyword, using(ScalaLexer)),
                  '#pop'),
                 (
                  '(-)(' + _dot + '*\n)',
                  bygroups(Punctuation, using(ScalaLexer)),
                  '#pop'),
                 (
                  ':' + _dot + '*\n', _starts_block(Name.Decorator, 'filter-block'),
                  '#pop'),
                 include('eval-or-plain')], 
       'tag': [
             include('css'),
             (
              '\\{(,\\n|' + _dot + ')*?\\}', using(ScalaLexer)),
             (
              '\\[' + _dot + '*?\\]', using(ScalaLexer)),
             (
              '\\(', Text, 'html-attributes'),
             (
              '/[ \\t]*\\n', Punctuation, '#pop:2'),
             (
              '[<>]{1,2}(?=[ \\t=])', Punctuation),
             include('eval-or-plain')], 
       'plain': [
               (
                '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text),
               (
                '(#\\{)(' + _dot + '*?)(\\})',
                bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
               (
                '\\n', Text, 'root')], 
       'html-attributes': [
                         (
                          '\\s+', Text),
                         (
                          '[a-z0-9_:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'),
                         (
                          '[a-z0-9_:-]+', Name.Attribute),
                         (
                          '\\)', Text, '#pop')], 
       'html-attribute-value': [
                              (
                               '[ \\t]+', Text),
                              (
                               '[a-z0-9_]+', Name.Variable, '#pop'),
                              (
                               '@[a-z0-9_]+', Name.Variable.Instance, '#pop'),
                              (
                               '\\$[a-z0-9_]+', Name.Variable.Global, '#pop'),
                              (
                               "'(\\\\\\\\|\\\\'|[^'\\n])*'", String, '#pop'),
                              (
                               '"(\\\\\\\\|\\\\"|[^"\\n])*"', String, '#pop')], 
       'html-comment-block': [
                            (
                             _dot + '+', Comment),
                            (
                             '\\n', Text, 'root')], 
       'scaml-comment-block': [
                             (
                              _dot + '+', Comment.Preproc),
                             (
                              '\\n', Text, 'root')], 
       'filter-block': [
                      (
                       '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator),
                      (
                       '(#\\{)(' + _dot + '*?)(\\})',
                       bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
                      (
                       '\\n', Text, 'root')]}


class JadeLexer(ExtendedRegexLexer):
    """
    For Jade markup.
    Jade is a variant of Scaml, see:
    http://scalate.fusesource.org/documentation/scaml-reference.html

    *New in Pygments 1.4.*
    """
    name = 'Jade'
    aliases = ['jade', 'JADE']
    filenames = ['*.jade']
    mimetypes = ['text/x-jade']
    flags = re.IGNORECASE
    _dot = '.'
    tokens = {'root': [
              (
               '[ \\t]*\\n', Text),
              (
               '[ \\t]*', _indentation)], 
       'css': [
             (
              '\\.[a-z0-9_:-]+', Name.Class, 'tag'),
             (
              '\\#[a-z0-9_:-]+', Name.Function, 'tag')], 
       'eval-or-plain': [
                       (
                        '[&!]?==', Punctuation, 'plain'),
                       (
                        '([&!]?[=~])(' + _dot + '*\n)',
                        bygroups(Punctuation, using(ScalaLexer)), 'root'),
                       (
                        '', Text, 'plain')], 
       'content': [
                 include('css'),
                 (
                  '!!!' + _dot + '*\n', Name.Namespace, '#pop'),
                 (
                  '(/)(\\[' + _dot + '*?\\])(' + _dot + '*\n)',
                  bygroups(Comment, Comment.Special, Comment),
                  '#pop'),
                 (
                  '/' + _dot + '*\n', _starts_block(Comment, 'html-comment-block'),
                  '#pop'),
                 (
                  '-#' + _dot + '*\n',
                  _starts_block(Comment.Preproc, 'scaml-comment-block'), '#pop'),
                 (
                  '(-@\\s*)(import)?(' + _dot + '*\n)',
                  bygroups(Punctuation, Keyword, using(ScalaLexer)),
                  '#pop'),
                 (
                  '(-)(' + _dot + '*\n)',
                  bygroups(Punctuation, using(ScalaLexer)),
                  '#pop'),
                 (
                  ':' + _dot + '*\n', _starts_block(Name.Decorator, 'filter-block'),
                  '#pop'),
                 (
                  '[a-z0-9_:-]+', Name.Tag, 'tag'),
                 (
                  '|', Text, 'eval-or-plain')], 
       'tag': [
             include('css'),
             (
              '\\{(,\\n|' + _dot + ')*?\\}', using(ScalaLexer)),
             (
              '\\[' + _dot + '*?\\]', using(ScalaLexer)),
             (
              '\\(', Text, 'html-attributes'),
             (
              '/[ \\t]*\\n', Punctuation, '#pop:2'),
             (
              '[<>]{1,2}(?=[ \\t=])', Punctuation),
             include('eval-or-plain')], 
       'plain': [
               (
                '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text),
               (
                '(#\\{)(' + _dot + '*?)(\\})',
                bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
               (
                '\\n', Text, 'root')], 
       'html-attributes': [
                         (
                          '\\s+', Text),
                         (
                          '[a-z0-9_:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'),
                         (
                          '[a-z0-9_:-]+', Name.Attribute),
                         (
                          '\\)', Text, '#pop')], 
       'html-attribute-value': [
                              (
                               '[ \\t]+', Text),
                              (
                               '[a-z0-9_]+', Name.Variable, '#pop'),
                              (
                               '@[a-z0-9_]+', Name.Variable.Instance, '#pop'),
                              (
                               '\\$[a-z0-9_]+', Name.Variable.Global, '#pop'),
                              (
                               "'(\\\\\\\\|\\\\'|[^'\\n])*'", String, '#pop'),
                              (
                               '"(\\\\\\\\|\\\\"|[^"\\n])*"', String, '#pop')], 
       'html-comment-block': [
                            (
                             _dot + '+', Comment),
                            (
                             '\\n', Text, 'root')], 
       'scaml-comment-block': [
                             (
                              _dot + '+', Comment.Preproc),
                             (
                              '\\n', Text, 'root')], 
       'filter-block': [
                      (
                       '([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator),
                      (
                       '(#\\{)(' + _dot + '*?)(\\})',
                       bygroups(String.Interpol, using(ScalaLexer), String.Interpol)),
                      (
                       '\\n', Text, 'root')]}


class XQueryLexer(ExtendedRegexLexer):
    """
    An XQuery lexer, parsing a stream and outputting the tokens needed to
    highlight xquery code.

    *New in Pygments 1.4.*
    """
    name = 'XQuery'
    aliases = ['xquery', 'xqy']
    filenames = ['*.xqy', '*.xquery']
    mimetypes = ['text/xquery', 'application/xquery']
    xquery_parse_state = []
    ncnamestartchar = '[A-Z]|_|[a-z]'
    ncnamechar = ncnamestartchar + '|-|\\.|[0-9]'
    ncname = '((%s)+(%s)*)' % (ncnamestartchar, ncnamechar)
    pitarget_namestartchar = '[A-KN-WY-Z]|_|:|[a-kn-wy-z]'
    pitarget_namechar = pitarget_namestartchar + '|-|\\.|[0-9]'
    pitarget = '(%s)+(%s)*' % (pitarget_namestartchar, pitarget_namechar)
    prefixedname = '%s:%s' % (ncname, ncname)
    unprefixedname = ncname
    qname = '((%s)|(%s))' % (prefixedname, unprefixedname)
    entityref = '&(lt|gt|amp|quot|apos|nbsp);'
    charref = '&#[0-9]+;|&#x[0-9a-fA-F]+;'
    stringdouble = '("((' + entityref + ')|(' + charref + ')|("")|([^&"]))*")'
    stringsingle = "('((" + entityref + ')|(' + charref + ")|('')|([^&']))*')"
    elementcontentchar = '[A-Za-z]|\\s|\\d|[!"#$%\\(\\)\\*\\+,\\-\\./\\:;=\\?\\@\\[\\\\\\]^_\\\'`\\|~]'
    quotattrcontentchar = "[A-Za-z]|\\s|\\d|[!#$%\\(\\)\\*\\+,\\-\\./\\:;=\\?\\@\\[\\\\\\]^_\\'`\\|~]"
    aposattrcontentchar = '[A-Za-z]|\\s|\\d|[!"#$%\\(\\)\\*\\+,\\-\\./\\:;=\\?\\@\\[\\\\\\]^_`\\|~]'
    flags = re.DOTALL | re.MULTILINE | re.UNICODE

    def operator_root_callback(lexer, match, ctx):
        yield (
         match.start(), Operator, match.group(1))
        ctx.stack = [
         'root']
        ctx.pos = match.end()

    def popstate_tag_callback(lexer, match, ctx):
        yield (
         match.start(), Name.Tag, match.group(1))
        ctx.stack.append(lexer.xquery_parse_state.pop())
        ctx.pos = match.end()

    def popstate_xmlcomment_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append(lexer.xquery_parse_state.pop())
        ctx.pos = match.end()

    def popstate_kindtest_callback(lexer, match, ctx):
        yield (
         match.start(), Punctuation, match.group(1))
        next_state = lexer.xquery_parse_state.pop()
        if next_state == 'occurrenceindicator':
            if re.match('[?*+]+', match.group(2)):
                yield (
                 match.start(), Punctuation, match.group(2))
                ctx.stack.append('operator')
                ctx.pos = match.end()
            else:
                ctx.stack.append('operator')
                ctx.pos = match.end(1)
        else:
            ctx.stack.append(next_state)
            ctx.pos = match.end(1)

    def popstate_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        if len(lexer.xquery_parse_state) == 0:
            ctx.stack.pop()
        elif len(ctx.stack) > 1:
            ctx.stack.append(lexer.xquery_parse_state.pop())
        else:
            ctx.stack = [
             'root']
        ctx.pos = match.end()

    def pushstate_element_content_starttag_callback(lexer, match, ctx):
        yield (
         match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append('element_content')
        ctx.stack.append('start_tag')
        ctx.pos = match.end()

    def pushstate_cdata_section_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append(ctx.state.pop)
        ctx.pos = match.end()

    def pushstate_starttag_callback(lexer, match, ctx):
        yield (
         match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append(ctx.state.pop)
        ctx.stack.append('start_tag')
        ctx.pos = match.end()

    def pushstate_operator_order_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_operator_root_validate(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_operator_root_validate_withmode(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Keyword, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_operator_processing_instruction_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('processing_instruction')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_element_content_processing_instruction_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('processing_instruction')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()

    def pushstate_element_content_cdata_section_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()

    def pushstate_operator_cdata_section_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_element_content_xmlcomment_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('xml_comment')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()

    def pushstate_operator_xmlcomment_callback(lexer, match, ctx):
        yield (
         match.start(), String.Doc, match.group(1))
        ctx.stack.append('xml_comment')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    def pushstate_kindtest_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('kindtest')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()

    def pushstate_operator_kindtestforpi_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('kindtestforpi')
        ctx.pos = match.end()

    def pushstate_operator_kindtest_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()

    def pushstate_occurrenceindicator_kindtest_callback(lexer, match, ctx):
        yield (
         match.start(), Name.Tag, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('occurrenceindicator')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()

    def pushstate_operator_starttag_callback(lexer, match, ctx):
        yield (
         match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('start_tag')
        ctx.pos = match.end()

    def pushstate_operator_root_callback(lexer, match, ctx):
        yield (
         match.start(), Punctuation, match.group(1))
        lexer.xquery_parse_state.append('operator')
        ctx.stack = ['root']
        ctx.pos = match.end()

    def pushstate_operator_root_construct_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack = ['root']
        ctx.pos = match.end()

    def pushstate_root_callback(lexer, match, ctx):
        yield (
         match.start(), Punctuation, match.group(1))
        cur_state = ctx.stack.pop()
        lexer.xquery_parse_state.append(cur_state)
        ctx.stack = ['root']
        ctx.pos = match.end()

    def pushstate_operator_callback(lexer, match, ctx):
        yield (
         match.start(), Keyword, match.group(1))
        yield (match.start(), Text, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()

    tokens = {'comment': [
                 (
                  '(:\\))', Comment, '#pop'),
                 (
                  '(\\(:)', Comment, '#push'),
                 (
                  '[^:)]', Comment),
                 (
                  '([^:)]|:|\\))', Comment)], 
       'whitespace': [
                    (
                     '\\s+', Text)], 
       'operator': [
                  include('whitespace'),
                  (
                   '(\\})', popstate_callback),
                  (
                   '\\(:', Comment, 'comment'),
                  (
                   '(\\{)', pushstate_root_callback),
                  (
                   'then|else|external|at|div|except', Keyword, 'root'),
                  (
                   'is|mod|order\\s+by|stable\\s+order\\s+by', Keyword, 'root'),
                  (
                   'and|or', Operator.Word, 'root'),
                  (
                   '(eq|ge|gt|le|lt|ne|idiv|intersect|in)(?=\\b)',
                   Operator.Word, 'root'),
                  (
                   'return|satisfies|to|union|where|preserve\\s+strip',
                   Keyword, 'root'),
                  (
                   '(::|;|>=|>>|>|\\[|<=|<<|<|-|\\*|!=|\\+|//|/|\\||:=|,|=)',
                   operator_root_callback),
                  (
                   '(castable|cast)(\\s+)(as)',
                   bygroups(Keyword, Text, Keyword), 'singletype'),
                  (
                   '(instance)(\\s+)(of)|(treat)(\\s+)(as)',
                   bygroups(Keyword, Text, Keyword), 'itemtype'),
                  (
                   '(case)|(as)', Keyword, 'itemtype'),
                  (
                   '(\\))(\\s*)(as)',
                   bygroups(Punctuation, Text, Keyword), 'itemtype'),
                  (
                   '\\$', Name.Variable, 'varname'),
                  (
                   '(for|let)(\\s+)(\\$)',
                   bygroups(Keyword, Text, Name.Variable), 'varname'),
                  (
                   '\\)|\\?|\\]', Punctuation),
                  (
                   '(empty)(\\s+)(greatest|least)', bygroups(Keyword, Text, Keyword)),
                  (
                   'ascending|descending|default', Keyword, '#push'),
                  (
                   'external', Keyword),
                  (
                   'collation', Keyword, 'uritooperator'),
                  (
                   stringdouble, String.Double),
                  (
                   stringsingle, String.Single),
                  (
                   '(catch)(\\s*)', bygroups(Keyword, Text), 'root')], 
       'uritooperator': [
                       (
                        stringdouble, String.Double, '#pop'),
                       (
                        stringsingle, String.Single, '#pop')], 
       'namespacedecl': [
                       include('whitespace'),
                       (
                        '\\(:', Comment, 'comment'),
                       (
                        '(at)(\\s+)' + stringdouble, bygroups(Keyword, Text, String.Double)),
                       (
                        '(at)(\\s+)' + stringsingle, bygroups(Keyword, Text, String.Single)),
                       (
                        stringdouble, String.Double),
                       (
                        stringsingle, String.Single),
                       (
                        ',', Punctuation),
                       (
                        '=', Operator),
                       (
                        ';', Punctuation, 'root'),
                       (
                        ncname, Name.Namespace)], 
       'namespacekeyword': [
                          include('whitespace'),
                          (
                           '\\(:', Comment, 'comment'),
                          (
                           stringdouble, String.Double, 'namespacedecl'),
                          (
                           stringsingle, String.Single, 'namespacedecl'),
                          (
                           'inherit|no-inherit', Keyword, 'root'),
                          (
                           'namespace', Keyword, 'namespacedecl'),
                          (
                           '(default)(\\s+)(element)', bygroups(Keyword, Text, Keyword)),
                          (
                           'preserve|no-preserve', Keyword),
                          (
                           ',', Punctuation)], 
       'varname': [
                 (
                  '\\(:', Comment, 'comment'),
                 (
                  qname, Name.Variable, 'operator')], 
       'singletype': [
                    (
                     '\\(:', Comment, 'comment'),
                    (
                     ncname + '(:\\*)', Name.Variable, 'operator'),
                    (
                     qname, Name.Variable, 'operator')], 
       'itemtype': [
                  include('whitespace'),
                  (
                   '\\(:', Comment, 'comment'),
                  (
                   '\\$', Punctuation, 'varname'),
                  (
                   'void\\s*\\(\\s*\\)',
                   bygroups(Keyword, Text, Punctuation, Text, Punctuation), 'operator'),
                  (
                   '(element|attribute|schema-element|schema-attribute|comment|text|node|binary|document-node)(\\s*)(\\()',
                   pushstate_occurrenceindicator_kindtest_callback),
                  (
                   '(processing-instruction)(\\s*)(\\()',
                   bygroups(Keyword, Text, Punctuation),
                   ('occurrenceindicator', 'kindtestforpi')),
                  (
                   '(item)(\\s*)(\\()(\\s*)(\\))(?=[*+?])',
                   bygroups(Keyword, Text, Punctuation, Text, Punctuation),
                   'occurrenceindicator'),
                  (
                   '\\(\\#', Punctuation, 'pragma'),
                  (
                   ';', Punctuation, '#pop'),
                  (
                   'then|else', Keyword, '#pop'),
                  (
                   '(at)(\\s+)' + stringdouble,
                   bygroups(Keyword, Text, String.Double), 'namespacedecl'),
                  (
                   '(at)(\\s+)' + stringsingle,
                   bygroups(Keyword, Text, String.Single), 'namespacedecl'),
                  (
                   'except|intersect|in|is|return|satisfies|to|union|where',
                   Keyword, 'root'),
                  (
                   'and|div|eq|ge|gt|le|lt|ne|idiv|mod|or', Operator.Word, 'root'),
                  (
                   ':=|=|,|>=|>>|>|\\[|\\(|<=|<<|<|-|!=|\\|', Operator, 'root'),
                  (
                   'external|at', Keyword, 'root'),
                  (
                   '(stable)(\\s+)(order)(\\s+)(by)',
                   bygroups(Keyword, Text, Keyword, Text, Keyword), 'root'),
                  (
                   '(castable|cast)(\\s+)(as)',
                   bygroups(Keyword, Text, Keyword), 'singletype'),
                  (
                   '(instance)(\\s+)(of)|(treat)(\\s+)(as)',
                   bygroups(Keyword, Text, Keyword)),
                  (
                   'case|as', Keyword, 'itemtype'),
                  (
                   '(\\))(\\s*)(as)', bygroups(Operator, Text, Keyword), 'itemtype'),
                  (
                   ncname + '(:\\*)', Keyword.Type, 'operator'),
                  (
                   qname, Keyword.Type, 'occurrenceindicator')], 
       'kindtest': [
                  (
                   '\\(:', Comment, 'comment'),
                  (
                   '({)', Punctuation, 'root'),
                  (
                   '(\\))([*+?]?)', popstate_kindtest_callback),
                  (
                   '\\*', Name, 'closekindtest'),
                  (
                   qname, Name, 'closekindtest'),
                  (
                   '(element|schema-element)(\\s*)(\\()', pushstate_kindtest_callback)], 
       'kindtestforpi': [
                       (
                        '\\(:', Comment, 'comment'),
                       (
                        '\\)', Punctuation, '#pop'),
                       (
                        ncname, bygroups(Name.Variable, Name.Variable)),
                       (
                        stringdouble, String.Double),
                       (
                        stringsingle, String.Single)], 
       'closekindtest': [
                       (
                        '\\(:', Comment, 'comment'),
                       (
                        '(\\))', popstate_callback),
                       (
                        ',', Punctuation),
                       (
                        '(\\{)', pushstate_operator_root_callback),
                       (
                        '\\?', Punctuation)], 
       'xml_comment': [
                     (
                      '(-->)', popstate_xmlcomment_callback),
                     (
                      '[^-]{1,2}', Literal),
                     (
                      '\\u009|\\u00A|\\u00D|[\\u0020-\\u00D7FF]|[\\u00E000-\\u00FFFD]|[\\u0010000-\\u0010FFFF]',
                      Literal)], 
       'processing_instruction': [
                                (
                                 '\\s+', Text, 'processing_instruction_content'),
                                (
                                 '\\?>', String.Doc, '#pop'),
                                (
                                 pitarget, Name)], 
       'processing_instruction_content': [
                                        (
                                         '\\?>', String.Doc, '#pop'),
                                        (
                                         '\\u009|\\u00A|\\u00D|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\u10000-\\u10FFFF]',
                                         Literal)], 
       'cdata_section': [
                       (
                        ']]>', String.Doc, '#pop'),
                       (
                        '\\u009|\\u00A|\\u00D|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\u10000-\\u10FFFF]',
                        Literal)], 
       'start_tag': [
                   include('whitespace'),
                   (
                    '(/>)', popstate_tag_callback),
                   (
                    '>', Name.Tag, 'element_content'),
                   (
                    '"', Punctuation, 'quot_attribute_content'),
                   (
                    "'", Punctuation, 'apos_attribute_content'),
                   (
                    '=', Operator),
                   (
                    qname, Name.Tag)], 
       'quot_attribute_content': [
                                (
                                 '"', Punctuation, 'start_tag'),
                                (
                                 '(\\{)', pushstate_root_callback),
                                (
                                 '""', Name.Attribute),
                                (
                                 quotattrcontentchar, Name.Attribute),
                                (
                                 entityref, Name.Attribute),
                                (
                                 charref, Name.Attribute),
                                (
                                 '\\{\\{|\\}\\}', Name.Attribute)], 
       'apos_attribute_content': [
                                (
                                 "'", Punctuation, 'start_tag'),
                                (
                                 '\\{', Punctuation, 'root'),
                                (
                                 "''", Name.Attribute),
                                (
                                 aposattrcontentchar, Name.Attribute),
                                (
                                 entityref, Name.Attribute),
                                (
                                 charref, Name.Attribute),
                                (
                                 '\\{\\{|\\}\\}', Name.Attribute)], 
       'element_content': [
                         (
                          '</', Name.Tag, 'end_tag'),
                         (
                          '(\\{)', pushstate_root_callback),
                         (
                          '(<!--)', pushstate_element_content_xmlcomment_callback),
                         (
                          '(<\\?)', pushstate_element_content_processing_instruction_callback),
                         (
                          '(<!\\[CDATA\\[)', pushstate_element_content_cdata_section_callback),
                         (
                          '(<)', pushstate_element_content_starttag_callback),
                         (
                          elementcontentchar, Literal),
                         (
                          entityref, Literal),
                         (
                          charref, Literal),
                         (
                          '\\{\\{|\\}\\}', Literal)], 
       'end_tag': [
                 include('whitespace'),
                 (
                  '(>)', popstate_tag_callback),
                 (
                  qname, Name.Tag)], 
       'xmlspace_decl': [
                       (
                        '\\(:', Comment, 'comment'),
                       (
                        'preserve|strip', Keyword, '#pop')], 
       'declareordering': [
                         (
                          '\\(:', Comment, 'comment'),
                         include('whitespace'),
                         (
                          'ordered|unordered', Keyword, '#pop')], 
       'xqueryversion': [
                       include('whitespace'),
                       (
                        '\\(:', Comment, 'comment'),
                       (
                        stringdouble, String.Double),
                       (
                        stringsingle, String.Single),
                       (
                        'encoding', Keyword),
                       (
                        ';', Punctuation, '#pop')], 
       'pragma': [
                (
                 qname, Name.Variable, 'pragmacontents')], 
       'pragmacontents': [
                        (
                         '#\\)', Punctuation, 'operator'),
                        (
                         '\\u009|\\u00A|\\u00D|[\\u0020-\\u00D7FF]|[\\u00E000-\\u00FFFD]|[\\u0010000-\\u0010FFFF]',
                         Literal),
                        (
                         '(\\s*)', Text)], 
       'occurrenceindicator': [
                             include('whitespace'),
                             (
                              '\\(:', Comment, 'comment'),
                             (
                              '\\*|\\?|\\+', Operator, 'operator'),
                             (
                              ':=', Operator, 'root'),
                             (
                              '', Text, 'operator')], 
       'option': [
                include('whitespace'),
                (
                 qname, Name.Variable, '#pop')], 
       'qname_braren': [
                      include('whitespace'),
                      (
                       '(\\{)', pushstate_operator_root_callback),
                      (
                       '(\\()', Punctuation, 'root')], 
       'element_qname': [
                       (
                        qname, Name.Variable, 'root')], 
       'attribute_qname': [
                         (
                          qname, Name.Variable, 'root')], 
       'root': [
              include('whitespace'),
              (
               '\\(:', Comment, 'comment'),
              (
               '\\d+(\\.\\d*)?[eE][\\+\\-]?\\d+', Number.Double, 'operator'),
              (
               '(\\.\\d+)[eE][\\+\\-]?\\d+', Number.Double, 'operator'),
              (
               '(\\.\\d+|\\d+\\.\\d*)', Number, 'operator'),
              (
               '(\\d+)', Number.Integer, 'operator'),
              (
               '(\\.\\.|\\.|\\)|\\*)', Punctuation, 'operator'),
              (
               '(declare)(\\s+)(construction)',
               bygroups(Keyword, Text, Keyword), 'operator'),
              (
               '(declare)(\\s+)(default)(\\s+)(order)',
               bygroups(Keyword, Text, Keyword, Text, Keyword), 'operator'),
              (
               ncname + ':\\*', Name, 'operator'),
              (
               stringdouble, String.Double, 'operator'),
              (
               stringsingle, String.Single, 'operator'),
              (
               '(\\})', popstate_callback),
              (
               '(declare)(\\s+)(default)(\\s+)(collation)',
               bygroups(Keyword, Text, Keyword, Text, Keyword)),
              (
               '(module|declare)(\\s+)(namespace)',
               bygroups(Keyword, Text, Keyword), 'namespacedecl'),
              (
               '(declare)(\\s+)(base-uri)',
               bygroups(Keyword, Text, Keyword), 'namespacedecl'),
              (
               '(declare)(\\s+)(default)(\\s+)(element|function)',
               bygroups(Keyword, Text, Keyword, Text, Keyword), 'namespacekeyword'),
              (
               '(import)(\\s+)(schema|module)',
               bygroups(Keyword.Pseudo, Text, Keyword.Pseudo), 'namespacekeyword'),
              (
               '(declare)(\\s+)(copy-namespaces)',
               bygroups(Keyword, Text, Keyword), 'namespacekeyword'),
              (
               '(for|let|some|every)(\\s+)(\\$)',
               bygroups(Keyword, Text, Name.Variable), 'varname'),
              (
               '\\$', Name.Variable, 'varname'),
              (
               '(declare)(\\s+)(variable)(\\s+)(\\$)',
               bygroups(Keyword, Text, Keyword, Text, Name.Variable), 'varname'),
              (
               '(\\))(\\s+)(as)', bygroups(Operator, Text, Keyword), 'itemtype'),
              (
               '(element|attribute|schema-element|schema-attribute|comment|text|node|document-node)(\\s+)(\\()',
               pushstate_operator_kindtest_callback),
              (
               '(processing-instruction)(\\s+)(\\()',
               pushstate_operator_kindtestforpi_callback),
              (
               '(<!--)', pushstate_operator_xmlcomment_callback),
              (
               '(<\\?)', pushstate_operator_processing_instruction_callback),
              (
               '(<!\\[CDATA\\[)', pushstate_operator_cdata_section_callback),
              (
               '(<)', pushstate_operator_starttag_callback),
              (
               '(declare)(\\s+)(boundary-space)',
               bygroups(Keyword, Text, Keyword), 'xmlspace_decl'),
              (
               '(validate)(\\s+)(lax|strict)',
               pushstate_operator_root_validate_withmode),
              (
               '(validate)(\\s*)(\\{)', pushstate_operator_root_validate),
              (
               '(typeswitch)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation)),
              (
               '(element|attribute)(\\s*)(\\{)',
               pushstate_operator_root_construct_callback),
              (
               '(document|text|processing-instruction|comment)(\\s*)(\\{)',
               pushstate_operator_root_construct_callback),
              (
               '(attribute)(\\s+)(?=' + qname + ')',
               bygroups(Keyword, Text), 'attribute_qname'),
              (
               '(element)(\\s+)(?=' + qname + ')',
               bygroups(Keyword, Text), 'element_qname'),
              (
               '(processing-instruction)(\\s+)' + ncname + '(\\s*)(\\{)',
               bygroups(Keyword, Text, Name.Variable, Text, Punctuation), 'operator'),
              (
               '(declare|define)(\\s+)(function)',
               bygroups(Keyword, Text, Keyword)),
              (
               '(\\{)', pushstate_operator_root_callback),
              (
               '(unordered|ordered)(\\s*)(\\{)',
               pushstate_operator_order_callback),
              (
               '(declare)(\\s+)(ordering)',
               bygroups(Keyword, Text, Keyword), 'declareordering'),
              (
               '(xquery)(\\s+)(version)',
               bygroups(Keyword.Pseudo, Text, Keyword.Pseudo), 'xqueryversion'),
              (
               '(\\(#)', Punctuation, 'pragma'),
              (
               'return', Keyword),
              (
               '(declare)(\\s+)(option)', bygroups(Keyword, Text, Keyword),
               'option'),
              (
               '(at)(\\s+)(' + stringdouble + ')', String.Double, 'namespacedecl'),
              (
               '(at)(\\s+)(' + stringsingle + ')', String.Single, 'namespacedecl'),
              (
               '(ancestor-or-self|ancestor|attribute|child|descendant-or-self)(::)',
               bygroups(Keyword, Punctuation)),
              (
               '(descendant|following-sibling|following|parent|preceding-sibling|preceding|self)(::)',
               bygroups(Keyword, Punctuation)),
              (
               '(if)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation)),
              (
               'then|else', Keyword),
              (
               '(try)(\\s*)', bygroups(Keyword, Text), 'root'),
              (
               '(catch)(\\s*)(\\()(\\$)',
               bygroups(Keyword, Text, Punctuation, Name.Variable), 'varname'),
              (
               '@' + qname, Name.Attribute),
              (
               '@\\*', Name.Attribute),
              (
               '@' + ncname, Name.Attribute),
              (
               '//|/|\\+|-|;|,|\\(|\\)', Punctuation),
              (
               qname + '(?=\\s*[{])', Name.Variable, 'qname_braren'),
              (
               qname + '(?=\\s*[(])', Name.Function, 'qname_braren'),
              (
               qname, Name.Variable, 'operator')]}
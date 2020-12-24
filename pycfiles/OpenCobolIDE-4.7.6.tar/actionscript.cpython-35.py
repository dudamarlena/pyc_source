# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/actionscript.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 11179 bytes
"""
    pygments.lexers.actionscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for ActionScript and MXML.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, bygroups, using, this, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = [
 'ActionScriptLexer', 'ActionScript3Lexer', 'MxmlLexer']

class ActionScriptLexer(RegexLexer):
    __doc__ = '\n    For ActionScript source code.\n\n    .. versionadded:: 0.9\n    '
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
               '[~^*!%&<>|+=:;,/?\\\\-]+', Operator),
              (
               '[{}\\[\\]();.]+', Punctuation),
              (
               words(('case', 'default', 'for', 'each', 'in', 'while', 'do', 'break', 'return', 'continue',
       'if', 'else', 'throw', 'try', 'catch', 'var', 'with', 'new', 'typeof', 'arguments',
       'instanceof', 'this', 'switch'), suffix='\\b'),
               Keyword),
              (
               words(('class', 'public', 'final', 'internal', 'native', 'override', 'private', 'protected',
       'static', 'import', 'extends', 'implements', 'interface', 'intrinsic', 'return',
       'super', 'dynamic', 'function', 'const', 'get', 'namespace', 'package', 'set'), suffix='\\b'),
               Keyword.Declaration),
              (
               '(true|false|null|NaN|Infinity|-Infinity|undefined|Void)\\b',
               Keyword.Constant),
              (
               words(('Accessibility', 'AccessibilityProperties', 'ActionScriptVersion', 'ActivityEvent',
       'AntiAliasType', 'ApplicationDomain', 'AsBroadcaster', 'Array', 'AsyncErrorEvent',
       'AVM1Movie', 'BevelFilter', 'Bitmap', 'BitmapData', 'BitmapDataChannel', 'BitmapFilter',
       'BitmapFilterQuality', 'BitmapFilterType', 'BlendMode', 'BlurFilter', 'Boolean',
       'ByteArray', 'Camera', 'Capabilities', 'CapsStyle', 'Class', 'Color', 'ColorMatrixFilter',
       'ColorTransform', 'ContextMenu', 'ContextMenuBuiltInItems', 'ContextMenuEvent',
       'ContextMenuItem', 'ConvultionFilter', 'CSMSettings', 'DataEvent', 'Date',
       'DefinitionError', 'DeleteObjectSample', 'Dictionary', 'DisplacmentMapFilter',
       'DisplayObject', 'DisplacmentMapFilterMode', 'DisplayObjectContainer', 'DropShadowFilter',
       'Endian', 'EOFError', 'Error', 'ErrorEvent', 'EvalError', 'Event', 'EventDispatcher',
       'EventPhase', 'ExternalInterface', 'FileFilter', 'FileReference', 'FileReferenceList',
       'FocusDirection', 'FocusEvent', 'Font', 'FontStyle', 'FontType', 'FrameLabel',
       'FullScreenEvent', 'Function', 'GlowFilter', 'GradientBevelFilter', 'GradientGlowFilter',
       'GradientType', 'Graphics', 'GridFitType', 'HTTPStatusEvent', 'IBitmapDrawable',
       'ID3Info', 'IDataInput', 'IDataOutput', 'IDynamicPropertyOutputIDynamicPropertyWriter',
       'IEventDispatcher', 'IExternalizable', 'IllegalOperationError', 'IME', 'IMEConversionMode',
       'IMEEvent', 'int', 'InteractiveObject', 'InterpolationMethod', 'InvalidSWFError',
       'InvokeEvent', 'IOError', 'IOErrorEvent', 'JointStyle', 'Key', 'Keyboard',
       'KeyboardEvent', 'KeyLocation', 'LineScaleMode', 'Loader', 'LoaderContext',
       'LoaderInfo', 'LoadVars', 'LocalConnection', 'Locale', 'Math', 'Matrix', 'MemoryError',
       'Microphone', 'MorphShape', 'Mouse', 'MouseEvent', 'MovieClip', 'MovieClipLoader',
       'Namespace', 'NetConnection', 'NetStatusEvent', 'NetStream', 'NewObjectSample',
       'Number', 'Object', 'ObjectEncoding', 'PixelSnapping', 'Point', 'PrintJob',
       'PrintJobOptions', 'PrintJobOrientation', 'ProgressEvent', 'Proxy', 'QName',
       'RangeError', 'Rectangle', 'ReferenceError', 'RegExp', 'Responder', 'Sample',
       'Scene', 'ScriptTimeoutError', 'Security', 'SecurityDomain', 'SecurityError',
       'SecurityErrorEvent', 'SecurityPanel', 'Selection', 'Shape', 'SharedObject',
       'SharedObjectFlushStatus', 'SimpleButton', 'Socket', 'Sound', 'SoundChannel',
       'SoundLoaderContext', 'SoundMixer', 'SoundTransform', 'SpreadMethod', 'Sprite',
       'StackFrame', 'StackOverflowError', 'Stage', 'StageAlign', 'StageDisplayState',
       'StageQuality', 'StageScaleMode', 'StaticText', 'StatusEvent', 'String', 'StyleSheet',
       'SWFVersion', 'SyncEvent', 'SyntaxError', 'System', 'TextColorType', 'TextField',
       'TextFieldAutoSize', 'TextFieldType', 'TextFormat', 'TextFormatAlign', 'TextLineMetrics',
       'TextRenderer', 'TextSnapshot', 'Timer', 'TimerEvent', 'Transform', 'TypeError',
       'uint', 'URIError', 'URLLoader', 'URLLoaderDataFormat', 'URLRequest', 'URLRequestHeader',
       'URLRequestMethod', 'URLStream', 'URLVariabeles', 'VerifyError', 'Video',
       'XML', 'XMLDocument', 'XMLList', 'XMLNode', 'XMLNodeType', 'XMLSocket', 'XMLUI'), suffix='\\b'),
               Name.Builtin),
              (
               words(('decodeURI', 'decodeURIComponent', 'encodeURI', 'escape', 'eval', 'isFinite',
       'isNaN', 'isXMLName', 'clearInterval', 'fscommand', 'getTimer', 'getURL',
       'getVersion', 'parseFloat', 'parseInt', 'setInterval', 'trace', 'updateAfterEvent',
       'unescape'), suffix='\\b'),
               Name.Function),
              (
               '[$a-zA-Z_]\\w*', Name.Other),
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


class ActionScript3Lexer(RegexLexer):
    __doc__ = '\n    For ActionScript 3 source code.\n\n    .. versionadded:: 0.11\n    '
    name = 'ActionScript 3'
    aliases = ['as3', 'actionscript3']
    filenames = ['*.as']
    mimetypes = ['application/x-actionscript3', 'text/x-actionscript3',
     'text/actionscript3']
    identifier = '[$a-zA-Z_]\\w*'
    typeidentifier = identifier + '(?:\\.<\\w+>)?'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(function\\s+)(' + identifier + ')(\\s*)(\\()',
               bygroups(Keyword.Declaration, Name.Function, Text, Operator),
               'funcparams'),
              (
               '(var|const)(\\s+)(' + identifier + ')(\\s*)(:)(\\s*)(' + typeidentifier + ')',
               bygroups(Keyword.Declaration, Text, Name, Text, Punctuation, Text, Keyword.Type)),
              (
               '(import|package)(\\s+)((?:' + identifier + '|\\.)+)(\\s*)',
               bygroups(Keyword, Text, Name.Namespace, Text)),
              (
               '(new)(\\s+)(' + typeidentifier + ')(\\s*)(\\()',
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
               '[~^*!%&<>|+=:;,/?\\\\{}\\[\\]().-]+', Operator)], 
     
     'funcparams': [
                    (
                     '\\s+', Text),
                    (
                     '(\\s*)(\\.\\.\\.)?(' + identifier + ')(\\s*)(:)(\\s*)(' + typeidentifier + '|\\*)(\\s*)',
                     bygroups(Text, Punctuation, Name, Text, Operator, Text, Keyword.Type, Text), 'defval'),
                    (
                     '\\)', Operator, 'type')], 
     
     'type': [
              (
               '(\\s*)(:)(\\s*)(' + typeidentifier + '|\\*)',
               bygroups(Text, Operator, Text, Keyword.Type), '#pop:2'),
              (
               '\\s+', Text, '#pop:2'),
              default('#pop:2')], 
     
     'defval': [
                (
                 '(=)(\\s*)([^(),]+)(\\s*)(,?)',
                 bygroups(Operator, Text, using(this), Text, Operator), '#pop'),
                (
                 ',', Operator, '#pop'),
                default('#pop')]}

    def analyse_text(text):
        if re.match('\\w+\\s*:\\s*\\w', text):
            return 0.3
        return 0


class MxmlLexer(RegexLexer):
    __doc__ = '\n    For MXML markup.\n    Nested AS3 in <script> tags is highlighted by the appropriate lexer.\n\n    .. versionadded:: 1.1\n    '
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
               '<\\s*[\\w:.-]+', Name.Tag, 'tag'),
              (
               '<\\s*/\\s*[\\w:.-]+\\s*>', Name.Tag)], 
     
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
              '[\\w.:-]+\\s*=', Name.Attribute, 'attr'),
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
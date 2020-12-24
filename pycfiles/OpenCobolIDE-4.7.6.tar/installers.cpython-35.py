# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/installers.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 12866 bytes
"""
    pygments.lexers.installers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for installer/packager DSLs and formats.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation, Generic, Number, Whitespace
__all__ = [
 'NSISLexer', 'RPMSpecLexer', 'SourcesListLexer',
 'DebianControlLexer']

class NSISLexer(RegexLexer):
    __doc__ = '\n    For `NSIS <http://nsis.sourceforge.net/>`_ scripts.\n\n    .. versionadded:: 1.6\n    '
    name = 'NSIS'
    aliases = ['nsis', 'nsi', 'nsh']
    filenames = ['*.nsi', '*.nsh']
    mimetypes = ['text/x-nsis']
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '[;#].*\\n', Comment),
              (
               "'.*?'", String.Single),
              (
               '"', String.Double, 'str_double'),
              (
               '`', String.Backtick, 'str_backtick'),
              include('macro'),
              include('interpol'),
              include('basic'),
              (
               '\\$\\{[a-z_|][\\w|]*\\}', Keyword.Pseudo),
              (
               '/[a-z_]\\w*', Name.Attribute),
              (
               '.', Text)], 
     
     'basic': [
               (
                '(\\n)(Function)(\\s+)([._a-z][.\\w]*)\\b',
                bygroups(Text, Keyword, Text, Name.Function)),
               (
                '\\b([_a-z]\\w*)(::)([a-z][a-z0-9]*)\\b',
                bygroups(Keyword.Namespace, Punctuation, Name.Function)),
               (
                '\\b([_a-z]\\w*)(:)', bygroups(Name.Label, Punctuation)),
               (
                '(\\b[ULS]|\\B)([!<>=]?=|\\<\\>?|\\>)\\B', Operator),
               (
                '[|+-]', Operator),
               (
                '\\\\', Punctuation),
               (
                '\\b(Abort|Add(?:BrandingImage|Size)|Allow(?:RootDirInstall|SkipFiles)|AutoCloseWindow|BG(?:Font|Gradient)|BrandingText|BringToFront|Call(?:InstDLL)?|(?:Sub)?Caption|ChangeUI|CheckBitmap|ClearErrors|CompletedText|ComponentText|CopyFiles|CRCCheck|Create(?:Directory|Font|Shortcut)|Delete(?:INI(?:Sec|Str)|Reg(?:Key|Value))?|DetailPrint|DetailsButtonText|Dir(?:Show|Text|Var|Verify)|(?:Disabled|Enabled)Bitmap|EnableWindow|EnumReg(?:Key|Value)|Exch|Exec(?:Shell|Wait)?|ExpandEnvStrings|File(?:BufSize|Close|ErrorText|Open|Read(?:Byte)?|Seek|Write(?:Byte)?)?|Find(?:Close|First|Next|Window)|FlushINI|Function(?:End)?|Get(?:CurInstType|CurrentAddress|DlgItem|DLLVersion(?:Local)?|ErrorLevel|FileTime(?:Local)?|FullPathName|FunctionAddress|InstDirError|LabelAddress|TempFileName)|Goto|HideWindow|Icon|If(?:Abort|Errors|FileExists|RebootFlag|Silent)|InitPluginsDir|Install(?:ButtonText|Colors|Dir(?:RegKey)?)|Inst(?:ProgressFlags|Type(?:[GS]etText)?)|Int(?:CmpU?|Fmt|Op)|IsWindow|LangString(?:UP)?|License(?:BkColor|Data|ForceSelection|LangString|Text)|LoadLanguageFile|LockWindow|Log(?:Set|Text)|MessageBox|MiscButtonText|Name|Nop|OutFile|(?:Uninst)?Page(?:Ex(?:End)?)?|PluginDir|Pop|Push|Quit|Read(?:(?:Env|INI|Reg)Str|RegDWORD)|Reboot|(?:Un)?RegDLL|Rename|RequestExecutionLevel|ReserveFile|Return|RMDir|SearchPath|Section(?:Divider|End|(?:(?:Get|Set)(?:Flags|InstTypes|Size|Text))|Group(?:End)?|In)?|SendMessage|Set(?:AutoClose|BrandingImage|Compress(?:ionLevel|or(?:DictSize)?)?|CtlColors|CurInstType|DatablockOptimize|DateSave|Details(?:Print|View)|Error(?:s|Level)|FileAttributes|Font|OutPath|Overwrite|PluginUnload|RebootFlag|ShellVarContext|Silent|StaticBkColor)|Show(?:(?:I|Uni)nstDetails|Window)|Silent(?:Un)?Install|Sleep|SpaceTexts|Str(?:CmpS?|Cpy|Len)|SubSection(?:End)?|Uninstall(?:ButtonText|(?:Sub)?Caption|EXEName|Icon|Text)|UninstPage|Var|VI(?:AddVersionKey|ProductVersion)|WindowIcon|Write(?:INIStr|Reg(:?Bin|DWORD|(?:Expand)?Str)|Uninstaller)|XPStyle)\\b',
                Keyword),
               (
                '\\b(CUR|END|(?:FILE_ATTRIBUTE_)?(?:ARCHIVE|HIDDEN|NORMAL|OFFLINE|READONLY|SYSTEM|TEMPORARY)|HK(CC|CR|CU|DD|LM|PD|U)|HKEY_(?:CLASSES_ROOT|CURRENT_(?:CONFIG|USER)|DYN_DATA|LOCAL_MACHINE|PERFORMANCE_DATA|USERS)|ID(?:ABORT|CANCEL|IGNORE|NO|OK|RETRY|YES)|MB_(?:ABORTRETRYIGNORE|DEFBUTTON[1-4]|ICON(?:EXCLAMATION|INFORMATION|QUESTION|STOP)|OK(?:CANCEL)?|RETRYCANCEL|RIGHT|SETFOREGROUND|TOPMOST|USERICON|YESNO(?:CANCEL)?)|SET|SHCTX|SW_(?:HIDE|SHOW(?:MAXIMIZED|MINIMIZED|NORMAL))|admin|all|auto|both|bottom|bzip2|checkbox|colored|current|false|force|hide|highest|if(?:diff|newer)|lastused|leave|left|listonly|lzma|nevershow|none|normal|off|on|pop|push|radiobuttons|right|show|silent|silentlog|smooth|textonly|top|true|try|user|zlib)\\b',
                Name.Constant)], 
     
     'macro': [
               (
                '\\!(addincludedir(?:dir)?|addplugindir|appendfile|cd|define|delfilefile|echo(?:message)?|else|endif|error|execute|if(?:macro)?n?(?:def)?|include|insertmacro|macro(?:end)?|packhdr|search(?:parse|replace)|system|tempfilesymbol|undef|verbose|warning)\\b',
                Comment.Preproc)], 
     
     'interpol': [
                  (
                   '\\$(R?[0-9])', Name.Builtin.Pseudo),
                  (
                   '\\$(ADMINTOOLS|APPDATA|CDBURN_AREA|COOKIES|COMMONFILES(?:32|64)|DESKTOP|DOCUMENTS|EXE(?:DIR|FILE|PATH)|FAVORITES|FONTS|HISTORY|HWNDPARENT|INTERNET_CACHE|LOCALAPPDATA|MUSIC|NETHOOD|PICTURES|PLUGINSDIR|PRINTHOOD|PROFILE|PROGRAMFILES(?:32|64)|QUICKLAUNCH|RECENT|RESOURCES(?:_LOCALIZED)?|SENDTO|SM(?:PROGRAMS|STARTUP)|STARTMENU|SYSDIR|TEMP(?:LATES)?|VIDEOS|WINDIR|\\{NSISDIR\\})',
                   Name.Builtin),
                  (
                   '\\$(CMDLINE|INSTDIR|OUTDIR|LANGUAGE)', Name.Variable.Global),
                  (
                   '\\$[a-z_]\\w*', Name.Variable)], 
     
     'str_double': [
                    (
                     '"', String, '#pop'),
                    (
                     '\\$(\\\\[nrt"]|\\$)', String.Escape),
                    include('interpol'),
                    (
                     '.', String.Double)], 
     
     'str_backtick': [
                      (
                       '`', String, '#pop'),
                      (
                       '\\$(\\\\[nrt"]|\\$)', String.Escape),
                      include('interpol'),
                      (
                       '.', String.Double)]}


class RPMSpecLexer(RegexLexer):
    __doc__ = '\n    For RPM ``.spec`` files.\n\n    .. versionadded:: 1.6\n    '
    name = 'RPMSpec'
    aliases = ['spec']
    filenames = ['*.spec']
    mimetypes = ['text/x-rpm-spec']
    _directives = '(?:package|prep|build|install|clean|check|pre[a-z]*|post[a-z]*|trigger[a-z]*|files)'
    tokens = {'root': [
              (
               '#.*\\n', Comment),
              include('basic')], 
     
     'description': [
                     (
                      '^(%' + _directives + ')(.*)$',
                      bygroups(Name.Decorator, Text), '#pop'),
                     (
                      '\\n', Text),
                     (
                      '.', Text)], 
     
     'changelog': [
                   (
                    '\\*.*\\n', Generic.Subheading),
                   (
                    '^(%' + _directives + ')(.*)$',
                    bygroups(Name.Decorator, Text), '#pop'),
                   (
                    '\\n', Text),
                   (
                    '.', Text)], 
     
     'string': [
                (
                 '"', String.Double, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                include('interpol'),
                (
                 '.', String.Double)], 
     
     'basic': [
               include('macro'),
               (
                '(?i)^(Name|Version|Release|Epoch|Summary|Group|License|Packager|Vendor|Icon|URL|Distribution|Prefix|Patch[0-9]*|Source[0-9]*|Requires\\(?[a-z]*\\)?|[a-z]+Req|Obsoletes|Suggests|Provides|Conflicts|Build[a-z]+|[a-z]+Arch|Auto[a-z]+)(:)(.*)$',
                bygroups(Generic.Heading, Punctuation, using(this))),
               (
                '^%description', Name.Decorator, 'description'),
               (
                '^%changelog', Name.Decorator, 'changelog'),
               (
                '^(%' + _directives + ')(.*)$', bygroups(Name.Decorator, Text)),
               (
                '%(attr|defattr|dir|doc(?:dir)?|setup|config(?:ure)?|make(?:install)|ghost|patch[0-9]+|find_lang|exclude|verify)',
                Keyword),
               include('interpol'),
               (
                "'.*?'", String.Single),
               (
                '"', String.Double, 'string'),
               (
                '.', Text)], 
     
     'macro': [
               (
                '%define.*\\n', Comment.Preproc),
               (
                '%\\{\\!\\?.*%define.*\\}', Comment.Preproc),
               (
                '(%(?:if(?:n?arch)?|else(?:if)?|endif))(.*)$',
                bygroups(Comment.Preproc, Text))], 
     
     'interpol': [
                  (
                   '%\\{?__[a-z_]+\\}?', Name.Function),
                  (
                   '%\\{?_([a-z_]+dir|[a-z_]+path|prefix)\\}?', Keyword.Pseudo),
                  (
                   '%\\{\\?\\w+\\}', Name.Variable),
                  (
                   '\\$\\{?RPM_[A-Z0-9_]+\\}?', Name.Variable.Global),
                  (
                   '%\\{[a-zA-Z]\\w+\\}', Keyword.Constant)]}


class SourcesListLexer(RegexLexer):
    __doc__ = '\n    Lexer that highlights debian sources.list files.\n\n    .. versionadded:: 0.7\n    '
    name = 'Debian Sourcelist'
    aliases = ['sourceslist', 'sources.list', 'debsources']
    filenames = ['sources.list']
    mimetype = ['application/x-debian-sourceslist']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*?$', Comment),
              (
               '^(deb(?:-src)?)(\\s+)',
               bygroups(Keyword, Text), 'distribution')], 
     
     'distribution': [
                      (
                       '#.*?$', Comment, '#pop'),
                      (
                       '\\$\\(ARCH\\)', Name.Variable),
                      (
                       '[^\\s$[]+', String),
                      (
                       '\\[', String.Other, 'escaped-distribution'),
                      (
                       '\\$', String),
                      (
                       '\\s+', Text, 'components')], 
     
     'escaped-distribution': [
                              (
                               '\\]', String.Other, '#pop'),
                              (
                               '\\$\\(ARCH\\)', Name.Variable),
                              (
                               '[^\\]$]+', String.Other),
                              (
                               '\\$', String.Other)], 
     
     'components': [
                    (
                     '#.*?$', Comment, '#pop:2'),
                    (
                     '$', Text, '#pop:2'),
                    (
                     '\\s+', Text),
                    (
                     '\\S+', Keyword.Pseudo)]}

    def analyse_text(text):
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('deb ') or line.startswith('deb-src '):
                return True


class DebianControlLexer(RegexLexer):
    __doc__ = '\n    Lexer for Debian ``control`` files and ``apt-cache show <pkg>`` outputs.\n\n    .. versionadded:: 0.9\n    '
    name = 'Debian Control file'
    aliases = ['control', 'debcontrol']
    filenames = ['control']
    tokens = {'root': [
              (
               '^(Description)', Keyword, 'description'),
              (
               '^(Maintainer)(:\\s*)', bygroups(Keyword, Text), 'maintainer'),
              (
               '^((Build-)?Depends)', Keyword, 'depends'),
              (
               '^((?:Python-)?Version)(:\\s*)(\\S+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^((?:Installed-)?Size)(:\\s*)(\\S+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^(MD5Sum|SHA1|SHA256)(:\\s*)(\\S+)$',
               bygroups(Keyword, Text, Number)),
              (
               '^([a-zA-Z\\-0-9\\.]*?)(:\\s*)(.*?)$',
               bygroups(Keyword, Whitespace, String))], 
     
     'maintainer': [
                    (
                     '<[^>]+>', Generic.Strong),
                    (
                     '<[^>]+>$', Generic.Strong, '#pop'),
                    (
                     ',\\n?', Text),
                    (
                     '.', Text)], 
     
     'description': [
                     (
                      '(.*)(Homepage)(: )(\\S+)',
                      bygroups(Text, String, Name, Name.Class)),
                     (
                      ':.*\\n', Generic.Strong),
                     (
                      ' .*\\n', Text),
                     default('#pop')], 
     
     'depends': [
                 (
                  ':\\s*', Text),
                 (
                  '(\\$)(\\{)(\\w+\\s*:\\s*\\w+)', bygroups(Operator, Text, Name.Entity)),
                 (
                  '\\(', Text, 'depend_vers'),
                 (
                  ',', Text),
                 (
                  '\\|', Operator),
                 (
                  '[\\s]+', Text),
                 (
                  '[})]\\s*$', Text, '#pop'),
                 (
                  '\\}', Text),
                 (
                  '[^,]$', Name.Function, '#pop'),
                 (
                  '([+.a-zA-Z0-9-])(\\s*)', bygroups(Name.Function, Text)),
                 (
                  '\\[.*?\\]', Name.Entity)], 
     
     'depend_vers': [
                     (
                      '\\),', Text, '#pop'),
                     (
                      '\\)[^,]', Text, '#pop:2'),
                     (
                      '([><=]+)(\\s*)([^)]+)', bygroups(Operator, Text, Number))]}
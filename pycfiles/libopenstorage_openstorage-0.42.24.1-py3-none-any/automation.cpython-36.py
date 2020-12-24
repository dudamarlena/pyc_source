# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/automation.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 19640 bytes
"""
    pygments.lexers.automation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for automation scripting languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups, combined
from pygments.token import Text, Comment, Operator, Name, String, Number, Punctuation, Generic
__all__ = [
 'AutohotkeyLexer', 'AutoItLexer']

class AutohotkeyLexer(RegexLexer):
    __doc__ = '\n    For `autohotkey <http://www.autohotkey.com/>`_ source code.\n\n    .. versionadded:: 1.4\n    '
    name = 'autohotkey'
    aliases = ['ahk', 'autohotkey']
    filenames = ['*.ahk', '*.ahkl']
    mimetypes = ['text/x-autohotkey']
    tokens = {'root':[
      (
       '^(\\s*)(/\\*)', bygroups(Text, Comment.Multiline), 'incomment'),
      (
       '^(\\s*)(\\()', bygroups(Text, Generic), 'incontinuation'),
      (
       '\\s+;.*?$', Comment.Single),
      (
       '^;.*?$', Comment.Single),
      (
       '[]{}(),;[]', Punctuation),
      (
       '(in|is|and|or|not)\\b', Operator.Word),
      (
       '\\%[a-zA-Z_#@$][\\w#@$]*\\%', Name.Variable),
      (
       '!=|==|:=|\\.=|<<|>>|[-~+/*%=<>&^|?:!.]', Operator),
      include('commands'),
      include('labels'),
      include('builtInFunctions'),
      include('builtInVariables'),
      (
       '"', String, combined('stringescape', 'dqs')),
      include('numbers'),
      (
       '[a-zA-Z_#@$][\\w#@$]*', Name),
      (
       "\\\\|\\'", Text),
      (
       '\\`([,%`abfnrtv\\-+;])', String.Escape),
      include('garbage')], 
     'incomment':[
      (
       '^\\s*\\*/', Comment.Multiline, '#pop'),
      (
       '[^*/]', Comment.Multiline),
      (
       '[*/]', Comment.Multiline)], 
     'incontinuation':[
      (
       '^\\s*\\)', Generic, '#pop'),
      (
       '[^)]', Generic),
      (
       '[)]', Generic)], 
     'commands':[
      (
       '(?i)^(\\s*)(global|local|static|#AllowSameLineComments|#ClipboardTimeout|#CommentFlag|#ErrorStdOut|#EscapeChar|#HotkeyInterval|#HotkeyModifierTimeout|#Hotstring|#IfWinActive|#IfWinExist|#IfWinNotActive|#IfWinNotExist|#IncludeAgain|#Include|#InstallKeybdHook|#InstallMouseHook|#KeyHistory|#LTrim|#MaxHotkeysPerInterval|#MaxMem|#MaxThreads|#MaxThreadsBuffer|#MaxThreadsPerHotkey|#NoEnv|#NoTrayIcon|#Persistent|#SingleInstance|#UseHook|#WinActivateForce|AutoTrim|BlockInput|Break|Click|ClipWait|Continue|Control|ControlClick|ControlFocus|ControlGetFocus|ControlGetPos|ControlGetText|ControlGet|ControlMove|ControlSend|ControlSendRaw|ControlSetText|CoordMode|Critical|DetectHiddenText|DetectHiddenWindows|Drive|DriveGet|DriveSpaceFree|Edit|Else|EnvAdd|EnvDiv|EnvGet|EnvMult|EnvSet|EnvSub|EnvUpdate|Exit|ExitApp|FileAppend|FileCopy|FileCopyDir|FileCreateDir|FileCreateShortcut|FileDelete|FileGetAttrib|FileGetShortcut|FileGetSize|FileGetTime|FileGetVersion|FileInstall|FileMove|FileMoveDir|FileRead|FileReadLine|FileRecycle|FileRecycleEmpty|FileRemoveDir|FileSelectFile|FileSelectFolder|FileSetAttrib|FileSetTime|FormatTime|GetKeyState|Gosub|Goto|GroupActivate|GroupAdd|GroupClose|GroupDeactivate|Gui|GuiControl|GuiControlGet|Hotkey|IfEqual|IfExist|IfGreaterOrEqual|IfGreater|IfInString|IfLess|IfLessOrEqual|IfMsgBox|IfNotEqual|IfNotExist|IfNotInString|IfWinActive|IfWinExist|IfWinNotActive|IfWinNotExist|If |ImageSearch|IniDelete|IniRead|IniWrite|InputBox|Input|KeyHistory|KeyWait|ListHotkeys|ListLines|ListVars|Loop|Menu|MouseClickDrag|MouseClick|MouseGetPos|MouseMove|MsgBox|OnExit|OutputDebug|Pause|PixelGetColor|PixelSearch|PostMessage|Process|Progress|Random|RegDelete|RegRead|RegWrite|Reload|Repeat|Return|RunAs|RunWait|Run|SendEvent|SendInput|SendMessage|SendMode|SendPlay|SendRaw|Send|SetBatchLines|SetCapslockState|SetControlDelay|SetDefaultMouseSpeed|SetEnv|SetFormat|SetKeyDelay|SetMouseDelay|SetNumlockState|SetScrollLockState|SetStoreCapslockMode|SetTimer|SetTitleMatchMode|SetWinDelay|SetWorkingDir|Shutdown|Sleep|Sort|SoundBeep|SoundGet|SoundGetWaveVolume|SoundPlay|SoundSet|SoundSetWaveVolume|SplashImage|SplashTextOff|SplashTextOn|SplitPath|StatusBarGetText|StatusBarWait|StringCaseSense|StringGetPos|StringLeft|StringLen|StringLower|StringMid|StringReplace|StringRight|StringSplit|StringTrimLeft|StringTrimRight|StringUpper|Suspend|SysGet|Thread|ToolTip|Transform|TrayTip|URLDownloadToFile|While|WinActivate|WinActivateBottom|WinClose|WinGetActiveStats|WinGetActiveTitle|WinGetClass|WinGetPos|WinGetText|WinGetTitle|WinGet|WinHide|WinKill|WinMaximize|WinMenuSelectItem|WinMinimizeAllUndo|WinMinimizeAll|WinMinimize|WinMove|WinRestore|WinSetTitle|WinSet|WinShow|WinWaitActive|WinWaitClose|WinWaitNotActive|WinWait)\\b',
       bygroups(Text, Name.Builtin))], 
     'builtInFunctions':[
      (
       '(?i)(Abs|ACos|Asc|ASin|ATan|Ceil|Chr|Cos|DllCall|Exp|FileExist|Floor|GetKeyState|IL_Add|IL_Create|IL_Destroy|InStr|IsFunc|IsLabel|Ln|Log|LV_Add|LV_Delete|LV_DeleteCol|LV_GetCount|LV_GetNext|LV_GetText|LV_Insert|LV_InsertCol|LV_Modify|LV_ModifyCol|LV_SetImageList|Mod|NumGet|NumPut|OnMessage|RegExMatch|RegExReplace|RegisterCallback|Round|SB_SetIcon|SB_SetParts|SB_SetText|Sin|Sqrt|StrLen|SubStr|Tan|TV_Add|TV_Delete|TV_GetChild|TV_GetCount|TV_GetNext|TV_Get|TV_GetParent|TV_GetPrev|TV_GetSelection|TV_GetText|TV_Modify|VarSetCapacity|WinActive|WinExist|Object|ComObjActive|ComObjArray|ComObjEnwrap|ComObjUnwrap|ComObjParameter|ComObjType|ComObjConnect|ComObjCreate|ComObjGet|ComObjError|ComObjValue|Insert|MinIndex|MaxIndex|Remove|SetCapacity|GetCapacity|GetAddress|_NewEnum|FileOpen|Read|Write|ReadLine|WriteLine|ReadNumType|WriteNumType|RawRead|RawWrite|Seek|Tell|Close|Next|IsObject|StrPut|StrGet|Trim|LTrim|RTrim)\\b',
       Name.Function)], 
     'builtInVariables':[
      (
       '(?i)(A_AhkPath|A_AhkVersion|A_AppData|A_AppDataCommon|A_AutoTrim|A_BatchLines|A_CaretX|A_CaretY|A_ComputerName|A_ControlDelay|A_Cursor|A_DDDD|A_DDD|A_DD|A_DefaultMouseSpeed|A_Desktop|A_DesktopCommon|A_DetectHiddenText|A_DetectHiddenWindows|A_EndChar|A_EventInfo|A_ExitReason|A_FormatFloat|A_FormatInteger|A_Gui|A_GuiEvent|A_GuiControl|A_GuiControlEvent|A_GuiHeight|A_GuiWidth|A_GuiX|A_GuiY|A_Hour|A_IconFile|A_IconHidden|A_IconNumber|A_IconTip|A_Index|A_IPAddress1|A_IPAddress2|A_IPAddress3|A_IPAddress4|A_ISAdmin|A_IsCompiled|A_IsCritical|A_IsPaused|A_IsSuspended|A_KeyDelay|A_Language|A_LastError|A_LineFile|A_LineNumber|A_LoopField|A_LoopFileAttrib|A_LoopFileDir|A_LoopFileExt|A_LoopFileFullPath|A_LoopFileLongPath|A_LoopFileName|A_LoopFileShortName|A_LoopFileShortPath|A_LoopFileSize|A_LoopFileSizeKB|A_LoopFileSizeMB|A_LoopFileTimeAccessed|A_LoopFileTimeCreated|A_LoopFileTimeModified|A_LoopReadLine|A_LoopRegKey|A_LoopRegName|A_LoopRegSubkey|A_LoopRegTimeModified|A_LoopRegType|A_MDAY|A_Min|A_MM|A_MMM|A_MMMM|A_Mon|A_MouseDelay|A_MSec|A_MyDocuments|A_Now|A_NowUTC|A_NumBatchLines|A_OSType|A_OSVersion|A_PriorHotkey|A_ProgramFiles|A_Programs|A_ProgramsCommon|A_ScreenHeight|A_ScreenWidth|A_ScriptDir|A_ScriptFullPath|A_ScriptName|A_Sec|A_Space|A_StartMenu|A_StartMenuCommon|A_Startup|A_StartupCommon|A_StringCaseSense|A_Tab|A_Temp|A_ThisFunc|A_ThisHotkey|A_ThisLabel|A_ThisMenu|A_ThisMenuItem|A_ThisMenuItemPos|A_TickCount|A_TimeIdle|A_TimeIdlePhysical|A_TimeSincePriorHotkey|A_TimeSinceThisHotkey|A_TitleMatchMode|A_TitleMatchModeSpeed|A_UserName|A_WDay|A_WinDelay|A_WinDir|A_WorkingDir|A_YDay|A_YEAR|A_YWeek|A_YYYY|Clipboard|ClipboardAll|ComSpec|ErrorLevel|ProgramFiles|True|False|A_IsUnicode|A_FileEncoding|A_OSVersion|A_PtrSize)\\b',
       Name.Variable)], 
     'labels':[
      (
       '(^\\s*)([^:\\s("]+?:{1,2})', bygroups(Text, Name.Label)),
      (
       '(^\\s*)(::[^:\\s]+?::)', bygroups(Text, Name.Label))], 
     'numbers':[
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+[eE][+-]?[0-9]+', Number.Float),
      (
       '0\\d+', Number.Oct),
      (
       '0[xX][a-fA-F0-9]+', Number.Hex),
      (
       '\\d+L', Number.Integer.Long),
      (
       '\\d+', Number.Integer)], 
     'stringescape':[
      (
       '\\"\\"|\\`([,%`abfnrtv])', String.Escape)], 
     'strings':[
      (
       '[^"\\n]+', String)], 
     'dqs':[
      (
       '"', String, '#pop'),
      include('strings')], 
     'garbage':[
      (
       '[^\\S\\n]', Text)]}


class AutoItLexer(RegexLexer):
    __doc__ = '\n    For `AutoIt <http://www.autoitscript.com/site/autoit/>`_ files.\n\n    AutoIt is a freeware BASIC-like scripting language\n    designed for automating the Windows GUI and general scripting\n\n    .. versionadded:: 1.6\n    '
    name = 'AutoIt'
    aliases = ['autoit']
    filenames = ['*.au3']
    mimetypes = ['text/x-autoit']
    keywords = '    #include-once #include #endregion #forcedef #forceref #region\n    and byref case continueloop dim do else elseif endfunc endif\n    endselect exit exitloop for func global\n    if local next not or return select step\n    then to until wend while exit'.split()
    functions = '    abs acos adlibregister adlibunregister asc ascw asin assign atan\n    autoitsetoption autoitwingettitle autoitwinsettitle beep binary binarylen\n    binarymid binarytostring bitand bitnot bitor bitrotate bitshift bitxor\n    blockinput break call cdtray ceiling chr chrw clipget clipput consoleread\n    consolewrite consolewriteerror controlclick controlcommand controldisable\n    controlenable controlfocus controlgetfocus controlgethandle controlgetpos\n    controlgettext controlhide controllistview controlmove controlsend\n    controlsettext controlshow controltreeview cos dec dircopy dircreate\n    dirgetsize dirmove dirremove dllcall dllcalladdress dllcallbackfree\n    dllcallbackgetptr dllcallbackregister dllclose dllopen dllstructcreate\n    dllstructgetdata dllstructgetptr dllstructgetsize dllstructsetdata\n    drivegetdrive drivegetfilesystem drivegetlabel drivegetserial drivegettype\n    drivemapadd drivemapdel drivemapget drivesetlabel drivespacefree\n    drivespacetotal drivestatus envget envset envupdate eval execute exp\n    filechangedir fileclose filecopy filecreatentfslink filecreateshortcut\n    filedelete fileexists filefindfirstfile filefindnextfile fileflush\n    filegetattrib filegetencoding filegetlongname filegetpos filegetshortcut\n    filegetshortname filegetsize filegettime filegetversion fileinstall filemove\n    fileopen fileopendialog fileread filereadline filerecycle filerecycleempty\n    filesavedialog fileselectfolder filesetattrib filesetpos filesettime\n    filewrite filewriteline floor ftpsetproxy guicreate guictrlcreateavi\n    guictrlcreatebutton guictrlcreatecheckbox guictrlcreatecombo\n    guictrlcreatecontextmenu guictrlcreatedate guictrlcreatedummy\n    guictrlcreateedit guictrlcreategraphic guictrlcreategroup guictrlcreateicon\n    guictrlcreateinput guictrlcreatelabel guictrlcreatelist\n    guictrlcreatelistview guictrlcreatelistviewitem guictrlcreatemenu\n    guictrlcreatemenuitem guictrlcreatemonthcal guictrlcreateobj\n    guictrlcreatepic guictrlcreateprogress guictrlcreateradio\n    guictrlcreateslider guictrlcreatetab guictrlcreatetabitem\n    guictrlcreatetreeview guictrlcreatetreeviewitem guictrlcreateupdown\n    guictrldelete guictrlgethandle guictrlgetstate guictrlread guictrlrecvmsg\n    guictrlregisterlistviewsort guictrlsendmsg guictrlsendtodummy\n    guictrlsetbkcolor guictrlsetcolor guictrlsetcursor guictrlsetdata\n    guictrlsetdefbkcolor guictrlsetdefcolor guictrlsetfont guictrlsetgraphic\n    guictrlsetimage guictrlsetlimit guictrlsetonevent guictrlsetpos\n    guictrlsetresizing guictrlsetstate guictrlsetstyle guictrlsettip guidelete\n    guigetcursorinfo guigetmsg guigetstyle guiregistermsg guisetaccelerators\n    guisetbkcolor guisetcoord guisetcursor guisetfont guisethelp guiseticon\n    guisetonevent guisetstate guisetstyle guistartgroup guiswitch hex hotkeyset\n    httpsetproxy httpsetuseragent hwnd inetclose inetget inetgetinfo inetgetsize\n    inetread inidelete iniread inireadsection inireadsectionnames\n    inirenamesection iniwrite iniwritesection inputbox int isadmin isarray\n    isbinary isbool isdeclared isdllstruct isfloat ishwnd isint iskeyword\n    isnumber isobj isptr isstring log memgetstats mod mouseclick mouseclickdrag\n    mousedown mousegetcursor mousegetpos mousemove mouseup mousewheel msgbox\n    number objcreate objcreateinterface objevent objevent objget objname\n    onautoitexitregister onautoitexitunregister opt ping pixelchecksum\n    pixelgetcolor pixelsearch pluginclose pluginopen processclose processexists\n    processgetstats processlist processsetpriority processwait processwaitclose\n    progressoff progresson progressset ptr random regdelete regenumkey\n    regenumval regread regwrite round run runas runaswait runwait send\n    sendkeepactive seterror setextended shellexecute shellexecutewait shutdown\n    sin sleep soundplay soundsetwavevolume splashimageon splashoff splashtexton\n    sqrt srandom statusbargettext stderrread stdinwrite stdioclose stdoutread\n    string stringaddcr stringcompare stringformat stringfromasciiarray\n    stringinstr stringisalnum stringisalpha stringisascii stringisdigit\n    stringisfloat stringisint stringislower stringisspace stringisupper\n    stringisxdigit stringleft stringlen stringlower stringmid stringregexp\n    stringregexpreplace stringreplace stringright stringsplit stringstripcr\n    stringstripws stringtoasciiarray stringtobinary stringtrimleft\n    stringtrimright stringupper tan tcpaccept tcpclosesocket tcpconnect\n    tcplisten tcpnametoip tcprecv tcpsend tcpshutdown tcpstartup timerdiff\n    timerinit tooltip traycreateitem traycreatemenu traygetmsg trayitemdelete\n    trayitemgethandle trayitemgetstate trayitemgettext trayitemsetonevent\n    trayitemsetstate trayitemsettext traysetclick trayseticon traysetonevent\n    traysetpauseicon traysetstate traysettooltip traytip ubound udpbind\n    udpclosesocket udpopen udprecv udpsend udpshutdown udpstartup vargettype\n    winactivate winactive winclose winexists winflash wingetcaretpos\n    wingetclasslist wingetclientsize wingethandle wingetpos wingetprocess\n    wingetstate wingettext wingettitle winkill winlist winmenuselectitem\n    winminimizeall winminimizeallundo winmove winsetontop winsetstate\n    winsettitle winsettrans winwait winwaitactive winwaitclose\n    winwaitnotactive'.split()
    macros = '    @appdatacommondir @appdatadir @autoitexe @autoitpid @autoitversion\n    @autoitx64 @com_eventobj @commonfilesdir @compiled @computername @comspec\n    @cpuarch @cr @crlf @desktopcommondir @desktopdepth @desktopdir\n    @desktopheight @desktoprefresh @desktopwidth @documentscommondir @error\n    @exitcode @exitmethod @extended @favoritescommondir @favoritesdir\n    @gui_ctrlhandle @gui_ctrlid @gui_dragfile @gui_dragid @gui_dropid\n    @gui_winhandle @homedrive @homepath @homeshare @hotkeypressed @hour\n    @ipaddress1 @ipaddress2 @ipaddress3 @ipaddress4 @kblayout @lf\n    @logondnsdomain @logondomain @logonserver @mday @min @mon @msec @muilang\n    @mydocumentsdir @numparams @osarch @osbuild @oslang @osservicepack @ostype\n    @osversion @programfilesdir @programscommondir @programsdir @scriptdir\n    @scriptfullpath @scriptlinenumber @scriptname @sec @startmenucommondir\n    @startmenudir @startupcommondir @startupdir @sw_disable @sw_enable @sw_hide\n    @sw_lock @sw_maximize @sw_minimize @sw_restore @sw_show @sw_showdefault\n    @sw_showmaximized @sw_showminimized @sw_showminnoactive @sw_showna\n    @sw_shownoactivate @sw_shownormal @sw_unlock @systemdir @tab @tempdir\n    @tray_id @trayiconflashing @trayiconvisible @username @userprofiledir @wday\n    @windowsdir @workingdir @yday @year'.split()
    tokens = {'root':[
      (
       ';.*\\n', Comment.Single),
      (
       '(#comments-start|#cs)(.|\\n)*?(#comments-end|#ce)',
       Comment.Multiline),
      (
       '[\\[\\]{}(),;]', Punctuation),
      (
       '(and|or|not)\\b', Operator.Word),
      (
       '[$|@][a-zA-Z_]\\w*', Name.Variable),
      (
       '!=|==|:=|\\.=|<<|>>|[-~+/*%=<>&^|?:!.]', Operator),
      include('commands'),
      include('labels'),
      include('builtInFunctions'),
      include('builtInMarcros'),
      (
       '"', String, combined('stringescape', 'dqs')),
      include('numbers'),
      (
       '[a-zA-Z_#@$][\\w#@$]*', Name),
      (
       "\\\\|\\'", Text),
      (
       '\\`([,%`abfnrtv\\-+;])', String.Escape),
      (
       '_\\n', Text),
      include('garbage')], 
     'commands':[
      (
       '(?i)(\\s*)(%s)\\b' % '|'.join(keywords),
       bygroups(Text, Name.Builtin))], 
     'builtInFunctions':[
      (
       '(?i)(%s)\\b' % '|'.join(functions),
       Name.Function)], 
     'builtInMarcros':[
      (
       '(?i)(%s)\\b' % '|'.join(macros),
       Name.Variable.Global)], 
     'labels':[
      (
       '(^\\s*)(\\{\\S+?\\})', bygroups(Text, Name.Label))], 
     'numbers':[
      (
       '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float),
      (
       '\\d+[eE][+-]?[0-9]+', Number.Float),
      (
       '0\\d+', Number.Oct),
      (
       '0[xX][a-fA-F0-9]+', Number.Hex),
      (
       '\\d+L', Number.Integer.Long),
      (
       '\\d+', Number.Integer)], 
     'stringescape':[
      (
       '\\"\\"|\\`([,%`abfnrtv])', String.Escape)], 
     'strings':[
      (
       '[^"\\n]+', String)], 
     'dqs':[
      (
       '"', String, '#pop'),
      include('strings')], 
     'garbage':[
      (
       '[^\\S\\n]', Text)]}
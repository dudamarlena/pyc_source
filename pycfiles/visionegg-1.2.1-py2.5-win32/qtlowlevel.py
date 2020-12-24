# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\qtlowlevel.py
# Compiled at: 2009-07-07 11:29:44
import os, sys, ctypes
if os.name == 'nt':
    QTMLClient = ctypes.CDLL('C:\\Program Files\\QuickTime\\QTSystem\\QTMLClient.dll')
elif sys.platform.startswith('darwin'):
    raise NotImplementedError('QuickTime support is not implemented for Mac OS X.')
OSErr = ctypes.c_short
OSStatus = ctypes.c_int
ItemCount = ctypes.c_uint
FourCharCode = ctypes.c_int
OSType = FourCharCode
QTPropertyClass = OSType
QTPropertyID = OSType
ByteCount = ctypes.c_uint
QTPropertyValuePtr = ctypes.c_void_p
QTVisualContextRef = ctypes.c_void_p

class Rect(ctypes.Structure):
    _fields_ = [
     (
      'top', ctypes.c_short),
     (
      'left', ctypes.c_short),
     (
      'bottom', ctypes.c_short),
     (
      'right', ctypes.c_short)]


Movie = ctypes.c_void_p

class QTNewMoviePropertyElement(ctypes.Structure):
    _fields_ = [
     (
      'propClass', QTPropertyClass),
     (
      'propID', QTPropertyID),
     (
      'propValueSize', ByteCount),
     (
      'propValueAddress', QTPropertyValuePtr),
     (
      'propStatus', OSStatus)]


def FOUR_CHAR_CODE(code):
    assert isinstance(code, str)
    assert len(code) == 4
    val = 0
    for i in range(4):
        c = code[i]
        ordc = ord(c)
        addval = ordc << (3 - i) * 8
        val += addval

    return val


kQTPropertyClass_DataLocation = FOUR_CHAR_CODE('dloc')
kQTDataLocationPropertyID_DataReference = FOUR_CHAR_CODE('dref')
kQTDataLocationPropertyID_CFStringNativePath = FOUR_CHAR_CODE('cfnp')
kQTDataLocationPropertyID_CFStringPosixPath = FOUR_CHAR_CODE('cfpp')
kQTDataLocationPropertyID_CFStringHFSPath = FOUR_CHAR_CODE('cfhp')
kQTDataLocationPropertyID_CFStringWindowsPath = FOUR_CHAR_CODE('cfwp')
kQTDataLocationPropertyID_CFURL = FOUR_CHAR_CODE('cfur')
kQTDataLocationPropertyID_QTDataHandler = FOUR_CHAR_CODE('qtdh')
kQTDataLocationPropertyID_Scrap = FOUR_CHAR_CODE('scrp')
kQTDataLocationPropertyID_LegacyMovieResourceHandle = FOUR_CHAR_CODE('rezh')
kQTDataLocationPropertyID_MovieUserProc = FOUR_CHAR_CODE('uspr')
kQTDataLocationPropertyID_ResourceFork = FOUR_CHAR_CODE('rfrk')
kQTDataLocationPropertyID_DataFork = FOUR_CHAR_CODE('dfrk')
kQTPropertyClass_Context = FOUR_CHAR_CODE('ctxt')
kQTContextPropertyID_AudioContext = FOUR_CHAR_CODE('audi')
kQTContextPropertyID_VisualContext = FOUR_CHAR_CODE('visu')
kQTPropertyClass_MovieResourceLocator = FOUR_CHAR_CODE('rloc')
kQTMovieResourceLocatorPropertyID_LegacyResID = FOUR_CHAR_CODE('rezi')
kQTMovieResourceLocatorPropertyID_LegacyResName = FOUR_CHAR_CODE('rezn')
kQTMovieResourceLocatorPropertyID_FileOffset = FOUR_CHAR_CODE('foff')
kQTMovieResourceLocatorPropertyID_Callback = FOUR_CHAR_CODE('calb')
kQTPropertyClass_MovieInstantiation = FOUR_CHAR_CODE('mins')
kQTMovieInstantiationPropertyID_DontResolveDataRefs = FOUR_CHAR_CODE('rdrn')
kQTMovieInstantiationPropertyID_DontAskUnresolvedDataRefs = FOUR_CHAR_CODE('aurn')
kQTMovieInstantiationPropertyID_DontAutoAlternates = FOUR_CHAR_CODE('aaln')
kQTMovieInstantiationPropertyID_DontUpdateForeBackPointers = FOUR_CHAR_CODE('fbpn')
kQTMovieInstantiationPropertyID_AsyncOK = FOUR_CHAR_CODE('asok')
kQTMovieInstantiationPropertyID_IdleImportOK = FOUR_CHAR_CODE('imok')
kQTMovieInstantiationPropertyID_DontAutoUpdateClock = FOUR_CHAR_CODE('aucl')
kQTMovieInstantiationPropertyID_ResultDataLocationChanged = FOUR_CHAR_CODE('dlch')
kQTPropertyClass_NewMovieProperty = FOUR_CHAR_CODE('mprp')
kQTNewMoviePropertyID_DefaultDataRef = FOUR_CHAR_CODE('ddrf')
kQTNewMoviePropertyID_Active = FOUR_CHAR_CODE('actv')
kQTNewMoviePropertyID_DontInteractWithUser = FOUR_CHAR_CODE('intn')

class qtlowlevelError(RuntimeError):
    pass


noErr = 0
paramErr = -50
movieToolboxUninitialized = -2020

def GetErrorString(value):
    if value == paramErr:
        return 'paramErr'
    elif value == movieToolboxUninitialized:
        return 'movieToolboxUninitialized'
    elif value != noErr:
        return 'error value: %d' % value
    else:
        return 'noErr'


def CheckOSStatus(value):
    if value != noErr:
        raise qtlowlevelError(GetErrorString(value))
    return value


NewMovieFromFile = QTMLClient.NewMovieFromFile
NewMovieFromProperties = QTMLClient.NewMovieFromProperties
NewMovieFromProperties.restype = CheckOSStatus
NewMovieFromProperties.argtypes = [ItemCount,
 ctypes.POINTER(QTNewMoviePropertyElement),
 ItemCount,
 ctypes.POINTER(QTNewMoviePropertyElement),
 ctypes.POINTER(Movie)]
InitializeQTML = QTMLClient.InitializeQTML
EnterMovies = QTMLClient.EnterMovies
QTGetCFConstant = QTMLClient.QTGetCFConstant
GetMovieBox = QTMLClient.GetMovieBox
GetMovieBox.argtypes = [Movie,
 ctypes.POINTER(Rect)]
SetMovieBox = QTMLClient.SetMovieBox
SetMovieBox.argtypes = [Movie,
 ctypes.POINTER(Rect)]
StartMovie = QTMLClient.StartMovie
StartMovie.argtypes = [Movie]
MoviesTask = QTMLClient.MoviesTask
MoviesTask.argtypes = [Movie, ctypes.c_long]
IsMovieDone = QTMLClient.IsMovieDone
IsMovieDone.argtypes = [Movie]
GoToBeginningOfMovie = QTMLClient.GoToBeginningOfMovie
GoToBeginningOfMovie.argtypes = [Movie]
FSSpec = ctypes.c_void_p
CFStringRef = ctypes.c_void_p
CFStringEncoding = ctypes.c_uint
CFAllocatorRef = ctypes.c_void_p
CFIndex = ctypes.c_int
CFStringCreateWithCharacters = QTMLClient.CFStringCreateWithCharacters
CFStringCreateWithCharacters.restype = CFStringRef
CFStringCreateWithCharacters.argtypes = [CFAllocatorRef,
 ctypes.c_wchar_p,
 CFIndex]
CFStringCreateWithCString = QTMLClient.CFStringCreateWithCString
CFStringCreateWithCString.restype = CFStringRef
CFStringCreateWithCString.argtypes = [CFAllocatorRef,
 ctypes.c_char_p,
 CFStringEncoding]
CFStringGetCString = QTMLClient.CFStringGetCString
CFStringGetCStringPtr = QTMLClient.CFStringGetCStringPtr
CFStringGetCStringPtr.restype = ctypes.c_char_p
NativePathNameToFSSpec = QTMLClient.NativePathNameToFSSpec
NativePathNameToFSSpec.restype = OSErr
NativePathNameToFSSpec.argtypes = [ctypes.c_char_p,
 ctypes.POINTER(FSSpec),
 ctypes.c_long]
OpenMovieFile = QTMLClient.OpenMovieFile
kCFAllocatorDefault = 0
kCFStringEncodingMacRoman = 0
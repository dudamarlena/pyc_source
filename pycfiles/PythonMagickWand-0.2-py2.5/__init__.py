# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PythonMagickWand/__init__.py
# Compiled at: 2008-07-20 15:32:03
"""
PythonMagickWand - Version 0.2dev
(c) 2007 - Achim Domma - domma@procoders.net
http://www.procoders.net

About
-----

I still get a lot requests to update PythonMagick, which is based on
boost.python and is too hard to maintain. So I decided to develop a
ctypes based wrapper for the MagickWand API, which should be enough
to do common image manipulation tasks in python.

This is a very early alpha version which is not tested very well and
will find the ImageMagick library only on a Mac OS X with macports
installed. But for the time beeing it should be easy to adjust the
path to the dll for your system.

Please don't ask questions about how to use the API! I'm not an
ImageMagick expert. Usually I need ImageMagick to do simple things
like resizing of images. You will find mailinglists about ImageMagick
on http://www.imagemagick.org. The documentation of the MagickWand
API can be found on http://www.imagemagick.org/script/magick-wand.php.

The package is licensed under the MIT license.

Any feedback is very welcome!

Achim

Usage
-----

If you import the PythonMagickWand module, it tries to load the ImageMagick
library, which is probably not found on your system. If you get the error
message 'Could not load ImageMagick library' you have to set the environment
variable MAGICK_WAND_LIB to point the library on your system. After that, the
following import should work:

    >>> from PythonMagickWand import *

Now we are ready to create a new wand

    >>> wand = NewMagickWand()

and to load an image from a file.

    >>> MagickReadImage(wand,"sample.jpg") #doctest: +ELLIPSIS
    <MagickBooleanType object at ...>

Let's resize the image

    >>> MagickScaleImage(wand,200,200) #doctest: +ELLIPSIS
    <MagickBooleanType object at ...>

and save it to a new file.

    >>> MagickWriteImage(wand,"out.png") #doctest: +ELLIPSIS
    <MagickBooleanType object at ...>
    >>> 

"""
import os, ctypes
searchPathes = [
 '/opt/local/lib/libMagickWand.dylib',
 '/usr/lib/libWand.so.9']
magickWandLib = os.environ.get('MAGICK_WAND_LIB')
if magickWandLib:
    searchPathes.insert(0, magickWandLib)
_magick = None
for path in searchPathes:
    try:
        _magick = ctypes.CDLL(path)
    except OSError:
        pass

    if _magick != None:
        break

if _magick == None:
    raise RuntimeError('Could not find ImageMagick library.')
_magick.MagickWandGenesis()

class MetricType(ctypes.c_int):
    pass


UndefinedMetric = MetricType(0)
AbsoluteErrorMetric = MetricType(1)
MeanAbsoluteErrorMetric = MetricType(2)
MeanErrorPerPixelMetric = MetricType(3)
MeanSquaredErrorMetric = MetricType(4)
PeakAbsoluteErrorMetric = MetricType(5)
PeakSignalToNoiseRatioMetric = MetricType(6)
RootMeanSquaredErrorMetric = MetricType(7)

class NoiseType(ctypes.c_int):
    pass


UndefinedNoise = NoiseType(0)
UniformNoise = NoiseType(1)
GaussianNoise = NoiseType(2)
MultiplicativeGaussianNoise = NoiseType(3)
ImpulseNoise = NoiseType(4)
LaplacianNoise = NoiseType(5)
PoissonNoise = NoiseType(6)
RandomNoise = NoiseType(7)

class ImageLayerMethod(ctypes.c_int):
    pass


UndefinedLayer = ImageLayerMethod(0)
CoalesceLayer = ImageLayerMethod(1)
CompareAnyLayer = ImageLayerMethod(2)
CompareClearLayer = ImageLayerMethod(3)
CompareOverlayLayer = ImageLayerMethod(4)
DisposeLayer = ImageLayerMethod(5)
OptimizeLayer = ImageLayerMethod(6)
OptimizeImageLayer = ImageLayerMethod(7)
OptimizePlusLayer = ImageLayerMethod(8)
OptimizeTransLayer = ImageLayerMethod(9)
RemoveDupsLayer = ImageLayerMethod(10)
RemoveZeroLayer = ImageLayerMethod(11)
CompositeLayer = ImageLayerMethod(12)
MergeLayer = ImageLayerMethod(13)
FlattenLayer = ImageLayerMethod(14)
MosaicLayer = ImageLayerMethod(15)

class MagickOption(ctypes.c_int):
    pass


MagickUndefinedOptions = MagickOption(-1)
MagickAlignOptions = MagickOption(0)
MagickAlphaOptions = MagickOption(1)
MagickBooleanOptions = MagickOption(2)
MagickChannelOptions = MagickOption(3)
MagickClassOptions = MagickOption(4)
MagickClipPathOptions = MagickOption(5)
MagickColorspaceOptions = MagickOption(6)
MagickCommandOptions = MagickOption(7)
MagickComposeOptions = MagickOption(8)
MagickCompressOptions = MagickOption(9)
MagickDataTypeOptions = MagickOption(10)
MagickDebugOptions = MagickOption(11)
MagickDecorateOptions = MagickOption(12)
MagickDisposeOptions = MagickOption(13)
MagickDistortOptions = MagickOption(14)
MagickEndianOptions = MagickOption(15)
MagickEvaluateOptions = MagickOption(16)
MagickFillRuleOptions = MagickOption(17)
MagickFilterOptions = MagickOption(18)
MagickFontsOptions = MagickOption(19)
MagickGravityOptions = MagickOption(20)
MagickIntentOptions = MagickOption(21)
MagickInterlaceOptions = MagickOption(22)
MagickInterpolateOptions = MagickOption(23)
MagickLayerOptions = MagickOption(24)
MagickLineCapOptions = MagickOption(25)
MagickLineJoinOptions = MagickOption(26)
MagickListOptions = MagickOption(27)
MagickLogEventOptions = MagickOption(28)
MagickMetricOptions = MagickOption(29)
MagickMethodOptions = MagickOption(30)
MagickModeOptions = MagickOption(31)
MagickMogrifyOptions = MagickOption(32)
MagickNoiseOptions = MagickOption(33)
MagickOrientationOptions = MagickOption(34)
MagickPreviewOptions = MagickOption(35)
MagickPrimitiveOptions = MagickOption(36)
MagickQuantumFormatOptions = MagickOption(37)
MagickResolutionOptions = MagickOption(38)
MagickResourceOptions = MagickOption(39)
MagickStorageOptions = MagickOption(40)
MagickStretchOptions = MagickOption(41)
MagickStyleOptions = MagickOption(42)
MagickTypeOptions = MagickOption(43)
MagickVirtualPixelOptions = MagickOption(44)
MagickCoderOptions = MagickOption(45)
MagickColorOptions = MagickOption(46)
MagickConfigureOptions = MagickOption(47)
MagickDelegateOptions = MagickOption(48)
MagickFontOptions = MagickOption(49)
MagickFormatOptions = MagickOption(50)
MagickMimeOptions = MagickOption(51)
MagickLocaleOptions = MagickOption(52)
MagickLogOptions = MagickOption(53)
MagickMagicOptions = MagickOption(54)
MagickModuleOptions = MagickOption(55)
MagickThresholdOptions = MagickOption(56)

class StretchType(ctypes.c_int):
    pass


UndefinedStretch = StretchType(0)
NormalStretch = StretchType(1)
UltraCondensedStretch = StretchType(2)
ExtraCondensedStretch = StretchType(3)
CondensedStretch = StretchType(4)
SemiCondensedStretch = StretchType(5)
SemiExpandedStretch = StretchType(6)
ExpandedStretch = StretchType(7)
ExtraExpandedStretch = StretchType(8)
UltraExpandedStretch = StretchType(9)
AnyStretch = StretchType(10)

class StyleType(ctypes.c_int):
    pass


UndefinedStyle = StyleType(0)
NormalStyle = StyleType(1)
ItalicStyle = StyleType(2)
ObliqueStyle = StyleType(3)
AnyStyle = StyleType(4)

class LineJoin(ctypes.c_int):
    pass


UndefinedJoin = LineJoin(0)
MiterJoin = LineJoin(1)
RoundJoin = LineJoin(2)
BevelJoin = LineJoin(3)

class PaintMethod(ctypes.c_int):
    pass


UndefinedMethod = PaintMethod(0)
PointMethod = PaintMethod(1)
ReplaceMethod = PaintMethod(2)
FloodfillMethod = PaintMethod(3)
FillToBorderMethod = PaintMethod(4)
ResetMethod = PaintMethod(5)

class AlphaChannelType(ctypes.c_int):
    pass


UndefinedAlphaChannel = AlphaChannelType(0)
ActivateAlphaChannel = AlphaChannelType(1)
DeactivateAlphaChannel = AlphaChannelType(2)
ResetAlphaChannel = AlphaChannelType(3)
SetAlphaChannel = AlphaChannelType(4)

class CompositeOperator(ctypes.c_int):
    pass


UndefinedCompositeOp = CompositeOperator(0)
NoCompositeOp = CompositeOperator(1)
AddCompositeOp = CompositeOperator(2)
AtopCompositeOp = CompositeOperator(3)
BlendCompositeOp = CompositeOperator(4)
BumpmapCompositeOp = CompositeOperator(5)
ChangeMaskCompositeOp = CompositeOperator(6)
ClearCompositeOp = CompositeOperator(7)
ColorBurnCompositeOp = CompositeOperator(8)
ColorDodgeCompositeOp = CompositeOperator(9)
ColorizeCompositeOp = CompositeOperator(10)
CopyBlackCompositeOp = CompositeOperator(11)
CopyBlueCompositeOp = CompositeOperator(12)
CopyCompositeOp = CompositeOperator(13)
CopyCyanCompositeOp = CompositeOperator(14)
CopyGreenCompositeOp = CompositeOperator(15)
CopyMagentaCompositeOp = CompositeOperator(16)
CopyOpacityCompositeOp = CompositeOperator(17)
CopyRedCompositeOp = CompositeOperator(18)
CopyYellowCompositeOp = CompositeOperator(19)
DarkenCompositeOp = CompositeOperator(20)
DstAtopCompositeOp = CompositeOperator(21)
DstCompositeOp = CompositeOperator(22)
DstInCompositeOp = CompositeOperator(23)
DstOutCompositeOp = CompositeOperator(24)
DstOverCompositeOp = CompositeOperator(25)
DifferenceCompositeOp = CompositeOperator(26)
DisplaceCompositeOp = CompositeOperator(27)
DissolveCompositeOp = CompositeOperator(28)
ExclusionCompositeOp = CompositeOperator(29)
HardLightCompositeOp = CompositeOperator(30)
HueCompositeOp = CompositeOperator(31)
InCompositeOp = CompositeOperator(32)
LightenCompositeOp = CompositeOperator(33)
LinearLightCompositeOp = CompositeOperator(34)
LuminizeCompositeOp = CompositeOperator(35)
MinusCompositeOp = CompositeOperator(36)
ModulateCompositeOp = CompositeOperator(37)
MultiplyCompositeOp = CompositeOperator(38)
OutCompositeOp = CompositeOperator(39)
OverCompositeOp = CompositeOperator(40)
OverlayCompositeOp = CompositeOperator(41)
PlusCompositeOp = CompositeOperator(42)
ReplaceCompositeOp = CompositeOperator(43)
SaturateCompositeOp = CompositeOperator(44)
ScreenCompositeOp = CompositeOperator(45)
SoftLightCompositeOp = CompositeOperator(46)
SrcAtopCompositeOp = CompositeOperator(47)
SrcCompositeOp = CompositeOperator(48)
SrcInCompositeOp = CompositeOperator(49)
SrcOutCompositeOp = CompositeOperator(50)
SrcOverCompositeOp = CompositeOperator(51)
SubtractCompositeOp = CompositeOperator(52)
ThresholdCompositeOp = CompositeOperator(53)
XorCompositeOp = CompositeOperator(54)
DivideCompositeOp = CompositeOperator(55)

class CompressionType(ctypes.c_int):
    pass


UndefinedCompression = CompressionType(0)
NoCompression = CompressionType(1)
BZipCompression = CompressionType(2)
FaxCompression = CompressionType(3)
Group4Compression = CompressionType(4)
JPEGCompression = CompressionType(5)
JPEG2000Compression = CompressionType(6)
LosslessJPEGCompression = CompressionType(7)
LZWCompression = CompressionType(8)
RLECompression = CompressionType(9)
ZipCompression = CompressionType(10)

class LineCap(ctypes.c_int):
    pass


UndefinedCap = LineCap(0)
ButtCap = LineCap(1)
RoundCap = LineCap(2)
SquareCap = LineCap(3)

class GravityType(ctypes.c_int):
    pass


UndefinedGravity = GravityType(0)
ForgetGravity = GravityType(0)
NorthWestGravity = GravityType(1)
NorthGravity = GravityType(2)
NorthEastGravity = GravityType(3)
WestGravity = GravityType(4)
CenterGravity = GravityType(5)
EastGravity = GravityType(6)
SouthWestGravity = GravityType(7)
SouthGravity = GravityType(8)
SouthEastGravity = GravityType(9)
StaticGravity = GravityType(10)

class RegistryType(ctypes.c_int):
    pass


UndefinedRegistryType = RegistryType(0)
ImageRegistryType = RegistryType(1)
ImageInfoRegistryType = RegistryType(2)
StringRegistryType = RegistryType(3)

class MontageMode(ctypes.c_int):
    pass


UndefinedMode = MontageMode(0)
FrameMode = MontageMode(1)
UnframeMode = MontageMode(2)
ConcatenateMode = MontageMode(3)

class ClipPathUnits(ctypes.c_int):
    pass


UndefinedPathUnits = ClipPathUnits(0)
UserSpace = ClipPathUnits(1)
UserSpaceOnUse = ClipPathUnits(2)
ObjectBoundingBox = ClipPathUnits(3)

class AlignType(ctypes.c_int):
    pass


UndefinedAlign = AlignType(0)
LeftAlign = AlignType(1)
CenterAlign = AlignType(2)
RightAlign = AlignType(3)

class ResolutionType(ctypes.c_int):
    pass


UndefinedResolution = ResolutionType(0)
PixelsPerInchResolution = ResolutionType(1)
PixelsPerCentimeterResolution = ResolutionType(2)

class OrientationType(ctypes.c_int):
    pass


UndefinedOrientation = OrientationType(0)
TopLeftOrientation = OrientationType(1)
TopRightOrientation = OrientationType(2)
BottomRightOrientation = OrientationType(3)
BottomLeftOrientation = OrientationType(4)
LeftTopOrientation = OrientationType(5)
RightTopOrientation = OrientationType(6)
RightBottomOrientation = OrientationType(7)
LeftBottomOrientation = OrientationType(8)

class InterlaceType(ctypes.c_int):
    pass


UndefinedInterlace = InterlaceType(0)
NoInterlace = InterlaceType(1)
LineInterlace = InterlaceType(2)
PlaneInterlace = InterlaceType(3)
PartitionInterlace = InterlaceType(4)
GIFInterlace = InterlaceType(5)
JPEGInterlace = InterlaceType(6)
PNGInterlace = InterlaceType(7)

class ImageType(ctypes.c_int):
    pass


UndefinedType = ImageType(0)
BilevelType = ImageType(1)
GrayscaleType = ImageType(2)
GrayscaleMatteType = ImageType(3)
PaletteType = ImageType(4)
PaletteMatteType = ImageType(5)
TrueColorType = ImageType(6)
TrueColorMatteType = ImageType(7)
ColorSeparationType = ImageType(8)
ColorSeparationMatteType = ImageType(9)
OptimizeType = ImageType(10)
PaletteBilevelMatteType = ImageType(11)

class LogEventType(ctypes.c_int):
    pass


UndefinedEvents = LogEventType(0)
NoEvents = LogEventType(0)
TraceEvent = LogEventType(1)
AnnotateEvent = LogEventType(2)
BlobEvent = LogEventType(4)
CacheEvent = LogEventType(8)
CoderEvent = LogEventType(16)
ConfigureEvent = LogEventType(32)
DeprecateEvent = LogEventType(64)
DrawEvent = LogEventType(128)
ExceptionEvent = LogEventType(256)
LocaleEvent = LogEventType(512)
ModuleEvent = LogEventType(1024)
ResourceEvent = LogEventType(2048)
TransformEvent = LogEventType(4096)
UserEvent = LogEventType(8192)
WandEvent = LogEventType(16384)
X11Event = LogEventType(32768)
AllEvents = LogEventType(2147483647)

class StorageType(ctypes.c_int):
    pass


UndefinedPixel = StorageType(0)
CharPixel = StorageType(1)
DoublePixel = StorageType(2)
FloatPixel = StorageType(3)
IntegerPixel = StorageType(4)
LongPixel = StorageType(5)
QuantumPixel = StorageType(6)
ShortPixel = StorageType(7)

class ColorspaceType(ctypes.c_int):
    pass


UndefinedColorspace = ColorspaceType(0)
RGBColorspace = ColorspaceType(1)
GRAYColorspace = ColorspaceType(2)
TransparentColorspace = ColorspaceType(3)
OHTAColorspace = ColorspaceType(4)
LabColorspace = ColorspaceType(5)
XYZColorspace = ColorspaceType(6)
YCbCrColorspace = ColorspaceType(7)
YCCColorspace = ColorspaceType(8)
YIQColorspace = ColorspaceType(9)
YPbPrColorspace = ColorspaceType(10)
YUVColorspace = ColorspaceType(11)
CMYKColorspace = ColorspaceType(12)
sRGBColorspace = ColorspaceType(13)
HSBColorspace = ColorspaceType(14)
HSLColorspace = ColorspaceType(15)
HWBColorspace = ColorspaceType(16)
Rec601LumaColorspace = ColorspaceType(17)
Rec601YCbCrColorspace = ColorspaceType(18)
Rec709LumaColorspace = ColorspaceType(19)
Rec709YCbCrColorspace = ColorspaceType(20)
LogColorspace = ColorspaceType(21)
CMYColorspace = ColorspaceType(22)

class InterpolatePixelMethod(ctypes.c_int):
    pass


UndefinedInterpolatePixel = InterpolatePixelMethod(0)
AverageInterpolatePixel = InterpolatePixelMethod(1)
BicubicInterpolatePixel = InterpolatePixelMethod(2)
BilinearInterpolatePixel = InterpolatePixelMethod(3)
FilterInterpolatePixel = InterpolatePixelMethod(4)
IntegerInterpolatePixel = InterpolatePixelMethod(5)
MeshInterpolatePixel = InterpolatePixelMethod(6)
NearestNeighborInterpolatePixel = InterpolatePixelMethod(7)
SplineInterpolatePixel = InterpolatePixelMethod(8)

class MagickEvaluateOperator(ctypes.c_int):
    pass


UndefinedEvaluateOperator = MagickEvaluateOperator(0)
AddEvaluateOperator = MagickEvaluateOperator(1)
AndEvaluateOperator = MagickEvaluateOperator(2)
DivideEvaluateOperator = MagickEvaluateOperator(3)
LeftShiftEvaluateOperator = MagickEvaluateOperator(4)
MaxEvaluateOperator = MagickEvaluateOperator(5)
MinEvaluateOperator = MagickEvaluateOperator(6)
MultiplyEvaluateOperator = MagickEvaluateOperator(7)
OrEvaluateOperator = MagickEvaluateOperator(8)
RightShiftEvaluateOperator = MagickEvaluateOperator(9)
SetEvaluateOperator = MagickEvaluateOperator(10)
SubtractEvaluateOperator = MagickEvaluateOperator(11)
XorEvaluateOperator = MagickEvaluateOperator(12)

class ExceptionType(ctypes.c_int):
    pass


UndefinedException = ExceptionType(0)
WarningException = ExceptionType(300)
ResourceLimitWarning = ExceptionType(300)
TypeWarning = ExceptionType(305)
OptionWarning = ExceptionType(310)
DelegateWarning = ExceptionType(315)
MissingDelegateWarning = ExceptionType(320)
CorruptImageWarning = ExceptionType(325)
FileOpenWarning = ExceptionType(330)
BlobWarning = ExceptionType(335)
StreamWarning = ExceptionType(340)
CacheWarning = ExceptionType(345)
CoderWarning = ExceptionType(350)
ModuleWarning = ExceptionType(355)
DrawWarning = ExceptionType(360)
ImageWarning = ExceptionType(365)
WandWarning = ExceptionType(370)
XServerWarning = ExceptionType(380)
MonitorWarning = ExceptionType(385)
RegistryWarning = ExceptionType(390)
ConfigureWarning = ExceptionType(395)
ErrorException = ExceptionType(400)
ResourceLimitError = ExceptionType(400)
TypeError = ExceptionType(405)
OptionError = ExceptionType(410)
DelegateError = ExceptionType(415)
MissingDelegateError = ExceptionType(420)
CorruptImageError = ExceptionType(425)
FileOpenError = ExceptionType(430)
BlobError = ExceptionType(435)
StreamError = ExceptionType(440)
CacheError = ExceptionType(445)
CoderError = ExceptionType(450)
ModuleError = ExceptionType(455)
DrawError = ExceptionType(460)
ImageError = ExceptionType(465)
WandError = ExceptionType(470)
XServerError = ExceptionType(480)
MonitorError = ExceptionType(485)
RegistryError = ExceptionType(490)
ConfigureError = ExceptionType(495)
FatalErrorException = ExceptionType(700)
ResourceLimitFatalError = ExceptionType(700)
TypeFatalError = ExceptionType(705)
OptionFatalError = ExceptionType(710)
DelegateFatalError = ExceptionType(715)
MissingDelegateFatalError = ExceptionType(720)
CorruptImageFatalError = ExceptionType(725)
FileOpenFatalError = ExceptionType(730)
BlobFatalError = ExceptionType(735)
StreamFatalError = ExceptionType(740)
CacheFatalError = ExceptionType(745)
CoderFatalError = ExceptionType(750)
ModuleFatalError = ExceptionType(755)
DrawFatalError = ExceptionType(760)
ImageFatalError = ExceptionType(765)
WandFatalError = ExceptionType(770)
XServerFatalError = ExceptionType(780)
MonitorFatalError = ExceptionType(785)
RegistryFatalError = ExceptionType(790)
ConfigureFatalError = ExceptionType(795)

class ChannelType(ctypes.c_int):
    pass


UndefinedChannel = ChannelType(0)
RedChannel = ChannelType(1)
GrayChannel = ChannelType(1)
CyanChannel = ChannelType(1)
GreenChannel = ChannelType(2)
MagentaChannel = ChannelType(2)
BlueChannel = ChannelType(4)
YellowChannel = ChannelType(4)
AlphaChannel = ChannelType(8)
OpacityChannel = ChannelType(8)
MatteChannel = ChannelType(8)
BlackChannel = ChannelType(32)
IndexChannel = ChannelType(32)
AllChannels = ChannelType(255)
DefaultChannels = ChannelType(247)

class DistortImageMethod(ctypes.c_int):
    pass


UndefinedDistortion = DistortImageMethod(0)
AffineDistortion = DistortImageMethod(1)
AffineProjectionDistortion = DistortImageMethod(2)
ArcDistortion = DistortImageMethod(3)
BilinearDistortion = DistortImageMethod(4)
PerspectiveDistortion = DistortImageMethod(5)
PerspectiveProjectionDistortion = DistortImageMethod(6)
ScaleRotateTranslateDistortion = DistortImageMethod(7)

class FillRule(ctypes.c_int):
    pass


UndefinedRule = FillRule(0)
EvenOddRule = FillRule(1)
NonZeroRule = FillRule(2)

class DecorationType(ctypes.c_int):
    pass


UndefinedDecoration = DecorationType(0)
NoDecoration = DecorationType(1)
UnderlineDecoration = DecorationType(2)
OverlineDecoration = DecorationType(3)
LineThroughDecoration = DecorationType(4)

class FilterTypes(ctypes.c_int):
    pass


UndefinedFilter = FilterTypes(0)
PointFilter = FilterTypes(1)
BoxFilter = FilterTypes(2)
TriangleFilter = FilterTypes(3)
HermiteFilter = FilterTypes(4)
HanningFilter = FilterTypes(5)
HammingFilter = FilterTypes(6)
BlackmanFilter = FilterTypes(7)
GaussianFilter = FilterTypes(8)
QuadraticFilter = FilterTypes(9)
CubicFilter = FilterTypes(10)
CatromFilter = FilterTypes(11)
MitchellFilter = FilterTypes(12)
LanczosFilter = FilterTypes(13)
BesselFilter = FilterTypes(14)
SincFilter = FilterTypes(15)
KaiserFilter = FilterTypes(16)
WelshFilter = FilterTypes(17)
ParzenFilter = FilterTypes(18)
LagrangeFilter = FilterTypes(19)
BohmanFilter = FilterTypes(20)
BartlettFilter = FilterTypes(21)
SentinelFilter = FilterTypes(22)

class VirtualPixelMethod(ctypes.c_int):
    pass


UndefinedVirtualPixelMethod = VirtualPixelMethod(0)
BackgroundVirtualPixelMethod = VirtualPixelMethod(1)
ConstantVirtualPixelMethod = VirtualPixelMethod(2)
DitherVirtualPixelMethod = VirtualPixelMethod(3)
EdgeVirtualPixelMethod = VirtualPixelMethod(4)
MirrorVirtualPixelMethod = VirtualPixelMethod(5)
RandomVirtualPixelMethod = VirtualPixelMethod(6)
TileVirtualPixelMethod = VirtualPixelMethod(7)
TransparentVirtualPixelMethod = VirtualPixelMethod(8)
MaskVirtualPixelMethod = VirtualPixelMethod(9)
BlackVirtualPixelMethod = VirtualPixelMethod(10)
GrayVirtualPixelMethod = VirtualPixelMethod(11)
WhiteVirtualPixelMethod = VirtualPixelMethod(12)

class DisposeType(ctypes.c_int):
    pass


UnrecognizedDispose = DisposeType(0)
UndefinedDispose = DisposeType(0)
NoneDispose = DisposeType(1)
BackgroundDispose = DisposeType(2)
PreviousDispose = DisposeType(3)

class MagickBooleanType(ctypes.c_int):
    pass


MagickFalse = MagickBooleanType(0)
MagickTrue = MagickBooleanType(1)

class PreviewType(ctypes.c_int):
    pass


UndefinedPreview = PreviewType(0)
RotatePreview = PreviewType(1)
ShearPreview = PreviewType(2)
RollPreview = PreviewType(3)
HuePreview = PreviewType(4)
SaturationPreview = PreviewType(5)
BrightnessPreview = PreviewType(6)
GammaPreview = PreviewType(7)
SpiffPreview = PreviewType(8)
DullPreview = PreviewType(9)
GrayscalePreview = PreviewType(10)
QuantizePreview = PreviewType(11)
DespecklePreview = PreviewType(12)
ReduceNoisePreview = PreviewType(13)
AddNoisePreview = PreviewType(14)
SharpenPreview = PreviewType(15)
BlurPreview = PreviewType(16)
ThresholdPreview = PreviewType(17)
EdgeDetectPreview = PreviewType(18)
SpreadPreview = PreviewType(19)
SolarizePreview = PreviewType(20)
ShadePreview = PreviewType(21)
RaisePreview = PreviewType(22)
SegmentPreview = PreviewType(23)
SwirlPreview = PreviewType(24)
ImplodePreview = PreviewType(25)
WavePreview = PreviewType(26)
OilPaintPreview = PreviewType(27)
CharcoalDrawingPreview = PreviewType(28)
JPEGPreview = PreviewType(29)

class RenderingIntent(ctypes.c_int):
    pass


UndefinedIntent = RenderingIntent(0)
SaturationIntent = RenderingIntent(1)
PerceptualIntent = RenderingIntent(2)
AbsoluteIntent = RenderingIntent(3)
RelativeIntent = RenderingIntent(4)

class ResourceType(ctypes.c_int):
    pass


UndefinedResource = ResourceType(0)
AreaResource = ResourceType(1)
DiskResource = ResourceType(2)
FileResource = ResourceType(3)
MapResource = ResourceType(4)
MemoryResource = ResourceType(5)

class ExceptionType(ctypes.c_int):
    pass


UndefinedException = ExceptionType(0)
WarningException = ExceptionType(300)
ResourceLimitWarning = ExceptionType(300)
TypeWarning = ExceptionType(305)
OptionWarning = ExceptionType(310)
DelegateWarning = ExceptionType(315)
MissingDelegateWarning = ExceptionType(320)
CorruptImageWarning = ExceptionType(325)
FileOpenWarning = ExceptionType(330)
BlobWarning = ExceptionType(335)
StreamWarning = ExceptionType(340)
CacheWarning = ExceptionType(345)
CoderWarning = ExceptionType(350)
ModuleWarning = ExceptionType(355)
DrawWarning = ExceptionType(360)
ImageWarning = ExceptionType(365)
WandWarning = ExceptionType(370)
XServerWarning = ExceptionType(380)
MonitorWarning = ExceptionType(385)
RegistryWarning = ExceptionType(390)
ConfigureWarning = ExceptionType(395)
ErrorException = ExceptionType(400)
ResourceLimitError = ExceptionType(400)
TypeError = ExceptionType(405)
OptionError = ExceptionType(410)
DelegateError = ExceptionType(415)
MissingDelegateError = ExceptionType(420)
CorruptImageError = ExceptionType(425)
FileOpenError = ExceptionType(430)
BlobError = ExceptionType(435)
StreamError = ExceptionType(440)
CacheError = ExceptionType(445)
CoderError = ExceptionType(450)
ModuleError = ExceptionType(455)
DrawError = ExceptionType(460)
ImageError = ExceptionType(465)
WandError = ExceptionType(470)
XServerError = ExceptionType(480)
MonitorError = ExceptionType(485)
RegistryError = ExceptionType(490)
ConfigureError = ExceptionType(495)
FatalErrorException = ExceptionType(700)
ResourceLimitFatalError = ExceptionType(700)
TypeFatalError = ExceptionType(705)
OptionFatalError = ExceptionType(710)
DelegateFatalError = ExceptionType(715)
MissingDelegateFatalError = ExceptionType(720)
CorruptImageFatalError = ExceptionType(725)
FileOpenFatalError = ExceptionType(730)
BlobFatalError = ExceptionType(735)
StreamFatalError = ExceptionType(740)
CacheFatalError = ExceptionType(745)
CoderFatalError = ExceptionType(750)
ModuleFatalError = ExceptionType(755)
DrawFatalError = ExceptionType(760)
ImageFatalError = ExceptionType(765)
WandFatalError = ExceptionType(770)
XServerFatalError = ExceptionType(780)
MonitorFatalError = ExceptionType(785)
RegistryFatalError = ExceptionType(790)
ConfigureFatalError = ExceptionType(795)

class ComplianceType(ctypes.c_int):
    pass


UndefinedCompliance = ComplianceType(0)
NoCompliance = ComplianceType(0)
SVGCompliance = ComplianceType(1)
X11Compliance = ComplianceType(2)
XPMCompliance = ComplianceType(4)
AllCompliance = ComplianceType(2147483647)

class RegistryType(ctypes.c_int):
    pass


UndefinedRegistryType = RegistryType(0)
ImageRegistryType = RegistryType(1)
ImageInfoRegistryType = RegistryType(2)
StringRegistryType = RegistryType(3)

class FILE(ctypes.c_void_p):
    pass


class MagickPixelPacket(ctypes.c_void_p):
    pass


class PixelWand(ctypes.c_void_p):
    pass


class TypeMetric(ctypes.c_void_p):
    pass


class PrimitiveInfo(ctypes.c_void_p):
    pass


class size_t(ctypes.c_void_p):
    pass


class AffineMatrix(ctypes.c_void_p):
    pass


class DrawInfo(ctypes.c_void_p):
    pass


class MagickProgressMonitor(ctypes.c_void_p):
    pass


class PointInfo(ctypes.c_void_p):
    pass


class DrawingWand(ctypes.c_void_p):
    pass


class Image(ctypes.c_void_p):
    pass


class ChannelStatistics(ctypes.c_void_p):
    pass


class MagickSizeType(ctypes.c_void_p):
    pass


class ImageInfo(ctypes.c_void_p):
    pass


class ExceptionInfo(ctypes.c_void_p):
    pass


class MagickStatusType(ctypes.c_void_p):
    pass


class MagickInfo(ctypes.c_void_p):
    pass


class MagickWand(ctypes.c_void_p):
    pass


try:
    _magick.MagickSetLastIterator.restype = None
    _magick.MagickSetLastIterator.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickSetLastIterator = _magick.MagickSetLastIterator

try:
    _magick.MagickSetFirstIterator.restype = None
    _magick.MagickSetFirstIterator.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickSetFirstIterator = _magick.MagickSetFirstIterator

try:
    _magick.MagickResetIterator.restype = None
    _magick.MagickResetIterator.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickResetIterator = _magick.MagickResetIterator

try:
    _magick.MagickRelinquishMemory.restype = ctypes.c_void_p
    _magick.MagickRelinquishMemory.argtypes = (ctypes.c_void_p,)
except AttributeError, e:
    print e
else:
    MagickRelinquishMemory = _magick.MagickRelinquishMemory

try:
    _magick.MagickWandTerminus.restype = None
    _magick.MagickWandTerminus.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickWandTerminus = _magick.MagickWandTerminus

try:
    _magick.MagickWandGenesis.restype = None
    _magick.MagickWandGenesis.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickWandGenesis = _magick.MagickWandGenesis

try:
    _magick.ClearMagickWand.restype = None
    _magick.ClearMagickWand.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    ClearMagickWand = _magick.ClearMagickWand

try:
    _magick.NewMagickWand.restype = MagickWand
    _magick.NewMagickWand.argtypes = ()
except AttributeError, e:
    print e
else:
    NewMagickWand = _magick.NewMagickWand

try:
    _magick.DestroyMagickWand.restype = MagickWand
    _magick.DestroyMagickWand.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    DestroyMagickWand = _magick.DestroyMagickWand

try:
    _magick.CloneMagickWand.restype = MagickWand
    _magick.CloneMagickWand.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    CloneMagickWand = _magick.CloneMagickWand

try:
    _magick.MagickSetIteratorIndex.restype = MagickBooleanType
    _magick.MagickSetIteratorIndex.argtypes = (MagickWand, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetIteratorIndex = _magick.MagickSetIteratorIndex

try:
    _magick.MagickClearException.restype = MagickBooleanType
    _magick.MagickClearException.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickClearException = _magick.MagickClearException

try:
    _magick.IsMagickWand.restype = MagickBooleanType
    _magick.IsMagickWand.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    IsMagickWand = _magick.IsMagickWand

try:
    _magick.MagickGetIteratorIndex.restype = ctypes.c_long
    _magick.MagickGetIteratorIndex.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetIteratorIndex = _magick.MagickGetIteratorIndex

try:
    _magick.MagickGetExceptionType.restype = ExceptionType
    _magick.MagickGetExceptionType.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetExceptionType = _magick.MagickGetExceptionType

try:
    _magick.MagickGetException.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetException.argtypes = (MagickWand, ctypes.POINTER(ExceptionType))
except AttributeError, e:
    print e
else:
    MagickGetException = _magick.MagickGetException

try:
    _magick.MagickGetImageVirtualPixelMethod.restype = VirtualPixelMethod
    _magick.MagickGetImageVirtualPixelMethod.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageVirtualPixelMethod = _magick.MagickGetImageVirtualPixelMethod

try:
    _magick.MagickGetNumberImages.restype = ctypes.c_ulong
    _magick.MagickGetNumberImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetNumberImages = _magick.MagickGetNumberImages

try:
    _magick.MagickGetImageWidth.restype = ctypes.c_ulong
    _magick.MagickGetImageWidth.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageWidth = _magick.MagickGetImageWidth

try:
    _magick.MagickGetImageTicksPerSecond.restype = ctypes.c_ulong
    _magick.MagickGetImageTicksPerSecond.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageTicksPerSecond = _magick.MagickGetImageTicksPerSecond

try:
    _magick.MagickGetImageScene.restype = ctypes.c_ulong
    _magick.MagickGetImageScene.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageScene = _magick.MagickGetImageScene

try:
    _magick.MagickGetImageIterations.restype = ctypes.c_ulong
    _magick.MagickGetImageIterations.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageIterations = _magick.MagickGetImageIterations

try:
    _magick.MagickGetImageHeight.restype = ctypes.c_ulong
    _magick.MagickGetImageHeight.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageHeight = _magick.MagickGetImageHeight

try:
    _magick.MagickGetImageDepth.restype = ctypes.c_ulong
    _magick.MagickGetImageDepth.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageDepth = _magick.MagickGetImageDepth

try:
    _magick.MagickGetImageChannelDepth.restype = ctypes.c_ulong
    _magick.MagickGetImageChannelDepth.argtypes = (MagickWand, ChannelType)
except AttributeError, e:
    print e
else:
    MagickGetImageChannelDepth = _magick.MagickGetImageChannelDepth

try:
    _magick.MagickGetImageDelay.restype = ctypes.c_ulong
    _magick.MagickGetImageDelay.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageDelay = _magick.MagickGetImageDelay

try:
    _magick.MagickGetImageCompressionQuality.restype = ctypes.c_ulong
    _magick.MagickGetImageCompressionQuality.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageCompressionQuality = _magick.MagickGetImageCompressionQuality

try:
    _magick.MagickGetImageColors.restype = ctypes.c_ulong
    _magick.MagickGetImageColors.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageColors = _magick.MagickGetImageColors

try:
    _magick.MagickGetImagesBlob.restype = ctypes.POINTER(ctypes.c_ubyte)
    _magick.MagickGetImagesBlob.argtypes = (MagickWand, size_t)
except AttributeError, e:
    print e
else:
    MagickGetImagesBlob = _magick.MagickGetImagesBlob

try:
    _magick.MagickGetImageBlob.restype = ctypes.POINTER(ctypes.c_ubyte)
    _magick.MagickGetImageBlob.argtypes = (MagickWand, size_t)
except AttributeError, e:
    print e
else:
    MagickGetImageBlob = _magick.MagickGetImageBlob

try:
    _magick.MagickGetImageUnits.restype = ResolutionType
    _magick.MagickGetImageUnits.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageUnits = _magick.MagickGetImageUnits

try:
    _magick.MagickGetImageRenderingIntent.restype = RenderingIntent
    _magick.MagickGetImageRenderingIntent.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageRenderingIntent = _magick.MagickGetImageRenderingIntent

try:
    _magick.MagickGetImageHistogram.restype = ctypes.POINTER(PixelWand)
    _magick.MagickGetImageHistogram.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetImageHistogram = _magick.MagickGetImageHistogram

try:
    _magick.MagickGetImageOrientation.restype = OrientationType
    _magick.MagickGetImageOrientation.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageOrientation = _magick.MagickGetImageOrientation

try:
    _magick.NewMagickWandFromImage.restype = MagickWand
    _magick.NewMagickWandFromImage.argtypes = (Image,)
except AttributeError, e:
    print e
else:
    NewMagickWandFromImage = _magick.NewMagickWandFromImage

try:
    _magick.MagickTransformImage.restype = MagickWand
    _magick.MagickTransformImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickTransformImage = _magick.MagickTransformImage

try:
    _magick.MagickTextureImage.restype = MagickWand
    _magick.MagickTextureImage.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickTextureImage = _magick.MagickTextureImage

try:
    _magick.MagickStereoImage.restype = MagickWand
    _magick.MagickStereoImage.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickStereoImage = _magick.MagickStereoImage

try:
    _magick.MagickSteganoImage.restype = MagickWand
    _magick.MagickSteganoImage.argtypes = (MagickWand, MagickWand, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSteganoImage = _magick.MagickSteganoImage

try:
    _magick.MagickPreviewImages.restype = MagickWand
    _magick.MagickPreviewImages.argtypes = (MagickWand, PreviewType)
except AttributeError, e:
    print e
else:
    MagickPreviewImages = _magick.MagickPreviewImages

try:
    _magick.MagickOptimizeImageLayers.restype = MagickWand
    _magick.MagickOptimizeImageLayers.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickOptimizeImageLayers = _magick.MagickOptimizeImageLayers

try:
    _magick.MagickMontageImage.restype = MagickWand
    _magick.MagickMontageImage.argtypes = (MagickWand, DrawingWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), MontageMode, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickMontageImage = _magick.MagickMontageImage

try:
    _magick.MagickMorphImages.restype = MagickWand
    _magick.MagickMorphImages.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickMorphImages = _magick.MagickMorphImages

try:
    _magick.MagickMergeImageLayers.restype = MagickWand
    _magick.MagickMergeImageLayers.argtypes = (MagickWand, ImageLayerMethod)
except AttributeError, e:
    print e
else:
    MagickMergeImageLayers = _magick.MagickMergeImageLayers

try:
    _magick.MagickGetImageRegion.restype = MagickWand
    _magick.MagickGetImageRegion.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickGetImageRegion = _magick.MagickGetImageRegion

try:
    _magick.MagickGetImageClipMask.restype = MagickWand
    _magick.MagickGetImageClipMask.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageClipMask = _magick.MagickGetImageClipMask

try:
    _magick.MagickGetImage.restype = MagickWand
    _magick.MagickGetImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImage = _magick.MagickGetImage

try:
    _magick.MagickFxImageChannel.restype = MagickWand
    _magick.MagickFxImageChannel.argtypes = (MagickWand, ChannelType, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickFxImageChannel = _magick.MagickFxImageChannel

try:
    _magick.MagickFxImage.restype = MagickWand
    _magick.MagickFxImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickFxImage = _magick.MagickFxImage

try:
    _magick.MagickDeconstructImages.restype = MagickWand
    _magick.MagickDeconstructImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickDeconstructImages = _magick.MagickDeconstructImages

try:
    _magick.MagickCompareImageLayers.restype = MagickWand
    _magick.MagickCompareImageLayers.argtypes = (MagickWand, ImageLayerMethod)
except AttributeError, e:
    print e
else:
    MagickCompareImageLayers = _magick.MagickCompareImageLayers

try:
    _magick.MagickCompareImages.restype = MagickWand
    _magick.MagickCompareImages.argtypes = (MagickWand, MagickWand, MetricType, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickCompareImages = _magick.MagickCompareImages

try:
    _magick.MagickCompareImageChannels.restype = MagickWand
    _magick.MagickCompareImageChannels.argtypes = (MagickWand, MagickWand, ChannelType, MetricType, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickCompareImageChannels = _magick.MagickCompareImageChannels

try:
    _magick.MagickCombineImages.restype = MagickWand
    _magick.MagickCombineImages.argtypes = (MagickWand, ChannelType)
except AttributeError, e:
    print e
else:
    MagickCombineImages = _magick.MagickCombineImages

try:
    _magick.MagickCoalesceImages.restype = MagickWand
    _magick.MagickCoalesceImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickCoalesceImages = _magick.MagickCoalesceImages

try:
    _magick.MagickAverageImages.restype = MagickWand
    _magick.MagickAverageImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickAverageImages = _magick.MagickAverageImages

try:
    _magick.MagickAppendImages.restype = MagickWand
    _magick.MagickAppendImages.argtypes = (MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickAppendImages = _magick.MagickAppendImages

try:
    _magick.MagickWriteImagesFile.restype = MagickBooleanType
    _magick.MagickWriteImagesFile.argtypes = (MagickWand, FILE)
except AttributeError, e:
    print e
else:
    MagickWriteImagesFile = _magick.MagickWriteImagesFile

try:
    _magick.MagickWriteImages.restype = MagickBooleanType
    _magick.MagickWriteImages.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickWriteImages = _magick.MagickWriteImages

try:
    _magick.MagickWriteImageFile.restype = MagickBooleanType
    _magick.MagickWriteImageFile.argtypes = (MagickWand, FILE)
except AttributeError, e:
    print e
else:
    MagickWriteImageFile = _magick.MagickWriteImageFile

try:
    _magick.MagickWriteImage.restype = MagickBooleanType
    _magick.MagickWriteImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickWriteImage = _magick.MagickWriteImage

try:
    _magick.MagickWhiteThresholdImage.restype = MagickBooleanType
    _magick.MagickWhiteThresholdImage.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickWhiteThresholdImage = _magick.MagickWhiteThresholdImage

try:
    _magick.MagickWaveImage.restype = MagickBooleanType
    _magick.MagickWaveImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickWaveImage = _magick.MagickWaveImage

try:
    _magick.MagickVignetteImage.restype = MagickBooleanType
    _magick.MagickVignetteImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickVignetteImage = _magick.MagickVignetteImage

try:
    _magick.MagickUnsharpMaskImageChannel.restype = MagickBooleanType
    _magick.MagickUnsharpMaskImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickUnsharpMaskImageChannel = _magick.MagickUnsharpMaskImageChannel

try:
    _magick.MagickUnsharpMaskImage.restype = MagickBooleanType
    _magick.MagickUnsharpMaskImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickUnsharpMaskImage = _magick.MagickUnsharpMaskImage

try:
    _magick.MagickUniqueImageColors.restype = MagickBooleanType
    _magick.MagickUniqueImageColors.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickUniqueImageColors = _magick.MagickUniqueImageColors

try:
    _magick.MagickTrimImage.restype = MagickBooleanType
    _magick.MagickTrimImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickTrimImage = _magick.MagickTrimImage

try:
    _magick.MagickThumbnailImage.restype = MagickBooleanType
    _magick.MagickThumbnailImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickThumbnailImage = _magick.MagickThumbnailImage

try:
    _magick.MagickThresholdImageChannel.restype = MagickBooleanType
    _magick.MagickThresholdImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickThresholdImageChannel = _magick.MagickThresholdImageChannel

try:
    _magick.MagickThresholdImage.restype = MagickBooleanType
    _magick.MagickThresholdImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickThresholdImage = _magick.MagickThresholdImage

try:
    _magick.MagickTransverseImage.restype = MagickBooleanType
    _magick.MagickTransverseImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickTransverseImage = _magick.MagickTransverseImage

try:
    _magick.MagickTransposeImage.restype = MagickBooleanType
    _magick.MagickTransposeImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickTransposeImage = _magick.MagickTransposeImage

try:
    _magick.MagickTintImage.restype = MagickBooleanType
    _magick.MagickTintImage.argtypes = (MagickWand, PixelWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickTintImage = _magick.MagickTintImage

try:
    _magick.MagickSwirlImage.restype = MagickBooleanType
    _magick.MagickSwirlImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSwirlImage = _magick.MagickSwirlImage

try:
    _magick.MagickStripImage.restype = MagickBooleanType
    _magick.MagickStripImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickStripImage = _magick.MagickStripImage

try:
    _magick.MagickSpreadImage.restype = MagickBooleanType
    _magick.MagickSpreadImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSpreadImage = _magick.MagickSpreadImage

try:
    _magick.MagickSpliceImage.restype = MagickBooleanType
    _magick.MagickSpliceImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSpliceImage = _magick.MagickSpliceImage

try:
    _magick.MagickSolarizeImage.restype = MagickBooleanType
    _magick.MagickSolarizeImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSolarizeImage = _magick.MagickSolarizeImage

try:
    _magick.MagickSketchImage.restype = MagickBooleanType
    _magick.MagickSketchImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSketchImage = _magick.MagickSketchImage

try:
    _magick.MagickSigmoidalContrastImageChannel.restype = MagickBooleanType
    _magick.MagickSigmoidalContrastImageChannel.argtypes = (MagickWand, ChannelType, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSigmoidalContrastImageChannel = _magick.MagickSigmoidalContrastImageChannel

try:
    _magick.MagickSigmoidalContrastImage.restype = MagickBooleanType
    _magick.MagickSigmoidalContrastImage.argtypes = (MagickWand, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSigmoidalContrastImage = _magick.MagickSigmoidalContrastImage

try:
    _magick.MagickShearImage.restype = MagickBooleanType
    _magick.MagickShearImage.argtypes = (MagickWand, PixelWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickShearImage = _magick.MagickShearImage

try:
    _magick.MagickShaveImage.restype = MagickBooleanType
    _magick.MagickShaveImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickShaveImage = _magick.MagickShaveImage

try:
    _magick.MagickSharpenImageChannel.restype = MagickBooleanType
    _magick.MagickSharpenImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSharpenImageChannel = _magick.MagickSharpenImageChannel

try:
    _magick.MagickSharpenImage.restype = MagickBooleanType
    _magick.MagickSharpenImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSharpenImage = _magick.MagickSharpenImage

try:
    _magick.MagickShadowImage.restype = MagickBooleanType
    _magick.MagickShadowImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickShadowImage = _magick.MagickShadowImage

try:
    _magick.MagickShadeImage.restype = MagickBooleanType
    _magick.MagickShadeImage.argtypes = (MagickWand, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickShadeImage = _magick.MagickShadeImage

try:
    _magick.MagickSetImageWhitePoint.restype = MagickBooleanType
    _magick.MagickSetImageWhitePoint.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageWhitePoint = _magick.MagickSetImageWhitePoint

try:
    _magick.MagickSetImageUnits.restype = MagickBooleanType
    _magick.MagickSetImageUnits.argtypes = (MagickWand, ResolutionType)
except AttributeError, e:
    print e
else:
    MagickSetImageUnits = _magick.MagickSetImageUnits

try:
    _magick.MagickSetImageType.restype = MagickBooleanType
    _magick.MagickSetImageType.argtypes = (MagickWand, ImageType)
except AttributeError, e:
    print e
else:
    MagickSetImageType = _magick.MagickSetImageType

try:
    _magick.MagickSetImageTicksPerSecond.restype = MagickBooleanType
    _magick.MagickSetImageTicksPerSecond.argtypes = (MagickWand, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetImageTicksPerSecond = _magick.MagickSetImageTicksPerSecond

try:
    _magick.MagickSetImageScene.restype = MagickBooleanType
    _magick.MagickSetImageScene.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageScene = _magick.MagickSetImageScene

try:
    _magick.MagickSetImageResolution.restype = MagickBooleanType
    _magick.MagickSetImageResolution.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageResolution = _magick.MagickSetImageResolution

try:
    _magick.MagickSetImageRenderingIntent.restype = MagickBooleanType
    _magick.MagickSetImageRenderingIntent.argtypes = (MagickWand, RenderingIntent)
except AttributeError, e:
    print e
else:
    MagickSetImageRenderingIntent = _magick.MagickSetImageRenderingIntent

try:
    _magick.MagickSetImageRedPrimary.restype = MagickBooleanType
    _magick.MagickSetImageRedPrimary.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageRedPrimary = _magick.MagickSetImageRedPrimary

try:
    _magick.MagickSetImagePixels.restype = MagickBooleanType
    _magick.MagickSetImagePixels.argtypes = (MagickWand, ctypes.c_long, ctypes.c_long, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_char), StorageType, ctypes.c_void_p)
except AttributeError, e:
    print e
else:
    MagickSetImagePixels = _magick.MagickSetImagePixels

try:
    _magick.MagickResetImagePage.restype = MagickBooleanType
    _magick.MagickResetImagePage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickResetImagePage = _magick.MagickResetImagePage

try:
    _magick.MagickSetImagePage.restype = MagickBooleanType
    _magick.MagickSetImagePage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetImagePage = _magick.MagickSetImagePage

try:
    _magick.MagickSetImageOrientation.restype = MagickBooleanType
    _magick.MagickSetImageOrientation.argtypes = (MagickWand, OrientationType)
except AttributeError, e:
    print e
else:
    MagickSetImageOrientation = _magick.MagickSetImageOrientation

try:
    _magick.MagickSetImageOpacity.restype = MagickBooleanType
    _magick.MagickSetImageOpacity.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageOpacity = _magick.MagickSetImageOpacity

try:
    _magick.MagickSetImageMatteColor.restype = MagickBooleanType
    _magick.MagickSetImageMatteColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickSetImageMatteColor = _magick.MagickSetImageMatteColor

try:
    _magick.MagickSetImageMatte.restype = MagickBooleanType
    _magick.MagickSetImageMatte.argtypes = (MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickSetImageMatte = _magick.MagickSetImageMatte

try:
    _magick.MagickSetImageIterations.restype = MagickBooleanType
    _magick.MagickSetImageIterations.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageIterations = _magick.MagickSetImageIterations

try:
    _magick.MagickSetImageInterpolateMethod.restype = MagickBooleanType
    _magick.MagickSetImageInterpolateMethod.argtypes = (MagickWand, InterpolatePixelMethod)
except AttributeError, e:
    print e
else:
    MagickSetImageInterpolateMethod = _magick.MagickSetImageInterpolateMethod

try:
    _magick.MagickSetImageInterlaceScheme.restype = MagickBooleanType
    _magick.MagickSetImageInterlaceScheme.argtypes = (MagickWand, InterlaceType)
except AttributeError, e:
    print e
else:
    MagickSetImageInterlaceScheme = _magick.MagickSetImageInterlaceScheme

try:
    _magick.MagickSetImageFormat.restype = MagickBooleanType
    _magick.MagickSetImageFormat.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetImageFormat = _magick.MagickSetImageFormat

try:
    _magick.MagickSetImageFilename.restype = MagickBooleanType
    _magick.MagickSetImageFilename.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetImageFilename = _magick.MagickSetImageFilename

try:
    _magick.MagickSetImageExtent.restype = MagickBooleanType
    _magick.MagickSetImageExtent.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageExtent = _magick.MagickSetImageExtent

try:
    _magick.MagickSetImageGamma.restype = MagickBooleanType
    _magick.MagickSetImageGamma.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageGamma = _magick.MagickSetImageGamma

try:
    _magick.MagickSetImageGreenPrimary.restype = MagickBooleanType
    _magick.MagickSetImageGreenPrimary.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageGreenPrimary = _magick.MagickSetImageGreenPrimary

try:
    _magick.MagickSetImageCompressionQuality.restype = MagickBooleanType
    _magick.MagickSetImageCompressionQuality.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageCompressionQuality = _magick.MagickSetImageCompressionQuality

try:
    _magick.MagickSetImageColorspace.restype = MagickBooleanType
    _magick.MagickSetImageColorspace.argtypes = (MagickWand, ColorspaceType)
except AttributeError, e:
    print e
else:
    MagickSetImageColorspace = _magick.MagickSetImageColorspace

try:
    _magick.MagickSetImageDispose.restype = MagickBooleanType
    _magick.MagickSetImageDispose.argtypes = (MagickWand, DisposeType)
except AttributeError, e:
    print e
else:
    MagickSetImageDispose = _magick.MagickSetImageDispose

try:
    _magick.MagickSetImageDepth.restype = MagickBooleanType
    _magick.MagickSetImageDepth.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageDepth = _magick.MagickSetImageDepth

try:
    _magick.MagickSetImageDelay.restype = MagickBooleanType
    _magick.MagickSetImageDelay.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageDelay = _magick.MagickSetImageDelay

try:
    _magick.MagickSetImageCompression.restype = MagickBooleanType
    _magick.MagickSetImageCompression.argtypes = (MagickWand, CompressionType)
except AttributeError, e:
    print e
else:
    MagickSetImageCompression = _magick.MagickSetImageCompression

try:
    _magick.MagickSetImageCompose.restype = MagickBooleanType
    _magick.MagickSetImageCompose.argtypes = (MagickWand, CompositeOperator)
except AttributeError, e:
    print e
else:
    MagickSetImageCompose = _magick.MagickSetImageCompose

try:
    _magick.MagickSetImageColormapColor.restype = MagickBooleanType
    _magick.MagickSetImageColormapColor.argtypes = (MagickWand, ctypes.c_ulong, PixelWand)
except AttributeError, e:
    print e
else:
    MagickSetImageColormapColor = _magick.MagickSetImageColormapColor

try:
    _magick.MagickSetImageClipMask.restype = MagickBooleanType
    _magick.MagickSetImageClipMask.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickSetImageClipMask = _magick.MagickSetImageClipMask

try:
    _magick.MagickSetImageChannelDepth.restype = MagickBooleanType
    _magick.MagickSetImageChannelDepth.argtypes = (MagickWand, ChannelType, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageChannelDepth = _magick.MagickSetImageChannelDepth

try:
    _magick.MagickSetImageBorderColor.restype = MagickBooleanType
    _magick.MagickSetImageBorderColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickSetImageBorderColor = _magick.MagickSetImageBorderColor

try:
    _magick.MagickSetImageBluePrimary.restype = MagickBooleanType
    _magick.MagickSetImageBluePrimary.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageBluePrimary = _magick.MagickSetImageBluePrimary

try:
    _magick.MagickSetImageBias.restype = MagickBooleanType
    _magick.MagickSetImageBias.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetImageBias = _magick.MagickSetImageBias

try:
    _magick.MagickSetImageBackgroundColor.restype = MagickBooleanType
    _magick.MagickSetImageBackgroundColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickSetImageBackgroundColor = _magick.MagickSetImageBackgroundColor

try:
    _magick.MagickSetImageAlphaChannel.restype = MagickBooleanType
    _magick.MagickSetImageAlphaChannel.argtypes = (MagickWand, AlphaChannelType)
except AttributeError, e:
    print e
else:
    MagickSetImageAlphaChannel = _magick.MagickSetImageAlphaChannel

try:
    _magick.MagickSetImage.restype = MagickBooleanType
    _magick.MagickSetImage.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickSetImage = _magick.MagickSetImage

try:
    _magick.MagickSepiaToneImage.restype = MagickBooleanType
    _magick.MagickSepiaToneImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSepiaToneImage = _magick.MagickSepiaToneImage

try:
    _magick.MagickSeparateImageChannel.restype = MagickBooleanType
    _magick.MagickSeparateImageChannel.argtypes = (MagickWand, ChannelType)
except AttributeError, e:
    print e
else:
    MagickSeparateImageChannel = _magick.MagickSeparateImageChannel

try:
    _magick.MagickSegmentImage.restype = MagickBooleanType
    _magick.MagickSegmentImage.argtypes = (MagickWand, ColorspaceType, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSegmentImage = _magick.MagickSegmentImage

try:
    _magick.MagickScaleImage.restype = MagickBooleanType
    _magick.MagickScaleImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickScaleImage = _magick.MagickScaleImage

try:
    _magick.MagickSampleImage.restype = MagickBooleanType
    _magick.MagickSampleImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSampleImage = _magick.MagickSampleImage

try:
    _magick.MagickRotateImage.restype = MagickBooleanType
    _magick.MagickRotateImage.argtypes = (MagickWand, PixelWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickRotateImage = _magick.MagickRotateImage

try:
    _magick.MagickRollImage.restype = MagickBooleanType
    _magick.MagickRollImage.argtypes = (MagickWand, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickRollImage = _magick.MagickRollImage

try:
    _magick.MagickResizeImage.restype = MagickBooleanType
    _magick.MagickResizeImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, FilterTypes, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickResizeImage = _magick.MagickResizeImage

try:
    _magick.MagickResampleImage.restype = MagickBooleanType
    _magick.MagickResampleImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, FilterTypes, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickResampleImage = _magick.MagickResampleImage

try:
    _magick.MagickRemoveImage.restype = MagickBooleanType
    _magick.MagickRemoveImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickRemoveImage = _magick.MagickRemoveImage

try:
    _magick.MagickReduceNoiseImage.restype = MagickBooleanType
    _magick.MagickReduceNoiseImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickReduceNoiseImage = _magick.MagickReduceNoiseImage

try:
    _magick.MagickRecolorImage.restype = MagickBooleanType
    _magick.MagickRecolorImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickRecolorImage = _magick.MagickRecolorImage

try:
    _magick.MagickReadImageFile.restype = MagickBooleanType
    _magick.MagickReadImageFile.argtypes = (MagickWand, FILE)
except AttributeError, e:
    print e
else:
    MagickReadImageFile = _magick.MagickReadImageFile

try:
    _magick.MagickReadImageBlob.restype = MagickBooleanType
    _magick.MagickReadImageBlob.argtypes = (MagickWand, ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickReadImageBlob = _magick.MagickReadImageBlob

try:
    _magick.MagickReadImage.restype = MagickBooleanType
    _magick.MagickReadImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickReadImage = _magick.MagickReadImage

try:
    _magick.MagickRandomThresholdImageChannel.restype = MagickBooleanType
    _magick.MagickRandomThresholdImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickRandomThresholdImageChannel = _magick.MagickRandomThresholdImageChannel

try:
    _magick.MagickRandomThresholdImage.restype = MagickBooleanType
    _magick.MagickRandomThresholdImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickRandomThresholdImage = _magick.MagickRandomThresholdImage

try:
    _magick.MagickRaiseImage.restype = MagickBooleanType
    _magick.MagickRaiseImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickRaiseImage = _magick.MagickRaiseImage

try:
    _magick.MagickRadialBlurImageChannel.restype = MagickBooleanType
    _magick.MagickRadialBlurImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickRadialBlurImageChannel = _magick.MagickRadialBlurImageChannel

try:
    _magick.MagickRadialBlurImage.restype = MagickBooleanType
    _magick.MagickRadialBlurImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickRadialBlurImage = _magick.MagickRadialBlurImage

try:
    _magick.MagickQuantizeImages.restype = MagickBooleanType
    _magick.MagickQuantizeImages.argtypes = (MagickWand, ctypes.c_ulong, ColorspaceType, ctypes.c_ulong, MagickBooleanType, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickQuantizeImages = _magick.MagickQuantizeImages

try:
    _magick.MagickQuantizeImage.restype = MagickBooleanType
    _magick.MagickQuantizeImage.argtypes = (MagickWand, ctypes.c_ulong, ColorspaceType, ctypes.c_ulong, MagickBooleanType, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickQuantizeImage = _magick.MagickQuantizeImage

try:
    _magick.MagickPreviousImage.restype = MagickBooleanType
    _magick.MagickPreviousImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickPreviousImage = _magick.MagickPreviousImage

try:
    _magick.MagickPosterizeImage.restype = MagickBooleanType
    _magick.MagickPosterizeImage.argtypes = (MagickWand, ctypes.c_ulong, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickPosterizeImage = _magick.MagickPosterizeImage

try:
    _magick.MagickPolaroidImage.restype = MagickBooleanType
    _magick.MagickPolaroidImage.argtypes = (MagickWand, DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickPolaroidImage = _magick.MagickPolaroidImage

try:
    _magick.MagickPingImageFile.restype = MagickBooleanType
    _magick.MagickPingImageFile.argtypes = (MagickWand, FILE)
except AttributeError, e:
    print e
else:
    MagickPingImageFile = _magick.MagickPingImageFile

try:
    _magick.MagickPingImageBlob.restype = MagickBooleanType
    _magick.MagickPingImageBlob.argtypes = (MagickWand, ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickPingImageBlob = _magick.MagickPingImageBlob

try:
    _magick.MagickPingImage.restype = MagickBooleanType
    _magick.MagickPingImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickPingImage = _magick.MagickPingImage

try:
    _magick.MagickPaintTransparentImage.restype = MagickBooleanType
    _magick.MagickPaintTransparentImage.argtypes = (MagickWand, PixelWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickPaintTransparentImage = _magick.MagickPaintTransparentImage

try:
    _magick.MagickPaintOpaqueImageChannel.restype = MagickBooleanType
    _magick.MagickPaintOpaqueImageChannel.argtypes = (MagickWand, ChannelType, PixelWand, PixelWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickPaintOpaqueImageChannel = _magick.MagickPaintOpaqueImageChannel

try:
    _magick.MagickPaintOpaqueImage.restype = MagickBooleanType
    _magick.MagickPaintOpaqueImage.argtypes = (MagickWand, PixelWand, PixelWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickPaintOpaqueImage = _magick.MagickPaintOpaqueImage

try:
    _magick.MagickPaintFloodfillImage.restype = MagickBooleanType
    _magick.MagickPaintFloodfillImage.argtypes = (MagickWand, ChannelType, PixelWand, ctypes.c_double, PixelWand, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickPaintFloodfillImage = _magick.MagickPaintFloodfillImage

try:
    _magick.MagickOrderedPosterizeImageChannel.restype = MagickBooleanType
    _magick.MagickOrderedPosterizeImageChannel.argtypes = (MagickWand, ChannelType, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickOrderedPosterizeImageChannel = _magick.MagickOrderedPosterizeImageChannel

try:
    _magick.MagickOrderedPosterizeImage.restype = MagickBooleanType
    _magick.MagickOrderedPosterizeImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickOrderedPosterizeImage = _magick.MagickOrderedPosterizeImage

try:
    _magick.MagickOilPaintImage.restype = MagickBooleanType
    _magick.MagickOilPaintImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickOilPaintImage = _magick.MagickOilPaintImage

try:
    _magick.MagickNormalizeImageChannel.restype = MagickBooleanType
    _magick.MagickNormalizeImageChannel.argtypes = (MagickWand, ChannelType)
except AttributeError, e:
    print e
else:
    MagickNormalizeImageChannel = _magick.MagickNormalizeImageChannel

try:
    _magick.MagickNormalizeImage.restype = MagickBooleanType
    _magick.MagickNormalizeImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickNormalizeImage = _magick.MagickNormalizeImage

try:
    _magick.MagickNextImage.restype = MagickBooleanType
    _magick.MagickNextImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickNextImage = _magick.MagickNextImage

try:
    _magick.MagickNewImage.restype = MagickBooleanType
    _magick.MagickNewImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, PixelWand)
except AttributeError, e:
    print e
else:
    MagickNewImage = _magick.MagickNewImage

try:
    _magick.MagickNegateImageChannel.restype = MagickBooleanType
    _magick.MagickNegateImageChannel.argtypes = (MagickWand, ChannelType, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickNegateImageChannel = _magick.MagickNegateImageChannel

try:
    _magick.MagickNegateImage.restype = MagickBooleanType
    _magick.MagickNegateImage.argtypes = (MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickNegateImage = _magick.MagickNegateImage

try:
    _magick.MagickMotionBlurImage.restype = MagickBooleanType
    _magick.MagickMotionBlurImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickMotionBlurImage = _magick.MagickMotionBlurImage

try:
    _magick.MagickModulateImage.restype = MagickBooleanType
    _magick.MagickModulateImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickModulateImage = _magick.MagickModulateImage

try:
    _magick.MagickMinifyImage.restype = MagickBooleanType
    _magick.MagickMinifyImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickMinifyImage = _magick.MagickMinifyImage

try:
    _magick.MagickMedianFilterImage.restype = MagickBooleanType
    _magick.MagickMedianFilterImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickMedianFilterImage = _magick.MagickMedianFilterImage

try:
    _magick.MagickMapImage.restype = MagickBooleanType
    _magick.MagickMapImage.argtypes = (MagickWand, MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickMapImage = _magick.MagickMapImage

try:
    _magick.MagickMagnifyImage.restype = MagickBooleanType
    _magick.MagickMagnifyImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickMagnifyImage = _magick.MagickMagnifyImage

try:
    _magick.MagickLinearStretchImage.restype = MagickBooleanType
    _magick.MagickLinearStretchImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickLinearStretchImage = _magick.MagickLinearStretchImage

try:
    _magick.MagickLevelImageChannel.restype = MagickBooleanType
    _magick.MagickLevelImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickLevelImageChannel = _magick.MagickLevelImageChannel

try:
    _magick.MagickLevelImage.restype = MagickBooleanType
    _magick.MagickLevelImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickLevelImage = _magick.MagickLevelImage

try:
    _magick.MagickLabelImage.restype = MagickBooleanType
    _magick.MagickLabelImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickLabelImage = _magick.MagickLabelImage

try:
    _magick.MagickImplodeImage.restype = MagickBooleanType
    _magick.MagickImplodeImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickImplodeImage = _magick.MagickImplodeImage

try:
    _magick.MagickHasPreviousImage.restype = MagickBooleanType
    _magick.MagickHasPreviousImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickHasPreviousImage = _magick.MagickHasPreviousImage

try:
    _magick.MagickHasNextImage.restype = MagickBooleanType
    _magick.MagickHasNextImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickHasNextImage = _magick.MagickHasNextImage

try:
    _magick.MagickGetImageWhitePoint.restype = MagickBooleanType
    _magick.MagickGetImageWhitePoint.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageWhitePoint = _magick.MagickGetImageWhitePoint

try:
    _magick.MagickGetImageResolution.restype = MagickBooleanType
    _magick.MagickGetImageResolution.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageResolution = _magick.MagickGetImageResolution

try:
    _magick.MagickGetImageRedPrimary.restype = MagickBooleanType
    _magick.MagickGetImageRedPrimary.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageRedPrimary = _magick.MagickGetImageRedPrimary

try:
    _magick.MagickGetImageRange.restype = MagickBooleanType
    _magick.MagickGetImageRange.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageRange = _magick.MagickGetImageRange

try:
    _magick.MagickGetImagePixels.restype = MagickBooleanType
    _magick.MagickGetImagePixels.argtypes = (MagickWand, ctypes.c_long, ctypes.c_long, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_char), StorageType, ctypes.c_void_p)
except AttributeError, e:
    print e
else:
    MagickGetImagePixels = _magick.MagickGetImagePixels

try:
    _magick.MagickGetImagePixelColor.restype = MagickBooleanType
    _magick.MagickGetImagePixelColor.argtypes = (MagickWand, ctypes.c_long, ctypes.c_long, PixelWand)
except AttributeError, e:
    print e
else:
    MagickGetImagePixelColor = _magick.MagickGetImagePixelColor

try:
    _magick.MagickGetImagePage.restype = MagickBooleanType
    _magick.MagickGetImagePage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
except AttributeError, e:
    print e
else:
    MagickGetImagePage = _magick.MagickGetImagePage

try:
    _magick.MagickGetImageLength.restype = MagickBooleanType
    _magick.MagickGetImageLength.argtypes = (MagickWand, MagickSizeType)
except AttributeError, e:
    print e
else:
    MagickGetImageLength = _magick.MagickGetImageLength

try:
    _magick.MagickGetImageMatteColor.restype = MagickBooleanType
    _magick.MagickGetImageMatteColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickGetImageMatteColor = _magick.MagickGetImageMatteColor

try:
    _magick.MagickGetImageMatte.restype = MagickBooleanType
    _magick.MagickGetImageMatte.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageMatte = _magick.MagickGetImageMatte

try:
    _magick.MagickGetImageGreenPrimary.restype = MagickBooleanType
    _magick.MagickGetImageGreenPrimary.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageGreenPrimary = _magick.MagickGetImageGreenPrimary

try:
    _magick.MagickGetImageColormapColor.restype = MagickBooleanType
    _magick.MagickGetImageColormapColor.argtypes = (MagickWand, ctypes.c_ulong, PixelWand)
except AttributeError, e:
    print e
else:
    MagickGetImageColormapColor = _magick.MagickGetImageColormapColor

try:
    _magick.MagickGetImageChannelRange.restype = MagickBooleanType
    _magick.MagickGetImageChannelRange.argtypes = (MagickWand, ChannelType, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageChannelRange = _magick.MagickGetImageChannelRange

try:
    _magick.MagickGetImageChannelMean.restype = MagickBooleanType
    _magick.MagickGetImageChannelMean.argtypes = (MagickWand, ChannelType, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageChannelMean = _magick.MagickGetImageChannelMean

try:
    _magick.MagickGetImageDistortion.restype = MagickBooleanType
    _magick.MagickGetImageDistortion.argtypes = (MagickWand, MagickWand, MetricType, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageDistortion = _magick.MagickGetImageDistortion

try:
    _magick.MagickGetImageChannelDistortion.restype = MagickBooleanType
    _magick.MagickGetImageChannelDistortion.argtypes = (MagickWand, MagickWand, ChannelType, MetricType, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageChannelDistortion = _magick.MagickGetImageChannelDistortion

try:
    _magick.MagickGetImageBorderColor.restype = MagickBooleanType
    _magick.MagickGetImageBorderColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickGetImageBorderColor = _magick.MagickGetImageBorderColor

try:
    _magick.MagickGetImageBluePrimary.restype = MagickBooleanType
    _magick.MagickGetImageBluePrimary.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickGetImageBluePrimary = _magick.MagickGetImageBluePrimary

try:
    _magick.MagickGetImageBackgroundColor.restype = MagickBooleanType
    _magick.MagickGetImageBackgroundColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickGetImageBackgroundColor = _magick.MagickGetImageBackgroundColor

try:
    _magick.MagickGaussianBlurImageChannel.restype = MagickBooleanType
    _magick.MagickGaussianBlurImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickGaussianBlurImageChannel = _magick.MagickGaussianBlurImageChannel

try:
    _magick.MagickGaussianBlurImage.restype = MagickBooleanType
    _magick.MagickGaussianBlurImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickGaussianBlurImage = _magick.MagickGaussianBlurImage

try:
    _magick.MagickGammaImageChannel.restype = MagickBooleanType
    _magick.MagickGammaImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickGammaImageChannel = _magick.MagickGammaImageChannel

try:
    _magick.MagickGammaImage.restype = MagickBooleanType
    _magick.MagickGammaImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickGammaImage = _magick.MagickGammaImage

try:
    _magick.MagickFrameImage.restype = MagickBooleanType
    _magick.MagickFrameImage.argtypes = (MagickWand, PixelWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickFrameImage = _magick.MagickFrameImage

try:
    _magick.MagickFlopImage.restype = MagickBooleanType
    _magick.MagickFlopImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickFlopImage = _magick.MagickFlopImage

try:
    _magick.MagickFlipImage.restype = MagickBooleanType
    _magick.MagickFlipImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickFlipImage = _magick.MagickFlipImage

try:
    _magick.MagickExtentImage.restype = MagickBooleanType
    _magick.MagickExtentImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickExtentImage = _magick.MagickExtentImage

try:
    _magick.MagickEvaluateImageChannel.restype = MagickBooleanType
    _magick.MagickEvaluateImageChannel.argtypes = (MagickWand, ChannelType, MagickEvaluateOperator, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickEvaluateImageChannel = _magick.MagickEvaluateImageChannel

try:
    _magick.MagickEvaluateImage.restype = MagickBooleanType
    _magick.MagickEvaluateImage.argtypes = (MagickWand, MagickEvaluateOperator, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickEvaluateImage = _magick.MagickEvaluateImage

try:
    _magick.MagickEqualizeImageChannel.restype = MagickBooleanType
    _magick.MagickEqualizeImageChannel.argtypes = (MagickWand, ChannelType)
except AttributeError, e:
    print e
else:
    MagickEqualizeImageChannel = _magick.MagickEqualizeImageChannel

try:
    _magick.MagickEqualizeImage.restype = MagickBooleanType
    _magick.MagickEqualizeImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickEqualizeImage = _magick.MagickEqualizeImage

try:
    _magick.MagickEnhanceImage.restype = MagickBooleanType
    _magick.MagickEnhanceImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickEnhanceImage = _magick.MagickEnhanceImage

try:
    _magick.MagickEmbossImage.restype = MagickBooleanType
    _magick.MagickEmbossImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickEmbossImage = _magick.MagickEmbossImage

try:
    _magick.MagickEdgeImage.restype = MagickBooleanType
    _magick.MagickEdgeImage.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickEdgeImage = _magick.MagickEdgeImage

try:
    _magick.MagickDrawImage.restype = MagickBooleanType
    _magick.MagickDrawImage.argtypes = (MagickWand, DrawingWand)
except AttributeError, e:
    print e
else:
    MagickDrawImage = _magick.MagickDrawImage

try:
    _magick.MagickDistortImage.restype = MagickBooleanType
    _magick.MagickDistortImage.argtypes = (MagickWand, DistortImageMethod, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double), MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickDistortImage = _magick.MagickDistortImage

try:
    _magick.MagickDisplayImages.restype = MagickBooleanType
    _magick.MagickDisplayImages.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickDisplayImages = _magick.MagickDisplayImages

try:
    _magick.MagickDisplayImage.restype = MagickBooleanType
    _magick.MagickDisplayImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickDisplayImage = _magick.MagickDisplayImage

try:
    _magick.MagickDespeckleImage.restype = MagickBooleanType
    _magick.MagickDespeckleImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickDespeckleImage = _magick.MagickDespeckleImage

try:
    _magick.MagickCycleColormapImage.restype = MagickBooleanType
    _magick.MagickCycleColormapImage.argtypes = (MagickWand, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickCycleColormapImage = _magick.MagickCycleColormapImage

try:
    _magick.MagickCropImage.restype = MagickBooleanType
    _magick.MagickCropImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickCropImage = _magick.MagickCropImage

try:
    _magick.MagickConvolveImageChannel.restype = MagickBooleanType
    _magick.MagickConvolveImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickConvolveImageChannel = _magick.MagickConvolveImageChannel

try:
    _magick.MagickConvolveImage.restype = MagickBooleanType
    _magick.MagickConvolveImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickConvolveImage = _magick.MagickConvolveImage

try:
    _magick.MagickContrastStretchImageChannel.restype = MagickBooleanType
    _magick.MagickContrastStretchImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickContrastStretchImageChannel = _magick.MagickContrastStretchImageChannel

try:
    _magick.MagickContrastStretchImage.restype = MagickBooleanType
    _magick.MagickContrastStretchImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickContrastStretchImage = _magick.MagickContrastStretchImage

try:
    _magick.MagickContrastImage.restype = MagickBooleanType
    _magick.MagickContrastImage.argtypes = (MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickContrastImage = _magick.MagickContrastImage

try:
    _magick.MagickConstituteImage.restype = MagickBooleanType
    _magick.MagickConstituteImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_char), StorageType, ctypes.c_void_p)
except AttributeError, e:
    print e
else:
    MagickConstituteImage = _magick.MagickConstituteImage

try:
    _magick.MagickCompositeImageChannel.restype = MagickBooleanType
    _magick.MagickCompositeImageChannel.argtypes = (MagickWand, ChannelType, MagickWand, CompositeOperator, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickCompositeImageChannel = _magick.MagickCompositeImageChannel

try:
    _magick.MagickCompositeImage.restype = MagickBooleanType
    _magick.MagickCompositeImage.argtypes = (MagickWand, MagickWand, CompositeOperator, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickCompositeImage = _magick.MagickCompositeImage

try:
    _magick.MagickCommentImage.restype = MagickBooleanType
    _magick.MagickCommentImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickCommentImage = _magick.MagickCommentImage

try:
    _magick.MagickColorizeImage.restype = MagickBooleanType
    _magick.MagickColorizeImage.argtypes = (MagickWand, PixelWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickColorizeImage = _magick.MagickColorizeImage

try:
    _magick.MagickClutImageChannel.restype = MagickBooleanType
    _magick.MagickClutImageChannel.argtypes = (MagickWand, ChannelType, MagickWand)
except AttributeError, e:
    print e
else:
    MagickClutImageChannel = _magick.MagickClutImageChannel

try:
    _magick.MagickClutImage.restype = MagickBooleanType
    _magick.MagickClutImage.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickClutImage = _magick.MagickClutImage

try:
    _magick.MagickClipImagePath.restype = MagickBooleanType
    _magick.MagickClipImagePath.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickClipImagePath = _magick.MagickClipImagePath

try:
    _magick.MagickClipImage.restype = MagickBooleanType
    _magick.MagickClipImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickClipImage = _magick.MagickClipImage

try:
    _magick.MagickChopImage.restype = MagickBooleanType
    _magick.MagickChopImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickChopImage = _magick.MagickChopImage

try:
    _magick.MagickCharcoalImage.restype = MagickBooleanType
    _magick.MagickCharcoalImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickCharcoalImage = _magick.MagickCharcoalImage

try:
    _magick.MagickBorderImage.restype = MagickBooleanType
    _magick.MagickBorderImage.argtypes = (MagickWand, PixelWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickBorderImage = _magick.MagickBorderImage

try:
    _magick.MagickBlurImageChannel.restype = MagickBooleanType
    _magick.MagickBlurImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickBlurImageChannel = _magick.MagickBlurImageChannel

try:
    _magick.MagickBlurImage.restype = MagickBooleanType
    _magick.MagickBlurImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickBlurImage = _magick.MagickBlurImage

try:
    _magick.MagickBlackThresholdImage.restype = MagickBooleanType
    _magick.MagickBlackThresholdImage.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickBlackThresholdImage = _magick.MagickBlackThresholdImage

try:
    _magick.MagickAnimateImages.restype = MagickBooleanType
    _magick.MagickAnimateImages.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickAnimateImages = _magick.MagickAnimateImages

try:
    _magick.MagickAnnotateImage.restype = MagickBooleanType
    _magick.MagickAnnotateImage.argtypes = (MagickWand, DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickAnnotateImage = _magick.MagickAnnotateImage

try:
    _magick.MagickAffineTransformImage.restype = MagickBooleanType
    _magick.MagickAffineTransformImage.argtypes = (MagickWand, DrawingWand)
except AttributeError, e:
    print e
else:
    MagickAffineTransformImage = _magick.MagickAffineTransformImage

try:
    _magick.MagickAddNoiseImageChannel.restype = MagickBooleanType
    _magick.MagickAddNoiseImageChannel.argtypes = (MagickWand, ChannelType, NoiseType)
except AttributeError, e:
    print e
else:
    MagickAddNoiseImageChannel = _magick.MagickAddNoiseImageChannel

try:
    _magick.MagickAddNoiseImage.restype = MagickBooleanType
    _magick.MagickAddNoiseImage.argtypes = (MagickWand, NoiseType)
except AttributeError, e:
    print e
else:
    MagickAddNoiseImage = _magick.MagickAddNoiseImage

try:
    _magick.MagickAddImage.restype = MagickBooleanType
    _magick.MagickAddImage.argtypes = (MagickWand, MagickWand)
except AttributeError, e:
    print e
else:
    MagickAddImage = _magick.MagickAddImage

try:
    _magick.MagickAdaptiveThresholdImage.restype = MagickBooleanType
    _magick.MagickAdaptiveThresholdImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickAdaptiveThresholdImage = _magick.MagickAdaptiveThresholdImage

try:
    _magick.MagickAdaptiveSharpenImageChannel.restype = MagickBooleanType
    _magick.MagickAdaptiveSharpenImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickAdaptiveSharpenImageChannel = _magick.MagickAdaptiveSharpenImageChannel

try:
    _magick.MagickAdaptiveSharpenImage.restype = MagickBooleanType
    _magick.MagickAdaptiveSharpenImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickAdaptiveSharpenImage = _magick.MagickAdaptiveSharpenImage

try:
    _magick.MagickAdaptiveResizeImage.restype = MagickBooleanType
    _magick.MagickAdaptiveResizeImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickAdaptiveResizeImage = _magick.MagickAdaptiveResizeImage

try:
    _magick.MagickAdaptiveBlurImageChannel.restype = MagickBooleanType
    _magick.MagickAdaptiveBlurImageChannel.argtypes = (MagickWand, ChannelType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickAdaptiveBlurImageChannel = _magick.MagickAdaptiveBlurImageChannel

try:
    _magick.MagickAdaptiveBlurImage.restype = MagickBooleanType
    _magick.MagickAdaptiveBlurImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickAdaptiveBlurImage = _magick.MagickAdaptiveBlurImage

try:
    _magick.MagickGetImageInterpolateMethod.restype = InterpolatePixelMethod
    _magick.MagickGetImageInterpolateMethod.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageInterpolateMethod = _magick.MagickGetImageInterpolateMethod

try:
    _magick.MagickGetImageInterlaceScheme.restype = InterlaceType
    _magick.MagickGetImageInterlaceScheme.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageInterlaceScheme = _magick.MagickGetImageInterlaceScheme

try:
    _magick.MagickGetImageType.restype = ImageType
    _magick.MagickGetImageType.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageType = _magick.MagickGetImageType

try:
    _magick.GetImageFromMagickWand.restype = Image
    _magick.GetImageFromMagickWand.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    GetImageFromMagickWand = _magick.GetImageFromMagickWand

try:
    _magick.MagickDestroyImage.restype = Image
    _magick.MagickDestroyImage.argtypes = (Image,)
except AttributeError, e:
    print e
else:
    MagickDestroyImage = _magick.MagickDestroyImage

try:
    _magick.MagickGetImageTotalInkDensity.restype = ctypes.c_double
    _magick.MagickGetImageTotalInkDensity.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageTotalInkDensity = _magick.MagickGetImageTotalInkDensity

try:
    _magick.MagickGetImageGamma.restype = ctypes.c_double
    _magick.MagickGetImageGamma.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageGamma = _magick.MagickGetImageGamma

try:
    _magick.MagickGetImageDispose.restype = DisposeType
    _magick.MagickGetImageDispose.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageDispose = _magick.MagickGetImageDispose

try:
    _magick.MagickGetImageCompression.restype = CompressionType
    _magick.MagickGetImageCompression.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageCompression = _magick.MagickGetImageCompression

try:
    _magick.MagickGetImageColorspace.restype = ColorspaceType
    _magick.MagickGetImageColorspace.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageColorspace = _magick.MagickGetImageColorspace

try:
    _magick.MagickGetImageCompose.restype = CompositeOperator
    _magick.MagickGetImageCompose.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageCompose = _magick.MagickGetImageCompose

try:
    _magick.MagickIdentifyImage.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickIdentifyImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickIdentifyImage = _magick.MagickIdentifyImage

try:
    _magick.MagickGetImageSignature.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetImageSignature.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageSignature = _magick.MagickGetImageSignature

try:
    _magick.MagickGetImageFormat.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetImageFormat.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageFormat = _magick.MagickGetImageFormat

try:
    _magick.MagickGetImageFilename.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetImageFilename.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageFilename = _magick.MagickGetImageFilename

try:
    _magick.MagickGetImageChannelStatistics.restype = ChannelStatistics
    _magick.MagickGetImageChannelStatistics.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageChannelStatistics = _magick.MagickGetImageChannelStatistics

try:
    _magick.MagickGetResourceLimit.restype = ctypes.c_ulong
    _magick.MagickGetResourceLimit.argtypes = (ResourceType,)
except AttributeError, e:
    print e
else:
    MagickGetResourceLimit = _magick.MagickGetResourceLimit

try:
    _magick.MagickGetResource.restype = ctypes.c_ulong
    _magick.MagickGetResource.argtypes = (ResourceType,)
except AttributeError, e:
    print e
else:
    MagickGetResource = _magick.MagickGetResource

try:
    _magick.MagickGetCompressionQuality.restype = ctypes.c_ulong
    _magick.MagickGetCompressionQuality.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetCompressionQuality = _magick.MagickGetCompressionQuality

try:
    _magick.MagickRemoveImageProfile.restype = ctypes.POINTER(ctypes.c_ubyte)
    _magick.MagickRemoveImageProfile.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), size_t)
except AttributeError, e:
    print e
else:
    MagickRemoveImageProfile = _magick.MagickRemoveImageProfile

try:
    _magick.MagickGetImageProfile.restype = ctypes.POINTER(ctypes.c_ubyte)
    _magick.MagickGetImageProfile.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), size_t)
except AttributeError, e:
    print e
else:
    MagickGetImageProfile = _magick.MagickGetImageProfile

try:
    _magick.MagickGetBackgroundColor.restype = PixelWand
    _magick.MagickGetBackgroundColor.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetBackgroundColor = _magick.MagickGetBackgroundColor

try:
    _magick.MagickSetType.restype = MagickBooleanType
    _magick.MagickSetType.argtypes = (MagickWand, ImageType)
except AttributeError, e:
    print e
else:
    MagickSetType = _magick.MagickSetType

try:
    _magick.MagickSetSizeOffset.restype = MagickBooleanType
    _magick.MagickSetSizeOffset.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetSizeOffset = _magick.MagickSetSizeOffset

try:
    _magick.MagickSetSize.restype = MagickBooleanType
    _magick.MagickSetSize.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetSize = _magick.MagickSetSize

try:
    _magick.MagickSetSamplingFactors.restype = MagickBooleanType
    _magick.MagickSetSamplingFactors.argtypes = (MagickWand, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    MagickSetSamplingFactors = _magick.MagickSetSamplingFactors

try:
    _magick.MagickSetResourceLimit.restype = MagickBooleanType
    _magick.MagickSetResourceLimit.argtypes = (ResourceType, ctypes.c_ulonglong)
except AttributeError, e:
    print e
else:
    MagickSetResourceLimit = _magick.MagickSetResourceLimit

try:
    _magick.MagickSetResolution.restype = MagickBooleanType
    _magick.MagickSetResolution.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetResolution = _magick.MagickSetResolution

try:
    _magick.MagickSetPointsize.restype = MagickBooleanType
    _magick.MagickSetPointsize.argtypes = (MagickWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickSetPointsize = _magick.MagickSetPointsize

try:
    _magick.MagickSetPassphrase.restype = MagickBooleanType
    _magick.MagickSetPassphrase.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetPassphrase = _magick.MagickSetPassphrase

try:
    _magick.MagickSetPage.restype = MagickBooleanType
    _magick.MagickSetPage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetPage = _magick.MagickSetPage

try:
    _magick.MagickSetOrientation.restype = MagickBooleanType
    _magick.MagickSetOrientation.argtypes = (MagickWand, OrientationType)
except AttributeError, e:
    print e
else:
    MagickSetOrientation = _magick.MagickSetOrientation

try:
    _magick.MagickSetOption.restype = MagickBooleanType
    _magick.MagickSetOption.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetOption = _magick.MagickSetOption

try:
    _magick.MagickSetInterpolateMethod.restype = MagickBooleanType
    _magick.MagickSetInterpolateMethod.argtypes = (MagickWand, InterpolatePixelMethod)
except AttributeError, e:
    print e
else:
    MagickSetInterpolateMethod = _magick.MagickSetInterpolateMethod

try:
    _magick.MagickSetInterlaceScheme.restype = MagickBooleanType
    _magick.MagickSetInterlaceScheme.argtypes = (MagickWand, InterlaceType)
except AttributeError, e:
    print e
else:
    MagickSetInterlaceScheme = _magick.MagickSetInterlaceScheme

try:
    _magick.MagickSetImageProperty.restype = MagickBooleanType
    _magick.MagickSetImageProperty.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetImageProperty = _magick.MagickSetImageProperty

try:
    _magick.MagickSetImageProfile.restype = MagickBooleanType
    _magick.MagickSetImageProfile.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetImageProfile = _magick.MagickSetImageProfile

try:
    _magick.MagickSetGravity.restype = MagickBooleanType
    _magick.MagickSetGravity.argtypes = (MagickWand, GravityType)
except AttributeError, e:
    print e
else:
    MagickSetGravity = _magick.MagickSetGravity

try:
    _magick.MagickSetFont.restype = MagickBooleanType
    _magick.MagickSetFont.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetFont = _magick.MagickSetFont

try:
    _magick.MagickSetFormat.restype = MagickBooleanType
    _magick.MagickSetFormat.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetFormat = _magick.MagickSetFormat

try:
    _magick.MagickSetFilename.restype = MagickBooleanType
    _magick.MagickSetFilename.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetFilename = _magick.MagickSetFilename

try:
    _magick.MagickSetDepth.restype = MagickBooleanType
    _magick.MagickSetDepth.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetDepth = _magick.MagickSetDepth

try:
    _magick.MagickSetCompressionQuality.restype = MagickBooleanType
    _magick.MagickSetCompressionQuality.argtypes = (MagickWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickSetCompressionQuality = _magick.MagickSetCompressionQuality

try:
    _magick.MagickSetCompression.restype = MagickBooleanType
    _magick.MagickSetCompression.argtypes = (MagickWand, CompressionType)
except AttributeError, e:
    print e
else:
    MagickSetCompression = _magick.MagickSetCompression

try:
    _magick.MagickSetBackgroundColor.restype = MagickBooleanType
    _magick.MagickSetBackgroundColor.argtypes = (MagickWand, PixelWand)
except AttributeError, e:
    print e
else:
    MagickSetBackgroundColor = _magick.MagickSetBackgroundColor

try:
    _magick.MagickSetAntialias.restype = MagickBooleanType
    _magick.MagickSetAntialias.argtypes = (MagickWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickSetAntialias = _magick.MagickSetAntialias

try:
    _magick.MagickProfileImage.restype = MagickBooleanType
    _magick.MagickProfileImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    MagickProfileImage = _magick.MagickProfileImage

try:
    _magick.MagickGetSizeOffset.restype = MagickBooleanType
    _magick.MagickGetSizeOffset.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_long))
except AttributeError, e:
    print e
else:
    MagickGetSizeOffset = _magick.MagickGetSizeOffset

try:
    _magick.MagickGetSize.restype = MagickBooleanType
    _magick.MagickGetSize.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetSize = _magick.MagickGetSize

try:
    _magick.MagickGetPage.restype = MagickBooleanType
    _magick.MagickGetPage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long))
except AttributeError, e:
    print e
else:
    MagickGetPage = _magick.MagickGetPage

try:
    _magick.MagickGetAntialias.restype = MagickBooleanType
    _magick.MagickGetAntialias.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetAntialias = _magick.MagickGetAntialias

try:
    _magick.MagickDeleteImageProperty.restype = MagickBooleanType
    _magick.MagickDeleteImageProperty.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickDeleteImageProperty = _magick.MagickDeleteImageProperty

try:
    _magick.MagickDeleteOption.restype = MagickBooleanType
    _magick.MagickDeleteOption.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickDeleteOption = _magick.MagickDeleteOption

try:
    _magick.MagickGetInterpolateMethod.restype = InterpolatePixelMethod
    _magick.MagickGetInterpolateMethod.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetInterpolateMethod = _magick.MagickGetInterpolateMethod

try:
    _magick.MagickGetInterlaceScheme.restype = InterlaceType
    _magick.MagickGetInterlaceScheme.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetInterlaceScheme = _magick.MagickGetInterlaceScheme

try:
    _magick.MagickGetType.restype = ImageType
    _magick.MagickGetType.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetType = _magick.MagickGetType

try:
    _magick.MagickGetGravity.restype = GravityType
    _magick.MagickGetGravity.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetGravity = _magick.MagickGetGravity

try:
    _magick.MagickQueryMultilineFontMetrics.restype = ctypes.POINTER(ctypes.c_double)
    _magick.MagickQueryMultilineFontMetrics.argtypes = (MagickWand, DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickQueryMultilineFontMetrics = _magick.MagickQueryMultilineFontMetrics

try:
    _magick.MagickQueryFontMetrics.restype = ctypes.POINTER(ctypes.c_double)
    _magick.MagickQueryFontMetrics.argtypes = (MagickWand, DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickQueryFontMetrics = _magick.MagickQueryFontMetrics

try:
    _magick.MagickGetSamplingFactors.restype = ctypes.POINTER(ctypes.c_double)
    _magick.MagickGetSamplingFactors.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetSamplingFactors = _magick.MagickGetSamplingFactors

try:
    _magick.MagickGetPointsize.restype = ctypes.c_double
    _magick.MagickGetPointsize.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetPointsize = _magick.MagickGetPointsize

try:
    _magick.MagickGetVersion.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetVersion.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    MagickGetVersion = _magick.MagickGetVersion

try:
    _magick.MagickGetReleaseDate.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetReleaseDate.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickGetReleaseDate = _magick.MagickGetReleaseDate

try:
    _magick.MagickGetQuantumRange.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetQuantumRange.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    MagickGetQuantumRange = _magick.MagickGetQuantumRange

try:
    _magick.MagickGetQuantumDepth.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetQuantumDepth.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    MagickGetQuantumDepth = _magick.MagickGetQuantumDepth

try:
    _magick.MagickGetPackageName.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetPackageName.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickGetPackageName = _magick.MagickGetPackageName

try:
    _magick.MagickGetCopyright.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetCopyright.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickGetCopyright = _magick.MagickGetCopyright

try:
    _magick.MagickGetCompression.restype = CompressionType
    _magick.MagickGetCompression.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetCompression = _magick.MagickGetCompression

try:
    _magick.MagickQueryFormats.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickQueryFormats.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickQueryFormats = _magick.MagickQueryFormats

try:
    _magick.MagickQueryFonts.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickQueryFonts.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickQueryFonts = _magick.MagickQueryFonts

try:
    _magick.MagickQueryConfigureOptions.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickQueryConfigureOptions.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickQueryConfigureOptions = _magick.MagickQueryConfigureOptions

try:
    _magick.MagickQueryConfigureOption.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickQueryConfigureOption.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    MagickQueryConfigureOption = _magick.MagickQueryConfigureOption

try:
    _magick.MagickGetOptions.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickGetOptions.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetOptions = _magick.MagickGetOptions

try:
    _magick.MagickGetOption.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetOption.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickGetOption = _magick.MagickGetOption

try:
    _magick.MagickGetImageProperties.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickGetImageProperties.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetImageProperties = _magick.MagickGetImageProperties

try:
    _magick.MagickGetImageProperty.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetImageProperty.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickGetImageProperty = _magick.MagickGetImageProperty

try:
    _magick.MagickGetImageProfiles.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.MagickGetImageProfiles.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetImageProfiles = _magick.MagickGetImageProfiles

try:
    _magick.MagickGetHomeURL.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetHomeURL.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickGetHomeURL = _magick.MagickGetHomeURL

try:
    _magick.MagickGetFont.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetFont.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetFont = _magick.MagickGetFont

try:
    _magick.MagickGetFormat.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetFormat.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetFormat = _magick.MagickGetFormat

try:
    _magick.MagickGetFilename.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetFilename.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetFilename = _magick.MagickGetFilename

try:
    _magick.DrawSetStrokeAlpha.restype = None
    _magick.DrawSetStrokeAlpha.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetStrokeAlpha = _magick.DrawSetStrokeAlpha

try:
    _magick.DrawSetFillAlpha.restype = None
    _magick.DrawSetFillAlpha.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetFillAlpha = _magick.DrawSetFillAlpha

try:
    _magick.DrawPushGraphicContext.restype = None
    _magick.DrawPushGraphicContext.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPushGraphicContext = _magick.DrawPushGraphicContext

try:
    _magick.DrawPopGraphicContext.restype = None
    _magick.DrawPopGraphicContext.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPopGraphicContext = _magick.DrawPopGraphicContext

try:
    _magick.MagickSetImageVirtualPixelMethod.restype = VirtualPixelMethod
    _magick.MagickSetImageVirtualPixelMethod.argtypes = (MagickWand, VirtualPixelMethod)
except AttributeError, e:
    print e
else:
    MagickSetImageVirtualPixelMethod = _magick.MagickSetImageVirtualPixelMethod

try:
    _magick.MagickWriteImageBlob.restype = ctypes.POINTER(ctypes.c_ubyte)
    _magick.MagickWriteImageBlob.argtypes = (MagickWand, size_t)
except AttributeError, e:
    print e
else:
    MagickWriteImageBlob = _magick.MagickWriteImageBlob

try:
    _magick.MagickGetImageSize.restype = MagickSizeType
    _magick.MagickGetImageSize.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageSize = _magick.MagickGetImageSize

try:
    _magick.MagickRegionOfInterestImage.restype = MagickWand
    _magick.MagickRegionOfInterestImage.argtypes = (MagickWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickRegionOfInterestImage = _magick.MagickRegionOfInterestImage

try:
    _magick.MagickMosaicImages.restype = MagickWand
    _magick.MagickMosaicImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickMosaicImages = _magick.MagickMosaicImages

try:
    _magick.MagickFlattenImages.restype = MagickWand
    _magick.MagickFlattenImages.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickFlattenImages = _magick.MagickFlattenImages

try:
    _magick.MagickTransparentImage.restype = MagickBooleanType
    _magick.MagickTransparentImage.argtypes = (MagickWand, PixelWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickTransparentImage = _magick.MagickTransparentImage

try:
    _magick.MagickSetImageOption.restype = MagickBooleanType
    _magick.MagickSetImageOption.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetImageOption = _magick.MagickSetImageOption

try:
    _magick.MagickSetImageIndex.restype = MagickBooleanType
    _magick.MagickSetImageIndex.argtypes = (MagickWand, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickSetImageIndex = _magick.MagickSetImageIndex

try:
    _magick.MagickSetImageAttribute.restype = MagickBooleanType
    _magick.MagickSetImageAttribute.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickSetImageAttribute = _magick.MagickSetImageAttribute

try:
    _magick.MagickOpaqueImage.restype = MagickBooleanType
    _magick.MagickOpaqueImage.argtypes = (MagickWand, PixelWand, PixelWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    MagickOpaqueImage = _magick.MagickOpaqueImage

try:
    _magick.MagickMatteFloodfillImage.restype = MagickBooleanType
    _magick.MagickMatteFloodfillImage.argtypes = (MagickWand, ctypes.c_double, ctypes.c_double, PixelWand, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickMatteFloodfillImage = _magick.MagickMatteFloodfillImage

try:
    _magick.MagickGetImageExtrema.restype = MagickBooleanType
    _magick.MagickGetImageExtrema.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetImageExtrema = _magick.MagickGetImageExtrema

try:
    _magick.MagickGetImageChannelExtrema.restype = MagickBooleanType
    _magick.MagickGetImageChannelExtrema.argtypes = (MagickWand, ChannelType, ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    MagickGetImageChannelExtrema = _magick.MagickGetImageChannelExtrema

try:
    _magick.MagickColorFloodfillImage.restype = MagickBooleanType
    _magick.MagickColorFloodfillImage.argtypes = (MagickWand, PixelWand, ctypes.c_double, PixelWand, ctypes.c_long, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickColorFloodfillImage = _magick.MagickColorFloodfillImage

try:
    _magick.MagickClipPathImage.restype = MagickBooleanType
    _magick.MagickClipPathImage.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char), MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickClipPathImage = _magick.MagickClipPathImage

try:
    _magick.MagickGetImageIndex.restype = ctypes.c_long
    _magick.MagickGetImageIndex.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickGetImageIndex = _magick.MagickGetImageIndex

try:
    _magick.MagickGetImageAttribute.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickGetImageAttribute.argtypes = (MagickWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickGetImageAttribute = _magick.MagickGetImageAttribute

try:
    _magick.MagickDescribeImage.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickDescribeImage.argtypes = (MagickWand,)
except AttributeError, e:
    print e
else:
    MagickDescribeImage = _magick.MagickDescribeImage

try:
    _magick.DrawPeekGraphicWand.restype = DrawInfo
    _magick.DrawPeekGraphicWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPeekGraphicWand = _magick.DrawPeekGraphicWand

try:
    _magick.DrawGetStrokeAlpha.restype = ctypes.c_double
    _magick.DrawGetStrokeAlpha.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeAlpha = _magick.DrawGetStrokeAlpha

try:
    _magick.DrawGetFillAlpha.restype = ctypes.c_double
    _magick.DrawGetFillAlpha.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFillAlpha = _magick.DrawGetFillAlpha

try:
    _magick.DrawTranslate.restype = None
    _magick.DrawTranslate.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawTranslate = _magick.DrawTranslate

try:
    _magick.DrawSkewY.restype = None
    _magick.DrawSkewY.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSkewY = _magick.DrawSkewY

try:
    _magick.DrawSkewX.restype = None
    _magick.DrawSkewX.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSkewX = _magick.DrawSkewX

try:
    _magick.DrawSetViewbox.restype = None
    _magick.DrawSetViewbox.argtypes = (DrawingWand, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    DrawSetViewbox = _magick.DrawSetViewbox

try:
    _magick.DrawSetTextUnderColor.restype = None
    _magick.DrawSetTextUnderColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawSetTextUnderColor = _magick.DrawSetTextUnderColor

try:
    _magick.DrawSetTextEncoding.restype = None
    _magick.DrawSetTextEncoding.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetTextEncoding = _magick.DrawSetTextEncoding

try:
    _magick.DrawSetTextDecoration.restype = None
    _magick.DrawSetTextDecoration.argtypes = (DrawingWand, DecorationType)
except AttributeError, e:
    print e
else:
    DrawSetTextDecoration = _magick.DrawSetTextDecoration

try:
    _magick.DrawSetTextAntialias.restype = None
    _magick.DrawSetTextAntialias.argtypes = (DrawingWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    DrawSetTextAntialias = _magick.DrawSetTextAntialias

try:
    _magick.DrawSetTextAlignment.restype = None
    _magick.DrawSetTextAlignment.argtypes = (DrawingWand, AlignType)
except AttributeError, e:
    print e
else:
    DrawSetTextAlignment = _magick.DrawSetTextAlignment

try:
    _magick.DrawSetStrokeWidth.restype = None
    _magick.DrawSetStrokeWidth.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetStrokeWidth = _magick.DrawSetStrokeWidth

try:
    _magick.DrawSetStrokeOpacity.restype = None
    _magick.DrawSetStrokeOpacity.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetStrokeOpacity = _magick.DrawSetStrokeOpacity

try:
    _magick.DrawSetStrokeMiterLimit.restype = None
    _magick.DrawSetStrokeMiterLimit.argtypes = (DrawingWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    DrawSetStrokeMiterLimit = _magick.DrawSetStrokeMiterLimit

try:
    _magick.DrawSetStrokeLineJoin.restype = None
    _magick.DrawSetStrokeLineJoin.argtypes = (DrawingWand, LineJoin)
except AttributeError, e:
    print e
else:
    DrawSetStrokeLineJoin = _magick.DrawSetStrokeLineJoin

try:
    _magick.DrawSetStrokeLineCap.restype = None
    _magick.DrawSetStrokeLineCap.argtypes = (DrawingWand, LineCap)
except AttributeError, e:
    print e
else:
    DrawSetStrokeLineCap = _magick.DrawSetStrokeLineCap

try:
    _magick.DrawSetStrokeDashOffset.restype = None
    _magick.DrawSetStrokeDashOffset.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetStrokeDashOffset = _magick.DrawSetStrokeDashOffset

try:
    _magick.DrawSetStrokeColor.restype = None
    _magick.DrawSetStrokeColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawSetStrokeColor = _magick.DrawSetStrokeColor

try:
    _magick.DrawSetStrokeAntialias.restype = None
    _magick.DrawSetStrokeAntialias.argtypes = (DrawingWand, MagickBooleanType)
except AttributeError, e:
    print e
else:
    DrawSetStrokeAntialias = _magick.DrawSetStrokeAntialias

try:
    _magick.DrawSetGravity.restype = None
    _magick.DrawSetGravity.argtypes = (DrawingWand, GravityType)
except AttributeError, e:
    print e
else:
    DrawSetGravity = _magick.DrawSetGravity

try:
    _magick.DrawSetFontWeight.restype = None
    _magick.DrawSetFontWeight.argtypes = (DrawingWand, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    DrawSetFontWeight = _magick.DrawSetFontWeight

try:
    _magick.DrawSetFontStyle.restype = None
    _magick.DrawSetFontStyle.argtypes = (DrawingWand, StyleType)
except AttributeError, e:
    print e
else:
    DrawSetFontStyle = _magick.DrawSetFontStyle

try:
    _magick.DrawSetFontStretch.restype = None
    _magick.DrawSetFontStretch.argtypes = (DrawingWand, StretchType)
except AttributeError, e:
    print e
else:
    DrawSetFontStretch = _magick.DrawSetFontStretch

try:
    _magick.DrawSetFontSize.restype = None
    _magick.DrawSetFontSize.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetFontSize = _magick.DrawSetFontSize

try:
    _magick.DrawSetFillRule.restype = None
    _magick.DrawSetFillRule.argtypes = (DrawingWand, FillRule)
except AttributeError, e:
    print e
else:
    DrawSetFillRule = _magick.DrawSetFillRule

try:
    _magick.DrawSetFillOpacity.restype = None
    _magick.DrawSetFillOpacity.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawSetFillOpacity = _magick.DrawSetFillOpacity

try:
    _magick.DrawSetFillColor.restype = None
    _magick.DrawSetFillColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawSetFillColor = _magick.DrawSetFillColor

try:
    _magick.DrawSetClipUnits.restype = None
    _magick.DrawSetClipUnits.argtypes = (DrawingWand, ClipPathUnits)
except AttributeError, e:
    print e
else:
    DrawSetClipUnits = _magick.DrawSetClipUnits

try:
    _magick.DrawSetClipRule.restype = None
    _magick.DrawSetClipRule.argtypes = (DrawingWand, FillRule)
except AttributeError, e:
    print e
else:
    DrawSetClipRule = _magick.DrawSetClipRule

try:
    _magick.DrawScale.restype = None
    _magick.DrawScale.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawScale = _magick.DrawScale

try:
    _magick.DrawRoundRectangle.restype = None
    _magick.DrawRoundRectangle.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawRoundRectangle = _magick.DrawRoundRectangle

try:
    _magick.DrawRotate.restype = None
    _magick.DrawRotate.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawRotate = _magick.DrawRotate

try:
    _magick.DrawResetVectorGraphics.restype = None
    _magick.DrawResetVectorGraphics.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawResetVectorGraphics = _magick.DrawResetVectorGraphics

try:
    _magick.DrawRectangle.restype = None
    _magick.DrawRectangle.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawRectangle = _magick.DrawRectangle

try:
    _magick.DrawPushDefs.restype = None
    _magick.DrawPushDefs.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPushDefs = _magick.DrawPushDefs

try:
    _magick.DrawPushClipPath.restype = None
    _magick.DrawPushClipPath.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawPushClipPath = _magick.DrawPushClipPath

try:
    _magick.DrawPopDefs.restype = None
    _magick.DrawPopDefs.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPopDefs = _magick.DrawPopDefs

try:
    _magick.DrawPopClipPath.restype = None
    _magick.DrawPopClipPath.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPopClipPath = _magick.DrawPopClipPath

try:
    _magick.DrawPolyline.restype = None
    _magick.DrawPolyline.argtypes = (DrawingWand, ctypes.c_ulong, PointInfo)
except AttributeError, e:
    print e
else:
    DrawPolyline = _magick.DrawPolyline

try:
    _magick.DrawPolygon.restype = None
    _magick.DrawPolygon.argtypes = (DrawingWand, ctypes.c_ulong, PointInfo)
except AttributeError, e:
    print e
else:
    DrawPolygon = _magick.DrawPolygon

try:
    _magick.DrawPoint.restype = None
    _magick.DrawPoint.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPoint = _magick.DrawPoint

try:
    _magick.DrawPathStart.restype = None
    _magick.DrawPathStart.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPathStart = _magick.DrawPathStart

try:
    _magick.DrawPathMoveToRelative.restype = None
    _magick.DrawPathMoveToRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathMoveToRelative = _magick.DrawPathMoveToRelative

try:
    _magick.DrawPathMoveToAbsolute.restype = None
    _magick.DrawPathMoveToAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathMoveToAbsolute = _magick.DrawPathMoveToAbsolute

try:
    _magick.DrawPathLineToVerticalRelative.restype = None
    _magick.DrawPathLineToVerticalRelative.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToVerticalRelative = _magick.DrawPathLineToVerticalRelative

try:
    _magick.DrawPathLineToVerticalAbsolute.restype = None
    _magick.DrawPathLineToVerticalAbsolute.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToVerticalAbsolute = _magick.DrawPathLineToVerticalAbsolute

try:
    _magick.DrawPathLineToHorizontalRelative.restype = None
    _magick.DrawPathLineToHorizontalRelative.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToHorizontalRelative = _magick.DrawPathLineToHorizontalRelative

try:
    _magick.DrawPathLineToHorizontalAbsolute.restype = None
    _magick.DrawPathLineToHorizontalAbsolute.argtypes = (DrawingWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToHorizontalAbsolute = _magick.DrawPathLineToHorizontalAbsolute

try:
    _magick.DrawPathLineToRelative.restype = None
    _magick.DrawPathLineToRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToRelative = _magick.DrawPathLineToRelative

try:
    _magick.DrawPathLineToAbsolute.restype = None
    _magick.DrawPathLineToAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathLineToAbsolute = _magick.DrawPathLineToAbsolute

try:
    _magick.DrawPathFinish.restype = None
    _magick.DrawPathFinish.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPathFinish = _magick.DrawPathFinish

try:
    _magick.DrawPathEllipticArcRelative.restype = None
    _magick.DrawPathEllipticArcRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, MagickBooleanType, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathEllipticArcRelative = _magick.DrawPathEllipticArcRelative

try:
    _magick.DrawPathEllipticArcAbsolute.restype = None
    _magick.DrawPathEllipticArcAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, MagickBooleanType, MagickBooleanType, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathEllipticArcAbsolute = _magick.DrawPathEllipticArcAbsolute

try:
    _magick.DrawPathCurveToSmoothRelative.restype = None
    _magick.DrawPathCurveToSmoothRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToSmoothRelative = _magick.DrawPathCurveToSmoothRelative

try:
    _magick.DrawPathCurveToSmoothAbsolute.restype = None
    _magick.DrawPathCurveToSmoothAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToSmoothAbsolute = _magick.DrawPathCurveToSmoothAbsolute

try:
    _magick.DrawPathCurveToQuadraticBezierSmoothRelative.restype = None
    _magick.DrawPathCurveToQuadraticBezierSmoothRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToQuadraticBezierSmoothRelative = _magick.DrawPathCurveToQuadraticBezierSmoothRelative

try:
    _magick.DrawPathCurveToQuadraticBezierSmoothAbsolute.restype = None
    _magick.DrawPathCurveToQuadraticBezierSmoothAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToQuadraticBezierSmoothAbsolute = _magick.DrawPathCurveToQuadraticBezierSmoothAbsolute

try:
    _magick.DrawPathCurveToQuadraticBezierRelative.restype = None
    _magick.DrawPathCurveToQuadraticBezierRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToQuadraticBezierRelative = _magick.DrawPathCurveToQuadraticBezierRelative

try:
    _magick.DrawPathCurveToQuadraticBezierAbsolute.restype = None
    _magick.DrawPathCurveToQuadraticBezierAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToQuadraticBezierAbsolute = _magick.DrawPathCurveToQuadraticBezierAbsolute

try:
    _magick.DrawPathCurveToRelative.restype = None
    _magick.DrawPathCurveToRelative.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToRelative = _magick.DrawPathCurveToRelative

try:
    _magick.DrawPathCurveToAbsolute.restype = None
    _magick.DrawPathCurveToAbsolute.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPathCurveToAbsolute = _magick.DrawPathCurveToAbsolute

try:
    _magick.DrawPathClose.restype = None
    _magick.DrawPathClose.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPathClose = _magick.DrawPathClose

try:
    _magick.DrawMatte.restype = None
    _magick.DrawMatte.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, PaintMethod)
except AttributeError, e:
    print e
else:
    DrawMatte = _magick.DrawMatte

try:
    _magick.DrawLine.restype = None
    _magick.DrawLine.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawLine = _magick.DrawLine

try:
    _magick.DrawGetTextUnderColor.restype = None
    _magick.DrawGetTextUnderColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawGetTextUnderColor = _magick.DrawGetTextUnderColor

try:
    _magick.DrawGetStrokeColor.restype = None
    _magick.DrawGetStrokeColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawGetStrokeColor = _magick.DrawGetStrokeColor

try:
    _magick.DrawGetFillColor.restype = None
    _magick.DrawGetFillColor.argtypes = (DrawingWand, PixelWand)
except AttributeError, e:
    print e
else:
    DrawGetFillColor = _magick.DrawGetFillColor

try:
    _magick.DrawEllipse.restype = None
    _magick.DrawEllipse.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawEllipse = _magick.DrawEllipse

try:
    _magick.DrawComment.restype = None
    _magick.DrawComment.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawComment = _magick.DrawComment

try:
    _magick.DrawColor.restype = None
    _magick.DrawColor.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, PaintMethod)
except AttributeError, e:
    print e
else:
    DrawColor = _magick.DrawColor

try:
    _magick.DrawCircle.restype = None
    _magick.DrawCircle.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawCircle = _magick.DrawCircle

try:
    _magick.DrawBezier.restype = None
    _magick.DrawBezier.argtypes = (DrawingWand, ctypes.c_ulong, PointInfo)
except AttributeError, e:
    print e
else:
    DrawBezier = _magick.DrawBezier

try:
    _magick.DrawArc.restype = None
    _magick.DrawArc.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawArc = _magick.DrawArc

try:
    _magick.DrawAnnotation.restype = None
    _magick.DrawAnnotation.argtypes = (DrawingWand, ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_ubyte))
except AttributeError, e:
    print e
else:
    DrawAnnotation = _magick.DrawAnnotation

try:
    _magick.DrawAffine.restype = None
    _magick.DrawAffine.argtypes = (DrawingWand, AffineMatrix)
except AttributeError, e:
    print e
else:
    DrawAffine = _magick.DrawAffine

try:
    _magick.ClearDrawingWand.restype = None
    _magick.ClearDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    ClearDrawingWand = _magick.ClearDrawingWand

try:
    _magick.DrawGetStrokeMiterLimit.restype = ctypes.c_ulong
    _magick.DrawGetStrokeMiterLimit.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeMiterLimit = _magick.DrawGetStrokeMiterLimit

try:
    _magick.DrawGetFontWeight.restype = ctypes.c_ulong
    _magick.DrawGetFontWeight.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFontWeight = _magick.DrawGetFontWeight

try:
    _magick.DrawGetFontStyle.restype = StyleType
    _magick.DrawGetFontStyle.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFontStyle = _magick.DrawGetFontStyle

try:
    _magick.DrawGetFontStretch.restype = StretchType
    _magick.DrawGetFontStretch.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFontStretch = _magick.DrawGetFontStretch

try:
    _magick.PushDrawingWand.restype = MagickBooleanType
    _magick.PushDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    PushDrawingWand = _magick.PushDrawingWand

try:
    _magick.PopDrawingWand.restype = MagickBooleanType
    _magick.PopDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    PopDrawingWand = _magick.PopDrawingWand

try:
    _magick.IsDrawingWand.restype = MagickBooleanType
    _magick.IsDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    IsDrawingWand = _magick.IsDrawingWand

try:
    _magick.DrawSetVectorGraphics.restype = MagickBooleanType
    _magick.DrawSetVectorGraphics.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetVectorGraphics = _magick.DrawSetVectorGraphics

try:
    _magick.DrawSetStrokePatternURL.restype = MagickBooleanType
    _magick.DrawSetStrokePatternURL.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetStrokePatternURL = _magick.DrawSetStrokePatternURL

try:
    _magick.DrawSetStrokeDashArray.restype = MagickBooleanType
    _magick.DrawSetStrokeDashArray.argtypes = (DrawingWand, ctypes.c_ulong, ctypes.POINTER(ctypes.c_double))
except AttributeError, e:
    print e
else:
    DrawSetStrokeDashArray = _magick.DrawSetStrokeDashArray

try:
    _magick.DrawSetFontFamily.restype = MagickBooleanType
    _magick.DrawSetFontFamily.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetFontFamily = _magick.DrawSetFontFamily

try:
    _magick.DrawSetFont.restype = MagickBooleanType
    _magick.DrawSetFont.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetFont = _magick.DrawSetFont

try:
    _magick.DrawSetFillPatternURL.restype = MagickBooleanType
    _magick.DrawSetFillPatternURL.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetFillPatternURL = _magick.DrawSetFillPatternURL

try:
    _magick.DrawSetClipPath.restype = MagickBooleanType
    _magick.DrawSetClipPath.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawSetClipPath = _magick.DrawSetClipPath

try:
    _magick.DrawRender.restype = MagickBooleanType
    _magick.DrawRender.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawRender = _magick.DrawRender

try:
    _magick.DrawPushPattern.restype = MagickBooleanType
    _magick.DrawPushPattern.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_char), ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)
except AttributeError, e:
    print e
else:
    DrawPushPattern = _magick.DrawPushPattern

try:
    _magick.DrawPopPattern.restype = MagickBooleanType
    _magick.DrawPopPattern.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawPopPattern = _magick.DrawPopPattern

try:
    _magick.DrawGetTextAntialias.restype = MagickBooleanType
    _magick.DrawGetTextAntialias.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetTextAntialias = _magick.DrawGetTextAntialias

try:
    _magick.DrawGetStrokeAntialias.restype = MagickBooleanType
    _magick.DrawGetStrokeAntialias.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeAntialias = _magick.DrawGetStrokeAntialias

try:
    _magick.DrawComposite.restype = MagickBooleanType
    _magick.DrawComposite.argtypes = (DrawingWand, CompositeOperator, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, MagickWand)
except AttributeError, e:
    print e
else:
    DrawComposite = _magick.DrawComposite

try:
    _magick.DrawClearException.restype = MagickBooleanType
    _magick.DrawClearException.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawClearException = _magick.DrawClearException

try:
    _magick.DrawGetStrokeLineJoin.restype = LineJoin
    _magick.DrawGetStrokeLineJoin.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeLineJoin = _magick.DrawGetStrokeLineJoin

try:
    _magick.DrawGetStrokeLineCap.restype = LineCap
    _magick.DrawGetStrokeLineCap.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeLineCap = _magick.DrawGetStrokeLineCap

try:
    _magick.DrawGetGravity.restype = GravityType
    _magick.DrawGetGravity.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetGravity = _magick.DrawGetGravity

try:
    _magick.DrawGetFillRule.restype = FillRule
    _magick.DrawGetFillRule.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFillRule = _magick.DrawGetFillRule

try:
    _magick.DrawGetClipRule.restype = FillRule
    _magick.DrawGetClipRule.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetClipRule = _magick.DrawGetClipRule

try:
    _magick.DrawGetExceptionType.restype = ExceptionType
    _magick.DrawGetExceptionType.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetExceptionType = _magick.DrawGetExceptionType

try:
    _magick.NewDrawingWand.restype = DrawingWand
    _magick.NewDrawingWand.argtypes = ()
except AttributeError, e:
    print e
else:
    NewDrawingWand = _magick.NewDrawingWand

try:
    _magick.DrawAllocateWand.restype = DrawingWand
    _magick.DrawAllocateWand.argtypes = (DrawInfo, Image)
except AttributeError, e:
    print e
else:
    DrawAllocateWand = _magick.DrawAllocateWand

try:
    _magick.DestroyDrawingWand.restype = DrawingWand
    _magick.DestroyDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DestroyDrawingWand = _magick.DestroyDrawingWand

try:
    _magick.CloneDrawingWand.restype = DrawingWand
    _magick.CloneDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    CloneDrawingWand = _magick.CloneDrawingWand

try:
    _magick.PeekDrawingWand.restype = DrawInfo
    _magick.PeekDrawingWand.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    PeekDrawingWand = _magick.PeekDrawingWand

try:
    _magick.DrawGetStrokeWidth.restype = ctypes.c_double
    _magick.DrawGetStrokeWidth.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeWidth = _magick.DrawGetStrokeWidth

try:
    _magick.DrawGetStrokeOpacity.restype = ctypes.c_double
    _magick.DrawGetStrokeOpacity.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeOpacity = _magick.DrawGetStrokeOpacity

try:
    _magick.DrawGetStrokeDashOffset.restype = ctypes.c_double
    _magick.DrawGetStrokeDashOffset.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetStrokeDashOffset = _magick.DrawGetStrokeDashOffset

try:
    _magick.DrawGetStrokeDashArray.restype = ctypes.POINTER(ctypes.c_double)
    _magick.DrawGetStrokeDashArray.argtypes = (DrawingWand, ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    DrawGetStrokeDashArray = _magick.DrawGetStrokeDashArray

try:
    _magick.DrawGetFontSize.restype = ctypes.c_double
    _magick.DrawGetFontSize.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFontSize = _magick.DrawGetFontSize

try:
    _magick.DrawGetFillOpacity.restype = ctypes.c_double
    _magick.DrawGetFillOpacity.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFillOpacity = _magick.DrawGetFillOpacity

try:
    _magick.DrawGetTextDecoration.restype = DecorationType
    _magick.DrawGetTextDecoration.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetTextDecoration = _magick.DrawGetTextDecoration

try:
    _magick.DrawGetClipUnits.restype = ClipPathUnits
    _magick.DrawGetClipUnits.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetClipUnits = _magick.DrawGetClipUnits

try:
    _magick.DrawGetVectorGraphics.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetVectorGraphics.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetVectorGraphics = _magick.DrawGetVectorGraphics

try:
    _magick.DrawGetTextEncoding.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetTextEncoding.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetTextEncoding = _magick.DrawGetTextEncoding

try:
    _magick.DrawGetFontFamily.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetFontFamily.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFontFamily = _magick.DrawGetFontFamily

try:
    _magick.DrawGetFont.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetFont.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetFont = _magick.DrawGetFont

try:
    _magick.DrawGetException.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetException.argtypes = (DrawingWand, ctypes.POINTER(ExceptionType))
except AttributeError, e:
    print e
else:
    DrawGetException = _magick.DrawGetException

try:
    _magick.DrawGetClipPath.restype = ctypes.POINTER(ctypes.c_char)
    _magick.DrawGetClipPath.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetClipPath = _magick.DrawGetClipPath

try:
    _magick.DrawGetTextAlignment.restype = AlignType
    _magick.DrawGetTextAlignment.argtypes = (DrawingWand,)
except AttributeError, e:
    print e
else:
    DrawGetTextAlignment = _magick.DrawGetTextAlignment

try:
    _magick.PixelSetMagickColor.restype = None
    _magick.PixelSetMagickColor.argtypes = (PixelWand, MagickPixelPacket)
except AttributeError, e:
    print e
else:
    PixelSetMagickColor = _magick.PixelSetMagickColor

try:
    _magick.PixelSetColorFromWand.restype = None
    _magick.PixelSetColorFromWand.argtypes = (PixelWand, PixelWand)
except AttributeError, e:
    print e
else:
    PixelSetColorFromWand = _magick.PixelSetColorFromWand

try:
    _magick.PixelGetMagickColor.restype = None
    _magick.PixelGetMagickColor.argtypes = (PixelWand, MagickPixelPacket)
except AttributeError, e:
    print e
else:
    PixelGetMagickColor = _magick.PixelGetMagickColor

try:
    _magick.ClearPixelWand.restype = None
    _magick.ClearPixelWand.argtypes = (PixelWand,)
except AttributeError, e:
    print e
else:
    ClearPixelWand = _magick.ClearPixelWand

try:
    _magick.NewPixelWands.restype = ctypes.POINTER(PixelWand)
    _magick.NewPixelWands.argtypes = (ctypes.c_ulong,)
except AttributeError, e:
    print e
else:
    NewPixelWands = _magick.NewPixelWands

try:
    _magick.NewPixelWand.restype = PixelWand
    _magick.NewPixelWand.argtypes = ()
except AttributeError, e:
    print e
else:
    NewPixelWand = _magick.NewPixelWand

try:
    _magick.DestroyPixelWands.restype = ctypes.POINTER(PixelWand)
    _magick.DestroyPixelWands.argtypes = (ctypes.POINTER(PixelWand), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    DestroyPixelWands = _magick.DestroyPixelWands

try:
    _magick.DestroyPixelWand.restype = PixelWand
    _magick.DestroyPixelWand.argtypes = (PixelWand,)
except AttributeError, e:
    print e
else:
    DestroyPixelWand = _magick.DestroyPixelWand

try:
    _magick.ClonePixelWands.restype = ctypes.POINTER(PixelWand)
    _magick.ClonePixelWands.argtypes = (ctypes.POINTER(PixelWand), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    ClonePixelWands = _magick.ClonePixelWands

try:
    _magick.ClonePixelWand.restype = PixelWand
    _magick.ClonePixelWand.argtypes = (PixelWand,)
except AttributeError, e:
    print e
else:
    ClonePixelWand = _magick.ClonePixelWand

try:
    _magick.IsPixelWandSimilar.restype = MagickBooleanType
    _magick.IsPixelWandSimilar.argtypes = (PixelWand, PixelWand, ctypes.c_double)
except AttributeError, e:
    print e
else:
    IsPixelWandSimilar = _magick.IsPixelWandSimilar

try:
    _magick.IsPixelWand.restype = MagickBooleanType
    _magick.IsPixelWand.argtypes = (PixelWand,)
except AttributeError, e:
    print e
else:
    IsPixelWand = _magick.IsPixelWand

try:
    _magick.IsMagickTrue.restype = MagickBooleanType
    _magick.IsMagickTrue.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    IsMagickTrue = _magick.IsMagickTrue

try:
    _magick.MagickOpenStream.restype = FILE
    _magick.MagickOpenStream.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickOpenStream = _magick.MagickOpenStream

try:
    _magick.GetMagickToken.restype = None
    _magick.GetMagickToken.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    GetMagickToken = _magick.GetMagickToken

try:
    _magick.RelinquishMagickResource.restype = None
    _magick.RelinquishMagickResource.argtypes = (ResourceType, ctypes.c_ulonglong)
except AttributeError, e:
    print e
else:
    RelinquishMagickResource = _magick.RelinquishMagickResource

try:
    _magick.InitializeMagickResources.restype = None
    _magick.InitializeMagickResources.argtypes = ()
except AttributeError, e:
    print e
else:
    InitializeMagickResources = _magick.InitializeMagickResources

try:
    _magick.DestroyMagickResources.restype = None
    _magick.DestroyMagickResources.argtypes = ()
except AttributeError, e:
    print e
else:
    DestroyMagickResources = _magick.DestroyMagickResources

try:
    _magick.AsynchronousDestroyMagickResources.restype = None
    _magick.AsynchronousDestroyMagickResources.argtypes = ()
except AttributeError, e:
    print e
else:
    AsynchronousDestroyMagickResources = _magick.AsynchronousDestroyMagickResources

try:
    _magick.GetMagickResourceLimit.restype = MagickSizeType
    _magick.GetMagickResourceLimit.argtypes = (ResourceType,)
except AttributeError, e:
    print e
else:
    GetMagickResourceLimit = _magick.GetMagickResourceLimit

try:
    _magick.GetMagickResource.restype = MagickSizeType
    _magick.GetMagickResource.argtypes = (ResourceType,)
except AttributeError, e:
    print e
else:
    GetMagickResource = _magick.GetMagickResource

try:
    _magick.SetMagickResourceLimit.restype = MagickBooleanType
    _magick.SetMagickResourceLimit.argtypes = (ResourceType, ctypes.c_ulonglong)
except AttributeError, e:
    print e
else:
    SetMagickResourceLimit = _magick.SetMagickResourceLimit

try:
    _magick.ListMagickResourceInfo.restype = MagickBooleanType
    _magick.ListMagickResourceInfo.argtypes = (FILE, ExceptionInfo)
except AttributeError, e:
    print e
else:
    ListMagickResourceInfo = _magick.ListMagickResourceInfo

try:
    _magick.AcquireMagickResource.restype = MagickBooleanType
    _magick.AcquireMagickResource.argtypes = (ResourceType, ctypes.c_ulonglong)
except AttributeError, e:
    print e
else:
    AcquireMagickResource = _magick.AcquireMagickResource

try:
    _magick.ListMagickOptions.restype = MagickBooleanType
    _magick.ListMagickOptions.argtypes = (FILE, MagickOption, ExceptionInfo)
except AttributeError, e:
    print e
else:
    ListMagickOptions = _magick.ListMagickOptions

try:
    _magick.IsMagickOption.restype = MagickBooleanType
    _magick.IsMagickOption.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    IsMagickOption = _magick.IsMagickOption

try:
    _magick.ParseMagickOption.restype = ctypes.c_long
    _magick.ParseMagickOption.argtypes = (MagickOption, MagickBooleanType, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    ParseMagickOption = _magick.ParseMagickOption

try:
    _magick.MagickOptionToMnemonic.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickOptionToMnemonic.argtypes = (MagickOption, ctypes.c_long)
except AttributeError, e:
    print e
else:
    MagickOptionToMnemonic = _magick.MagickOptionToMnemonic

try:
    _magick.GetMagickOptions.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.GetMagickOptions.argtypes = (MagickOption,)
except AttributeError, e:
    print e
else:
    GetMagickOptions = _magick.GetMagickOptions

try:
    _magick.MagickToMime.restype = ctypes.POINTER(ctypes.c_char)
    _magick.MagickToMime.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    MagickToMime = _magick.MagickToMime

try:
    _magick.GetMagickVersion.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickVersion.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    GetMagickVersion = _magick.GetMagickVersion

try:
    _magick.GetMagickReleaseDate.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickReleaseDate.argtypes = ()
except AttributeError, e:
    print e
else:
    GetMagickReleaseDate = _magick.GetMagickReleaseDate

try:
    _magick.GetMagickQuantumRange.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickQuantumRange.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    GetMagickQuantumRange = _magick.GetMagickQuantumRange

try:
    _magick.GetMagickQuantumDepth.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickQuantumDepth.argtypes = (ctypes.POINTER(ctypes.c_ulong),)
except AttributeError, e:
    print e
else:
    GetMagickQuantumDepth = _magick.GetMagickQuantumDepth

try:
    _magick.GetMagickPackageName.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickPackageName.argtypes = ()
except AttributeError, e:
    print e
else:
    GetMagickPackageName = _magick.GetMagickPackageName

try:
    _magick.GetMagickCopyright.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickCopyright.argtypes = ()
except AttributeError, e:
    print e
else:
    GetMagickCopyright = _magick.GetMagickCopyright

try:
    _magick.GetMagickHomeURL.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickHomeURL.argtypes = ()
except AttributeError, e:
    print e
else:
    GetMagickHomeURL = _magick.GetMagickHomeURL

try:
    _magick.ResizeMagickMemory.restype = ctypes.c_void_p
    _magick.ResizeMagickMemory.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    ResizeMagickMemory = _magick.ResizeMagickMemory

try:
    _magick.ResetMagickMemory.restype = ctypes.c_void_p
    _magick.ResetMagickMemory.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    ResetMagickMemory = _magick.ResetMagickMemory

try:
    _magick.RelinquishMagickMemory.restype = ctypes.c_void_p
    _magick.RelinquishMagickMemory.argtypes = (ctypes.c_void_p,)
except AttributeError, e:
    print e
else:
    RelinquishMagickMemory = _magick.RelinquishMagickMemory

try:
    _magick.DestroyMagickMemory.restype = None
    _magick.DestroyMagickMemory.argtypes = ()
except AttributeError, e:
    print e
else:
    DestroyMagickMemory = _magick.DestroyMagickMemory

try:
    _magick.CopyMagickMemory.restype = ctypes.c_void_p
    _magick.CopyMagickMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    CopyMagickMemory = _magick.CopyMagickMemory

try:
    _magick.AcquireMagickMemory.restype = ctypes.c_void_p
    _magick.AcquireMagickMemory.argtypes = (ctypes.c_ulong,)
except AttributeError, e:
    print e
else:
    AcquireMagickMemory = _magick.AcquireMagickMemory

try:
    _magick.RelinquishMagickMatrix.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
    _magick.RelinquishMagickMatrix.argtypes = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    RelinquishMagickMatrix = _magick.RelinquishMagickMatrix

try:
    _magick.AcquireMagickMatrix.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
    _magick.AcquireMagickMatrix.argtypes = (ctypes.c_ulong, ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    AcquireMagickMatrix = _magick.AcquireMagickMatrix

try:
    _magick.MagickCoreTerminus.restype = None
    _magick.MagickCoreTerminus.argtypes = ()
except AttributeError, e:
    print e
else:
    MagickCoreTerminus = _magick.MagickCoreTerminus

try:
    _magick.MagickCoreGenesis.restype = None
    _magick.MagickCoreGenesis.argtypes = (ctypes.POINTER(ctypes.c_char), MagickBooleanType)
except AttributeError, e:
    print e
else:
    MagickCoreGenesis = _magick.MagickCoreGenesis

try:
    _magick.DestroyMagickList.restype = None
    _magick.DestroyMagickList.argtypes = ()
except AttributeError, e:
    print e
else:
    DestroyMagickList = _magick.DestroyMagickList

try:
    _magick.GetMagickThreadSupport.restype = MagickStatusType
    _magick.GetMagickThreadSupport.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickThreadSupport = _magick.GetMagickThreadSupport

try:
    _magick.SetMagickInfo.restype = MagickInfo
    _magick.SetMagickInfo.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    SetMagickInfo = _magick.SetMagickInfo

try:
    _magick.RegisterMagickInfo.restype = MagickInfo
    _magick.RegisterMagickInfo.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    RegisterMagickInfo = _magick.RegisterMagickInfo

try:
    _magick.GetMagickInfoList.restype = ctypes.POINTER(MagickInfo)
    _magick.GetMagickInfoList.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong), ExceptionInfo)
except AttributeError, e:
    print e
else:
    GetMagickInfoList = _magick.GetMagickInfoList

try:
    _magick.GetMagickInfo.restype = MagickInfo
    _magick.GetMagickInfo.argtypes = (ctypes.POINTER(ctypes.c_char), ExceptionInfo)
except AttributeError, e:
    print e
else:
    GetMagickInfo = _magick.GetMagickInfo

try:
    _magick.UnregisterMagickInfo.restype = MagickBooleanType
    _magick.UnregisterMagickInfo.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    UnregisterMagickInfo = _magick.UnregisterMagickInfo

try:
    _magick.IsMagickInstantiated.restype = MagickBooleanType
    _magick.IsMagickInstantiated.argtypes = ()
except AttributeError, e:
    print e
else:
    IsMagickInstantiated = _magick.IsMagickInstantiated

try:
    _magick.GetMagickSeekableStream.restype = MagickBooleanType
    _magick.GetMagickSeekableStream.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickSeekableStream = _magick.GetMagickSeekableStream

try:
    _magick.GetMagickEndianSupport.restype = MagickBooleanType
    _magick.GetMagickEndianSupport.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickEndianSupport = _magick.GetMagickEndianSupport

try:
    _magick.GetMagickBlobSupport.restype = MagickBooleanType
    _magick.GetMagickBlobSupport.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickBlobSupport = _magick.GetMagickBlobSupport

try:
    _magick.GetMagickAdjoin.restype = MagickBooleanType
    _magick.GetMagickAdjoin.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickAdjoin = _magick.GetMagickAdjoin

try:
    _magick.GetMagickDescription.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetMagickDescription.argtypes = (MagickInfo,)
except AttributeError, e:
    print e
else:
    GetMagickDescription = _magick.GetMagickDescription

try:
    _magick.GetImageMagick.restype = ctypes.POINTER(ctypes.c_char)
    _magick.GetImageMagick.argtypes = (ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    GetImageMagick = _magick.GetImageMagick

try:
    _magick.GetMagickList.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
    _magick.GetMagickList.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_ulong), ExceptionInfo)
except AttributeError, e:
    print e
else:
    GetMagickList = _magick.GetMagickList

try:
    _magick.LogMagickEventList.restype = MagickBooleanType
    _magick.LogMagickEventList.argtypes = (LogEventType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    LogMagickEventList = _magick.LogMagickEventList

try:
    _magick.LogMagickEvent.restype = MagickBooleanType
    _magick.LogMagickEvent.argtypes = (LogEventType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    LogMagickEvent = _magick.LogMagickEvent

try:
    _magick.InitializeMagick.restype = None
    _magick.InitializeMagick.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    InitializeMagick = _magick.InitializeMagick

try:
    _magick.GetMagickRegistry.restype = ctypes.c_void_p
    _magick.GetMagickRegistry.argtypes = (ctypes.c_long, ctypes.POINTER(RegistryType), size_t, ExceptionInfo)
except AttributeError, e:
    print e
else:
    GetMagickRegistry = _magick.GetMagickRegistry

try:
    _magick.DestroyMagickRegistry.restype = None
    _magick.DestroyMagickRegistry.argtypes = ()
except AttributeError, e:
    print e
else:
    DestroyMagickRegistry = _magick.DestroyMagickRegistry

try:
    _magick.DestroyMagick.restype = None
    _magick.DestroyMagick.argtypes = ()
except AttributeError, e:
    print e
else:
    DestroyMagick = _magick.DestroyMagick

try:
    _magick.GetMagickGeometry.restype = ctypes.c_uint
    _magick.GetMagickGeometry.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_ulong))
except AttributeError, e:
    print e
else:
    GetMagickGeometry = _magick.GetMagickGeometry

try:
    _magick.MagickMonitor.restype = MagickBooleanType
    _magick.MagickMonitor.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_longlong, ctypes.c_ulonglong, ctypes.c_void_p)
except AttributeError, e:
    print e
else:
    MagickMonitor = _magick.MagickMonitor

try:
    _magick.DeleteMagickRegistry.restype = MagickBooleanType
    _magick.DeleteMagickRegistry.argtypes = (ctypes.c_long,)
except AttributeError, e:
    print e
else:
    DeleteMagickRegistry = _magick.DeleteMagickRegistry

try:
    _magick.SetMagickRegistry.restype = ctypes.c_long
    _magick.SetMagickRegistry.argtypes = (RegistryType, ctypes.c_void_p, ctypes.c_ulong, ExceptionInfo)
except AttributeError, e:
    print e
else:
    SetMagickRegistry = _magick.SetMagickRegistry

try:
    _magick.GetImageFromMagickRegistry.restype = Image
    _magick.GetImageFromMagickRegistry.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_long), ExceptionInfo)
except AttributeError, e:
    print e
else:
    GetImageFromMagickRegistry = _magick.GetImageFromMagickRegistry

try:
    _magick.FormatMagickCaption.restype = ctypes.c_long
    _magick.FormatMagickCaption.argtypes = (Image, DrawInfo, ctypes.POINTER(ctypes.c_char), TypeMetric)
except AttributeError, e:
    print e
else:
    FormatMagickCaption = _magick.FormatMagickCaption

try:
    _magick.GetDrawInfo.restype = None
    _magick.GetDrawInfo.argtypes = (ImageInfo, DrawInfo)
except AttributeError, e:
    print e
else:
    GetDrawInfo = _magick.GetDrawInfo

try:
    _magick.DrawPrimitive.restype = MagickBooleanType
    _magick.DrawPrimitive.argtypes = (Image, DrawInfo, PrimitiveInfo)
except AttributeError, e:
    print e
else:
    DrawPrimitive = _magick.DrawPrimitive

try:
    _magick.DrawPatternPath.restype = MagickBooleanType
    _magick.DrawPatternPath.argtypes = (Image, DrawInfo, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(Image))
except AttributeError, e:
    print e
else:
    DrawPatternPath = _magick.DrawPatternPath

try:
    _magick.DrawImage.restype = MagickBooleanType
    _magick.DrawImage.argtypes = (Image, DrawInfo)
except AttributeError, e:
    print e
else:
    DrawImage = _magick.DrawImage

try:
    _magick.DrawGradientImage.restype = MagickBooleanType
    _magick.DrawGradientImage.argtypes = (Image, DrawInfo)
except AttributeError, e:
    print e
else:
    DrawGradientImage = _magick.DrawGradientImage

try:
    _magick.DrawClipPath.restype = MagickBooleanType
    _magick.DrawClipPath.argtypes = (Image, DrawInfo, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    DrawClipPath = _magick.DrawClipPath

try:
    _magick.DrawAffineImage.restype = MagickBooleanType
    _magick.DrawAffineImage.argtypes = (Image, Image, AffineMatrix)
except AttributeError, e:
    print e
else:
    DrawAffineImage = _magick.DrawAffineImage

try:
    _magick.DestroyDrawInfo.restype = DrawInfo
    _magick.DestroyDrawInfo.argtypes = (DrawInfo,)
except AttributeError, e:
    print e
else:
    DestroyDrawInfo = _magick.DestroyDrawInfo

try:
    _magick.CloneDrawInfo.restype = DrawInfo
    _magick.CloneDrawInfo.argtypes = (ImageInfo, DrawInfo)
except AttributeError, e:
    print e
else:
    CloneDrawInfo = _magick.CloneDrawInfo

try:
    _magick.AcquireDrawInfo.restype = DrawInfo
    _magick.AcquireDrawInfo.argtypes = ()
except AttributeError, e:
    print e
else:
    AcquireDrawInfo = _magick.AcquireDrawInfo

try:
    _magick.AcquireOneMagickPixel.restype = MagickPixelPacket
    _magick.AcquireOneMagickPixel.argtypes = (Image, ctypes.c_long, ctypes.c_long, ExceptionInfo)
except AttributeError, e:
    print e
else:
    AcquireOneMagickPixel = _magick.AcquireOneMagickPixel

try:
    _magick.ListMagickInfo.restype = MagickBooleanType
    _magick.ListMagickInfo.argtypes = (FILE, ExceptionInfo)
except AttributeError, e:
    print e
else:
    ListMagickInfo = _magick.ListMagickInfo

try:
    _magick.IsMagickConflict.restype = MagickBooleanType
    _magick.IsMagickConflict.argtypes = (ctypes.POINTER(ctypes.c_char),)
except AttributeError, e:
    print e
else:
    IsMagickConflict = _magick.IsMagickConflict

try:
    _magick.NewMagickImage.restype = Image
    _magick.NewMagickImage.argtypes = (ImageInfo, ctypes.c_ulong, ctypes.c_ulong, MagickPixelPacket)
except AttributeError, e:
    print e
else:
    NewMagickImage = _magick.NewMagickImage

try:
    _magick.CopyMagickString.restype = size_t
    _magick.CopyMagickString.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    CopyMagickString = _magick.CopyMagickString

try:
    _magick.ConcatenateMagickString.restype = size_t
    _magick.ConcatenateMagickString.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong)
except AttributeError, e:
    print e
else:
    ConcatenateMagickString = _magick.ConcatenateMagickString

try:
    _magick.FormatMagickTime.restype = ctypes.c_long
    _magick.FormatMagickTime.argtypes = (ctypes.c_long, ctypes.c_ulong, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    FormatMagickTime = _magick.FormatMagickTime

try:
    _magick.FormatMagickStringList.restype = ctypes.c_long
    _magick.FormatMagickStringList.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    FormatMagickStringList = _magick.FormatMagickStringList

try:
    _magick.FormatMagickString.restype = ctypes.c_long
    _magick.FormatMagickString.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    FormatMagickString = _magick.FormatMagickString

try:
    _magick.FormatMagickSize.restype = ctypes.c_long
    _magick.FormatMagickSize.argtypes = (ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    FormatMagickSize = _magick.FormatMagickSize

try:
    _magick.QueryMagickColorname.restype = MagickBooleanType
    _magick.QueryMagickColorname.argtypes = (Image, MagickPixelPacket, ComplianceType, MagickBooleanType, ctypes.POINTER(ctypes.c_char), ExceptionInfo)
except AttributeError, e:
    print e
else:
    QueryMagickColorname = _magick.QueryMagickColorname

try:
    _magick.QueryMagickColor.restype = MagickBooleanType
    _magick.QueryMagickColor.argtypes = (ctypes.POINTER(ctypes.c_char), MagickPixelPacket, ExceptionInfo)
except AttributeError, e:
    print e
else:
    QueryMagickColor = _magick.QueryMagickColor

try:
    _magick.IsMagickColorSimilar.restype = MagickBooleanType
    _magick.IsMagickColorSimilar.argtypes = (MagickPixelPacket, MagickPixelPacket)
except AttributeError, e:
    print e
else:
    IsMagickColorSimilar = _magick.IsMagickColorSimilar

try:
    _magick.MagickWarning.restype = None
    _magick.MagickWarning.argtypes = (ExceptionType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickWarning = _magick.MagickWarning

try:
    _magick.MagickFatalError.restype = None
    _magick.MagickFatalError.argtypes = (ExceptionType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickFatalError = _magick.MagickFatalError

try:
    _magick.MagickError.restype = None
    _magick.MagickError.argtypes = (ExceptionType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    MagickError = _magick.MagickError

try:
    _magick.ClearMagickException.restype = None
    _magick.ClearMagickException.argtypes = (ExceptionInfo,)
except AttributeError, e:
    print e
else:
    ClearMagickException = _magick.ClearMagickException

try:
    _magick.ThrowMagickExceptionList.restype = MagickBooleanType
    _magick.ThrowMagickExceptionList.argtypes = (ExceptionInfo, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ExceptionType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    ThrowMagickExceptionList = _magick.ThrowMagickExceptionList

try:
    _magick.ThrowMagickException.restype = MagickBooleanType
    _magick.ThrowMagickException.argtypes = (ExceptionInfo, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.c_ulong, ExceptionType, ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))
except AttributeError, e:
    print e
else:
    ThrowMagickException = _magick.ThrowMagickException

try:
    _magick.GetMagickPixelPacket.restype = None
    _magick.GetMagickPixelPacket.argtypes = (Image, MagickPixelPacket)
except AttributeError, e:
    print e
else:
    GetMagickPixelPacket = _magick.GetMagickPixelPacket

if __name__ == '__main__':
    import doctest
    doctest.testmod()
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/lib/EXIF.py
# Compiled at: 2009-09-04 10:38:20


def make_string(seq):
    str = ''
    for c in seq:
        if 32 <= c and c < 256:
            str += chr(c)

    if not str:
        return seq
    return str


def make_string_uc(seq):
    code = seq[0:8]
    seq = seq[8:]
    return make_string(seq)


FIELD_TYPES = (
 (
  0, 'X', 'Proprietary'), (1, 'B', 'Byte'), (1, 'A', 'ASCII'), (2, 'S', 'Short'), (4, 'L', 'Long'), (8, 'R', 'Ratio'), (1, 'SB', 'Signed Byte'), (1, 'U', 'Undefined'), (2, 'SS', 'Signed Short'), (4, 'SL', 'Signed Long'), (8, 'SR', 'Signed Ratio'))
EXIF_TAGS = {256: ('ImageWidth',), 257: ('ImageLength',), 258: ('BitsPerSample',), 259: ('Compression', {1: 'Uncompressed', 2: 'CCITT 1D', 3: 'T4/Group 3 Fax', 4: 'T6/Group 4 Fax', 5: 'LZW', 6: 'JPEG (old-style)', 7: 'JPEG', 8: 'Adobe Deflate', 9: 'JBIG B&W', 10: 'JBIG Color', 32766: 'Next', 32769: 'Epson ERF Compressed', 32771: 'CCIRLEW', 32773: 'PackBits', 32809: 'Thunderscan', 32895: 'IT8CTPAD', 32896: 'IT8LW', 32897: 'IT8MP', 32898: 'IT8BL', 32908: 'PixarFilm', 32909: 'PixarLog', 32946: 'Deflate', 32947: 'DCS', 34661: 'JBIG', 34676: 'SGILog', 34677: 'SGILog24', 34712: 'JPEG 2000', 34713: 'Nikon NEF Compressed', 65000: 'Kodak DCR Compressed', 65535: 'Pentax PEF Compressed'}), 262: ('PhotometricInterpretation',), 263: ('Thresholding',), 266: ('FillOrder',), 269: ('DocumentName',), 270: ('ImageDescription',), 271: ('Make',), 272: ('Model',), 273: ('StripOffsets',), 274: ('Orientation', {1: 'Horizontal (normal)', 2: 'Mirrored horizontal', 3: 'Rotated 180', 4: 'Mirrored vertical', 5: 'Mirrored horizontal then rotated 90 CCW', 6: 'Rotated 90 CW', 7: 'Mirrored horizontal then rotated 90 CW', 8: 'Rotated 90 CCW'}), 277: ('SamplesPerPixel',), 278: ('RowsPerStrip',), 279: ('StripByteCounts',), 282: ('XResolution',), 283: ('YResolution',), 284: ('PlanarConfiguration',), 285: ('PageName', make_string), 296: ('ResolutionUnit', {1: 'Not Absolute', 2: 'Pixels/Inch', 3: 'Pixels/Centimeter'}), 301: ('TransferFunction',), 305: ('Software',), 306: ('DateTime',), 315: ('Artist',), 318: ('WhitePoint',), 319: ('PrimaryChromaticities',), 342: ('TransferRange',), 512: ('JPEGProc',), 513: ('JPEGInterchangeFormat',), 514: ('JPEGInterchangeFormatLength',), 529: ('YCbCrCoefficients',), 530: ('YCbCrSubSampling',), 531: ('YCbCrPositioning', {1: 'Centered', 2: 'Co-sited'}), 532: ('ReferenceBlackWhite',), 18246: ('Rating',), 33421: ('CFARepeatPatternDim',), 33422: ('CFAPattern',), 33423: ('BatteryLevel',), 33432: ('Copyright',), 33434: ('ExposureTime',), 33437: ('FNumber',), 33723: ('IPTC/NAA',), 34665: ('ExifOffset',), 34675: ('InterColorProfile',), 34850: ('ExposureProgram', {0: 'Unidentified', 1: 'Manual', 2: 'Program Normal', 3: 'Aperture Priority', 4: 'Shutter Priority', 5: 'Program Creative', 6: 'Program Action', 7: 'Portrait Mode', 8: 'Landscape Mode'}), 34852: ('SpectralSensitivity',), 34853: ('GPSInfo',), 34855: ('ISOSpeedRatings',), 34856: ('OECF',), 36864: ('ExifVersion', make_string), 36867: ('DateTimeOriginal',), 36868: ('DateTimeDigitized',), 37121: ('ComponentsConfiguration', {0: '', 1: 'Y', 2: 'Cb', 3: 'Cr', 4: 'Red', 5: 'Green', 6: 'Blue'}), 37122: ('CompressedBitsPerPixel',), 37377: ('ShutterSpeedValue',), 37378: ('ApertureValue',), 37379: ('BrightnessValue',), 37380: ('ExposureBiasValue',), 37381: ('MaxApertureValue',), 37382: ('SubjectDistance',), 37383: ('MeteringMode', {0: 'Unidentified', 1: 'Average', 2: 'CenterWeightedAverage', 3: 'Spot', 4: 'MultiSpot', 5: 'Pattern'}), 37384: ('LightSource', {0: 'Unknown', 1: 'Daylight', 2: 'Fluorescent', 3: 'Tungsten', 9: 'Fine Weather', 10: 'Flash', 11: 'Shade', 12: 'Daylight Fluorescent', 13: 'Day White Fluorescent', 14: 'Cool White Fluorescent', 15: 'White Fluorescent', 17: 'Standard Light A', 18: 'Standard Light B', 19: 'Standard Light C', 20: 'D55', 21: 'D65', 22: 'D75', 255: 'Other'}), 37385: ('Flash', {0: 'No', 1: 'Fired', 5: 'Fired (?)', 7: 'Fired (!)', 9: 'Fill Fired', 13: 'Fill Fired (?)', 15: 'Fill Fired (!)', 16: 'Off', 24: 'Auto Off', 25: 'Auto Fired', 29: 'Auto Fired (?)', 31: 'Auto Fired (!)', 32: 'Not Available'}), 37386: ('FocalLength',), 37396: ('SubjectArea',), 37500: ('MakerNote',), 37510: ('UserComment', make_string_uc), 37520: ('SubSecTime',), 37521: ('SubSecTimeOriginal',), 37522: ('SubSecTimeDigitized',), 40091: ('XPTitle',), 40092: ('XPComment',), 40093: ('XPAuthor',), 40094: ('XPKeywords',), 40095: ('XPSubject',), 40960: ('FlashPixVersion', make_string), 40961: ('ColorSpace', {1: 'sRGB', 2: 'Adobe RGB', 65535: 'Uncalibrated'}), 40962: ('ExifImageWidth',), 40963: ('ExifImageLength',), 40965: ('InteroperabilityOffset',), 41483: ('FlashEnergy',), 41484: ('SpatialFrequencyResponse',), 41486: ('FocalPlaneXResolution',), 41487: ('FocalPlaneYResolution',), 41488: ('FocalPlaneResolutionUnit',), 41492: ('SubjectLocation',), 41493: ('ExposureIndex',), 41495: ('SensingMethod', {1: 'Not defined', 2: 'One-chip color area', 3: 'Two-chip color area', 4: 'Three-chip color area', 5: 'Color sequential area', 7: 'Trilinear', 8: 'Color sequential linear'}), 41728: ('FileSource', {1: 'Film Scanner', 2: 'Reflection Print Scanner', 3: 'Digital Camera'}), 41729: ('SceneType', {1: 'Directly Photographed'}), 41730: ('CVAPattern',), 41985: ('CustomRendered', {0: 'Normal', 1: 'Custom'}), 41986: ('ExposureMode', {0: 'Auto Exposure', 1: 'Manual Exposure', 2: 'Auto Bracket'}), 41987: ('WhiteBalance', {0: 'Auto', 1: 'Manual'}), 41988: ('DigitalZoomRatio',), 41989: ('FocalLengthIn35mmFilm',), 41990: ('SceneCaptureType', {0: 'Standard', 1: 'Landscape', 2: 'Portrait', 3: 'Night)'}), 41991: ('GainControl', {0: 'None', 1: 'Low gain up', 2: 'High gain up', 3: 'Low gain down', 4: 'High gain down'}), 41992: ('Contrast', {0: 'Normal', 1: 'Soft', 2: 'Hard'}), 41993: ('Saturation', {0: 'Normal', 1: 'Soft', 2: 'Hard'}), 41994: ('Sharpness', {0: 'Normal', 1: 'Soft', 2: 'Hard'}), 41995: ('DeviceSettingDescription',), 41996: ('SubjectDistanceRange',), 42240: ('Gamma',), 50341: ('PrintIM',), 59932: ('Padding',)}
INTR_TAGS = {1: ('InteroperabilityIndex',), 2: ('InteroperabilityVersion',), 4096: ('RelatedImageFileFormat',), 4097: ('RelatedImageWidth',), 4098: ('RelatedImageLength',)}
GPS_TAGS = {0: ('GPSVersionID',), 1: ('GPSLatitudeRef',), 2: ('GPSLatitude',), 3: ('GPSLongitudeRef',), 4: ('GPSLongitude',), 5: ('GPSAltitudeRef',), 6: ('GPSAltitude',), 7: ('GPSTimeStamp',), 8: ('GPSSatellites',), 9: ('GPSStatus',), 10: ('GPSMeasureMode',), 11: ('GPSDOP',), 12: ('GPSSpeedRef',), 13: ('GPSSpeed',), 14: ('GPSTrackRef',), 15: ('GPSTrack',), 16: ('GPSImgDirectionRef',), 17: ('GPSImgDirection',), 18: ('GPSMapDatum',), 19: ('GPSDestLatitudeRef',), 20: ('GPSDestLatitude',), 21: ('GPSDestLongitudeRef',), 22: ('GPSDestLongitude',), 23: ('GPSDestBearingRef',), 24: ('GPSDestBearing',), 25: ('GPSDestDistanceRef',), 26: ('GPSDestDistance',), 29: ('GPSDate',)}
IGNORE_TAGS = (
 37510, 37500)

def nikon_ev_bias(seq):
    if len(seq) < 4:
        return ''
    if seq == [252, 1, 6, 0]:
        return '-2/3 EV'
    if seq == [253, 1, 6, 0]:
        return '-1/2 EV'
    if seq == [254, 1, 6, 0]:
        return '-1/3 EV'
    if seq == [0, 1, 6, 0]:
        return '0 EV'
    if seq == [2, 1, 6, 0]:
        return '+1/3 EV'
    if seq == [3, 1, 6, 0]:
        return '+1/2 EV'
    if seq == [4, 1, 6, 0]:
        return '+2/3 EV'
    a = seq[0]
    if a == 0:
        return '0 EV'
    if a > 127:
        a = 256 - a
        ret_str = '-'
    else:
        ret_str = '+'
    b = seq[2]
    whole = a / b
    a = a % b
    if whole != 0:
        ret_str = ret_str + str(whole) + ' '
    if a == 0:
        ret_str = ret_str + 'EV'
    else:
        r = Ratio(a, b)
        ret_str = ret_str + r.__repr__() + ' EV'
    return ret_str


MAKERNOTE_NIKON_NEWER_TAGS = {1: ('MakernoteVersion', make_string), 2: ('ISOSetting', make_string), 3: ('ColorMode',), 4: ('Quality',), 5: ('Whitebalance',), 6: ('ImageSharpening',), 7: ('FocusMode',), 8: ('FlashSetting',), 9: ('AutoFlashMode',), 11: ('WhiteBalanceBias',), 12: ('WhiteBalanceRBCoeff',), 13: ('ProgramShift', nikon_ev_bias), 14: ('ExposureDifference', nikon_ev_bias), 15: ('ISOSelection',), 17: ('NikonPreview',), 18: ('FlashCompensation', nikon_ev_bias), 19: ('ISOSpeedRequested',), 22: ('PhotoCornerCoordinates',), 24: ('FlashBracketCompensationApplied', nikon_ev_bias), 25: ('AEBracketCompensationApplied',), 26: ('ImageProcessing',), 27: ('CropHiSpeed',), 29: ('SerialNumber',), 30: ('ColorSpace',), 31: ('VRInfo',), 32: ('ImageAuthentication',), 34: ('ActiveDLighting',), 35: ('PictureControl',), 36: ('WorldTime',), 37: ('ISOInfo',), 128: ('ImageAdjustment',), 129: ('ToneCompensation',), 130: ('AuxiliaryLens',), 131: ('LensType',), 132: ('LensMinMaxFocalMaxAperture',), 133: ('ManualFocusDistance',), 134: ('DigitalZoomFactor',), 135: ('FlashMode', {0: 'Did Not Fire', 1: 'Fired, Manual', 7: 'Fired, External', 8: 'Fired, Commander Mode ', 9: 'Fired, TTL Mode'}), 136: ('AFFocusPosition', {0: 'Center', 256: 'Top', 512: 'Bottom', 768: 'Left', 1024: 'Right'}), 137: ('BracketingMode', {0: 'Single frame, no bracketing', 1: 'Continuous, no bracketing', 2: 'Timer, no bracketing', 16: 'Single frame, exposure bracketing', 17: 'Continuous, exposure bracketing', 18: 'Timer, exposure bracketing', 64: 'Single frame, white balance bracketing', 65: 'Continuous, white balance bracketing', 66: 'Timer, white balance bracketing'}), 138: ('AutoBracketRelease',), 139: ('LensFStops',), 140: ('NEFCurve1',), 141: ('ColorMode',), 143: ('SceneMode',), 144: ('LightingType',), 145: ('ShotInfo',), 146: ('HueAdjustment',), 147: ('Compression',), 148: ('Saturation', {-3: 'B&W', -2: '-2', -1: '-1', 0: '0', 1: '1', 2: '2'}), 149: ('NoiseReduction',), 150: ('NEFCurve2',), 151: ('ColorBalance',), 152: ('LensData',), 153: ('RawImageCenter',), 154: ('SensorPixelSize',), 156: ('Scene Assist',), 158: ('RetouchHistory',), 160: ('SerialNumber',), 162: ('ImageDataSize',), 165: ('ImageCount',), 166: ('DeletedImageCount',), 167: ('TotalShutterReleases',), 168: ('FlashInfo',), 169: ('ImageOptimization',), 170: ('Saturation',), 171: ('DigitalVariProgram',), 172: ('ImageStabilization',), 173: ('Responsive AF',), 176: ('MultiExposure',), 177: ('HighISONoiseReduction',), 183: ('AFInfo',), 184: ('FileInfo',), 256: ('DigitalICE',), 259: ('PreviewCompression', {1: 'Uncompressed', 2: 'CCITT 1D', 3: 'T4/Group 3 Fax', 4: 'T6/Group 4 Fax', 5: 'LZW', 6: 'JPEG (old-style)', 7: 'JPEG', 8: 'Adobe Deflate', 9: 'JBIG B&W', 10: 'JBIG Color', 32766: 'Next', 32769: 'Epson ERF Compressed', 32771: 'CCIRLEW', 32773: 'PackBits', 32809: 'Thunderscan', 32895: 'IT8CTPAD', 32896: 'IT8LW', 32897: 'IT8MP', 32898: 'IT8BL', 32908: 'PixarFilm', 32909: 'PixarLog', 32946: 'Deflate', 32947: 'DCS', 34661: 'JBIG', 34676: 'SGILog', 34677: 'SGILog24', 34712: 'JPEG 2000', 34713: 'Nikon NEF Compressed', 65000: 'Kodak DCR Compressed', 65535: 'Pentax PEF Compressed'}), 513: ('PreviewImageStart',), 514: ('PreviewImageLength',), 531: ('PreviewYCbCrPositioning', {1: 'Centered', 2: 'Co-sited'}), 16: ('DataDump',)}
MAKERNOTE_NIKON_OLDER_TAGS = {3: ('Quality', {1: 'VGA Basic', 2: 'VGA Normal', 3: 'VGA Fine', 4: 'SXGA Basic', 5: 'SXGA Normal', 6: 'SXGA Fine'}), 4: ('ColorMode', {1: 'Color', 2: 'Monochrome'}), 5: ('ImageAdjustment', {0: 'Normal', 1: 'Bright+', 2: 'Bright-', 3: 'Contrast+', 4: 'Contrast-'}), 6: ('CCDSpeed', {0: 'ISO 80', 2: 'ISO 160', 4: 'ISO 320', 5: 'ISO 100'}), 7: ('WhiteBalance', {0: 'Auto', 1: 'Preset', 2: 'Daylight', 3: 'Incandescent', 4: 'Fluorescent', 5: 'Cloudy', 6: 'Speed Light'})}

def olympus_special_mode(v):
    a = {0: 'Normal', 1: 'Unknown', 2: 'Fast', 3: 'Panorama'}
    b = {0: 'Non-panoramic', 1: 'Left to right', 2: 'Right to left', 3: 'Bottom to top', 4: 'Top to bottom'}
    if v[0] not in a or v[2] not in b:
        return v
    return '%s - sequence %d - %s' % (a[v[0]], v[1], b[v[2]])


MAKERNOTE_OLYMPUS_TAGS = {256: ('JPEGThumbnail',), 512: ('SpecialMode', olympus_special_mode), 513: ('JPEGQual', {1: 'SQ', 2: 'HQ', 3: 'SHQ'}), 514: ('Macro', {0: 'Normal', 1: 'Macro', 2: 'SuperMacro'}), 515: ('BWMode', {0: 'Off', 1: 'On'}), 516: ('DigitalZoom',), 517: ('FocalPlaneDiagonal',), 518: ('LensDistortionParams',), 519: ('SoftwareRelease',), 520: ('PictureInfo',), 521: ('CameraID', make_string), 3840: ('DataDump',), 768: ('PreCaptureFrames',), 1028: ('SerialNumber',), 4096: ('ShutterSpeedValue',), 4097: ('ISOValue',), 4098: ('ApertureValue',), 4099: ('BrightnessValue',), 4100: ('FlashMode',), 4100: ('FlashMode', {2: 'On', 3: 'Off'}), 4101: ('FlashDevice', {0: 'None', 1: 'Internal', 4: 'External', 5: 'Internal + External'}), 4102: ('ExposureCompensation',), 4103: ('SensorTemperature',), 4104: ('LensTemperature',), 4107: ('FocusMode', {0: 'Auto', 1: 'Manual'}), 4119: ('RedBalance',), 4120: ('BlueBalance',), 4122: ('SerialNumber',), 4131: ('FlashExposureComp',), 4134: ('ExternalFlashBounce', {0: 'No', 1: 'Yes'}), 4135: ('ExternalFlashZoom',), 4136: ('ExternalFlashMode',), 4137: ('Contrast \tint16u', {0: 'High', 1: 'Normal', 2: 'Low'}), 4138: ('SharpnessFactor',), 4139: ('ColorControl',), 4140: ('ValidBits',), 4141: ('CoringFilter',), 4142: ('OlympusImageWidth',), 4143: ('OlympusImageHeight',), 4148: ('CompressionRatio',), 4149: ('PreviewImageValid', {0: 'No', 1: 'Yes'}), 4150: ('PreviewImageStart',), 4151: ('PreviewImageLength',), 4153: ('CCDScanMode', {0: 'Interlaced', 1: 'Progressive'}), 4154: ('NoiseReduction', {0: 'Off', 1: 'On'}), 4155: ('InfinityLensStep',), 4156: ('NearLensStep',), 8208: ('Equipment',), 8224: ('CameraSettings',), 8240: ('RawDevelopment',), 8256: ('ImageProcessing',), 8272: ('FocusInfo',), 12288: ('RawInfo ',)}
MAKERNOTE_OLYMPUS_TAG_0x2020 = {256: ('PreviewImageValid', {0: 'No', 1: 'Yes'}), 257: ('PreviewImageStart',), 258: ('PreviewImageLength',), 512: ('ExposureMode', {1: 'Manual', 2: 'Program', 3: 'Aperture-priority AE', 4: 'Shutter speed priority AE', 5: 'Program-shift'}), 513: ('AELock', {0: 'Off', 1: 'On'}), 514: ('MeteringMode', {2: 'Center Weighted', 3: 'Spot', 5: 'ESP', 261: 'Pattern+AF', 515: 'Spot+Highlight control', 1027: 'Spot+Shadow control'}), 768: ('MacroMode', {0: 'Off', 1: 'On'}), 769: ('FocusMode', {0: 'Single AF', 1: 'Sequential shooting AF', 2: 'Continuous AF', 3: 'Multi AF', 10: 'MF'}), 770: ('FocusProcess', {0: 'AF Not Used', 1: 'AF Used'}), 771: ('AFSearch', {0: 'Not Ready', 1: 'Ready'}), 772: ('AFAreas',), 1025: ('FlashExposureCompensation',), 1280: ('WhiteBalance2', {0: 'Auto', 16: '7500K (Fine Weather with Shade)', 17: '6000K (Cloudy)', 18: '5300K (Fine Weather)', 20: '3000K (Tungsten light)', 21: '3600K (Tungsten light-like)', 33: '6600K (Daylight fluorescent)', 34: '4500K (Neutral white fluorescent)', 35: '4000K (Cool white fluorescent)', 48: '3600K (Tungsten light-like)', 256: 'Custom WB 1', 257: 'Custom WB 2', 258: 'Custom WB 3', 259: 'Custom WB 4', 512: 'Custom WB 5400K', 513: 'Custom WB 2900K', 514: 'Custom WB 8000K'}), 1281: ('WhiteBalanceTemperature',), 1282: ('WhiteBalanceBracket',), 1283: ('CustomSaturation',), 1284: ('ModifiedSaturation', {0: 'Off', 1: 'CM1 (Red Enhance)', 2: 'CM2 (Green Enhance)', 3: 'CM3 (Blue Enhance)', 4: 'CM4 (Skin Tones)'}), 1285: ('ContrastSetting',), 1286: ('SharpnessSetting',), 1287: ('ColorSpace', {0: 'sRGB', 1: 'Adobe RGB', 2: 'Pro Photo RGB'}), 1289: ('SceneMode', {0: 'Standard', 6: 'Auto', 7: 'Sport', 8: 'Portrait', 9: 'Landscape+Portrait', 10: 'Landscape', 11: 'Night scene', 13: 'Panorama', 16: 'Landscape+Portrait', 17: 'Night+Portrait', 19: 'Fireworks', 20: 'Sunset', 22: 'Macro', 25: 'Documents', 26: 'Museum', 28: 'Beach&Snow', 30: 'Candle', 35: 'Underwater Wide1', 36: 'Underwater Macro', 39: 'High Key', 40: 'Digital Image Stabilization', 44: 'Underwater Wide2', 45: 'Low Key', 46: 'Children', 48: 'Nature Macro'}), 1290: ('NoiseReduction', {0: 'Off', 1: 'Noise Reduction', 2: 'Noise Filter', 3: 'Noise Reduction + Noise Filter', 4: 'Noise Filter (ISO Boost)', 5: 'Noise Reduction + Noise Filter (ISO Boost)'}), 1291: ('DistortionCorrection', {0: 'Off', 1: 'On'}), 1292: ('ShadingCompensation', {0: 'Off', 1: 'On'}), 1293: ('CompressionFactor',), 1295: ('Gradation', {'-1 -1 1': 'Low Key', '0 -1 1': 'Normal', '1 -1 1': 'High Key'}), 1312: ('PictureMode', {1: 'Vivid', 2: 'Natural', 3: 'Muted', 256: 'Monotone', 512: 'Sepia'}), 1313: ('PictureModeSaturation',), 1314: ('PictureModeHue?',), 1315: ('PictureModeContrast',), 1316: ('PictureModeSharpness',), 1317: ('PictureModeBWFilter', {0: 'n/a', 1: 'Neutral', 2: 'Yellow', 3: 'Orange', 4: 'Red', 5: 'Green'}), 1318: ('PictureModeTone', {0: 'n/a', 1: 'Neutral', 2: 'Sepia', 3: 'Blue', 4: 'Purple', 5: 'Green'}), 1536: ('Sequence',), 1537: ('PanoramaMode',), 1539: ('ImageQuality2', {1: 'SQ', 2: 'HQ', 3: 'SHQ', 4: 'RAW'}), 2305: ('ManometerReading',)}
MAKERNOTE_CASIO_TAGS = {1: ('RecordingMode', {1: 'Single Shutter', 2: 'Panorama', 3: 'Night Scene', 4: 'Portrait', 5: 'Landscape'}), 2: ('Quality', {1: 'Economy', 2: 'Normal', 3: 'Fine'}), 3: ('FocusingMode', {2: 'Macro', 3: 'Auto Focus', 4: 'Manual Focus', 5: 'Infinity'}), 4: ('FlashMode', {1: 'Auto', 2: 'On', 3: 'Off', 4: 'Red Eye Reduction'}), 5: ('FlashIntensity', {11: 'Weak', 13: 'Normal', 15: 'Strong'}), 6: ('Object Distance',), 7: ('WhiteBalance', {1: 'Auto', 2: 'Tungsten', 3: 'Daylight', 4: 'Fluorescent', 5: 'Shade', 129: 'Manual'}), 11: ('Sharpness', {0: 'Normal', 1: 'Soft', 2: 'Hard'}), 12: ('Contrast', {0: 'Normal', 1: 'Low', 2: 'High'}), 13: ('Saturation', {0: 'Normal', 1: 'Low', 2: 'High'}), 20: ('CCDSpeed', {64: 'Normal', 80: 'Normal', 100: 'High', 125: '+1.0', 244: '+3.0', 250: '+2.0'})}
MAKERNOTE_FUJIFILM_TAGS = {0: ('NoteVersion', make_string), 4096: ('Quality',), 4097: ('Sharpness', {1: 'Soft', 2: 'Soft', 3: 'Normal', 4: 'Hard', 5: 'Hard'}), 4098: ('WhiteBalance', {0: 'Auto', 256: 'Daylight', 512: 'Cloudy', 768: 'DaylightColor-Fluorescent', 769: 'DaywhiteColor-Fluorescent', 770: 'White-Fluorescent', 1024: 'Incandescent', 3840: 'Custom'}), 4099: ('Color', {0: 'Normal', 256: 'High', 512: 'Low'}), 4100: ('Tone', {0: 'Normal', 256: 'High', 512: 'Low'}), 4112: ('FlashMode', {0: 'Auto', 1: 'On', 2: 'Off', 3: 'Red Eye Reduction'}), 4113: ('FlashStrength',), 4128: ('Macro', {0: 'Off', 1: 'On'}), 4129: ('FocusMode', {0: 'Auto', 1: 'Manual'}), 4144: ('SlowSync', {0: 'Off', 1: 'On'}), 4145: ('PictureMode', {0: 'Auto', 1: 'Portrait', 2: 'Landscape', 4: 'Sports', 5: 'Night', 6: 'Program AE', 256: 'Aperture Priority AE', 512: 'Shutter Priority AE', 768: 'Manual Exposure'}), 4352: ('MotorOrBracket', {0: 'Off', 1: 'On'}), 4864: ('BlurWarning', {0: 'Off', 1: 'On'}), 4865: ('FocusWarning', {0: 'Off', 1: 'On'}), 4866: ('AEWarning', {0: 'Off', 1: 'On'})}
MAKERNOTE_CANON_TAGS = {6: ('ImageType',), 7: ('FirmwareVersion',), 8: ('ImageNumber',), 9: ('OwnerName',)}
MAKERNOTE_CANON_TAG_0x001 = {1: ('Macromode', {1: 'Macro', 2: 'Normal'}), 2: ('SelfTimer',), 3: ('Quality', {2: 'Normal', 3: 'Fine', 5: 'Superfine'}), 4: ('FlashMode', {0: 'Flash Not Fired', 1: 'Auto', 2: 'On', 3: 'Red-Eye Reduction', 4: 'Slow Synchro', 5: 'Auto + Red-Eye Reduction', 6: 'On + Red-Eye Reduction', 16: 'external flash'}), 5: ('ContinuousDriveMode', {0: 'Single Or Timer', 1: 'Continuous'}), 7: ('FocusMode', {0: 'One-Shot', 1: 'AI Servo', 2: 'AI Focus', 3: 'MF', 4: 'Single', 5: 'Continuous', 6: 'MF'}), 10: ('ImageSize', {0: 'Large', 1: 'Medium', 2: 'Small'}), 11: ('EasyShootingMode', {0: 'Full Auto', 1: 'Manual', 2: 'Landscape', 3: 'Fast Shutter', 4: 'Slow Shutter', 5: 'Night', 6: 'B&W', 7: 'Sepia', 8: 'Portrait', 9: 'Sports', 10: 'Macro/Close-Up', 11: 'Pan Focus'}), 12: ('DigitalZoom', {0: 'None', 1: '2x', 2: '4x'}), 13: ('Contrast', {65535: 'Low', 0: 'Normal', 1: 'High'}), 14: ('Saturation', {65535: 'Low', 0: 'Normal', 1: 'High'}), 15: ('Sharpness', {65535: 'Low', 0: 'Normal', 1: 'High'}), 16: ('ISO', {0: 'See ISOSpeedRatings Tag', 15: 'Auto', 16: '50', 17: '100', 18: '200', 19: '400'}), 17: ('MeteringMode', {3: 'Evaluative', 4: 'Partial', 5: 'Center-weighted'}), 18: ('FocusType', {0: 'Manual', 1: 'Auto', 3: 'Close-Up (Macro)', 8: 'Locked (Pan Mode)'}), 19: ('AFPointSelected', {12288: 'None (MF)', 12289: 'Auto-Selected', 12290: 'Right', 12291: 'Center', 12292: 'Left'}), 20: ('ExposureMode', {0: 'Easy Shooting', 1: 'Program', 2: 'Tv-priority', 3: 'Av-priority', 4: 'Manual', 5: 'A-DEP'}), 23: ('LongFocalLengthOfLensInFocalUnits',), 24: ('ShortFocalLengthOfLensInFocalUnits',), 25: ('FocalUnitsPerMM',), 28: ('FlashActivity', {0: 'Did Not Fire', 1: 'Fired'}), 29: ('FlashDetails', {14: 'External E-TTL', 13: 'Internal Flash', 11: 'FP Sync Used', 7: '2nd("Rear")-Curtain Sync Used', 4: 'FP Sync Enabled'}), 32: ('FocusMode', {0: 'Single', 1: 'Continuous'})}
MAKERNOTE_CANON_TAG_0x004 = {7: ('WhiteBalance', {0: 'Auto', 1: 'Sunny', 2: 'Cloudy', 3: 'Tungsten', 4: 'Fluorescent', 5: 'Flash', 6: 'Custom'}), 9: ('SequenceNumber',), 14: ('AFPointUsed',), 15: ('FlashBias', {65472: '-2 EV', 65484: '-1.67 EV', 65488: '-1.50 EV', 65492: '-1.33 EV', 65504: '-1 EV', 65516: '-0.67 EV', 65520: '-0.50 EV', 65524: '-0.33 EV', 0: '0 EV', 12: '0.33 EV', 16: '0.50 EV', 20: '0.67 EV', 32: '1 EV', 44: '1.33 EV', 48: '1.50 EV', 52: '1.67 EV', 64: '2 EV'}), 19: ('SubjectDistance',)}

def s2n_motorola(str):
    x = 0
    for c in str:
        x = x << 8 | ord(c)

    return x


def s2n_intel(str):
    x = 0
    y = 0
    for c in str:
        x = x | ord(c) << y
        y = y + 8

    return x


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


class Ratio:
    __module__ = __name__

    def __init__(self, num, den):
        self.num = num
        self.den = den

    def __repr__(self):
        self.reduce()
        if self.den == 1:
            return str(self.num)
        return '%d/%d' % (self.num, self.den)

    def reduce(self):
        div = gcd(self.num, self.den)
        if div > 1:
            self.num = self.num / div
            self.den = self.den / div


class IFD_Tag:
    __module__ = __name__

    def __init__(self, printable, tag, field_type, values, field_offset, field_length):
        self.printable = printable
        self.tag = tag
        self.field_type = field_type
        self.field_offset = field_offset
        self.field_length = field_length
        self.values = values

    def __str__(self):
        return self.printable

    def __repr__(self):
        return '(0x%04X) %s=%s @ %d' % (self.tag, FIELD_TYPES[self.field_type][2], self.printable, self.field_offset)


class EXIF_header:
    __module__ = __name__

    def __init__(self, file, endian, offset, fake_exif, strict, debug=0):
        self.file = file
        self.endian = endian
        self.offset = offset
        self.fake_exif = fake_exif
        self.strict = strict
        self.debug = debug
        self.tags = {}

    def s2n(self, offset, length, signed=0):
        self.file.seek(self.offset + offset)
        slice = self.file.read(length)
        if self.endian == 'I':
            val = s2n_intel(slice)
        else:
            val = s2n_motorola(slice)
        if signed:
            msb = 1 << 8 * length - 1
            if val & msb:
                val = val - (msb << 1)
        return val

    def n2s(self, offset, length):
        s = ''
        for dummy in range(length):
            if self.endian == 'I':
                s = s + chr(offset & 255)
            else:
                s = chr(offset & 255) + s
            offset = offset >> 8

        return s

    def first_IFD(self):
        return self.s2n(4, 4)

    def next_IFD(self, ifd):
        entries = self.s2n(ifd, 2)
        return self.s2n(ifd + 2 + 12 * entries, 4)

    def list_IFDs(self):
        i = self.first_IFD()
        a = []
        while i:
            a.append(i)
            i = self.next_IFD(i)

        return a

    def dump_IFD(self, ifd, ifd_name, dict=EXIF_TAGS, relative=0, stop_tag='UNDEF'):
        global detailed
        entries = self.s2n(ifd, 2)
        for i in range(entries):
            entry = ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)
            tag_entry = dict.get(tag)
            if tag_entry:
                tag_name = tag_entry[0]
            else:
                tag_name = 'Tag 0x%04X' % tag
            if not (not detailed and tag in IGNORE_TAGS):
                field_type = self.s2n(entry + 2, 2)
                if not 0 < field_type < len(FIELD_TYPES):
                    if not self.strict:
                        continue
                    else:
                        raise ValueError('unknown type %d in tag 0x%04X' % (field_type, tag))
                typelen = FIELD_TYPES[field_type][0]
                count = self.s2n(entry + 4, 4)
                offset = entry + 8
                if count * typelen > 4:
                    if relative:
                        tmp_offset = self.s2n(offset, 4)
                        offset = tmp_offset + ifd - 8
                        if self.fake_exif:
                            offset = offset + 18
                    else:
                        offset = self.s2n(offset, 4)
                field_offset = offset
                if field_type == 2:
                    if count != 0 and count < 2 ** 31:
                        self.file.seek(self.offset + offset)
                        values = self.file.read(count)
                        values = values.split('\x00', 1)[0]
                    else:
                        values = ''
                else:
                    values = []
                    signed = field_type in [6, 8, 9, 10]
                    if count < 1000:
                        for dummy in range(count):
                            if field_type in (5, 10):
                                value = Ratio(self.s2n(offset, 4, signed), self.s2n(offset + 4, 4, signed))
                            else:
                                value = self.s2n(offset, typelen, signed)
                            values.append(value)
                            offset = offset + typelen

                    elif tag_name == 'MakerNote':
                        for dummy in range(count):
                            value = self.s2n(offset, typelen, signed)
                            values.append(value)
                            offset = offset + typelen

                if count == 1 and field_type != 2:
                    printable = str(values[0])
                elif count > 50 and len(values) > 20:
                    printable = str(values[0:20])[0:-1] + ', ... ]'
                else:
                    printable = str(values)
                if tag_entry:
                    if len(tag_entry) != 1:
                        if callable(tag_entry[1]):
                            printable = tag_entry[1](values)
                        else:
                            printable = ''
                            for i in values:
                                printable += tag_entry[1].get(i, repr(i))

                self.tags[ifd_name + ' ' + tag_name] = IFD_Tag(printable, tag, field_type, values, field_offset, count * typelen)
                if self.debug:
                    print ' debug:   %s: %s' % (tag_name, repr(self.tags[(ifd_name + ' ' + tag_name)]))
            if tag_name == stop_tag:
                break

    def extract_TIFF_thumbnail(self, thumb_ifd):
        entries = self.s2n(thumb_ifd, 2)
        if self.endian == 'M':
            tiff = 'MM\x00*\x00\x00\x00\x08'
        else:
            tiff = 'II*\x00\x08\x00\x00\x00'
        self.file.seek(self.offset + thumb_ifd)
        tiff += self.file.read(entries * 12 + 2) + '\x00\x00\x00\x00'
        for i in range(entries):
            entry = thumb_ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)
            field_type = self.s2n(entry + 2, 2)
            typelen = FIELD_TYPES[field_type][0]
            count = self.s2n(entry + 4, 4)
            oldoff = self.s2n(entry + 8, 4)
            ptr = i * 12 + 18
            if tag == 273:
                strip_off = ptr
                strip_len = count * typelen
            if count * typelen > 4:
                newoff = len(tiff)
                tiff = tiff[:ptr] + self.n2s(newoff, 4) + tiff[ptr + 4:]
                if tag == 273:
                    strip_off = newoff
                    strip_len = 4
                self.file.seek(self.offset + oldoff)
                tiff += self.file.read(count * typelen)

        old_offsets = self.tags['Thumbnail StripOffsets'].values
        old_counts = self.tags['Thumbnail StripByteCounts'].values
        for i in range(len(old_offsets)):
            offset = self.n2s(len(tiff), strip_len)
            tiff = tiff[:strip_off] + offset + tiff[strip_off + strip_len:]
            strip_off += strip_len
            self.file.seek(self.offset + old_offsets[i])
            tiff += self.file.read(old_counts[i])

        self.tags['TIFFThumbnail'] = tiff

    def decode_maker_note(self):
        note = self.tags['EXIF MakerNote']
        make = self.tags['Image Make'].printable
        if 'NIKON' in make:
            if note.values[0:7] == [78, 105, 107, 111, 110, 0, 1]:
                if self.debug:
                    print 'Looks like a type 1 Nikon MakerNote.'
                self.dump_IFD(note.field_offset + 8, 'MakerNote', dict=MAKERNOTE_NIKON_OLDER_TAGS)
            elif note.values[0:7] == [78, 105, 107, 111, 110, 0, 2]:
                if self.debug:
                    print 'Looks like a labeled type 2 Nikon MakerNote'
                if note.values[12:14] != [0, 42] and note.values[12:14] != [42, 0]:
                    raise ValueError("Missing marker tag '42' in MakerNote.")
                self.dump_IFD(note.field_offset + 10 + 8, 'MakerNote', dict=MAKERNOTE_NIKON_NEWER_TAGS, relative=1)
            else:
                if self.debug:
                    print 'Looks like an unlabeled type 2 Nikon MakerNote'
                self.dump_IFD(note.field_offset, 'MakerNote', dict=MAKERNOTE_NIKON_NEWER_TAGS)
            return
        if make.startswith('OLYMPUS'):
            self.dump_IFD(note.field_offset + 8, 'MakerNote', dict=MAKERNOTE_OLYMPUS_TAGS)
        if 'CASIO' in make or 'Casio' in make:
            self.dump_IFD(note.field_offset, 'MakerNote', dict=MAKERNOTE_CASIO_TAGS)
            return
        if make == 'FUJIFILM':
            endian = self.endian
            self.endian = 'I'
            offset = self.offset
            self.offset += note.field_offset
            self.dump_IFD(12, 'MakerNote', dict=MAKERNOTE_FUJIFILM_TAGS)
            self.endian = endian
            self.offset = offset
            return
        if make == 'Canon':
            self.dump_IFD(note.field_offset, 'MakerNote', dict=MAKERNOTE_CANON_TAGS)
            for i in (('MakerNote Tag 0x0001', MAKERNOTE_CANON_TAG_0x001), ('MakerNote Tag 0x0004', MAKERNOTE_CANON_TAG_0x004)):
                self.canon_decode_tag(self.tags[i[0]].values, i[1])

            return

    def olympus_decode_tag(self, value, dict):
        pass

    def canon_decode_tag(self, value, dict):
        for i in range(1, len(value)):
            x = dict.get(i, ('Unknown', ))
            if self.debug:
                print i, x
            name = x[0]
            if len(x) > 1:
                val = x[1].get(value[i], 'Unknown')
            else:
                val = value[i]
            self.tags['MakerNote ' + name] = IFD_Tag(str(val), None, 0, None, None, None)

        return


def process_file(f, stop_tag='UNDEF', details=True, strict=False, debug=False):
    global detailed
    detailed = details
    fake_exif = 0
    data = f.read(12)
    if data[0:4] in ['II*\x00', 'MM\x00*']:
        f.seek(0)
        endian = f.read(1)
        f.read(1)
        offset = 0
    elif data[0:2] == b'\xff\xd8':
        while data[2] == b'\xff' and data[6:10] in ('JFIF', 'JFXX', 'OLYM', 'Phot'):
            length = ord(data[4]) * 256 + ord(data[5])
            f.read(length - 8)
            data = b'\xff\x00' + f.read(10)
            fake_exif = 1

        if data[2] == b'\xff' and data[6:10] == 'Exif':
            offset = f.tell()
            endian = f.read(1)
        else:
            return {}
    else:
        return {}
    if debug:
        print {'I': 'Intel', 'M': 'Motorola'}[endian], 'format'
    hdr = EXIF_header(f, endian, offset, fake_exif, strict, debug)
    ifd_list = hdr.list_IFDs()
    ctr = 0
    for i in ifd_list:
        if ctr == 0:
            IFD_name = 'Image'
        elif ctr == 1:
            IFD_name = 'Thumbnail'
            thumb_ifd = i
        else:
            IFD_name = 'IFD %d' % ctr
        if debug:
            print ' IFD %d (%s) at offset %d:' % (ctr, IFD_name, i)
        hdr.dump_IFD(i, IFD_name, stop_tag=stop_tag)
        exif_off = hdr.tags.get(IFD_name + ' ExifOffset')
        if exif_off:
            if debug:
                print ' EXIF SubIFD at offset %d:' % exif_off.values[0]
            hdr.dump_IFD(exif_off.values[0], 'EXIF', stop_tag=stop_tag)
            intr_off = hdr.tags.get('EXIF SubIFD InteroperabilityOffset')
            if intr_off:
                if debug:
                    print ' EXIF Interoperability SubSubIFD at offset %d:' % intr_off.values[0]
                hdr.dump_IFD(intr_off.values[0], 'EXIF Interoperability', dict=INTR_TAGS, stop_tag=stop_tag)
        gps_off = hdr.tags.get(IFD_name + ' GPSInfo')
        if gps_off:
            if debug:
                print ' GPS SubIFD at offset %d:' % gps_off.values[0]
            hdr.dump_IFD(gps_off.values[0], 'GPS', dict=GPS_TAGS, stop_tag=stop_tag)
        ctr += 1

    thumb = hdr.tags.get('Thumbnail Compression')
    if thumb and thumb.printable == 'Uncompressed TIFF':
        hdr.extract_TIFF_thumbnail(thumb_ifd)
    thumb_off = hdr.tags.get('Thumbnail JPEGInterchangeFormat')
    if thumb_off:
        f.seek(offset + thumb_off.values[0])
        size = hdr.tags['Thumbnail JPEGInterchangeFormatLength'].values[0]
        hdr.tags['JPEGThumbnail'] = f.read(size)
    if 'EXIF MakerNote' in hdr.tags and 'Image Make' in hdr.tags and detailed:
        hdr.decode_maker_note()
    if 'JPEGThumbnail' not in hdr.tags:
        thumb_off = hdr.tags.get('MakerNote JPEGThumbnail')
        if thumb_off:
            f.seek(offset + thumb_off.values[0])
            hdr.tags['JPEGThumbnail'] = file.read(thumb_off.field_length)
    return hdr.tags


def usage(exit_status):
    msg = 'Usage: EXIF.py [OPTIONS] file1 [file2 ...]\n'
    msg += 'Extract EXIF information from digital camera image files.\n\nOptions:\n'
    msg += '-q --quick   Do not process MakerNotes.\n'
    msg += '-t TAG --stop-tag TAG   Stop processing when this tag is retrieved.\n'
    msg += '-s --strict   Run in strict mode (stop on errors).\n'
    msg += '-d --debug   Run in debug mode (display extra info).\n'
    print msg
    sys.exit(exit_status)


if __name__ == '__main__':
    import sys, getopt
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hqsdt:v', ['help', 'quick', 'strict', 'debug', 'stop-tag='])
    except getopt.GetoptError:
        usage(2)
    else:
        if args == []:
            usage(2)
        detailed = True
        stop_tag = 'UNDEF'
        debug = False
        strict = False
        for (o, a) in opts:
            if o in ('-h', '--help'):
                usage(0)
            if o in ('-q', '--quick'):
                detailed = False
            if o in ('-t', '--stop-tag'):
                stop_tag = a
            if o in ('-s', '--strict'):
                strict = True
            if o in ('-d', '--debug'):
                debug = True

        for filename in args:
            try:
                file = open(filename, 'rb')
            except:
                print "'%s' is unreadable\n" % filename
                continue

            print filename + ':'
            data = process_file(file, stop_tag=stop_tag, details=detailed, strict=strict, debug=debug)
            if not data:
                print 'No EXIF information found'
                continue
            x = data.keys()
            x.sort()
            for i in x:
                if i in ('JPEGThumbnail', 'TIFFThumbnail'):
                    continue
                try:
                    print '   %s (%s): %s' % (i, FIELD_TYPES[data[i].field_type][2], data[i].printable)
                except:
                    print 'error', i, '"', data[i], '"'

            if 'JPEGThumbnail' in data:
                print 'File has JPEG thumbnail'
            print
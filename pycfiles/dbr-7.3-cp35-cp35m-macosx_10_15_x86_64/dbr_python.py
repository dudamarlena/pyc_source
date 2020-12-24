# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dbr_python.py
# Compiled at: 2020-04-23 21:22:46
# Size of source mod 2**32: 83201 bytes
import sys, os, cv2, numpy
from enum import IntEnum
from dbr import DynamsoftBarcodeReader

class EnumErrorCode(IntEnum):
    __doc__ = 'Error code'
    DBR_OK = 0
    DBRERR_UNKNOWN = -10000
    DBRERR_NO_MEMORY = -10001
    DBRERR_NULL_POINTER = -10002
    DBRERR_LICENSE_INVALID = -10003
    DBRERR_LICENSE_EXPIRED = -10004
    DBRERR_FILE_NOT_FOUND = -10005
    DBRERR_FILETYPE_NOT_SUPPORTED = -10006
    DBRERR_BPP_NOT_SUPPORTED = -10007
    DBRERR_INDEX_INVALID = -10008
    DBRERR_BARCODE_FORMAT_INVALID = -10009
    DBRERR_CUSTOM_REGION_INVALID = -10010
    DBRERR_MAX_BARCODE_NUMBER_INVALID = -10011
    DBRERR_IMAGE_READ_FAILED = -10012
    DBRERR_TIFF_READ_FAILED = -10013
    DBRERR_QR_LICENSE_INVALID = -10016
    DBRERR_1D_LICENSE_INVALID = -10017
    DBRERR_DIB_BUFFER_INVALID = -10018
    DBRERR_PDF417_LICENSE_INVALID = -10019
    DBRERR_DATAMATRIX_LICENSE_INVALID = -10020
    DBRERR_PDF_READ_FAILED = -10021
    DBRERR_PDF_DLL_MISSING = -10022
    DBRERR_PAGE_NUMBER_INVALID = -10023
    DBRERR_CUSTOM_SIZE_INVALID = -10024
    DBRERR_CUSTOM_MODULESIZE_INVALID = -10025
    DBRERR_RECOGNITION_TIMEOUT = -10026
    DBRERR_JSON_PARSE_FAILED = -10030
    DBRERR_JSON_TYPE_INVALID = -10031
    DBRERR_JSON_KEY_INVALID = -10032
    DBRERR_JSON_VALUE_INVALID = -10033
    DBRERR_JSON_NAME_KEY_MISSING = -10034
    DBRERR_JSON_NAME_VALUE_DUPLICATED = -10035
    DBRERR_TEMPLATE_NAME_INVALID = -10036
    DBRERR_JSON_NAME_REFERENCE_INVALID = -10037
    DBRERR_PARAMETER_VALUE_INVALID = -10038
    DBRERR_DOMAIN_NOT_MATCHED = -10039
    DBRERR_RESERVEDINFO_NOT_MATCHED = -10040
    DBRERR_AZTEC_LICENSE_INVALID = -10041
    DBRERR_LICENSE_DLL_MISSING = -10042
    DBRERR_LICENSEKEY_NOT_MATCHED = -10043
    DBRERR_REQUESTED_FAILED = -10044
    DBRERR_LICENSE_INIT_FAILED = -10045
    DBRERR_PATCHCODE_LICENSE_INVALID = -10046
    DBRERR_POSTALCODE_LICENSE_INVALID = -10047
    DBRERR_DPM_LICENSE_INVALID = -10048
    DBRERR_FRAME_DECODING_THREAD_EXISTS = -10049
    DBRERR_STOP_DECODING_THREAD_FAILED = -10050
    DBRERR_SET_MODE_ARGUMENT_ERROR = -10051
    DBRERR_LICENSE_CONTENT_INVALID = -10052
    DBRERR_LICENSE_KEY_INVALID = -10053
    DBRERR_LICENSE_DEVICE_RUNS_OUT = -10054
    DBRERR_GET_MODE_ARGUMENT_ERROR = -10055
    DBRERR_IRT_LICENSE_INVALID = -10056
    DBRERR_MAXICODE_LICENSE_INVALID = -10057
    DBRERR_GS1_DATABAR_LICENSE_INVALID = -10058
    DBRERR_GS1_COMPOSITE_LICENSE_INVALID = -10059


class EnumBarcodeFormat(IntEnum):
    __doc__ = ' Describes the barcode types in BarcodeFormat group 1. '
    BF_ALL = -32505857
    BF_ONED = 2047
    BF_GS1_DATABAR = 260096
    BF_CODE_39 = 1
    BF_CODE_128 = 2
    BF_CODE_93 = 4
    BF_CODABAR = 8
    BF_ITF = 16
    BF_EAN_13 = 32
    BF_EAN_8 = 64
    BF_UPC_A = 128
    BF_UPC_E = 256
    BF_INDUSTRIAL_25 = 512
    BF_CODE_39_EXTENDED = 1024
    BF_GS1_DATABAR_OMNIDIRECTIONAL = 2048
    BF_GS1_DATABAR_TRUNCATED = 4096
    BF_GS1_DATABAR_STACKED = 8192
    BF_GS1_DATABAR_STACKED_OMNIDIRECTIONAL = 16384
    BF_GS1_DATABAR_EXPANDED = 32768
    BF_GS1_DATABAR_EXPANDED_STACKED = 65536
    BF_GS1_DATABAR_LIMITED = 131072
    BF_PATCHCODE = 262144
    BF_PDF417 = 33554432
    BF_QR_CODE = 67108864
    BF_DATAMATRIX = 134217728
    BF_AZTEC = 268435456
    BF_MAXICODE = 536870912
    BF_MICRO_QR = 1073741824
    BF_MICRO_PDF417 = 524288
    BF_GS1_COMPOSITE = -2147483648
    BF_NULL = 0


class EnumBarcodeFormat_2(IntEnum):
    __doc__ = ' Describes the barcode types in BarcodeFormat group 2. '
    BF2_NULL = 0
    BF2_POSTALCODE = 32505856
    BF2_NONSTANDARD_BARCODE = 1
    BF2_USPSINTELLIGENTMAIL = 1048576
    BF2_POSTNET = 2097152
    BF2_PLANET = 4194304
    BF2_AUSTRALIANPOST = 8388608
    BF2_RM4SCC = 16777216


class EnumBarcodeComplementMode(IntEnum):
    __doc__ = ' Describes the barcode complement mode. '
    BCM_AUTO = 1
    BCM_GENERAL = 2
    BCM_SKIP = 0


class EnumImagePixelFormat(IntEnum):
    __doc__ = ' Describes the image pixel format. '
    IPF_BINARY = 0
    IPF_BINARYINVERTED = 1
    IPF_GRAYSCALED = 2
    IPF_NV21 = 3
    IPF_RGB_565 = 4
    IPF_RGB_555 = 5
    IPF_RGB_888 = 6
    IPF_ARGB_8888 = 7
    IPF_RGB_161616 = 8
    IPF_ARGB_16161616 = 9


class EnumBarcodeColourMode(IntEnum):
    __doc__ = ' Describes the barcode colour mode. '
    BICM_DARK_ON_LIGHT = 1
    BICM_LIGHT_ON_DARK = 2
    BICM_DARK_ON_DARK = 4
    BICM_LIGHT_ON_LIGHT = 8
    BICM_DARK_LIGHT_MIXED = 16
    BICM_DARK_ON_LIGHT_DARK_SURROUNDING = 32
    BICM_SKIP = 0


class EnumBinarizationMode(IntEnum):
    __doc__ = ' Describes the binarization mode. '
    BM_AUTO = 1
    BM_LOCAL_BLOCK = 2
    BM_SKIP = 0


class EnumColourClusteringMode(IntEnum):
    __doc__ = ' Describes the colour clustering mode. '
    CCM_AUTO = 1
    CCM_GENERAL_HSV = 2
    CCM_SKIP = 0


class EnumColourConversionMode(IntEnum):
    __doc__ = ' Describes the colour conversion mode. '
    CICM_GENERAL = 1
    CICM_SKIP = 0


class EnumDPMCodeReadingMode(IntEnum):
    __doc__ = ' Describes the DPM code reading mode. '
    DPMCRM_AUTO = 1
    DPMCRM_GENERAL = 2
    DPMCRM_SKIP = 0


class EnumConflictMode(IntEnum):
    __doc__ = ' Describes the conflict mode. '
    CM_IGNORE = 1
    CM_OVERWRITE = 2


class EnumImagePreprocessingMode(IntEnum):
    __doc__ = ' Describes the image preprocessing mode. '
    IPM_AUTO = 1
    IPM_GENERAL = 2
    IPM_GRAY_EQUALIZE = 4
    IPM_GRAY_SMOOTH = 8
    IPM_SHARPEN_SMOOTH = 16
    IPM_SKIP = 0


class EnumIntermediateResultType(IntEnum):
    __doc__ = ' Describes the intermediate result type. '
    IRT_NO_RESULT = 0
    IRT_ORIGINAL_IMAGE = 1
    IRT_COLOUR_CLUSTERED_IMAGE = 2
    IRT_COLOUR_CONVERTED_GRAYSCALE_IMAGE = 4
    IRT_TRANSFORMED_GRAYSCALE_IMAGE = 8
    IRT_PREDETECTED_REGION = 16
    IRT_PREPROCESSED_IMAGE = 32
    IRT_BINARIZED_IMAGE = 64
    IRT_TEXT_ZONE = 128
    IRT_CONTOUR = 256
    IRT_LINE_SEGMENT = 512
    IRT_FORM = 1024
    IRT_SEGMENTATION_BLOCK = 2048
    IRT_TYPED_BARCODE_ZONE = 4096


class EnumLocalizationMode(IntEnum):
    __doc__ = ' Describes the localization mode. '
    LM_AUTO = 1
    LM_CONNECTED_BLOCKS = 2
    LM_STATISTICS = 4
    LM_LINES = 8
    LM_SCAN_DIRECTLY = 16
    LM_STATISTICS_MARKS = 32
    LM_STATISTICS_POSTAL_CODE = 64
    LM_SKIP = 0


class EnumQRCodeErrorCorrectionLevel(IntEnum):
    __doc__ = ' Describes the QR Code error correction level. '
    QRECL_ERROR_CORRECTION_H = 0
    QRECL_ERROR_CORRECTION_L = 1
    QRECL_ERROR_CORRECTION_M = 2
    QRECL_ERROR_CORRECTION_Q = 3


class EnumRegionPredetectionMode(IntEnum):
    __doc__ = ' Describes the region predetection mode. '
    RPM_AUTO = 1
    RPM_GENERAL = 2
    RPM_GENERAL_RGB_CONTRAST = 4
    RPM_GENERAL_GRAY_CONTRAST = 8
    RPM_GENERAL_HSV_CONTRAST = 16
    RPM_SKIP = 0


class EnumDeformationResistingMode(IntEnum):
    __doc__ = ' Describes the deformation resisting mode. '
    DRM_AUTO = 1
    DRM_GENERAL = 2
    DRM_SKIP = 0


class EnumResultType(IntEnum):
    __doc__ = ' Describes the extended result type. '
    RT_STANDARD_TEXT = 0
    RT_RAW_TEXT = 1
    RT_CANDIDATE_TEXT = 2
    RT_PARTIAL_TEXT = 3


class EnumTerminatePhase(IntEnum):
    __doc__ = ' Describes the terminate phase. '
    TP_REGION_PREDETECTED = 1
    TP_IMAGE_PREPROCESSED = 2
    TP_IMAGE_BINARIZED = 4
    TP_BARCODE_LOCALIZED = 8
    TP_BARCODE_TYPE_DETERMINED = 16
    TP_BARCODE_RECOGNIZED = 32


class EnumTextAssistedCorrectionMode(IntEnum):
    __doc__ = ' Describes the text assisted correction mode. '
    TACM_AUTO = 1
    TACM_VERIFYING = 2
    TACM_VERIFYING_PATCHING = 4
    TACM_SKIP = 0


class EnumTextFilterMode(IntEnum):
    __doc__ = ' Describes the text filter mode. '
    TFM_AUTO = 1
    TFM_GENERAL_CONTOUR = 2
    TFM_SKIP = 0


class EnumIntermediateResultSavingMode(IntEnum):
    __doc__ = ' Describes the intermediate result saving mode. '
    IRSM_MEMORY = 1
    IRSM_FILESYSTEM = 2
    IRSM_BOTH = 4


class EnumTextResultOrderMode(IntEnum):
    __doc__ = ' Describes the text result order mode. '
    TROM_CONFIDENCE = 1
    TROM_POSITION = 2
    TROM_FORMAT = 4
    TROM_SKIP = 0


class EnumTextureDetectionMode(IntEnum):
    __doc__ = ' Describes the texture detection mode. '
    TDM_AUTO = 1
    TDM_GENERAL_WIDTH_CONCENTRATION = 2
    TDM_SKIP = 0


class EnumGrayscaleTransformationMode(IntEnum):
    __doc__ = ' Describes the grayscale transformation mode. '
    GTM_INVERTED = 1
    GTM_ORIGINAL = 2
    GTM_SKIP = 0


class EnumResultCoordinateType(IntEnum):
    __doc__ = ' Describes the result coordinate type. '
    RCT_PIXEL = 1
    RCT_PERCENTAGE = 2


class EnumIMResultDataType(IntEnum):
    __doc__ = ' Describes the intermediate result data type. '
    IMRDT_IMAGE = 1
    IMRDT_CONTOUR = 2
    IMRDT_LINESEGMENT = 4
    IMRDT_LOCALIZATIONRESULT = 8
    IMRDT_REGIONOFINTEREST = 16


class EnumScaleUpMode(IntEnum):
    __doc__ = ' Describes the scale up mode. '
    SUM_AUTO = 1
    SUM_LINEAR_INTERPOLATION = 2
    SUM_NEAREST_NEIGHBOUR_INTERPOLATION = 4
    SUM_SKIP = 0


class EnumAccompanyingTextRecognitionMode(IntEnum):
    __doc__ = ' Describes the accompanying text recognition mode. '
    ATRM_GENERAL = 1
    ATRM_SKIP = 0


class SamplingImageData:
    __doc__ = ' \n    Stores the sampling image data. \n\n    Attributes:\n    -----------\n    - bytes <bytearray> : The sampling image data in a byte array\n\n    - width <int> : The width of the sampling image\n\n    - height <int> : The height of the sampling image\n    '

    def __init__(self, sampling_image_data):
        """Init Function"""
        self.bytes = sampling_image_data['Bytes']
        self.width = sampling_image_data['Width']
        self.height = sampling_image_data['Height']


class FrameDecodingParameters:
    __doc__ = " \n    Defines a class to configure the frame decoding Parameters. \n    \n    Attributes:\n    -----------\n    - max_queue_length <int> : The maximum number of frames waiting for decoding\n        - Value range : [0,0x7fffffff]\n        - Default value : 3\n\n    - max_result_queue_length <int> : The maximum number of frames waiting results (text result/localization result) will be kept for further reference\n        - Value range : [0,0x7fffffff]\n        - Default value : 10\n\n    - width <int> : The width of the frame image in pixels\n        - Value range : [0,0x7fffffff]\n        - Default value : 0\n\n    - height <int> : The height of the frame image in pixels\n        - Value range : [0,0x7fffffff]\n        - Default value : 0\n\n    - stride <int> : The stride (or scan width) of the frame image\n        - Value range : [0,0x7fffffff]\n        - Default value : 0\n\n    - image_pixel_format <EnumImagePixelFormat> : The image pixel format used in the image byte array\n        - Value range : A value of ImagePixelFormat Enumeration items\n        - Default value : EnumImagePixelFormat.IPF_GRAYSCALED\n    \n    - region_top <int> : The region definition of the frame to calculate the internal indicator.The top-most coordinate or percentage of the region.\n        - Value range : \n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100] \n        - Default value : 0\n\n    - region_left <int> : The region definition of the frame to calculate the internal indicator.The left-most coordinate or percentage of the region\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100] \n        - Default value : 0\n\n    - region_right <int> : The region definition of the frame to calculate the internal indicator.The right-most coordinate or percentage of the region\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100] \n        - Default value : 0\n\n    - region_bottom <int> : The region definition of the frame to calculate the internal indicator.The bottom-most coordinate or percentage of the region\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100] \n        - Default value : 0\n\n    - region_measured_by_percentage <int> : Sets whether or not to use percentage to measure the region size\n        - Value range : [0,1]\n        - Default value : 0\n        - remarks : When it's set to 1, the values of Top, Left, Right, Bottom indicate percentage (from 0 to 100); Otherwise, they indicate coordinates. 0: not by percentage, 1: by percentage.\n\n    - threshold <double> : The threshold used for filtering frames.\n        - Value range : [0,1]\n        - Default value : 0.1\n        - Remarks : The SDK will calculate an inner indicator for each frame from append_frame(), if the change rate of the indicators between the current frame \n        and the history frames is larger than the given threshold, the current frame will not be added to the inner frame queue waiting for decoding.\n    \n    - fps <int> : The frequency of calling AppendFrame() per second.\n        - Value range : [0,0x7fffffff]\n        - Default value : 0\n        - Remarks : 0 means the frequency will be calculated automatically by the SDK.\n\n    - auto_filter <int> : Sets whether to filter frames automatically.\n        - Value range : [0,1]\n        - Default value : 1\n        - Remarks : 0:Diable filtering frames automatically. 1:Enable filtering frames automatically.\n\n    "

    def __init__(self, parameters):
        """ Init Function """
        self.max_queue_length = parameters['MaxQueueLength']
        self.max_result_queue_length = parameters['MaxResultQueueLength']
        self.width = parameters['Width']
        self.height = parameters['Height']
        self.stride = parameters['Stride']
        self.image_pixel_format = parameters['ImagePixelFormat']
        self.region_top = parameters['RegionTop']
        self.region_left = parameters['RegionLeft']
        self.region_right = parameters['RegionRight']
        self.region_bottom = parameters['RegionBottom']
        self.region_measured_by_percentage = parameters['RegionMeasuredByPercentage']
        self.threshold = parameters['Threshold']
        self.fps = parameters['FPS']
        self.auto_filter = parameters['AutoFilter']

    def update_parameters(self, parameters):
        """ update frame decoding parameters """
        parameters['MaxQueueLength'] = self.max_queue_length
        parameters['MaxResultQueueLength'] = self.max_result_queue_length
        parameters['Width'] = self.width
        parameters['Height'] = self.height
        parameters['Stride'] = self.stride
        parameters['ImagePixelFormat'] = self.image_pixel_format
        parameters['RegionTop'] = self.region_top
        parameters['RegionLeft'] = self.region_left
        parameters['RegionRight'] = self.region_right
        parameters['RegionBottom'] = self.region_bottom
        parameters['RegionMeasuredByPercentage'] = self.region_measured_by_percentage
        parameters['Threshold'] = self.threshold
        parameters['FPS'] = self.fps
        parameters['AutoFilter'] = self.auto_filter


class PublicRuntimeSetting:
    __doc__ = '"\n    Defines a struct to configure the barcode reading runtime settings. These settings control the barcode recognition process such as which barcode types to decode. \n\n    Attributes:\n    -----------\n    - terminate_phase <EnumTerminatePhase> : Sets the phase to stop the barcode reading algorithm.\n        - Value range : Any one of the TerminatePhase Enumeration items\n        - Default value : EnumTerminatePhase.TP_BARCODE_RECOGNIZED\n        - Remarks : When the recognition result is not desired, you can set this parameter can be set to skip certain processing stages.\n\n    - timeout <int> : Sets the maximum amount of time (in milliseconds) that should be spent searching for a barcode per page. It does not include the time taken to load/decode an image (TIFF, PNG, etc.) from disk into memory.\n        - Value range : [0, 0x7fffffff]\n        - Default value : 10000\n        - Remarks : If you want to stop reading barcodes after a certain period of time, you can use this parameter to set a timeout.\n\n    - max_algorithm_thread_count <int> : Sets the number of threads the image processing algorithm will use to decode barcodes.\n        - Value range : [1, 4]\n        - Default value : 4\n        - Remarks : To keep a balance between speed and quality, the library concurrently runs four different threads for barcode decoding by default. \n\n    - expected_barcodes_count <int> : Sets the number of barcodes expected to be detected for each image.\n        - Value range : [0, 0x7fffffff]\n        - Default value : 0\n        - Remarks : \n            - 0: means Unknown and it will find at least one barcode.\n            - 1: try to find one barcode. If one barcode is found, the library will stop the localization process and perform barcode decoding.\n            - n: try to find n barcodes. If the library only finds m (m<n) barcode, it will try different algorithms till n barcodes are found or all algorithms are tried.\n\n    - barcode_format_ids <int> : Sets the formats of the barcode in BarcodeFormat group 1 to be read. Barcode formats in BarcodeFormat group 1 can be combined.\n        - Value range : A combined value of BarcodeFormat Enumeration items\n        - Default value : EnumBarcodeFormat.BF_ALL\n        - Remarks : If the barcode type(s) are certain, specifying the barcode type(s) to be read will speed up the recognition process.\n\n    - barcode_format_ids_2 <int> : Sets the formats of the barcode in BarcodeFormat group 2 to be read. Barcode formats in BarcodeFormat group 2 can be combined.\n        - Value range : A combined value of BarcodeFormat_2 Enumeration items\n        - Default value : EnumBarcodeFormat_2.BF2_NULL\n        - Remarks : If the barcode type(s) are certain, specifying the barcode type(s) to be read will speed up the recognition process.\n\n    - pdf_raster_dpi <int> : Sets the output image resolution.\n        - Value range : [100, 600]\n        - Default value : 300\n        - Remarks :  When decoding barcodes from a PDF file using the DecodeFile method, the library will convert the PDF file to image(s) first, then perform barcode recognition.\n\n    - scale_down_threshold <int> : Sets the threshold for the image shrinking.\n        - Value range : [512, 0x7fffffff]\n        - Default value : 2300\n        - Remarks : If the shorter edge size is larger than the given threshold value, the library will calculate the required height and width of the barcode image and shrink the image to that size before localization. \n        Otherwise, the library will perform barcode localization on the original image.\n\n    - binarization_modes <list[EnumBinarizationMode]> : Sets the mode and priority for binarization.\n        - Value range : Each list item can be any one of the BinarizationMode Enumeration items.\n        - Default value : [EnumBinarizationMode.BM_LOCAL_BLOCK, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP, EnumBinarizationMode.BM_SKIP]\n        - Remarks : If the barcode type(s) are certain, specifying the barcode type(s) to be read will speed up the recognition process.\n\n    - localization_modes <list[EnumLocalizationMode]> : Sets the mode and priority for localization algorithms.\n        - Value range : Each list item can be any one of the LocalizationMode Enumeration items\n        - Default value : [EnumLocalizationMode.LM_CONNECTED_BLOCKS, EnumLocalizationMode.LM_SCAN_DIRECTLY, EnumLocalizationMode.LM_STATISTICS, EnumLocalizationMode.LM_LINES, EnumLocalizationMode.LM_SKIP, EnumLocalizationMode.LM_SKIP, EnumLocalizationMode.LM_SKIP, EnumLocalizationMode.LM_SKIP]\n        - Remarks : If the barcode type(s) are certain, specifying the barcode type(s) to be read will speed up the recognition process.\n\n    - colour_clustering_modes <list[EnumColourClusteringMode]> : Sets the mode and priority for colour categorization. Not supported yet.\n        - Value range : Each list item can be any one of the ColourClusteringMode Enumeration items.\n        - Default value : [EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP, EnumColourClusteringMode.CCM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - colour_conversion_modes <list[EnumColourConversionMode]> : Sets the mode and priority for converting a colour image to a grayscale image.\n        - Value range : Each list item can be any one of the ColourConversionMode Enumeration items.\n        - Default value : [EnumColourConversionMode.CICM_GENERAL, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP, EnumColourConversionMode.CICM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - grayscale_transformation_modes <list[EnumGrayscaleTransformationMode]> : Sets the mode and priority for the grayscale image conversion.\n        - Value range : Each list item can be any one of the GrayscaleTransformationMode Enumeration items.\n        - Default value : [EnumGrayscaleTransformationMode.GTM_ORIGINAL, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP, EnumGrayscaleTransformationMode.GTM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - region_predetection_modes <list[EnumRegionPredetectionMode]> : Sets the region pre-detection mode for barcodes search.\n        - Value range : Each list item can be any one of the RegionPredetectionMode Enumeration items.\n        - Default value : [EnumRegionPredetectionMode.RPM_GENERAL, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP, EnumRegionPredetectionMode.RPM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n        If the image is large and the barcode on the image is very small, it is recommended to enable region predetection to speed up the localization process and recognition accuracy.\n\n    - image_preprocessing_modes <list[EnumImagePreprocessingMode]> : Sets the mode and priority for image preprocessing algorithms.\n        - Value range : Each list item can be any one of the ImagePreprocessingMode Enumeration items.\n        - Default value : [EnumImagePreprocessingMode.IPM_GENERAL, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP, EnumImagePreprocessingMode.IPM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - texture_detection_modes <list[EnumTextureDetectionMode]> : Sets the mode and priority for texture detection.\n        - Value range : Each list item can be any one of the TextureDetectionMode Enumeration items.\n        - Default value : [EnumTextureDetectionMode.TDM_GENERAL_WIDTH_CONCENTRATION, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP, EnumTextureDetectionMode.TDM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - text_filter_modes <list[EnumTextFilterMode]> : Sets the mode and priority for text filter.\n        - Value range : Each list item can be any one of the TextFilterMode Enumeration items.\n        - Default value : [EnumTextFilterMode.TFM_GENERAL_CONTOUR, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP, EnumTextFilterMode.TFM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n        If the image contains a lot of text, you can enable text filter to speed up the localization process.\n    \n    - dpm_code_reading_modes <list[EnumDPMCodeReadingMode]> : Sets the mode and priority for DPM code reading.\n        - Value range : Each list item can be any one of the DPMCodeReadingMode Enumeration items.\n        - Default value : [EnumDPMCodeReadingMode.DPMCRM_GENERAL, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP, EnumDPMCodeReadingMode.DPMCRM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - deformation_resisting_modes <list[EnumDeformationResistingMode]> : Sets the mode and priority for deformation resisting.\n        - Value range : Each list item can be any one of the DeformationResistingMode Enumeration items.\n        - Default value : [EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP, EnumDeformationResistingMode.DRM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - barcode_complement_modes <list[EnumBarcodeComplementMode]> : Sets the mode and priority to complement the missing parts in the barcode.\n        - Value range : Each list item can be any one of the BarcodeComplementMode Enumeration items.\n        - Default value : [EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP, EnumBarcodeComplementMode.BCM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - barcode_colour_modes <list[EnumBarcodeColourMode]> : Sets the mode and priority for the barcode colour mode used to process the barcode zone.\n        - Value range : Each list item can be any one of the BarcodeColourMode Enumeration items.\n        - Default value : [EnumBarcodeColourMode.BICM_DARK_ON_LIGHT, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP, EnumBarcodeColourMode.BICM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - accompanying_text_recognition_modes <list[EnumAccompanyingTextRecognitionMode]> : Sets the mode and priority to recognize accompanying text.\n        - Value range : Each list item can be any one of the AccompanyingTextRecognitionMode Enumeration items.\n        - Default value : [EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP, EnumAccompanyingTextRecognitionMode.ATRM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - text_result_order_modes <list[EnumTextResultOrderMode]> : Sets the mode and priority for the order of the text results returned.\n        - Value range : Each list item can be any one of the TextResultOrderMode Enumeration items.\n        - Default value : [EnumTextResultOrderMode.TROM_CONFIDENCE, EnumTextResultOrderMode.TROM_POSITION, EnumTextResultOrderMode.TROM_FORMAT, EnumTextResultOrderMode.TROM_SKIP, EnumTextResultOrderMode.TROM_SKIP, EnumTextResultOrderMode.TROM_SKIP, EnumTextResultOrderMode.TROM_SKIP, EnumTextResultOrderMode.TROM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - scale_up_modes <list[EnumScaleUpMode]> : Sets the mode and priority to control the sampling methods of scale-up for linear barcode with small module sizes.\n        - Value range : Each list item can be any one of the ScaleUpMode Enumeration items.\n        - Default value : [EnumScaleUpMode.SUM_AUTO, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP, EnumScaleUpMode.SUM_SKIP]\n        - Remarks : The list index represents the priority of the item. The smaller index is, the higher priority is.\n\n    - text_assisted_correction_mode <list[EnumTextAssistedCorrectionMode]> : Sets the mode of text assisted correction for barcode decoding. Not supported yet.\n        - Value range : Each list item can be any one of the TextAssistedCorrectionMode Enumeration items.\n        - Default value : EnumTextAssistedCorrectionMode.TACM_VERIFYING\n\n    - intermediate_result_saving_mode <list[EnumIntermediateResultSavingMode]> : Sets the mode for saving intermediate result.\n        - Value range : Each list item can be any one of the IntermediateResultSavingMode Enumeration items.\n        - Default value : EnumIntermediateResultSavingMode.IRSM_MEMORY\n\n    - deblur_level <int> : Sets the degree of blurriness of the barcode.\n        - Value range : [0, 9]\n        - Default value : 9\n        - Remarks : If you have a blurry image, you can set this property to a larger value. The higher the value set, the more effort the library will spend to decode images, but it may also slow down the recognition process.\n\n    - intermediate_result_types <int> : Sets which types of intermediate result to be kept for further reference. Intermediate result types can be combined.\n        - Value range : A combined value of IntermediateResultType Enumeration items\n        - Default value : 0\n\n    - result_coordinate_type <EnumResultCoordinateType> : Specifies the format for the coordinates returned.\n        - Value range : Any one of the ResultCoordinateType Enumeration items\n        - Default value : 0\n\n    - return_barcode_zone_clarity <int> : Sets whether or not to return the clarity of the barcode zone.\n        - Value range : [0,1]\n        - Default value : 0\n        - Remarks : 0 : Do not return the clarity of the barcode zone; 1 : Return the clarity of the batcode zone.\n\n    - region_top <int> : The top-most coordinate or percentage of the region.\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100]\n        - Default value : 0\n\n    - region_bottom <int> : The bottom-most coordinate or percentage of the region.\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100]\n        - Default value : 0\n\n    - region_left <int> : The left-most coordinate or percentage of the region.\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100]\n        - Default value : 0\n\n    - region_right <int> : The right-most coordinate or percentage of the region.\n        - Value range :\n            - if region_measured_by_percentage = 0, [0,0x7fffffff] \n            - if region_measured_by_percentage = 1, [0,100]\n        - Default value : 0\n\n    - region_measured_by_percentage <int> : Sets whether or not to use percentage to measure the region size.\n        - Value range : [0,1]\n        - Default value : 0\n        - Remarks : When it\'s set to 1, the values of Top, Left, Right, Bottom indicate percentage (from 0 to 100); Otherwise, they indicate coordinates. 0: not by percentage; 1: by percentage.\n\n    - min_barcode_text_length <int> : Sets the range of barcode text length for barcodes search.\n        - Value range : [0, 0x7fffffff]\n        - Default value : 0\n        - Remarks : 0: means no limitation on the barcode text length.\n\n    - min_result_confidence <int> : The minimum confidence of the result.\n        - Value range : [0, 100]\n        - Default value : 0\n        - Remarks : 0: means no limitation on the result confidence.\n\n    '

    def __init__(self, settings):
        """Init Function"""
        self.terminate_phase = settings['TerminatePhase']
        self.timeout = settings['Timeout']
        self.max_algorithm_thread_count = settings['MaxAlgorithmThreadCount']
        self.expected_barcodes_count = settings['ExpectedBarcodesCount']
        self.barcode_format_ids = settings['BarcodeFormatIds']
        self.barcode_format_ids_2 = settings['BarcodeFormatIds_2']
        self.pdf_raster_dpi = settings['PDFRasterDPI']
        self.scale_down_threshold = settings['ScaleDownThreshold']
        self.binarization_modes = settings['BinarizationModes']
        self.localization_modes = settings['LocalizationModes']
        self.colour_clustering_modes = settings['ColourClusteringModes']
        self.colour_conversion_modes = settings['ColourConversionModes']
        self.grayscale_transformation_modes = settings['GrayscaleTransformationModes']
        self.region_predetection_modes = settings['RegionPredetectionModes']
        self.image_preprocessing_modes = settings['ImagePreprocessingModes']
        self.texture_detection_modes = settings['TextureDetectionModes']
        self.text_filter_modes = settings['TextFilterModes']
        self.dpm_code_reading_modes = settings['DPMCodeReadingModes']
        self.deformation_resisting_modes = settings['DeformationResistingModes']
        self.barcode_complement_modes = settings['BarcodeComplementModes']
        self.barcode_colour_modes = settings['BarcodeColourModes']
        self.text_result_order_modes = settings['TextResultOrderModes']
        self.text_assisted_correction_mode = settings['TextAssistedCorrectionMode']
        self.deblur_level = settings['DeblurLevel']
        self.intermediate_result_types = settings['IntermediateResultTypes']
        self.intermediate_result_saving_mode = settings['IntermediateResultSavingMode']
        self.result_coordinate_type = settings['ResultCoordinateType']
        self.return_barcode_zone_clarity = settings['ReturnBarcodeZoneClarity']
        self.region_top = settings['RegionTop']
        self.region_bottom = settings['RegionBottom']
        self.region_left = settings['RegionLeft']
        self.region_right = settings['RegionRight']
        self.region_measured_by_percentage = settings['RegionMeasuredByPercentage']
        self.min_barcode_text_length = settings['MinBarcodeTextLength']
        self.min_result_confidence = settings['MinResultConfidence']
        self.scale_up_modes = settings['ScaleUpModes']
        self.accompanying_text_recognition_modes = settings['AccompanyingTextRecognitionModes']

    def update_settings(self, settings):
        """update settings"""
        settings['TerminatePhase'] = self.terminate_phase
        settings['Timeout'] = self.timeout
        settings['MaxAlgorithmThreadCount'] = self.max_algorithm_thread_count
        settings['ExpectedBarcodesCount'] = self.expected_barcodes_count
        settings['BarcodeFormatIds'] = self.barcode_format_ids
        settings['BarcodeFormatIds_2'] = self.barcode_format_ids_2
        settings['PDFRasterDPI'] = self.pdf_raster_dpi
        settings['ScaleDownThreshold'] = self.scale_down_threshold
        settings['BinarizationModes'] = self.binarization_modes
        settings['LocalizationModes'] = self.localization_modes
        settings['ColourClusteringModes'] = self.colour_clustering_modes
        settings['ColourConversionModes'] = self.colour_conversion_modes
        settings['GrayscaleTransformationModes'] = self.grayscale_transformation_modes
        settings['RegionPredetectionModes'] = self.region_predetection_modes
        settings['ImagePreprocessingModes'] = self.image_preprocessing_modes
        settings['TextureDetectionModes'] = self.texture_detection_modes
        settings['TextFilterModes'] = self.text_filter_modes
        settings['DPMCodeReadingModes'] = self.dpm_code_reading_modes
        settings['DeformationResistingModes'] = self.deformation_resisting_modes
        settings['BarcodeComplementModes'] = self.barcode_complement_modes
        settings['BarcodeColourModes'] = self.barcode_colour_modes
        settings['TextResultOrderModes'] = self.text_result_order_modes
        settings['TextAssistedCorrectionMode'] = self.text_assisted_correction_mode
        settings['DeblurLevel'] = self.deblur_level
        settings['IntermediateResultTypes'] = self.intermediate_result_types
        settings['IntermediateResultSavingMode'] = self.intermediate_result_saving_mode
        settings['ResultCoordinateType'] = self.result_coordinate_type
        settings['ReturnBarcodeZoneClarity'] = self.return_barcode_zone_clarity
        settings['RegionTop'] = self.region_top
        settings['RegionBottom'] = self.region_bottom
        settings['RegionLeft'] = self.region_left
        settings['RegionRight'] = self.region_right
        settings['RegionMeasuredByPercentage'] = self.region_measured_by_percentage
        settings['MinBarcodeTextLength'] = self.min_barcode_text_length
        settings['MinResultConfidence'] = self.min_result_confidence
        settings['ScaleUpModes'] = self.scale_up_modes
        settings['AccompanyingTextRecognitionModes'] = self.accompanying_text_recognition_modes


class OnedDetailedResult:
    __doc__ = '\n    Stores the OneD code details.\n    \n    Attributes:\n    -----------\n    - module_size <int> : The barcode module size (the minimum bar width in pixel) \n\n    - start_chars_bytes <bytearray> : The start chars in a byte array\n\n    - stop_chars_bytes <bytearray> : The stop chars in a byte array\n\n    - check_digit_bytes <bytearray> : The check digit chars in a byte array\n    '

    def __init__(self, detailed_result):
        """ Init Function """
        self.module_size = detailed_result['ModuleSize']
        self.start_chars_bytes = detailed_result['StartCharsBytes']
        self.stop_chars_bytes = detailed_result['StopCharsBytes']
        self.check_digit_bytes = detailed_result['CheckDigitBytes']


class QRCodeDetailedResult:
    __doc__ = '\n    Stores the QRCode details.\n    \n    Attributes:\n    -----------\n    - module_size <int> : The barcode module size (the minimum bar width in pixel) \n\n    - rows <int> : The row count of the barcode\n\n    - columns <int> : The column count of the barcode\n\n    - error_correction_level <EnumQRCodeErrorCorrectionLevel> : The error correction level of the barcode\n    \n    - versions <int> : The version of the QR Code\n    \n    - model <int> : Number of the models\n\n    '

    def __init__(self, detailed_result):
        """ Init Function """
        self.module_size = detailed_result['ModuleSize']
        self.rows = detailed_result['Rows']
        self.columns = detailed_result['Columns']
        self.error_correction_level = detailed_result['ErrorCorrectionLevel']
        self.versions = detailed_result['Version']
        self.model = detailed_result['Model']


class DataMatrixDetailedResult:
    __doc__ = '\n    Stores the DataMatrix details.\n    \n    Attributes:\n    -----------\n    - module_size <int> : The barcode module size (the minimum bar width in pixel) \n\n    - rows <int> : The row count of the barcode\n\n    - columns <int> : The column count of the barcode\n\n    - data_region_rows <int> : The data region row count of the barcode\n    \n    - data_region_columns <int> : The data region column count of the barcode\n    \n    - data_region_number <int> : The data region count\n\n    '

    def __init__(self, detailed_result):
        """ Init Function """
        self.module_size = detailed_result['ModuleSize']
        self.rows = detailed_result['Rows']
        self.columns = detailed_result['Columns']
        self.data_region_rows = detailed_result['DataRegionRows']
        self.data_region_columns = detailed_result['DataRegionColumns']
        self.data_region_number = detailed_result['DataRegionNumber']


class PDFDetailedResult:
    __doc__ = ' \n    Stores the PDF details.\n    \n    Attributes:\n    -----------\n    - module_size <int> : The barcode module size (the minimum bar width in pixel) \n\n    - rows <int> : The row count of the barcode\n\n    - columns <int> : The column count of the barcode\n\n    - error_correction_level <EnumQRCodeErrorCorrectionLevel> : The error correction level of the barcode\n    \n    '

    def __init__(self, detailed_result):
        """ Init Function """
        self.module_size = detailed_result['ModuleSize']
        self.rows = detailed_result['Rows']
        self.columns = detailed_result['Columns']
        self.error_correction_level = detailed_result['ErrorCorrectionLevel']


class AztecDetailedResult:
    __doc__ = '\n    Stores the Aztec details.\n\n    Attributes:\n    -----------\n    - module_size <int> : The barcode module size (the minimum bar width in pixel) \n\n    - rows <int> : The row count of the barcode\n\n    - columns <int> : The column count of the barcode\n\n    - layer_number <int> : A negative number (-1, -2, -3, -4) specifies a compact Aztec code. A positive number (1, 2, .. 32) specifies a normal (full-rang) Aztec code.\n\n    '

    def __init__(self, detailed_result):
        """ Init Function """
        self.module_size = detailed_result['ModuleSize']
        self.rows = detailed_result['Rows']
        self.columns = detailed_result['Columns']
        self.layer_number = detailed_result['LayerNumber']


class ExtendedResult:
    __doc__ = '\n    Stores the extended result.\n    \n    Attributes:\n    -----------\n    - result_type <EnumResultType> : Extended result type\n\n    - barcode_format <EnumBarcodeFormat> : Barcode type in BarcodeFormat group 1\n\n    - barcode_format_string <str> : Barcode type in BarcodeFormat group 1 as string\n\n    - barcode_format_2 <EnumBarcodeFormat_2> : Barcode type in BarcodeFormat group 2\n\n    - barcode_format_string_2 <str> : Barcode type in BarcodeFormat group 2 as string\n\n    - confidence <EnumResultType> : The confidence of the result\n\n    - bytes <bytearray> : The content in a byte array\n\n    - accompanying_text_bytes <bytearray> : The accompanying text content in a byte array\n\n    - deformation <int> : The deformation value\n\n    - detailed_result <class> : One of the following: OnedDetailedResult, PDFDetailedResult, DataMatrixDetailedResult, AztecDetailedResult, QRCodeDetailedResult\n\n    - sampling_image <class SamplingImageData> : The sampling image info\n\n    - clarity <int> : The clarity of the barcode zone in percentage.\n\n    '

    def __init__(self, extended_result):
        """ Init Function """
        self.result_type = extended_result['ResultType']
        self.barcode_format = extended_result['BarcodeFormat']
        self.barcode_format_string = extended_result['BarcodeFormatString']
        self.barcode_format_2 = extended_result['BarcodeFormat_2']
        self.barcode_format_string_2 = extended_result['BarcodeFormatString_2']
        self.confidence = extended_result['Confidence']
        self.bytes = extended_result['Bytes']
        self.accompanying_text_bytes = extended_result['AccompanyingTextBytes']
        self.deformation = extended_result['Deformation']
        detailed_result = extended_result['DetailedResult']
        is_oned = self.barcode_format & EnumBarcodeFormat.BF_ONED
        if is_oned != 0:
            self.detailed_result = OnedDetailedResult(detailed_result)
        else:
            if self.barcode_format == EnumBarcodeFormat.BF_QR_CODE:
                self.detailed_result = QRCodeDetailedResult(detailed_result)
            else:
                if self.barcode_format == EnumBarcodeFormat.BF_DATAMATRIX:
                    self.detailed_result = DataMatrixDetailedResult(detailed_result)
                else:
                    if self.barcode_format == EnumBarcodeFormat.BF_PDF417:
                        self.detailed_result = PDFDetailedResult(detailed_result)
                    else:
                        if self.barcode_format == EnumBarcodeFormat.BF_AZTEC:
                            self.detailed_result = AztecDetailedResult(detailed_result)
                        else:
                            self.detailed_result = None
        sampling_image = extended_result['SamplingImage']
        self.sampling_image = SamplingImageData(sampling_image)
        self.clarity = extended_result['Clarity']


class LocalizationResult:
    __doc__ = '\n    Stores the localization result.\n\n    Attributes:\n    -----------\n    - terminate_phase <EnumTerminatePhase> : The terminate phase of localization result\n\n    - barcode_format <EnumBarcodeFormat> : Barcode type in BarcodeFormat group 1\n\n    - barcode_format_string <str> : Barcode type in BarcodeFormat group 1 as string\n\n    - barcode_format_2 <EnumBarcodeFormat_2> : Barcode type in BarcodeFormat group 2\n\n    - barcode_format_string_2 <str> : Barcode type in BarcodeFormat group 2 as string\n\n    - localization_points <tuple> : The 4 localization points\n\n    - angle <int> : The angle of a barcode. Values range is from 0 to 360\n\n    - module_size <int> : The barcode module size (the minimum bar width in pixel)\n\n    - page_number <int> : The page number the barcode located in. The index is 0-based\n\n    - region_name <int> : The region name the barcode located in\n\n    - document_name <int> : The document name\n\n    - result_coordinate_type <EnumResultCoordinateType> : The coordinate type\n\n    - accompanying_text_bytes <bytearray> : The accompanying text content in a byte array\n\n    - confidence <int> : The confidence of the localization result\n\n    '

    def __init__(self, localization_result):
        """ Init Function """
        self.terminate_phase = localization_result['TerminatePhase']
        self.barcode_format = localization_result['BarcodeFormat']
        self.barcode_format_string = localization_result['BarcodeFormatString']
        self.barcode_format_2 = localization_result['BarcodeFormat_2']
        self.barcode_format_string_2 = localization_result['BarcodeFormatString_2']
        x1 = localization_result['X1']
        y1 = localization_result['Y1']
        x2 = localization_result['X2']
        y2 = localization_result['Y2']
        x3 = localization_result['X3']
        y3 = localization_result['Y3']
        x4 = localization_result['X4']
        y4 = localization_result['Y4']
        self.localization_points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.angle = localization_result['Angle']
        self.module_size = localization_result['ModuleSize']
        self.page_number = localization_result['PageNumber']
        self.region_name = localization_result['RegionName']
        self.document_name = localization_result['DocumentName']
        self.result_coordinate_type = localization_result['ResultCoordinateType']
        self.accompanying_text_bytes = localization_result['AccompanyingTextBytes']
        self.confidence = localization_result['Confidence']


class TextResult:
    __doc__ = '\n    Stores the text result.\n    \n    Attributes:\n    -----------\n    - barcode_format <EnumBarcodeFormat> : Barcode type in BarcodeFormat group 1\n\n    - barcode_format_string <str> : Barcode type in BarcodeFormat group 1 as string\n\n    - barcode_format_2 <EnumBarcodeFormat_2> : Barcode type in BarcodeFormat group 2\n\n    - barcode_format_string_2 <str> : Barcode type in BarcodeFormat group 2 as string\n\n    - barcode_text <str> : The barcode text\n\n    - barcode_bytes <bytearray> : The barcode content in a byte array\n\n    - localization_result <class LocalizationResult> : The corresponding localization result\n\n    - detailed_result <class> : One of the following: OnedDetailedResult, PDFDetailedResult, DataMatrixDetailedResult, AztecDetailedResult, QRCodeDetailedResult\n\n    - extended_results <class ExtendedResult> : The extended result list\n\n    '

    def __init__(self, text_result):
        """ Init Function """
        self.barcode_format = text_result['BarcodeFormat']
        self.barcode_format_string = text_result['BarcodeFormatString']
        self.barcode_format_2 = text_result['BarcodeFormat_2']
        self.barcode_format_string_2 = text_result['BarcodeFormatString_2']
        self.barcode_text = text_result['BarcodeText']
        self.barcode_bytes = text_result['BarcodeBytes']
        localization_result = text_result['LocalizationResult']
        self.localization_result = LocalizationResult(localization_result)
        detailed_result = text_result['DetailedResult']
        is_oned = self.barcode_format & EnumBarcodeFormat.BF_ONED
        if is_oned != 0:
            self.detailed_result = OnedDetailedResult(detailed_result)
        else:
            if self.barcode_format == EnumBarcodeFormat.BF_QR_CODE:
                self.detailed_result = QRCodeDetailedResult(detailed_result)
            else:
                if self.barcode_format == EnumBarcodeFormat.BF_DATAMATRIX:
                    self.detailed_result = DataMatrixDetailedResult(detailed_result)
                else:
                    if self.barcode_format == EnumBarcodeFormat.BF_PDF417:
                        self.detailed_result = PDFDetailedResult(detailed_result)
                    else:
                        if self.barcode_format == EnumBarcodeFormat.BF_AZTEC:
                            self.detailed_result = AztecDetailedResult(detailed_result)
                        else:
                            self.detailed_result = None
            extended_results = text_result['ExtendedResults']
            if type(extended_results) is list:
                self.extended_results = []
                length = len(extended_results)
                for extended_result in extended_results:
                    self.extended_results.append(ExtendedResult(extended_result))

            else:
                self.extended_results = None


class Point:
    __doc__ = '\n    Stores an x- and y-coordinate pair in two-dimensional space.\n    \n    Attributes:\n    -----------\n    - x <int> : The X coordinate of the point\n\n    - y <int> : The Y coordinate of the point\n\n    '

    def __init__(self, point):
        """ Init Function """
        self.x = point['X']
        self.y = point['Y']


class ImageData:
    __doc__ = '\n    Stores the image data.\n    \n    Attributes:\n    -----------\n    - bytes <bytearray> : The image data content in a byte array\n\n    - width <bytearray> : The width of the image in pixels\n\n    - height <bytearray> : The height of the image in pixels\n\n    - stride <bytearray> : The image data content in a byte array\n\n    - image_pixel_format <bytearray> : The image data content in a byte array\n    '

    def __init__(self, image_data):
        """ Init Function """
        self.bytes = image_data['Bytes']
        self.width = image_data['Width']
        self.height = image_data['Height']
        self.stride = image_data['Stride']
        self.image_pixel_format = image_data['ImagePixelFormat']


class Contour:
    __doc__ = '\n    Stores the contour\n\n    Attributes:\n    -----------\n    - points <list[class Point]> : The points list\n\n    '

    def __init__(self, contour):
        """ Init Function """
        points = contour['Points']
        self.points = []
        for point in points:
            self.points.append(Point(point))


class LineSegment:
    __doc__ = ' \n    Stores line segment data. \n    \n    Attributes:\n    -----------\n    - start_point <class Point> : The start point of the line segment\n\n    - end_point <class Point> : The end point of the line segment\n\n    - lines_confidence_coefficients <list[int]> : The end point of the line segment\n\n    '

    def __init__(self, line_segment):
        """ Init Function """
        start_point = line_segment['StartPoint']
        self.start_point = Point(start_point)
        end_point = line_segment['EndPoint']
        self.end_point = Point(end_point)
        self.lines_confidence_coefficients = line_segment['LinesConfidenceCoefficients']


class RegionOfInterest:
    __doc__ = ' \n    Stores the region of interest. \n    \n    Attributes:\n    -----------\n    - roi_id <int> : The ID generated by the SDK\n\n    - point <class Point> : The left top point of the region\n\n    - width <int> : The width of the region\n\n    - height <int> : The height of the region\n\n    '

    def __init__(self, result):
        """ Init Function """
        self.roi_id = result['ROIId']
        point = result['Point']
        self.point = Point(point)
        self.width = result['Width']
        self.height = result['Height']


class IntermediateResult:
    __doc__ = ' \n    Stores the intermediate result. \n    \n    Attributes:\n    -----------\n    - data_type <EnumIMResultDataType> : The data type of the intermediate result\n\n    - results <list[class]> : One of the following types: List of class Contour, List of class ImageData, List of class LineSegment, List of class LocalizationResult, List of class RegionOfInterest\n\n    - result_type <EnumIntermediateResultType> : Intermediate result type\n\n    - barcode_complement_mode <EnumBarcodeComplementMode> : The BarcodeComplementMode used when generating the current intermediate result\n\n    - bcm_index <int> : The list index of current used ColourClusteringMode in the ColourClusteringModes setting\n\n    - deformation_resisting_mode <EnumDeformationResistingMode> : The DeformationResistingMode used when generating the current intermediate result\n\n    - drm_index <int> : The list index of current used DeformationResistingMode in the DeformationResistingModes setting\n\n    - dpm_code_reading_mode <EnumDPMCodeReadingMode> : The DPMCodeReadingMode used when generating the current intermediate result\n\n    - dpmcrm_index <int> : The list index of current used DPMCodeReadingMode in the DPMCodeReadingModes setting\n\n    - text_filter_mode <EnumTextFilterMode> : The TextFilterMode used when generating the current intermediate result\n\n    - tfm_index <int> : The list index of current used TextFilterMode in the TextFilterModes setting\n\n    - localization_mode <EnumLocalizationMode> : The LocalizationMode used when generating the current intermediate result\n\n    - lm_index <int> : The list index of current used LocalizationMode in the LocalizationModes setting\n\n    - binarization_mode <EnumBinarizationMode> : The BinarizationMode used when generating the current intermediate result\n\n    - bm_index <int> : The list index of current used BinarizationMode in the BinarizationModes setting\n\n    - image_preprocessing_mode <EnumImagePreprocessingMode> : The ImagePreprocessingMode used when generating the current intermediate result\n\n    - ipm_index <int> : The list index of current used ImagePreprocessingMode in the ImagePreprocessingModes setting\n\n    - region_predetection_mode <EnumRegionPredetectionMode> : The RegionPredetectionMode used when generating the current intermediate result\n\n    - rpm_index <int> : The list index of current used RegionPredetectionMode in the RegionPredetectionModes setting\n\n    - grayscale_transformation_mode <EnumGrayscaleTransformationMode> : The GrayscaleTransformationMode used when generating the current intermediate result\n\n    - gtm_index <int> : The list index of current used GrayscaleTransformationMode in the GrayscaleTransformationModes setting\n\n    - colour_conversion_mode <EnumColourConversionMode> : The ColourConversionMode used when generating the current intermediate result\n\n    - cicm_index <int> : The list index of current used ColourConversionMode in the ColourConversionModes setting\n\n    - colour_clustering_mode <EnumColourClusteringMode> : The ColourClusteringMode used when generating the current intermediate result\n\n    - ccm_index <int> : The list index of current used ColourClusteringMode in the ColourClusteringModes setting\n\n    - rotation_matrix <list[double]> : The rotation matrix\n\n    - roi_id <int> : The ID of the ROI (Region Of Interest) generated by the SDK. -1 means the original image.\n\n    - scale_down_ratio <int> : The scale down ratio\n\n    - frame_id <int> : The ID of the operated frame\n\n    '

    def __init__(self, intermediate_result):
        """ Init Function """
        self.data_type = intermediate_result['DataType']
        im_results = intermediate_result['IMResults']
        if type(im_results) is list:
            self.results = []
            if self.data_type == EnumIMResultDataType.IMRDT_IMAGE:
                for im_result in im_results:
                    self.results.append(ImageData(im_result))

            else:
                if self.data_type == EnumIMResultDataType.IMRDT_CONTOUR:
                    for im_result in im_results:
                        self.results.append(Contour(im_result))

                else:
                    if self.data_type == EnumIMResultDataType.IMRDT_LINESEGMENT:
                        for im_result in im_results:
                            self.results.append(LineSegment(im_result))

                    else:
                        if self.data_type == EnumIMResultDataType.IMRDT_LOCALIZATIONRESULT:
                            for im_result in im_results:
                                self.results.append(LocalizationResult(im_result))

                        elif self.data_type == EnumIMResultDataType.IMRDT_REGIONOFINTEREST:
                            for im_result in im_results:
                                self.results.append(RegionOfInterest(im_result))

        else:
            self.results = None
        self.result_type = intermediate_result['ResultType']
        self.barcode_complement_mode = intermediate_result['BarcodeComplementMode']
        self.bcm_index = intermediate_result['BCMIndex']
        self.deformation_resisting_mode = intermediate_result['DeformationResistingMode']
        self.drm_index = intermediate_result['DRMIndex']
        self.dpm_code_reading_mode = intermediate_result['DPMCodeReadingMode']
        self.dpmcrm_index = intermediate_result['DPMCRMIndex']
        self.text_filter_mode = intermediate_result['TextFilterMode']
        self.tfm_index = intermediate_result['TFMIndex']
        self.localization_mode = intermediate_result['LocalizationMode']
        self.lm_index = intermediate_result['LMIndex']
        self.binarization_mode = intermediate_result['BinarizationMode']
        self.bm_index = intermediate_result['BMIndex']
        self.image_preprocessing_mode = intermediate_result['ImagePreprocessingMode']
        self.ipm_index = intermediate_result['IPMIndex']
        self.region_predetection_mode = intermediate_result['RegionPredetectionMode']
        self.rpm_index = intermediate_result['RPMIndex']
        self.grayscale_transformation_mode = intermediate_result['GrayscaleTransformationMode']
        self.gtm_index = intermediate_result['GTMIndex']
        self.colour_conversion_mode = intermediate_result['ColourConversionMode']
        self.cicm_index = intermediate_result['CICMIndex']
        self.colour_clustering_mode = intermediate_result['ColourClusteringMode']
        self.ccm_index = intermediate_result['CCMIndex']
        self.rotation_matrix = intermediate_result['RotationMatrix']
        self.roi_id = intermediate_result['ROIId']
        self.scale_down_ratio = intermediate_result['ScaleDownRatio']
        self.frame_id = intermediate_result['FrameId']


class BarcodeReaderError(Exception):
    __doc__ = ' Custom Exception '

    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class BarcodeReader:
    __doc__ = ' \n    Defines a class that provides functions for decoding barcodes in images. This is the main interface for recognizing barcodes.\n    \n    Attributes:\n    -----------\n    - version <str> : The Dynamsoft Barcode Reader - Python Edition version\n    - dbr_version <str> : The Dynamsoft Barcode Reader version\n\n    Methods:\n    -----------\n    - Common Functions\n        - get_error_string(error_code)\n    - License Functions\n        - init_license(dbr_license)\n        - init_license_from_server(license_server, license_key)\n        - init_license_from_license_content(license_key, license_content)\n        - output_license_to_string()\n    - Runtime Settings Functions\n        - get_runtime_settings()\n        - update_runtime_settings(settings)\n        - reset_runtime_settings()\n        - set_mode_argument(modes_name, index, argument_name, argument_value)\n        - get_mode_argument(modes_name, index, argument_name)\n    - Template Settings Funtions\n        - init_runtime_settings_with_string(json_string, conflict_mode=EnumConflictMode.CM_OVERWRITE)\n        - init_runtime_settings_with_file(json_file, conflict_mode=EnumConflictMode.CM_OVERWRITE)\n        - append_template_string_to_runtime_settings(json_string, conflict_mode)\n        - append_template_file_to_runtime_settings(json_file, conflict_mode)\n        - output_settings_to_json_string()\n        - output_settings_to_json_file(save_file_path)\n        - get_all_template_names()\n    - Image Decoding Functions\n        - decode_file(image_file_name, template_name="")\n        - decode_buffer(image, image_pixel_format=EnumImagePixelFormat.IPF_RGB_888, template_name="")\n        - decode_file_stream(file_stream, template_name="")\n        - get_all_intermediate_results()\n    - Frame Decoding Functions\n        - init_frame_decoding_parameters()\n        - start_video_mode(frame_decoding_parameters, call_back_func, template_name="")\n        - append_video_frame(video_frame)\n        - stop_video_mode()\n        - get_length_of_frame_queue()\n\n    '

    def __init__(self):
        """ Init Function """
        self._BarcodeReader__dbr = DynamsoftBarcodeReader()
        self.version = 'dbr-python 7.3'
        self.dbr_version = self._BarcodeReader__dbr.GetDBRVersion()

    def get_error_string(self, error_code):
        """ Get the detailed error message by error code
            :param error_code    <int> : Error code
            :return error_string <str> : The detailed error message
        """
        error_string = self._BarcodeReader__dbr.GetErrorString(error_code)
        return error_string

    def init_license(self, dbr_license):
        """ Reads product key and activates the SDK. 
            :param dbr_license <str>   : The product keys
            :return error      <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.InitLicense(dbr_license)
        return error

    def init_license_from_server(self, license_server, license_key):
        """ Initializes barcode reader license and connects to the specified server for online verification. 
            :param license_server <str>   : The name/IP of the license server.
            :param license_key    <str>   : The license key.
            :return error         <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.InitLicenseFromServer(license_server, license_key)
        return error

    def init_license_from_license_content(self, license_key, license_content):
        """ Initializes barcode reader license from the license content on the client machine for offline verification.
            :param license_key     <str>   : The license key.
            :param license_content <str>   : An encrypted string representing the license content (quota, expiration date, barcode type, etc.) obtained from the method output_license_to_string().
            :return error          <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.InitLicenseFromLicenseContent(license_key, license_content)
        return error

    def output_license_to_string(self):
        """ Outputs the license content as an encrypted string from the license server to be used for offline license verification. 
            :return license_string  <str> : An encrypted string which stores the content of license.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        license_string = self._BarcodeReader__dbr.OutputLicenseToString()
        if type(license_string) is int:
            error_string = self._BarcodeReader__dbr.GetErrorString(license_string)
            raise BarcodeReaderError(error_string)
        else:
            return license_string

    def get_runtime_settings(self):
        """ Get current runtime settings
            :return runtime_settings <class PublicRuntimeSetting> : The PublicRuntimeSetting object of current runtime settings.
        """
        cp_settings = self._BarcodeReader__dbr.GetRuntimeSettings()
        settings = PublicRuntimeSetting(cp_settings)
        return settings

    def update_runtime_settings(self, settings):
        """ Update runtime settings with a PublicRuntimeSetting object
            :param settings <class PublicRuntimeSetting> : a PublicRuntimeSetting object.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        cp_settings = self._BarcodeReader__dbr.GetRuntimeSettings()
        settings.update_settings(cp_settings)
        error = self._BarcodeReader__dbr.UpdataRuntimeSettings(cp_settings)
        error_code = error[0]
        error_message = error[1]
        if error_code != EnumErrorCode.DBR_OK:
            raise BarcodeReaderError(error_message)

    def reset_runtime_settings(self):
        """ Resets all parameters to default values. """
        self._BarcodeReader__dbr.ResetRuntimeSettings()

    def set_mode_argument(self, modes_name, index, argument_name, argument_value):
        """ Sets the optional argument for a specified mode in Modes(Mode) parameters. 
            :param modes_name     <str>   : The modes(mode) parameter name to set argument.
            :param index          <int>   : The array index of modes parameter to indicate a specific mode.
            :param argument_name  <str>   : The name of the argument to set.
            :param argument_value <str>   : The value of the argument to set.
            :return error         <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.SetModeArgument(modes_name, index, argument_name, argument_value)
        return error

    def get_mode_argument(self, modes_name, index, argument_name):
        """ Gets the optional argument for a specified mode in Modes(Mode) parameters. 
            :param modes_name      <str> : The modes(mode) parameter name to get argument.
            :param index           <int> : The array index of modes parameter to indicate a specific mode.
            :param argument_name   <str> : The name of the argument to get.
            :return argument_value <str> : The value of the argument to get.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        return_value = self._BarcodeReader__dbr.GetModeArgument(modes_name, index, argument_name)
        if type(return_value) is str:
            return return_value
        error_code = return_value[0]
        error_message = return_value[1]
        raise BarcodeReaderError(error_message)

    def init_runtime_settings_with_string(self, json_string, conflict_mode=EnumConflictMode.CM_OVERWRITE):
        """ Initializes runtime settings with the parameters obtained from a JSON string. 
            :param json_string <str> : A JSON string that represents the content of the settings.
            :param conflict_mode(optional) <EnumConflictMode> : The parameter setting mode, which decides whether to inherit parameters 
                from previous template setting or to overwrite previous settings with the new template.
            :return error <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.InitRuntimeSettingsByJsonString(json_string, conflict_mode)
        return error

    def init_runtime_settings_with_file(self, json_file, conflict_mode=EnumConflictMode.CM_OVERWRITE):
        """ Initializes runtime settings with the parameters obtained from a JSON file. 
            :param json_file <str> : A JSON template file's path.
            :param conflict_mode(optional) <EnumConflictMode> : The parameter setting mode, which decides whether to inherit parameters 
                from previous template setting or to overwrite previous settings with the new template.
            :return error <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.InitRuntimeSettingsByJsonFile(json_file, conflict_mode)
        return error

    def append_template_string_to_runtime_settings(self, json_string, conflict_mode):
        """ Appends a new template string to the current runtime settings. 
            :param json_string <str> : A JSON string that represents the content of the settings.
            :param conflict_mode <EnumConflictMode> : The parameter setting mode, which decides whether to inherit parameters 
                from previous template setting or to overwrite previous settings with the new template.
            :return error <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.AppendTplStringToRuntimeSettings(json_string, conflict_mode)
        return error

    def append_template_file_to_runtime_settings(self, json_file, conflict_mode):
        """ Appends a new template file to the current runtime settings. 
            :param json_file <str> : A JSON template file's path.
            :param conflict_mode <EnumConflictMode> : The parameter setting mode, which decides whether to inherit parameters 
                from previous template setting or to overwrite previous settings with the new template.
            :return error <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.AppendTplFileToRuntimeSettings(json_file, conflict_mode)
        return error

    def output_settings_to_json_string(self):
        """ Outputs runtime settings to a json string.
            :return settings_string <str> : The output string which stores the contents of current settings.
        """
        settings_string = self._BarcodeReader__dbr.OutputSettingsToJsonString()
        return settings_string

    def output_settings_to_json_file(self, save_file_path):
        """ Outputs runtime settings and save them into a settings file (JSON file).
            :param save_file_path <str> : The path of the output file which stores current settings.
            :return error <tuple> : error_code = error[0], error_message = error[1], if error_code != EnumErrorCode.DBR_OK, 
                you can get the detailed error message by error_message.
        """
        error = self._BarcodeReader__dbr.OutputSettingsToJsonFile(save_file_path)
        return error

    def get_all_template_names(self):
        """ Gets all parameter template names.
            :return template_names <list[str]> : all parameter template names
        """
        template_names = self._BarcodeReader__dbr.GetAllTemplateNames()
        return template_names

    def decode_file(self, image_file_name, template_name=''):
        """ Decodes barcodes in the specified image file.
            :param image_file_name           <str> : A string defining the file name.
            :param template_name(optional)   <str> : The template name.
            :return text_results <list[class TextResult]> : All text results.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        error_code = self._BarcodeReader__dbr.DecodeFile(image_file_name, template_name)
        if error_code == EnumErrorCode.DBR_OK or error_code == EnumErrorCode.DBRERR_LICENSE_EXPIRED or error_code == EnumErrorCode.DBRERR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_RECOGNITION_TIMEOUT or error_code == EnumErrorCode.DBRERR_1D_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_QR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PDF417_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_AZTEC_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_DATAMATRIX_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_DATABAR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_COMPOSITE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_MAXICODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PATCHCODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_POSTALCODE_LICENSE_INVALID:
            cp_text_results = self._BarcodeReader__dbr.GetAllTextResults()
            text_results = []
            if type(cp_text_results) is list:
                for cp_text_result in cp_text_results:
                    text_results.append(TextResult(cp_text_result))

                return text_results
            else:
                return
        else:
            error_message = self._BarcodeReader__dbr.GetErrorString(error_code)
            raise BarcodeReaderError(error_message)

    def decode_buffer(self, image, image_pixel_format=EnumImagePixelFormat.IPF_RGB_888, template_name=''):
        """ Decodes barcodes from the memory buffer containing image pixels in defined format. 
            :param image <class numpy.ndarray> : The image which is processed by opencv.( image = cv2.imread('image_name') )
            :param image_pixel_format(optional) <EnumImagePixelFormat> : The image pixel format used in the image byte array. Default value = EnumImagePixelFormat.IPF_RGB_888.
            :param template_name(optional) <str> : The template name.
            :return text_results <list[class TextResult]> : All text results.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        height = image.shape[0]
        width = image.shape[1]
        stride = image.strides[0]
        error_code = self._BarcodeReader__dbr.DecodeBuffer(image, height, width, stride, image_pixel_format, template_name)
        if error_code == EnumErrorCode.DBR_OK or error_code == EnumErrorCode.DBRERR_LICENSE_EXPIRED or error_code == EnumErrorCode.DBRERR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_RECOGNITION_TIMEOUT or error_code == EnumErrorCode.DBRERR_1D_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_QR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PDF417_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_AZTEC_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_DATAMATRIX_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_DATABAR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_COMPOSITE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_MAXICODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PATCHCODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_POSTALCODE_LICENSE_INVALID:
            cp_text_results = self._BarcodeReader__dbr.GetAllTextResults()
            text_results = []
            if type(cp_text_results) is list:
                for cp_text_result in cp_text_results:
                    text_results.append(TextResult(cp_text_result))

                return text_results
            else:
                return
        else:
            error_message = self._BarcodeReader__dbr.GetErrorString(error_code)
            raise BarcodeReaderError(error_message)

    def decode_file_stream(self, file_stream, template_name=''):
        """ Decodes barcodes from an image file in memory.
            :param file_stream <bytearray> : The image file bytes in memory.
            :param template_name(optional) <str> : The template name. 
            :return text_results <list[class TextResult]> : All text results.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        file_size = len(file_stream)
        error_code = self._BarcodeReader__dbr.DecodeFileStream(file_stream, file_size, template_name)
        if error_code == EnumErrorCode.DBR_OK or error_code == EnumErrorCode.DBRERR_LICENSE_EXPIRED or error_code == EnumErrorCode.DBRERR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_RECOGNITION_TIMEOUT or error_code == EnumErrorCode.DBRERR_1D_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_QR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PDF417_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_AZTEC_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_DATAMATRIX_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_DATABAR_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_GS1_COMPOSITE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_MAXICODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_PATCHCODE_LICENSE_INVALID or error_code == EnumErrorCode.DBRERR_POSTALCODE_LICENSE_INVALID:
            cp_text_results = self._BarcodeReader__dbr.GetAllTextResults()
            text_results = []
            if type(cp_text_results) is list:
                for cp_text_result in cp_text_results:
                    text_results.append(TextResult(cp_text_result))

                return text_results
            else:
                return
        else:
            error_message = self._BarcodeReader__dbr.GetErrorString(error_code)
            raise BarcodeReaderError(error_message)

    def get_all_intermediate_results(self):
        """ Returns intermediate results containing the original image, the colour clustered image, the binarized image, contours, lines, text blocks, etc. 
            :return intermediate_results <liset[class IntermediateResult]> : All intermediate results.
        """
        cp_intermediate_results = self._BarcodeReader__dbr.GetAllIntermediateResults()
        if cp_intermediate_results == None:
            return
        else:
            intermediate_results = []
            for cp_intermediate_result in cp_intermediate_results:
                intermediate_results.append(IntermediateResult(cp_intermediate_result))

            return intermediate_results

    def init_frame_decoding_parameters(self):
        """ Init frame decoding parameters.
            :return frame_decoding_parameters <class FrameDecodingParameters> : The frame decoding parameters.
        """
        cp_frame_decoding_parameters = self._BarcodeReader__dbr.InitFrameDecodingParameters()
        try:
            frame_decoding_parameters = FrameDecodingParameters(cp_frame_decoding_parameters)
            return frame_decoding_parameters
        except KeyError as ke:
            print(ke)

    def start_video_mode(self, frame_decoding_parameters, call_back_func, template_name=''):
        """ Starts a new thread to decode barcodes from the inner frame queue.
            :param frame_decoding_parameters <class FrameDecodingParameters> : The frame decoding parameters. You can get it by init_frame_decoding_parameters(), then modify its parameters' value.
            :param call_back_func <function pointer> : Sets callback function to process text results generated during frame decoding.
            :param template_name(optional) <str> : The template name.
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        cp_frame_decoding_parameters = self._BarcodeReader__dbr.InitFrameDecodingParameters()
        try:
            frame_decoding_parameters.update_parameters(cp_frame_decoding_parameters)
        except KeyError as ke:
            print(ke)

        error_code = self._BarcodeReader__dbr.StartVideoMode(cp_frame_decoding_parameters, call_back_func, template_name)
        if error_code != EnumErrorCode.DBR_OK:
            error_message = self._BarcodeReader__dbr.GetErrorString(error_code)
            raise BarcodeReaderError(error_message)

    def append_video_frame(self, video_frame):
        """ Appends a video frame to the inner frame queue. 
            :param video_frame : Gets by opencv.
            :return frame_id <int> : Current frame id.
        """
        frame_id = self._BarcodeReader__dbr.AppendVideoFrame(video_frame)
        return frame_id

    def stop_video_mode(self):
        """ Stops the frame decoding thread created by start_video_mode().
            :exception BarcodeReaderError : If error happens, this function will throw a BarcodeReaderError exception that can report the detailed error message.
        """
        error_code = self._BarcodeReader__dbr.StopVideoMode()
        if error_code != EnumErrorCode.DBR_OK:
            error_message = self._BarcodeReader__dbr.GetErrorString(error_code)
            raise BarcodeReaderError(error_message)

    def get_length_of_frame_queue(self):
        """ Gets current length of the inner frame queue. 
            :return frame_queue_length <int> : The length of the inner frame queue.
        """
        frame_queue_length = self._BarcodeReader__dbr.GetLengthOfFrameQueue()
        return frame_queue_length
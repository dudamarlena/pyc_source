# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/sift.py
# Compiled at: 2019-12-12 01:17:45
# Size of source mod 2**32: 16526 bytes
import cv2, numpy as np
from .error import *
from .utils import generate_result, check_image_valid
from .cal_confidence import cal_ccoeff_confidence, cal_rgb_confidence
FLANN_INDEX_KDTREE = 0
FLANN = cv2.FlannBasedMatcher({'algorithm':FLANN_INDEX_KDTREE,  'trees':5}, dict(checks=50))
FILTER_RATIO = 0.59
ONE_POINT_CONFI = 0.5

def find_sift(im_source, im_search, threshold=0.8, rgb=True, good_ratio=FILTER_RATIO):
    """基于sift进行图像识别，只筛选出最优区域."""
    if not check_image_valid(im_source, im_search):
        return
        kp_sch, kp_src, good = _get_key_points(im_source, im_search, good_ratio)
        if len(good) == 0:
            return
        if len(good) == 1:
            if ONE_POINT_CONFI >= threshold:
                return _handle_one_good_points(kp_src, good, threshold)
            return
        if len(good) == 2:
            origin_result = _handle_two_good_points(im_source, im_search, kp_src, kp_sch, good)
            if isinstance(origin_result, dict):
                if ONE_POINT_CONFI >= threshold:
                    return origin_result
                return
            middle_point, pypts, w_h_range = _handle_two_good_points(im_source, im_search, kp_src, kp_sch, good)
    elif len(good) == 3:
        origin_result = _handle_three_good_points(im_source, im_search, kp_src, kp_sch, good)
        if isinstance(origin_result, dict):
            if ONE_POINT_CONFI >= threshold:
                return origin_result
            return
        middle_point, pypts, w_h_range = _handle_three_good_points(im_source, im_search, kp_src, kp_sch, good)
    else:
        middle_point, pypts, w_h_range = _many_good_pts(im_source, im_search, kp_sch, kp_src, good)
    _target_error_check(w_h_range)
    x_min, x_max, y_min, y_max, w, h = w_h_range
    target_img = im_source[y_min:y_max, x_min:x_max]
    resize_img = cv2.resize(target_img, (w, h))
    confidence = _cal_sift_confidence(im_search, resize_img, rgb=rgb)
    best_match = generate_result(middle_point, pypts, confidence)
    if confidence >= threshold:
        return [best_match]


def find_sift_2(im_source, im_search):
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(im_source, None)
    kp2, des2 = sift.detectAndCompute(im_search, None)
    indexParams = dict(algorithm=0, trees=10)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    matches = flann.knnMatch(des1, des2, k=2)
    matches = sorted(matches, key=(lambda x: x[0].distance))
    goodMatches = []
    for m, n in matches:
        if m.distance < 0.25 * n.distance:
            goodMatches.append(m)

    totalX = 0
    totoalY = 0
    length = len(goodMatches)
    if length > 0:
        for index in xrange(0, length):
            x, y = kp1[goodMatches[index].queryIdx].pt
            totalX += x
            totoalY += y

        midX = totalX / length
        midY = totoalY / length
        point = (
         int(midX), int(midY))
        return point


def mask_sift(im_source, im_search, threshold=0.8, rgb=True, good_ratio=FILTER_RATIO):
    """基于sift查找多个目标区域的方法."""
    raise NotImplementedError


def find_all_sift(im_source, im_search, threshold=0.8, rgb=True, good_ratio=FILTER_RATIO):
    """基于sift查找多个目标区域的方法."""
    raise NotImplementedError


def _init_sift():
    """Make sure that there is SIFT module in OpenCV."""
    if cv2.__version__.startswith('3.'):
        try:
            sift = cv2.xfeatures2d.SIFT_create(edgeThreshold=10)
        except:
            print('to use SIFT, you should build contrib with opencv3.0')
            raise NoSIFTModuleError('There is no SIFT module in your OpenCV environment !')

    else:
        sift = cv2.SIFT(edgeThreshold=10)
    return sift


def _get_key_points(im_source, im_search, good_ratio):
    """根据传入图像,计算图像所有的特征点,并得到匹配特征点对."""
    sift = _init_sift()
    kp_sch, des_sch = sift.detectAndCompute(im_search, None)
    kp_src, des_src = sift.detectAndCompute(im_source, None)
    if len(kp_sch) < 2 or len(kp_src) < 2:
        raise NoSiftMatchPointError('Not enough feature points in input images !')
    matches = FLANN.knnMatch(des_sch, des_src, k=2)
    good = []
    for m, n in matches:
        if m.distance < good_ratio * n.distance:
            good.append(m)

    good_diff, diff_good_point = [], [[]]
    for m in good:
        diff_point = [
         int(kp_src[m.trainIdx].pt[0]), int(kp_src[m.trainIdx].pt[1])]
        if diff_point not in diff_good_point:
            good_diff.append(m)
            diff_good_point.append(diff_point)

    good = good_diff
    return (
     kp_sch, kp_src, good)


def _handle_one_good_points(kp_src, good, threshold):
    """sift匹配中只有一对匹配的特征点对的情况."""
    middle_point = (
     int(kp_src[good[0].trainIdx].pt[0]), int(kp_src[good[0].trainIdx].pt[1]))
    confidence = ONE_POINT_CONFI
    pypts = [middle_point for i in range(4)]
    result = generate_result(middle_point, pypts, confidence)
    if confidence < threshold:
        return
    return result


def _handle_two_good_points(im_source, im_search, kp_src, kp_sch, good):
    """处理两对特征点的情况."""
    pts_sch1 = (
     int(kp_sch[good[0].queryIdx].pt[0]), int(kp_sch[good[0].queryIdx].pt[1]))
    pts_sch2 = (int(kp_sch[good[1].queryIdx].pt[0]), int(kp_sch[good[1].queryIdx].pt[1]))
    pts_src1 = (int(kp_src[good[0].trainIdx].pt[0]), int(kp_src[good[0].trainIdx].pt[1]))
    pts_src2 = (int(kp_src[good[1].trainIdx].pt[0]), int(kp_src[good[1].trainIdx].pt[1]))
    return _two_good_points(pts_sch1, pts_sch2, pts_src1, pts_src2, im_search, im_source)


def _handle_three_good_points(im_source, im_search, kp_src, kp_sch, good):
    """处理三对特征点的情况."""
    pts_sch1 = (
     int(kp_sch[good[0].queryIdx].pt[0]), int(kp_sch[good[0].queryIdx].pt[1]))
    pts_sch2 = (int((kp_sch[good[1].queryIdx].pt[0] + kp_sch[good[2].queryIdx].pt[0]) / 2),
     int((kp_sch[good[1].queryIdx].pt[1] + kp_sch[good[2].queryIdx].pt[1]) / 2))
    pts_src1 = (int(kp_src[good[0].trainIdx].pt[0]), int(kp_src[good[0].trainIdx].pt[1]))
    pts_src2 = (int((kp_src[good[1].trainIdx].pt[0] + kp_src[good[2].trainIdx].pt[0]) / 2),
     int((kp_src[good[1].trainIdx].pt[1] + kp_src[good[2].trainIdx].pt[1]) / 2))
    return _two_good_points(pts_sch1, pts_sch2, pts_src1, pts_src2, im_search, im_source)


def _many_good_pts(im_source, im_search, kp_sch, kp_src, good):
    """特征点匹配点对数目>=4个，可使用单矩阵映射,求出识别的目标区域."""
    sch_pts, img_pts = np.float32([kp_sch[m.queryIdx].pt for m in good]).reshape(-1, 1, 2), np.float32([kp_src[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = _find_homography(sch_pts, img_pts)
    matches_mask = mask.ravel().tolist()
    selected = [v for k, v in enumerate(good) if matches_mask[k]]
    sch_pts, img_pts = np.float32([kp_sch[m.queryIdx].pt for m in selected]).reshape(-1, 1, 2), np.float32([kp_src[m.trainIdx].pt for m in selected]).reshape(-1, 1, 2)
    M, mask = _find_homography(sch_pts, img_pts)
    h, w = im_search.shape[:2]
    h_s, w_s = im_source.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    def cal_rect_pts(dst):
        return [tuple(npt[0]) for npt in dst.astype(int).tolist()]

    pypts = cal_rect_pts(dst)
    lt, br = pypts[0], pypts[2]
    middle_point = (int((lt[0] + br[0]) / 2), int((lt[1] + br[1]) / 2))
    x_min, x_max = min(lt[0], br[0]), max(lt[0], br[0])
    y_min, y_max = min(lt[1], br[1]), max(lt[1], br[1])
    x_min, x_max = int(max(x_min, 0)), int(max(x_max, 0))
    x_min, x_max = int(min(x_min, w_s - 1)), int(min(x_max, w_s - 1))
    y_min, y_max = int(max(y_min, 0)), int(max(y_max, 0))
    y_min, y_max = int(min(y_min, h_s - 1)), int(min(y_max, h_s - 1))
    pts = np.float32([[x_min, y_min], [x_min, y_max],
     [
      x_max, y_max], [x_max, y_min]]).reshape(-1, 1, 2)
    pypts = cal_rect_pts(pts)
    return (
     middle_point, pypts, [x_min, x_max, y_min, y_max, w, h])


def _two_good_points--- This code section failed: ---

 L. 255         0  LOAD_GLOBAL              int
                2  LOAD_FAST                'pts_src1'
                4  LOAD_CONST               0
                6  BINARY_SUBSCR    
                8  LOAD_FAST                'pts_src2'
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  BINARY_ADD       
               16  LOAD_CONST               2
               18  BINARY_TRUE_DIVIDE
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_GLOBAL              int
               24  LOAD_FAST                'pts_src1'
               26  LOAD_CONST               1
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'pts_src2'
               32  LOAD_CONST               1
               34  BINARY_SUBSCR    
               36  BINARY_ADD       
               38  LOAD_CONST               2
               40  BINARY_TRUE_DIVIDE
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  BUILD_LIST_2          2 
               46  STORE_FAST               'middle_point'

 L. 256        48  BUILD_LIST_0          0 
               50  STORE_FAST               'pypts'

 L. 258        52  LOAD_FAST                'pts_sch1'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'pts_sch2'
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_TRUE    116  'to 116'
               68  LOAD_FAST                'pts_sch1'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  LOAD_FAST                'pts_sch2'
               76  LOAD_CONST               1
               78  BINARY_SUBSCR    
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_TRUE    116  'to 116'
               84  LOAD_FAST                'pts_src1'
               86  LOAD_CONST               0
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'pts_src2'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    116  'to 116'
              100  LOAD_FAST                'pts_src1'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'pts_src2'
              108  LOAD_CONST               1
              110  BINARY_SUBSCR    
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   136  'to 136'
            116_0  COME_FROM            98  '98'
            116_1  COME_FROM            82  '82'
            116_2  COME_FROM            66  '66'

 L. 259       116  LOAD_GLOBAL              ONE_POINT_CONFI
              118  STORE_FAST               'confidence'

 L. 260       120  LOAD_GLOBAL              generate_result
              122  LOAD_FAST                'middle_point'
              124  LOAD_FAST                'pypts'
              126  LOAD_FAST                'confidence'
              128  CALL_FUNCTION_3       3  '3 positional arguments'
              130  STORE_FAST               'one_match'

 L. 261       132  LOAD_FAST                'one_match'
              134  RETURN_VALUE     
            136_0  COME_FROM           114  '114'

 L. 263       136  LOAD_FAST                'im_search'
              138  LOAD_ATTR                shape
              140  LOAD_CONST               None
              142  LOAD_CONST               2
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'h'
              152  STORE_FAST               'w'

 L. 264       154  LOAD_FAST                'im_source'
              156  LOAD_ATTR                shape
              158  LOAD_CONST               None
              160  LOAD_CONST               2
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  UNPACK_SEQUENCE_2     2 
              168  STORE_FAST               'h_s'
              170  STORE_FAST               'w_s'

 L. 265       172  LOAD_GLOBAL              abs
              174  LOAD_CONST               1.0
              176  LOAD_FAST                'pts_src2'
              178  LOAD_CONST               0
              180  BINARY_SUBSCR    
              182  LOAD_FAST                'pts_src1'
              184  LOAD_CONST               0
              186  BINARY_SUBSCR    
              188  BINARY_SUBTRACT  
              190  BINARY_MULTIPLY  
              192  LOAD_FAST                'pts_sch2'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'pts_sch1'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  BINARY_SUBTRACT  
              206  BINARY_TRUE_DIVIDE
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  STORE_FAST               'x_scale'

 L. 266       212  LOAD_GLOBAL              abs
              214  LOAD_CONST               1.0
              216  LOAD_FAST                'pts_src2'
              218  LOAD_CONST               1
              220  BINARY_SUBSCR    
              222  LOAD_FAST                'pts_src1'
              224  LOAD_CONST               1
              226  BINARY_SUBSCR    
              228  BINARY_SUBTRACT  
              230  BINARY_MULTIPLY  
              232  LOAD_FAST                'pts_sch2'
              234  LOAD_CONST               1
              236  BINARY_SUBSCR    
              238  LOAD_FAST                'pts_sch1'
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  BINARY_SUBTRACT  
              246  BINARY_TRUE_DIVIDE
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  STORE_FAST               'y_scale'

 L. 268       252  LOAD_GLOBAL              int
              254  LOAD_FAST                'pts_sch1'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_FAST                'pts_sch2'
              262  LOAD_CONST               0
              264  BINARY_SUBSCR    
              266  BINARY_ADD       
              268  LOAD_CONST               2
              270  BINARY_TRUE_DIVIDE
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  LOAD_GLOBAL              int
              276  LOAD_FAST                'pts_sch1'
              278  LOAD_CONST               1
              280  BINARY_SUBSCR    
              282  LOAD_FAST                'pts_sch2'
              284  LOAD_CONST               1
              286  BINARY_SUBSCR    
              288  BINARY_ADD       
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BUILD_TUPLE_2         2 
              298  STORE_FAST               'sch_middle_point'

 L. 269       300  LOAD_FAST                'middle_point'
              302  LOAD_CONST               0
              304  BINARY_SUBSCR    
              306  LOAD_GLOBAL              int
              308  LOAD_FAST                'sch_middle_point'
              310  LOAD_CONST               0
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'w'
              316  LOAD_CONST               2
              318  BINARY_TRUE_DIVIDE
              320  BINARY_SUBTRACT  
              322  LOAD_FAST                'x_scale'
              324  BINARY_MULTIPLY  
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  BINARY_SUBTRACT  
              330  LOAD_FAST                'middle_point'
              332  LOAD_CONST               0
              334  STORE_SUBSCR     

 L. 270       336  LOAD_FAST                'middle_point'
              338  LOAD_CONST               1
              340  BINARY_SUBSCR    
              342  LOAD_GLOBAL              int
              344  LOAD_FAST                'sch_middle_point'
              346  LOAD_CONST               1
              348  BINARY_SUBSCR    
              350  LOAD_FAST                'h'
              352  LOAD_CONST               2
              354  BINARY_TRUE_DIVIDE
              356  BINARY_SUBTRACT  
              358  LOAD_FAST                'y_scale'
              360  BINARY_MULTIPLY  
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  BINARY_SUBTRACT  
              366  LOAD_FAST                'middle_point'
              368  LOAD_CONST               1
              370  STORE_SUBSCR     

 L. 271       372  LOAD_GLOBAL              max
              374  LOAD_FAST                'middle_point'
              376  LOAD_CONST               0
              378  BINARY_SUBSCR    
              380  LOAD_CONST               0
              382  CALL_FUNCTION_2       2  '2 positional arguments'
              384  LOAD_FAST                'middle_point'
              386  LOAD_CONST               0
              388  STORE_SUBSCR     

 L. 272       390  LOAD_GLOBAL              min
              392  LOAD_FAST                'middle_point'
              394  LOAD_CONST               0
              396  BINARY_SUBSCR    
              398  LOAD_FAST                'w_s'
              400  LOAD_CONST               1
              402  BINARY_SUBTRACT  
              404  CALL_FUNCTION_2       2  '2 positional arguments'
              406  LOAD_FAST                'middle_point'
              408  LOAD_CONST               0
              410  STORE_SUBSCR     

 L. 273       412  LOAD_GLOBAL              max
              414  LOAD_FAST                'middle_point'
              416  LOAD_CONST               1
              418  BINARY_SUBSCR    
              420  LOAD_CONST               0
              422  CALL_FUNCTION_2       2  '2 positional arguments'
              424  LOAD_FAST                'middle_point'
              426  LOAD_CONST               1
              428  STORE_SUBSCR     

 L. 274       430  LOAD_GLOBAL              min
              432  LOAD_FAST                'middle_point'
              434  LOAD_CONST               1
              436  BINARY_SUBSCR    
              438  LOAD_FAST                'h_s'
              440  LOAD_CONST               1
              442  BINARY_SUBTRACT  
              444  CALL_FUNCTION_2       2  '2 positional arguments'
              446  LOAD_FAST                'middle_point'
              448  LOAD_CONST               1
              450  STORE_SUBSCR     

 L. 278       452  LOAD_GLOBAL              int
              454  LOAD_GLOBAL              max
              456  LOAD_FAST                'middle_point'
              458  LOAD_CONST               0
              460  BINARY_SUBSCR    
              462  LOAD_FAST                'w'
              464  LOAD_FAST                'x_scale'
              466  BINARY_MULTIPLY  
              468  LOAD_CONST               2
              470  BINARY_TRUE_DIVIDE
              472  BINARY_SUBTRACT  
              474  LOAD_CONST               0
              476  CALL_FUNCTION_2       2  '2 positional arguments'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  LOAD_GLOBAL              int

 L. 279       482  LOAD_GLOBAL              min
              484  LOAD_FAST                'middle_point'
              486  LOAD_CONST               0
              488  BINARY_SUBSCR    
              490  LOAD_FAST                'w'
              492  LOAD_FAST                'x_scale'
              494  BINARY_MULTIPLY  
              496  LOAD_CONST               2
              498  BINARY_TRUE_DIVIDE
              500  BINARY_ADD       
              502  LOAD_FAST                'w_s'
              504  LOAD_CONST               1
              506  BINARY_SUBTRACT  
              508  CALL_FUNCTION_2       2  '2 positional arguments'
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  ROT_TWO          
              514  STORE_FAST               'x_min'
              516  STORE_FAST               'x_max'

 L. 280       518  LOAD_GLOBAL              int
              520  LOAD_GLOBAL              max
              522  LOAD_FAST                'middle_point'
              524  LOAD_CONST               1
              526  BINARY_SUBSCR    
              528  LOAD_FAST                'h'
              530  LOAD_FAST                'y_scale'
              532  BINARY_MULTIPLY  
              534  LOAD_CONST               2
              536  BINARY_TRUE_DIVIDE
              538  BINARY_SUBTRACT  
              540  LOAD_CONST               0
              542  CALL_FUNCTION_2       2  '2 positional arguments'
              544  CALL_FUNCTION_1       1  '1 positional argument'
              546  LOAD_GLOBAL              int

 L. 281       548  LOAD_GLOBAL              min
              550  LOAD_FAST                'middle_point'
              552  LOAD_CONST               1
              554  BINARY_SUBSCR    
              556  LOAD_FAST                'h'
              558  LOAD_FAST                'y_scale'
              560  BINARY_MULTIPLY  
              562  LOAD_CONST               2
              564  BINARY_TRUE_DIVIDE
              566  BINARY_ADD       
              568  LOAD_FAST                'h_s'
              570  LOAD_CONST               1
              572  BINARY_SUBTRACT  
              574  CALL_FUNCTION_2       2  '2 positional arguments'
              576  CALL_FUNCTION_1       1  '1 positional argument'
              578  ROT_TWO          
              580  STORE_FAST               'y_min'
              582  STORE_FAST               'y_max'

 L. 283       584  LOAD_GLOBAL              np
              586  LOAD_METHOD              float32
              588  LOAD_FAST                'x_min'
              590  LOAD_FAST                'y_min'
              592  BUILD_LIST_2          2 
              594  LOAD_FAST                'x_min'
              596  LOAD_FAST                'y_max'
              598  BUILD_LIST_2          2 
              600  LOAD_FAST                'x_max'
              602  LOAD_FAST                'y_max'
              604  BUILD_LIST_2          2 
              606  LOAD_FAST                'x_max'
              608  LOAD_FAST                'y_min'
              610  BUILD_LIST_2          2 
              612  BUILD_LIST_4          4 
              614  CALL_METHOD_1         1  '1 positional argument'
              616  LOAD_METHOD              reshape
              618  LOAD_CONST               -1
              620  LOAD_CONST               1
              622  LOAD_CONST               2
              624  CALL_METHOD_3         3  '3 positional arguments'
              626  STORE_FAST               'pts'

 L. 284       628  SETUP_LOOP          672  'to 672'
              630  LOAD_FAST                'pts'
              632  LOAD_METHOD              astype
              634  LOAD_GLOBAL              int
              636  CALL_METHOD_1         1  '1 positional argument'
              638  LOAD_METHOD              tolist
              640  CALL_METHOD_0         0  '0 positional arguments'
              642  GET_ITER         
              644  FOR_ITER            670  'to 670'
              646  STORE_FAST               'npt'

 L. 285       648  LOAD_FAST                'pypts'
              650  LOAD_METHOD              append
              652  LOAD_GLOBAL              tuple
              654  LOAD_FAST                'npt'
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  CALL_METHOD_1         1  '1 positional argument'
              664  POP_TOP          
          666_668  JUMP_BACK           644  'to 644'
              670  POP_BLOCK        
            672_0  COME_FROM_LOOP      628  '628'

 L. 287       672  LOAD_FAST                'middle_point'
              674  LOAD_FAST                'pypts'
              676  LOAD_FAST                'x_min'
              678  LOAD_FAST                'x_max'
              680  LOAD_FAST                'y_min'
              682  LOAD_FAST                'y_max'
              684  LOAD_FAST                'w'
              686  LOAD_FAST                'h'
              688  BUILD_LIST_6          6 
              690  BUILD_TUPLE_3         3 
              692  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 692


def _find_homography(sch_pts, src_pts):
    """多组特征点对时，求取单向性矩阵."""
    try:
        M, mask = cv2.findHomography(sch_pts, src_pts, cv2.RANSAC, 5.0)
    except Exception:
        import traceback
        traceback.print_exc()
        raise HomographyError('OpenCV error in _find_homography()...')
    else:
        if mask is None:
            raise HomographyError('In _find_homography(), find no mask...')
        else:
            return (
             M, mask)


def _target_error_check--- This code section failed: ---

 L. 307         0  LOAD_FAST                'w_h_range'
                2  UNPACK_SEQUENCE_6     6 
                4  STORE_FAST               'x_min'
                6  STORE_FAST               'x_max'
                8  STORE_FAST               'y_min'
               10  STORE_FAST               'y_max'
               12  STORE_FAST               'w'
               14  STORE_FAST               'h'

 L. 308        16  LOAD_FAST                'x_max'
               18  LOAD_FAST                'x_min'
               20  BINARY_SUBTRACT  
               22  LOAD_FAST                'y_max'
               24  LOAD_FAST                'y_min'
               26  BINARY_SUBTRACT  
               28  ROT_TWO          
               30  STORE_FAST               'tar_width'
               32  STORE_FAST               'tar_height'

 L. 310        34  LOAD_FAST                'tar_width'
               36  LOAD_CONST               5
               38  COMPARE_OP               <
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_FAST                'tar_height'
               44  LOAD_CONST               5
               46  COMPARE_OP               <
               48  POP_JUMP_IF_FALSE    58  'to 58'
             50_0  COME_FROM            40  '40'

 L. 311        50  LOAD_GLOBAL              SiftResultCheckError
               52  LOAD_STR                 'In src_image, Taget area: width or height < 5 pixel.'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            48  '48'

 L. 313        58  LOAD_FAST                'tar_width'
               60  LOAD_CONST               0.2
               62  LOAD_FAST                'w'
               64  BINARY_MULTIPLY  
               66  COMPARE_OP               <
               68  POP_JUMP_IF_TRUE    106  'to 106'
               70  LOAD_FAST                'tar_width'
               72  LOAD_CONST               5
               74  LOAD_FAST                'w'
               76  BINARY_MULTIPLY  
               78  COMPARE_OP               >
               80  POP_JUMP_IF_TRUE    106  'to 106'
               82  LOAD_FAST                'tar_height'
               84  LOAD_CONST               0.2
               86  LOAD_FAST                'h'
               88  BINARY_MULTIPLY  
               90  COMPARE_OP               <
               92  POP_JUMP_IF_TRUE    106  'to 106'
               94  LOAD_FAST                'tar_height'
               96  LOAD_CONST               5
               98  LOAD_FAST                'h'
              100  BINARY_MULTIPLY  
              102  COMPARE_OP               >
              104  POP_JUMP_IF_FALSE   114  'to 114'
            106_0  COME_FROM            92  '92'
            106_1  COME_FROM            80  '80'
            106_2  COME_FROM            68  '68'

 L. 314       106  LOAD_GLOBAL              SiftResultCheckError
              108  LOAD_STR                 'Target area is 5 times bigger or 0.2 times smaller than sch_img.'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 112


def _cal_sift_confidence(im_search, resize_img, rgb=False):
    if rgb:
        confidence = cal_rgb_confidence(im_search, resize_img)
    else:
        confidence = cal_ccoeff_confidence(im_search, resize_img)
    confidence = (1 + confidence) / 2
    return confidence
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/keypoint_base.py
# Compiled at: 2019-12-11 09:22:26
# Size of source mod 2**32: 16680 bytes
"""Detect keypoints with KAZE."""
import cv2, time, numpy as np
from airtest.utils.logger import get_logger
from .error import *
from .utils import generate_result, check_image_valid
from .cal_confidence import cal_ccoeff_confidence, cal_rgb_confidence
LOGGING = get_logger(__name__)

def print_run_time(func):

    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        ret = func(self, *args, **kwargs)
        LOGGING.debug('%s() run time is %.2f s.' % (func.__name__, time.time() - start_time))
        return ret

    return wrapper


class KeypointMatching(object):
    __doc__ = '基于特征点的识别基类: KAZE.'
    METHOD_NAME = 'KAZE'
    FILTER_RATIO = 0.59
    ONE_POINT_CONFI = 0.5

    def __init__(self, im_search, im_source, threshold=0.8, rgb=True):
        super(KeypointMatching, self).__init__()
        self.im_source = im_source
        self.im_search = im_search
        self.threshold = threshold
        self.rgb = rgb

    def mask_kaze(self):
        """基于kaze查找多个目标区域的方法."""
        raise NotImplementedError

    def find_all_results(self):
        """基于kaze查找多个目标区域的方法."""
        raise NotImplementedError

    @print_run_time
    def find_best_result(self):
        """基于kaze进行图像识别，只筛选出最优区域."""
        if not check_image_valid(self.im_source, self.im_search):
            return
            self.kp_sch, self.kp_src, self.good = self._get_key_points()
            if len(self.good) in (0, 1):
                return
            if len(self.good) in (2, 3):
                if len(self.good) == 2:
                    origin_result = self._handle_two_good_points(self.kp_sch, self.kp_src, self.good)
                else:
                    origin_result = self._handle_three_good_points(self.kp_sch, self.kp_src, self.good)
                if origin_result is None:
                    return origin_result
                middle_point, pypts, w_h_range = origin_result
        else:
            middle_point, pypts, w_h_range = self._many_good_pts(self.kp_sch, self.kp_src, self.good)
        self._target_error_check(w_h_range)
        x_min, x_max, y_min, y_max, w, h = w_h_range
        target_img = self.im_source[y_min:y_max, x_min:x_max]
        resize_img = cv2.resize(target_img, (w, h))
        confidence = self._cal_confidence(resize_img)
        best_match = generate_result(middle_point, pypts, confidence)
        LOGGING.debug('[%s] threshold=%s, result=%s' % (self.METHOD_NAME, self.threshold, best_match))
        if confidence >= self.threshold:
            return best_match

    def show_match_image(self):
        """Show how the keypoints matches."""
        from random import random
        h_sch, w_sch = self.im_search.shape[:2]
        h_src, w_src = self.im_source.shape[:2]
        self.find_best_result()
        matching_info_img = np.zeros([max(h_sch, h_src), w_sch + w_src, 3], np.uint8)
        matching_info_img[:h_sch, :w_sch, :] = self.im_search
        matching_info_img[:h_src, w_sch:, :] = self.im_source
        for m in self.good:
            color = tuple([int(random() * 255) for _ in range(3)])
            cv2.line(matching_info_img, (int(self.kp_sch[m.queryIdx].pt[0]), int(self.kp_sch[m.queryIdx].pt[1])), (int(self.kp_src[m.trainIdx].pt[0] + w_sch), int(self.kp_src[m.trainIdx].pt[1])), color)

        return matching_info_img

    def _cal_confidence(self, resize_img):
        """计算confidence."""
        if self.rgb:
            confidence = cal_rgb_confidence(self.im_search, resize_img)
        else:
            confidence = cal_ccoeff_confidence(self.im_search, resize_img)
        confidence = (1 + confidence) / 2
        return confidence

    def init_detector(self):
        """Init keypoint detector object."""
        self.detector = cv2.KAZE_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_L1)

    def get_keypoints_and_descriptors(self, image):
        """获取图像特征点和描述符."""
        keypoints, descriptors = self.detector.detectAndCompute(image, None)
        return (keypoints, descriptors)

    def match_keypoints(self, des_sch, des_src):
        """Match descriptors (特征值匹配)."""
        return self.matcher.knnMatch(des_sch, des_src, k=2)

    def _get_key_points(self):
        """根据传入图像,计算图像所有的特征点,并得到匹配特征点对."""
        self.init_detector()
        kp_sch, des_sch = self.get_keypoints_and_descriptors(self.im_search)
        kp_src, des_src = self.get_keypoints_and_descriptors(self.im_source)
        if len(kp_sch) < 2 or len(kp_src) < 2:
            raise NoMatchPointError('Not enough feature points in input images !')
        matches = self.match_keypoints(des_sch, des_src)
        good = []
        for m, n in matches:
            if m.distance < self.FILTER_RATIO * n.distance:
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

    def _handle_two_good_points(self, kp_sch, kp_src, good):
        """处理两对特征点的情况."""
        pts_sch1 = (
         int(kp_sch[good[0].queryIdx].pt[0]), int(kp_sch[good[0].queryIdx].pt[1]))
        pts_sch2 = (int(kp_sch[good[1].queryIdx].pt[0]), int(kp_sch[good[1].queryIdx].pt[1]))
        pts_src1 = (int(kp_src[good[0].trainIdx].pt[0]), int(kp_src[good[0].trainIdx].pt[1]))
        pts_src2 = (int(kp_src[good[1].trainIdx].pt[0]), int(kp_src[good[1].trainIdx].pt[1]))
        return self._get_origin_result_with_two_points(pts_sch1, pts_sch2, pts_src1, pts_src2)

    def _handle_three_good_points(self, kp_sch, kp_src, good):
        """处理三对特征点的情况."""
        pts_sch1 = (
         int(kp_sch[good[0].queryIdx].pt[0]), int(kp_sch[good[0].queryIdx].pt[1]))
        pts_sch2 = (int((kp_sch[good[1].queryIdx].pt[0] + kp_sch[good[2].queryIdx].pt[0]) / 2),
         int((kp_sch[good[1].queryIdx].pt[1] + kp_sch[good[2].queryIdx].pt[1]) / 2))
        pts_src1 = (int(kp_src[good[0].trainIdx].pt[0]), int(kp_src[good[0].trainIdx].pt[1]))
        pts_src2 = (int((kp_src[good[1].trainIdx].pt[0] + kp_src[good[2].trainIdx].pt[0]) / 2),
         int((kp_src[good[1].trainIdx].pt[1] + kp_src[good[2].trainIdx].pt[1]) / 2))
        return self._get_origin_result_with_two_points(pts_sch1, pts_sch2, pts_src1, pts_src2)

    def _many_good_pts(self, kp_sch, kp_src, good):
        """特征点匹配点对数目>=4个，可使用单矩阵映射,求出识别的目标区域."""
        sch_pts, img_pts = np.float32([kp_sch[m.queryIdx].pt for m in good]).reshape(-1, 1, 2), np.float32([kp_src[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = self._find_homography(sch_pts, img_pts)
        matches_mask = mask.ravel().tolist()
        selected = [v for k, v in enumerate(good) if matches_mask[k]]
        sch_pts, img_pts = np.float32([kp_sch[m.queryIdx].pt for m in selected]).reshape(-1, 1, 2), np.float32([kp_src[m.trainIdx].pt for m in selected]).reshape(-1, 1, 2)
        M, mask = self._find_homography(sch_pts, img_pts)
        h, w = self.im_search.shape[:2]
        h_s, w_s = self.im_source.shape[:2]
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

    def _get_origin_result_with_two_points--- This code section failed: ---

 L. 247         0  LOAD_GLOBAL              int
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

 L. 248        48  BUILD_LIST_0          0 
               50  STORE_FAST               'pypts'

 L. 250        52  LOAD_FAST                'pts_sch1'
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
              114  POP_JUMP_IF_FALSE   120  'to 120'
            116_0  COME_FROM            98  '98'
            116_1  COME_FROM            82  '82'
            116_2  COME_FROM            66  '66'

 L. 251       116  LOAD_CONST               None
              118  RETURN_VALUE     
            120_0  COME_FROM           114  '114'

 L. 253       120  LOAD_FAST                'self'
              122  LOAD_ATTR                im_search
              124  LOAD_ATTR                shape
              126  LOAD_CONST               None
              128  LOAD_CONST               2
              130  BUILD_SLICE_2         2 
              132  BINARY_SUBSCR    
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'h'
              138  STORE_FAST               'w'

 L. 254       140  LOAD_FAST                'self'
              142  LOAD_ATTR                im_source
              144  LOAD_ATTR                shape
              146  LOAD_CONST               None
              148  LOAD_CONST               2
              150  BUILD_SLICE_2         2 
              152  BINARY_SUBSCR    
              154  UNPACK_SEQUENCE_2     2 
              156  STORE_FAST               'h_s'
              158  STORE_FAST               'w_s'

 L. 255       160  LOAD_GLOBAL              abs
              162  LOAD_CONST               1.0
              164  LOAD_FAST                'pts_src2'
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'pts_src1'
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  BINARY_SUBTRACT  
              178  BINARY_MULTIPLY  
              180  LOAD_FAST                'pts_sch2'
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'pts_sch1'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  BINARY_SUBTRACT  
              194  BINARY_TRUE_DIVIDE
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  STORE_FAST               'x_scale'

 L. 256       200  LOAD_GLOBAL              abs
              202  LOAD_CONST               1.0
              204  LOAD_FAST                'pts_src2'
              206  LOAD_CONST               1
              208  BINARY_SUBSCR    
              210  LOAD_FAST                'pts_src1'
              212  LOAD_CONST               1
              214  BINARY_SUBSCR    
              216  BINARY_SUBTRACT  
              218  BINARY_MULTIPLY  
              220  LOAD_FAST                'pts_sch2'
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    
              226  LOAD_FAST                'pts_sch1'
              228  LOAD_CONST               1
              230  BINARY_SUBSCR    
              232  BINARY_SUBTRACT  
              234  BINARY_TRUE_DIVIDE
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  STORE_FAST               'y_scale'

 L. 258       240  LOAD_GLOBAL              int
              242  LOAD_FAST                'pts_sch1'
              244  LOAD_CONST               0
              246  BINARY_SUBSCR    
              248  LOAD_FAST                'pts_sch2'
              250  LOAD_CONST               0
              252  BINARY_SUBSCR    
              254  BINARY_ADD       
              256  LOAD_CONST               2
              258  BINARY_TRUE_DIVIDE
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  LOAD_GLOBAL              int
              264  LOAD_FAST                'pts_sch1'
              266  LOAD_CONST               1
              268  BINARY_SUBSCR    
              270  LOAD_FAST                'pts_sch2'
              272  LOAD_CONST               1
              274  BINARY_SUBSCR    
              276  BINARY_ADD       
              278  LOAD_CONST               2
              280  BINARY_TRUE_DIVIDE
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  BUILD_TUPLE_2         2 
              286  STORE_FAST               'sch_middle_point'

 L. 259       288  LOAD_FAST                'middle_point'
              290  LOAD_CONST               0
              292  BINARY_SUBSCR    
              294  LOAD_GLOBAL              int
              296  LOAD_FAST                'sch_middle_point'
              298  LOAD_CONST               0
              300  BINARY_SUBSCR    
              302  LOAD_FAST                'w'
              304  LOAD_CONST               2
              306  BINARY_TRUE_DIVIDE
              308  BINARY_SUBTRACT  
              310  LOAD_FAST                'x_scale'
              312  BINARY_MULTIPLY  
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  BINARY_SUBTRACT  
              318  LOAD_FAST                'middle_point'
              320  LOAD_CONST               0
              322  STORE_SUBSCR     

 L. 260       324  LOAD_FAST                'middle_point'
              326  LOAD_CONST               1
              328  BINARY_SUBSCR    
              330  LOAD_GLOBAL              int
              332  LOAD_FAST                'sch_middle_point'
              334  LOAD_CONST               1
              336  BINARY_SUBSCR    
              338  LOAD_FAST                'h'
              340  LOAD_CONST               2
              342  BINARY_TRUE_DIVIDE
              344  BINARY_SUBTRACT  
              346  LOAD_FAST                'y_scale'
              348  BINARY_MULTIPLY  
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  BINARY_SUBTRACT  
              354  LOAD_FAST                'middle_point'
              356  LOAD_CONST               1
              358  STORE_SUBSCR     

 L. 261       360  LOAD_GLOBAL              max
              362  LOAD_FAST                'middle_point'
              364  LOAD_CONST               0
              366  BINARY_SUBSCR    
              368  LOAD_CONST               0
              370  CALL_FUNCTION_2       2  '2 positional arguments'
              372  LOAD_FAST                'middle_point'
              374  LOAD_CONST               0
              376  STORE_SUBSCR     

 L. 262       378  LOAD_GLOBAL              min
              380  LOAD_FAST                'middle_point'
              382  LOAD_CONST               0
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'w_s'
              388  LOAD_CONST               1
              390  BINARY_SUBTRACT  
              392  CALL_FUNCTION_2       2  '2 positional arguments'
              394  LOAD_FAST                'middle_point'
              396  LOAD_CONST               0
              398  STORE_SUBSCR     

 L. 263       400  LOAD_GLOBAL              max
              402  LOAD_FAST                'middle_point'
              404  LOAD_CONST               1
              406  BINARY_SUBSCR    
              408  LOAD_CONST               0
              410  CALL_FUNCTION_2       2  '2 positional arguments'
              412  LOAD_FAST                'middle_point'
              414  LOAD_CONST               1
              416  STORE_SUBSCR     

 L. 264       418  LOAD_GLOBAL              min
              420  LOAD_FAST                'middle_point'
              422  LOAD_CONST               1
              424  BINARY_SUBSCR    
              426  LOAD_FAST                'h_s'
              428  LOAD_CONST               1
              430  BINARY_SUBTRACT  
              432  CALL_FUNCTION_2       2  '2 positional arguments'
              434  LOAD_FAST                'middle_point'
              436  LOAD_CONST               1
              438  STORE_SUBSCR     

 L. 268       440  LOAD_GLOBAL              int
              442  LOAD_GLOBAL              max
              444  LOAD_FAST                'middle_point'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  LOAD_FAST                'w'
              452  LOAD_FAST                'x_scale'
              454  BINARY_MULTIPLY  
              456  LOAD_CONST               2
              458  BINARY_TRUE_DIVIDE
              460  BINARY_SUBTRACT  
              462  LOAD_CONST               0
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  LOAD_GLOBAL              int

 L. 269       470  LOAD_GLOBAL              min
              472  LOAD_FAST                'middle_point'
              474  LOAD_CONST               0
              476  BINARY_SUBSCR    
              478  LOAD_FAST                'w'
              480  LOAD_FAST                'x_scale'
              482  BINARY_MULTIPLY  
              484  LOAD_CONST               2
              486  BINARY_TRUE_DIVIDE
              488  BINARY_ADD       
              490  LOAD_FAST                'w_s'
              492  LOAD_CONST               1
              494  BINARY_SUBTRACT  
              496  CALL_FUNCTION_2       2  '2 positional arguments'
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  ROT_TWO          
              502  STORE_FAST               'x_min'
              504  STORE_FAST               'x_max'

 L. 270       506  LOAD_GLOBAL              int
              508  LOAD_GLOBAL              max
              510  LOAD_FAST                'middle_point'
              512  LOAD_CONST               1
              514  BINARY_SUBSCR    
              516  LOAD_FAST                'h'
              518  LOAD_FAST                'y_scale'
              520  BINARY_MULTIPLY  
              522  LOAD_CONST               2
              524  BINARY_TRUE_DIVIDE
              526  BINARY_SUBTRACT  
              528  LOAD_CONST               0
              530  CALL_FUNCTION_2       2  '2 positional arguments'
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  LOAD_GLOBAL              int

 L. 271       536  LOAD_GLOBAL              min
              538  LOAD_FAST                'middle_point'
              540  LOAD_CONST               1
              542  BINARY_SUBSCR    
              544  LOAD_FAST                'h'
              546  LOAD_FAST                'y_scale'
              548  BINARY_MULTIPLY  
              550  LOAD_CONST               2
              552  BINARY_TRUE_DIVIDE
              554  BINARY_ADD       
              556  LOAD_FAST                'h_s'
              558  LOAD_CONST               1
              560  BINARY_SUBTRACT  
              562  CALL_FUNCTION_2       2  '2 positional arguments'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  ROT_TWO          
              568  STORE_FAST               'y_min'
              570  STORE_FAST               'y_max'

 L. 273       572  LOAD_GLOBAL              np
              574  LOAD_METHOD              float32
              576  LOAD_FAST                'x_min'
              578  LOAD_FAST                'y_min'
              580  BUILD_LIST_2          2 
              582  LOAD_FAST                'x_min'
              584  LOAD_FAST                'y_max'
              586  BUILD_LIST_2          2 
              588  LOAD_FAST                'x_max'
              590  LOAD_FAST                'y_max'
              592  BUILD_LIST_2          2 
              594  LOAD_FAST                'x_max'
              596  LOAD_FAST                'y_min'
              598  BUILD_LIST_2          2 
              600  BUILD_LIST_4          4 
              602  CALL_METHOD_1         1  '1 positional argument'
              604  LOAD_METHOD              reshape
              606  LOAD_CONST               -1
              608  LOAD_CONST               1
              610  LOAD_CONST               2
              612  CALL_METHOD_3         3  '3 positional arguments'
              614  STORE_FAST               'pts'

 L. 274       616  SETUP_LOOP          660  'to 660'
              618  LOAD_FAST                'pts'
              620  LOAD_METHOD              astype
              622  LOAD_GLOBAL              int
              624  CALL_METHOD_1         1  '1 positional argument'
              626  LOAD_METHOD              tolist
              628  CALL_METHOD_0         0  '0 positional arguments'
              630  GET_ITER         
              632  FOR_ITER            658  'to 658'
              634  STORE_FAST               'npt'

 L. 275       636  LOAD_FAST                'pypts'
              638  LOAD_METHOD              append
              640  LOAD_GLOBAL              tuple
              642  LOAD_FAST                'npt'
              644  LOAD_CONST               0
              646  BINARY_SUBSCR    
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  CALL_METHOD_1         1  '1 positional argument'
              652  POP_TOP          
          654_656  JUMP_BACK           632  'to 632'
              658  POP_BLOCK        
            660_0  COME_FROM_LOOP      616  '616'

 L. 277       660  LOAD_FAST                'middle_point'
              662  LOAD_FAST                'pypts'
              664  LOAD_FAST                'x_min'
              666  LOAD_FAST                'x_max'
              668  LOAD_FAST                'y_min'
              670  LOAD_FAST                'y_max'
              672  LOAD_FAST                'w'
              674  LOAD_FAST                'h'
              676  BUILD_LIST_6          6 
              678  BUILD_TUPLE_3         3 
              680  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 680

    def _find_homography(self, sch_pts, src_pts):
        """多组特征点对时，求取单向性矩阵."""
        try:
            M, mask = cv2.findHomography(sch_pts, src_pts, cv2.RANSAC, 5.0)
        except Exception:
            import traceback
            traceback.print_exc()
            raise HomographyError('OpenCV error in _find_homography()...')
        else:
            if mask is None:
                raise HomographyError('In _find_homography(), find no transfomation matrix...')
            else:
                return (
                 M, mask)

    def _target_error_check--- This code section failed: ---

 L. 295         0  LOAD_FAST                'w_h_range'
                2  UNPACK_SEQUENCE_6     6 
                4  STORE_FAST               'x_min'
                6  STORE_FAST               'x_max'
                8  STORE_FAST               'y_min'
               10  STORE_FAST               'y_max'
               12  STORE_FAST               'w'
               14  STORE_FAST               'h'

 L. 296        16  LOAD_FAST                'x_max'
               18  LOAD_FAST                'x_min'
               20  BINARY_SUBTRACT  
               22  LOAD_FAST                'y_max'
               24  LOAD_FAST                'y_min'
               26  BINARY_SUBTRACT  
               28  ROT_TWO          
               30  STORE_FAST               'tar_width'
               32  STORE_FAST               'tar_height'

 L. 298        34  LOAD_FAST                'tar_width'
               36  LOAD_CONST               5
               38  COMPARE_OP               <
               40  POP_JUMP_IF_TRUE     50  'to 50'
               42  LOAD_FAST                'tar_height'
               44  LOAD_CONST               5
               46  COMPARE_OP               <
               48  POP_JUMP_IF_FALSE    58  'to 58'
             50_0  COME_FROM            40  '40'

 L. 299        50  LOAD_GLOBAL              MatchResultCheckError
               52  LOAD_STR                 'In src_image, Taget area: width or height < 5 pixel.'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            48  '48'

 L. 301        58  LOAD_FAST                'tar_width'
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

 L. 302       106  LOAD_GLOBAL              MatchResultCheckError
              108  LOAD_STR                 'Target area is 5 times bigger or 0.2 times smaller than sch_img.'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 112
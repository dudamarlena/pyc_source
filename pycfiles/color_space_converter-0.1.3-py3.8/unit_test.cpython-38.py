# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/unit_test.py
# Compiled at: 2020-04-24 19:21:21
# Size of source mod 2**32: 5806 bytes
__author__ = 'Christopher Hahne'
__email__ = 'inbox@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from color_space_converter.top_level import ColorSpaceConverter, METHODS, normalize_img
from color_space_converter import gry_conv, hsv_conv, lab_conv, lms_conv, xyz_conv, yuv_conv
import unittest, os, sys, numpy as np, imageio
from ddt import ddt, idata, unpack, data

@ddt
class ColorSpaceConverterTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        (super(ColorSpaceConverterTester, self).__init__)(*args, **kwargs)

    def setUp(self):
        """ set up test environment """
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')
        self.fn_img = 'chelsea.png'
        self.ref_img = imageio.imread('imageio:' + self.fn_img)
        os.mkdir(self.dat_path) if not os.path.exists(self.dat_path) else None
        fp = os.path.join(self.dat_path, self.fn_img)
        if not os.path.exists(fp):
            imageio.imwrite(uri=fp, im=(normalize_img(self.ref_img)))

    @staticmethod
    def avg_hist_dist(img1, img2, bins=255):
        """ compute average histogram distance """
        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]
        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    @idata(([kw] for kw in (['-s ', '-m "yuv"', '-i', '-s SDTV'],
     [
      '--src=', '--method="hsv"', '--inverse', '--standard=HDTV'])))
    @unpack
    def test_cli(self, kw=None):
        """ scrutinize  CLI command usage """
        from color_space_converter.bin.cli import main
        sys.argv.append(kw[0] + os.path.join(self.dat_path, self.fn_img)) if len(kw) > 0 else None
        sys.argv.append(kw[1]) if len(kw) > 1 else None
        ret = main()
        self.assertEqual(True, ret)
        return True

    @idata(([m, ref] for m, ref in zip(METHODS + ['wrong_arg'], (16971, 255, 515, 2000,
                                                                 583, 474, 0))))
    @unpack
    def test_match_method_imageio--- This code section failed: ---

 L.  91         0  SETUP_FINALLY        46  'to 46'

 L.  93         2  LOAD_GLOBAL              ColorSpaceConverter
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                ref_img
                8  LOAD_METHOD              copy
               10  CALL_METHOD_0         0  ''
               12  LOAD_FAST                'method'
               14  LOAD_CONST               ('method',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  LOAD_METHOD              main
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'img_conv'

 L.  96        24  LOAD_GLOBAL              ColorSpaceConverter
               26  LOAD_FAST                'img_conv'
               28  LOAD_FAST                'method'
               30  LOAD_CONST               True
               32  LOAD_CONST               ('method', 'inverse')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  LOAD_METHOD              main
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'img_inv'
               42  POP_BLOCK        
               44  JUMP_FORWARD        118  'to 118'
             46_0  COME_FROM_FINALLY     0  '0'

 L.  99        46  DUP_TOP          
               48  LOAD_GLOBAL              BaseException
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE   116  'to 116'
               54  POP_TOP          
               56  STORE_FAST               'e'
               58  POP_TOP          
               60  SETUP_FINALLY       104  'to 104'

 L. 101        62  LOAD_GLOBAL              print
               64  LOAD_FAST                'e'
               66  CALL_FUNCTION_1       1  ''
               68  POP_TOP          

 L. 102        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_CONST               True
               76  LOAD_FAST                'method'
               78  LOAD_GLOBAL              METHODS
               80  COMPARE_OP               not-in
               82  POP_JUMP_IF_FALSE    88  'to 88'
               84  LOAD_CONST               True
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            82  '82'
               88  LOAD_CONST               False
             90_0  COME_FROM            86  '86'
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          

 L. 104        94  POP_BLOCK        
               96  POP_EXCEPT       
               98  CALL_FINALLY        104  'to 104'
              100  LOAD_CONST               True
              102  RETURN_VALUE     
            104_0  COME_FROM            98  '98'
            104_1  COME_FROM_FINALLY    60  '60'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            52  '52'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM            44  '44'

 L. 107       118  LOAD_FAST                'self'
              120  LOAD_METHOD              avg_hist_dist
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                ref_img
              126  LOAD_FAST                'img_inv'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'dist_val'

 L. 108       132  LOAD_GLOBAL              print
              134  LOAD_STR                 'Avg. histogram distance for %s is %s'
              136  LOAD_FAST                'method'
              138  LOAD_GLOBAL              round
              140  LOAD_FAST                'dist_val'
              142  LOAD_CONST               3
              144  CALL_FUNCTION_2       2  ''
              146  BUILD_TUPLE_2         2 
              148  BINARY_MODULO    
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L. 111       154  LOAD_FAST                'self'
              156  LOAD_METHOD              assertEqual
              158  LOAD_CONST               True
              160  LOAD_FAST                'ref_val'
              162  LOAD_FAST                'dist_val'
              164  COMPARE_OP               >=
              166  CALL_METHOD_2         2  ''
              168  POP_TOP          

 L. 114       170  LOAD_GLOBAL              os
              172  LOAD_ATTR                path
              174  LOAD_METHOD              join
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                dat_path
              180  LOAD_FAST                'self'
              182  LOAD_ATTR                fn_img
              184  LOAD_METHOD              split
              186  LOAD_STR                 '.'
              188  CALL_METHOD_1         1  ''
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  LOAD_STR                 '_'
              196  BINARY_ADD       
              198  LOAD_FAST                'method'
              200  BINARY_ADD       
              202  LOAD_STR                 '.png'
              204  BINARY_ADD       
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'fp'

 L. 115       210  LOAD_GLOBAL              imageio
              212  LOAD_ATTR                imwrite
              214  LOAD_FAST                'fp'
              216  LOAD_GLOBAL              normalize_img
              218  LOAD_FAST                'img_conv'
              220  CALL_FUNCTION_1       1  ''
              222  LOAD_CONST               ('uri', 'im')
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  POP_TOP          

 L. 118       228  LOAD_GLOBAL              os
              230  LOAD_ATTR                path
              232  LOAD_METHOD              join
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                dat_path
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                fn_img
              242  LOAD_METHOD              split
              244  LOAD_STR                 '.'
              246  CALL_METHOD_1         1  ''
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_STR                 '_'
              254  BINARY_ADD       
              256  LOAD_FAST                'method'
              258  BINARY_ADD       
              260  LOAD_STR                 '_re-converted.png'
              262  BINARY_ADD       
              264  CALL_METHOD_2         2  ''
              266  STORE_FAST               'fp'

 L. 119       268  LOAD_GLOBAL              imageio
              270  LOAD_ATTR                imwrite
              272  LOAD_FAST                'fp'
              274  LOAD_GLOBAL              normalize_img
              276  LOAD_FAST                'img_inv'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_CONST               ('uri', 'im')
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  POP_TOP          

 L. 121       286  LOAD_CONST               True
              288  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 98

    @data((
     ColorSpaceConverter().gry_conv, gry_conv), (
     ColorSpaceConverter().hsv_conv, hsv_conv), (
     ColorSpaceConverter().lab_conv, lab_conv), (
     ColorSpaceConverter().lms_conv, lms_conv), (
     ColorSpaceConverter().xyz_conv, xyz_conv), (
     ColorSpaceConverter().yuv_conv, yuv_conv), (
     ColorSpaceConverter().gry_conv, gry_conv, True), (
     ColorSpaceConverter().hsv_conv, hsv_conv, True), (
     ColorSpaceConverter().lab_conv, lab_conv, True), (
     ColorSpaceConverter().lms_conv, lms_conv, True), (
     ColorSpaceConverter().xyz_conv, xyz_conv, True), (
     ColorSpaceConverter().yuv_conv, yuv_conv, True))
    @unpack
    def test_compare_functions(self, obj_method, prd_method, inverse=False):
        """ validate that instance methods yield same result as their procedural counterparts """
        res_obj = obj_method((self.ref_img.copy()), inverse=inverse)
        res_prd = prd_method((self.ref_img.copy()), inverse=inverse)
        dist_val = self.avg_hist_dist(res_obj, res_prd)
        print('Avg. histogram distance for %s is %s' % (prd_method, round(dist_val, 3)))
        self.assertEqual(True, 1 > dist_val)
        self.assertEqual(True, len(res_obj.shape) == len(res_prd.shape))
        return True


if __name__ == '__main__':
    unittest.main()
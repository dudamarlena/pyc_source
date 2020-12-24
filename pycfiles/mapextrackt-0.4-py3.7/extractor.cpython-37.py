# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MapExtrackt/extractor.py
# Compiled at: 2020-05-09 06:33:31
# Size of source mod 2**32: 29026 bytes
import torch, numpy as np, cv2, datetime, torchvision
from PIL import Image
import PIL
import matplotlib.pyplot as plt
from PIL import Image
from MapExtrackt.functions import get_rows_cols, ResizeMe, convert, weight_images, get_bar, pad_arr, intensity_sort, colourize_image, draw_text

class Features:
    features = {}

    def __init__(self):
        self.features = {}
        self.hooks = 0
        self.names = []
        self.bias = {}

    def hook_fn(self, module, input, output):
        if len(output[0].shape) > 2:
            if output[0].shape[2] > 1:
                self.features[self.hooks] = output
                self.hooks += 1
                if str(module).find('\n') >= 0:
                    name = str(module).split('(')[0] + ' (Block)'
                else:
                    name = str(module).split('(')[0]
                self.add_name(name)

    def add_name(self, name):
        self.names.append(name)

    def get_layers_number(self):
        return len(self.features)

    def get_layer_type(self, layer_no):
        return self.names[layer_no]

    def get_cells(self, layer_no):
        return self.features[layer_no].shape[1]


class FeatureExtractor:

    def __init__(self, model):
        """
        Accepts pytorch models for feature extraction from convolutional layers.
        Must call set_image after to load image before use.

        :param model: (pytorch model)

        """
        self._FeatureExtractor__device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = model.to(self._FeatureExtractor__device)
        self.name = str(self.model).split('(')[0]
        self._FeatureExtractor__hooks = None
        self.layers = None
        self.outputs = []
        self.layer_names = []
        self.image = None
        self._FeatureExtractor__set_default_exp_attrs()

    def __set_default_exp_attrs(self):
        self.colourize = 20
        self.outsize = (800, 600)
        self.out_type = 'pil'
        self.border = 0.03
        self.picture_in_picture = True
        self.write_text = 'full'

    def __str__(self):
        try:
            cells = self.get_total_cells()
        except:
            cells = 'Not Loaded'

        return f"<BASE MODEL: {self.name}>\n---------------------------\n----- Class  settings -----\n---------------------------\nLayers: {self.layers}\nTotal Cells: {cells}\nImage: {'Not Loaded' if self.image == None else self.image.size}\nDevice: {self._FeatureExtractor__device}\n---------------------------\n-- Image output settings --\n---------------------------\nOutput Size: {self.outsize}\nOut Type: {self.out_type}\nBorder Size: {self.border * 100}%\nPicture in picture: {self.picture_in_picture}\nColourize Style: {self.colourize}\nWrite Text: {self.write_text}"

    def __getitem__(self, item):
        if type(item) == int:
            if 0 > item or item > self.layers or type(self.layers) != int:
                raise ValueError(f"Layer Number not in range 0-{self.layers} or not INT\n(Slicing layers not supported)")
            return self.display_from_map(layer_no=item, cell_no=None)
        if len(item) == 2:
            return self.display_from_map(layer_no=(item[0]), cell_no=(item[1]))
        raise ValueError('Too many indices')

    def set_output--- This code section failed: ---

 L. 120         0  LOAD_FAST                'colourize'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    46  'to 46'

 L. 121         8  LOAD_FAST                'colourize'
               10  LOAD_LISTCOMP            '<code_object <listcomp>>'
               12  LOAD_STR                 'FeatureExtractor.set_output.<locals>.<listcomp>'
               14  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               16  LOAD_GLOBAL              range
               18  LOAD_CONST               0
               20  LOAD_CONST               21
               22  CALL_FUNCTION_2       2  '2 positional arguments'
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  COMPARE_OP               in
               30  POP_JUMP_IF_TRUE     40  'to 40'
               32  LOAD_ASSERT              AssertionError
               34  LOAD_STR                 'Colourize value not in correct range of 0-20'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L. 122        40  LOAD_FAST                'colourize'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               colourize
             46_0  COME_FROM             6  '6'

 L. 124        46  LOAD_FAST                'outsize'
               48  LOAD_CONST               None
               50  COMPARE_OP               is-not
               52  POP_JUMP_IF_TRUE     62  'to 62'
               54  LOAD_FAST                'outsize'
               56  LOAD_CONST               False
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   124  'to 124'
             62_0  COME_FROM            52  '52'

 L. 125        62  LOAD_GLOBAL              type
               64  LOAD_FAST                'outsize'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  LOAD_GLOBAL              tuple
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  LOAD_GLOBAL              len

 L. 126        76  LOAD_FAST                'outsize'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  LOAD_CONST               2
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_TRUE    102  'to 102'
             86_0  COME_FROM            72  '72'
               86  LOAD_FAST                'outsize'
               88  LOAD_CONST               False
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE    102  'to 102'
               94  LOAD_ASSERT              AssertionError
               96  LOAD_STR                 'Outsize value not tuple of (Width,Height)'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            84  '84'

 L. 127       102  LOAD_FAST                'outsize'
              104  LOAD_CONST               False
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   118  'to 118'

 L. 128       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               outsize
              116  JUMP_FORWARD        124  'to 124'
            118_0  COME_FROM           108  '108'

 L. 130       118  LOAD_FAST                'outsize'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               outsize
            124_0  COME_FROM           116  '116'
            124_1  COME_FROM            60  '60'

 L. 132       124  LOAD_FAST                'out_type'
              126  LOAD_CONST               None
              128  COMPARE_OP               is-not
              130  POP_JUMP_IF_FALSE   158  'to 158'

 L. 133       132  LOAD_FAST                'out_type'
              134  LOAD_METHOD              lower
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  LOAD_CONST               ('pil', 'np', 'mat')
              140  COMPARE_OP               in
              142  POP_JUMP_IF_TRUE    152  'to 152'
              144  LOAD_ASSERT              AssertionError
              146  LOAD_STR                 'out_type value not in "pil","np","mat"]'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           142  '142'

 L. 134       152  LOAD_FAST                'out_type'
              154  LOAD_FAST                'self'
              156  STORE_ATTR               out_type
            158_0  COME_FROM           130  '130'

 L. 136       158  LOAD_FAST                'border'
              160  LOAD_CONST               None
              162  COMPARE_OP               is-not
              164  POP_JUMP_IF_FALSE   214  'to 214'

 L. 137       166  LOAD_GLOBAL              type
              168  LOAD_FAST                'border'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  LOAD_GLOBAL              float
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   200  'to 200'
              178  LOAD_CONST               0.001
              180  LOAD_FAST                'border'
              182  DUP_TOP          
              184  ROT_THREE        
              186  COMPARE_OP               <
              188  POP_JUMP_IF_FALSE   198  'to 198'
              190  LOAD_CONST               1
              192  COMPARE_OP               <
              194  POP_JUMP_IF_TRUE    208  'to 208'
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           188  '188'
              198  POP_TOP          
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           176  '176'
              200  LOAD_GLOBAL              AssertionError
              202  LOAD_STR                 'Border not float in range 0-1'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  RAISE_VARARGS_1       1  'exception instance'
            208_0  COME_FROM           194  '194'

 L. 138       208  LOAD_FAST                'border'
              210  LOAD_FAST                'self'
              212  STORE_ATTR               border
            214_0  COME_FROM           164  '164'

 L. 140       214  LOAD_FAST                'picture_in_picture'
              216  LOAD_CONST               None
              218  COMPARE_OP               is-not
              220  POP_JUMP_IF_FALSE   248  'to 248'

 L. 141       222  LOAD_GLOBAL              type
              224  LOAD_FAST                'picture_in_picture'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  LOAD_GLOBAL              bool
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_TRUE    242  'to 242'
              234  LOAD_ASSERT              AssertionError
              236  LOAD_STR                 'picture_in_picture value not bool'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  RAISE_VARARGS_1       1  'exception instance'
            242_0  COME_FROM           232  '232'

 L. 142       242  LOAD_FAST                'picture_in_picture'
              244  LOAD_FAST                'self'
              246  STORE_ATTR               picture_in_picture
            248_0  COME_FROM           220  '220'

 L. 144       248  LOAD_FAST                'write_text'
              250  LOAD_CONST               None
              252  COMPARE_OP               is-not
          254_256  POP_JUMP_IF_FALSE   296  'to 296'

 L. 145       258  LOAD_GLOBAL              type
              260  LOAD_FAST                'write_text'
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  LOAD_GLOBAL              str
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   282  'to 282'
              272  LOAD_FAST                'write_text'
              274  LOAD_CONST               ('full', 'some', 'none')
              276  COMPARE_OP               in
          278_280  POP_JUMP_IF_TRUE    290  'to 290'
            282_0  COME_FROM           268  '268'
              282  LOAD_ASSERT              AssertionError
              284  LOAD_STR                 'write_text value not bool or not in ["full","some","none"]'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           278  '278'

 L. 147       290  LOAD_FAST                'write_text'
              292  LOAD_FAST                'self'
              294  STORE_ATTR               write_text
            296_0  COME_FROM           254  '254'

Parse error at or near `STORE_ATTR' instruction at offset 294

    def display_from_map(self, layer_no, cell_no=None, out_type=None, colourize=None, outsize=None, border=None, picture_in_picture=None, write_text=None):
        """
        returns image map of layer N and [cell n] if specified.

        Class settings are updated

        :param layer_no: (int) The specific layer number to output
        :param cell_no: (int) The specific channel that you want to extract  DEFAULT None = Return full map
        :param out_type: (str) "pil" - for pillow image, "mat" for matplotlib, "np" for numpy array
        :param colourize: (int) from 1-20 applies different colour maps 0 == False or B.W Image
        :param outsize: (tuple) The size to reshape the cell in format (w,h)  FALSE defaults to actual size of cell, or stacked cells that form layer.
        :param border: (float in range 0-1) Percentage of cell size to pad with border
        :param picture_in_picture: (bool) Draw original picture over the map
        :param write_text: (str) [default] "full" includes layer,cell, cell size and layer type to output
        "some" only includes layer,cell, cell size
        "none" does not write text to output
        :return: output image
        """
        self.set_output(out_type=out_type, colourize=colourize,
          outsize=outsize,
          border=border,
          picture_in_picture=picture_in_picture,
          write_text=write_text)
        self._FeatureExtractor__has_layers(layer_no)
        img = self._FeatureExtractor__return_feature_map(layer_no, single=cell_no)
        if self.outsize != None:
            img = np.array(ResizeMe(self.outsize)(Image.fromarray(img)))
        else:
            if self.picture_in_picture:
                img = self._FeatureExtractor__write_picture_in_picture(img)
            if self.write_text.lower() != 'none':
                subtext = ''
                img = self._FeatureExtractor__write_text_(img, layer_no, cell_no)
            if self.out_type.lower() == 'pil':
                return Image.fromarray(img)
                if self.out_type.lower() == 'mat':
                    fig = plt.figure()
                    plt.imshow(img)
            else:
                return img

    def __write_text_(self, img, layer_no, cell_no, flip=False):
        if self.write_text.lower() == 'full':
            subtext = self.name + ' - ' + self.layer_names[layer_no]
        elif cell_no is None:
            text = f"Layer {layer_no:<3} Cells {self.get_cells(layer_no):<4} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
        else:
            if type(cell_no) == slice:
                if cell_no.step == None:
                    step_text = ''
                else:
                    step_text = f"Step {cell_no.step}"
                if cell_no.start == None:
                    if cell_no.stop == None:
                        text = f"Layer {layer_no:<3} Cells {self.get_cells(layer_no):<4} {step_text} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
                    elif cell_no.start == None:
                        text = f"Layer {layer_no:<3} Cell Range {'0':<4}-{cell_no.stop:<4} {step_text} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
                elif cell_no.stop == None:
                    text = f"Layer {layer_no:<3} Cell Range {cell_no.start:<4}-{self.get_cells(layer_no):<4} {step_text} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
                else:
                    text = f"Layer {layer_no:<3} Cell Range {cell_no.start:<4}-{cell_no.stop:<4} {step_text} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
            else:
                text = f"Layer {layer_no:<3} Cell # {cell_no + 1:<4} ( {self.outputs[layer_no].shape[0]}x{self.outputs[layer_no].shape[1]} )"
        if flip:
            text, subtext = subtext, text
        img = draw_text(img, text, subtext)
        return img

    def set_image(self, img, order_by_intensity=True, allowed_modules=[], normalize_layer=False, tensor_normalization_mean=[
 0.485, 0.456, 0.406], tensor_normalization_std=[
 0.229, 0.224, 0.225]):
        """
        Used to set the input image.
        Can accept PIL image / numpy array / location of image as string

        :param img: (np.array / Pil image / STR path to file) The input file to be analysed
        :param order_by_intensity: (bool) If TRUE features from each layer are reordered by intensity.
        :param allowed_modules: (list or str) ["conv","relu"]  only extracts conv or relu layers, no need to add full
        name. i.e "conv" will extract Conv2d layers. "pool" would extract any layer is "pool" in the name.
        For models constructed in blocks you can use "block" if you want to extract only the block outputs.
        Empty list [] returns all layers.
        :param normalize_layer: (bool) The output tensor of each layer need normalizing between 0-255 for viewing.
        True conducts this over the whole layer, if false normalization is conducted on an
        image by image basis.
        :param tensor_normalization_std: (list) DEFAULT is for models trained on imagenet False does not apply
        transformation.
        :param tensor_normalization_mean: (list) DEFAULT is for models trained on imagenet False does not apply
        transformation.

        :return: None
        """
        if self._FeatureExtractor__device == 'cuda':
            torch.cuda.empty_cache()
        elif type(tensor_normalization_std) == list:
            if len(tensor_normalization_std) == 3:
                self._FeatureExtractor__tensor_norm_std = tensor_normalization_std
            else:
                self._FeatureExtractor__tensor_norm_std = None
            if type(tensor_normalization_mean) == list and len(tensor_normalization_mean) == 3:
                self._FeatureExtractor__tensor_norm_mean = tensor_normalization_mean
        else:
            self._FeatureExtractor__tensor_norm_mean = None
        self._FeatureExtractor__hooks = self._FeatureExtractor__set_hooks(allowed_modules)
        self.layers = self._FeatureExtractor__hooks.get_layers_number()
        self.outputs = self._FeatureExtractor__hooks.features
        img = self._FeatureExtractor__convert_image_to_torch(img)
        out = self.model(img.unsqueeze(0).to(self._FeatureExtractor__device))
        self.layers = self._FeatureExtractor__hooks.get_layers_number()
        self.outputs = self._FeatureExtractor__hooks.features
        self.layer_names = self._FeatureExtractor__hooks.names
        self._FeatureExtractor__normalize_features(normalize_layer)
        if order_by_intensity:
            for k, v in self.outputs.items():
                self.outputs[k] = intensity_sort(v)

    def get_total_cells(self):
        tot = 0
        for x in range(self.layers):
            for y in range(self.get_cells(x) - 1):
                tot += 1

        return tot

    def get_cells(self, layer_no):
        self._FeatureExtractor__has_layers(layer_no)
        return self.outputs[layer_no].shape[2]

    def write_video(self, out_size, file_name, draw_type='layers', fps=40, time_for_layer=None, transition_perc_layer=None, time_for_cells=None, transition_perc_cells=None, colourize=None, border=None, write_text=None, picture_in_picture=None):
        """
        Used to render video output from feature maps

        :param out_size: (tuple) desired output size
        :param file_name: (str) desired output file name - must be .mp4 ext
        :param draw_type: (str) "layers" to only draw layers "cells" to only draw cells "both" to draw both
        :param fps: (int) fps of video output
        :param transition_perc_cells: (float) changes the fade time of cells, to a % on their onscreen duration
        :param time_for_cells: (int) time in seconds to take to display ALL cells
        :param transition_perc_layer: (float) changes the fade time of layers, to a % on their onscreen duration
        :param time_for_layer:  (int) time in seconds to take to display ALL layers
        :param colourize: (int) from 1-20 applies different colour maps 0 == False or B.W Image
        :param border: (float in range 0-1) Percentage of cell size to pad with border
        :param write_text: (bool) Write layer numbers to output
        :param picture_in_picture: (bool) Draw original image over cell
        :return: None
        """
        self.set_output(colourize=colourize, outsize=out_size,
          border=border,
          picture_in_picture=picture_in_picture,
          write_text=write_text)
        if time_for_layer is not None:
            frames_per_layer = time_for_layer * fps / self.layers + 1
            if transition_perc_layer is not None:
                fade_frames_per_layer = frames_per_layer * transition_perc_layer
                frames_per_layer -= fade_frames_per_layer
            else:
                fade_frames_per_layer = 0
        if time_for_cells is not None:
            frames_per_cell = time_for_cells * fps / self.get_total_cells() + 1
            if transition_perc_cells is not None:
                fade_frames_between_cells = frames_per_cell * transition_perc_cells
                frames_per_cell -= fade_frames_between_cells
            else:
                fade_frames_between_cells = 0
        elif not file_name.endswith('.avi'):
            raise ValueError('Output filename must end with .avi')
        else:
            fourcc = (cv2.VideoWriter_fourcc)(*'XVID')
            out = cv2.VideoWriter(('./' + file_name), fourcc=fourcc, fps=fps, frameSize=out_size)
            if draw_type == 'layers':
                draw_layers = True
                draw_cells = False
            else:
                if draw_type == 'cells':
                    draw_layers = False
                    draw_cells = True
                else:
                    if draw_type == 'both':
                        draw_layers = True
                        draw_cells = True
                    else:
                        raise ValueError('Incorrect draw type')
        tot = self.get_total_cells()
        count = 0
        start = datetime.datetime.now()
        if draw_layers:
            for layer in range(0, self.layers):
                if layer < self.layers - 1:
                    img = self.display_from_map(layer_no=layer, out_type='np', colourize=(self.colourize),
                      outsize=(self.outsize),
                      border=(self.border),
                      picture_in_picture=(self.picture_in_picture))[:, :, ::-1]
                    img1 = self.display_from_map(layer_no=(layer + 1), out_type='np', colourize=(self.colourize),
                      outsize=(self.outsize),
                      border=(self.border),
                      picture_in_picture=(self.picture_in_picture))[:, :, ::-1]
                    img1_base = img1.copy()
                else:
                    img = img1_base.copy()
                    img1 = img1_base.copy()
                if write_text:
                    img = self._FeatureExtractor__write_text_(img, layer_no=layer, cell_no=None)
                    img1 = self._FeatureExtractor__write_text_(img1, layer_no=layer, cell_no=None)
                for times in range(int(frames_per_layer)):
                    out.write(img)

                for im in weight_images(img, img1, int(fade_frames_per_layer)):
                    out.write(im)

                count += 1
                total_time = (datetime.datetime.now() - start).total_seconds()
                print(f"\rDrawing Layers {count:<5}/{self.layers}   Total Time Taken {convert(total_time):10} Time Left {convert(total_time / count * (self.layers - count)):10} {get_bar(count, self.layers + 1)} ",
                  end='')

        count = 0
        start = datetime.datetime.now()
        if draw_cells:
            for layer in range(self.layers):
                for cell in range(self.get_cells(layer) - 1):
                    img = self.display_from_map(layer, cell, colourize=(self.colourize), out_type='np', outsize=(self.outsize),
                      border=(self.border),
                      picture_in_picture=(self.picture_in_picture))[:, :,
                     ::-1]
                    img1 = self._FeatureExtractor__get_next_image(layer, cell, colourize=(self.colourize), outsize=(self.outsize), border=(self.border),
                      picture_in_picture=(self.picture_in_picture))[:, :, ::-1]
                    if self.write_text:
                        img = draw_text(img, f"Layer {layer} Cell {cell}   - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
                        img1 = draw_text(img, f"Layer {layer} Cell {cell}   - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
                    for static in range(frames_per_cell):
                        out.write(img)

                    for im in weight_images(img, img1, fade_frames_between_cells):
                        out.write(im)

                    count += 1
                    total_time = (datetime.datetime.now() - start).total_seconds()
                    print(f"\rDrawing Cells {count:<5}/{tot}   Total Time Taken {convert(total_time):10} Time Left {convert(total_time / count * (tot - count)):10} {get_bar(count, tot)} ",
                      end='')

        print(f"\nVideo saved as {file_name}")
        out.release()

    def __get_next_image(self, x, y, outsize, border, colourize, picture_in_picture):
        try:
            return self.display_from_map(x, (y + 1), colourize=colourize, out_type='np', outsize=outsize, border=border, picture_in_picture=picture_in_picture)
        except:
            return self.display_from_map((x + 1), 0, colourize=colourize, out_type='np', outsize=outsize, border=border, picture_in_picture=picture_in_picture)

    def __normalize_features(self, normalize_layer=True):
        for k, v in self.outputs.items():
            if not normalize_layer:
                for i, img in enumerate(v.squeeze()):
                    mx = torch.max(img.squeeze())
                    mn = torch.min(img.squeeze())
                    changed = (img.squeeze() - mn) / (mx - mn)
                    out = (changed * 255).detach().to('cpu').numpy().astype(np.uint8)
                    if i == 0:
                        new_output = out.reshape((out.shape[0], out.shape[1], 1))
                    else:
                        new_output = np.concatenate((new_output, out.reshape((out.shape[0], out.shape[1], 1))), 2)

                self.outputs[k] = new_output
            else:
                mx = torch.max(v.squeeze())
                mn = torch.min(v.squeeze())
                changed = v.squeeze() - mn
                changed = changed / mx
                print(self._FeatureExtractor__hooks.names[k])
                out = (changed * 255).detach().to('cpu').numpy().astype(np.uint8).transpose((1,
                                                                                             2,
                                                                                             0))
                self.outputs[k] = out

    def __has_layers(self, layer_no):
        if layer_no < 0 or layer_no > self.layers:
            raise ValueError(f"Layer number not available. Please choose layer between range 0-{self.layers}")

    def __set_hooks(self, allowed_modules):
        hooker = Features()
        if type(allowed_modules) == str:
            allowed_modules = [
             allowed_modules]
        allowed_modules = [x.lower() for x in allowed_modules]
        count = 0
        for module in self.model.modules():
            name = ''
            if count != 0 and type(module) is not torch.nn.Sequential and str(module).find('\n') >= 0:
                name = str(module).split('(')[0] + ' (Block)'
            else:
                if str(module).find('\n') < 0:
                    name = str(module).split('(')[0]
            if name.lower().find('linear') >= 0:
                break
            if name != '':
                if len(allowed_modules) > 0:
                    for allow in allowed_modules:
                        if allow in name.lower():
                            count += 1
                            module.register_forward_hook(hooker.hook_fn)

                elif allowed_modules == []:
                    count += 1
                    module.register_forward_hook(hooker.hook_fn)

        if count == 0:
            raise ValueError(f"No layers extracted with current 'allowed_module' paramater {allowed_modules}")
        return hooker

    def __convert_image_to_torch(self, img):
        if type(img) == np.ndarray or type(img) == np.array:
            self.image = Image.fromarray(img)
        else:
            if type(img) == PIL.Image.Image:
                self.image = img
            else:
                if str(type(img)).find('PIL') >= 0:
                    self.image = img
                else:
                    if type(img) == str:
                        self.image = Image.open(img)
                    else:
                        raise ValueError('Input Unknown')
        if self._FeatureExtractor__tensor_norm_std == None:
            transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
        else:
            if type(self._FeatureExtractor__tensor_norm_std) == list:
                transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                 torchvision.transforms.Normalize(self._FeatureExtractor__tensor_norm_mean, self._FeatureExtractor__tensor_norm_std)])
            else:
                raise ValueError('Tensor mean/std error. Must be either None or list(x,x,x) one value for each channel in range 0 to 1')
        return transforms(self.image)

    def __write_picture_in_picture(self, base_img, size=0.25):
        h, w, _ = base_img.shape
        top_img = np.array(self.image)
        t_h, t_w, _ = top_img.shape
        new_w = w * size
        new_h = new_w * (t_h / t_w)
        for x in range(-2, 2):
            try:
                base_img[int(h - new_h) + x:, int(w - new_w):, :] = cv2.resize(top_img, (
                 int(new_w),
                 int(new_h)))
            except ValueError:
                pass

        return base_img

    def __return_feature_map(self, layer_no, single=None):
        total_cells = self.get_cells(layer_no) - 1
        stepper = 1
        if type(single) == slice:
            if single.start == None and single.stop == None:
                length = self.outputs[layer_no].shape[2]
                count = 0
                count_to = total_cells
            else:
                if single.start == None and type(single.stop) == int:
                    length = single.stop
                    count = 0
                    count_to = single.stop
                else:
                    if type(single.start) == int:
                        if single.stop == None:
                            length = total_cells - single.start
                            count = single.start
                            count_to = total_cells
                        else:
                            length = single.stop - single.start
                            count = single.start
                            count_to = single.stop
                    elif single.step == None:
                        pass
                    elif single.step < 0:
                        count, count_to = count_to, count
                        if count == total_cells:
                            count = total_cells
                        stepper = single.step
                    else:
                        if single.step >= 1:
                            stepper = single.step
                    if length < 0:
                        length *= -1
            if hasattr(single, 'step') and single.step is not None and single.step != -1:
                length = int(length / abs(single.step))
        elif single != None:
            if 0 <= single < total_cells:
                img = self.outputs[layer_no][:, :, single]
                if self.colourize > -1:
                    img = colourize_image(img, self.colourize)
                if self.border is not None or self.border != 0:
                    img = pad_arr(img, self.border)
                return img
        if single == None:
            length = self.outputs[layer_no].shape[2]
            count = 0
            count_to = total_cells
        else:
            if single < 0 or single > total_cells:
                if single is not None:
                    raise ValueError(f"Cell number not valid please select from range 0-{total_cells}")
            x, y = get_rows_cols(length, width=(self.outputs[layer_no].shape[1]),
              height=(self.outputs[layer_no].shape[0]),
              act_size=(self.outsize))
            for idx in range(x):
                for idy in range(y):
                    img = self.outputs[layer_no][:, :, count]
                    if self.colourize > -1:
                        img = colourize_image(img, self.colourize)
                    else:
                        if self.border != None:
                            img = pad_arr(img, self.border)
                        if idy == 0:
                            colu = img
                        else:
                            colu = np.hstack([colu, img])
                    if count + stepper > count_to and stepper > 0:
                        break
                    elif count + stepper < count_to and stepper < 0:
                        break
                    else:
                        count += stepper

                if idx == 0:
                    rows = colu
                else:
                    rows = np.vstack([rows, colu])

            return rows
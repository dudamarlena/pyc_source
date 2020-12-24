# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MapExtrakt/extractor.py
# Compiled at: 2020-05-05 10:13:51
# Size of source mod 2**32: 19554 bytes
import torch
import torchvision.transforms as transforms
import numpy as np, cv2, datetime
from PIL import Image
import PIL
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import os

def get_rows_cols(no, width, height, act_size):
    act_h = act_size[1]
    act_w = act_size[0]
    ratio = act_h / act_w
    answers = {}
    for x in range(100):
        for y in range(100):
            if x * y == no:
                answers[abs(x * height / (y * width) - ratio)] = [
                 x, y]

    return (
     answers[sorted(answers.keys())[0]][0], answers[sorted(answers.keys())[0]][1])


class ResizeMe(object):

    def __init__(self, desired_size):
        self.desired_size = desired_size

    def __call__(self, img):
        img = np.array(img).astype(np.uint8)
        desired_ratio = self.desired_size[1] / self.desired_size[0]
        actual_ratio = img.shape[0] / img.shape[1]
        desired_ratio1 = self.desired_size[0] / self.desired_size[1]
        actual_ratio1 = img.shape[1] / img.shape[0]
        if desired_ratio < actual_ratio:
            img = cv2.resize(img, (int(self.desired_size[1] * actual_ratio1), self.desired_size[1]), None, interpolation=(cv2.INTER_AREA))
        else:
            if desired_ratio > actual_ratio:
                img = cv2.resize(img, (self.desired_size[0], int(self.desired_size[0] * actual_ratio)), None, interpolation=(cv2.INTER_AREA))
            else:
                img = cv2.resize(img, (self.desired_size[0], self.desired_size[1]), None, interpolation=(cv2.INTER_AREA))
        h, w, _ = img.shape
        new_img = np.zeros((self.desired_size[1], self.desired_size[0], 3))
        hh, ww, _ = new_img.shape
        yoff = int((hh - h) / 2)
        xoff = int((ww - w) / 2)
        new_img[yoff:yoff + h, xoff:xoff + w, :] = img
        return Image.fromarray(new_img.astype(np.uint8))


def normalize_output(img):
    img = img - img.min()
    img = img / img.max()
    return img


def convert(seconds):
    seconds = seconds % 86400
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '%d:%02d:%02d' % (hour, minutes, seconds)


def weight_images(img, img1, fades=4):
    for x in np.linspace(0, 1, fades + 1):
        yield cv2.addWeighted(np.array(img), 1 - x, np.array(img1), x, 0)


def get_bar(current, maxx, bar_length=30, bar_load='=', bar_blank='-'):
    perc = current / maxx
    bar = int(round(bar_length * perc, 0))
    blank = int(round(bar_length - bar_length * perc, 0))
    return '[' + bar_load * bar + bar_blank * blank + ']' + f" {round(current / maxx * 100, 2)} % "


class FeatureExtractor:

    def __init__(self, model):
        """
        Accepts pytorch models for feature extraction from convolutional layers.
        Must call set_image after to load image before use.

        :param model: (pytorch model)

        """
        self._FeatureExtractor__device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = model.to(self._FeatureExtractor__device)
        self.layers = self._FeatureExtractor__create_layers(count=True) - 1
        self.outputs = {}
        self.image = None

    def display_from_map(self, layer_no, cell_no=None, out_type='pil', colourize=20, outsize=None, border=None, picture_in_picture=True):
        """
        returns image map of layer N and [cell n] if specified.

        :param layer_no: (int) The specific layer number to output
        :param cell_no: (int) The specific channel that you want to extract  DEFAULT None = Return full map
        :param out_type: (str) "pil" - for pillow image, "mat" for matplotlib, "np" for numpy array
        :param colourize: (int) from 1-20 applies different colour maps 0 == False or B.W Image
        :param outsize: (tuple) The size to reshape the cell in format (w,h)
        :param border: (float in range 0-1) Percentage of cell size to pad with border
        :param picture_in_picture: (bool) Draw original picture over the map
        :return:
        """
        self._FeatureExtractor__has_layers(layer_no)
        img = self._FeatureExtractor__return_feature_map(layer_no, single=cell_no, border=border, colourize=colourize, out_size=outsize)
        if outsize != None:
            img = np.array(ResizeMe(outsize)(Image.fromarray(img)))
        else:
            if picture_in_picture:
                img = self._FeatureExtractor__write_picture_in_picture(img)
            if out_type.lower() == 'pil':
                return Image.fromarray(img)
                if out_type.lower() == 'mat':
                    fig = plt.figure()
                    plt.imshow(img)
            else:
                return img

    def set_image(self, img, order_by_intensity=True):
        """
        Used to set the imput image.
        Can accept PIL image / numpy array / location of image as string

        :param img: (np.array / Pil image / STR path to file) The input file to be analysed
        :param order_by_intensity: (bool) If TRUE features from each layer are reordered by intensity.
        :return:
        """
        img = self._FeatureExtractor__convert_image_to_torch(img)
        self._FeatureExtractor__create_layers(img, intensity=order_by_intensity)

    def get_total_cells(self):
        tot = 0
        for x in range(self.layers):
            for y in range(self.get_cells(x)):
                tot += 1

        return tot

    def get_cells(self, layer_no):
        self._FeatureExtractor__has_layers(layer_no)
        return self.outputs[layer_no].shape[1] - 1

    def write_video(self, out_size, file_name, colourize=20, border=0.03, fps=40, frames_per_cell=1, fade_frames_between_cells=2, write_text=True, picture_in_picture=True, frames_per_layer=90, fade_frames_per_layer=20, draw_type='layers'):
        """
        Used to render video output from feature maps

        :param out_size: (tuple) desired output size
        :param file_name: (str) desired output file name - must be .mp4 ext
        :param colourize: (int) from 1-20 applies different colour maps 0 == False or B.W Image
        :param border: (float in range 0-1) Percentage of cell size to pad with border
        :param fps: (int) fps of video output, more = faster video
        :param frames_per_cell: (int) number of static frames for each map: more = longer screen time per cell
        :param fade_frames_between_cells: (int) number of frames to fade between cells: more = smoother transition
        :param write_text: (bool) Write layer numbers to output
        :param picture_in_picture: (bool) Draw original image over cell
        :param frames_per_layer: (int) Frames to draw per layer IF draw_layers == True
        :param fade_frames_per_layer: Frames to fade between layers IF draw_layers == True
        :param draw_type: (str) "layers" to only draw layers "cells" to only draw cells "both" to draw both
        :return: None
        """
        if not file_name.endswith('.mp4'):
            raise ValueError('Output filename must end with .mp4')
        else:
            fourcc = cv2.VideoWriter_fourcc('x', 'v', 'i', 'd')
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
            for layer in range(0, self.layers + 1):
                if layer < self.layers:
                    img = self.display_from_map(layer_no=layer, out_type='np', colourize=colourize, outsize=out_size, border=border,
                      picture_in_picture=picture_in_picture)
                    img1 = self.display_from_map(layer_no=(layer + 1), out_type='np', colourize=colourize, outsize=out_size,
                      border=border,
                      picture_in_picture=picture_in_picture)
                    img1_base = img1.copy()
                else:
                    img = img1_base.copy()
                    img1 = img1_base.copy()
                if write_text:
                    img = self._FeatureExtractor__draw_text(img, f"Layer {layer}  Cells {self.get_cells(layer) + 1: 4} - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
                    img1 = self._FeatureExtractor__draw_text(img1, f"Layer {layer} - Cells {self.get_cells(layer) + 1: 4} - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
                for times in range(frames_per_layer):
                    out.write(img[:, :, ::-1])

                for im in weight_images(img, img1, fade_frames_per_layer):
                    out.write(im[:, :, ::-1])

                count += 1
                total_time = (datetime.datetime.now() - start).total_seconds()
                print(f"\rDrawing Layers {count:<5}/{self.layers + 1}   Total Time Taken {convert(total_time):10} Time Left {convert(total_time / count * (self.layers + 1 - count)):10} {get_bar(count, self.layers + 1)} ",
                  end='')

        count = 0
        start = datetime.datetime.now()
        if draw_cells:
            for layer in range(self.layers):
                for cell in range(self.get_cells(layer)):
                    img = self.display_from_map(layer, cell, colourize=colourize, out_type='np', outsize=out_size, border=border,
                      picture_in_picture=picture_in_picture)[:, :, ::-1]
                    img1 = self._FeatureExtractor__get_next_image(layer, cell, colourize=colourize, outsize=out_size, border=border, picture_in_picture=picture_in_picture)[:, :, ::-1]
                    if write_text:
                        img = self._FeatureExtractor__draw_text(img, f"Layer {layer} Cell {cell}   - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
                        img1 = self._FeatureExtractor__draw_text(img, f"Layer {layer} Cell {cell}   - {self.outputs[layer].size()[2]}x{self.outputs[layer].size()[3]}")
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

    def __draw_text(self, img, text):
        img = Image.fromarray(img)
        size = int(img.size[0] / 20)
        if os.name == 'nt':
            font = ImageFont.truetype('C:\\Windows\\Fonts\x07rial.ttf', size)
        else:
            if os.name == 'posix':
                try:
                    font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf', size)
                except:
                    font = ImageFont.truetype('/usr/share/consolefonts/FOO.psf.gz', size)

        draw = ImageDraw.Draw(img)
        draw.text((int(img.size[0] * 0.01), int(img.size[1] * 0.01)), text, (255, 255,
                                                                             255), font=font, stroke_width=2, stroke_fill=(0,
                                                                                                                           0,
                                                                                                                           0))
        return np.array(img)

    def __has_layers(self, layer_no):
        if layer_no < 0 or layer_no > self.layers:
            raise ValueError(f"Layer number not available. Please choose layer between range 0-{self.layers}")

    def __create_layers(self, x=None, count=False, intensity=True):
        if count:
            x = torch.rand(1, 3, 400, 400).to(self._FeatureExtractor__device)
        self.outputs = {}
        counter = -1
        for name, module in self.model.named_children():
            try:
                if type(module) == torch.nn.modules.Sequential:
                    for module1 in module.children():
                        x = module1(x)
                        if 'Conv' in str(module1):
                            counter = counter + 1
                            if intensity:
                                self.outputs[counter] = self._FeatureExtractor__intensity_sort(x).squeeze(1)
                            else:
                                self.outputs[counter] = x

                else:
                    x = module(x)
                    if 'Conv' in str(module):
                        counter = counter + 1
                        if intensity:
                            self.outputs[counter] = self._FeatureExtractor__intensity_sort(x).squeeze(1)
                        else:
                            self.outputs[counter] = x
            except RuntimeError as e:
                try:
                    if str(e).find('size mismatch') < 0:
                        print('Error !')
                        print(e)
                finally:
                    e = None
                    del e

        if count:
            return counter

    def __convert_image_to_torch(self, img):
        if type(img) == np.ndarray or type(img) == np.array:
            self.image = Image.fromarray(img)
            img = torch.tensor(img.transpose((2, 0, 1))).unsqueeze(0).float().to(self._FeatureExtractor__device)
        else:
            if type(img) == PIL.Image.Image:
                self.image = img
                img = torch.tensor(np.array(img).astype(np.uint8).transpose((2, 0,
                                                                             1))).unsqueeze(0).float().to(self._FeatureExtractor__device)
            else:
                if type(img) == str:
                    self.image = Image.fromarray(cv2.imread(img))
                    img = torch.tensor(cv2.imread(img).transpose((2, 0, 1))).unsqueeze(0).float().to(self._FeatureExtractor__device)
                else:
                    raise ValueError('Input Unknown')
        return img

    def __colourize(self, img, colour_type=0):
        if colour_type == 0:
            base = np.zeros((img.shape[0], img.shape[1], 3))
            base[:, :, 0] = img
            base[:, :, 1] = img
            base[:, :, 2] = img
        else:
            return cv2.applyColorMap(img, colour_type, None)

    def __write_picture_in_picture(self, base_img, size=0.25):
        h, w, _ = base_img.shape
        top_img = np.array(self.image)[:, :, ::-1]
        t_h, t_w, _ = top_img.shape
        new_w = w * size
        new_h = new_w * (t_h / t_w)
        try:
            base_img[int(h - new_h) + 1:, int(w - new_w):, :] = cv2.resize(top_img, (
             int(new_w),
             int(new_h)))
        except ValueError:
            base_img[int(h - new_h):, int(w - new_w):, :] = cv2.resize(top_img, (
             int(new_w),
             int(new_h)))

        return base_img

    def __return_feature_map(self, layer_no, single=None, border=None, colourize=20, out_size=None):
        out = (normalize_output(self.outputs[layer_no][0, :, :, :]) * 255).to('cpu').detach().numpy().astype(np.uint8).transpose(1, 2, 0)
        length = out.shape[2]
        if single != None:
            if type(single) == int and not single > length:
                if single < 0:
                    raise ValueError(f"Cell number not valid please select from range 0-{length}")
                img = out[:, :, single]
                img = self._FeatureExtractor__colourize(img, colourize)
                if border != None:
                    img = self._FeatureExtractor__pad_arr(img, border)
                return img
        x, y = get_rows_cols(length, width=(out.shape[1]), height=(out.shape[0]), act_size=out_size)
        count = 0
        for idx in range(x):
            for idy in range(y):
                img = out[:, :, count]
                img = self._FeatureExtractor__colourize(img, colourize)
                if border != None:
                    img = self._FeatureExtractor__pad_arr(img, border)
                elif idy == 0:
                    colu = img
                else:
                    colu = np.hstack([colu, img])
                count += 1

            if idx == 0:
                rows = colu
            else:
                rows = np.vstack([rows, colu])

        return rows

    def __intensity_sort(self, tensor):
        pixel_mean = {}
        for i, x in enumerate(tensor.view(1, tensor.size(1), -1).squeeze()):
            pixel_mean[i] = torch.mean(x)

        pixel_mean = {k:v for k, v in sorted((pixel_mean.items()), key=(lambda item: item[1]), reverse=True)}
        return tensor[:, [list(pixel_mean.keys())], :, :]

    def __pad_arr(self, img, size):
        imgchange = Image.fromarray(img)
        pad = int(imgchange.size[0] * size)
        if pad <= 0:
            pad = 1
        return np.array(transforms.functional.pad(img=imgchange, padding=pad, fill=(0,
                                                                                    0,
                                                                                    0)))
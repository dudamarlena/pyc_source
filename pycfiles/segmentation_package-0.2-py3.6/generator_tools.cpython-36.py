# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\segmentation_tools\generator_tools.py
# Compiled at: 2019-03-11 07:41:09
# Size of source mod 2**32: 8763 bytes
import glob, itertools, os, h5py, numpy as np, PIL.Image as Image
from tqdm import tqdm, trange
import cv2
from segmentation_module.segmentation_tools.generator import data_generator, read_h5
from segmentation_module.segmentation_tools.segmentation_tools import map_label_2_sandwich
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir

def read_img(filename, width, height):
    img = cv2.imread(filename, 1)
    img = cv2.resize(img, (width, height))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def normalize_img(img, operations=[
 'subtract_mean', 'divide']):
    if 'divide' in operations:
        divider = 255.0
    else:
        divider = 1
    if 'subtract_mean' in operations:
        img = img / divider
        img[:, :, 0] -= 103.939 / divider
        img[:, :, 1] -= 116.779 / divider
        img[:, :, 2] -= 123.68 / divider
    return img


class DataGenerator(object):

    def __init__(self, images_path, segs_path, width, height, nClasses, is_h5=False, h5_path='', dataset_type=''):
        images = get_photos_from_dir(images_path)
        images.sort()
        labels = get_photos_from_dir(segs_path)
        labels.sort()
        self.width = width
        self.height = height
        self.nClasses = nClasses
        if not len(images) == len(labels):
            raise AssertionError
        else:
            self.dataset_size = len(images)
            perm = np.random.permutation(self.dataset_size)
            images = np.array(images)[perm]
            labels = np.array(labels)[perm]
            if is_h5:
                print('Starting reading images.')
                images = self._read_img_from_h5_file(h5_path, self.width, self.height, dataset_type, 'img')
                print('Loaded {} images to generator.'.format(len(images)))
                print('Starting reading labels.')
                labels = self._read_img_from_h5_file(h5_path, self.width, self.height, dataset_type, 'labels')
                print('Loaded {} labels to generator.'.format(len(labels)))
            else:
                print('Starting reading images.')
                images = self._read_imgs_to_numpy(images, self.width, self.height)
                print('Loaded {} images to generator.'.format(len(images)))
                print('Starting reading labels.')
                labels = self._read_labels_to_numpy(labels, self.width, self.height, nClasses)
                print('Loaded {} labels to generator.'.format(len(labels)))
        self.zipped = itertools.cycle(zip(images, labels))

    def _read_labels_to_numpy(self, filenames, width, height, nClasses):
        labels = []
        for filename in tqdm(filenames):
            label_img = np.asarray(Image.open(filename))
            labels.append(label_img)

        labels = np.array(labels)
        return labels

    def _read_imgs_to_numpy(self, filenames, width, height):
        imgs = []
        for filename in tqdm(filenames):
            img = read_img(filename, width, height)
            imgs.append(img)

        imgs = np.array(imgs)
        return imgs

    def generate_imgs(self, batch_size, augmentation=False):
        augmentator = DataAugmentator(verbose=False)
        while True:
            X = []
            Y = []
            for _ in range(batch_size):
                img, label = next(self.zipped)
                if augmentation:
                    p = np.random.rand(1)[0]
                    if p > 0.9:
                        img, label = augmentator(img, label)
                img = img.astype(np.float32)
                img = normalize_img(img, operations=[])
                label_processed = map_label_2_sandwich(label, self.nClasses, self.width, self.height)
                X.append(img)
                Y.append(label_processed)

            print(np.array(X).shape)
            yield (
             np.array(X), np.array(Y))

    def _reshape_image_set(self, dataset, width, height, nchannels):
        reshaped_dataset = []
        for image in dataset:
            image = image.reshape(height, width, nchannels)
            reshaped_dataset.append(image)

        return np.array(reshaped_dataset)

    def _read_img_from_h5_file(self, h5_filename, width, height, dataset_type, images_type='img'):
        """
                Read data from h5 file to numpy arrays
                """
        data = h5py.File(h5_filename, 'r')
        if images_type == 'labels':
            img_raw = data.get('/' + dataset_type + '/y')
            img = self._reshape_image_set(img_raw, width, height, 1)
        else:
            imgs_raw = data.get('/' + dataset_type + '/x')
            img = self._reshape_image_set(imgs_raw, width, height, 3)
        return img

    def _get_images_list_from_h5(self, image_set):
        images = []
        for image in image_set:
            images.append(image)

        return np.array(images)


def prepare_generators_adapt(config_parameters, config_paths, config_classes):
    train_batch_size = config_parameters['train_batch_size']
    val_batch_size = config_parameters['val_batch_size']
    h5_path = config_paths['h5_file_path']
    height = config_parameters['input_height']
    width = config_parameters['input_width']
    classes_no = max(list(config_classes.values())) + 1
    x_train, y_train, x_val, y_val, train_dataset_size, val_dataset_size = read_h5(h5_path)
    train_gen = data_generator(x_train, y_train, height, width, config_classes, train_batch_size, 'train')
    val_gen = data_generator(x_val, y_val, height, width, config_classes, val_batch_size, 'val')
    steps_per_train_epoch = np.ceil(train_dataset_size / train_batch_size)
    steps_per_val_epoch = np.ceil(val_dataset_size / val_batch_size)
    return (
     train_gen, val_gen, steps_per_train_epoch, steps_per_val_epoch)
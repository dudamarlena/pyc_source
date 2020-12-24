# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/generator.py
# Compiled at: 2020-04-26 23:42:39
# Size of source mod 2**32: 32278 bytes
import csv, os, os.path, random, sys
from collections import OrderedDict
import numpy as np
from PIL import Image
from six import raise_from
import tensorflow.keras as K
from tensorflow.keras.utils import Sequence
from notekeras.model.retinanet.utils.anchors import anchor_targets_bbox, anchors_for_shape, guess_shapes
from notekeras.model.retinanet.utils.config import parse_anchor_parameters
from notekeras.model.retinanet.utils.image import TransformParameters, adjust_transform_for_image
from notekeras.model.retinanet.utils.image import apply_transform, preprocess_image, resize_image
from notekeras.model.retinanet.utils.image import read_image_bgr
from notekeras.model.retinanet.utils.transform import transform_aabb
from notekeras.utils import read_lines

class Generator(Sequence):

    def __init__(self, transform_generator=None, visual_effect_generator=None, batch_size=1, group_method='ratio', shuffle_groups=True, image_min_side=800, image_max_side=1333, no_resize=False, transform_parameters=None, compute_anchor_targets=anchor_targets_bbox, compute_shapes=guess_shapes, preprocess_image=preprocess_image, config=None):
        """ Initialize Generator object.

        Args
            transform_generator    : A generator used to randomly transform images and annotations.
            batch_size             : The size of the batches to generate.
            group_method           : Determines how images are grouped together (defaults to 'ratio', one of ('none', 'random', 'ratio')).
            shuffle_groups         : If True, shuffles the groups each epoch.
            image_min_side         : After resizing the minimum side of an image is equal to image_min_side.
            image_max_side         : If after resizing the maximum side is larger than image_max_side, scales down further so that the max side is equal to image_max_side.
            no_resize              : If True, no image/annotation resizing is performed.
            transform_parameters   : The transform parameters used for data augmentation.
            compute_anchor_targets : Function handler for computing the targets of anchors for an image and its annotations.
            compute_shapes         : Function handler for computing the shapes of the pyramid for a given input.
            preprocess_image       : Function handler for preprocessing an image (scaling / normalizing) for passing through a network.
        """
        self.transform_generator = transform_generator
        self.visual_effect_generator = visual_effect_generator
        self.batch_size = int(batch_size)
        self.group_method = group_method
        self.shuffle_groups = shuffle_groups
        self.image_min_side = image_min_side
        self.image_max_side = image_max_side
        self.no_resize = no_resize
        self.transform_parameters = transform_parameters or TransformParameters()
        self.compute_anchor_targets = compute_anchor_targets
        self.compute_shapes = compute_shapes
        self.preprocess_image = preprocess_image
        self.config = config
        self.group_images()
        if self.shuffle_groups:
            self.on_epoch_end()

    def on_epoch_end(self):
        if self.shuffle_groups:
            random.shuffle(self.groups)

    def size(self):
        """ Size of the dataset.
        """
        raise NotImplementedError('size method not implemented')

    def num_classes(self):
        """ Number of classes in the dataset.
        """
        raise NotImplementedError('num_classes method not implemented')

    def has_label(self, label):
        """ Returns True if label is a known label.
        """
        raise NotImplementedError('has_label method not implemented')

    def has_name(self, name):
        """ Returns True if name is a known class.
        """
        raise NotImplementedError('has_name method not implemented')

    def name_to_label(self, name):
        """ Map name to label.
        """
        raise NotImplementedError('name_to_label method not implemented')

    def label_to_name(self, label):
        """ Map label to name.
        """
        raise NotImplementedError('label_to_name method not implemented')

    def image_aspect_ratio(self, image_index):
        """ Compute the aspect ratio for an image with image_index.
        """
        raise NotImplementedError('image_aspect_ratio method not implemented')

    def image_path(self, image_index):
        """ Get the path to an image.
        """
        raise NotImplementedError('image_path method not implemented')

    def load_image(self, image_index):
        """ Load an image at the image_index.
        """
        raise NotImplementedError('load_image method not implemented')

    def load_annotations(self, image_index):
        """ Load annotations for an image_index.
        """
        raise NotImplementedError('load_annotations method not implemented')

    def load_annotations_group(self, group):
        """ Load annotations for all images in group.
        """
        annotations_group = [self.load_annotations(image_index) for image_index in group]
        for annotations in annotations_group:
            assert isinstance(annotations, dict), "'load_annotations' should return a list of dictionaries, received: {}".format(type(annotations))
            assert 'labels' in annotations, "'load_annotations' should return a list of dictionaries that contain 'labels' and 'bboxes'."
            assert 'bboxes' in annotations, "'load_annotations' should return a list of dictionaries that contain 'labels' and 'bboxes'."

        return annotations_group

    def filter_annotations(self, image_group, annotations_group, group):
        """ Filter annotations by removing those that are outside of the image bounds or whose width/height < 0.
        """
        for index, (image, annotations) in enumerate(zip(image_group, annotations_group)):
            invalid_indices = np.where((annotations['bboxes'][:, 2] <= annotations['bboxes'][:, 0]) | (annotations['bboxes'][:, 3] <= annotations['bboxes'][:, 1]) | (annotations['bboxes'][:, 0] < 0) | (annotations['bboxes'][:, 1] < 0) | (annotations['bboxes'][:, 2] > image.shape[1]) | (annotations['bboxes'][:, 3] > image.shape[0]))[0]
            if len(invalid_indices):
                for k in annotations_group[index].keys():
                    annotations_group[index][k] = np.delete((annotations[k]), invalid_indices, axis=0)

        return (
         image_group, annotations_group)

    def load_image_group(self, group):
        """ Load images for all images in a group.
        """
        return [self.load_image(image_index) for image_index in group]

    def random_visual_effect_group_entry(self, image, annotations):
        """ Randomly transforms image and annotation.
        """
        visual_effect = next(self.visual_effect_generator)
        image = visual_effect(image)
        return (image, annotations)

    def random_visual_effect_group(self, image_group, annotations_group):
        """ Randomly apply visual effect on each image.
        """
        assert len(image_group) == len(annotations_group)
        if self.visual_effect_generator is None:
            return (image_group, annotations_group)
        for index in range(len(image_group)):
            image_group[index], annotations_group[index] = self.random_visual_effect_group_entry(image_group[index], annotations_group[index])

        return (
         image_group, annotations_group)

    def random_transform_group_entry(self, image, annotations, transform=None):
        """ Randomly transforms image and annotation.
        """
        if transform is not None or self.transform_generator:
            if transform is None:
                transform = adjust_transform_for_image(next(self.transform_generator), image, self.transform_parameters.relative_translation)
            image = apply_transform(transform, image, self.transform_parameters)
            annotations['bboxes'] = annotations['bboxes'].copy()
            for index in range(annotations['bboxes'].shape[0]):
                annotations['bboxes'][index, :] = transform_aabb(transform, annotations['bboxes'][index, :])

        return (
         image, annotations)

    def random_transform_group(self, image_group, annotations_group):
        """ Randomly transforms each image and its annotations.
        """
        assert len(image_group) == len(annotations_group)
        for index in range(len(image_group)):
            image_group[index], annotations_group[index] = self.random_transform_group_entry(image_group[index], annotations_group[index])

        return (image_group, annotations_group)

    def resize_image(self, image):
        """ Resize an image using image_min_side and image_max_side.
        """
        if self.no_resize:
            return (
             image, 1)
        return resize_image(image, min_side=(self.image_min_side), max_side=(self.image_max_side))

    def preprocess_group_entry(self, image, annotations):
        """ Preprocess image and its annotations.
        """
        image = self.preprocess_image(image)
        image, image_scale = self.resize_image(image)
        annotations['bboxes'] *= image_scale
        image = K.cast_to_floatx(image)
        return (
         image, annotations)

    def preprocess_group(self, image_group, annotations_group):
        """ Preprocess each image and its annotations in its group.
        """
        assert len(image_group) == len(annotations_group)
        for index in range(len(image_group)):
            image_group[index], annotations_group[index] = self.preprocess_group_entry(image_group[index], annotations_group[index])

        return (image_group, annotations_group)

    def group_images(self):
        """ Order the images according to self.order and makes groups of self.batch_size.
        """
        order = list(range(self.size()))
        if self.group_method == 'random':
            random.shuffle(order)
        else:
            if self.group_method == 'ratio':
                order.sort(key=(lambda x: self.image_aspect_ratio(x)))
        self.groups = [[order[(x % len(order))] for x in range(i, i + self.batch_size)] for i in range(0, len(order), self.batch_size)]

    def compute_inputs(self, image_group):
        """ Compute inputs for the network using an image_group.
        """
        max_shape = tuple((max((image.shape[x] for image in image_group)) for x in range(3)))
        image_batch = np.zeros(((self.batch_size,) + max_shape), dtype=(K.floatx()))
        for image_index, image in enumerate(image_group):
            image_batch[image_index, :image.shape[0], :image.shape[1], :image.shape[2]] = image

        if K.image_data_format() == 'channels_first':
            image_batch = image_batch.transpose((0, 3, 1, 2))
        return image_batch

    def generate_anchors(self, image_shape):
        anchor_params = None
        if self.config:
            if 'anchor_parameters' in self.config:
                anchor_params = parse_anchor_parameters(self.config)
        return anchors_for_shape(image_shape, anchor_params=anchor_params, shapes_callback=(self.compute_shapes))

    def compute_targets(self, image_group, annotations_group):
        """ Compute target outputs for the network using images and their annotations.
        """
        max_shape = tuple((max((image.shape[x] for image in image_group)) for x in range(3)))
        anchors = self.generate_anchors(max_shape)
        batches = self.compute_anchor_targets(anchors, image_group, annotations_group, self.num_classes())
        return list(batches)

    def compute_input_output(self, group):
        """ Compute inputs and target outputs for the network.
        """
        image_group = self.load_image_group(group)
        annotations_group = self.load_annotations_group(group)
        image_group, annotations_group = self.filter_annotations(image_group, annotations_group, group)
        image_group, annotations_group = self.random_visual_effect_group(image_group, annotations_group)
        image_group, annotations_group = self.random_transform_group(image_group, annotations_group)
        image_group, annotations_group = self.preprocess_group(image_group, annotations_group)
        inputs = self.compute_inputs(image_group)
        targets = self.compute_targets(image_group, annotations_group)
        return (
         inputs, targets)

    def __len__(self):
        """
        Number of batches for generator.
        """
        return len(self.groups)

    def __getitem__(self, index):
        group = self.groups[index]
        inputs, targets = self.compute_input_output(group)
        return (
         inputs, targets)


class CSVGenerator(Generator):
    __doc__ = ' Generate data for a custom CSV dataset.\n\n    See https://github.com/fizyr/keras-retinanet#csv-datasets for more information.\n    '

    def __init__(self, csv_data_file, csv_class_file, base_dir=None, **kwargs):
        """ Initialize a CSV data generator.

        Args
            csv_data_file: Path to the CSV annotations file.
            csv_class_file: Path to the CSV classes file.
            base_dir: Directory w.r.t. where the files are to be searched (defaults to the directory containing the csv_data_file).
        """
        self.image_names = []
        self.image_data = {}
        self.base_dir = base_dir
        self.csv_data_file = csv_data_file
        if self.base_dir is None:
            self.base_dir = os.path.dirname(csv_data_file)
        try:
            with self._open_for_csv(csv_class_file) as (file):
                self.classes = self._read_classes(csv.reader(file, delimiter=','))
        except ValueError as e:
            try:
                raise_from(ValueError('invalid CSV class file: {}: {}'.format(csv_class_file, e)), None)
            finally:
                e = None
                del e

        self.labels = {}
        for key, value in self.classes.items():
            self.labels[value] = key

        try:
            with self._open_for_csv(csv_data_file) as (file):
                self.image_data = self._read_annotations(csv.reader(file, delimiter=','), self.classes)
        except ValueError as e:
            try:
                raise_from(ValueError('invalid CSV annotations file: {}: {}'.format(csv_data_file, e)), None)
            finally:
                e = None
                del e

        self.image_names = list(self.image_data.keys())
        (super(CSVGenerator, self).__init__)(**kwargs)

    def size(self):
        """ Size of the dataset.
        """
        return len(self.image_names)

    def num_classes(self):
        """ Number of classes in the dataset.
        """
        return max(self.classes.values()) + 1

    def has_label(self, label):
        """ Return True if label is a known label.
        """
        return label in self.labels

    def has_name(self, name):
        """ Returns True if name is a known class.
        """
        return name in self.classes

    def name_to_label(self, name):
        """ Map name to label.
        """
        return self.classes[name]

    def label_to_name(self, label):
        """ Map label to name.
        """
        return self.labels[label]

    def image_path(self, image_index):
        """ Returns the image path for image_index.
        """
        return os.path.join(self.base_dir, self.image_names[image_index])

    def image_aspect_ratio(self, image_index):
        """ Compute the aspect ratio for an image with image_index.
        """
        image = Image.open(self.image_path(image_index))
        return float(image.width) / float(image.height)

    def load_image(self, image_index):
        """ Load an image at the image_index.
        """
        return read_image_bgr(self.image_path(image_index))

    def load_annotations(self, image_index):
        """ Load annotations for an image_index.
        """
        path = self.image_names[image_index]
        annotations = {'labels':np.empty((0, )),  'bboxes':np.empty((0, 4))}
        for idx, annot in enumerate(self.image_data[path]):
            annotations['labels'] = np.concatenate((annotations['labels'], [self.name_to_label(annot['class'])]))
            annotations['bboxes'] = np.concatenate((annotations['bboxes'],
             [
              [
               float(annot['x1']),
               float(annot['y1']),
               float(annot['x2']),
               float(annot['y2'])]]))

        return annotations

    @staticmethod
    def _open_for_csv(path):
        """ Open a file with flags suitable for csv.reader.

        This is different for python2 it means with mode 'rb',
        for python3 this means 'r' with "universal newlines".
        """
        if sys.version_info[0] < 3:
            return open(path, 'rb')
        return open(path, 'r', newline='')

    def _read_annotations(self, csv_reader, classes):
        result = OrderedDict()
        for line, row in enumerate(csv_reader):
            line += 1
            try:
                img_file, x1, y1, x2, y2, class_name = row[:6]
            except ValueError:
                raise_from(ValueError("line {}: format should be 'img_file,x1,y1,x2,y2,class_name' or 'img_file,,,,,'".format(line)), None)

            if img_file not in result:
                result[img_file] = []
            if (x1, y1, x2, y2, class_name) == ('', '', '', '', ''):
                continue
            x1 = self._parse(x1, int, 'line {}: malformed x1: {{}}'.format(line))
            y1 = self._parse(y1, int, 'line {}: malformed y1: {{}}'.format(line))
            x2 = self._parse(x2, int, 'line {}: malformed x2: {{}}'.format(line))
            y2 = self._parse(y2, int, 'line {}: malformed y2: {{}}'.format(line))
            if x2 <= x1:
                raise ValueError('line {}: x2 ({}) must be higher than x1 ({})'.format(line, x2, x1))
            if y2 <= y1:
                raise ValueError('line {}: y2 ({}) must be higher than y1 ({})'.format(line, y2, y1))
            if class_name not in classes:
                raise ValueError("line {}: unknown class name: '{}' (classes: {})".format(line, class_name, classes))
            result[img_file].append({'x1':x1,  'x2':x2,  'y1':y1,  'y2':y2,  'class':class_name})

        return result

    @staticmethod
    def _parse(value, function, fmt):
        """
        Parse a string into a value, and format a nice ValueError if it fails.

        Returns `function(value)`.
        Any `ValueError` raised is catched and a new `ValueError` is raised
        with message `fmt.format(e)`, where `e` is the caught `ValueError`.
        """
        try:
            return function(value)
        except ValueError as e:
            try:
                raise_from(ValueError(fmt.format(e)), None)
            finally:
                e = None
                del e

    def _read_classes(self, csv_reader):
        """ Parse the classes file given by csv_reader.
        """
        result = OrderedDict()
        for line, row in enumerate(csv_reader):
            line += 1
            try:
                class_name, class_id = row
            except ValueError:
                raise_from(ValueError("line {}: format should be 'class_name,class_id'".format(line)), None)

            class_id = self._parse(class_id, int, 'line {}: malformed class ID: {{}}'.format(line))
            if class_name in result:
                raise ValueError("line {}: duplicate class name: '{}'".format(line, class_name))
            result[class_name] = class_id

        return result


class TextGenerator(Generator):
    __doc__ = ' Generate data for a custom CSV dataset.\n\n    See https://github.com/fizyr/keras-retinanet#csv-datasets for more information.\n    '

    def __init__(self, csv_data_file, csv_class_file, base_dir=None, **kwargs):
        """ Initialize a CSV data generator.

        Args
            csv_data_file: Path to the CSV annotations file.
            csv_class_file: Path to the CSV classes file.
            base_dir: Directory w.r.t. where the files are to be searched (defaults to the directory containing the csv_data_file).
        """
        self.class_names = []
        self.image_names = []
        self.image_data = {}
        self.base_dir = base_dir
        self.csv_data_file = csv_data_file
        self.csv_class_file = csv_class_file
        if self.base_dir is None:
            self.base_dir = os.path.dirname(csv_data_file)
        try:
            self.class_names = read_lines(csv_class_file)
            self.classes = {}
            for i, name in enumerate(self.class_names):
                self.classes[name] = i

        except ValueError as e:
            try:
                raise_from(ValueError('invalid CSV class file: {}: {}'.format(csv_class_file, e)), None)
            finally:
                e = None
                del e

        self.labels = {}
        for key, value in self.classes.items():
            self.labels[value] = key

        try:
            self.image_data = self._read_annotations()
        except ValueError as e:
            try:
                raise_from(ValueError('invalid CSV annotations file: {}: {}'.format(csv_data_file, e)), None)
            finally:
                e = None
                del e

        self.image_names = list(self.image_data.keys())
        (super(TextGenerator, self).__init__)(**kwargs)

    def size(self):
        """ Size of the dataset.
        """
        return len(self.image_names)

    def num_classes(self):
        """ Number of classes in the dataset.
        """
        return max(self.classes.values()) + 1

    def has_label(self, label):
        """ Return True if label is a known label.
        """
        return label in self.labels

    def has_name(self, name):
        """ Returns True if name is a known class.
        """
        return name in self.classes

    def name_to_label(self, name):
        """ Map name to label.
        """
        return self.classes[name]

    def label_to_name(self, label):
        """ Map label to name.
        """
        return self.labels[label]

    def image_path(self, image_index):
        """ Returns the image path for image_index.
        """
        return os.path.join(self.base_dir, self.image_names[image_index])

    def image_aspect_ratio(self, image_index):
        """ Compute the aspect ratio for an image with image_index.
        """
        image = Image.open(self.image_path(image_index))
        return float(image.width) / float(image.height)

    def load_image(self, image_index):
        """ Load an image at the image_index.
        """
        return read_image_bgr(self.image_path(image_index))

    def load_annotations(self, image_index):
        """ Load annotations for an image_index.
        """
        path = self.image_names[image_index]
        annotations = {'labels':np.empty((0, )),  'bboxes':np.empty((0, 4))}
        for idx, annot in enumerate(self.image_data[path]):
            annotations['labels'] = np.concatenate((annotations['labels'], [self.name_to_label(annot['class'])]))
            annotations['bboxes'] = np.concatenate((annotations['bboxes'],
             [
              [
               float(annot['x1']),
               float(annot['y1']),
               float(annot['x2']),
               float(annot['y2'])]]))

        return annotations

    @staticmethod
    def _open_for_csv(path):
        """ Open a file with flags suitable for csv.reader.

        This is different for python2 it means with mode 'rb',
        for python3 this means 'r' with "universal newlines".
        """
        if sys.version_info[0] < 3:
            return open(path, 'rb')
        return open(path, 'r', newline='')

    def _read_annotations(self):
        result = OrderedDict()
        for annotation in read_lines(self.csv_data_file):
            rows = annotation.split(' ')
            img_file = rows[0]
            if img_file not in result:
                result[img_file] = []
            for box in rows[1:]:
                if len(box) < 5:
                    continue
                x1, y1, x2, y2, class_name = box.split(',')
                x1, y1, x2, y2 = (int(x1), int(y1), int(x2), int(y2))
                class_name = self.class_names[int(class_name)]
                result[img_file].append({'x1':x1,  'x2':x2,  'y1':y1,  'y2':y2,  'class':class_name})

        print('read annotations done')
        return result

    @staticmethod
    def _parse(value, function, fmt):
        try:
            return function(value)
        except ValueError as e:
            try:
                raise_from(ValueError(fmt.format(e)), None)
            finally:
                e = None
                del e


class KittiGenerator(Generator):
    kitti_classes = {'Car':0, 
     'Van':1, 
     'Truck':2, 
     'Pedestrian':3, 
     'Person_sitting':4, 
     'Cyclist':5, 
     'Tram':6, 
     'Misc':7, 
     'DontCare':7}

    def __init__(self, base_dir, subset='train', **kwargs):
        """ Initialize a KITTI data generator.

        Args
            base_dir: Directory w.r.t. where the files are to be searched (defaults to the directory containing the csv_data_file).
            subset: The subset to generate data for (defaults to 'train').
        """
        self.base_dir = base_dir
        label_dir = os.path.join(self.base_dir, subset, 'labels')
        image_dir = os.path.join(self.base_dir, subset, 'images')
        self.labels = {}
        self.classes = self.kitti_classes
        for name, label in self.classes.items():
            self.labels[label] = name

        self.image_data = dict()
        self.images = []
        for i, fn in enumerate(os.listdir(label_dir)):
            label_fp = os.path.join(label_dir, fn)
            image_fp = os.path.join(image_dir, fn.replace('.txt', '.png'))
            self.images.append(image_fp)
            fieldnames = [
             'type', 'truncated', 'occluded', 'alpha', 'left', 'top', 'right', 'bottom', 'dh', 'dw', 'dl',
             'lx', 'ly', 'lz', 'ry']
            with open(label_fp, 'r') as (csv_file):
                reader = csv.DictReader(csv_file, delimiter=' ', fieldnames=fieldnames)
                boxes = []
                for line, row in enumerate(reader):
                    label = row['type']
                    cls_id = self.kitti_classes[label]
                    annotation = {'cls_id':cls_id, 
                     'x1':row['left'],  'x2':row['right'],  'y2':row['bottom'],  'y1':row['top']}
                    boxes.append(annotation)

                self.image_data[i] = boxes

        (super(KittiGenerator, self).__init__)(**kwargs)

    def size(self):
        """ Size of the dataset.
        """
        return len(self.images)

    def num_classes(self):
        """ Number of classes in the dataset.
        """
        return max(self.classes.values()) + 1

    def has_label(self, label):
        """ Return True if label is a known label.
        """
        return label in self.labels

    def has_name(self, name):
        """ Returns True if name is a known class.
        """
        return name in self.classes

    def name_to_label(self, name):
        """ Map name to label.
        """
        raise NotImplementedError()

    def label_to_name(self, label):
        """ Map label to name.
        """
        return self.labels[label]

    def image_aspect_ratio(self, image_index):
        """ Compute the aspect ratio for an image with image_index.
        """
        image = Image.open(self.images[image_index])
        return float(image.width) / float(image.height)

    def image_path(self, image_index):
        """ Get the path to an image.
        """
        return self.images[image_index]

    def load_image(self, image_index):
        """ Load an image at the image_index.
        """
        return read_image_bgr(self.image_path(image_index))

    def load_annotations(self, image_index):
        """ Load annotations for an image_index.
        """
        image_data = self.image_data[image_index]
        annotations = {'labels':np.empty((len(image_data),)),  'bboxes':np.empty((len(image_data), 4))}
        for idx, ann in enumerate(image_data):
            annotations['bboxes'][(idx, 0)] = float(ann['x1'])
            annotations['bboxes'][(idx, 1)] = float(ann['y1'])
            annotations['bboxes'][(idx, 2)] = float(ann['x2'])
            annotations['bboxes'][(idx, 3)] = float(ann['y2'])
            annotations['labels'][idx] = int(ann['cls_id'])

        return annotations
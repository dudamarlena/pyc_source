# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_tensor/object_detector/yolo2voc.py
# Compiled at: 2019-08-16 06:33:35
# Size of source mod 2**32: 4198 bytes
import os, xml.etree.cElementTree as ET, cv2
ANNOTATIONS_DIR_PREFIX = 'labels'
DESTINATION_DIR = 'results'
CLASS_MAPPING = {'0': 'pneumonia'}

def create_root(file_prefix, width, height):
    """[summary]
    
    Arguments:
        file_prefix {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    root = ET.Element('annotations')
    ET.SubElement(root, 'filename').text = '{}.jpg'.format(file_prefix)
    ET.SubElement(root, 'folder').text = 'images'
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = '3'
    return root


def create_object_annotation(root, voc_labels):
    """[summary]
    
    Arguments:
        root {[type]} -- [description]
        voc_labels {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    for voc_label in voc_labels:
        obj = ET.SubElement(root, 'object')
        ET.SubElement(obj, 'name').text = voc_label[0]
        ET.SubElement(obj, 'pose').text = 'Unspecified'
        ET.SubElement(obj, 'truncated').text = str(0)
        ET.SubElement(obj, 'difficult').text = str(0)
        bbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(voc_label[1])
        ET.SubElement(bbox, 'ymin').text = str(voc_label[2])
        ET.SubElement(bbox, 'xmax').text = str(voc_label[3])
        ET.SubElement(bbox, 'ymax').text = str(voc_label[4])

    return root


def create_file(file_prefix, width, height, voc_labels):
    """[summary]
    
    Arguments:
        file_prefix {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
        voc_labels {[type]} -- [description]
    """
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write('{}/{}.xml'.format(DESTINATION_DIR, file_prefix))


def read_file(file_path):
    """[summary]
    
    Arguments:
        file_path {[type]} -- [description]
    """
    file_prefix = file_path.split('.txt')[0]
    image_file_name = 'images/' + '{}.jpg'.format(file_prefix)
    img = cv2.imread(image_file_name)
    h, w, c = img.shape
    with open('labels/' + file_path, 'r') as (file):
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - bbox_width / 2)
            voc.append(center_y - bbox_height / 2)
            voc.append(center_x + bbox_width / 2)
            voc.append(center_y + bbox_height / 2)
            voc_labels.append(voc)

        create_file(file_prefix, w, h, voc_labels)
    print('Processing complete for file: {}'.format(file_path))


def start():
    """[summary]
    """
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print('Skipping file: {}'.format(filename))


if __name__ == '__main__':
    start()
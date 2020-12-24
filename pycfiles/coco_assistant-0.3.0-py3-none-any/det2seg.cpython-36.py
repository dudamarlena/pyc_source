# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ashwin/Desktop/Projects/COCO-Assistant/coco_assistant/utils/det2seg.py
# Compiled at: 2019-11-27 15:20:28
# Size of source mod 2**32: 2524 bytes
import os, numpy as np
from PIL import Image, ImageDraw
from pycocotools.coco import COCO
from tqdm import tqdm

def det2seg(cann, output_dir):
    """
    Function for converting segmentation polygons in MS-COCO
    object detection dataset to segmentation masks. The seg-
    mentation masks are stored with a colour palette that's
    randomly assigned based on class. Change the seed if you
    want to change colours.

    :param cann: COCO annotation object
    :param output_dir: Directory to store segmentation masks.
    """
    if os.path.isdir(output_dir) is False:
        os.makedirs(output_dir, exist_ok=True)
    imids = cann.getImgIds()
    cats = cann.loadCats(cann.getCatIds())
    cat_colours = {0: (0, 0, 0)}
    np.random.seed(121)
    for c in cats:
        cat_colours[c['id']] = (
         np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))

    colour_map = np.array(list(cat_colours.values()))
    if colour_map.shape != (len(cats) + 1, 3):
        raise AssertionError('Incorrect shape of color map array')
    for imid in tqdm(imids):
        img = cann.loadImgs(imid)
        if len(img) > 1:
            raise AssertionError('Multiple images with same id')
        h, w = img[0]['height'], img[0]['width']
        name = img[0]['file_name']
        if name[-4:] != '.png':
            name = name[:-4] + '.png'
        im = np.zeros((h, w), dtype=(np.uint8))
        annids = cann.getAnnIds(imgIds=[imid])
        if not annids:
            res = Image.fromarray(im)
            res.save(os.path.join(output_dir, '{}'.format(name)))
        else:
            anns = cann.loadAnns(annids)
            for ann in anns:
                poly = ann['segmentation'][0]
                cat = ann['category_id']
                img = Image.new('L', (w, h))
                if len(poly) >= 6:
                    ImageDraw.Draw(img).polygon(poly, fill=cat)
                else:
                    continue
                mask = np.array(img)
                im = np.maximum(im, mask)

            res = Image.fromarray(im)
            res.putpalette(colour_map.astype(np.uint8))
            res.save(os.path.join(output_dir, '{}'.format(name)))


if __name__ == '__main__':
    ann = COCO('/home/ashwin/Desktop/Projects/COCO-Assistant/data/annotations/tiny2.json')
    output_dir = '/home/ashwin/Desktop/Projects/COCO-Assistant/data/annotations/seg'
    det2seg(ann, output_dir)
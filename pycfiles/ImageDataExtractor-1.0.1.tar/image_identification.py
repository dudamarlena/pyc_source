# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: imagedataextractor/image_identification.py
# Compiled at: 2019-05-16 11:15:11
"""
Identify TEM images from scientific articles using chemdataextractor

@author : Ed Beard

"""
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from chemdataextractor import Document
import urllib, multiprocessing as mp, os, csv, io, sys, logging
logging.basicConfig()
log = logging.getLogger(__name__)

class TEMImageExtractor:

    def __init__(self, input, output=b'', typ=b'tem'):
        self.input = input
        self.output = output
        self.img_csv_path = str(os.path.join(self.output, os.path.basename(self.output) + b'_raw.csv'))
        self.docs = []
        self.paths = []
        self.imgs = []
        self.urls = []
        self.img_type = typ

    def get_img_paths(self):
        """ Get paths to all images """
        docs = os.listdir(self.input)
        self.docs = [ (doc, os.path.join(self.input, doc)) for doc in docs ]
        if not os.path.exists(os.path.join(self.output, b'raw_images')):
            os.makedirs(os.path.join(self.output, b'raw_images'))

    def get_img(self, doc):
        """Get images from doc using chemdataextractor"""
        tem_images = []
        cde_doc = Document.from_file(open(doc[1], b'rb'))
        print(b'This article is : %s' % doc[0])
        imgs = cde_doc.figures
        del cde_doc
        for img in imgs:
            detected = False
            records = img.records
            caption = img.caption
            for record in records:
                if detected is True:
                    break
                rec = record.serialize()
                if [self.img_type] in rec.values():
                    detected = True
                    print(b'%s instance found!' % self.img_type)
                    tem_images.append((doc[0], img.id, img.url, caption.text.replace(b'\n', b' ')))

        if len(tem_images) != 0:
            return tem_images
        else:
            return
            return

    def download_image(self, url, file, id):
        """ Download all TEM images"""
        imgs_dir = os.path.join(self.output, b'raw_images')
        if len(os.listdir(imgs_dir)) <= 999999999:
            img_format = url[-3:]
            print(url, img_format)
            filename = file[:-5] + b'_' + id + b'.' + img_format
            path = os.path.join(imgs_dir, filename)
            print(b'Downloading %s...' % filename)
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path)
            else:
                print(b'File exists! Going to next image')
        else:
            sys.exit()

    def save_img_data_to_file(self):
        """ Saves list of tem images"""
        imgf = open(self.img_csv_path, b'w')
        output_csvwriter = csv.writer(imgf)
        output_csvwriter.writerow([b'article', b'fig id', b'url', b'caption'])
        for row in self.imgs:
            if row[2] != b'':
                output_csvwriter.writerow(row)

    def get_all_tem_imgs(self, parallel=True):
        """ Get all TEM images """
        self.get_img_paths()
        if os.path.isfile(self.img_csv_path):
            with io.open(self.img_csv_path, b'r') as (imgf):
                img_csvreader = csv.reader(imgf)
                next(img_csvreader)
                self.imgs = list(img_csvreader)
        else:
            if parallel:
                pool = mp.Pool(processes=mp.cpu_count())
                tem_images = pool.map(self.get_img, self.docs)
            else:
                tem_images = []
                for doc in self.docs:
                    try:
                        imgs = self.get_img(doc)
                        if imgs is not None:
                            tem_images.append(imgs)
                    except Exception as e:
                        print(e)

                self.imgs = [ img for doc in tem_images if doc is not None for img in doc ]
                self.save_img_data_to_file()
                print(b'%s image info saved to file' % self.img_type)
            for file, id, url, caption in self.imgs:
                self.download_image(url, file, id)

        return

    def get_tem_imgs(self):
        """ Get the TEM images for a single Document"""
        if not os.path.isfile(self.input):
            raise Exception(b'Input should be a single document for this method')
        if not os.path.exists(os.path.join(self.output, b'raw_images')):
            os.makedirs(os.path.join(self.output, b'raw_images'))
        if os.path.isfile(self.img_csv_path):
            with io.open(self.img_csv_path, b'r') as (imgf):
                img_csvreader = csv.reader(imgf)
                next(img_csvreader)
                self.imgs = list(img_csvreader)
        else:
            try:
                doc = (
                 self.input.split(b'/')[(-1)], self.input)
                self.imgs = self.get_img(doc)
            except Exception as e:
                print(e)

            self.save_img_data_to_file()
            print(b'%s image info saved to file' % self.img_type)
            for file, id, url, caption in self.imgs:
                self.download_image(url, file, id)
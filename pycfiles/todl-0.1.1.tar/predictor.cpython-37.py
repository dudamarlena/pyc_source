# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/todl/predictor.py
# Compiled at: 2020-04-05 21:22:32
# Size of source mod 2**32: 8997 bytes
import os, io, base64, hashlib, logging, logging.config, boto3, tempfile, requests, numpy as np
from urllib.parse import urlparse
from PIL import Image
from PIL import ImageFile
from todl.model import Model
ImageFile.LOAD_TRUNCATED_IMAGES = True
PREFIX_PATH = '/opt/ml/'
CACHE_PATH = os.path.join(PREFIX_PATH, 'cache')
MODEL_PATH = os.path.join(PREFIX_PATH, 'model')
PRETRAINED_MODEL_PATH = os.path.join(PREFIX_PATH, 'pretrained')
LABEL_PATH = os.path.join(MODEL_PATH, 'label_map.pbtxt')
DEFAULT_MODEL = 'faster_rcnn_resnet101_coco'
PRETRAINED_MODELS = [
 'ssd_mobilenet_v1_coco.pb',
 'ssd_mobilenet_v2_coco.pb',
 'faster_rcnn_resnet101_coco.pb',
 'rfcn_resnet101_coco.pb',
 'faster_rcnn_inception_v2_coco.pb',
 'ssd_inception_v2_coco.pb',
 'faster_rcnn_resnet50_coco.pb',
 'faster_rcnn_resnet50_lowproposals_coco.pb',
 'faster_rcnn_resnet101_lowproposals_coco.pb',
 'faster_rcnn_inception_resnet_v2_atrous_coco.pb',
 'faster_rcnn_inception_resnet_v2_atrous_lowproposals_coco.pb',
 'faster_rcnn_nas_coco.pb',
 'faster_rcnn_nas_lowproposals_coco.pb']

class Configuration:

    def __init__(self, data: dict):
        self.file = data.get('file', None)
        self.image = data.get('image', None)
        self.stride = data.get('stride', 1)
        self.model = data.get('model', DEFAULT_MODEL)
        self.cache = data.get('cache', False)
        self.cache_id = data.get('cache_id', None)
        self.aws_region = data.get('aws_region', None)
        self.aws_access_key = data.get('aws_access_key', None)
        self.aws_secret_access_key = data.get('aws_secret_access_key', None)


class Cache:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.enabled = configuration.cache
        self.path = CACHE_PATH

    def get(self, key: str):
        if self.enabled:
            entry = os.path.join(self.path, f"{key}.npz")
            if os.path.exists(entry):
                data = np.load(entry, allow_pickle=True)
                return data['data']

    def put(self, key: str, value):
        if self.enabled:
            np.savez_compressed((os.path.join(self.path, f"{key}.npz")), data=value)


class Processor:
    models = {}

    @staticmethod
    def factory(configuration: Configuration):
        if (configuration.image is not None or configuration.file) is not None:
            if configuration.file.lower().endswith(('.jpg', '.png', '.jpeg')):
                return ImageProcessor(configuration, Cache(configuration))

    @staticmethod
    def get_model(frozen_graph=DEFAULT_MODEL):
        if not frozen_graph.lower().endswith('.pb'):
            frozen_graph += '.pb'
        model_path = os.path.join(PRETRAINED_MODEL_PATH, frozen_graph) if frozen_graph in PRETRAINED_MODELS else os.path.join(MODEL_PATH, frozen_graph)
        if frozen_graph not in Processor.models:
            Processor.models[frozen_graph] = Model(LABEL_PATH, model_path)
        return Processor.models[frozen_graph]

    def __init__(self, configuration: Configuration, cache: Cache):
        self.configuration = configuration
        self.cache = cache

    def inference(self):
        pass

    def predict(self, image):
        return Processor.get_model(self.configuration.model).inference(image)


class ImageProcessor(Processor):

    def __init__(self, configuration, cache):
        super(ImageProcessor, self).__init__(configuration, cache)

    def inference(self):
        logging.info('Running inference on image...')
        inference_cache_key = self._ImageProcessor__get_key(self._ImageProcessor__get_source(), 'inference')
        predictions = None
        value = self.cache.get(inference_cache_key)
        if value is not None:
            predictions = value.tolist()
            logging.debug('Inference from image found in cache')
        if predictions is None:
            logging.debug('Inference from image not found in cache')
            image = self._ImageProcessor__get_image()
            inference = self.predict(image)
            predictions = {'predictions': []}
            for index, label in enumerate(inference['detection_classes']):
                box = inference['detection_boxes'][index].astype(float)
                score = float(inference['detection_scores'][index])
                ymin = box[0]
                xmin = box[1]
                ymax = box[2]
                xmax = box[3]
                prediction = [
                 float(label - 1),
                 score,
                 xmin,
                 ymin,
                 xmax,
                 ymax]
                predictions['predictions'].append(prediction)

            self.cache.put(inference_cache_key, np.array(predictions))
        return predictions

    def __get_source(self):
        if self.configuration.image is not None:
            return base64.b64decode(self.configuration.image)
        return self.configuration.file

    def __get_image(self):
        source_cache_key = self._ImageProcessor__get_key(self._ImageProcessor__get_source(), 'source')
        image = self.cache.get(source_cache_key)
        if image is None:
            logging.debug('Image not found in cache')
            try:
                if self.configuration.image is not None:
                    image = self._ImageProcessor__get_image_from_base64_string(self._ImageProcessor__get_source())
                else:
                    fragments = urlparse((self._ImageProcessor__get_source()), allow_fragments=False)
                    if fragments.scheme == 's3':
                        image = self._ImageProcessor__get_image_from_s3(self._ImageProcessor__get_source(), fragments)
                    else:
                        if fragments.scheme == 'http' or fragments.scheme == 'https':
                            image = self._ImageProcessor__get_image_from_url(self._ImageProcessor__get_source())
                        else:
                            image = self._ImageProcessor__get_image_from_file(self._ImageProcessor__get_source(), fragments)
                self.cache.put(source_cache_key, image)
            except Exception as e:
                try:
                    logging.error('There was an error handling image', e)
                finally:
                    e = None
                    del e

        else:
            logging.debug('Image found in cache')
        return image

    def __get_image_from_base64_string(self, source) -> np.array:
        logging.info('Creating image from base64 string...')
        image = Image.open(io.BytesIO(source))
        return self._ImageProcessor__numpy(image)

    def __get_image_from_s3(self, file, fragments) -> np.array:
        logging.info(f"Downloading image from S3. Filename {file}...")
        s3 = boto3.client('s3', region_name=(self.configuration.aws_region), aws_access_key_id=(self.configuration.aws_access_key), aws_secret_access_key=(self.configuration.aws_secret_access_key)) if self.configuration.aws_access_key else boto3.client('s3')
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'wb') as (f):
            s3.download_fileobj(fragments.netloc, fragments.path[1:], f)
            return self._ImageProcessor__numpy(Image.open(tmp.name))

    def __get_image_from_url(self, file) -> np.array:
        logging.info(f"Downloading image from URL. Filename {file}...")
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'wb') as (f):
            response = requests.get(file, stream=True)
            if not response.ok:
                raise RuntimeError(f"There was an error downloading image from URL. Filename {file}. Response {response}.")
            for block in response.iter_content(1024):
                if not block:
                    break
                f.write(block)

            return self._ImageProcessor__numpy(Image.open(tmp.name))

    def __get_image_from_file(self, file, fragments) -> np.array:
        logging.info(f"Downloading image from file. Filename {file}...")
        if fragments.scheme == 'file':
            return self._ImageProcessor__numpy(Image.open(fragments.path))
        return self._ImageProcessor__numpy(Image.open(file))

    def __get_key(self, file: str, suffix: str):
        tmp = hashlib.md5(str(file).encode('utf8'))
        tmp.update(str(suffix).encode('utf8'))
        return tmp.hexdigest()

    def __numpy(self, image):
        width, height = image.size
        return np.array(image.getdata()).reshape((height, width, 3)).astype(np.uint8)
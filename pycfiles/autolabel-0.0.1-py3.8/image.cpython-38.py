# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autolabel/image.py
# Compiled at: 2020-04-03 05:01:17
# Size of source mod 2**32: 2153 bytes
import logging
from pathlib import Path
from typing import List, Tuple
from PIL import ImageFile
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
DEFAULT_IMAGE_SIZE = (224, 224)

def get_image(image_path: List[Path]) -> Image:
    """
    Read image at given path into PIL RGB format
    :param image_path:
    :return: PIL Image
    """
    im = Image.open(str(image_path)).convert('RGB')
    return im


class ImageListDataset(Dataset):

    def __init__(self, image_paths: List[Path], image_size: Tuple[int]=DEFAULT_IMAGE_SIZE):
        """
        :param image_paths: List of image paths
        :param image_size: Image size
        """
        self.transform = transforms.Compose([
         transforms.Resize(image_size),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        self._image_paths = image_paths
        self._image_size = image_size

    def __len__(self):
        return sum((p is not None for p in self._image_paths))

    def __getitem__(self, item: str) -> Image:
        """
        Get image by given path
        :param item: image path
        :return: Image
        """
        path = self._image_paths[item]
        try:
            im = get_image(path)
        except Exception as e:
            try:
                logging.error(f"Could not load {path}: {e}")
                im = Image.new('RGB', self._image_size)
            finally:
                e = None
                del e

        else:
            return self.transform(im)

    @property
    def paths(self):
        return self._image_paths

    def loader(self, batch_size: int=None) -> DataLoader:
        """
        torch dataset loader for this dataset
        :param batch_size: Used batch size
        :return: dataset loader
        """
        if batch_size is None:
            batch_size = len(self)
        return DataLoader(self, batch_size=batch_size)
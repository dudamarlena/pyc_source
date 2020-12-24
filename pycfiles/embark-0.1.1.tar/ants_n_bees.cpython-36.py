# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/naresh/Projects/embark/embark/tensorflow_classifier/utils/datasets/ants_n_bees.py
# Compiled at: 2020-02-03 14:39:12
# Size of source mod 2**32: 3587 bytes
import os, sys, zipfile, pathlib, requests, numpy as np, pandas as pd, tensorflow as tf, matplotlib.pyplot as plt
from PIL import Image

class AntsNBees:

    def __init__(self, dataset_path, phase, transforms):
        self.dataset_path = pathlib.Path(dataset_path)
        self.req_dataset_path = self.dataset_path / 'hymenoptera_data/{}'.format(phase)
        self.phase = phase
        if not self.dataset_path.exists():
            self.download()
        self.labels = pd.read_csv(self.req_dataset_path / '{}.csv'.format(self.phase))
        self.transforms = transforms

    def get_dataset(self):
        files_ds = tf.data.Dataset.list_files(str(self.req_dataset_path / 'images/*'))
        files_ds = files_ds.map(self._read_images_n_labels)
        return files_ds

    def _read_images_n_labels(self, file_path):
        image, label = tf.py_function(self._py_read_images_n_labels, [file_path], [tf.float32, tf.int32])
        image = tf.image.convert_image_dtype(image, tf.float32)
        image.set_shape((self.transforms['resize'][0], self.transforms['resize'][1], 3))
        label.set_shape((None, ))
        return (image, label)

    def _py_read_images_n_labels(self, file_path):
        file_path = file_path.numpy().decode()
        img = Image.open(file_path)
        if 'resize' in self.transforms:
            img = img.resize(self.transforms['resize'], Image.ANTIALIAS)
        img = np.asarray(img)
        img = img / 127.5 - 1
        label = self.labels[(self.labels['Image'] == file_path.split('/')[(-1)])].to_numpy()[0][2]
        return (img, np.array([label], dtype=(np.int32)))

    def download(self):
        file_url = 'https://files.naresh1318.com/public/embark/hymenoptera_data.zip'
        print('Downloading AntsNBees dataset from: {}'.format(file_url))
        zip_file_path = '../../hymenoptera_data.zip'
        with open(zip_file_path, 'wb') as (f):
            response = requests.get(file_url, stream=True)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write('\r[{}{}] Downloaded: {}/{} bytes'.format('=' * done, ' ' * (50 - done), dl, total_length))
                    sys.stdout.flush()

        if response.status_code == 200:
            with zipfile.ZipFile(zip_file_path, 'r') as (z):
                if not os.path.exists(self.dataset_path):
                    os.mkdir(self.dataset_path)
                z.extractall(self.dataset_path)
            os.remove(zip_file_path)
            print('\nDownloaded and extracted here: {}'.format(os.path.abspath(self.dataset_path)))
        else:
            print('Unable to download file: {}'.format(response.status_code))


def _show(image, label):
    plt.figure()
    plt.imshow(image)
    plt.title(label.numpy())
    plt.axis('off')
    plt.show()


def main():
    transforms = {'resize': (224, 224)}
    anb = AntsNBees('../../data', 'train', transforms)
    ds = anb.get_dataset()
    for img, lab in ds.take(10):
        _show(img, lab)


if __name__ == '__main__':
    main()
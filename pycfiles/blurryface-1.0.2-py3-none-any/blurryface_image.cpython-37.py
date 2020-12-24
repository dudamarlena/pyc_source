# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\jmd0421\dev\blurryface\blurryface\blurryface_image.py
# Compiled at: 2019-10-17 15:19:48
# Size of source mod 2**32: 1823 bytes
import os
from imutils import paths
import argparse, cv2

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def test_images(image_path, threshold):
    if not os.path.exists(image_path):
        print(f"Directory for images not found: {image_path}")
        return
    else:
        num_blurry = 0
        num_not_blurry = 0
        for imagePath in paths.list_images(image_path):
            image = cv2.imread(imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            blurry = fm < threshold
            if blurry:
                num_blurry += 1
            else:
                num_not_blurry += 1
            print(f"{imagePath} - Blurry={blurry}")

        if num_blurry + num_not_blurry == 0:
            print('No results.')
        else:
            print(f"\nResults: {num_blurry} blurry, {num_not_blurry} not blurry")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image-path', help='path to input directory of images',
      default='img')
    ap.add_argument('-t', '--threshold', type=float, default=200.0, help="focus measures that fall below this value will be considered 'blurry'")
    args = vars(ap.parse_args())
    test_images(args['image_path'], args['threshold'])


if __name__ == '__main__':
    main()
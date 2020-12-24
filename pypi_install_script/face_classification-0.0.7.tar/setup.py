from setuptools import setup

# TODO: More informative metadata creation

setup(
    name='face_classification',
    version='0.0.7',
    description='Train and classifiy faces from images using deep learning. https://gitlab.lftechnology.com/leapfrogai/face-classification/',
    author='Leapfrog Technology INC',
    license='Apache License 2.0',
    packages=['face_classification'],
    install_requires=[
          'dlib==19.17.0',
          'face_recognition',
          'scikit-learn==0.19.1'
      ],
    zip_safe=False
)

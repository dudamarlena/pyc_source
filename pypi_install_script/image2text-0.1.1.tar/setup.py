from setuptools import setup, find_packages
from image2text.statement import path_to_full_text

install_requires = [
    'matplotlib==2.2.2',
    'numpy==1.15.0',
    'opencv-python==3.4.2.17',
    'pytesseract==0.2.4',
    'scikit-image'
]

setup(
    name='image2text',
    version='0.1.1',
    description='Change kor, eng document image to text',
    author='nonameP',
    author_email='nonamep765@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    zip_safe=False
    )
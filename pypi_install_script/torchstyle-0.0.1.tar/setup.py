from setuptools import setup, find_packages

requirements = [
    'numpy',
    'torch',
    'torchvision'
]

readme = open('README.rst').read()

setup(
    name='torchstyle',
    version='0.0.1',
    description='TorchStyle is a Pytorch based framework for GAN based Neural Style Transfer.',
    license='MIT',
    author='Zhi Zhang',
    author_email='850734033@qq.com',
    keywords=['pytorch', 'style transfer'],
    url='https://github.com/tczhangzhi/torchstyle',
    packages=find_packages(exclude=['tests']),
    long_description=readme,
    setup_requires=requirements
)
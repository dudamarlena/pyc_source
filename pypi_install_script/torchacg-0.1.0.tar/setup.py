from setuptools import setup, find_packages

requirements = [
    'numpy',
    'torch',
    'torchvision'
]

readme = open('README.rst').read()

setup(
    name='torchacg',
    version='0.1.0',
    description='TorchACG is a Pytorch based framework for GAN based ACG applications.',
    license='MIT',
    author='Zhi Zhang',
    author_email='850734033@qq.com',
    keywords=['pytorch', 'ACG'],
    url='https://github.com/tczhangzhi/torchacg',
    packages=find_packages(exclude=['tests']),
    long_description=readme,
    setup_requires=requirements
)
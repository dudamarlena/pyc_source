__version__ = '0.0.3'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='robogercontrib.android',
                 version=__version__,
                 author='altertech',
                 author_email='div@altertech.com',
                 description='roboger android plugin',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/alttch/robogercontrib.android',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent',
                 ],
                 python_requires='>=3.6',
                 install_requires=['filetype', 'pyfcm', 'roboger'])

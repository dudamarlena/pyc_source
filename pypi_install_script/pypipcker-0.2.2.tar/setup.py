from setuptools import setup, find_packages
import sys, os

README = open('README.md').read()

setup(name='pypipcker',
    version='0.2.2',
    description='Creates a minimal python package',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Software Development :: Code Generators',
      ],
    keywords='pip package template',
    author='saledddar',
    author_email='saledddar@gmail.com',
    url='https://github.com/saledddar/pypipcker',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=['argparse']
)

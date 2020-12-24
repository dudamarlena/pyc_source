import io
import os
from setuptools import setup


# pip workaround
os.chdir(os.path.abspath(os.path.dirname(__file__)))


# Need to specify encoding for PY3, which has the worst unicode handling ever
with io.open('README.rst', encoding='utf-8') as fp:
    description = fp.read()
setup(name='dockerimage',
      version='0.0',
      py_modules=['dockerimage'],
      description="Manipulate Docker image files directly",
      author="Remi Rampin",
      author_email='remirampin@gmail.com',
      maintainer="Remi Rampin",
      maintainer_email='remirampin@gmail.com',
      url='https://gitlab.com/remram44/dockerimage',
      project_urls={
          'Homepage': 'https://gitlab.com/remram44/dockerimage',
          'Say Thanks': 'https://saythanks.io/to/remram44',
          'Source': 'https://gitlab.com/remram44/dockerimage',
          'Tracker': 'https://gitlab.com/remram44/dockerimage/issues',
      },
      long_description=description,
      license='BSD-3-Clause',
      keywords=['docker', 'image', 'container', 'layers'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering',
          'Topic :: System :: Filesystems'])

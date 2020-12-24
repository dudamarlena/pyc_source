from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()



setup(
  name = 'hsvpicker',
  packages = ['hsvpicker'],
  version = '4.0',
  license='MIT',
  description = 'Finding HSV bounding values for tracking/masking an object.',
  author = 'Karthik Prabu V',
  author_email = 'sanjkar13@gmail.com',
  url = 'https://github.com/Karthikprabuvetrivel/hsvpicker',
  download_url = 'https://github.com/Karthikprabuvetrivel/hsvpicker/archive/v4.0.tar.gz',
  keywords = ['hsv', 'opencv', 'cv2', 'mask', 'track', 'object', 'images', 'videos'],
  install_requires=[
          'numpy',
          'opencv-python',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)

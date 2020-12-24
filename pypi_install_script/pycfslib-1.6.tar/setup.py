from setuptools import setup

setup(name='pycfslib',
      version='1.6',
      description='Library to read, write amd create CFS file and stream, now supports the NEO sleep scoring system. CFS V1, V2 and V3 are supported.',
      url='https://github.com/neurobittechnologies/pycfslib',
      author='Amiya Patanaik',
      author_email='amiya@neurobit.io',
      license='GPL',
      packages=['pycfslib'],
      install_requires=[
          'numpy',
          'scikit-image',
          'scipy',
          'bottleneck',
          'msgpack',
      ],
      zip_safe=False)

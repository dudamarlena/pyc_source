from distutils.core import setup
setup(
  name = 'deepeeg',
  packages = ['deepeeg'],
  version = '0.1',
  license='MIT',
  description = 'A simple library for applying CNN / LSTM models to EEG data.',   # Give a short description about your library
  author = 'Tobias Bredow, Emanuel Metzenthin',
  author_email = 'emanuel.metzenthin@student.hpi.de',
  url = 'https://github.com/emanuel-metzenthin/deepeeg',
  download_url = 'https://github.com/emanuel-metzenthin/deepeeg/archive/v_0.1.tar.gz',
  keywords = ['EEG', 'Electroencephalography', 'Deep Learning', 'CNN', "convolutional neural network",
              'LSTM', 'long-short term memory', 'classification', 'machine learning'],
  install_requires=[
          'numpy',
          'pandas',
          'tensorflow',
          'keras',
          'logging',
          'mne',
          'sklearn',
          'matplotlib'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
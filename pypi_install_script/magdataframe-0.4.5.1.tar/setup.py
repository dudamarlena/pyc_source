from distutils.core import setup
setup(
  name='magdataframe',
  packages=['magdataframe'],
  version='0.4.5.1',
  license='GNU GPLv3',
  description='Extension of the Pandas dataframe for magnetic tensor gradiometry data handling',
  author='Zackary Flansberry',
  author_email='zf@sbquantum.com',
  url='https://github.com/sbquantum2/magdataframe',
  download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords=['pandas', 'dataframe', 'magnetism', 'GIS'],
  install_requires=[
          'pandas',      # Base class
          'numpy',       # Most non-trivial mathematical treatment
          'scipy',       # Interpolation
          'matplotlib',  # All plotting
          'nfft',        # FFTs on non-uniform data
          'haversine',   # Conversions (lon, lat, alt) -> (x,y,z)
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

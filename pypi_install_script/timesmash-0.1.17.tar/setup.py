from setuptools import setup


version = {}
with open("timesmash/_version.py") as fp:
    exec(fp.read(), version)


setup(name='timesmash',
      version=version['__version__'],
      packages=['timesmash', 'timesmash.bin'],
      keywords='timeseries',      
      install_requires=['pandas', 'numpy', 'scikit-learn', 'haversine', 'sodapy'],
      include_package_data=True,
      package_data={
          'bin':
              ['bin/smash',
               'bin/embed',
               'bin/smashmatch',
               'bin/Quantizer',
               'bin/serializer',
               'bin/genESeSS',
               'bin/genESeSS_feature',
               'bin/lsmash',               
               'bin/XgenESeSS'
              ]
      },

      # metadata for PyPI upload
      url='https://gitlab.datadrivendiscovery.org/uchicago/datasmash',
      download_url=('https://gitlab.datadrivendiscovery.org/uchicago/datasmash/archive/'
                    + version['__version__'] + '.tar.gz'),

      maintainer_email='virotaru@uchicago.edu',
      maintainer='Victor Rotaru',

      description=('Quantifier of universal similarity amongst arbitrary data'
                   + ' streams without a priori knowledge, features, or'
                   + ' training.'),

      classifiers=[
          "Programming Language :: Python :: 3"
      ],
      entry_points={
          'd3m.primitives': [
              'timesmash.lsmash_distance=timesmash.lsmash_distance:Lsmash_distance',
              'timesmash.quantizer=timesmash.quantizer:Quantizer'
          ],
      },
     )

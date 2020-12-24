from distutils.core import setup
setup(
  name = 'covidcharter',
  packages = ['covidcharter'],
  version = '0.1',
  license='MIT',
  description = 'A package for charting covid in Virginia counties',
  author = 'Haley Creech',
  author_email = 'haley.creech@gmail.com',
  url = 'https://github.com/creecherr/virginia-covid-charter',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/creecherr/virginia-covid-charter/archive/v.0.1.tar.gz',
  keywords = ['covid', 'vdh', 'virgnia'],
  install_requires=[
          'matplotlib',
          'pandas',
          'click',
          'requests',
          'urllib3'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Healthcare Industry',
    'Topic :: Multimedia :: Graphics :: Capture',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
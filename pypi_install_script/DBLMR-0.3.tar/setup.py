from distutils.core import setup
setup(
  name='DBLMR',
  packages=['DBLMR'],
  version='0.3',
  license='MIT',
  description='A simple OOP Python API wrapper for the dbl.marcorennmaus.de api!',
  author='Arthurdw (Arthur De Witte)',
  author_email='mail.arthurdw@gmail.com',
  url='https://github.com/Arthurdw/DBLMR',
  download_url='https://github.com/Arthurdw/DBLMR/archive/v0.3.tar.gz',
  keywords=['DBL', 'API', 'wrapper', 'Marco'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 4 - Beta',      #  "3 - Alpha", "4 - Beta" or "5 - Production/Stable
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
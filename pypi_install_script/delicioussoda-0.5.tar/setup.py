from distutils.core import setup
setup(
  name='delicioussoda',
  packages=['delicioussoda'],
  version='0.5',
  license='MIT License',
  description='A webscraper for robots.txt files',
  author='Ben Antonellis',
  author_email='strikerbda@gmail.com',
  url='https://github.com/Linnydude3347/delicioussoda',
  download_url='https://github.com/Linnydude3347/delicioussoda/archive/v_0.5.tar.gz',
  keywords=['scraper', 'robot.txt', 'python'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
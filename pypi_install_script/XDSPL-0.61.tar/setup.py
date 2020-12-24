from distutils.core import setup
setup(
  name='XDSPL',
  packages=['XDSPL'],
  version='0.61',
  license='MIT',
  description='The Python library for the Xiler DataServer.',
  author='Arthurdw',
  author_email='mail.arthurdw@gmail.com',
  url='https://github.com/Arthurdw/Xiler-Bots',
  download_url='https://github.com/Arthurdw/Xiler-Bots/blob/master/DataHandeler/Python%20Libary/XDSPL.tar.gz',
  keywords=['XDSPL', 'Xiler', 'Bot', 'DataServer'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)

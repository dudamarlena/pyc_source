from distutils.core import setup

setup(
  name='BeatPy',
  packages=['BeatPy', 'BeatPy.discord', 'BeatPy.util.core'],
  version='v0.0.6',
  license='MIT',
  description='A python utility library to make your python coder life easier!',
  author='Arthurdw (Arthur De Witte)',
  author_email='mail.arthurdw@gmail.com',
  url='https://github.com/Arthurdw/BeatPy',
  download_url='https://github.com/Arthurdw/BeatPy/archive/v0.0.6.tar.gz',
  keywords=['discord', 'util', 'beatpy'],
  classifiers=[
    'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)

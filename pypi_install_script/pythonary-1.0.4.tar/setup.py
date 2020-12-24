from distutils.core import setup

def readme_file_contents():
  with open('README.rst') as f:
    data = f.read()
  return data

setup(
  name = 'pythonary',
  packages = ['pythonary'],
  version = '1.0.4',
  license='MIT',
  description = 'A Python dictionary Module',
  long_description=readme_file_contents(),
  author = 'Arthurdw',
  author_email = 'arthur.dewitte@gmail.com',
  url = 'https://github.com/Arthurdw/pythonary',
  download_url = 'https://github.com/Arthurdw/pythonary/archive/1.0.0.tar.gz',
  keywords = ['oxford', 'dictionary', 'dictionaries'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
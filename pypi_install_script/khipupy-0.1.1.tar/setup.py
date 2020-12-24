from distutils.core import setup

setup(
  name = 'khipupy',
  packages = ['khipupy'],
  version = '0.1.1',
  license='MIT',
  description = 'A Python wrapper for the khipu APIs, for the forgotten devs',
  author = 'Nicolás Góngora ',
  author_email = 'nicolasgongar@gmail.com',
  url = 'https://github.com/N1c0Dev/khipupy',
  download_url = 'https://github.com/N1c0Dev/khipupy/archive/v0.1.1.tar.gz',
  keywords = ['khipu', 'api', 'apiclient', 'api-wrapper', 'pagos-khipu'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

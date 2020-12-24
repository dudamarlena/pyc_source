from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

setup(name='bitshift',
      version='0.0.0',
      description='Unknown',
      long_description=long_description,
      url='https://github.com/monzita/bitshift',
      author='Monika Ilieva',
      author_email='hidden@hidden.com',
      license='MIT',
      keywords='bitshift',
      packages=['bitshift'],
      package_dir={'bitshift' : 'bitshift'},
      install_requires = ['docopt'],
      entry_points = {
        'console_scripts': [
          'bitshift=bitshift.cli:main'
        ],
      },
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Utilities'
      ],
      zip_safe=True)
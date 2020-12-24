from setuptools import setup

setup(name='viper-swift',
      version='0.8',
      description='Create skeleton files for VIPER projects',
      url='https://github.com/eduardocardoso/viper-swift',
      packages=['viper_swift', 'viper_swift.templates'],
      scripts=['bin/viper-swift'],
      install_requires=[
          'argparse',
          'jinja2',
      ],
      include_package_data=True,
      zip_safe=False)

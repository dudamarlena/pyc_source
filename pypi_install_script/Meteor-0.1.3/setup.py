import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'Pillow',
    'qrcode'
    ]

setup(name='Meteor',
      version='0.1.3',
      description='Frontend toolbox',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Build Tools"
        ],
      author='Amadeus',
      author_email='gliheng@gmail.com',
      url='http://github.com/gliheng/Meteor',
      keywords='web frontend javascript build',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="meteor",
      entry_points={
          'console_scripts': [
              'meteor = meteor.scripts.main:main']
      }
      
)

from setuptools import setup

setup(name='dh-poetry',
      version='0.1.2',
      description='Shim between dh-virtualenv and poetry',
      url='http://github.com/maikelwever/dh-poetry',
      author='Maikel Wever',
      author_email='maikelwever@gmail.com',
      license='MIT',
      zip_safe=False,
      packages=['dh_poetry'],
      entry_points={
          'console_scripts': ['dh-poetry=dh_poetry.command_line:main'],
      },
)

from setuptools import setup

setup(name='bclean',
      version='0.0.3',
      description='Delete git branches',
      url='https://github.com/ngeor/bclean',
      author='Nikolaos Georgiou',
      author_email='Nikolaos.Georgiou@gmail.com',
      license='MIT',
      packages=['bclean'],
      zip_safe=False,
      entry_points={
        'console_scripts': ['bclean=bclean.bclean:main']
      })

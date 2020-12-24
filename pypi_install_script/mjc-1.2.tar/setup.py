from setuptools import setup

setup(name='mjc',
      version='1.2',
      description='Minimum Jump Cost dissimilarity algorithm.',
      url='https://github.com/nup002/mjc',
      author='Magne Eik Laruitzen',
      author_email='mag.lauritzen@gmail.com',
      license='MIT',
      packages=['mjc'],
      install_requires=[
        "matplotlib",
        "numpy",
    ],
      zip_safe=False)
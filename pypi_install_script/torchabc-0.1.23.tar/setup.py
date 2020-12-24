from setuptools import setup

setup(
    name='torchabc',
    version='0.1.23',
    description='Abstract Base Classes for pytorch',
    url='http://github.com/blythed/torchabc',
    author='Duncan Blythe',
    author_email='duncanblythe@gmail.com',
    license='MIT',
    packages=['torchabc'],
    install_requires=[
      'pandas',
      'pillow',
      'matplotlib',
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'torchabc = torchabc.__main__:main'
        ]
    },
)

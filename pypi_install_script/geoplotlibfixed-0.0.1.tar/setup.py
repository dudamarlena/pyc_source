from setuptools import setup

setup(name='geoplotlibfixed',
      use_2to3=True,
      packages=['geoplotlibfixed'],
      version='0.0.1',
      description='python toolbox for geographic visualizations',
      author='John Landa',
      author_email='jonathanlanda@gmail.com',
      url='https://github.com/johnlanda/geoplotlib',
      download_url='https://github.com/johnlanda/geoplotlib-fixed/archive/v0.0.1.tar.gz',
      install_requires=['numpy>=1.12','pyglet>=1.2.4']
)

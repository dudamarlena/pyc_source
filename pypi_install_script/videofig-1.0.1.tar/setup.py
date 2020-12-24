from setuptools import setup

setup(name='videofig',
      version='1.0.1',
      description='Lightweight image sequence visualization utility based on matplotlib',
      url="https://github.com/bilylee/videofig",
      author='Bily Lee',
      author_email='bily.lee@qq.com',
      license='MIT',
      packages=['videofig'],
      install_requires=['matplotlib>=2.0.0'],
      zip_safe=False)

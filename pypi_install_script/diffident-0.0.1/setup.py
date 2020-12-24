try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='diffident',
      version='0.0.1',
      description='Dual-pushdown automation about shell or other scripting.',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 1 - Planning',
                   "Programming Language :: Unix Shell",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Other Scripting Engines",
                   "License :: OSI Approved :: MIT License"],
      long_description=open('README.md', 'r').read(),
      packages=['diffident']
      )

from distutils.core import setup
import os

# -------------------------
# Setup
# -------------------------

def read_file(fname):
    "Read a local file"
    HERE = os.path.dirname(__file__)
    try:
        with open(os.path.join(HERE, fname)) as f:
            return f.read()
    except FileNotFoundError:
        return "WARNING: File '%s' not found!" % fname

setup(name='repackage',
      version='0.7.3',
      description= ("Repackaging, call a non-registered package in any "
                    "directory (with relative call). "
                    "Used either by modules moved into to a subdirectory "
                    "or to prepare the import of a non-registered package "
                    "(in any relative path)."),
      url='https://www.settlenext.com',
      author='Laurent Franceschetti',
      author_email='developer@settlenext.com',
      keywords ="package relative path module import library",
      license='MIT',
      packages=['repackage'],
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License"
      ])

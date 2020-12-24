import event,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

#缺少模块ctypes时引发异常,停止安装
try:from ctypes import windll
except ImportError:
    raise NotImplementedError("Module ctypes required")

desc="{} Author:{}".format(
    event.__doc__.replace('\n',''),event.__author__)
try:
    long_desc=event.__doc__+open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='user-event',
  version=event.__version__,
  description=desc,
  long_description=long_desc,
  author=event.__author__,
  author_email=event.__email__,
  platform="win32",
  packages=['event'],
  keywords=["simulate","key","mouse","event"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)"],
)

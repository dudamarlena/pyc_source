import painter,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc=painter.__doc__.replace('\n',' ')

setup(
  name='painter-tk',
  version=painter._ver,
  description=desc,
  long_description=desc+" Welcome to install!",
  author=painter.__author__,
  author_email=painter.__email__,
  py_modules=['painter'], #这里是代码所在的文件名称
  keywords=["simple","text","editor","notepad","tkinter"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Multimedia :: Graphics"],
)

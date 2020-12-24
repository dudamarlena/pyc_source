import py_smile,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

long_desc="由于上传问题,说明暂无法正常显示。详见模块内的文档字符串。See doc string in this module for more info."

setup(
  name='py-smile',
  version=py_smile.__version__,
  description="A small smile program in command-line.",
  long_description=long_desc,
  author=py_smile.__author__,
  author_email=py_smile.__email__,
  py_modules=['py_smile'], #这里是代码所在的文件名称
  keywords=["smile","terminal","command-line"],
  classifiers=[
      'Programming Language :: Python',
      "Topic :: Terminals"],
  install_requires=["console-tool"]
)
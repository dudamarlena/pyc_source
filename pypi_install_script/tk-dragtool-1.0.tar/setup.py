import tk_dragtool,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc=tk_dragtool.__doc__.replace('\n',' ')
long_desc=desc+"  注:由于上传问题,说明暂无法正常显示。详见模块内的文档字符串。See doc string in this module for more info."

setup(
  name='tk-dragtool',
  version=tk_dragtool.__version__,
  description=desc,
  long_description=long_desc,
  author=tk_dragtool.__author__,
  author_email="3416445406@qq.com",
  py_modules=['tk_dragtool'], #这里是代码所在的文件名称
  keywords=["tkinter","drag","tool"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)"],
)

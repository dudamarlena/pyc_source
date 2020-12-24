# from distutils.core import setup
from setuptools import setup

def readme_file():
    with open("README.rst",encoding="utf-8") as rf:
        return rf.read()
setup(name="chang",version="1.0.0",description="this is a niubi lib",packages=["chang"],py_modules=["Tool"],author="changhaiyang",author_email="635498322@qq.com",long_description=readme_file(),
      url="https://study.163.com/course/courseLearn.htm?courseId=1004569003#/learn/video?lessonId=1051875146&courseId=1004569003")

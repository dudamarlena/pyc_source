VERSION = "1.0.10"

from distutils.core import setup

setup(name="hzpromise",
     author="Huzheng",
     author_email= "backbye@163.com",
     description= "An implementation of Promises/A+ for Python",
     version=str(VERSION),
     url = "https://gitee.com/hu321/promise",
     #py_modules=["hzpromise"],
     packages=["hzpromise"],
     python_requires='>=3.5'
     )


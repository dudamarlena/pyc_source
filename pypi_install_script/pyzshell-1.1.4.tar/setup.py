#conding=utf-8
from distutils.core import setup
with open("README.rst", "r",encoding='utf-8') as fh:
    long_desc = fh.read()
setup(

    name= 'pyzshell',

    version= '1.1.4',

    py_modules =['zshell'],

    author= 'cedar12',

    author_email='cedar12.zxd@qq.com',

    url='https://github.com/cedar12/zshell.git',

    description= '快速构建命令行(shell)应用',

    long_description=long_desc

)
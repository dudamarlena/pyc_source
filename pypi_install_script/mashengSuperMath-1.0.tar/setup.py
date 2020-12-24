from distutils.core import setup


setup(
    name='mashengSuperMath',    #对外我们模块的名字
    version='1.0',  #版本号
    description='这是第一个对外发布的模块，里面只有数学测试哦',  #描述
    author='Benson',    #作者
    author_email='hbma_2008@126.com',
    py_modules=['mashengSuperMath.demo1','mashengSuperMath.demo']   #要发布的模块

)
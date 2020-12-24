from distutils.core import setup

setup(
    name="baizhanSuperMath2" ,    #对外我们模块的名字
    version="1.0",   #版本号
    description="这是第一个对外发布的模块，仅限测试哦",    #描述
    author="zsx",    #作者
    author_email="459361408@qq.com",
    py_modules=["baizhanSuperMath2.demo_01","baizhanSuperMath2.demo_02"]      #要发布的模块
)
from distutils.core import setup
setup( name='baizhanSuperMathModules234521',#对外我们模块的名字
        version='1.0',# 版本号
        description='这是第一个对外发布的模块，测试哦',# 描述
        author='gaoqi',# 作者
        author_email='349095590@qq.com',
        py_modules=['math3420935.demo1','math3420935.demo2']# 要发布的模块
)

# open in terminal
# python setup.py sdist
# python setup.py install
# 通过文本文件保存为所有文件类型
# python setup.py sdist upload
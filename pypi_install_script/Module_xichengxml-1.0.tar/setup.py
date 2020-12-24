from distutils.core import setup

# ---------------------------
# @description 模块的本地发布
# 发布流程：cd T009_Module → python setup.py sdist → python setup.py install → 进入pycharm setttings project interpreter
# 可以看到发布的模块
# @author xichengxml
# @date 2020/3/21 下午 06:21
# ---------------------------


setup(
    name='Module_xichengxml',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author='xichengxml',  # 作者
    author_email='xichengxml@163.com',
    py_modules=['Module_xichengxml.Demo01', 'Module_xichengxml.Demo02']  # 要发布的模块
)

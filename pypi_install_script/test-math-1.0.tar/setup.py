from distutils.core import setup

setup(
    name = 'test-math',  #对外我们模块的名字
    version = '1.0',  #版本号
    description = '这只是测试', ##模块说明
    author = 'LQ',  ##作者
    author_email='lksh@130.com',  #作者邮箱
    py_modules =['test-math.module_A1','test-math.module_A2']   ##要发布的模块
)
#引入构建包信息的模块
from distutils.core import setup

#定义发布包文件信息
setup(
    name ="huanying",
    version ="1.0",
    description="我的测试包",
    author="幻影",
    author_email="850287262@qq.com",
    py_modules=['__init__','game_engine32','game_sprites32','main']

)
from distutils.core import setup

setup(name="linlianqin_1",#压缩包的名字
      version="52.0",#版本
      description="linlianqin发送与接收消息模块",#简要描述信息
      long_description="刘锦林给她的发送与接收信息模块",#完整的描述信息
      author="liujinlin",#开发者的名字
      author_email="1371174718@qq.com",#开发者的邮箱
      url="http://www.linlianqin.com",#开发者的个人主页
      py_modules=["linlianqin_1.send_message",
                   "linlianqin_1.reseive_message"])#需要发布的包中的模块
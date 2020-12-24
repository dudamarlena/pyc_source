from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "pydobotlink",      #这里是pip项目发布的名称
    version = "1.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "pydobotlink"),
    description = "dobotlink python demo",
    long_description = "dobotlink python demo",
    license = "MIT Licence",
 
    url = "https://github.com/songlijun2019/pydobotlink",
    author = "SongliJun",
    author_email = "songlijun@dobot.cc",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["websockets", "asyncio", "colorlog"]          #这个项目需要的第三方库
)
#https://blog.csdn.net/szfhy/article/details/79833491?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
from distutils.core import setup
setup(
    name="cdnutil",
    version="1.0.3",
    description="cdnutil version1.0.3, envrionment 2.7.x latter",
    author="liangzhi",
    py_modules=[
        "cdnutil.basepy",
        "cdnutil.cdnmstk",
        "cdnutil.common",
        "cdnutil.config",
        "cdnutil.configYML",
        "cdnutil.configINI",
        "cdnutil.Log",
        "setup"
    ],
    url="https://github.com/nigth-mare/ipanel-cdn-py.git"
)
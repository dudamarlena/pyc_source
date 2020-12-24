from setuptools import setup, find_packages

# files = ["src/*"]


setup(
      name="tcpth.cmd",
      version="1.1",
      keywords='tcp through cmd',
      description="The cmd which can modify tcp through server config",
      author="wls",
      author_email="wanglongshengdf@gmail.com",
      url="https://github.com/wanglongshengdf",
      license="GNU",
      python_requires='==2.7.*',
      install_requires=['requests==2.20.0','pyfiglet==0.8.post1'],
      packages=find_packages(),
      scripts=["scripts/tcpthcmd"],
      )

from setuptools import setup 
import sys



setup(name='yxs_required',   
      version='1.0',    
      description='Pypi modules that I need to install for a new python environment',    
      author='Blacksong',    
      install_requires=['lxml','pandas','bs4','requests','PyQt5','imageio','rsa','scipy','matplotlib','opencv-python',
        'tushare','lulu','yxspkg_encrypt','yxspkg_tecfile','yxspkg_wget','lulu','ipython',
        'yxspkg_songzgif','tensorflow','keras','pyinstaller'],
      author_email='blacksong@yeah.net',       
      url='https://github.com/blacksong',
      py_modules=['yxspkg_required'], 
      classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)   

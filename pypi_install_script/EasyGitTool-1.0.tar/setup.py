from setuptools import setup, find_packages  
  
setup(  
    name = "EasyGitTool",  
    version = "1.0",  
    long_description = "EasyGitTool for python",  
    license = "Apache License",  
  
    url = "https://easygittool.github.io",  
    author = "Mr.yan",  
    author_email = "A2564011261@163.com",  
  
    packages = find_packages(),  
    include_package_data = True,  
    platforms = "any",  
    install_requires = [],  
  
    scripts = [],  
    entry_points = {  
        'console_scripts': [  
            'EasyGitTool = EasyGitTool:main'  
        ]  
    }  
)
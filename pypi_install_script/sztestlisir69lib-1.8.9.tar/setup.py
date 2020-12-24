from setuptools import setup 
 
#在这里可以定议一个函数用来读取README中的字符信息，再放入description中
def readme_file():
    with open('README.rst',encoding='utf-8') as rf:
        content = rf.read()
        print(content)
        return content

setup(
        name='sztestlisir69lib',
        version='1.8.9',
        long_description=readme_file(),
        author='huoty',  # 作者
        author_email='sudohuoty@163.com',
        url='https://www.konghy.com',
        packages=['sztestlisir69lib'],
		py_modules = ['tool'] ,
		license = 'MIT')
from setuptools import setup 
 
#在这里可以定议一个函数用来读取README中的字符信息，再放入description中
def readme_file():
    with open('README.rst',encoding='utf-8') as rf:
        content = rf.read()
        print(content)
        return content

setup(
        name='lbplistlib',
        version='1.1.0',
        description = 'this BIF is use for print list.',
        long_description=readme_file(),
        author='libin',  # 作者
        author_email='unifacecode@163.com',
        url='https://www.hongkongcity.com',
        packages=['lbplistlib'],
		py_modules = ['Tool'] ,
		license = 'MIT')
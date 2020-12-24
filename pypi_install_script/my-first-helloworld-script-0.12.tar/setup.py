import setuptools

setuptools.setup(
    name='my-first-helloworld-script',
    version='0.12',
    author="lian zheng",
    author_email="lianzheng07@163.com",
    description="This is my first pip package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LeonLian/pipPackagingTest.git",
    # packages=setuptools.find_packages(),
    scripts=['helloworld.py']
)










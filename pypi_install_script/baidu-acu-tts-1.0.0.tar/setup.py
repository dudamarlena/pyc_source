from setuptools import setup, find_packages

# here = os.path.abspath(os.path.dirname(__file__))
# changes = open(os.path.join(here, 'CHANGES.md')).read()
# with open('CHANGES.md') as f:
#     changes = f.read()

setup(
    name="baidu-acu-tts",
    version="1.0.0",
    description="tts grpc client",
    long_description="init",
    long_description_content_type='text/markdown',
    author="Baidu",
    url="",
    author_email="1908131339@qq.com",
    packages=find_packages(),
    license="Apache License",
    python_requires=">=2.7",
    install_requires=["protobuf", "grpcio", 'threadpool'],
    keywords=['baidu', 'tts', 'speech'],
)

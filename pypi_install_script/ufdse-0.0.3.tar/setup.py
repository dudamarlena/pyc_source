from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf-8') as f:
    README = f.read()

setup(
    name='ufdse',
    version='0.0.3',
    description="Magnificent demos in Python.",
    long_description=README,
    long_description_content_type='text/markdown',
    author='sc-1123',
    author_email='2125587278@qq.com',
    maintainer='sc-1123',
    maintainer_email='2125587278@qq.com',
    url='https://github.com/sc-1123/ufdse',
    packages=find_packages(),
    keywords=['demo', 'tools'],
    platforms=['any'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ]
    )

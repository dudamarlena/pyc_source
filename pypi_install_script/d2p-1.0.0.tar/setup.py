try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name='d2p',
      version='1.0.0',
      description="exchange xml comments from you-get to plain text comments.",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Jian Gao',
      author_email='2125587278@qq.com',
      maintainer='Jian Gao',
      maintainer_email='2125587278@qq.com',
      url='https://github.com/sc-1123/d2p',
      packages=['d2p'],
      keywords=['exchange'],
      platforms=['any'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ]
      )
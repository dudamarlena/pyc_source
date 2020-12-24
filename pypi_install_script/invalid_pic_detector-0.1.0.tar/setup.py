from setuptools import setup


setup(
    name='invalid_pic_detector',
    version='0.1.0',
    description='图片有效性检测（是否为黑/白屏）',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/IPD',
    py_modules=['ipd'],
    install_requires=[
        'scikit-image',
        'loguru',
        'opencv-python',
        'numpy',
        'scipy',
    ]
)

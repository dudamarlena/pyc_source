from setuptools import setup

setup(
    name='auto-battleship',
    version='1.0',
    packages=['autobattleship'],
    license='MIT',
    author='UNCC ACM',
    install_requires=[
        'Pillow',
        'PyAutoGUI',
        'PyGetWindow',
        'PyMsgBox',
        'PyRect',
        'PyScreeze',
        'PyTweening'
    ],
    package_data={
        'autobattleship': [
            'res/*.png'
        ]
    }
)

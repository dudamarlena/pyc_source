from setuptools import setup

setup(
    name='spell-terminal',
    version='1.0',
    py_modules=['spell'],
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
        'requests',
        'pyperclip'
    ],
    entry_points='''
        [console_scripts]
        spell=spell:command_line
    '''
)

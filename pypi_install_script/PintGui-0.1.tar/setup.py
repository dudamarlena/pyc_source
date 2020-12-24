from setuptools import setup, find_packages

version = '0.1'

setup(
    name="PintGui",
    version=version,
    packages=find_packages(),
    package_data={"PintGui":["MainWindow.qml"]},
    install_requires=['pint','pyside2'],
    entry_points = '''
      [gui_scripts]
      PintGui = PintGui.scripts.main:start
      ''' 
    )

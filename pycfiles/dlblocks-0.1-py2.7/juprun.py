# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/dlblocks/juprun.py
# Compiled at: 2018-12-11 12:52:10
r"""

commands 

cp juprun.py /usr/bin/juprun
chmod +x /usr/bin/juprun
touch /usr/bin/juprun2
echo "jupyter nbconvert --to notebook --execute "\$1" --output "\$2"" > /usr/bin/juprun2
chmod +x /usr/bin/juprun2
"""
import random
from shutil import copyfile
import os, sys
source_notebook = sys.argv[1]
destination_notebook = sys.argv[2]
print 'source_notebook', source_notebook
print 'destination_notebook', destination_notebook
port_no = 9200 + random.randint(0, 600)
from subprocess import Popen
import subprocess, time
commands = [
 'jupyter', 'notebook', "--NotebookApp.token=''", '--NotebookApp.port=%d' % port_no, '--ip=127.0.0.1', '--allow-root']
tmp_name = '.' + str(random.randint(999999, 99999999)) + '.ipynb'
copyfile(source_notebook, tmp_name)
p = subprocess.Popen(commands)
import atexit

def exit_handler():
    p.terminate()


atexit.register(exit_handler)
time.sleep(5)
print 'The notebook server is ready'
from selenium import webdriver
d = webdriver.PhantomJS()
d.get('http://localhost:%d' % port_no)
d.find_element_by_css_selector('[name=password]').send_keys('letmein2')
d.find_element_by_css_selector('[type=submit]').click()
d.find_element_by_css_selector('body').text
d.get('http://localhost:%d/notebooks/%s' % (port_no, tmp_name))
d.find_element_by_css_selector('body').text
time.sleep(7)
d.execute_script('IPython.notebook.execute_all_cells();')
copyfile(tmp_name, destination_notebook)
i = 0
while True:
    i += 1
    time.sleep(5)
    if i % 2 == 0:
        d.execute_script('IPython.notebook.save_checkpoint();')
        copyfile(tmp_name, destination_notebook)
        os.system('jupyter nbconvert --to html %s' % destination_notebook)
        print 'saving'
        if not d.execute_script('return  IPython.notebook.kernel_busy;'):
            break

d.execute_script('IPython.notebook.save_checkpoint();')
time.sleep(5)
print 'Execution complete'
copyfile(tmp_name, destination_notebook)
os.system('jupyter nbconvert --to html %s' % destination_notebook)
os.remove(tmp_name)
p.terminate()
try:
    os.remove('ghostdriver.log')
except:
    pass
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globenet/paste/project/create-bootstrap.py
# Compiled at: 2008-08-24 07:46:59
import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("\nimport os, subprocess\ndef after_install(options, home_dir):\n    subprocess.call([join(home_dir, 'bin', 'easy_install'),'--always-unzip','globenet'])\n"))
f = open('bootstrap.py', 'w')
f.write(output)
f.close()
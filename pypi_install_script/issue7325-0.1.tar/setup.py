import os
import sys
import sysconfig

print("setup.py is executing")
msg = """
WARNING: use of "pip download --no-deps" allowed arbitrary code execution
         see https://github.com/pypa/pip/issues/7325
"""
pth = "import sys; f = sys.__stderr__; f.write(%r); f.flush()" % msg
site_packages = sysconfig.get_path("purelib")
fname = os.path.join(site_packages, "issue7325.pth")
open(fname, "w").write(pth)
sys.exit("setup.py was executed :(")

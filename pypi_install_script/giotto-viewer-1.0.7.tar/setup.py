import subprocess
from distutils.command.build import build as _build
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

# This class handles the pip install mechanism.
class build(_build):  # pylint: disable=invalid-name
  sub_commands = _build.sub_commands + [("CustomCommands", None)]

CUSTOM_COMMANDS = [
	["libdir=`ls -1 build|grep \"lib\"`; cd build/$libdir/giotto_viewer/ && touch finished"]]

class CustomCommands(setuptools.Command):
  """A setuptools Command class able to run arbitrary commands."""

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def RunCustomCommand(self, command_list):
    print("Running command: %s" % command_list)
    p = subprocess.Popen(
        command_list,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # Can use communicate(input='y\n'.encode()) if the command run requires
    # some confirmation.
    stdout_data, _ = p.communicate()
    print("Command output: %s" % stdout_data)
    if p.returncode != 0:
      raise RuntimeError(
          "Command %s failed: exit code: %s" % (command_list, p.returncode))

  def run(self):
    for command in CUSTOM_COMMANDS:
      self.RunCustomCommand(command)

setuptools.setup(
	name="giotto-viewer",
	version="1.0.7",
	author="Qian Zhu",
	author_email="zqian@jimmy.harvard.edu",
	description="giotto-viewer is a web-based locally hosted visualization tool for spatial transcriptomic data",
	long_description="Includes side-by-side interactive exploration of single-cell imaging data in physical space and in expression space. It also includes the ability to overlay of multiple types of additional data such as staining images, segmentations, cluster annotations, and gene expression. Users can easily select cells and save them for downstream analyses.",
	long_description_content_type="text/markdown",
	url="http://spatial.rc.fas.harvard.edu",
	packages=setuptools.find_packages(),
	entry_points = {
		"console_scripts": [
			"giotto_prepare_annot = giotto_viewer.prepare_annot:main", 
			"giotto_read_matrix_custom = giotto_viewer.read_matrix_custom:main",
			"giotto_setup_image = giotto_viewer.giotto_setup_image:main",
			"giotto_setup_viewer = giotto_viewer.giotto_setup_viewer:main",
			"giotto_copy_js_css = giotto_viewer.giotto_copy_js_css:main",
			"giotto_step1_modify_json = giotto_viewer.giotto_step1_modify_json:main"
		]
	},
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	python_requires=">=3.5",
	package_data={"giotto_viewer":  ["prepare_annot.py", 
		"read_matrix_custom.py", "giotto_setup_image.py", "giotto_setup_viewer.py",
		"giotto_step1_modify_json.py",
		"giotto_copy_js_css.py",
		"js/bootstrap.4.1.0.min.js", 
		"js/jquery.3.3.1.min.js", 
		"js/jquery-ui.min.js", 
		"js/L.Control.MousePosition.js", 
		"js/leaflet.js", 
		"js/leaflet-lasso-2.js", 
		"js/L.Map.Sync.js", 
		"js/popper.min.js", 
		"js/script.stitched.class.js", 
		"css/leaflet.css", 
		"css/L.Control.MousePosition.css", 
		"css/font-awesome.4.7.0.min.css", 
		"css/jquery-ui.min.css", 
		"css/bootstrap.4.1.0.min.css"]},

	install_requires=[
		"scipy", "numpy", "pandas", "seaborn", "matplotlib", "jsbeautifier"],
	cmdclass={
		"build": build,
		"CustomCommands": CustomCommands,
		}	
)
	

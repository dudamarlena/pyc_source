
import site, shutil, os, sys

#print(site.getusersitepackages()) # https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory

s = site.getusersitepackages()
where = input ("Where do you like to install Pyabr? ")

shutil.copyfile(s+"/pyabr/pyabr",where+"/pyabr.zip")
os.mkdir(where+"/pyabr-install")
shutil.unpack_archive(where+"/pyabr.zip",where+"/pyabr-install","zip")
os.system("cd "+where+"/pyabr-install && \""+sys.executable+"\" install.py")
if os.path.isdir(where+"/Pyabr"): shutil.rmtree(where+"/Pyabr")
shutil.copytree(where+"/pyabr-install/stor",where+"/Pyabr")
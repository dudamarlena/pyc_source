import hashlib
import filecmp
def gethash(filepath):
    hasher=hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    result=hasher.hexdigest()
    return result

def folder_diff(folderpath1,folderpath2):
    result=filecmp.dircmp(folderpath1,folderpath2)
    report=result.report()
    

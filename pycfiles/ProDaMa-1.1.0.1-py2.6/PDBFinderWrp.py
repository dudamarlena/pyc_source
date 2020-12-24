# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/PDBFinderWrp.py
# Compiled at: 2009-09-24 03:11:06
import cPickle, datetime, calendar
from ftplib import FTP
from config import DATA
protein_fields = [
 'Header', 'Date', 'Compound', 'Source', 'Author', 'Exp-Method', 'Resolution', 'R-Factor', 'Free-R', 'N-Models', 'Ref-Prog',
 'HSSP-N-Align', 'T-Frac-Helix', 'T-Frac-Beta', 'T-Nres-Prot', 'T-non-Std', 'T-Nres-Nucl', 'T-Water-Mols', 'HET-Groups', 'Het-Id', 'Natom', 'Name']
chain_fields = [
 'Sec-Struc', 'Helix', 'i,i+3', 'i,i+5', 'Beta', 'B-Bridge', 'Para-Hb', 'Anti-Hb', 'Amino-Acids', 'T-non-Std', 'Miss-BB', 'Miss-SC', 'only-Ca', 'UNK', 'CYSS', ' Break', 'Nucl-Acids', 'Substrate', 'Water-Mols']
local_file_date = None
pdbfinder_data = None

def __getFtpConnection():
    """
    Returns a FTP connection to the PDBFINDER web server
    """
    ftpConnection = FTP('ftp.cmbi.ru.nl')
    ftpConnection.login()
    ftpConnection.cwd('/pub/molbio/data/pdbfinder/')
    return ftpConnection


def __getDate(ftp):
    """
    Looks for the last update of PDBFINDER. 
    
    arguments:
        ftp: a ftp connection to PDBFINDER
    
    return:
        the date of the last update
    """
    directory = []
    ftp.retrlines('LIST', directory.append)
    date = [ i for i in directory[0].split(' ') if i ][5:7]
    month = [ i for i in calendar.month_abbr ].index(date[0])
    return datetime.date(datetime.date.today().year, month, int(date[1]))


def __getFile(ftp):
    """
    Retrieves the PDFFINDER database.
    
    arguments:
        ftp: a ftp connection to PDBFINDER
    """
    local_file = open(DATA + '/PDBFIND.TXT', 'w')
    ftp.retrbinary('RETR PDBFIND.TXT', local_file.write)
    local_file.close()


def __pdbFinderPickleUpdate():
    """
    Looks for changes in the PDBFINDER database  and update the local database if needed.
    """
    ftpConnection = __getFtpConnection()
    remote_file_date = __getDate(ftpConnection)
    try:
        local_file = open(DATA + '/fndrpickle', 'r')
        local_file_date = cPickle.load(local_file)
    except:
        local_file_date = datetime.date(1, 1, 1)

    if remote_file_date > local_file_date:
        local_file = open(DATA + '/fndrpickle', 'w')
        cPickle.dump(remote_file_date, local_file)
        __getFile(ftpConnection)
        remote_finder_file = open(DATA + '/PDBFIND.TXT', 'r')
        remote_finder_split = ('').join(remote_finder_file.readlines()).replace('  ', '')
        remote_finder_split = [ line[line.find('\n') + 1:] for line in remote_finder_split.split('//') if line.find('ID') != -1 ]
        pdbfinder_data = {}
        for prot in remote_finder_split:
            id = prot.splitlines()[0][5:]
            pdbfinder_data[id] = prot

        cPickle.dump(pdbfinder_data, local_file)
        local_file.close()
        remote_finder_file.close()
        ftpConnection.quit()
        return True
    else:
        ftpConnection.quit()
        return False


def __update(force=False):
    """
    Checks for changes in the local copy of the PDBFINDER file.
    
    arguments:
        force: to force the upload 
    """
    global local_file_date
    global pdbfinder_data
    if force or __pdbFinderPickleUpdate():
        try:
            pdbfinder_file = open(DATA + '/fndrpickle', 'r')
        except:
            __pdbFinderPickleUpdate()
            pdbfinder_file = open(DATA + '/fndrpickle', 'r')
        else:
            local_file_date = cPickle.load(pdbfinder_file)
            pdbfinder_data = cPickle.load(pdbfinder_file)
            pdbfinder_file.close()


def __getData(protein_data, field_name):
    """
    Reads the data associated on a protein to recovery the values for the given filed name
    
    arguments:
        protein_data: all pdb finder data related with a protein
    
        field_name: a value in protein_fields
    
    return:
        a string with the different values for the given field_name
    """
    return (',').join([ line[line.find(':') + 2:] for line in protein_data.splitlines() if line.find(field_name) != -1
                      ])


def getStructureData(str_id):
    """
    Reads the PDBFINDER database to recovery the protein data for a given protein.
    
    arguments:
        str_id: a  protein structure identifier 
    
    return:
        a dictionary with keys the PDBFINDER fields and values a list of the corresponding items retrieved by the database
    """
    try:
        protein_data = pdbfinder_data[str_id]
    except:
        return
    else:
        structure_data = {}
        for protein_field in protein_fields:
            structure_data[protein_field.replace('-', '_').replace('+', '').replace(',', '')] = __getData(protein_data, protein_field)

    return structure_data


def getChainData(str_id):
    """
    Reads the PDBFINDER database to recovery the chain data for a given protein.
    
    arguments:
        str_id: a  protein structure identifier 
    
    return:
        a dictionary with keys the pdbfinder fields and values a list of the corresponding items retrieved by the database
    """
    try:
        protein_data = pdbfinder_data[str_id]
    except:
        return
    else:
        protein_data = protein_data.split('Chain')[1:]
        chains_data = {}
        for chain in protein_data:
            chain_data = {}
            chain_id = chain.splitlines()[0][2]
            for chain_field in chain_fields:
                chain_data[chain_field.replace('-', '_').replace('+', '').replace(',', '').strip()] = __getData(chain, chain_field)

            if chains_data.has_key(chain_id):
                for key in [ key for key in chains_data[chain_id].keys() if not chains_data[chain_id][key] ]:
                    chains_data[chain_id][key] = chain_data[key]

            else:
                chains_data[chain_id] = chain_data

    return chains_data


def checkForChanges():
    if datetime.date.today() > local_file_date:
        __update()


notImported = True
if notImported:
    __update(True)
    notImported = False
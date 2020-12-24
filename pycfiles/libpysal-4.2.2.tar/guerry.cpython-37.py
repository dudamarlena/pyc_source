# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/guerry.py
# Compiled at: 2019-12-05 21:58:01
# Size of source mod 2**32: 6700 bytes
"""Guerry Moral Statistics dataset.

The version retrieved here comes from:
     https://s3.amazonaws.com/geoda/data/guerry.zip
"""
from .base import _fetch, RemoteFileMetadata
GUERRY = RemoteFileMetadata(filename='guerry.zip',
  url='https://s3.amazonaws.com/geoda/data/guerry.zip',
  checksum='e781a4be1450c9e4fb287440bbb5ffafd9ec63bdf42745158205d92970cca187')
description = '\nguerry\n======\n\nAndre-Michel Guerry data on "moral statistics" 1930 crime, suicide, literacy and other “moral statistics” in 1830s France.\n\n- Observations = 85\n- Variables = 23\n- Years = 1915-1934\n- Support = polygon\n\nFiles\n-----\nGuerry.dbf  Guerry_documentation.html  Guerry.geojson  Guerry.prj  Guerry.shp  Guerry.shx  README.md\n\n\nVariables\n---------\n\ndept, code_de \tDepartment ID: Standard numbers for the departments \t \nregion \tRegion of France (‘N’=’North’, ‘S’=’South’, ‘E’=’East’, ‘W’=’West’, ‘C’=’Central’). Corsica is coded as NA. \t \ndprtmnt \tDepartment name: Departments are named according to usage in 1830, but without accents. A factor with levels Ain Aisne Allier … Vosges Yonne \t \ncrm_prs \tPopulation per Crime against persons. \tA2. Compte général, 1825-1830\ncrm_prp \tPopulation per Crime against property. \tCompte général, 1825-1830\nlitercy \tPercent of military conscripts who can read and write. \tA2 \ndonatns \tDonations to the poor. \tA2. Bulletin des lois\ninfants \tPopulation per illegitimate birth. \tA2. Bureau des Longitudes, 1817-1821\nsuicids \tPopulation per suicide. \tA2. Compte général, 1827-1830\nmaincty \tSize of principal city (‘1:Sm’, ‘2:Med’, ‘3:Lg’), used as a surrogate for population density. Large refers to the top 10, small to the bottom 10; all the rest are classed Medium. \tA1. An ordered factor with levels: 1:Sm < 2:Med < 3:Lg\nwealth \tPer capita tax on personal property. A ranked index based on taxes on personal and movable property per inhabitant. \tA1\ncommerc \tCommerce and Industry, measured by the rank of the number of patents / population. \tA1\nclergy \tDistribution of clergy, measured by the rank of the number of Catholic priests in active service population. \tA1. Almanach officiel du clergy, 1829\ncrim_prn \tCrimes against parents, measured by the rank of the ratio of crimes against parents to all crimes – Average for the years 1825-1830. \tA1. Compte général\ninfntcd \tInfanticides per capita. A ranked ratio of number of infanticides to population – Average for the years 1825-1830. \tA1. Compte général\ndntn_cl \tDonations to the clergy. A ranked ratio of the number of bequests and donations inter vivios to population – Average for the years 1815-1824. \tA1. Bull. des lois, ordunn. d’autorisation\nlottery \tPer capita wager on Royal Lottery. Ranked ratio of the proceeds bet on the royal lottery to population — Average for the years 1822-1826. \tA1. Compte rendu par le ministre des finances\ndesertn \tMilitary desertion, ratio of number of young soldiers accused of desertion to the force of the military contingent, minus the deficit produced by the insufficiency of available billets – Average of the years 1825-1827. \tA1. Compte du ministère du guerre, 1829 état V\ninstrct \tInstruction. Ranks recorded from Guerry’s map of Instruction. Note: this is inversely related to Literacy \t \nPrsttts \tNumber of prostitutes registered in Paris from 1816 to 1834, classified by the department of their birth \tParent-Duchatelet (1836), De la prostitution en Paris\ndistanc \tDistance to Paris (km). Distance of each department centroid to the centroid of the Seine (Paris) \tCalculated from department centroids\narea \tArea (1000 km^2). \tAngeville (1836)\npop1831 \tPopulation in 1831, in 1000s \tTaken from Angeville (1836), Essai sur la Statistique de la Population français\nDetails\n\nNote that most of the variables (e.g., Crime_pers) are scaled so that more is “better”. \n\nValues for the quantitative variables displayed on Guerry’s maps were taken from Table A2 in the English translation of Guerry (1833) by Whitt and Reinking. Values for the ranked variables were taken from Table A1, with some corrections applied. The maximum is indicated by rank 1, and the minimum by rank 86. \nSources\n\nAngeville, A. (1836). Essai sur la Statistique de la Population française Paris: F. Doufour. \n\nGuerry, A.-M. (1833). Essai sur la statistique morale de la France Paris: Crochard. English translation: Hugh P. Whitt and Victor W. Reinking, Lewiston, N.Y. : Edwin Mellen Press, 2002. \n\nParent-Duchatelet, A. (1836). De la prostitution dans la ville de Paris, 3rd ed, 1857, p. 32, 36 \nReferences\n\nDray, S. and Jombart, T. (2011). A Revisit Of Guerry’s Data: Introducing Spatial Constraints In Multivariate Analysis. The Annals of Applied Statistics, Vol. 5, No. 4, 2278-2299., DOI: 10.1214/10-AOAS356. \n\nBrunsdon, C. and Dykes, J. (2007). Geographically weighted visualization: interactive graphics for scale-varying exploratory analysis. Geographical Information Science Research Conference (GISRUK 07), NUI Maynooth, Ireland, April, 2007. \n\nFriendly, M. (2007). A.-M. Guerry’s Moral Statistics of France: Challenges for Multivariable Spatial Analysis. Statistical Science, 22, 368-399. \n\nFriendly, M. (2007). Data from A.-M. Guerry, Essay on the Moral Statistics of France (1833). \nSee Also\n\nThe Guerry package for maps of France: gfrance and related data. \n\nPrepared by Center for Spatial Data Science. Last updated July 3, 2017. Data provided “as is,” no warranties.\n\n\n\n'

def fetch_guerry(meta_data=GUERRY, dir_name='guerry', data_home=None, download_if_missing=True, description=description):
    """Download the guerry data-set.

    Download it if necessary - will check if it has already been fetched.

    Parameters
    ----------
    meta_data: RemoteFileMetadata
            fields of remote archive
             - filename
             - url
             - checksum

    dir_name: string
            the name of the dataset directory under the examples parent directory

    description: string
            Contents of the README.md file for the example dataset.

    data_home : option, default: None
        Specify another download and cache folder for the datasets. By default
        all libpysal data is stored in ~/libpysal_data' subfolders

    download_if_missing : optional, True by default
       If False, raise a IOError if the data is not locally available instead
       of trying to download the data from the source site.

    """
    _fetch(meta_data,
      dir_name,
      description,
      data_home=data_home,
      download_if_missing=download_if_missing,
      is_dir=False)
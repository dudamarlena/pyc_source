# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/access/datasets/datasets.py
# Compiled at: 2020-02-24 17:09:30
# Size of source mod 2**32: 4517 bytes
import os, requests, pandas as pd

class datasets(object):
    _dir = 'chi_med_data'
    _dir_path = os.path.join('./', _dir)
    _abs_path = os.path.abspath(_dir_path)
    _dwnld_data = {'chi_times':'https://drive.google.com/uc?authuser=0&id=1IcfJimPj4C5ZN5Xc-nvq_DModcCO6GY3&export=download', 
     'chi_euclidean':'https://drive.google.com/uc?authuser=0&id=1qq5ZWOaq5uxJOu9QzsNCw5WhdATgIhzK&export=download', 
     'chi_euclidean_neighbors':'https://drive.google.com/uc?authuser=0&id=1GQFBbWEtltT5MhbtC3iJXXfPCoXUPfTJ&export=download', 
     'chi_doc':'https://drive.google.com/uc?authuser=0&id=12QXTHucipDfa-8KCThVdoHjx2LYEkAdI&export=download', 
     'chi_pop':'https://drive.google.com/uc?authuser=0&id=1PFXuuZBwOxMn2P-KVjdPOBslghoPOdGy&export=download', 
     'chi_doc_geom':'https://drive.google.com/uc?authuser=0&id=1rSuhCqCF64SVdoeiv8RbqGnJOg1Y8-rQ&export=download', 
     'chi_pop_geom':'https://drive.google.com/uc?authuser=0&id=1P83jZSzf3cGC0lTqfuhSFx4VlcLv0JJr&export=download', 
     'cook_county_hospitals_geom':'https://drive.google.com/uc?authuser=0&id=1hBXhC1kohwcxgw--iGSSQEcewTLMtB3p&export=download', 
     'cook_county_hospitals':'https://drive.google.com/uc?authuser=0&id=1GZj5Rtkcbyj83ZXLcsETzGNCV2RiVAcW&export=download', 
     'cook_county_tracts':'https://drive.google.com/uc?authuser=0&id=1GXStA35qG6odMJv8cGYlt-dDOQPEZB6t&export=download'}
    _datasets = {'chi_times':'chicago_metro_times.csv.bz2', 
     'chi_doc':'chicago_metro_docs_dentists.csv', 
     'chi_pop':'chicago_metro_pop.csv', 
     'chi_doc_geom':'chicago_metro_docs_dentists.geojson', 
     'chi_pop_geom':'chicago_metro_pop.geojson', 
     'chi_euclidean':'chicago_metro_euclidean_costs.csv.bz2', 
     'chi_euclidean_neighbors':'chicago_metro_euclidean_cost_neighbors.csv.bz2', 
     'cook_county_hospitals':'cook_county_hospitals.csv', 
     'cook_county_hospitals_geom':'hospitals_cookcty.geojson', 
     'cook_county_tracts':'cook_county_tracts.geojson'}

    @staticmethod
    def load_data(key):
        """
        Return path for available datasets.
        """
        if not os.path.exists(datasets._dir_path):
            os.mkdir(datasets._dir_path)
            print('Creating directory chi_med_data...')
        else:
            if key not in datasets._datasets.keys():
                print('{key} not an available dataset. Use datasets.available_datasets to see the available datasets.'.format(key=key))
            else:
                path = os.path.join(datasets._dir_path, datasets._datasets[key])
                if key in datasets._dwnld_data.keys():
                    if not os.path.exists(path):
                        print('Downloading {key} to {path}...'.format(key=key, path=(datasets._abs_path)))
                        req = requests.get(datasets._dwnld_data[key])
                        file_path = os.path.join(datasets._dir_path, datasets._datasets[key])
                        with open(file_path, 'wb') as (f):
                            f.write(req.content)
                        print('Download complete.')
                if '.geojson' in path:
                    import geopandas as gpd
                    return gpd.read_file(path)
                else:
                    return pd.read_csv(path)

    @staticmethod
    def available_datasets():
        desc = '\nchi_times: Cost matrix with travel times from each Chicago Census Tract to all others.\n\nchi_doc: Doctor and dentist counts for each Chicago Census Tract.\n\nchi_pop: Population counts for each Chicago Census Tract.\n\nchi_doc_geom: Doctor and dentist counts for each Chicago Census Tract along with geometric representations for Census Tracts.\n\nchi_pop_geom: Population counts for each Chicago Census Tract along with geometric representations for Census Tracts.\n\nchi_euclidean: Euclidean distance cost matrix with distances from each demand Chicago Census Tract to all others.\n\nchi_euclidean_neighbors: Euclidean distance cost matrix with distances from each supply Census Tract to all others.\n\ncook_county_hospitals: Contains data for each hospital location in Cook County including X Y coordinates.\n\ncook_county_hospitals_geom: Contains data for each hospital location in Cook County including X Y coordinates, and geometric points for each hospital.\n\ncook_county_tracts: Geometric representation of each Census Tract in Cook County.\n        '
        print(desc)
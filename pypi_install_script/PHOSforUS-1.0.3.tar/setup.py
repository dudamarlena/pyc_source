#!/usr/bin/env python

from distutils.core import setup

#### Descriptions

setup(name= "PHOSforUS", version = '1.0.3', 
description = "PHOSforUS horizontal information-based phosphorylation site predictor", 
url = "https://github.com/bxlab/PHOSforUS", 
author = "Min Hyung Cho", author_email = "mcho22@jhu.edu", license = "MIT", 
packages = ['phosforus', 'phosforus/accessory_modules'], 
package_dir = {'phosforus': 'phosforus', 'accessory_modules': 'phosforus/accessory_modules'}, 
package_data = {'phosforus': ['preset_indices/eScape_sorted_filled.csv', 'preset_indices/index_reselect.txt', 'preset_params/class_0/*.txt', 'preset_params/class_1/*.txt', 'preset_params/class_2/*.txt', 'preset_params/class_3/*.txt', 'preset_params/class_4/*.txt']}, 
keywords = ['phosphorylation', 'protein', 'predictor'])

# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/build_paths.py
# Compiled at: 2018-11-12 11:52:43
# Size of source mod 2**32: 5818 bytes
"""
Copyright (2017) Raydel Miranda 

This file is part of "Villa Flores product creator".

    "Villa Flores product creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "Villa Flores product creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "Villa Flores product creator".  If not, see <http://www.gnu.org/licenses/>.
"""
import itertools, glob, logging, os
from colorama import Fore, Style, init
import re
init()
logger = logging.getLogger('vf_productcreate')

def get_all_flowers(path_to_flowers, extension='png'):
    return glob.glob(('{}/**/*.{}'.format(os.path.abspath(path_to_flowers), extension)),
      recursive=True)


def get_all_backgrounds(path_to_backgrounds, extension='svg'):
    return glob.glob(('{}/**/*.{}'.format(os.path.abspath(path_to_backgrounds), extension)),
      recursive=True)


def get_all_bundles(path_to_bundles, extension='png'):
    return glob.glob(('{}/**/*.{}'.format(os.path.abspath(path_to_bundles), extension)),
      recursive=True)


def build_combinations(path_to_backgrounds, path_to_flowers=None, path_to_bundles=None, bundles_number=1):
    backgrounds = get_all_backgrounds(path_to_backgrounds)
    flowers = get_all_flowers(path_to_flowers) if path_to_flowers else []
    bundles = get_all_bundles(path_to_bundles)
    if len(bundles) < bundles_number:
        print(Fore.RED, 'You have bundles_number setting settled to {}, but have only {} bundles images.'.format(bundles_number, len(bundles)))
        print(Fore.RESET)
    if bundles:
        if flowers:
            img_permutations = itertools.product(backgrounds, flowers, list(itertools.permutations(bundles, int(bundles_number))))
        else:
            img_permutations = itertools.product(backgrounds, [None], list(itertools.permutations(bundles, int(bundles_number))))
        return list(img_permutations)
    else:
        if flowers:
            image_permutations = itertools.product(backgrounds, flowers, [None])
            return image_permutations
        return []


def compute_output(background, flower=None, bundles=[], extension='png', flower_code_pattern='.*', background_code_pattern='.*', bundle_code_pattern='.*'):
    if flower is not None:
        _, flower_name = os.path.split(flower)
        flower_name, _ = os.path.splitext(flower_name)
        flower_name = flower_name.split('_')[0]
        flower_match = re.match(flower_code_pattern, flower_name)
        if flower_match:
            flower_name = flower_match.group()
        else:
            flower_name = ''
            logger.warning(Fore.CYAN + 'Warning: pattern ' + Fore.YELLOW + flower_code_pattern + Fore.CYAN + 'do not match ' + Fore.GREEN + flower_name)
            logger.warning(Style.RESET_ALL)
    else:
        flower_name = ''
    _, background_name = os.path.split(background)
    background_name, _ = os.path.splitext(background_name)
    back_ground_match = re.match(background_code_pattern, background_name)
    if back_ground_match:
        background_name = back_ground_match.group()
    else:
        background_name = ''
        logger.warning(Fore.CYAN + 'Warning: pattern ' + Fore.YELLOW + background_code_pattern + Fore.CYAN + 'do not match ' + Fore.GREEN + background_name)
        logger.warning(Style.RESET_ALL)
    if bundles:
        bundles = [os.path.split(bundle_name)[1] for bundle_name in bundles]
        bundles = [os.path.splitext(bundle_name)[0] for bundle_name in bundles]
        bundles = [bundle_name.split('_')[0] for bundle_name in bundles]
    else:
        bundles = []
    _bundles = []
    for bundle in bundles:
        match = re.match(bundle_code_pattern, bundle)
        if match:
            _bundles.append(match.group())
        else:
            logger.warning(Fore.CYAN + 'Warning: pattern ' + Fore.YELLOW + bundle_code_pattern + Fore.CYAN + 'do not match ' + Fore.GREEN + bundle)
            logger.warning(Style.RESET_ALL)

    name_components = filter(lambda x: x != '', [
     flower_name, background_name, '_'.join(_bundles)])
    return (
     flower_name or background_name, '{}.{}'.format('_'.join(name_components), extension))
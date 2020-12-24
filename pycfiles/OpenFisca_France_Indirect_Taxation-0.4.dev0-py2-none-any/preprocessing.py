# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbenz/Dev/openfisca/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/param/preprocessing.py
# Compiled at: 2015-11-09 09:49:22
from openfisca_core import reforms

def preprocess_legislation(legislation_json):
    """
    Preprocess the legislation parameters to add prices and amounts from national accounts
    """
    import os, pkg_resources, pandas as pd
    default_config_files_directory = os.path.join(pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_annuel_carburants = pd.read_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets', 'prix_annuel_carburants.csv'), sep=';')
    prix_annuel_carburants['Date'] = prix_annuel_carburants['Date'].astype(int)
    prix_annuel_carburants = prix_annuel_carburants.set_index('Date')
    all_values = {}
    prix_carburants = {'@type': 'Node', 
       'description': 'prix des carburants en euros par hectolitre', 
       'children': {}}
    prix_annuel = prix_annuel_carburants['super_95_e10_ttc']
    all_values['super_95_e10_ttc'] = []
    for year in range(1990, 2009):
        values1 = dict()
        values1['start'] = ('{}-01-01').format(year)
        values1['stop'] = ('{}-12-31').format(year)
        values1['value'] = prix_annuel.loc[year] * 100
        all_values['super_95_e10_ttc'].append(values1)

    prix_annuel = prix_annuel_carburants['super_95_ttc']
    for year in range(2009, 2013):
        values2 = dict()
        values2['start'] = ('{}-01-01').format(year)
        values2['stop'] = ('{}-12-31').format(year)
        values2['value'] = prix_annuel.loc[year] * 100
        all_values['super_95_e10_ttc'].append(values2)

    prix_annuel = prix_annuel_carburants['super_95_e10_ttc']
    for year in range(2013, 2015):
        values3 = dict()
        values3['start'] = ('{}-01-01').format(year)
        values3['stop'] = ('{}-12-31').format(year)
        values3['value'] = prix_annuel.loc[year] * 100
        all_values['super_95_e10_ttc'].append(values3)

    prix_carburants['children']['super_95_e10_ttc'] = {'@type': 'Parameter', 
       'description': ('super_95_e10_ttc').replace('_', ' '), 
       'format': 'float', 
       'values': all_values['super_95_e10_ttc']}
    for element in ['diesel_ht', 'diesel_ttc', 'super_95_ht', 'super_95_ttc', 'super_98_ht', 'super_98_ttc',
     'super_95_e10_ht', 'gplc_ht', 'gplc_ttc', 'super_plombe_ht', 'super_plombe_ttc']:
        assert element in prix_annuel_carburants.columns
        prix_annuel = prix_annuel_carburants[element]
        all_values[element] = []
        for year in range(1990, 2015):
            values = dict()
            values['start'] = ('{}-01-01').format(year)
            values['stop'] = ('{}-12-31').format(year)
            values['value'] = prix_annuel.loc[year] * 100
            all_values[element].append(values)

        prix_carburants['children'][element] = {'@type': 'Parameter', 
           'description': element.replace('_', ' '), 
           'format': 'float', 
           'values': all_values[element]}

    legislation_json['children']['imposition_indirecte']['children']['prix_carburants'] = prix_carburants
    default_config_files_directory = os.path.join(pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parc_annuel_moyen_vp = pd.read_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets', 'parc_annuel_moyen_vp.csv'), sep=';')
    parc_annuel_moyen_vp = parc_annuel_moyen_vp.set_index('Unnamed: 0')
    values_parc = {}
    parc_vp = {'@type': 'Node', 
       'description': 'taille moyenne du parc automobile en France métropolitaine en milliers de véhicules', 
       'children': {}}
    for element in ['diesel', 'essence']:
        taille_parc = parc_annuel_moyen_vp[element]
        values_parc[element] = []
        for year in range(1990, 2014):
            values = dict()
            values['start'] = ('{}-01-01').format(year)
            values['stop'] = ('{}-12-31').format(year)
            values['value'] = taille_parc.loc[year]
            values_parc[element].append(values)

        parc_vp['children'][element] = {'@type': 'Parameter', 
           'description': 'nombre de véhicules particuliers immatriculés en France à motorisation ' + element, 
           'format': 'float', 
           'values': values_parc[element]}
        legislation_json['children']['imposition_indirecte']['children']['parc_vp'] = parc_vp

    default_config_files_directory = os.path.join(pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    quantite_carbu_vp_france = pd.read_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets', 'quantite_carbu_vp_france.csv'), sep=';')
    quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('Unnamed: 0')
    values_quantite = {}
    quantite_carbu_vp = {'@type': 'Node', 
       'description': 'quantite de carburants consommés en France métropolitaine', 
       'children': {}}
    for element in ['diesel', 'essence']:
        quantite_carburants = quantite_carbu_vp_france[element]
        values_quantite[element] = []
        for year in range(1990, 2014):
            values = dict()
            values['start'] = ('{}-01-01').format(year)
            values['stop'] = ('{}-12-31').format(year)
            values['value'] = quantite_carburants.loc[year]
            values_quantite[element].append(values)

        quantite_carbu_vp['children'][element] = {'@type': 'Parameter', 
           'description': 'consommation totale de ' + element + ' en France', 
           'format': 'float', 
           'values': values_quantite[element]}
        legislation_json['children']['imposition_indirecte']['children']['quantite_carbu_vp'] = quantite_carbu_vp

    default_config_files_directory = os.path.join(pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    part_des_types_de_supercarburants = pd.read_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets', 'part_des_types_de_supercarburants.csv'), sep=';')
    del part_des_types_de_supercarburants['Source']
    part_des_types_de_supercarburants = part_des_types_de_supercarburants[(part_des_types_de_supercarburants['annee'] > 0)].copy()
    part_des_types_de_supercarburants['annee'] = part_des_types_de_supercarburants['annee'].astype(int)
    part_des_types_de_supercarburants = part_des_types_de_supercarburants.set_index('annee')
    cols = part_des_types_de_supercarburants.columns
    for element in cols:
        part_des_types_de_supercarburants[element] = part_des_types_de_supercarburants[element] / (part_des_types_de_supercarburants['somme'] - part_des_types_de_supercarburants['sp_e85'])

    del part_des_types_de_supercarburants['sp_e85']
    del part_des_types_de_supercarburants['somme']
    cols = part_des_types_de_supercarburants.columns
    part_des_types_de_supercarburants['somme'] = 0
    for element in cols:
        part_des_types_de_supercarburants['somme'] += part_des_types_de_supercarburants[element]

    assert (part_des_types_de_supercarburants['somme'] == 1).any(), 'The weighting of the shares did not work'
    values_part_supercarburants = {}
    part_type_supercaburant = {'@type': 'Node', 
       'description': "part de la consommation totale d'essence de chaque type supercarburant", 
       'children': {}}
    for element in ['super_plombe', 'sp_95', 'sp_98', 'sp_e10']:
        part_par_carburant = part_des_types_de_supercarburants[element]
        values_part_supercarburants[element] = []
        for year in range(2000, 2015):
            values = dict()
            values['start'] = ('{}-01-01').format(year)
            values['stop'] = ('{}-12-31').format(year)
            values['value'] = part_par_carburant.loc[year]
            values_part_supercarburants[element].append(values)

        part_type_supercaburant['children'][element] = {'@type': 'Parameter', 
           'description': 'part de ' + element + " dans la consommation totale d'essences", 
           'format': 'float', 
           'values': values_part_supercarburants[element]}
        legislation_json['children']['imposition_indirecte']['children']['part_type_supercarburants'] = part_type_supercaburant

    alcool_conso_et_vin = {'@type': 'Node', 
       'description': 'alcools', 
       'children': {}}
    alcool_conso_et_vin['children']['vin'] = {'@type': 'Node', 
       'description': 'Pour calculer le taux de taxation implicite sur le vin', 
       'children': {'droit_cn_vin': {'@type': 'Parameter', 
                                     'description': 'Masse droit vin, vin mousseux, cidres et poirés selon comptabilité nationale', 
                                     'format': 'float', 
                                     'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 129}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 130}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 129}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 132}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 133}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 127}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 127}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 127}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 127}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 125}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 117}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 119}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 117}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 114}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 117}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 119}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 118}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 120}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 122}]}, 
                    'masse_conso_cn_vin': {'@type': 'Parameter', 
                                           'description': 'Masse consommation vin, vin mousseux, cidres et poirés selon comptabilité nationale', 
                                           'format': 'float', 
                                           'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 7191}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 7419}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 7636}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 8025}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 8451}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 8854}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 9168}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 9476}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 9695}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 9985}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 9933}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 10002}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 10345}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 10461}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 10728}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 11002}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 11387}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 11407}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 11515}]}}}
    alcool_conso_et_vin['children']['biere'] = {'@type': 'Node', 
       'description': 'Pour calculer le taux de taxation implicite sur la bière', 
       'children': {'droit_cn_biere': {'@type': 'Parameter', 
                                       'description': 'Masse droit biere selon comptabilité nationale', 
                                       'format': 'float', 
                                       'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 361}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 366}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 364}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 365}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 380}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 359}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 364}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 361}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 370}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 378}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 364}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 396}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 382}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 375}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 376}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 375}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 393}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 783}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 897}]}, 
                    'masse_conso_cn_biere': {'@type': 'Parameter', 
                                             'description': 'Masse consommation biere selon comptabilité nationale', 
                                             'format': 'float', 
                                             'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 2111}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 2144}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 2186}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 2291}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 2334}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 2290}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 2327}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 2405}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 2554}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 2484}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 2466}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 2486}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 2458}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 2287}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 2375}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 2461}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 2769}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 2868}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 3321}]}}}
    alcool_conso_et_vin['children']['alcools_forts'] = {'@type': 'Node', 
       'description': 'Pour calculer le taux de taxation implicite sur alcools forts', 
       'children': {'droit_cn_alcools': {'@type': 'Parameter', 
                                         'description': 'Masse droit alcool selon comptabilité nationale sans droits sur les produits intermediaires et cotisation spéciale alcool fort', 
                                         'format': 'float', 
                                         'values': [{'start': '2000-01-01', 'stop': '2000-12-31', 'value': 1872}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 1957}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 1932}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 1891}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 1908}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 1842}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 1954}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 1990}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 2005}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 2031}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 2111}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 2150}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 2225}]}, 
                    'droit_cn_alcools_total': {'@type': 'Parameter', 
                                               'description': 'Masse droit alcool selon comptabilité nationale avec les differents droits', 
                                               'format': 'float', 
                                               'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 2337}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 2350}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 2366}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 2369}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 2385}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 2416}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 2514}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 2503}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 2453}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 2409}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 2352}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 2477}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 2516}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 2528}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 2629}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 2734}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 3078}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 2718}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 3022}]}, 
                    'masse_conso_cn_alcools': {'@type': 'Parameter', 
                                               'description': 'Masse consommation alcool selon comptabilité nationale', 
                                               'format': 'float', 
                                               'values': [{'start': '1995-01-01', 'stop': '1995-12-31', 'value': 4893}, {'start': '1996-01-01', 'stop': '1996-12-31', 'value': 5075}, {'start': '1997-01-01', 'stop': '1997-12-31', 'value': 5065}, {'start': '1998-01-01', 'stop': '1998-12-31', 'value': 5123}, {'start': '1999-01-01', 'stop': '1999-12-31', 'value': 5234}, {'start': '2000-01-01', 'stop': '2000-12-31', 'value': 5558}, {'start': '2001-01-01', 'stop': '2001-12-31', 'value': 5721}, {'start': '2002-01-01', 'stop': '2002-12-31', 'value': 5932}, {'start': '2003-01-01', 'stop': '2003-12-31', 'value': 5895}, {'start': '2004-01-01', 'stop': '2004-12-31', 'value': 5967}, {'start': '2005-01-01', 'stop': '2005-12-31', 'value': 5960}, {'start': '2006-01-01', 'stop': '2006-12-31', 'value': 6106}, {'start': '2007-01-01', 'stop': '2007-12-31', 'value': 6142}, {'start': '2008-01-01', 'stop': '2008-12-31', 'value': 6147}, {'start': '2009-01-01', 'stop': '2009-12-31', 'value': 6342}, {'start': '2010-01-01', 'stop': '2010-12-31', 'value': 6618}, {'start': '2011-01-01', 'stop': '2011-12-31', 'value': 6680}, {'start': '2012-01-01', 'stop': '2012-12-31', 'value': 6996}, {'start': '2013-01-01', 'stop': '2013-12-31', 'value': 7022}]}}}
    legislation_json['children']['imposition_indirecte']['children']['alcool_conso_et_vin'] = alcool_conso_et_vin
    keys_ticpe = legislation_json['children']['imposition_indirecte']['children']['ticpe']['children'].keys()
    for element in keys_ticpe:
        get_values = legislation_json['children']['imposition_indirecte']['children']['ticpe']['children'][element]['values']
        for each_value in get_values:
            get_character = ('{}').format(each_value['start'])
            year = int(get_character[:4])
            if year < 2002:
                each_value['value'] = each_value['value'] / 6.55957
            else:
                each_value['value'] = each_value['value']

    return legislation_json
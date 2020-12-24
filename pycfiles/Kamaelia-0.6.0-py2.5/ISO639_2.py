# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Data/ISO639_2.py
# Compiled at: 2008-10-19 12:19:52
"""ISO 639-2 and 639-2T language code mappings
"""

def code2names(code):
    return mappings[code][:]


def code2name(code):
    return mappings[code][0]


def name2code(name):
    return reverse_mappings[name]


mappings = {'aar': [
         'Afar, afar'], 
   'abk': [
         'Abkhazian'], 
   'ace': [
         'Achinese'], 
   'ach': [
         'Acoli'], 
   'ada': [
         'Adangme'], 
   'ady': [
         'adyghé'], 
   'afa': [
         'Afro-Asiatic (Other)', 'afro-asiatiques, autres langues'], 
   'afh': [
         'Afrihili', 'afrihili'], 
   'afr': [
         'Afrikaans', 'afrikaans'], 
   'ain': [
         'Ainu', 'aïnou'], 
   'aka': [
         'Akan', 'akan'], 
   'akk': [
         'Akkadian', 'akkadien'], 
   'alb': [
         'Albania', 'albanais'], 
   'ale': [
         'Aleut', 'aléoute'], 
   'alg': [
         'Algonquian languages', 'algonquines, langues'], 
   'alt': [
         'Southern Altai', 'altaï du Sud'], 
   'amh': [
         'Amharic', 'amharique'], 
   'ang': [
         'English, Old (ca.450-1100)', 'anglo-saxon (ca.450-1100)'], 
   'anp': [
         'Angika', 'angika'], 
   'apa': [
         'Apache languages', 'apache'], 
   'ara': [
         'Arabic', 'arabe'], 
   'arc': [
         'Aramaic', 'araméen'], 
   'arg': [
         'Aragonese', 'aragonais'], 
   'arm': [
         'Armenian', 'arménien'], 
   'arn': [
         'Araucanian', 'araucan'], 
   'arp': [
         'Arapaho', 'arapaho'], 
   'art': [
         'Artificial (Other)', 'artificielles, autres langues'], 
   'arw': [
         'Arawak', 'arawak'], 
   'asm': [
         'Assamese', 'assamais'], 
   'ast': [
         'Asturian, Bable', 'asturien,  bable'], 
   'ath': [
         'Athapascan languages', 'athapascanes, langues'], 
   'aus': [
         'Australian languages', 'australiennes, langues'], 
   'ava': [
         'Avaric', 'avar'], 
   'ave': [
         'Avestan', 'avestique'], 
   'awa': [
         'Awadhi', 'awadhi'], 
   'aym': [
         'Aymara', 'aymara'], 
   'aze': [
         'Azerbaijani', 'azéri'], 
   'bad': [
         'Banda', 'banda'], 
   'bai': [
         'Bamileke languages', 'bamilékés, langues'], 
   'bak': [
         'Bashkir', 'bachkir'], 
   'bal': [
         'Baluchi', 'baloutchi'], 
   'bam': [
         'Bambara', 'bambara'], 
   'ban': [
         'Balinese', 'balinais'], 
   'baq': [
         'Basque', 'basque'], 
   'bas': [
         'Basa', 'basa'], 
   'bat': [
         'Baltic (Other)', 'baltiques, autres langues'], 
   'bej': [
         'Beja', 'bedja'], 
   'bel': [
         'Belarusian', 'biélorusse'], 
   'bem': [
         'Bemba', 'bemba'], 
   'ben': [
         'Bengali', 'bengali'], 
   'ber': [
         'Berber (Other)', 'berbères, autres langues'], 
   'bho': [
         'Bhojpuri', 'bhojpuri'], 
   'bih': [
         'Bihari', 'bihari'], 
   'bik': [
         'Bikol', 'bikol'], 
   'bin': [
         'Bini', 'bini'], 
   'bis': [
         'Bislama', 'bichlamar'], 
   'bla': [
         'Siksika', 'blackfoot'], 
   'bnt': [
         'Bantu (Other)', 'bantoues, autres langues'], 
   'bod': [
         'Tibetan', 'tibétain'], 
   'bos': [
         'Bosnian', 'bosniaque'], 
   'bra': [
         'Braj', 'braj'], 
   'bre': [
         'Breton', 'breton'], 
   'btk': [
         'Batak (Indonesia)', 'batak (Indonésie)'], 
   'bua': [
         'Buriat', 'bouriate'], 
   'bug': [
         'Buginese', 'bugi'], 
   'bul': [
         'Bulgarian', 'bulgare'], 
   'bur': [
         'Burmese', 'birman'], 
   'byn': [
         'Blin', 'Bilin'], 
   'cad': [
         'Caddo', 'caddo'], 
   'cai': [
         'Central American Indian (Other)',
         "indiennes d'Amérique centrale, autres langues"], 
   'car': [
         'Carib', 'caribe'], 
   'cat': [
         'Catalan', 'Valencian catalan', 'valencien'], 
   'cau': [
         'Caucasian (Other)', 'caucasiennes, autres langues'], 
   'ceb': [
         'Cebuano', 'cebuano'], 
   'cel': [
         'Celtic (Other)', 'celtiques, autres langues'], 
   'cha': [
         'Chamorro', 'chamorro'], 
   'chb': [
         'Chibcha', 'chibcha'], 
   'che': [
         'Chechen', 'tchétchène'], 
   'chg': [
         'Chagatai', 'djaghataï'], 
   'chi': [
         'Chinese', 'chinois'], 
   'chk': [
         'Chuukese', 'chuuk'], 
   'chm': [
         'Mari', 'mari'], 
   'chn': [
         'Chinook jargon', 'chinook, jargon'], 
   'cho': [
         'Choctaw', 'choctaw'], 
   'chp': [
         'Chipewyan', 'chipewyan'], 
   'chr': [
         'Cherokee', 'cherokee'], 
   'chu': [
         'Church Slavic',
         'Old Slavonic',
         'Church Slavonic',
         'Old Bulgarian',
         'Old Church Slavonic',
         "slavon d'église",
         'vieux slave',
         'slavon liturgique',
         'vieux bulgare'], 
   'chv': [
         'Chuvash', 'tchouvache'], 
   'chy': [
         'Cheyenne', 'cheyenne'], 
   'cmc': [
         'Chamic languages', 'chames, langues'], 
   'cop': [
         'Coptic', 'copte'], 
   'cor': [
         'Cornish', 'cornique'], 
   'cos': [
         'Corsican', 'corse'], 
   'cpe': [
         'Creoles and pidgins, English based (Other)',
         'créoles et pidgins anglais, autres'], 
   'cpf': [
         'Creoles and pidgins, French-based (Other)',
         'créoles et pidgins français, autres'], 
   'cpp': [
         'Creoles and pidgins, Portuguese-based (Other)',
         'créoles et pidgins portugais, autres'], 
   'cre': [
         'Cree', 'cree'], 
   'crh': [
         'Crimean Tatar', 'Crimean Turkish, tatar de Crimé'], 
   'crp': [
         'Creoles and pidgins (Other)', 'créoles et pidgins divers'], 
   'csb': [
         'Kashubian', 'kachoube'], 
   'cus': [
         "Cushitic (Other)' couchitiques, autres langues"], 
   'cym': [
         'Welsh', 'gallois'], 
   'cze': [
         'Czech', 'tchèque'], 
   'dak': [
         'Dakota', 'dakota'], 
   'dan': [
         'Danish', 'danois'], 
   'dar': [
         'Dargwa', 'dargwa'], 
   'day': [
         'Dayak', 'dayak'], 
   'del': [
         'Delaware', 'delaware'], 
   'den': [
         'Slave (Athapascan)', 'esclave (athapascan)'], 
   'deu': [
         'German', 'allemand'], 
   'dgr': [
         'Dogrib', 'dogrib'], 
   'din': [
         'Dinka', 'dinka'], 
   'div': [
         'Divehi', 'Dhivehi', 'Maldivian', 'maldivien'], 
   'doi': [
         'Dogri', 'dogri'], 
   'dra': [
         'Dravidian (Other)', 'dravidiennes, autres langues'], 
   'dsb': [
         'Lower Sorbian', 'bas-sorabe'], 
   'dua': [
         'Duala', 'douala'], 
   'dum': [
         'Dutch, Middle (ca.1050-1350)',
         'néerlandais moyen (ca. 1050-1350)'], 
   'dut': [
         'Dutch', 'Flemish', 'néerlandais', 'flamand'], 
   'dyu': [
         'Dyula', 'dioula'], 
   'dzo': [
         'Dzongkha', 'dzongkha'], 
   'efi': [
         'Efik', 'efik'], 
   'egy': [
         'Egyptian (Ancient)', 'égyptien'], 
   'eka': [
         'Ekajuk', 'ekajuk'], 
   'ell': [
         'Greek, Modern (1453-)', 'grec moderne (après 1453)'], 
   'elx': [
         'Elamite', 'élamite'], 
   'eng': [
         'English', 'anglais'], 
   'enm': [
         'English, Middle (1100-1500)', 'anglais moyen (1100-1500)'], 
   'epo': [
         'Esperanto', 'espéranto'], 
   'est': [
         'Estonian', 'estonien'], 
   'eus': [
         'Basque', 'basque'], 
   'ewe': [
         'Ewe', 'éwé'], 
   'ewo': [
         'Ewondo', 'éwondo'], 
   'fan': [
         'Fang', 'fang'], 
   'fao': [
         'Faroese', 'féroïen'], 
   'fas': [
         'Persian', 'persan'], 
   'fat': [
         'Fanti', 'fanti'], 
   'fij': [
         'Fijian', 'fidjien'], 
   'fil': [
         'Filipino', 'Pilipino', 'filipino', 'pilipino'], 
   'fin': [
         'Finnish', 'finnois'], 
   'fiu': [
         'Finno-Ugrian (Other)', 'finno-ougriennes, autres langues'], 
   'fon': [
         'Fon', 'fon'], 
   'fra': [
         'French', 'français'], 
   'fre': [
         'French', 'français'], 
   'frm': [
         'French, Middle (ca.1400-1600)', 'français moyen (1400-1600)'], 
   'fro': [
         'French, Old (842-ca.1400)', 'français ancien (842-ca.1400)'], 
   'frr': [
         'Northern Frisian', 'frison septentrional'], 
   'frs': [
         'Eastern Frisian', 'frison oriental'], 
   'fry': [
         'Western Frisian', 'frison occidental'], 
   'ful': [
         'Fulah', 'peul'], 
   'fur': [
         'Friulian', 'frioulan'], 
   'gaa': [
         'Ga', 'ga'], 
   'gay': [
         'Gayo', 'gayo'], 
   'gba': [
         'Gbaya', 'gbaya'], 
   'gem': [
         'Germanic (Other)', 'germaniques, autres langues'], 
   'geo': [
         'Georgian', 'géorgien'], 
   'ger': [
         'German', 'allemand'], 
   'gez': [
         'Geez', 'guèze'], 
   'gil': [
         'Gilbertese', 'kiribati'], 
   'gla': [
         'Gaelic',
         'Scottish Gaelic',
         'gaélique',
         'gaélique écossais'], 
   'gle': [
         'Irish', 'irlandais'], 
   'glg': [
         'Galician', 'galicien'], 
   'glv': [
         'Manx', 'manx', 'mannois'], 
   'gmh': [
         'German, Middle High (ca.1050-1500)',
         'allemand, moyen haut (ca. 1050-1500)'], 
   'goh': [
         'German, Old High (ca.750-1050)',
         'allemand, vieux haut (ca. 750-1050)'], 
   'gon': [
         'Gondi', 'gond'], 
   'gor': [
         'Gorontalo', 'gorontalo'], 
   'got': [
         'Gothic', 'gothique'], 
   'grb': [
         'Grebo', 'grebo'], 
   'grc': [
         'Greek, Ancient (to 1453)', "grec ancien (jusqu'à 1453)"], 
   'gre': [
         'Greek, Modern (1453-)', 'grec moderne (après 1453)'], 
   'grn': [
         'Guarani', 'guarani'], 
   'gsw': [
         'Alemanic', 'Swiss German', 'alémanique'], 
   'guj': [
         'Gujarati', 'goudjrati'], 
   'gwi': [
         'Gwich´in', 'gwich´in'], 
   'hai': [
         'Haida', 'haida'], 
   'hat': [
         'Haitian',
         'Haitian Creole',
         'haïtien',
         'créole haïtien'], 
   'hau': [
         'Hausa', 'haoussa'], 
   'haw': [
         'Hawaiian', 'hawaïen'], 
   'heb': [
         'Hebrew', 'hébreu'], 
   'her': [
         'Herero', 'herero'], 
   'hil': [
         'Hiligaynon', 'hiligaynon'], 
   'him': [
         'Himachali', 'himachali'], 
   'hin': [
         'Hindi', 'hindi'], 
   'hit': [
         'Hittite', 'hittite'], 
   'hmn': [
         'Hmong', 'hmong'], 
   'hmo': [
         'Hiri Motu', 'hiri motu'], 
   'hrv': [
         'Croatian', 'croate'], 
   'hsb': [
         'Upper Sorbian', 'haut-sorabe'], 
   'hun': [
         'Hungarian', 'hongrois'], 
   'hup': [
         'Hupa', 'hupa'], 
   'hye': [
         'Armenian', 'arménien'], 
   'iba': [
         'Iban', 'iban'], 
   'ibo': [
         'Igbo', 'igbo'], 
   'ice': [
         'Icelandic', 'islandais'], 
   'ido': [
         'Ido', 'ido'], 
   'iii': [
         'Sichuan Yi', 'yi de Sichuan'], 
   'ijo': [
         'Ijo', 'ijo'], 
   'iku': [
         'Inuktitut', 'inuktitut'], 
   'ile': [
         'Interlingue', 'interlingue'], 
   'ilo': [
         'Iloko', 'ilocano'], 
   'ina': [
         'Interlingua (International Auxiliary Language Association)',
         'interlingua (langue auxiliaire internationale)'], 
   'inc': [
         'Indic (Other)', 'indo-aryennes, autres langues'], 
   'ind': [
         'Indonesian', 'indonésien'], 
   'ine': [
         'Indo-European (Other)', 'indo-européennes, autres langues'], 
   'inh': [
         'Ingush', 'ingouche'], 
   'ipk': [
         'Inupiaq', 'inupiaq'], 
   'ira': [
         'Iranian (Other)', 'iraniennes, autres langues'], 
   'iro': [
         'Iroquoian languages', 'iroquoises, langues (famille)'], 
   'isl': [
         'Icelandic', 'islandais'], 
   'ita': [
         'Italian', 'italien'], 
   'jav': [
         'Javanese', 'javanais'], 
   'jbo': [
         'Lojban', 'lojban'], 
   'jpn': [
         'Japanese', 'japonais'], 
   'jpr': [
         'Judeo-Persian', 'judéo-persan'], 
   'jrb': [
         'Judeo-Arabic', 'judéo-arabe'], 
   'kaa': [
         'Kara-Kalpak', 'karakalpak'], 
   'kab': [
         'Kabyle', 'kabyle'], 
   'kac': [
         'Kachin', 'kachin'], 
   'kal': [
         'Kalaallisut', 'Greenlandic', 'groenlandais'], 
   'kam': [
         'Kamba', 'kamba'], 
   'kan': [
         'Kannada', 'kannada'], 
   'kar': [
         'Karen', 'karen'], 
   'kas': [
         'Kashmiri', 'kashmiri'], 
   'kat': [
         'Georgian', 'géorgien'], 
   'kau': [
         'Kanuri', 'kanouri'], 
   'kaw': [
         'Kawi', 'kawi'], 
   'kaz': [
         'Kazakh', 'kazakh'], 
   'kbd': [
         'Kabardian', 'kabardien'], 
   'kha': [
         'Khasi', 'khasi'], 
   'khi': [
         'Khoisan (Other)', 'khoisan, autres langues'], 
   'khm': [
         'Khmer', 'khmer'], 
   'kho': [
         'Khotanese', 'khotanais'], 
   'kik': [
         'Kikuyu', 'Gikuyu', 'kikuyu'], 
   'kin': [
         'Kinyarwanda', 'rwanda'], 
   'kir': [
         'Kirghiz', 'kirghize'], 
   'kmb': [
         'Kimbundu', 'kimbundu'], 
   'kok': [
         'Konkani', 'konkani'], 
   'kom': [
         'Komi', 'kom'], 
   'kon': [
         'Kongo', 'kongo'], 
   'kor': [
         'Korean', 'coréen'], 
   'kos': [
         'Kosraean', 'kosrae'], 
   'kpe': [
         'Kpelle', 'kpellé'], 
   'krc': [
         'Karachay-Balkar', 'karatchaï balkar'], 
   'krl': [
         'Karelian', 'carélien'], 
   'kro': [
         'Kru', 'krou'], 
   'kru': [
         'Kurukh', 'kurukh'], 
   'kua': [
         'Kuanyama', 'Kwanyama', 'kuanyama', 'kwanyama'], 
   'kum': [
         'Kumyk', 'koumyk'], 
   'kur': [
         'Kurdish', 'kurde'], 
   'kut': [
         'Kutenai', 'kutenai'], 
   'lad': [
         'Ladino', 'judéo-espagnol'], 
   'lah': [
         'Lahnda', 'lahnda'], 
   'lam': [
         'Lamba', 'lamba'], 
   'lao': [
         'Lao', 'lao'], 
   'lat': [
         'Latin', 'latin'], 
   'lav': [
         'Latvian', 'letton'], 
   'lez': [
         'Lezghian', 'lezghien'], 
   'lim': [
         'Limburgan', 'Limburger', 'Limburgish', 'limbourgeois'], 
   'lin': [
         'Lingala', 'lingala'], 
   'lit': [
         'Lithuanian', 'lituanien'], 
   'lol': [
         'Mongo', 'mongo'], 
   'loz': [
         'Lozi', 'lozi'], 
   'ltz': [
         'Luxembourgish', 'Letzeburgesch', 'luxembourgeois'], 
   'lua': [
         'Luba-Lulua', 'luba-lulua'], 
   'lub': [
         'Luba-Katanga', 'luba-katanga'], 
   'lug': [
         'Ganda', 'ganda'], 
   'lui': [
         'Luiseno', 'luiseno'], 
   'lun': [
         'Lunda', 'lunda'], 
   'luo': [
         'Luo (Kenya and Tanzania)', 'luo (Kenya et Tanzanie)'], 
   'lus': [
         'lushai', 'Lushai'], 
   'mac': [
         'Macedonian', 'macédonien'], 
   'mad': [
         'Madurese', 'madourais'], 
   'mag': [
         'Magahi', 'magahi'], 
   'mah': [
         'Marshallese', 'marshall'], 
   'mai': [
         'Maithili', 'maithili'], 
   'mak': [
         'Makasar', 'makassar'], 
   'mal': [
         'Malayalam', 'malayalam'], 
   'man': [
         'Mandingo', 'mandingue'], 
   'mao': [
         'Maori', 'maori'], 
   'map': [
         'Austronesian (Other)',
         'malayo-polynésiennes, autres langues'], 
   'mar': [
         'Marathi', 'marathe'], 
   'mas': [
         'Masai', 'massaï'], 
   'may': [
         'Malay', 'malais'], 
   'mdf': [
         'Moksha', 'moksa'], 
   'mdr': [
         'Mandar', 'mandar'], 
   'men': [
         'Mende', 'mendé'], 
   'mga': [
         'Irish, Middle (900-1200)', 'irlandais moyen (900-1200)'], 
   'mic': [
         "Mi'kmaq", 'Micmac', "mi'kmaq", 'micmac'], 
   'min': [
         'Minangkabau', 'minangkabau'], 
   'mis': [
         'Miscellaneous languages', 'diverses, langues'], 
   'mkd': [
         'Macedonian', 'macédonien'], 
   'mkh': [
         'Mon-Khmer (Other)', 'môn-khmer, autres langues'], 
   'mlg': [
         'Malagasy', 'malgache'], 
   'mlt': [
         'Maltese', 'maltais'], 
   'mnc': [
         'Manchu', 'mandchou'], 
   'mni': [
         'Manipuri', 'manipuri'], 
   'mno': [
         'Manobo languages', 'manobo, langues'], 
   'moh': [
         'Mohawk', 'mohawk'], 
   'mol': [
         'Moldavian', 'moldave'], 
   'mon': [
         'Mongolian', 'mongol'], 
   'mos': [
         'Mossi', 'moré'], 
   'mri': [
         'Maori', 'maori'], 
   'msa': [
         'Malay', 'malais'], 
   'mul': [
         'Multiple languages', 'multilingue'], 
   'mun': [
         'Munda languages', 'mounda, langues'], 
   'mus': [
         'Creek', 'muskogee'], 
   'mwl': [
         'Mirandese', 'mirandais'], 
   'mwr': [
         'Marwari', 'marvari'], 
   'mya': [
         'Burmese', 'birman'], 
   'myn': [
         'Mayan languages', 'maya, langues'], 
   'myv': [
         'Erzya', 'erza'], 
   'nah': [
         'Nahuatl', 'nahuatl'], 
   'nai': [
         'North American Indian',
         "indiennes d'Amérique du Nord, autres langues"], 
   'nap': [
         'Neapolitan', 'napolitain'], 
   'nau': [
         'Nauru', 'nauruan'], 
   'nav': [
         'Navajo', 'Navaho', 'navaho'], 
   'nbl': [
         'Ndebele, South',
         'South Ndebele',
         'ndébélé du Sud'], 
   'nde': [
         'Ndebele, North',
         'North Ndebele',
         'ndébélé du Nord'], 
   'ndo': [
         'Ndonga', 'ndonga'], 
   'nds': [
         'Low German',
         'Low Saxon',
         'German, Low',
         'Saxon, Low',
         'bas allemand',
         'bas saxon',
         'allemand, bas',
         'saxon, bas'], 
   'nep': [
         'Nepali', 'népalais'], 
   'new': [
         'Nepal Bhasa', 'Newari', 'nepal bhasa', 'newari'], 
   'nia': [
         'Nias', 'nias'], 
   'nic': [
         'Niger-Kordofanian (Other)',
         'nigéro-congolaises, autres langues'], 
   'niu': [
         'Niuean', 'niué'], 
   'nld': [
         'Dutch', 'Flemish, néerlandais', 'flamand'], 
   'nno': [
         'Norwegian Nynorsk', 'norvégien nynorsk'], 
   'nob': [
         'Norwegian Bokmål', 'norvégien bokmål'], 
   'nog': [
         'Nogai', 'nogaï', 'nogay'], 
   'non': [
         'Norse, Old', 'norrois, vieux'], 
   'nor': [
         'Norwegian', 'norvégien'], 
   'nqo': [
         "N'ko", "n'ko"], 
   'nso': [
         'Northern Sotho',
         'Pedi',
         'Sepedi',
         'sotho du Nord',
         'pedi',
         'sepedi'], 
   'nub': [
         'Nubian languages', 'nubiennes, langues'], 
   'nwc': [
         'Classical Newari',
         'Old Newari',
         'Classical Nepal Bhasa',
         'newari classique'], 
   'nya': [
         'Chichewa', 'Chewa', 'Nyanja', 'chichewa', 'chewa', 'nyanja'], 
   'nym': [
         'Nyamwezi', 'nyamwezi'], 
   'nyn': [
         'Nyankole', 'nyankolé'], 
   'nyo': [
         'Nyoro', 'nyoro'], 
   'nzi': [
         'Nzima', 'nzema'], 
   'oci': [
         'Occitan (post 1500)',
         'Provençal',
         'occitan (après 1500)',
         'provençal'], 
   'oji': [
         'Ojibwa', 'ojibwa'], 
   'ori': [
         'Oriya', 'oriya'], 
   'orm': [
         'Oromo', 'galla'], 
   'osa': [
         'Osage', 'osage'], 
   'oss': [
         'Ossetian', 'Ossetic', 'ossète'], 
   'ota': [
         'Turkish, Ottoman (1500-1928)', 'turc ottoman (1500-1928)'], 
   'oto': [
         'Otomian languages', 'otomangue, langues'], 
   'paa': [
         'Papuan (Other)', 'papoues, autres langues'], 
   'pag': [
         'Pangasinan', 'pangasinan'], 
   'pal': [
         'Pahlavi', 'pahlavi'], 
   'pam': [
         'Pampanga', 'pampangan'], 
   'pan': [
         'Panjabi', 'Punjabi', 'pendjabi'], 
   'pap': [
         'Papiamento', 'papiamento'], 
   'pau': [
         'Palauan', 'palau'], 
   'peo': [
         'Persian, Old (ca.600-400 B.C.)',
         'perse, vieux (ca. 600-400 av. J.-C.)'], 
   'per': [
         'Persian', 'persan'], 
   'phi': [
         'Philippine (Other)', 'philippines, autres langues'], 
   'phn': [
         'Phoenician', 'phénicien'], 
   'pli': [
         'Pali', 'pali'], 
   'pol': [
         'Polish', 'polonais'], 
   'pon': [
         'Pohnpeian', 'pohnpei'], 
   'por': [
         'Portuguese', 'portugais'], 
   'pra': [
         'Prakrit languages', 'prâkrit'], 
   'pro': [
         'Provençal, Old (to 1500)',
         "provençal ancien (jusqu'à 1500)"], 
   'pus': [
         'Pushto', 'pachto'], 
   'qaa-qtz': [
             'Reserved for local use',
             "réservée à l'usage local"], 
   'que': [
         'Quechua', 'quechua'], 
   'raj': [
         'Rajasthani', 'rajasthani'], 
   'rap': [
         'Rapanui', 'rapanui'], 
   'rar': [
         'Rarotongan', 'rarotonga'], 
   'roa': [
         'Romance (Other)', 'romanes, autres langues'], 
   'roh': [
         'Raeto-Romance', 'rhéto-roman'], 
   'rom': [
         'Romany', 'tsigane'], 
   'ron': [
         'Romanian', 'roumain'], 
   'run': [
         'Rundi', 'rundi'], 
   'rup': [
         'Aromanian',
         'Arumanian',
         'Macedo-Romanian',
         'aroumain',
         'macédo-roumain'], 
   'rus': [
         'Russian', 'russe'], 
   'sad': [
         'Sandawe', 'sandawe'], 
   'sag': [
         'Sango', 'sango'], 
   'sah': [
         'Yakut', 'iakoute'], 
   'sai': [
         'South American Indian (Other)',
         "indiennes d'Amérique du Sud, autres langues"], 
   'sal': [
         'Salishan languages', 'salish, langues'], 
   'sam': [
         'Samaritan Aramaic', 'samaritain'], 
   'san': [
         'Sanskrit', 'sanskrit'], 
   'sas': [
         'Sasak', 'sasak'], 
   'sat': [
         'Santali', 'santal'], 
   'scc': [
         'Serbian', 'serbe'], 
   'scn': [
         'Sicilian', 'sicilien'], 
   'sco': [
         'Scots', 'écossais'], 
   'scr': [
         'Croatian', 'croate'], 
   'sel': [
         'Selkup', 'selkoupe'], 
   'sem': [
         'Semitic (Other)', 'sémitiques, autres langues'], 
   'sga': [
         'Irish, Old (to 900)', "irlandais ancien (jusqu'à 900)"], 
   'sgn': [
         'Sign Languages', 'langues des signes'], 
   'shn': [
         'Shan', 'chan'], 
   'sid': [
         'Sidamo', 'sidamo'], 
   'sin': [
         'Sinhalese', 'Sinhala', 'singhalais'], 
   'sio': [
         'Siouan languages', 'sioux, langues'], 
   'sit': [
         'Sino-Tibetan (Other)', 'sino-tibétaines, autres langues'], 
   'sla': [
         'Slavic (Other)', 'slaves, autres langues'], 
   'slk': [
         'Slovak', 'slovaque'], 
   'slo': [
         'Slovak', 'slovaque'], 
   'slv': [
         'Slovenian', 'slovène'], 
   'sma': [
         'Southern Sami', 'sami du Sud'], 
   'sme': [
         'Northern Sami', 'sami du Nord'], 
   'smi': [
         'Sami languages (Other)', 'sami, autres langues'], 
   'smj': [
         'Lule Sami', 'sami de Lule'], 
   'smn': [
         'Inari Sami', "sami d'Inari"], 
   'smo': [
         'Samoan', 'samoan'], 
   'sms': [
         'Skolt Sami', 'sami skolt'], 
   'sna': [
         'Shona', 'shona'], 
   'snd': [
         'Sindhi', 'sindhi'], 
   'snk': [
         'Soninke', 'soninké'], 
   'sog': [
         'Sogdian', 'sogdien'], 
   'som': [
         'Somali', 'somali'], 
   'son': [
         'Songhai', 'songhai'], 
   'sot': [
         'Sotho, Southern', 'sotho du Sud'], 
   'spa': [
         'Spanish', 'Castilian', 'espagnol', 'castillan'], 
   'sqi': [
         'Albanian', 'albanais'], 
   'srd': [
         'Sardinian', 'sarde'], 
   'srn': [
         'Sranan Togo', 'sranan togo'], 
   'srp': [
         'Serbian', 'serbe'], 
   'srr': [
         'Serer', 'sérère'], 
   'ssa': [
         'Nilo-Saharan (Other)', 'nilo-sahariennes, autres langues'], 
   'ssw': [
         'Swati', 'swati'], 
   'suk': [
         'Sukuma', 'sukuma'], 
   'sun': [
         'Sundanese', 'soundanais'], 
   'sus': [
         'Susu', 'soussou'], 
   'sux': [
         'Sumerian', 'sumérien'], 
   'swa': [
         'Swahili', 'swahili'], 
   'swe': [
         'Swedish', 'suédois'], 
   'syr': [
         'Syriac', 'syriaque'], 
   'tah': [
         'Tahitian', 'tahitien'], 
   'tai': [
         'Tai (Other)', 'thaïes, autres langues'], 
   'tam': [
         'Tamil', 'tamoul'], 
   'tat': [
         'Tatar', 'tatar'], 
   'tel': [
         'Telugu', 'télougou'], 
   'tem': [
         'Timne', 'temne'], 
   'ter': [
         'Tereno', 'tereno'], 
   'tet': [
         'Tetum', 'tetum'], 
   'tgk': [
         'Tajik', 'tadjik'], 
   'tgl': [
         'Tagalog', 'tagalog'], 
   'tha': [
         'Thai', 'thaï'], 
   'tib': [
         'Tibetan', 'tibétain'], 
   'tig': [
         'Tigre', 'tigré'], 
   'tir': [
         'Tigrinya', 'tigrigna'], 
   'tiv': [
         'Tiv', 'tiv'], 
   'tkl': [
         'Tokelau', 'tokelau'], 
   'tlh': [
         'Klingon', 'tlhIngan-Hol', 'klingon'], 
   'tli': [
         'Tlingit', 'tlingit'], 
   'tmh': [
         'Tamashek', 'tamacheq'], 
   'tog': [
         'Tonga (Nyasa)', 'tonga (Nyasa)'], 
   'ton': [
         'Tonga (Tonga Islands)', 'tongan (Îles Tonga)'], 
   'tpi': [
         'Tok Pisin', 'tok pisin'], 
   'tsi': [
         'Tsimshian', 'tsimshian'], 
   'tsn': [
         'Tswana', 'tswana'], 
   'tso': [
         'Tsonga', 'tsonga'], 
   'tuk': [
         'Turkmen', 'turkmène'], 
   'tum': [
         'Tumbuka', 'tumbuka'], 
   'tup': [
         'Tupi languages', 'tupi, langues'], 
   'tur': [
         'Turkish', 'turc'], 
   'tut': [
         'Altaic (Other)', 'altaïques, autres langues'], 
   'tvl': [
         'Tuvalu', 'tuvalu'], 
   'twi': [
         'Twi', 'twi'], 
   'tyv': [
         'Tuvinian', 'touva'], 
   'udm': [
         'Udmurt', 'oudmourte'], 
   'uga': [
         'Ugaritic', 'ougaritique'], 
   'uig': [
         'Uighur', 'Uyghur', 'ouïgour'], 
   'ukr': [
         'Ukrainian', 'ukrainien'], 
   'umb': [
         'Umbundu', 'umbundu'], 
   'und': [
         'Undetermined', 'indéterminée'], 
   'urd': [
         'Urdu', 'ourdou'], 
   'uzb': [
         'Uzbek', 'ouszbek'], 
   'vai': [
         'Vai', 'vaï'], 
   'ven': [
         'Venda', 'venda'], 
   'vie': [
         'Vietnamese', 'vietnamien'], 
   'vol': [
         'Volapük', 'volapük'], 
   'vot': [
         'Votic', 'vote'], 
   'wak': [
         'Wakashan languages', 'wakashennes, langues'], 
   'wal': [
         'Walamo', 'walamo'], 
   'war': [
         'Waray', 'waray'], 
   'was': [
         'Washo', 'washo'], 
   'wel': [
         'Welsh', 'gallois'], 
   'wen': [
         'Sorbian languages', 'sorabes, langues'], 
   'wln': [
         'Walloon', 'wallon'], 
   'wol': [
         'Wolof', 'wolof'], 
   'xal': [
         'Kalmyk', 'Oirat', 'kalmouk', 'oïrat'], 
   'xho': [
         'Xhosa', 'xhosa'], 
   'yao': [
         'Yao', 'yao'], 
   'yap': [
         'Yapese', 'yapois'], 
   'yid': [
         'Yiddish', 'yiddish'], 
   'yor': [
         'Yoruba', 'yoruba'], 
   'ypk': [
         'Yupik languages', 'yupik, langues'], 
   'zap': [
         'Zapotec', 'zapotèque'], 
   'zen': [
         'Zenaga', 'zenaga'], 
   'zha': [
         'Zhuang', 'Chuang', 'zhuang', 'chuang'], 
   'zho': [
         'Chinese, chinois'], 
   'znd': [
         'Zande', 'zandé'], 
   'zul': [
         'Zulu', 'zoulou'], 
   'zun': [
         'Zuni', 'zuni'], 
   'zxx': [
         'No linguistic content', 'pas de contenu linguistique']}
reverse_mappings = {'abkhazian': 'abk', 
   'achinese': 'ace', 
   'acoli': 'ach', 
   'adangme': 'ada', 
   'adyghé': 'ady', 
   'afar, afar': 'aar', 
   'afrihili': 'afh', 
   'afrikaans': 'afr', 
   'afro-asiatic (other)': 'afa', 
   'afro-asiatiques, autres langues': 'afa', 
   'ainu': 'ain', 
   'akan': 'aka', 
   'akkadian': 'akk', 
   'akkadien': 'akk', 
   'albanais': 'sqi', 
   'albania': 'alb', 
   'albanian': 'sqi', 
   'alemanic': 'gsw', 
   'aleut': 'ale', 
   'algonquian languages': 'alg', 
   'algonquines, langues': 'alg', 
   'allemand': 'ger', 
   'allemand, bas': 'nds', 
   'allemand, moyen haut (ca. 1050-1500)': 'gmh', 
   'allemand, vieux haut (ca. 750-1050)': 'goh', 
   'altaic (other)': 'tut', 
   'altaï du sud': 'alt', 
   'altaïques, autres langues': 'tut', 
   'alémanique': 'gsw', 
   'aléoute': 'ale', 
   'amharic': 'amh', 
   'amharique': 'amh', 
   'angika': 'anp', 
   'anglais': 'eng', 
   'anglais moyen (1100-1500)': 'enm', 
   'anglo-saxon (ca.450-1100)': 'ang', 
   'apache': 'apa', 
   'apache languages': 'apa', 
   'arabe': 'ara', 
   'arabic': 'ara', 
   'aragonais': 'arg', 
   'aragonese': 'arg', 
   'aramaic': 'arc', 
   'araméen': 'arc', 
   'arapaho': 'arp', 
   'araucan': 'arn', 
   'araucanian': 'arn', 
   'arawak': 'arw', 
   'armenian': 'hye', 
   'arménien': 'hye', 
   'aromanian': 'rup', 
   'aroumain': 'rup', 
   'artificial (other)': 'art', 
   'artificielles, autres langues': 'art', 
   'arumanian': 'rup', 
   'assamais': 'asm', 
   'assamese': 'asm', 
   'asturian, bable': 'ast', 
   'asturien,  bable': 'ast', 
   'athapascan languages': 'ath', 
   'athapascanes, langues': 'ath', 
   'australian languages': 'aus', 
   'australiennes, langues': 'aus', 
   'austronesian (other)': 'map', 
   'avar': 'ava', 
   'avaric': 'ava', 
   'avestan': 'ave', 
   'avestique': 'ave', 
   'awadhi': 'awa', 
   'aymara': 'aym', 
   'azerbaijani': 'aze', 
   'azéri': 'aze', 
   'aïnou': 'ain', 
   'bachkir': 'bak', 
   'balinais': 'ban', 
   'balinese': 'ban', 
   'baloutchi': 'bal', 
   'baltic (other)': 'bat', 
   'baltiques, autres langues': 'bat', 
   'baluchi': 'bal', 
   'bambara': 'bam', 
   'bamileke languages': 'bai', 
   'bamilékés, langues': 'bai', 
   'banda': 'bad', 
   'bantoues, autres langues': 'bnt', 
   'bantu (other)': 'bnt', 
   'bas allemand': 'nds', 
   'bas saxon': 'nds', 
   'bas-sorabe': 'dsb', 
   'basa': 'bas', 
   'bashkir': 'bak', 
   'basque': 'eus', 
   'batak (indonesia)': 'btk', 
   'batak (indonésie)': 'btk', 
   'bedja': 'bej', 
   'beja': 'bej', 
   'belarusian': 'bel', 
   'bemba': 'bem', 
   'bengali': 'ben', 
   'berber (other)': 'ber', 
   'berbères, autres langues': 'ber', 
   'bhojpuri': 'bho', 
   'bichlamar': 'bis', 
   'bihari': 'bih', 
   'bikol': 'bik', 
   'bilin': 'byn', 
   'bini': 'bin', 
   'birman': 'mya', 
   'bislama': 'bis', 
   'biélorusse': 'bel', 
   'blackfoot': 'bla', 
   'blin': 'byn', 
   'bosnian': 'bos', 
   'bosniaque': 'bos', 
   'bouriate': 'bua', 
   'braj': 'bra', 
   'breton': 'bre', 
   'bugi': 'bug', 
   'buginese': 'bug', 
   'bulgare': 'bul', 
   'bulgarian': 'bul', 
   'buriat': 'bua', 
   'burmese': 'mya', 
   'caddo': 'cad', 
   'carib': 'car', 
   'caribe': 'car', 
   'carélien': 'krl', 
   'castilian': 'spa', 
   'castillan': 'spa', 
   'catalan': 'cat', 
   'caucasian (other)': 'cau', 
   'caucasiennes, autres langues': 'cau', 
   'cebuano': 'ceb', 
   'celtic (other)': 'cel', 
   'celtiques, autres langues': 'cel', 
   'central american indian (other)': 'cai', 
   'chagatai': 'chg', 
   'chames, langues': 'cmc', 
   'chamic languages': 'cmc', 
   'chamorro': 'cha', 
   'chan': 'shn', 
   'chechen': 'che', 
   'cherokee': 'chr', 
   'chewa': 'nya', 
   'cheyenne': 'chy', 
   'chibcha': 'chb', 
   'chichewa': 'nya', 
   'chinese': 'chi', 
   'chinese, chinois': 'zho', 
   'chinois': 'chi', 
   'chinook jargon': 'chn', 
   'chinook, jargon': 'chn', 
   'chipewyan': 'chp', 
   'choctaw': 'cho', 
   'chuang': 'zha', 
   'church slavic': 'chu', 
   'church slavonic': 'chu', 
   'chuuk': 'chk', 
   'chuukese': 'chk', 
   'chuvash': 'chv', 
   'classical nepal bhasa': 'nwc', 
   'classical newari': 'nwc', 
   'copte': 'cop', 
   'coptic': 'cop', 
   'cornique': 'cor', 
   'cornish': 'cor', 
   'corse': 'cos', 
   'corsican': 'cos', 
   'coréen': 'kor', 
   'cree': 'cre', 
   'creek': 'mus', 
   'creoles and pidgins (other)': 'crp', 
   'creoles and pidgins, english based (other)': 'cpe', 
   'creoles and pidgins, french-based (other)': 'cpf', 
   'creoles and pidgins, portuguese-based (other)': 'cpp', 
   'crimean tatar': 'crh', 
   'crimean turkish, tatar de crimé': 'crh', 
   'croate': 'scr', 
   'croatian': 'scr', 
   'créole haïtien': 'hat', 
   'créoles et pidgins anglais, autres': 'cpe', 
   'créoles et pidgins divers': 'crp', 
   'créoles et pidgins français, autres': 'cpf', 
   'créoles et pidgins portugais, autres': 'cpp', 
   "cushitic (other)' couchitiques, autres langues": 'cus', 
   'czech': 'cze', 
   'dakota': 'dak', 
   'danish': 'dan', 
   'danois': 'dan', 
   'dargwa': 'dar', 
   'dayak': 'day', 
   'delaware': 'del', 
   'dhivehi': 'div', 
   'dinka': 'din', 
   'dioula': 'dyu', 
   'divehi': 'div', 
   'diverses, langues': 'mis', 
   'djaghataï': 'chg', 
   'dogri': 'doi', 
   'dogrib': 'dgr', 
   'douala': 'dua', 
   'dravidian (other)': 'dra', 
   'dravidiennes, autres langues': 'dra', 
   'duala': 'dua', 
   'dutch': 'nld', 
   'dutch, middle (ca.1050-1350)': 'dum', 
   'dyula': 'dyu', 
   'dzongkha': 'dzo', 
   'eastern frisian': 'frs', 
   'efik': 'efi', 
   'egyptian (ancient)': 'egy', 
   'ekajuk': 'eka', 
   'elamite': 'elx', 
   'english': 'eng', 
   'english, middle (1100-1500)': 'enm', 
   'english, old (ca.450-1100)': 'ang', 
   'erza': 'myv', 
   'erzya': 'myv', 
   'esclave (athapascan)': 'den', 
   'espagnol': 'spa', 
   'esperanto': 'epo', 
   'espéranto': 'epo', 
   'estonian': 'est', 
   'estonien': 'est', 
   'ewe': 'ewe', 
   'ewondo': 'ewo', 
   'fang': 'fan', 
   'fanti': 'fat', 
   'faroese': 'fao', 
   'fidjien': 'fij', 
   'fijian': 'fij', 
   'filipino': 'fil', 
   'finnish': 'fin', 
   'finno-ougriennes, autres langues': 'fiu', 
   'finno-ugrian (other)': 'fiu', 
   'finnois': 'fin', 
   'flamand': 'nld', 
   'flemish': 'dut', 
   'flemish, néerlandais': 'nld', 
   'fon': 'fon', 
   'français': 'fre', 
   'français ancien (842-ca.1400)': 'fro', 
   'français moyen (1400-1600)': 'frm', 
   'french': 'fre', 
   'french, middle (ca.1400-1600)': 'frm', 
   'french, old (842-ca.1400)': 'fro', 
   'frioulan': 'fur', 
   'frison occidental': 'fry', 
   'frison oriental': 'frs', 
   'frison septentrional': 'frr', 
   'friulian': 'fur', 
   'fulah': 'ful', 
   'féroïen': 'fao', 
   'ga': 'gaa', 
   'gaelic': 'gla', 
   'galician': 'glg', 
   'galicien': 'glg', 
   'galla': 'orm', 
   'gallois': 'wel', 
   'ganda': 'lug', 
   'gayo': 'gay', 
   'gaélique': 'gla', 
   'gaélique écossais': 'gla', 
   'gbaya': 'gba', 
   'geez': 'gez', 
   'georgian': 'kat', 
   'german': 'ger', 
   'german, low': 'nds', 
   'german, middle high (ca.1050-1500)': 'gmh', 
   'german, old high (ca.750-1050)': 'goh', 
   'germanic (other)': 'gem', 
   'germaniques, autres langues': 'gem', 
   'gikuyu': 'kik', 
   'gilbertese': 'gil', 
   'gond': 'gon', 
   'gondi': 'gon', 
   'gorontalo': 'gor', 
   'gothic': 'got', 
   'gothique': 'got', 
   'goudjrati': 'guj', 
   'grebo': 'grb', 
   "grec ancien (jusqu'à 1453)": 'grc', 
   'grec moderne (après 1453)': 'gre', 
   'greek, ancient (to 1453)': 'grc', 
   'greek, modern (1453-)': 'gre', 
   'greenlandic': 'kal', 
   'groenlandais': 'kal', 
   'guarani': 'grn', 
   'gujarati': 'guj', 
   'guèze': 'gez', 
   'gwich´in': 'gwi', 
   'géorgien': 'kat', 
   'haida': 'hai', 
   'haitian': 'hat', 
   'haitian creole': 'hat', 
   'haoussa': 'hau', 
   'hausa': 'hau', 
   'haut-sorabe': 'hsb', 
   'hawaiian': 'haw', 
   'hawaïen': 'haw', 
   'haïtien': 'hat', 
   'hebrew': 'heb', 
   'herero': 'her', 
   'hiligaynon': 'hil', 
   'himachali': 'him', 
   'hindi': 'hin', 
   'hiri motu': 'hmo', 
   'hittite': 'hit', 
   'hmong': 'hmn', 
   'hongrois': 'hun', 
   'hungarian': 'hun', 
   'hupa': 'hup', 
   'hébreu': 'heb', 
   'iakoute': 'sah', 
   'iban': 'iba', 
   'icelandic': 'isl', 
   'ido': 'ido', 
   'igbo': 'ibo', 
   'ijo': 'ijo', 
   'ilocano': 'ilo', 
   'iloko': 'ilo', 
   'inari sami': 'smn', 
   'indic (other)': 'inc', 
   "indiennes d'amérique centrale, autres langues": 'cai', 
   "indiennes d'amérique du nord, autres langues": 'nai', 
   "indiennes d'amérique du sud, autres langues": 'sai', 
   'indo-aryennes, autres langues': 'inc', 
   'indo-european (other)': 'ine', 
   'indo-européennes, autres langues': 'ine', 
   'indonesian': 'ind', 
   'indonésien': 'ind', 
   'indéterminée': 'und', 
   'ingouche': 'inh', 
   'ingush': 'inh', 
   'interlingua (international auxiliary language association)': 'ina', 
   'interlingua (langue auxiliaire internationale)': 'ina', 
   'interlingue': 'ile', 
   'inuktitut': 'iku', 
   'inupiaq': 'ipk', 
   'iranian (other)': 'ira', 
   'iraniennes, autres langues': 'ira', 
   'irish': 'gle', 
   'irish, middle (900-1200)': 'mga', 
   'irish, old (to 900)': 'sga', 
   'irlandais': 'gle', 
   "irlandais ancien (jusqu'à 900)": 'sga', 
   'irlandais moyen (900-1200)': 'mga', 
   'iroquoian languages': 'iro', 
   'iroquoises, langues (famille)': 'iro', 
   'islandais': 'isl', 
   'italian': 'ita', 
   'italien': 'ita', 
   'japanese': 'jpn', 
   'japonais': 'jpn', 
   'javanais': 'jav', 
   'javanese': 'jav', 
   'judeo-arabic': 'jrb', 
   'judeo-persian': 'jpr', 
   'judéo-arabe': 'jrb', 
   'judéo-espagnol': 'lad', 
   'judéo-persan': 'jpr', 
   'kabardian': 'kbd', 
   'kabardien': 'kbd', 
   'kabyle': 'kab', 
   'kachin': 'kac', 
   'kachoube': 'csb', 
   'kalaallisut': 'kal', 
   'kalmouk': 'xal', 
   'kalmyk': 'xal', 
   'kamba': 'kam', 
   'kannada': 'kan', 
   'kanouri': 'kau', 
   'kanuri': 'kau', 
   'kara-kalpak': 'kaa', 
   'karachay-balkar': 'krc', 
   'karakalpak': 'kaa', 
   'karatchaï balkar': 'krc', 
   'karelian': 'krl', 
   'karen': 'kar', 
   'kashmiri': 'kas', 
   'kashubian': 'csb', 
   'kawi': 'kaw', 
   'kazakh': 'kaz', 
   'khasi': 'kha', 
   'khmer': 'khm', 
   'khoisan (other)': 'khi', 
   'khoisan, autres langues': 'khi', 
   'khotanais': 'kho', 
   'khotanese': 'kho', 
   'kikuyu': 'kik', 
   'kimbundu': 'kmb', 
   'kinyarwanda': 'kin', 
   'kirghiz': 'kir', 
   'kirghize': 'kir', 
   'kiribati': 'gil', 
   'klingon': 'tlh', 
   'kom': 'kom', 
   'komi': 'kom', 
   'kongo': 'kon', 
   'konkani': 'kok', 
   'korean': 'kor', 
   'kosrae': 'kos', 
   'kosraean': 'kos', 
   'koumyk': 'kum', 
   'kpelle': 'kpe', 
   'kpellé': 'kpe', 
   'krou': 'kro', 
   'kru': 'kro', 
   'kuanyama': 'kua', 
   'kumyk': 'kum', 
   'kurde': 'kur', 
   'kurdish': 'kur', 
   'kurukh': 'kru', 
   'kutenai': 'kut', 
   'kwanyama': 'kua', 
   'ladino': 'lad', 
   'lahnda': 'lah', 
   'lamba': 'lam', 
   'langues des signes': 'sgn', 
   'lao': 'lao', 
   'latin': 'lat', 
   'latvian': 'lav', 
   'letton': 'lav', 
   'letzeburgesch': 'ltz', 
   'lezghian': 'lez', 
   'lezghien': 'lez', 
   'limbourgeois': 'lim', 
   'limburgan': 'lim', 
   'limburger': 'lim', 
   'limburgish': 'lim', 
   'lingala': 'lin', 
   'lithuanian': 'lit', 
   'lituanien': 'lit', 
   'lojban': 'jbo', 
   'low german': 'nds', 
   'low saxon': 'nds', 
   'lower sorbian': 'dsb', 
   'lozi': 'loz', 
   'luba-katanga': 'lub', 
   'luba-lulua': 'lua', 
   'luiseno': 'lui', 
   'lule sami': 'smj', 
   'lunda': 'lun', 
   'luo (kenya and tanzania)': 'luo', 
   'luo (kenya et tanzanie)': 'luo', 
   'lushai': 'lus', 
   'luxembourgeois': 'ltz', 
   'luxembourgish': 'ltz', 
   'macedo-romanian': 'rup', 
   'macedonian': 'mkd', 
   'macédo-roumain': 'rup', 
   'macédonien': 'mkd', 
   'madourais': 'mad', 
   'madurese': 'mad', 
   'magahi': 'mag', 
   'maithili': 'mai', 
   'makasar': 'mak', 
   'makassar': 'mak', 
   'malagasy': 'mlg', 
   'malais': 'msa', 
   'malay': 'msa', 
   'malayalam': 'mal', 
   'malayo-polynésiennes, autres langues': 'map', 
   'maldivian': 'div', 
   'maldivien': 'div', 
   'malgache': 'mlg', 
   'maltais': 'mlt', 
   'maltese': 'mlt', 
   'manchu': 'mnc', 
   'mandar': 'mdr', 
   'mandchou': 'mnc', 
   'mandingo': 'man', 
   'mandingue': 'man', 
   'manipuri': 'mni', 
   'mannois': 'glv', 
   'manobo languages': 'mno', 
   'manobo, langues': 'mno', 
   'manx': 'glv', 
   'maori': 'mri', 
   'marathe': 'mar', 
   'marathi': 'mar', 
   'mari': 'chm', 
   'marshall': 'mah', 
   'marshallese': 'mah', 
   'marvari': 'mwr', 
   'marwari': 'mwr', 
   'masai': 'mas', 
   'massaï': 'mas', 
   'maya, langues': 'myn', 
   'mayan languages': 'myn', 
   'mende': 'men', 
   'mendé': 'men', 
   "mi'kmaq": 'mic', 
   'micmac': 'mic', 
   'minangkabau': 'min', 
   'mirandais': 'mwl', 
   'mirandese': 'mwl', 
   'miscellaneous languages': 'mis', 
   'mohawk': 'moh', 
   'moksa': 'mdf', 
   'moksha': 'mdf', 
   'moldave': 'mol', 
   'moldavian': 'mol', 
   'mon-khmer (other)': 'mkh', 
   'mongo': 'lol', 
   'mongol': 'mon', 
   'mongolian': 'mon', 
   'moré': 'mos', 
   'mossi': 'mos', 
   'mounda, langues': 'mun', 
   'multilingue': 'mul', 
   'multiple languages': 'mul', 
   'munda languages': 'mun', 
   'muskogee': 'mus', 
   'môn-khmer, autres langues': 'mkh', 
   "n'ko": 'nqo', 
   'nahuatl': 'nah', 
   'napolitain': 'nap', 
   'nauru': 'nau', 
   'nauruan': 'nau', 
   'navaho': 'nav', 
   'navajo': 'nav', 
   'ndebele, north': 'nde', 
   'ndebele, south': 'nbl', 
   'ndonga': 'ndo', 
   'ndébélé du nord': 'nde', 
   'ndébélé du sud': 'nbl', 
   'neapolitan': 'nap', 
   'nepal bhasa': 'new', 
   'nepali': 'nep', 
   'newari': 'new', 
   'newari classique': 'nwc', 
   'nias': 'nia', 
   'niger-kordofanian (other)': 'nic', 
   'nigéro-congolaises, autres langues': 'nic', 
   'nilo-saharan (other)': 'ssa', 
   'nilo-sahariennes, autres langues': 'ssa', 
   'niuean': 'niu', 
   'niué': 'niu', 
   'no linguistic content': 'zxx', 
   'nogai': 'nog', 
   'nogay': 'nog', 
   'nogaï': 'nog', 
   'norrois, vieux': 'non', 
   'norse, old': 'non', 
   'north american indian': 'nai', 
   'north ndebele': 'nde', 
   'northern frisian': 'frr', 
   'northern sami': 'sme', 
   'northern sotho': 'nso', 
   'norvégien': 'nor', 
   'norvégien bokmål': 'nob', 
   'norvégien nynorsk': 'nno', 
   'norwegian': 'nor', 
   'norwegian bokmål': 'nob', 
   'norwegian nynorsk': 'nno', 
   'nubian languages': 'nub', 
   'nubiennes, langues': 'nub', 
   'nyamwezi': 'nym', 
   'nyanja': 'nya', 
   'nyankole': 'nyn', 
   'nyankolé': 'nyn', 
   'nyoro': 'nyo', 
   'nzema': 'nzi', 
   'nzima': 'nzi', 
   'néerlandais': 'dut', 
   'néerlandais moyen (ca. 1050-1350)': 'dum', 
   'népalais': 'nep', 
   'occitan (après 1500)': 'oci', 
   'occitan (post 1500)': 'oci', 
   'oirat': 'xal', 
   'ojibwa': 'oji', 
   'old bulgarian': 'chu', 
   'old church slavonic': 'chu', 
   'old newari': 'nwc', 
   'old slavonic': 'chu', 
   'oriya': 'ori', 
   'oromo': 'orm', 
   'osage': 'osa', 
   'ossetian': 'oss', 
   'ossetic': 'oss', 
   'ossète': 'oss', 
   'otomangue, langues': 'oto', 
   'otomian languages': 'oto', 
   'oudmourte': 'udm', 
   'ougaritique': 'uga', 
   'ourdou': 'urd', 
   'ouszbek': 'uzb', 
   'ouïgour': 'uig', 
   'oïrat': 'xal', 
   'pachto': 'pus', 
   'pahlavi': 'pal', 
   'palau': 'pau', 
   'palauan': 'pau', 
   'pali': 'pli', 
   'pampanga': 'pam', 
   'pampangan': 'pam', 
   'pangasinan': 'pag', 
   'panjabi': 'pan', 
   'papiamento': 'pap', 
   'papoues, autres langues': 'paa', 
   'papuan (other)': 'paa', 
   'pas de contenu linguistique': 'zxx', 
   'pedi': 'nso', 
   'pendjabi': 'pan', 
   'persan': 'per', 
   'perse, vieux (ca. 600-400 av. j.-c.)': 'peo', 
   'persian': 'per', 
   'persian, old (ca.600-400 b.c.)': 'peo', 
   'peul': 'ful', 
   'philippine (other)': 'phi', 
   'philippines, autres langues': 'phi', 
   'phoenician': 'phn', 
   'phénicien': 'phn', 
   'pilipino': 'fil', 
   'pohnpei': 'pon', 
   'pohnpeian': 'pon', 
   'polish': 'pol', 
   'polonais': 'pol', 
   'portugais': 'por', 
   'portuguese': 'por', 
   'prakrit languages': 'pra', 
   'provençal': 'oci', 
   "provençal ancien (jusqu'à 1500)": 'pro', 
   'provençal, old (to 1500)': 'pro', 
   'prâkrit': 'pra', 
   'punjabi': 'pan', 
   'pushto': 'pus', 
   'quechua': 'que', 
   'raeto-romance': 'roh', 
   'rajasthani': 'raj', 
   'rapanui': 'rap', 
   'rarotonga': 'rar', 
   'rarotongan': 'rar', 
   'reserved for local use': 'qaa-qtz', 
   'rhéto-roman': 'roh', 
   'romance (other)': 'roa', 
   'romanes, autres langues': 'roa', 
   'romanian': 'ron', 
   'romany': 'rom', 
   'roumain': 'ron', 
   'rundi': 'run', 
   'russe': 'rus', 
   'russian': 'rus', 
   'rwanda': 'kin', 
   "réservée à l'usage local": 'qaa-qtz', 
   'salish, langues': 'sal', 
   'salishan languages': 'sal', 
   'samaritain': 'sam', 
   'samaritan aramaic': 'sam', 
   "sami d'inari": 'smn', 
   'sami de lule': 'smj', 
   'sami du nord': 'sme', 
   'sami du sud': 'sma', 
   'sami languages (other)': 'smi', 
   'sami skolt': 'sms', 
   'sami, autres langues': 'smi', 
   'samoan': 'smo', 
   'sandawe': 'sad', 
   'sango': 'sag', 
   'sanskrit': 'san', 
   'santal': 'sat', 
   'santali': 'sat', 
   'sarde': 'srd', 
   'sardinian': 'srd', 
   'sasak': 'sas', 
   'saxon, bas': 'nds', 
   'saxon, low': 'nds', 
   'scots': 'sco', 
   'scottish gaelic': 'gla', 
   'selkoupe': 'sel', 
   'selkup': 'sel', 
   'semitic (other)': 'sem', 
   'sepedi': 'nso', 
   'serbe': 'srp', 
   'serbian': 'srp', 
   'serer': 'srr', 
   'shan': 'shn', 
   'shona': 'sna', 
   'sichuan yi': 'iii', 
   'sicilian': 'scn', 
   'sicilien': 'scn', 
   'sidamo': 'sid', 
   'sign languages': 'sgn', 
   'siksika': 'bla', 
   'sindhi': 'snd', 
   'singhalais': 'sin', 
   'sinhala': 'sin', 
   'sinhalese': 'sin', 
   'sino-tibetan (other)': 'sit', 
   'sino-tibétaines, autres langues': 'sit', 
   'siouan languages': 'sio', 
   'sioux, langues': 'sio', 
   'skolt sami': 'sms', 
   'slave (athapascan)': 'den', 
   'slaves, autres langues': 'sla', 
   'slavic (other)': 'sla', 
   "slavon d'église": 'chu', 
   'slavon liturgique': 'chu', 
   'slovak': 'slo', 
   'slovaque': 'slo', 
   'slovenian': 'slv', 
   'slovène': 'slv', 
   'sogdian': 'sog', 
   'sogdien': 'sog', 
   'somali': 'som', 
   'songhai': 'son', 
   'soninke': 'snk', 
   'soninké': 'snk', 
   'sorabes, langues': 'wen', 
   'sorbian languages': 'wen', 
   'sotho du nord': 'nso', 
   'sotho du sud': 'sot', 
   'sotho, southern': 'sot', 
   'soundanais': 'sun', 
   'soussou': 'sus', 
   'south american indian (other)': 'sai', 
   'south ndebele': 'nbl', 
   'southern altai': 'alt', 
   'southern sami': 'sma', 
   'spanish': 'spa', 
   'sranan togo': 'srn', 
   'sukuma': 'suk', 
   'sumerian': 'sux', 
   'sumérien': 'sux', 
   'sundanese': 'sun', 
   'susu': 'sus', 
   'suédois': 'swe', 
   'swahili': 'swa', 
   'swati': 'ssw', 
   'swedish': 'swe', 
   'swiss german': 'gsw', 
   'syriac': 'syr', 
   'syriaque': 'syr', 
   'sémitiques, autres langues': 'sem', 
   'sérère': 'srr', 
   'tadjik': 'tgk', 
   'tagalog': 'tgl', 
   'tahitian': 'tah', 
   'tahitien': 'tah', 
   'tai (other)': 'tai', 
   'tajik': 'tgk', 
   'tamacheq': 'tmh', 
   'tamashek': 'tmh', 
   'tamil': 'tam', 
   'tamoul': 'tam', 
   'tatar': 'tat', 
   'tchouvache': 'chv', 
   'tchèque': 'cze', 
   'tchétchène': 'che', 
   'telugu': 'tel', 
   'temne': 'tem', 
   'tereno': 'ter', 
   'tetum': 'tet', 
   'thai': 'tha', 
   'thaï': 'tha', 
   'thaïes, autres langues': 'tai', 
   'tibetan': 'tib', 
   'tibétain': 'tib', 
   'tigre': 'tig', 
   'tigrigna': 'tir', 
   'tigrinya': 'tir', 
   'tigré': 'tig', 
   'timne': 'tem', 
   'tiv': 'tiv', 
   'tlhingan-hol': 'tlh', 
   'tlingit': 'tli', 
   'tok pisin': 'tpi', 
   'tokelau': 'tkl', 
   'tonga (nyasa)': 'tog', 
   'tonga (tonga islands)': 'ton', 
   'tongan (Îles tonga)': 'ton', 
   'touva': 'tyv', 
   'tsigane': 'rom', 
   'tsimshian': 'tsi', 
   'tsonga': 'tso', 
   'tswana': 'tsn', 
   'tumbuka': 'tum', 
   'tupi languages': 'tup', 
   'tupi, langues': 'tup', 
   'turc': 'tur', 
   'turc ottoman (1500-1928)': 'ota', 
   'turkish': 'tur', 
   'turkish, ottoman (1500-1928)': 'ota', 
   'turkmen': 'tuk', 
   'turkmène': 'tuk', 
   'tuvalu': 'tvl', 
   'tuvinian': 'tyv', 
   'twi': 'twi', 
   'télougou': 'tel', 
   'udmurt': 'udm', 
   'ugaritic': 'uga', 
   'uighur': 'uig', 
   'ukrainian': 'ukr', 
   'ukrainien': 'ukr', 
   'umbundu': 'umb', 
   'undetermined': 'und', 
   'upper sorbian': 'hsb', 
   'urdu': 'urd', 
   'uyghur': 'uig', 
   'uzbek': 'uzb', 
   'vai': 'vai', 
   'valencian catalan': 'cat', 
   'valencien': 'cat', 
   'vaï': 'vai', 
   'venda': 'ven', 
   'vietnamese': 'vie', 
   'vietnamien': 'vie', 
   'vieux bulgare': 'chu', 
   'vieux slave': 'chu', 
   'volapük': 'vol', 
   'vote': 'vot', 
   'votic': 'vot', 
   'wakashan languages': 'wak', 
   'wakashennes, langues': 'wak', 
   'walamo': 'wal', 
   'wallon': 'wln', 
   'walloon': 'wln', 
   'waray': 'war', 
   'washo': 'was', 
   'welsh': 'wel', 
   'western frisian': 'fry', 
   'wolof': 'wol', 
   'xhosa': 'xho', 
   'yakut': 'sah', 
   'yao': 'yao', 
   'yapese': 'yap', 
   'yapois': 'yap', 
   'yi de sichuan': 'iii', 
   'yiddish': 'yid', 
   'yoruba': 'yor', 
   'yupik languages': 'ypk', 
   'yupik, langues': 'ypk', 
   'zande': 'znd', 
   'zandé': 'znd', 
   'zapotec': 'zap', 
   'zapotèque': 'zap', 
   'zenaga': 'zen', 
   'zhuang': 'zha', 
   'zoulou': 'zul', 
   'zulu': 'zul', 
   'zuni': 'zun', 
   'écossais': 'sco', 
   'égyptien': 'egy', 
   'élamite': 'elx', 
   'éwondo': 'ewo', 
   'éwé': 'ewe'}
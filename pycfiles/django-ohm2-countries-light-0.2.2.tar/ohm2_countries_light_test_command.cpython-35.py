# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev-light/application/backend/apps/ohm2_countries_light/management/commands/ohm2_countries_light_test_command.py
# Compiled at: 2017-08-01 13:34:52
# Size of source mod 2**32: 4054 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from ohm2_countries_light import utils as ohm2_countries_light_utils
from ohm2_countries_light import settings
from collections import defaultdict
import os, pycountry

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
                files = defaultdict(dict)
                sizes = ["16", "24", "32", "48"]

                
                for c in pycountry.countries:

                        alpha_2 = c.alpha_2.lower()
                        name = c.name
                        
                        files[name] = defaultdict(dict)
                        for size in sizes:
                                files[name][size] = True

                        for size in sizes:
                                size_dst_path = os.path.join(settings.FLAGS_BASE_PATH, size, alpha_2 + ".png")  

                                files[name][size] &= os.path.isfile(size_dst_path)

                
                
                all_around = []
                not_around = []
                for country, sizes in files.items():
                        all_exist = True
                        for v in sizes.values():
                                all_exist &= v
                        

                        print(country, sizes)   

                        if all_exist:
                                all_around.append(country)
                        else:
                                not_around.append(country)

                print(sorted(all_around))
                """
        dst_path = os.path.join(settings.FLAGS_SMALL_BASE_PATH, 'cl.png')
        uploaded_image = h_utils.new_local_file(dst_path)
        processed_image = h_utils.process_uploaded_image_2(uploaded_image)
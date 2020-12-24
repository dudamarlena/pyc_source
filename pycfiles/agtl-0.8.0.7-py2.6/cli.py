# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/cli.py
# Compiled at: 2011-05-10 14:38:51
import geocaching, sys, geo, math, os
usage = 'Here\'s how to use this app:\n\nIf you want to use the gui:\n%(name)s --simple\n    Simple User Interface, for mobile devices such as the Openmoko Freerunner\n%(name)s --desktop\n    Full User Interface, for desktop usage (not implemented yet)\n\nIf you don\'t like your mouse:\n%(name)s update\n        Search and install a new listing parser.\n%(name)s set [options]\n        Change the configuration.\n%(name)s import [importactions]\n        Fetch geocaches from geocaching.com and write to the internal database.\n%(name)s import [importactions] do [actions]\n        Fetch geocaches from geocaching.com, put them into the internal database and do whatever actions are listed.\n%(name)s filter [filter-options] do [actions]\n        Query the internal database for geocaches and do the desired actions.\n%(name)s import [importactions] filter [filter-options] do [actions]\n        Import geocaches, put them into the internal database, filter the imported geocaches and run the actions.\n%(name)s sql "SELECT * FROM geocaches WHERE ... ORDER BY ... LIMIT ..." do [actions]\n        Select geocaches from local database and run the actions afterwards. Additional use of the filter is also supported. To get more information, run "%(name)s sql".\noptions:\n        --user(name) username\n        --pass(word) password\n                Your geocaching.com login data.\nimportactions:\n        --in coord1 coord2\n                Fetches the index of geocaches between the given coordinates.\n                These are interpreted as the corners of a rectangle. All caches\n                within the rectangle are retrieved. No details are retrieved.\n        --around coord radius-in-km\n                Fetches the index of geocaches at the given coordinate and radius\n                kilometers around it. No details are retrieved.\n        --at-route coord1 coord2 radius-in-km\n                Find caches along the route from coord1 to coord2. Uses OpenRouteService\n                and is not available for routes outside of europe.\n\nfilter-options:\n        --in coord1 coord2\n        --around coord1 radius-in-km\n                See import actions.\n        -f|--found\n        -F|--not-found\n                Filter out geocaches which have (not) been found by the user.\n        -w|--was-downloaded\n                caches which have full detail information available\n\n        -s|--size (min|max) 1..4|micro|small|regular|huge|other\n                Specify a minimum or maximum size. If min/max is not given, show\n                only geocaches with the given size.\n        -d|--difficulty (min|max) 1.0..5.0\n        -t|--terrain (min|max) 1.0..5.0\n                Filter out geocaches by difficulty or terrain.\n        -T|--type type,type,...\n         type: virtual|regular|unknown|multi|event\n                Only show geocaches of the given type(s)\n        -o|--owner owner-search-string\n        -n|--name name-search-string\n        -i|--id id-search-string\n                Search owner, name (title) or id of the geocaches.\n        --new\n                Caches which were downloaded in current session. Useful to\n                get alerted when new caches arrive.\nactions:\n        --print\n                Default action, prints tab-separated list of geocaches\n        --fetch-details\n                Downloads Descriptions etc. for selected geocaches\n        --export-html folder\n                Dumps HTML pages to given folder\n        --command command\n                Runs command if more than one geocache has survived the filtering.\n                The placeholder %%s is replaced by a shell-escaped list of geocaches.\n\n        Not implemented yet:\n        --export-gpx folder\n                Dumps geocaches into separate GPX files\n        --export-single-gpx file\n                Dumps selected geocaches into a single GPX file\n        --draw-map zoom file\n                Draws one big JPEG file with the positions of the selected geocaches\n        --draw-maps zoom folder [tiles]\n                Draws a small JPEG image for every geocache.\n\nPreferred format for coordinates:\n    \'N49 44.111 E6 29.123\'\n    or\n    \'N49.123456 E6.043212\'\n\nInstead of a coordinate, you may also query geonames.com for a place name.\nJust start the string with \'q:\':\n    q:London\n    \'q:Brisbane, Australia\'\n\n'

class ParseError(Exception):

    def __init__(self, errormsg, token=None):
        self.msg = errormsg
        self.token = token

    def __str__(self):
        return repr(self.msg)


class RunError(Exception):

    def __init__(self, errormsg):
        self.msg = errormsg

    def __str__(self):
        return repr(self.msg)


class Cli:
    USES = [
     'geonames']
    EQ = 0
    MIN = 1
    MAX = 2

    def __init__(self, core, dataroot):
        self.nt = 1
        self.core = core
        self.caches = None
        self.new_caches = []
        self.pointprovider = core.pointprovider
        core.connect('progress', lambda caller, fraction, text: self.show_progress(fraction, text))
        core.connect('hide-progress', lambda caller: self.show_done())
        core.connect('error', lambda caller, message: self.show_error(message))
        return

    def show(self):
        print '$ The command line interface is not fully implemented yet, feel'
        print '$ free to contribute at git://github.com/webhamster/advancedcaching.git'
        try:
            self.parse_input()
        except ParseError, e:
            if e.token == None:
                print "# Parse Error at token '%s': " % sys.argv[(self.nt - 1)]
            else:
                print "# Parse Error after Token '%s':" % sys.argv[e.token]
            print '# %s' % e.msg
        except RunError, e:
            print "# Execution Error at token '%s': " % sys.argv[(self.nt - 1)]
            print '# %s' % e.msg

        return

    def show_progress(self, fraction, text):
        print '$ %3d%% %s' % (fraction * 100, text)
        return False

    def show_done(self):
        print '$ done'
        return False

    def check_caches_retrieved(self):
        if self.caches == None:
            self.caches = self.pointprovider.get_all()
            print '* retrieved all caches (%d) from database' % len(self.caches)
        return

    def parse_input(self):
        while self.has_next():
            if sys.argv[self.nt] == 'set':
                self.parse_set()
            elif sys.argv[self.nt] == 'import':
                self.parse_import()
            elif sys.argv[self.nt] == 'sql':
                self.parse_sql()
            elif sys.argv[self.nt] == 'filter':
                self.parse_filter()
            elif sys.argv[self.nt] == 'do':
                self.parse_actions()
            elif sys.argv[self.nt] == 'update':
                self.perform_update()
            elif sys.argv[self.nt] == '-v':
                self.nt += 1
            else:
                raise ParseError("Expected 'import', 'sql', 'filter' or 'do'", self.nt - 1)

        self.core.on_destroy()

    def parse_set(self):
        self.nt += 1
        if not self.has_next():
            raise ParseError('Expected some options.')
        while self.has_next():
            token = sys.argv[self.nt]
            self.nt += 1
            if token == '--pass' or token == '--password':
                password = self.parse_string()
                self.set_password(password)
            elif token == '--user' or token == '--username':
                username = self.parse_string()
                self.set_username(username)
            else:
                raise ParseError("I don't understand '%s'" % token)

        print '* Finished setting options.'

    def parse_import(self):
        self.nt += 1
        if not self.has_next():
            raise ParseError('Expected import actions.')
        token = sys.argv[self.nt]
        self.nt += 1
        if token == '--in':
            coord1 = self.parse_coord()
            coord2 = self.parse_coord()
            self.import_points(coord1, coord2)
        elif token == '--around':
            coord1 = self.parse_coord()
            radius = self.parse_int()
            self.import_points(coord1, radius)
        elif token == '--at-route':
            coord1 = self.parse_coord()
            coord2 = self.parse_coord()
            radius = self.parse_int()
            self.import_points_route(coord1, coord2, radius)
        else:
            self.nt -= 1
            return

    def parse_sql(self):
        self.nt += 1
        if not self.has_next():
            print 'Table structure for geocaches:'
            info = self.pointprovider.get_table_info()
            for row in info:
                print ('\t').join([ str(x) for x in row ])

            print 'Example SQL-Query:'
            print "SELECT * FROM geocaches WHERE type = 'multi' AND name LIKE 'GC1X%' AND found = 0 ORDER BY title DESC LIMIT 5"
            raise ParseError('Expected sql string.')
        text = self.parse_string()
        self.caches = self.pointprovider.get_by_query(text)

    def parse_filter(self):
        self.check_caches_retrieved()
        self.nt += 1
        if not self.has_next():
            raise ParseError('Expected filter options.')
        while self.has_next():
            token = sys.argv[self.nt]
            self.nt += 1
            if token == '--in':
                coord1 = self.parse_coord()
                coord2 = self.parse_coord()
                self.add_filter_in(coord1, coord2)
            elif token == '--around':
                coord1 = self.parse_coord()
                radius = self.parse_int()
                self.add_filter_in(coord1, radius)
            elif token == '--found' or token == '-f':
                self.add_filter_found(True)
            elif token == '--not-found' or token == '-F':
                self.add_filter_found(False)
            elif token == '-w' or token == '--was-downloaded':
                self.add_filter_has_details(True)
            elif token == '-s' or token == '--size':
                op = self.parse_operator()
                size = self.parse_size()
                self.add_filter_size(op, size)
            elif token == '-d' or token == '--difficulty':
                op = self.parse_operator()
                diff = self.parse_decimal()
                self.add_filter_difficulty(op, diff)
            elif token == '-t' or token == '--terrain':
                op = self.parse_operator()
                terr = self.parse_decimal()
                self.add_filter_terrain(op, terr)
            elif token == '-T' or token == '--type':
                types = self.parse_types()
                self.add_filter_types(types)
            elif token == '-o' or token == '--owner':
                owner = self.parse_string()
                self.add_filter_owner(owner)
            elif token == '-n' or token == '--name':
                name = self.parse_string()
                self.add_filter_name(name)
            elif token == '-i' or token == '--id':
                id = self.parse_string()
                self.add_filter_id(id)
            elif token == '--new':
                self.caches = self.new_caches
            else:
                self.nt -= 1
                return

    def parse_actions(self):
        self.check_caches_retrieved()
        self.nt += 1
        if not self.has_next():
            raise ParseError('Expected actions.')
        while self.has_next():
            token = sys.argv[self.nt]
            self.nt += 1
            if token == '--print':
                self.action_print()
            elif token == '--fetch-details':
                self.action_fetch_details()
            elif token == '--export-html':
                folder = self.parse_string()
                self.action_export('html', folder)
            elif token == '--export-gpx':
                folder = self.parse_string()
                self.action_export('gpx', folder)
            elif token == '--export-single-gpx':
                raise ParseError('Exporting to a single gpx file is currently not supported, sorry.')
                filename = self.parse_string()
                self.action_export_single_gpx(filename)
            elif token == '--draw-map':
                zoom = self.parse_integer()
                filename = self.parse_string()
                self.action_draw_map(zoom, filename)
            elif token == '--draw-maps':
                zoom = self.parse_integer()
                folder = self.parse_string()
                self.action_draw_maps(zoom, folder)
            elif token == '--command':
                cmd = self.parse_string()
                self.action_command(cmd)
            else:
                raise ParseError('Unknown action: %s' % token)

    def perform_update(self):
        try:
            updated = self.core.try_update(False, True)
        except Exception, e:
            self.show_error(e)
        else:
            if updated > 0:
                print '$ Successfully updated %d module(s).' % updated
            else:
                print '$ No updates available.'

        self.nt += 1

    def show_error(self, message):
        print '# Failed: %s' % message

    def has_next(self):
        return self.nt < len(sys.argv)

    def parse_coord(self):
        if not self.has_next():
            raise ParseError('Expected Coordinate but there was none.', self.nt - 1)
        text = sys.argv[self.nt]
        self.nt += 1
        if text.startswith('q:'):
            query = text[2:]
            try:
                c = self.core.get_coord_by_name(query)
            except Exception, e:
                raise ParseError(e)

        else:
            try:
                c = geo.try_parse_coordinate(text)
            except Exception, e:
                raise ParseError(e)

        return c

    def parse_string(self):
        if not self.has_next():
            raise ParseError('Expected some Input, found nothing', self.nt - 1)
        text = sys.argv[self.nt]
        self.nt += 1
        return text.strip()

    def parse_int(self):
        if not self.has_next():
            raise ParseError('Expected a number, found nothing.', self.nt - 1)
        text = sys.argv[self.nt]
        self.nt += 1
        return int(text)

    def parse_size(self):
        if not self.has_next():
            raise ParseError('Expected a size (1..4/micro/small/regular/huge/other), found nothing.', self.nt - 1)
        text = sys.argv[self.nt].lower()
        self.nt += 1
        if text in ('1', '2', '3', '4', '5'):
            return int(text)
        if text == 'micro':
            return 1
        if text == 'small':
            return 2
        if text in ('normal', 'regular'):
            return 3
        if text in ('huge', 'big'):
            return 4
        if text == 'other':
            return 5
        raise ParseError('Unknown size: %s' % text)

    def parse_types(self):
        if not self.has_next():
            raise ParseError('Expected geocache type, found not even an electronic sausage.', self.nt - 1)
        text = sys.argv[self.nt].lower()
        self.nt += 1
        types = text.split(',')
        output = []
        for i in types:
            if i in geocaching.GeocacheCoordinate.TYPES:
                output.append(i)
            else:
                raise ParseError('Unknown Type: %s (expected one of: %s)' % (i, (', ').join(geocaching.GeocacheCoordinate.TYPES)))

        return output

    def parse_operator(self):
        text = sys.argv[self.nt]
        if text == 'min':
            self.nt += 1
            return self.MIN
        else:
            if text == 'max':
                self.nt += 1
                return self.MAX
            return self.EQ

    def parse_decimal(self):
        if not self.has_next():
            raise ParseError('Expected a number', self.nt - 1)
        text = sys.argv[self.nt]
        try:
            return 10 * float(text)
        except:
            raise ParseError("Could not parse '%s' as a valid number." % text)

    def set_username(self, string):
        new_settings = {'options_username': string}
        self.core.save_settings(new_settings, self)

    def set_password(self, string):
        new_settings = {'options_password': string}
        self.core.save_settings(new_settings, self)

    def import_points(self, c1, c2):
        if isinstance(c2, geo.Coordinate):
            print '* Downloading Caches between %s and %s' % (c1, c2)
            (self.caches, self.new_caches) = self.core.on_download((c1, c2))
        else:
            new_c1 = c1.transform(-45, c2 * 1000 * math.sqrt(2))
            new_c2 = c1.transform(135, c2 * 1000 * math.sqrt(2))
            print '* Downloading Caches in %d km distance to %s' % (c2, c1)
            print '* Approximation: Caches between %s and %s' % (new_c1, new_c2)
            (self.caches, self.new_caches) = self.core.on_download((new_c1, new_c2), sync=True)

    def import_points_route(self, c1, c2, r):
        print '* Querying OpenRouteService for route from startpoint to endpoint'
        points = self.core.get_route(c1, c2, r)
        print '* Found route, now retrieving partial cache overviews'
        for p in points:
            self.import_points(p[0], p[1])

        print '* Done.'

    def add_filter_in(self, coord1, coord2):
        if isinstance(coord2, geo.Coordinate):
            self.caches = filter(lambda x: self.filter_in(coord1, coord2, x), self.caches)
        else:
            self.caches = filter(lambda x: self.filter_in_radius(coord1, coord2, x), self.caches)
        print '* filter in radius/coordinates: %d left' % len(self.caches)

    def filter_in(self, c1, c2, check):
        return check.lat > min(c1.lat, c2.lat) and check.lat < max(c1.lat, c2.lat) and check.lon > min(c1.lon, c2.lon) and check.lon < max(c1.lon, c2.lon)

    def filter_in_radius(self, coord1, radius, check):
        return check.distance_to(coord1) <= radius * 1000

    def add_filter_found(self, found):
        self.caches = filter(lambda x: x.found == found, self.caches)
        print '* filter width found: %d left' % len(self.caches)

    def add_filter_has_details(self, has_details):
        self.caches = filter(lambda x: x.was_downloaded() == has_details, self.caches)
        print "* filter with 'has details': %d left" % len(self.caches)

    def add_filter_size(self, op, size):
        if op == self.EQ:
            self.caches = filter(lambda x: x.size == size, self.caches)
        elif op == self.MIN:
            self.caches = filter(lambda x: x.size >= size, self.caches)
        elif op == self.MAX:
            self.caches = filter(lambda x: x.size <= size, self.caches)
        else:
            raise RunError('What Happen? Somebody set us up the geocache.')
        print '* filter with size: %d left' % len(self.caches)

    def add_filter_difficulty(self, op, diff):
        if op == self.EQ:
            self.caches = filter(lambda x: x.diff == diff, self.caches)
        elif op == self.MIN:
            self.caches = filter(lambda x: x.diff >= diff, self.caches)
        elif op == self.MAX:
            self.caches = filter(lambda x: x.diff <= diff, self.caches)
        else:
            raise RunError('What Happen? Somebody set us up the geocache.')
        print '* filter with difficulty: %d left' % len(self.caches)

    def add_filter_terrain(self, op, terr):
        if op == self.EQ:
            self.caches = filter(lambda x: x.terr == terr, self.caches)
        elif op == self.MIN:
            self.caches = filter(lambda x: x.terr >= terr, self.caches)
        elif op == self.MAX:
            self.caches = filter(lambda x: x.terr <= terr, self.caches)
        else:
            raise RunError('What Happen? Somebody set us up the geocache.')
        print '* filter with terrain: %d left' % len(self.caches)

    def add_filter_types(self, types):
        self.caches = filter(lambda x: x.type in types, self.caches)
        print '* filter with types: %d left' % len(self.caches)

    def add_filter_owner(self, owner):
        self.caches = filter(lambda x: owner.lower() in x.owner.lower(), self.caches)
        print '* filter with owner: %d left' % len(self.caches)

    def add_filter_name(self, name):
        self.caches = filter(lambda x: name.lower() in x.title.lower(), self.caches)
        print '* filter with name: %d left' % len(self.caches)

    def add_filter_id(self, idstring):
        self.caches = filter(lambda x: idstring.lower() in x.name.lower(), self.caches)
        print '* filter with id: %d left' % len(self.caches)

    def action_print(self):
        print 'Found %d Caches:' % len(self.caches)
        for c in self.caches:
            print '%s\t%s (%s)' % (c.name, c.title, c.type)

    def action_fetch_details(self):
        i = 1
        for c in self.caches:
            print "* (%d of %d)\tDownloading '%s'" % (i, len(self.caches), c.title)
            self.core.on_download_cache(c, sync=True)
            i += 1

    def action_export(self, format, folder):
        i = 1
        for c in self.caches:
            print "* (%d of %d)\tExporting to %s: '%s'" % (i, len(self.caches), format, c.title)
            self.core.on_export_cache(c, format, folder)
            i += 1

    def action_command(self, commandline):
        import unicodedata
        if len(self.caches) == 0:
            print '* Not running command (no geocaches left)'
            return
        list = (' -- ').join([ '%s (%s)' % (a.title, a.type) for a in self.caches ])
        if not isinstance(list, str):
            list = unicodedata.normalize('NFKD', list).encode('ascii', 'ignore')
        os.system(commandline % ('"%s"' % list.encode('string-escape')))

    def set_download_progress(self, some, thing):
        pass

    def hide_progress(self):
        pass

    def show_error(self, message):
        raise RunError(message)
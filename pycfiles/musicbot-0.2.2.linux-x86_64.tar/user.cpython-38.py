# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/user.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 15279 bytes
import base64, json, logging, functools, click, click_spinner, requests
from tqdm import tqdm
from . import helpers
from .graphql import GraphQL
from .config import config
from .helpers import config_string
from .exceptions import FailedAuthentication
from .music import file, mfilter
logger = logging.getLogger(__name__)
DEFAULT_EMAIL = None
email_option = [click.option('--email', '-e', help='User email', default=DEFAULT_EMAIL, is_eager=True, callback=config_string)]
DEFAULT_PASSWORD = None
password_option = [click.option('--password', '-p', help='User password', default=DEFAULT_PASSWORD, is_eager=True, callback=config_string)]
DEFAULT_FIRST_NAME = None
first_name_option = [click.option('--first-name', help='User first name', default=DEFAULT_FIRST_NAME, is_eager=True, callback=config_string, show_default=True)]
DEFAULT_LAST_NAME = None
last_name_option = [click.option('--last-name', help='User last name', default=DEFAULT_FIRST_NAME, is_eager=True, callback=config_string, show_default=True)]
DEFAULT_GRAPHQL = 'http://127.0.0.1:5000/graphql'
graphql_option = [click.option('--graphql', help='GraphQL endpoint', default=DEFAULT_GRAPHQL, is_eager=True, callback=config_string, show_default=True)]

def sane_user(ctx, param, value):
    email = ctx.params['email']
    ctx.params.pop('email')
    password = ctx.params['password']
    ctx.params.pop('password')
    graphql = ctx.params['graphql']
    ctx.params.pop('graphql')
    token = value
    ctx.params['user'] = User(email=email,
      password=password,
      graphql=graphql,
      token=token)
    return ctx.params['user']


DEFAULT_TOKEN = None
token_option = [click.option('--token', '-t', help='User token', expose_value=False, callback=sane_user)]
register_options = email_option + password_option + first_name_option + last_name_option + graphql_option
login_options = email_option + password_option + graphql_option
auth_options = login_options + token_option

class User(GraphQL):

    @helpers.timeit
    def __init__(self, graphql=None, email=None, password=None, token=None):
        self.graphql = graphql if graphql is not None else DEFAULT_GRAPHQL
        self.email = email
        self.password = password
        self.token = token
        self.authenticated = False
        if self.token:
            logger.debug('using token : %s', self.token)
        else:
            if self.email and self.password:
                query = f'\n            mutation\n            {{\n                authenticate(input: {{email: "{self.email}", password: "{self.password}"}})\n                {{\n                    jwtToken\n                }}\n            }}'
                self.headers = None
                response = self._post(query, failure=(FailedAuthentication(f"Authentication failed for email {self.email}")))
                try:
                    self.token = response['data']['authenticate']['jwtToken']
                except KeyError:
                    raise FailedAuthentication(f"Invalid response received : {response}")
                else:
                    if not self.token:
                        raise FailedAuthentication(f"Invalid token received : {self.token}")
            else:
                raise FailedAuthentication('No credentials or token provided')
        self.authenticated = True
        GraphQL.__init__(self, graphql=graphql, headers={'Authorization': f"Bearer {self.token}"})

    @classmethod
    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def new(cls, **kwargs):
        self = User(**kwargs)
        return self

    @helpers.timeit
    def load_default_filters(self):
        query = '\n        mutation\n        {\n            default:           createFilter(input: {filter: {name: "default"                                                                           }}){clientMutationId}\n            no_artist_set:     createFilter(input: {filter: {name: "no artist set",     artists:    ""                                                 }}){clientMutationId}\n            no_album_set:      createFilter(input: {filter: {name: "no album set",      albums:     ""                                                 }}){clientMutationId}\n            no_title_set:      createFilter(input: {filter: {name: "no title set",      titles:     ""                                                 }}){clientMutationId}\n            no_genre_set:      createFilter(input: {filter: {name: "no genre set",      genres:     ""                                                 }}){clientMutationId}\n            youtube_not_found: createFilter(input: {filter: {name: "youtube not found", youtubes:   ["not found"]                                      }}){clientMutationId}\n            spotify_not_found: createFilter(input: {filter: {name: "spotify not found", spotifys:   ["not found"]                                      }}){clientMutationId}\n            no_youtube_links:  createFilter(input: {filter: {name: "no youtube links",  youtubes:   []                                                 }}){clientMutationId}\n            no_spotify_links:  createFilter(input: {filter: {name: "no spotify links",  spotifys:   ["not found"]                                      }}){clientMutationId}\n            no_rating:         createFilter(input: {filter: {name: "no rating",         minRating:  0.0, maxRating: 0.0                                }}){clientMutationId}\n            bests_40:          createFilter(input: {filter: {name: "best (4.0+)",       minRating:  4.0, noKeywords: ["cutoff", "bad", "demo", "intro"]}}){clientMutationId}\n            bests_45:          createFilter(input: {filter: {name: "best (4.5+)",       minRating:  4.5, noKeywords: ["cutoff", "bad", "demo", "intro"]}}){clientMutationId}\n            bests_50:          createFilter(input: {filter: {name: "best (5.0+)",       minRating:  5.0, noKeywords: ["cutoff", "bad", "demo", "intro"]}}){clientMutationId}\n            no_live:           createFilter(input: {filter: {name: "no live",           noKeywords: ["live"]                                           }}){clientMutationId}\n            only_live:         createFilter(input: {filter: {name: "only live",         keywords:   ["live"]                                           }}){clientMutationId}\n        }'
        return self._post(query)

    @helpers.timeit
    def playlist(self, mf=None):
        mf = mf if mf is not None else mfilter.Filter()
        query = f"\n        {{\n            playlist({mf.to_graphql()})\n        }}"
        return self._post(query)['data']['playlist']

    @helpers.timeit
    def bests(self, mf=None):
        mf = mf if mf is not None else mfilter.Filter()
        query = f"\n        {{\n            bests({mf.to_graphql()})\n            {{\n                nodes\n                {{\n                    name,\n                    content\n                }}\n            }}\n        }}"
        return self._post(query)['data']['bests']['nodes']

    @helpers.timeit
    def do_filter(self, mf=None):
        mf = mf if mf is not None else mfilter.Filter()
        if mf.name:
            kwargs = self.filter(mf.name)
            print(kwargs)
            mf = (mfilter.Filter)(**kwargs)
        query = f"\n        {{\n            doFilter({mf.to_graphql()})\n            {{\n                nodes\n                {{\n                    title,\n                    album,\n                    genre,\n                    artist,\n                    folder,\n                    youtube,\n                    spotify,\n                    number,\n                    path,\n                    rating,\n                    duration,\n                    size,\n                    keywords\n                }}\n            }}\n        }}"
        return self._post(query)['data']['doFilter']['nodes']

    @helpers.timeit
    def do_stat(self, mf=None):
        mf = mf if mf is not None else mfilter.Filter()
        query = f"\n        {{\n            doStat({mf.to_graphql()})\n            {{\n              musics,\n              artists,\n              albums,\n              genres,\n              keywords,\n              size,\n              duration\n            }}\n        }}"
        return self._post(query)['data']['doStat']

    @helpers.timeit
    def upsert_music(self, music):
        query = f"\n        mutation\n        {{\n            upsertMusic(input: {{{music.to_graphql()}}})\n            {{\n                clientMutationId\n            }}\n        }}"
        return self._post(query)

    @helpers.timeit
    def bulk_insert--- This code section failed: ---

 L. 216         0  LOAD_FAST                'musics'
                2  POP_JUMP_IF_TRUE     18  'to 18'

 L. 217         4  LOAD_GLOBAL              logger
                6  LOAD_METHOD              info
                8  LOAD_STR                 'no musics to insert'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L. 218        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM             2  '2'

 L. 219        18  LOAD_GLOBAL              config
               20  LOAD_ATTR                debug
               22  POP_JUMP_IF_FALSE    98  'to 98'

 L. 220        24  LOAD_GLOBAL              tqdm
               26  LOAD_GLOBAL              len
               28  LOAD_FAST                'musics'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_STR                 'inserting music one by one'
               34  LOAD_CONST               ('total', 'desc')
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  SETUP_WITH           88  'to 88'
               40  STORE_FAST               'pbar'

 L. 221        42  LOAD_FAST                'musics'
               44  GET_ITER         
               46  FOR_ITER             84  'to 84'
               48  STORE_FAST               'music'

 L. 222        50  LOAD_GLOBAL              logger
               52  LOAD_METHOD              debug
               54  LOAD_STR                 'inserting %s'
               56  LOAD_FAST                'music'
               58  CALL_METHOD_2         2  ''
               60  POP_TOP          

 L. 223        62  LOAD_FAST                'self'
               64  LOAD_METHOD              upsert_music
               66  LOAD_FAST                'music'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 224        72  LOAD_FAST                'pbar'
               74  LOAD_METHOD              update
               76  LOAD_CONST               1
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_BACK            46  'to 46'
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_WITH       38  '38'
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

 L. 225        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            22  '22'

 L. 227        98  LOAD_GLOBAL              json
              100  LOAD_METHOD              dumps
              102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'User.bulk_insert.<locals>.<listcomp>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  LOAD_FAST                'musics'
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'j'

 L. 228       118  LOAD_FAST                'j'
              120  LOAD_METHOD              encode
              122  LOAD_STR                 'utf-8'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'b64'

 L. 229       128  LOAD_GLOBAL              base64
              130  LOAD_METHOD              b64encode
              132  LOAD_FAST                'b64'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'data'

 L. 230       138  LOAD_STR                 '\n        mutation\n        {\n            bulkInsert(input: {data: "'

 L. 233       140  LOAD_FAST                'data'
              142  LOAD_METHOD              decode
              144  CALL_METHOD_0         0  ''

 L. 230       146  FORMAT_VALUE          0  ''
              148  LOAD_STR                 '"})\n            {\n                clientMutationId\n            }\n        }'
              150  BUILD_STRING_3        3 
              152  STORE_FAST               'query'

 L. 238       154  LOAD_GLOBAL              click_spinner
              156  LOAD_ATTR                spinner
              158  LOAD_GLOBAL              config
              160  LOAD_ATTR                quiet
              162  LOAD_CONST               ('disable',)
              164  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              166  SETUP_WITH          192  'to 192'
              168  POP_TOP          

 L. 239       170  LOAD_FAST                'self'
              172  LOAD_METHOD              _post
              174  LOAD_FAST                'query'
              176  CALL_METHOD_1         1  ''
              178  POP_BLOCK        
              180  ROT_TWO          
              182  BEGIN_FINALLY    
              184  WITH_CLEANUP_START
              186  WITH_CLEANUP_FINISH
              188  POP_FINALLY           0  ''
              190  RETURN_VALUE     
            192_0  COME_FROM_WITH      166  '166'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 180

    @property
    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def folders(self):
        query = '\n        {\n            foldersList\n        }'
        return self._post(query)['data']['foldersList']

    @property
    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def artists(self):
        query = '\n        {\n          artistsTreeList {\n            name\n            albums {\n              name\n              musics {\n                folder\n                name\n                path\n              }\n            }\n          }\n        }'
        return self._post(query)['data']['artistsTreeList']

    @property
    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def genres(self):
        query = '\n        {\n          genresTreeList {\n            name\n          }\n        }'
        return self._post(query)['data']['genresTreeList']

    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def filter(self, name):
        default_filter = mfilter.Filter()
        filter_members = ','.join(default_filter.ordered_dict().keys())
        query = f'\n        {{\n            filtersList(filter: {{name: {{equalTo: "{name}"}}}})\n            {{\n                name,\n                {filter_members}\n            }}\n        }}'
        return self._post(query)['data']['filtersList'][0]

    @property
    @functools.lru_cache(maxsize=None)
    @helpers.timeit
    def filters(self):
        default_filter = mfilter.Filter()
        filter_members = ','.join(default_filter.ordered_dict().keys())
        query = f"\n        {{\n            filtersList\n            {{\n                name,\n                {filter_members}\n            }}\n        }}"
        return self._post(query)['data']['filtersList']

    def watch(self):
        from watchdog.observers import Observer
        from watchdog.events import PatternMatchingEventHandler
        import time

        class MusicWatcherHandler(PatternMatchingEventHandler):
            patterns = []

            def __init__(self, user):
                super().__init__()
                self.user = user
                MusicWatcherHandler.patterns = ['*.' + f for f in file.supported_formats]

            def on_modified(self, event):
                self.update_music(event.src_path)

            def on_created(self, event):
                self.update_music(event.src_path)

            def on_deleted(self, event):
                logger.debug('Deleting entry in DB for: %s %s', event.src_path, event.event_type)
                self.user.delete_music(event.src_path)

            def on_moved(self, event):
                logger.debug('Moving entry in DB for: %s %s', event.src_path, event.event_type)
                self.user.delete_music(event.src_path)
                self.update_music(event.dest_path)

            def update_music(self, path):
                for folder in self.user.folders:
                    if path.startswith(folder) and path.endswith(tuple(file.supported_formats)):
                        logger.debug('Creating/modifying DB for: %s', path)
                        f = file.File(path, folder)
                        self.user.upsert_music(f)
                        return None

        logger.info('Watching: %s', self.folders)
        event_handler = MusicWatcherHandler(self)
        observer = Observer()
        for f in self.folders:
            observer.schedule(event_handler, f, recursive=True)
        else:
            observer.start()
            try:
                while True:
                    time.sleep(50)

            except KeyboardInterrupt:
                observer.stop()
            else:
                observer.join()

    @classmethod
    @helpers.timeit
    def register(cls, graphql=None, first_name=None, last_name=None, email=None, password=None):
        first_name = first_name if first_name is not None else DEFAULT_FIRST_NAME
        last_name = last_name if last_name is not None else DEFAULT_LAST_NAME
        email = email if email is not None else DEFAULT_EMAIL
        password = password if password is not None else DEFAULT_PASSWORD
        if email is None:
            raise click.BadParameter('Missing value for email')
        if password is None:
            raise click.BadParameter('Missing value for password')
        query = f'\n        mutation\n        {{\n            registerUser(input: {{firstName: "{first_name}", lastName: "{last_name}", email: "{email}", password: "{password}"}})\n            {{\n                clientMutationId\n            }}\n        }}'
        logger.debug(query)
        response = requests.post(graphql, json={'query': query})
        json_response = response.json()
        logger.debug(json_response)
        if response.status_code != 200:
            raise FailedAuthentication(f"Cannot create user: {email}")
        if 'errors' in json_response:
            if json_response['errors']:
                errors = [e['message'] for e in json_response['errors']]
                raise FailedAuthentication(f"Cannot create user: {errors}")
        return User(graphql, email, password)

    @helpers.timeit
    def unregister(self):
        query = '\n        mutation\n        {\n            unregisterUser(input: {})\n            {\n                clientMutationId\n            }\n        }'
        result = self._post(query, failure=(FailedAuthentication(f"Cannot delete user {self.email}")))
        self.authenticated = False
        return result

    @helpers.timeit
    def delete_music(self, path):
        query = f'\n        mutation\n        {{\n            deleteMusic(input: {{path: "{path}"}})\n            {{\n                clientMutationId\n            }}\n        }}'
        return self._post(query)

    @helpers.timeit
    def clean_musics(self):
        query = '\n        mutation\n        {\n            deleteAllMusic(input: {})\n            {\n                clientMutationId\n            }\n        }'
        return self._post(query)
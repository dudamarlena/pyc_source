# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/fixtures.py
# Compiled at: 2013-04-11 17:47:52
import datetime, StringIO, os

def load_movie_fixtures():
    from camelot.model.fixture import Fixture
    from camelot.model.party import Person
    from camelot_example.model import Movie, VisitorReport
    from camelot.core.files.storage import Storage, StoredImage
    from camelot.core.resources import resource_filename
    storage = Storage(upload_to='covers', stored_file_implementation=StoredImage)
    movies = [
     [
      'The Shining',
      'The tide of terror that swept America is here.',
      datetime.date(1980, 5, 23),
      ('Stanley', 'Kubrick'),
      [
       'Jack Nicholson',
       'Shelley Duvall',
       'Danny Lloyd',
       'Scatman Crothers',
       'Barry Nelson'],
      [
       'Horror', 'Mystery', 'Thriller'],
      'thriller',
      4,
      'shining.png',
      'A family heads to an isolated hotel for the winter where an evil and spiritual presence influences the father into violence, while his psychic son sees horrific forebodings from the past and of the future.'],
     [
      'The Bourne Identity',
      'Matt Damon is Jason Bourne.',
      datetime.date(2002, 6, 14),
      ('Doug', 'Liman'),
      [
       'Matt Damon',
       'Franka Potente',
       'Chris Cooper',
       'Clive Owen',
       'Brian Cox'],
      [
       'Action', 'Adventure'],
      'action',
      4,
      'bourne.png',
      'A man is picked up by a fishing boat, bullet-riddled and without memory, then races to elude assassins and recover from amnesia.'],
     [
      'Casino Royale',
      'Discover how James became Bond.',
      datetime.date(2006, 11, 17),
      ('Martin', 'Campbell'),
      [
       'Daniel Craig',
       'Eva Green',
       'Mads Mikkelsen',
       'Judi Dench',
       'Jeffrey',
       'Wright'],
      [
       'Action', 'Adventure'],
      'action',
      5,
      'casino.png',
      "In his first mission, James Bond must stop Le Chiffre, a banker to the world's terrorist organizations, from winning a high-stakes poker tournament at Casino Royale in Montenegro."],
     [
      'Toy Story',
      'Oooh...3-D.',
      datetime.date(1995, 11, 22),
      ('John', 'Lasseter'),
      [
       'Tom Hanks',
       'Tim Allen',
       'Don Rickles',
       'Jim Varney',
       'Wallace Shawn'],
      [
       'Animation', 'Adventure'],
      'animation',
      4,
      'toystory.png',
      "a cowboy toy is profoundly threatened and jealous when a fancy spaceman toy supplants him as top toy in a boy's room."],
     [
      "Harry Potter and the Sorcerer's Stone",
      'Let The Magic Begin.',
      datetime.date(2001, 11, 16),
      ('Chris', 'Columbus'),
      [
       'Richard Harris',
       'Maggie Smith',
       'Daniel Radcliffe',
       'Fiona Shaw',
       'Richard Griffiths'],
      [
       'Family', 'Adventure'],
      'family',
      3,
      'potter.png',
      'Rescued from the outrageous neglect of his aunt and uncle, a young boy with a great destiny proves his worth while attending Hogwarts School of Witchcraft and Wizardry.'],
     [
      'Iron Man 2',
      'The world now becomes aware of the dual life of the Iron Man.',
      datetime.date(2010, 5, 17),
      ('Jon', 'Favreau'),
      [
       'Robert Downey Jr.',
       'Gwyneth Paltrow',
       'Don Cheadle',
       'Scarlett Johansson',
       'Mickey Rourke'],
      [
       'Action', 'Adventure', 'Sci-fi'],
      'sci-fi',
      3,
      'ironman.png',
      'billionaire Tony Stark must contend with deadly issues involving the government, his own friends, as well as new enemies due to his superhero alter ego Iron Man.'],
     [
      'The Lion King',
      "Life's greatest adventure is finding your place in the Circle of Life.",
      datetime.date(1994, 6, 24),
      ('Roger', 'Allers'),
      [
       'Matthew Broderick',
       'Jeremy Irons',
       'James Earl Jones',
       'Jonathan Taylor Thomas',
       'Nathan Lane'],
      [
       'Animation', 'Adventure'],
      'animation',
      5,
      'lionking.png',
      'Tricked into thinking he killed his father, a guilt ridden lion cub flees into exile and abandons his identity as the future King.'],
     [
      'Avatar',
      'Enter the World.',
      datetime.date(2009, 12, 18),
      ('James', 'Cameron'),
      [
       'Sam Worthington',
       'Zoe Saldana',
       'Stephen Lang',
       'Michelle Rodriguez',
       'Sigourney Weaver'],
      [
       'Action', 'Adventure', 'Sci-fi'],
      'sci-fi',
      5,
      'avatar.png',
      'A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.'],
     [
      'Pirates of the Caribbean: The Curse of the Black Pearl',
      'Prepare to be blown out of the water.',
      datetime.date(2003, 7, 9),
      ('Gore', 'Verbinski'),
      [
       'Johnny Depp',
       'Geoffrey Rush',
       'Orlando Bloom',
       'Keira Knightley',
       'Jack Davenport'],
      [
       'Action', 'Adventure'],
      'action',
      5,
      'pirates.png',
      'Blacksmith Will Turner teams up with eccentric pirate "Captain" Jack Sparrow to save his love, the governor\'s daughter, from Jack\'s former pirate allies, who are now undead.'],
     [
      'The Dark Knight',
      'Why so serious?',
      datetime.date(2008, 7, 18),
      ('Christopher', 'Nolan'),
      [
       'Christian Bale',
       'Heath Ledger',
       'Aaron Eckhart',
       'Michael Caine',
       'Maggie Gyllenhaal'],
      [
       'Action', 'Drama'],
      'action',
      5,
      'darkknight.png',
      'Batman, Gordon and Harvey Dent are forced to deal with the chaos unleashed by an anarchist mastermind known only as the Joker, as it drives each of them to their limits.']]
    visits = {'The Shining': [
                     (
                      'Washington D.C.', 10000, datetime.date(1980, 5, 23)),
                     (
                      'Buesnos Aires', 4000, datetime.date(1980, 6, 12)),
                     (
                      'California', 13000, datetime.date(1980, 5, 23))], 
       'The Dark Knight': [
                         (
                          'New York', 20000, datetime.date(2008, 7, 18)),
                         (
                          'London', 15000, datetime.date(2008, 7, 20)),
                         (
                          'Tokyo', 3000, datetime.date(2008, 7, 24))], 
       'Avatar': [
                (
                 'Shangai', 6000, datetime.date(2010, 1, 5)),
                (
                 'Atlanta', 3000, datetime.date(2009, 12, 18)),
                (
                 'Boston', 5000, datetime.date(2009, 12, 18))]}
    for title, short_description, releasedate, (director_first_name, director_last_name), cast, tags, genre, rating, cover, description in movies:
        director = Fixture.insert_or_update_fixture(Person, fixture_key='%s_%s' % (director_first_name, director_last_name), values={'first_name': director_first_name, 'last_name': director_last_name})
        movie = Fixture.find_fixture(Movie, title)
        if not movie:
            image = resource_filename('camelot_example', os.path.join('media', 'covers', cover))
            stored_image = storage.checkin(image)
            movie = Fixture.insert_or_update_fixture(Movie, fixture_key=title, values={'title': title, 
               'director': director, 
               'short_description': short_description, 
               'releasedate': releasedate, 
               'rating': rating, 
               'genre': genre, 
               'description': description, 
               'cover': stored_image})
        rep = visits.get(title, None)
        if rep:
            for city, visitors, date in rep:
                Fixture.insert_or_update_fixture(VisitorReport, fixture_key='%s_%s' % (title, city), values={'movie': movie, 
                   'date': date, 
                   'visitors': visitors})

    return
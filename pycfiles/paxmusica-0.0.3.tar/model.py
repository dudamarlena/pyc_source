# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: paxmusica/model.py
# Compiled at: 2013-03-05 16:27:54
import os, fnmatch, id3reader
from flask import g
from os.path import join, isdir
import sqlite3
db_location = 'paxmusica.db'

class Song(object):

    def __init__(self, id, track, artist, album, title, path):
        self.id = id
        self.track = track
        self.artist = artist
        self.album = album
        self.title = title
        self.path = path

    def get_adder(self):
        return g.cur.execute('SELECT adder from playist WHERE id=?', [self.id])

    def get_time(self):
        return g.cur.execute('SELECT time from playlist WHERE id=?', [self.id])

    def insert_into_playlist(self):
        g.cur.execute('INSERT INTO playlist (song_id, adder, time) VALUES (?, "test", datetime(\'now\'))', [self.id])

    def remove_from_playlist(self):
        con = sqlite3.connect(db_location)
        cur = con.cursor()
        cur.execute('DELETE FROM playlist WHERE song_id=?', [self.id])
        con.commit()
        con.close()

    def delete(self):
        g.cur.execute('DELETE FROM playlist WHERE song_id=?', [self.id])
        g.cur.execute('DELETE FROM songs WHERE id=?', [self.id])


def update_song_library():
    in_db = []
    in_basedir = []
    g.cur.execute('SELECT path FROM songs')
    for song_path in g.cur.fetchall():
        in_db.append(song_path[0])

    for directory in get_basedirs():
        for root, dirs, files in os.walk(str(directory.directory)):
            for name in files:
                if name.endswith('.mp3'):
                    tags = id3reader.Reader(join(root, name))
                    track = tags.getValue('track')
                    artist = tags.getValue('performer')
                    album = tags.getValue('album')
                    path = join(root, name).decode('ISO 8859-15')
                    title = tags.getValue('title')
                    in_basedir.append(path)
                    if path not in in_db:
                        g.cur.execute('INSERT INTO songs (track, artist, album,\n                                        title, path) VALUES (?, ?, ?, ?, ?)', [
                         track, artist, album, title, path])

    for path in in_db:
        if path not in in_basedir:
            song = get_song_by_path(path)
            song.delete()


def migrate():
    drop = [
     'songs', 'playlist']
    create = [
     'CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY\n                  AUTOINCREMENT, track VARCHAR(50), artist VARCHAR (50),\n                  album VARCHAR (59), title VARCHAR (50), path TEXT)',
     'CREATE TABLE IF NOT EXISTS playlist (song_id KEY, adder INT,\n                  time DATETIME)',
     'CREATE TABLE IF NOT EXISTS basedirs (id INTEGER PRIMARY KEY\n                  AUTOINCREMENT, directory TEXT)']
    for table in drop:
        g.cur.execute('DROP TABLE IF EXISTS ' + table)

    for query in create:
        g.cur.execute(query)


def get_all_songs():
    g.cur.execute('SELECT id, track, artist, album, title, path FROM songs ORDER BY track')
    return [ Song(*item) for item in g.cur.fetchall() ]


def get_all_artists():
    g.cur.execute('SELECT DISTINCT artist FROM songs ORDER BY artist')
    return g.cur.fetchall()


def get_albums_by_artist(artist):
    g.cur.execute('SELECT DISTINCT album FROM songs WHERE artist=? ORDER BY album', [artist])
    return g.cur.fetchall()


def get_songs_by_artist_and_album(artist, album):
    g.cur.execute('SELECT id, track, artist, album, title, path FROM songs WHERE artist=? AND album=? ORDER BY track', [artist, album])
    return [ Song(*item) for item in g.cur.fetchall() ]


def get_song_by_id(id):
    g.cur.execute('SELECT id, track, artist, album, title, path FROM songs WHERE id=?', [id])
    return Song(*g.cur.fetchone())


def get_song_by_path(path):
    g.cur.execute('SELECT id, track, artist, album, title, path FROM songs WHERE path=?', [path])
    return Song(*g.cur.fetchone())


def get_first_playlist_entry():
    con = sqlite3.connect(db_location)
    cur = con.cursor()
    cur.execute('SELECT song_id FROM playlist ORDER BY time')
    playlist_entry = cur.fetchone()
    if playlist_entry != None:
        cur.execute('SELECT id, track, artist, album, title, path FROM songs WHERE id=?', playlist_entry)
        return Song(*cur.fetchone())
    else:
        con.commit()
        con.close()
        return


def get_remaining_playlist_entries():
    g.cur.execute('SELECT song_id FROM playlist ORDER BY time')
    list = []
    for song_id in g.cur.fetchall()[1:]:
        song = get_song_by_id(song_id[0])
        list.append(song)

    return list


class Basedir(object):

    def __init__(self, id, directory):
        self.id = id
        self.directory = directory

    def add(self):
        g.cur.execute('INSERT INTO basedirs (directory) VALUES (?)', [self.directory])

    def delete(self):
        g.cur.execute('DELETE FROM basedirs WHERE id = ?', [self.id])


def get_basedir_by_id(id):
    g.cur.execute('SELECT id, directory FROM basedirs WHERE id = ?', [id])
    return Basedir(*g.cur.fetchone())


def get_basedirs():
    g.cur.execute('SELECT id, directory FROM basedirs')
    return [ Basedir(*item) for item in g.cur.fetchall() ]


import subprocess

def play_and_update():
    if get_first_playlist_entry():
        song = get_first_playlist_entry()
        subprocess.check_call(['vlc', '-I dummy', song.path, 'vlc://quit'])
        song.remove_from_playlist()
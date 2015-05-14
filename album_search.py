import spotipy
import os
import qrcode
import json
import urllib
import re
from zbarfunc import QRCODE_PATH

SPOTIPY = spotipy.Spotify()


def ms_to_hr(total_milliseconds):
    """

    Returns a human readable with input in milliseconds

    """
    minutes, milliseconds = divmod(total_milliseconds, 60000)
    seconds = int(float(milliseconds) / 10000)
    return "%02i:%02i" % (minutes, seconds)


def get_artist_albums(artist_uri):
    """

	Returns a list of dictionaries, each dictionary contains the following entries:
	'album_type'
	'name'
	'release_date'
	'uri'
	'image'			this is a url of highest quality if available
	'tracks' []		this is a list containing the following:
		'name'
		'track_number'	(int)
		'disk_number'	(if available)
		'duration'
	'artists' []	this is a list containing the following:
		'name'
		'uri'

	"""

    albums_results = SPOTIPY.artist_albums(
        artist_uri,
        album_type='album', limit=50, country='CA'
    )
    albums_items = albums_results['items']
    singles_results = SPOTIPY.artist_albums(
        artist_uri,
        album_type='single', limit=50, country='CA'
    )
    singles_items = singles_results['items']

    while albums_results['next']:
        albums_results = SPOTIPY.next(albums_results)
        albums_items.extend(albums_results['items'])

    while singles_results['next']:
        singles_results = SPOTIPY.next(singles_results)
        singles_items.extend(singles_results['items'])

    albums = []

    for album in albums_items:
        try:
            albums.append(
                {
                    u'name': album['name'],
                    u'uri': album['uri'],
                    u'image': album['images'][0]['url'],
                    u'album_type' : album['album_type']
                }
            )
        except IndexError:
            albums.append(
                {
                    u'name': album['name'],
                    u'uri': album['uri'],
                    u'album_type' : album['album_type']
                }
            )
    for single in singles_items:
        try:
            albums.append(
                {
                    u'name': single['name'],
                    u'uri': single['uri'],
                    u'image': single['images'][0]['url'],
                    u'album_type' : single['album_type']
                }
            )
        except IndexError:
            albums.append(
                {
                    u'name': single['name'],
                    u'uri': single['uri'],
                    u'album_type' : single['album_type']
                }
            )

    for album in albums:
        searched_artist = SPOTIPY.artist(artist_uri)['name']
        album[u'artists'] = [{u'name': searched_artist, u'uri': artist_uri}]
        album = SPOTIPY.album(album['uri'])
        album[u'release_date'] = album[u'release_date']
        album[u'tracks'] = []

        track_results = SPOTIPY.album(album['uri'])['tracks']
        track_items = track_results['items']
        while track_results['next']:
            track_results = SPOTIPY.next(track_results)
            track_items.extend(track_results['items'])

        for track in track_items:
            try:
                album['tracks'].append(
                    {
                        u'name': track['name'],
                        u'track_number': track['track_number'],
                        u'duration' : track['duration_ms'],
                        u'disc_number': track['disc_number']
                    }
                )
            except KeyError:
                album['tracks'].append(
                    {
                        u'name': track['name'],
                        u'track_number': track['track_number'],
                        u'duration': track['duration_ms'],
                        u'disc_number': 1
                    }
                )
            for artist in track['artists']:
                if {
                        u'name': artist['name'],
                        u'uri': artist['uri']
                    } not in album[u'artists']:
                    album[u'artists'].append(
                        {
                            u'name': artist['name'],
                            u'uri': artist['uri']
                        }
                    )

    return albums


def human_album(album):
    """

	Takes the output of get_artist_albums[i] and prints info to disk

	"""

    artist = album['artists'][0]['name']
    album_type = album['album_type']
    album_name = album['name']
    artist = re.sub('/', '-', artist)
    album_type = re.sub('/', '-', album_type)
    album_name = re.sub('/', '-', album_name)
    location = (
        QRCODE_PATH +
        artist + '/'
        + album_type + '/' +
        album_name
    )

    if os.path.isfile(location):
        return album

    to_print = []
    total_duration = 0
    try:
        to_print.append(
            'name: ' + album['name'] +
            '\turi: ' + album['uri'] +
            '\tdate: ' + album['release_date']
        )
    except KeyError:
        to_print.append('name: ' + album['name'] + '\turi: ' + album['uri'])
    for artist in album['artists']:
        to_print.append('artist: ' + artist['name'] + '\turi: ' + artist['uri'])
    try:
        to_print.append('Album Art: ' + album['image'])
    except KeyError:
        to_print.append('No Album Art')
    for track in album['tracks']:
        duration = track['duration']
        total_duration += duration
        duration = ms_to_hr(duration)
        to_print.append(
            'Disk: ' + str(track['disk_number']) +
            '\tTrack: ' + str(track['track_number']) +
            '\tTrack Name: ' + track['name'] +
            '\tDuration: ' + duration
        )
    total_duration = ms_to_hr(total_duration)
    to_print.append(total_duration)

    if not os.path.exists(os.path.dirname(location)):
        os.makedirs(os.path.dirname(location))
    with open(location.encode('utf-8'), 'w') as text_file:
        for line in to_print:
            text_file.write("%s\n" % line.encode('utf-8'))
    return album


def create_qrcode(album):
    """

	Takes the output of get_artist_albums[i] and creates a qr code

	"""

    artist = album['artists'][0]['name']
    album_type = album['album_type']
    album_name = album['name']
    artist = re.sub('/', '-', artist)
    album_type = re.sub('/', '-', album_type)
    album_name = re.sub('/', '-', album_name)
    location = QRCODE_PATH + artist + '/' + album_type + '/' + album_name

    if os.path.isfile(location + '.png'):
        return album

    img = qrcode.make(album['uri'])
    if not os.path.exists(os.path.dirname(location)):
        os.makedirs(os.path.dirname(location))
    img.save(location + '.png')


def save_json(album):
    """

	Takes the output of get_artist_albums[i] and
    saves the relevant data as a .json

	"""

    artist = album['artists'][0]['name']
    album_type = album['album_type']
    album_name = album['name']
    artist = re.sub('/', '-', artist)
    album_type = re.sub('/', '-', album_type)
    album_name = re.sub('/', '-', album_name)
    location = QRCODE_PATH + artist + '/' + album_type + '/' + album_name

    if os.path.isfile(location + '.json'):
        return album

    if not os.path.exists(os.path.dirname(location)):
        os.makedirs(os.path.dirname(location))
    with open(location.encode('utf-8') + '.json', 'w') as text_file:
        text_file.write(json.dumps(album))


def download_art(album):
    """

    Takes the output of get_artist_albums[i] and saves the Album Art

    """



    artist = album['artists'][0]['name']
    album_type = album['album_type']
    album_name = album['name']
    artist = re.sub('/', '-', artist)
    album_type = re.sub('/', '-', album_type)
    album_name = re.sub('/', '-', album_name)
    location = QRCODE_PATH + artist + '/' + album_type + '/' + album_name

    if os.path.isfile(location + '.jpeg'):
        return album

    try:
        urllib.urlretrieve(album['image'], location + '.jpeg')
    except KeyError:
        pass


def full_artists(albums):
    """

    Takes the output of get_artist_albums and
    saves a list of all artist mentioned

    """
    artists = []
    for album in albums:
        for artist in album['artists']:
            if artist not in artists:
                artists.append(artist)

    artist = artists[0]['name']
    artist = re.sub('/', '-', artist)
    location = QRCODE_PATH + artist + '/' + 'all_artists'
    with open(location.encode('utf-8'), 'w') as text_file:
        for line in artists:
            text_file.write(
                "name: %s\n\turi: %s\n\n" % (
                    line['name'].encode('utf-8'),
                    line['uri'].encode('utf-8')
                )
            )




def populate_folders(artist_uri):
    """

    This function calls the other necessary
    functions for creating and filling folders.

    """
    print 'populating...'
    albums = get_artist_albums(artist_uri)
    print str(len(albums)) + ' entries to download.'
    for album in albums:
        human_album(album)
        create_qrcode(album)
        save_json(album)
        download_art(album)
    full_artists(albums)
    print 'done'


def search_for_artist(search_term):
    """

    This function takes a search term and returns the top result with a prompt.
    It then calls the main populate_folders() function on the selected artist.

    """


    results = SPOTIPY.search(search_term, type='artist')
    artists = results['artists']['items']
    results_index = 0
    while True:
        try:
            print '\n' + search_term
            print artists[results_index]['name'] + '\n'
            prompt = raw_input(
                'Is this what you were looking for?\n'
                '[y] for yes [n] for next [x] '
                'for new term or [q] to quit: '
            )
            #prompt= 'y'
            if prompt.startswith('y'):
                populate_folders(artists[results_index]['uri'])
                break
            elif prompt.startswith('x'):
                break
            elif prompt.startswith('q'):
                return 0
            elif prompt.startswith('n'):
                results_index += 1
            else:
                break
        except IndexError:
            if results_index >= 1:
                print 'No more results'
            else:
                print '\nNo results returned\n'
            break


#composers = open('composers', 'rb').readlines()
#for composer in composers:
#    search_for_artist(composer.strip())

def artist_search_loop():
    while True:
        if search_for_artist(raw_input("Enter a search query: ").strip()) == 0:
            break

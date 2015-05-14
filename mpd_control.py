from mpd import MPDClient

ADDRESS = 'localhost'
PORT = 6600

MPD_CLIENT = MPDClient()
MPD_CLIENT.timeout = 10
MPD_CLIENT.idletimeout = None
MPD_CLIENT.connect(ADDRESS, PORT)


def probe_playlists():
    #Returns a list of valid mpd playlists
    playlists = []
    for i, pl in enumerate(MPD_CLIENT.listplaylists()):
        playlists.append(MPD_CLIENT.listplaylists()[i].get('playlist'))
    return playlists

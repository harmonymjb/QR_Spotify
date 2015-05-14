import zbarfunc
import album_search
from spotify_qdbus import Spotify
from mpd_control import MPD_CLIENT
from mpd_control import probe_playlists


def qr_functions(last_code):
    """

    Main scan and processing functions. Calls functions for QR scanning.
    Takes the last code scanned as an input to prevent play inturruption
    if the same code is scanned multiple times.

    """
    print 'Scanning...'
    MPD_CLIENT.send_idle()
    scanned_code = str(zbarfunc.QRCode().get_data())
    print scanned_code
    media_functions = [
        'artist_search',
        'next',
        'previous',
        'pause',
        'playpause',
        'stop',
        'play',
        'break'
    ]
    for each in media_functions:
        zbarfunc.QRCode.save_qrcode(each, 'functions/' + each)
    MPD_CLIENT.noidle()
    if scanned_code != last_code and scanned_code in media_functions:
        if scanned_code == 'artist_search':
            album_search.artist_search_loop()
        elif scanned_code == 'next':
            SPOTIFY.next()
            MPD_CLIENT.next()
        elif scanned_code == 'previous':
            SPOTIFY.previous()
            MPD_CLIENT.previous()
        elif scanned_code == 'pause':
            SPOTIFY.pause()
            MPD_CLIENT.pause()
        elif scanned_code == 'playpause':
            SPOTIFY.play_pause()
            MPD_CLIENT.pause()
        elif scanned_code == 'stop':
            SPOTIFY.stop()
            MPD_CLIENT.clear()
        elif scanned_code == 'play':
            SPOTIFY.play()
            MPD_CLIENT.play()
        elif scanned_code == 'break':
            SPOTIFY.quit()
            MPD_CLIENT.clear()
            return scanned_code
        return 'function_used'
    elif scanned_code != last_code and scanned_code.startswith('spotify:'):
        MPD_CLIENT.clear()
        if SPOTIFY.exists() == False:
            SPOTIFY.start(3)
        SPOTIFY.openuri(scanned_code)
        return scanned_code
    elif scanned_code != last_code and scanned_code in probe_playlists():
        SPOTIFY.quit()
        MPD_CLIENT.load(scanned_code)
        MPD_CLIENT.play()
        return scanned_code
    else:
        print 'No functions called. (Did you scan a valid code?)'
        return scanned_code


if __name__ == '__main__':
    SPOTIFY = Spotify()
    LAST_CODE = None
    while True:
        if LAST_CODE == 'break':
            break
        else:
            LAST_CODE = qr_functions(LAST_CODE)



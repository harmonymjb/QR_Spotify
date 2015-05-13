import os
import zbarfunc
from spotify_qdbus import Spotify

SPOTIFY = Spotify()
os.system('spotify 1>/dev/null 2>&1 &')
LAST_CODE = None


def qr_functions(last_code):
    #Main scan and processing functions. Calls functions for QR scanning
    print 'Scanning...'
    scanned_code = str(zbarfunc.QRCode().get_data())
    print scanned_code
    allowed = [
        'next',
        'previous',
        'pause',
        'playpause',
        'stop',
        'play',
        'break'
    ]
    for each in allowed:
        zbarfunc.save_qrcode(each, '00 ' + each)
    if scanned_code != last_code and scanned_code in allowed:
        if scanned_code == 'next':
            SPOTIFY.next()
        elif scanned_code == 'previous':
            SPOTIFY.previous()
        elif scanned_code == 'pause':
            SPOTIFY.pause()
        elif scanned_code == 'playpause':
            SPOTIFY.play_pause()
        elif scanned_code == 'stop':
            SPOTIFY.stop()
        elif scanned_code == 'play':
            SPOTIFY.play()
        elif scanned_code == 'break':
            SPOTIFY.stop()
            return scanned_code
    elif scanned_code != last_code and scanned_code.startswith('spotify:'):
        SPOTIFY.openuri(scanned_code)
        return scanned_code
    else:
        return scanned_code


while True:
    try:
        if LAST_CODE == 'break':
            break
        else:
            LAST_CODE = qr_functions(LAST_CODE)
    except NameError:
        LAST_CODE = qr_functions(None)

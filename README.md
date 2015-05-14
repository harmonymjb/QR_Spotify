# QR_Spotify
main_app.py runs in a terminal allowing entry via QR code of generated plain text commands that point to functions.

These functions control media playback via Spotify and mpd.

QR codes can be encoded with links to playlists, albums, artist, or tracks of music.

Try the qrcodes/functions/artist_search.png code and enter an artist with tracks available on spotify. The program will generate QR codes for each album referencing that artist and place them along with plain text information, a json file, and album art in qrcodes/.

The other generated QR codes in qrcode/functions/ can be used to control mpd or spotify.

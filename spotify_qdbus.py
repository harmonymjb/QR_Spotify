import os

class Spotify:

    def __init__(self):
        self.qdbus = 'qdbus org.mpris.MediaPlayer2.spotify / '
        'org.freedesktop.MediaPlayer2.'

    def next(self):
        os.system(self.qdbus + 'Next')

    def previous(self):
        os.system(self.qdbus + 'Previous')

    def pause(self):
        os.system(self.qdbus + 'Pause')

    def play_pause(self):
        os.system(self.qdbus + 'PlayPause')

    def stop(self):
        os.system(self.qdbus + 'Stop')

    def play(self):
        os.system(self.qdbus + 'Play')

    def openuri(self, uri):
        os.system(self.qdbus + 'OpenUri %s' % uri)

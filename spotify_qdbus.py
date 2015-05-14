import os
import subprocess
import re


def findProcess(name):
    processes = subprocess.Popen(
        "ps -eaf | grep " + name,
        shell=True,
        stdout=subprocess.PIPE
    )
    output = processes.stdout.read()
    processes.stdout.close()
    processes.wait()
    return output


def processRunning(name, path):
    output = findProcess(name)
    if re.search(path+name, output) is None:
        return False
    else:
        return True


class Spotify:

    def __init__(self):
        self.qdbus = 'qdbus org.mpris.MediaPlayer2.spotify / '
        'org.freedesktop.MediaPlayer2.'

    def start(self, sleep):
        os.system('(spotify 1>/dev/null 2>&1 &) && sleep %i' % sleep)

    def exists(self):
        path = '/opt/spotify/spotify-client/Data/'
        name = 'SpotifyHelper'
        return processRunning(name, path)

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

    def quit(self):
        os.system(self.qdbus + 'Quit')

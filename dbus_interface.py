import dbus
import zbarfunc

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
BUS = dbus.SessionBus()

SPOTIFY = BUS.get_object(
    'org.mpris.MediaPlayer2.spotify',
    '/org/mpris/MediaPlayer2'
)
IFACE = dbus.Interface(SPOTIFY, 'org.mpris.MediaPlayer2.Player')

IFACE.OpenUri(str(zbarfunc.QRCode().get_data()))

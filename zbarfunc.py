from sys import argv
import zbar
import os
import qrcode

QRCODE_PATH = 'qrcodes/'

class QRCode():

    data = None
    proc = None

    def __init__(self):
        self.proc = zbar.Processor()
        self.proc.parse_config('enable')
        device = '/dev/video0'
        if len(argv) > 1:
            device = argv[1]
        self.proc.init(device)
        self.proc.visible = True
    #display cam window if True,  hide if False

    def get_data(self):
        self.proc.process_one()
        for symbol in self.proc.results:
            return symbol.data

    @staticmethod
    def save_qrcode(content, name):
        img = qrcode.make(content)
        if not os.path.exists(os.path.dirname(QRCODE_PATH + name + '.png')):
            os.makedirs(os.path.dirname(QRCODE_PATH + name + '.png'))
        img.save(QRCODE_PATH + name + '.png')

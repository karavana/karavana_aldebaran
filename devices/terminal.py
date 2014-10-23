import device
import sys


DEVICE_TYPE = 0x01
DEVICE_ID = 0xABCDEF
DEVICE_CLASS = 'Terminal'


class Terminal(device.Device):

    def handle_data(self, data):
        print '\033[0;36m%s\033[0m' % data
        return 200, 'Ok\n'

    def run(self, args):
        retval = 0
        try:
            while True:
                text = raw_input('Type some text: ')
                retval = self.send_data(text)
                if retval == 1:
                    break
                if retval == 2:
                    print 'Text could not be sent: %s' % text
        except:
            pass
        return retval
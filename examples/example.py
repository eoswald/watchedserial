# Example used along with arduino_example

import time

import serial
from watchedserial import WatchedReaderThread


PORT = "COM3"

class MyPacket(serial.threaded.FramedPacket):
    def handle_packet(self, packet):
        print(packet)


class MyWatchedReaderThread(WatchedReaderThread):
    def handle_reconnect(self):
        print("Reconnected")

    def handle_disconnect(self, error):
        print("Disconnected")


ser = serial.Serial(PORT, baudrate=115200)
with MyWatchedReaderThread(ser, MyPacket) as protocol:
    while True:
        time.sleep(1)

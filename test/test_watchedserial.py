import os
import sys
import time
import unittest
from unittest.mock import MagicMock

import serial
import serial.threaded

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import watchedserial


# on which port should the test be performed:
PORT = 'loop://'


class Test_watchedserial(unittest.TestCase):
    """Test watchedserial related functionality"""

    def test_watched_reader(self):
        """test the watched reader thread disconnect, reconnect,
        then stay disconnected"""

        class TestPacketizer(serial.threaded.Packetizer):
            def __init__(self):
                super(TestPacketizer, self).__init__()
                self.received_packets = []
                self.disconnect_count = 0
                self.reconnect_count = 0

            def handle_packet(self, packet):
                self.received_packets.append(bytes(packet))


        class TestWatchedReaderThread(watchedserial.WatchedReaderThread):
            def handle_disconnect(self, error):
                self.protocol.disconnect_count += 1

            def handle_reconnect(self):
                self.protocol.reconnect_count += 1


        def open_side_effect():
            """Reconnect once then disconnect for good"""
            count = 0
            while True:
                if not count:
                    count += 1
                    yield
                else:
                    count += 1
                    yield serial.SerialException

        ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)
        ser.read = MagicMock(side_effect=[
            b'1\0',
            b'2\0',
            serial.SerialException, # disconnect once
            b'4\0',
            serial.SerialException]) # stay disconnected
        ser.open = MagicMock(side_effect=open_side_effect())
        ser.close = MagicMock() # to make sure it doesn't override ser.is_open
        with TestWatchedReaderThread(ser, TestPacketizer) as protocol:
            time.sleep(0.25)
            self.assertEqual(protocol.received_packets, [b'1', b'2', b'4'])
            self.assertEqual(protocol.disconnect_count, 2)
            self.assertEqual(protocol.reconnect_count, 1)


if __name__ == '__main__':
    unittest.main()

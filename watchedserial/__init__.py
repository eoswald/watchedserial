import serial.threaded
import time


class WatchedReaderThread(serial.threaded.ReaderThread):
    """
    Subclass of serial.threaded.Reader thread that adds handling of the serial
    device connecting and disconnecting.

    Calls handle_reconnect() when the serial device is reconnected and
    handle_disconnect() when the serial device is disconnected. Neither of
    these callbacks are implemented and need to be overridden by subclassing.
    They should not be blocking calls.

    """

    def run(self):
        """Reader loop"""
        if not hasattr(self.serial, 'cancel_read'):
            self.serial.timeout = 1
        self.protocol = self.protocol_factory()
        try:
            self.protocol.connection_made(self)
        except Exception as e:
            self.alive = False
            self.protocol.connection_lost(e)
            self._connection_made.set()
            return
        error = None
        self._connection_made.set()
        while True:
            while self.alive and self.serial.is_open:
                try:
                    # read all that is there or wait for one byte (blocking)
                    data = self.serial.read(self.serial.in_waiting or 1)
                except serial.SerialException as e:
                    # probably some I/O problem such as disconnected USB serial
                    # adapters -> exit
                    self.serial.close()
                    self.handle_disconnect(e)
                    break
                else:
                    if data:
                        # make a separated try-except for called used code
                        try:
                            self.protocol.data_received(data)
                        except Exception as e:
                            error = e
                            break
            # if there was an error calling data_received
            if error:
                break
            while True:
                try:
                    self.serial.open()
                except serial.SerialException:
                    time.sleep(0.1)
                    continue
                else:
                    self.handle_reconnect()
                    break
        self.alive = False
        self.protocol.connection_lost(error)
        self.protocol = None 

    def handle_reconnect(self):
        """Handle serial reconnection - to be overridden by subclassing"""
        raise NotImplementedError('please implement functionality in handle_reconnect')

    def handle_disconnect(self, error):
        """Handle serial disconnection - to be overridden by subclassing"""
        raise NotImplementedError('please implement functionality in handle_disconnect')

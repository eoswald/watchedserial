=============
watchedserial
=============

|build-status| |pypi|

Installation
============

.. code-block:: bash

        $ pip install watchedserial


Description
===========
``WatchedReaderThread`` is a subclass of pySerial's
``serial.threaded.ReaderThread``. Similar to ``ReaderThread``,
``WatchedReaderThread`` implements a serial port read loop in it's own thread but
instead of killing the thread on a serial disconnection, it calls a callback and
waits for the port to become available again before attempting a reconnect. On
reconnect it calls a reconnect callback. This should make writing apps that need to
deal with unreliable serial connections more seamless and make it easier to write
apps that should allow the user to disconnect and reconnect a serial device safely.

Usage
=====
Subclass ``watchedserial.WatchedReaderThread`` to implement the
``handle_reconnect()`` and ``handle_disconnect()`` callbacks. Both of these
functions should be non-blocking (similar to an ISR).

.. code-block:: python

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



.. |build-status| image:: https://travis-ci.org/eoswald/watchedserial.svg?branch=master

.. |pypi| image:: https://img.shields.io/pypi/v/watchedserial.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/watchedserial
    :alt: Latest version released on PyPi


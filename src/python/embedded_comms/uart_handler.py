#!/usr/bin/env python3

import serial
import threading


class UARTHandler:
    def __init__(
        self,
        port="/dev/serial0",
        baudrate=115200,
        timeout=1,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
        )

        self.lock = threading.Lock()

    def send(self, data):
        """
        Send bytes, bytearray, string, or list of integers.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif isinstance(data, list):
            data = bytes(data)

        with self.lock:
            self.ser.write(data)
            self.ser.flush()

    def send_array(self, messages, delay=None):
        """
        Send an iterable of messages.
        """
        import time

        for msg in messages:
            self.send(msg)

            if delay:
                time.sleep(delay)

    def read(self, size=1):
        """
        Read a fixed number of bytes.
        """
        with self.lock:
            return self.ser.read(size)

    def readline(self):
        """
        Read until newline.
        """
        with self.lock:
            return self.ser.readline()

    def available(self):
        """
        Number of bytes waiting in RX buffer.
        """
        return self.ser.in_waiting

    def close(self):
        if self.ser.is_open:
            self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
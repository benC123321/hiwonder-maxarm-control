import logging
import signal
import sys

from embedded_comms.uart_handler import UARTHandler
from embedded_comms.gpio_handler import GPIOHandler
from networking.grpc_interface import MotorControlServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

uart = UARTHandler(port="/dev/ttyAMA0", baudrate=115200)
gpio = GPIOHandler()
server = MotorControlServer(uart, gpio)
server.start()

def _shutdown(*_):
    server.stop()
    uart.close()
    gpio.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

server.wait_for_termination()

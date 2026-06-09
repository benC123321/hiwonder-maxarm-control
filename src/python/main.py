import logging
import signal
import sys

from embedded_comms.uart_handler import UARTHandler
from networking.grpc_interface import MotorControlServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

uart = UARTHandler(port="/dev/ttyAMA0", baudrate=115200)
server = MotorControlServer(uart)
server.start()

def _shutdown(*_):
    server.stop()
    uart.close()
    sys.exit(0)

signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

server.wait_for_termination()

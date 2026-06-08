from uart_handler import UARTHandler
from checksum import lobot_check_sum

uart = UARTHandler(
    port="/dev/serial0",
    baudrate=115200
)

message = [
    0x55,
    0x55,
    0x01,
    0x07,
    0x03,
    0x01,
    0xF4,
    0x01,
    0xF4,
    0x01,
    0x00,
]

message[9] = lobot_check_sum(message)

uart.send(message)

uart.close()
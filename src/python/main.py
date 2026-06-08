from uart_handler import UARTHandler
from checksum import lobot_check_sum


# This interface must be enabled in board config prior to use
uart = UARTHandler(
    port="/dev/ttyAMA0",
    baudrate=115200
)

message = [
    0x55,
    0x55,
    0x01,
    0x07,
    0x01,
    0xF4,
    0x01,
    0xF4,
    0x01,
]

message.append(lobot_check_sum(message))

uart.send(message)

uart.close()
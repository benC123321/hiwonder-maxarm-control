from uart_handler import UARTHandler
from motor_position_command import MotorPositionCommand

# This interface must be enabled in board config prior to use
uart = UARTHandler(
    port="/dev/ttyAMA0",
    baudrate=115200
)

command_template = MotorPositionCommand(motor_id=1, position=0x01F4, move_time=0x01F4)

uart.send(command_template.get_send_list)

uart.close()
from functools import cached_property
from typing import List
from pydantic import BaseModel, Field
from checksum import lobot_check_sum


class MotorPositionCommand(BaseModel):
    # Fixed frame headers and commands
    LOBOT_SERVO_FRAME_HEADER_1: int = Field(default=0x55, init=False)
    LOBOT_SERVO_FRAME_HEADER_2: int = Field(default=0x55, init=False)
    MOTOR_ID: int
    UNKOWN_PARAM: int = Field(default=0x07, init=False)
    LOBOT_SERVO_MOVE_TIME_WRITE: int = Field(default=0x01, init=False)
    
    # Dynamically calculated bytes
    POSITION_LOW_BYTE: int
    POSITION_HIGH_BYTE: int
    MOVE_TIME_LOW_BYTE: int
    MOVE_TIME_HIGH_BYTE: int
    
    # Placeholder for checksum
    CHECKSUM: int = 0x00

    def __init__(self, motor_id: int, position: int, move_time: int):
        """
        Explicit initializer that takes human-readable values,
        splits them into byte components, and populates the Pydantic model.
        """
        # Extract low and high bytes (16-bit splits)
        position_low = position & 0xFF
        position_high = (position >> 8) & 0xFF
        
        move_time_low = move_time & 0xFF
        move_time_high = (move_time >> 8) & 0xFF

        # Pass the processed values into Pydantic's internal initializer
        super().__init__(
            MOTOR_ID=motor_id,
            POSITION_LOW_BYTE=position_low,
            POSITION_HIGH_BYTE=position_high,
            MOVE_TIME_LOW_BYTE=move_time_low,
            MOVE_TIME_HIGH_BYTE=move_time_high
        )
        
        self.CHECKSUM = lobot_check_sum(self.get_send_list)

    def get_send_list(self) -> List[int]:
        """
        Returns all attributes in the exact required packet structure order.
        """
        return [
            self.LOBOT_SERVO_FRAME_HEADER_1,
            self.LOBOT_SERVO_FRAME_HEADER_2,
            self.MOTOR_ID,
            self.UNKOWN_PARAM,
            self.LOBOT_SERVO_MOVE_TIME_WRITE,
            self.POSITION_LOW_BYTE,
            self.POSITION_HIGH_BYTE,
            self.MOVE_TIME_LOW_BYTE,
            self.MOVE_TIME_HIGH_BYTE,
            self.CHECKSUM,
        ]
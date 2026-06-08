def lobot_check_sum(buf: bytes | list | bytearray) -> int:
    """
    Calculates the Lobot checksum from a buffer.
    
    :param buf: A list, bytes, or bytearray object containing the packet data.
    :return: The 8-bit checksum as an integer.
    """
    # temp is a 16-bit unsigned integer
    temp = 0
    
    # buf[3] + 2 determines the range. 
    # Python's range(start, stop) is exclusive of the 'stop' value, 
    # matching the 'i < buf[3] + 2' condition in C.
    end_index = buf[3] + 2
    
    for i in range(2, end_index):
        temp += buf[i]
        temp &= 0xFFFF  # Simulate 16-bit unsigned overflow
        
    # Bitwise NOT (~) in Python works on signed integers, 
    # so we mask with 0xFFFF to keep it a 16-bit unsigned value.
    temp = (~temp) & 0xFFFF
    
    # Cast to uint8_t by masking the lowest 8 bits
    return temp & 0xFF
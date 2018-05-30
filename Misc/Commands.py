from enum import IntEnum

class Commands(IntEnum):
    ack_nack = 0
    control = 1
    firmware_reset = 2
    firmware_ready_to_accept = 3
    firmware_segment_count = 4
    firmware_segment = 5
    max_profiles = 6
import numpy as np
import struct

def hex_to_rgb(byte_array):
    # Convert the bytearray to a packed binary string
    binary_str = struct.pack('BBB', *byte_array)

    # Unpack the binary string as an RGB color tuple
    rgb_color = struct.unpack('BBB', binary_str)

    return rgb_color

input=b'\x01\x00\x02\x00\x03\x00\x04\x00\x06\x00\x07\x00'
result=[]
for i in range(len(input)//3):
    part=input[i*3:i*3+3]
    #print(part)
    result.append(hex_to_rgb(part))
print(result)
result=np.array(result).reshape(2,2,3)
print(result)
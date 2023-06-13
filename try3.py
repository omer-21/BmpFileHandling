import struct

def read_bmp_file(file_path):
    # Open the BMP file in binary mode
    with open(file_path, "rb") as bmp_file:
        # Read the file header (14 bytes)
        file_header = bmp_file.read(14)
        # Read the bitmap header (40 bytes)
        bitmap_header = bmp_file.read(40)

        # Extract relevant information from the headers
        # File header
        signature = file_header[:2].decode('ascii')
        file_size = int.from_bytes(file_header[2:6], byteorder='little')
        pixel_data_offset = int.from_bytes(file_header[10:14], byteorder='little')

        # Bitmap header
        image_width = int.from_bytes(bitmap_header[4:8], byteorder='little')
        image_height = int.from_bytes(bitmap_header[8:12], byteorder='little')
        bits_per_pixel = int.from_bytes(bitmap_header[14:16], byteorder='little')

        # Read the color palette
        color_palette = []
        if bits_per_pixel <= 8:
            palette_size = 2 ** bits_per_pixel
            for _ in range(palette_size):
                # Read three bytes (blue, green, red)
                color = bmp_file.read(3)
                color_palette.append(color)

        # Read the pixel data section
        bmp_file.seek(pixel_data_offset)

        # Read the pixel data bit by bit
        pixel_data = []
        for _ in range(image_height):
            row_data = []
            for _ in range(image_width):
                # Read one byte from the file
                byte = bmp_file.read(1)
                # Convert the byte to its binary representation
                binary = bin(int.from_bytes(byte, byteorder='little'))[2:].zfill(8)
                # Append each bit to the row_data list
                row_data.extend(list(binary))
            # Append the row data to the pixel_data list
            pixel_data.append(row_data)

    return pixel_data, color_palette, image_width, image_height, bits_per_pixel


def write_to_txt(pixel_data, color_palette, image_width, image_height, bits_per_pixel, output_file):
    # Open the output file in write mode
    with open(output_file, "w") as txt_file:
        # Write the image information to the text file
        txt_file.write(f"Image Width: {image_width}\n")
        txt_file.write(f"Image Height: {image_height}\n")
        txt_file.write(f"Bits per Pixel: {bits_per_pixel}\n")

        txt_file.write("\n")

        # Write the color palette data to the text file
        for color in color_palette:
            txt_file.write(f"Color: {color}\n")

        txt_file.write("\n")

        # Write the pixel data to the text file
        for row in pixel_data:
            for bit in row:
                txt_file.write(bit)
            txt_file.write("\n")

def hex_to_rgb(byte_array):
    # Convert the bytearray to a packed binary string
    binary_str = struct.pack('BBB', *byte_array)

    # Unpack the binary string as an RGB color tuple
    rgb_color = struct.unpack('BBB', binary_str)

    return rgb_color

def read_from_txt(input_file):
    # Open the input file in read mode
    with open(input_file, "r") as txt_file:
        lines = txt_file.readlines()

        # Extract image information from the text file
        image_width = int(lines[0].split(":")[1].strip())
        image_height = int(lines[1].split(":")[1].strip())
        bits_per_pixel = int(lines[2].split(":")[1].strip())

        # Extract color palette data from the text file
        color_palette = []
        palette_start = 4
        palette_end = palette_start + (2 ** bits_per_pixel)
        for line in lines[palette_start:palette_end]:
            print(line)
            start_index =line.find("b'")
            end_index = line.find("'", start_index + 2)
            color_str = line[start_index + 2:end_index]
            # Split the string by '\x' and convert each hexadecimal value to an integer
            color = tuple(int(value, 16) for value in color_str.split("\\x"))
            color_palette.append(color)
        # Extract pixel data from the text file
        pixel_data = []
        for line in lines[palette_end:]:
            bits = line.strip()
            row_data = [bits[i:i+8] for i in range(0, len(bits), 8)]
            pixel_data.append(row_data)

    return pixel_data, color_palette, image_width, image_height, bits_per_pixel


def write_bmp_file(pixel_data, color_palette, image_width, image_height, bits_per_pixel, output_file):
    # Calculate file size and pixel data offset
    palette_size = 2 ** bits_per_pixel
    row_size = (image_width * bits_per_pixel + 31) // 32 * 4  # Row size must be multiple of 4 bytes
    pixel_data_size = row_size * image_height
    file_size = 14 + 40 + (palette_size * 3) + pixel_data_size
    pixel_data_offset = 14 + 40 + (palette_size * 3)

    # Create the new BMP file
    with open(output_file, "wb") as bmp_file:
        # Write file header
        bmp_file.write(b"BM")  # Signature
        bmp_file.write(file_size.to_bytes(4, byteorder='little'))  # File size
        bmp_file.write(b"\x00\x00\x00\x00")  # Reserved
        bmp_file.write(pixel_data_offset.to_bytes(4, byteorder='little'))  # Pixel data offset

        # Write bitmap header
        bmp_file.write(b"\x28\x00\x00\x00")  # Header size (40 bytes)
        bmp_file.write(image_width.to_bytes(4, byteorder='little'))  # Image width
        bmp_file.write(image_height.to_bytes(4, byteorder='little'))  # Image height
        bmp_file.write(b"\x01\x00")  # Number of color planes (1)
        bmp_file.write(bits_per_pixel.to_bytes(2, byteorder='little'))  # Bits per pixel
        bmp_file.write(b"\x00\x00\x00\x00")  # Compression method (none)
        bmp_file.write(pixel_data_size.to_bytes(4, byteorder='little'))  # Pixel data size
        bmp_file.write(b"\x00\x00\x00\x00")  # Horizontal resolution (pixels per meter)
        bmp_file.write(b"\x00\x00\x00\x00")  # Vertical resolution (pixels per meter)
        bmp_file.write(b"\x00\x00\x00\x00")  # Number of colors in palette (default)
        bmp_file.write(b"\x00\x00\x00\x00")  # Number of important colors (all)

        # Write color palette
        for color in color_palette:
            bmp_file.write(bytes(color))

        # Write pixel data
        for row in pixel_data:
            for bits in row:
                byte = int(bits, 2).to_bytes(1, byteorder='little')
                bmp_file.write(byte)

        print("BMP file created successfully!")
"""
# Example usage
bmp_file_path = "Design.bmp"
txt_output_file = "output.txt"

# Read the BMP file and get the pixel data, color palette, and image information
pixel_data, color_palette, image_width, image_height, bits_per_pixel = read_bmp_file(bmp_file_path)

# Write the pixel data, color palette, and image information to a new text file
write_to_txt(pixel_data, color_palette, image_width, image_height, bits_per_pixel, txt_output_file)
"""

"""Reading Bmp file from txt"""

# Example usage
txt_input_file = "output.txt"
bmp_output_file = "output.bmp"

# Read the data from the text file
pixel_data, color_palette, image_width, image_height, bits_per_pixel = read_from_txt(txt_input_file)

# Create a new BMP file based on the data
write_bmp_file(pixel_data, color_palette, image_width, image_height, bits_per_pixel, bmp_output_file)

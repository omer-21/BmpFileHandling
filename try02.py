def convert_8bit_to_1bit(input_file, output_file):
    # Open the input BMP file in binary mode
    with open(input_file, 'rb') as f:
        # Read the BMP header (54 bytes)
        bmp_header = f.read(54)
        hesder=bmp_header
        # Read the color palette (256 colors, each represented by 4 bytes)
        color_palette = f.read(256 * 4)

        # Read the pixel data
        pixel_data = f.read()

    # Calculate the width and height of the image from the header
    width = int.from_bytes(bmp_header[18:22], byteorder='little')
    height = int.from_bytes(bmp_header[22:26], byteorder='little')

    # Calculate the number of bytes per row (including padding)
    bytes_per_row = (width + 31) // 32 * 4

    # Create a new bytearray to store the 1-bit pixel data
    new_pixel_data = bytearray()

    # Iterate over each pixel row
    for row in range(height):
        # Get the start and end indices of the current row in the pixel data
        start_index = row * bytes_per_row
        end_index = start_index + bytes_per_row

        # Extract the pixels for the current row
        row_pixels = pixel_data[start_index:end_index]

        # Iterate over each pixel in the row
        for i in range(width):
            # Get the color index for the current pixel
            color_index = row_pixels[i // 8]

            # Calculate the bit position within the color index
            bit_position = 7 - (i % 8)

            # Extract the bit value (0 or 1) from the color index
            bit_value = (color_index >> bit_position) & 1

            # Append the bit value to the new pixel data
            new_pixel_data.append(bit_value)

    # Calculate the new size of the image and update the header
    new_file_size = 54 + 8 + len(new_pixel_data)
    bmp_header = bmp_header[:2] + new_file_size.to_bytes(4, byteorder='little') + bmp_header[6:]

    # Update the color palette to only contain two colors (black and white)
    new_color_palette = color_palette[:8] + color_palette[24:32]

    # Write the new BMP file with the 1-bit pixel data
    with open(output_file, 'wb') as f:
        f.write(bmp_header)
        f.write(new_color_palette)
        f.write(new_pixel_data)


# Usage example:
convert_8bit_to_1bit('Design.bmp', 'outputDesign8-1.bmp')

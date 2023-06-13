def read_bmp_file(file_path):
    with open(file_path, 'rb') as file:
        # Read the BMP header (14 bytes)
        header_data = file.read(14)
        # Extract relevant header information
        file_size = int.from_bytes(header_data[2:6], byteorder='little')
        pixel_data_offset = int.from_bytes(header_data[10:14], byteorder='little')

        # Move the file pointer to the pixel data
        file.seek(pixel_data_offset)

        # Read the DIB header size (4 bytes)
        dib_header_size_data = file.read(4)
        dib_header_size = int.from_bytes(dib_header_size_data, byteorder='little')

        # Read the DIB header
        dib_header_data = file.read(dib_header_size)
        width = int.from_bytes(dib_header_data[4:8], byteorder='little', signed=True)
        color_table_entries = int.from_bytes(dib_header_data[46:50], byteorder='little')

        # Calculate the row size in bytes, accounting for padding
        bytes_per_pixel = 1
        padding = (4 - (width * bytes_per_pixel) % 4) % 4
        row_size = (width * bytes_per_pixel + padding)

        # Read the color table
        color_table = []
        for _ in range(color_table_entries):
            color_entry = file.read(4)
            color_table.append(color_entry)

        # Read the pixel data
        while True:
            # Read a row of pixel data
            row_data = file.read(row_size)
            if len(row_data) == 0:
                break

            # Process each pixel in the row
            for i in range(width):
                # Read a byte
                index = row_data[i]

                # Extract the desired bit (e.g., the least significant bit)
                bit = (index >> 7) & 1  # Assuming the most significant bit represents the bit of interest

                # Process the bit as needed
                # (e.g., store it, manipulate it, convert to RGB, etc.)
                process_bit(bit)

    # Close the file
    file.close()

def process_bit(bit):
    # Placeholder function for processing a single bit
    print(bit)


# Example usage
bmp_file_path = 'Design.bmp'
read_bmp_file(bmp_file_path)

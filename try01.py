def read_file(file_path):
    with open(file_path, 'rb') as file:
        # Read the BMP file header
        header = file.read(54)
        
        # Read the color table
        color_table = file.read(256 * 4)  # Assuming an 8-bit BMP with a 256-color palette
        
        # Read the image data
        data = file.read()
        
    return header, color_table, data

def write_file(file_path):
    header, color_table, data = read_file(file_path)
    
    # Modify the color table data
    new_color_table = bytearray(color_table)
    # Modify the color entries as per your new color palette
    for i in range(256):
        # Update the RGB values for each color entry
        index = i * 4
        # Modify the RGB values to represent the new color palette
        # Example: Set all colors to shades of gray based on pixel value
        gray_value = i * 255 // 255  # Map the 8-bit pixel value to desired grayscale intensity
        new_color_table[index : index + 3] = bytes([gray_value, gray_value, gray_value])

    # Convert the pixel data to new color palette values
    new_data = bytearray()
    for byte in data:
        # Map the original pixel value to the corresponding index in the new color palette
        pixel_index = byte
        # Append the pixel value based on the new color palette
        new_data.append(pixel_index)

    output_path = file_path.split('.')[0] + '-2-.bmp'
    
    # Write the modified bytes to the output file
    with open(output_path, 'wb') as file:
        file.write(header)
        file.write(new_color_table)
        file.write(new_data)

write_file('Design.bmp')

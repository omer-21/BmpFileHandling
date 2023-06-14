from math import floor
#first we have to import the orijinal bmp file
def read_file_8(file_path):
    with open(file_path, 'rb') as file:
        # Read the BMP file header
        header = file.read(54)
        
        # Read the color table
        color_table = file.read(256 * 4)  # Assuming an 8-bit BMP with a 256-color palette
        
        # Read the image data
        data = file.read()
    return header, color_table, data

def read_file_1(file_path):
    with open(file_path, 'rb') as file:
        # Read the BMP file header
        header = file.read(54)
        
        # Read the color table
        color_table = file.read(2 * 4)  # Assuming an 8-bit BMP with a 256-color palette
        
        # Read the image data
        data = file.read()

    return header, color_table, data
def get_width(header):
    # Extract the width from the BMP header
    width_bytes = header[18:22]
    width = int.from_bytes(width_bytes, byteorder='little')
    return width
def get_height(header):
    # Extract the height from the BMP header
    height_bytes = header[22:26]
    height = int.from_bytes(height_bytes, byteorder='little')
    return height
def subtract_one(num):
    result = num - 1
    if result < 0:
        return 0
    else:
        return result

def write_file(file_path,weave_files):
    header, color_table, data = read_file_8(file_path)

    weaves=get_weave_images(weave_files)
    print(weaves)
    output_path = file_path.split('.')[0] + '-2-.bmp'    
    # Modify the color table data

    new_color_table = bytearray(color_table)
    new_color_table[0:16] = bytes([255, 255, 255,255, 0, 0,0,0  ,0, 0, 255,0, 255, 255, 0,0])
    for i in range(4,256):
        # Update the RGB values for each color entry
        index = i * 4
        new_color_table[index : index + 3] = bytes([0,0,0])

    # Convert the pixel data to new color palette values depend on the weave
    new_data = bytearray()
    dRow=0
    dColumn=0
    new_color_palette={1:'w12.bmp',2:'w22.bmp',3:'w32.bmp',4:'wave32.bmp'}
    org_w=get_width(header)
    org_h=get_height(header)
    for index, byte in enumerate(data):
        """if index==16:
            break"""
        if not(byte == 0):
            dRow=floor(index/org_w)
            dColumn=floor(index%org_h)
            weave_index = new_color_palette[byte]
            #weave_index='wave32.bmp'
            weave_data = weaves[weave_index][2]
            weave_w = get_width(weaves[weave_index][0])
            weave_h = get_height(weaves[weave_index][0])
            wColumn=dColumn % weave_w
            wRow=dRow % weave_h
            weave_xy=(weave_w*wRow+wColumn)
            weave_pixel=weave_data[weave_xy]
            new_data.append(weave_pixel)
            #new_data[index]=weave_pixel

    with open('newData.txt','w') as outTxt:
        print(header,'\n\n',new_data,file=outTxt)

    """# Update the header to reflect 1-bit depth
    header = bytearray(header)
    header[28:30] = bytes([1, 0])  # Set the biBitCount field to 1"""

    # Write the modified bytes to the output file
    with open(output_path, 'wb') as file:
        file.write(header)
        file.write(new_color_table)
        file.write(new_data)

    for index in range(len(weaves)):
        output_weave_path='weave'+str(index)+'2.bmp'
        weave=list(weaves.values())[index]
        with open(output_weave_path, 'wb') as file:
            file.write(weave[0])
            file.write(weave[1])
            file.write(weave[2])
def get_weave_images(file_paths):
    weaves={}
    for file in file_paths:
        weave1_header,weave1_color_palette,weave1_data=read_file_8(file)
        """
        new_color_table = bytearray(weave1_color_palette)
        new_color_table[0:8] = bytes([0, 0, 0, 0, 255, 255, 255, 0])
        for i in range(2,256):
            # Update the RGB values for each color entry
            index = i * 4
            new_color_table[index : index + 3] = bytes([0,0,0])
        # Update the header to reflect 1-bit depth
        weave1_header = bytearray(weave1_header)
        weave1_header[28:30] = bytes([8, 0])  # Set the biBitCount field to 1
        weave1_color_palette=new_color_table
        """
        weaves[file]=(weave1_header,weave1_color_palette,weave1_data)
    return weaves

write_file('Design.bmp',['w12.bmp','w22.bmp','w32.bmp','wave32.bmp'])

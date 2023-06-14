#first we have to import the orijinal bmp file
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
    waves=get_wave_images(['w1.bmp','w2.bmp','w3.bmp','w4.bmp'])
    print(waves)
    output_path = file_path.split('.')[0] + '-2-.bmp'    
    # Write the modified bytes to the output file
    with open(output_path, 'wb') as file:
        file.write(header)
        file.write(color_table)
        file.write(data)
    index=0
    for f in waves:
        f = f.split('.')[0] + '-2-.txt'    
        with open(output_path, 'w') as file:
            file.write(f)
            file.write(color_table)
            file.write(data)
def get_wave_images(file_paths):
    waves=[]
    for i in file_paths:
        wave1=(read_file(i))
        waves.append(wave1)
    return waves
write_file('Design.bmp')

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path

def parse_bmp(file_path):
    with open(file_path, 'rb') as f:
        # Read BMP header
        signature = f.read(2).decode('ascii')
        file_size = int.from_bytes(f.read(4), 'little')
        reserved_1 = int.from_bytes(f.read(2), 'little')
        reserved_2 = int.from_bytes(f.read(2), 'little')
        pixel_data_offset = int.from_bytes(f.read(4), 'little')

        # Read DIB header
        dib_header_size = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little', signed=True)
        height = int.from_bytes(f.read(4), 'little', signed=True)
        color_planes = int.from_bytes(f.read(2), 'little')
        bit_depth = int.from_bytes(f.read(2), 'little')
        compression_method = int.from_bytes(f.read(4), 'little')
        image_size = int.from_bytes(f.read(4), 'little')
        horizontal_resolution = int.from_bytes(f.read(4), 'little')
        vertical_resolution = int.from_bytes(f.read(4), 'little')
        colors_in_palette = int.from_bytes(f.read(4), 'little')
        important_colors = int.from_bytes(f.read(4), 'little')

        # Process pixel data
        f.seek(pixel_data_offset)

        # Calculate row padding
        row_size = ((bit_depth * width + 31) // 32) * 4
        padding = row_size - ((bit_depth * width) // 8)

        pixel_data = []
        for _ in range(abs(height)):
            row = []
            for _ in range(width):
                if bit_depth <= 24:
                    blue = ord(f.read(1))
                    green = ord(f.read(1))
                    red = ord(f.read(1))
                    row.append((red, green, blue))
                elif bit_depth == 32:
                    blue = ord(f.read(1))
                    green = ord(f.read(1))
                    red = ord(f.read(1))
                    alpha = ord(f.read(1))
                    row.append((red, green, blue, alpha))
                else:
                    raise ValueError("Unsupported bit depth")
            f.read(padding)  # Skip padding bytes
            pixel_data.append(row)

    # Create list of field information
    bmp_info = [
        ('Signature', 0, 2, signature.encode('ascii').hex(), signature),
        ('File Size', 2, 4, chr(file_size), file_size),
        ('Reserved 1', 6, 2, hex(reserved_1), reserved_1),
        ('Reserved 2', 8, 2, hex(reserved_2), reserved_2),
        ('Pixel Data Offset', 10, 4, hex(pixel_data_offset), pixel_data_offset),
        ('DIB Header Size', 14, 4, hex(dib_header_size), dib_header_size),
        ('Width', 18, 4, hex(width), width),
        ('Height', 22, 4, hex(height), height),
        ('Color Planes', 26, 2, hex(color_planes), color_planes),
        ('Bit Depth', 28, 2, hex(bit_depth), bit_depth),
        ('Compression Method', 30, 4, hex(compression_method), compression_method),
        ('Image Size', 34, 4, hex(image_size), image_size),
        ('Horizontal Resolution', 38, 4, hex(horizontal_resolution), horizontal_resolution),
        ('Vertical Resolution', 42, 4, hex(vertical_resolution), vertical_resolution),
        ('Colors in Palette', 46, 4, hex(colors_in_palette), colors_in_palette),
        ('Important Colors', 50, 4, hex(important_colors), important_colors)
    ]

    # Print field information as tab-separated values
    print("field_name,offset,size,value,hex")
    for field_info in bmp_info:
        field_name, offset, size, hex_value, value = field_info
        if isinstance(value, str):
            hex_value = ' '.join(f"{byte:02X}" for byte in value.encode())
        else:
            hex_value = ' '.join(f"{byte:02X}" for byte in value.to_bytes(size, 'little'))
        print(f"{field_name},{hex(offset)},{size},{value},{hex_value}")

    return pixel_data


root=Tk()
root.withdraw()

bmp_file_path = Path(askopenfilename(title='Select a bitmap file', initialdir='bmp_parser', filetypes=[('Bitmap files', '*.bmp'),('All files', '*.*')])) # shows dialog box and return the path

bmp_info = parse_bmp(bmp_file_path)
#print(f"Pixel Data: {pixel_data}")
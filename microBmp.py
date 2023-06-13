from microbmp import MicroBMP
import struct
import numpy as np

def parray_to_RGB_matrix(byte_array,height,width):
    result=[]
    for i in range(len(byte_array)//3):
        part=byte_array[i*3:i*3+3]
        #print(part)
        result.append(hex_to_rgb(part))
    #print(result)
    result=np.array(result).reshape(height,width,3)
    #print(result)
    return result

def hex_to_rgb(byte_array):
    # Convert the bytearray to a packed binary string
    binary_str = struct.pack('BBB', *byte_array)

    # Unpack the binary string as an RGB color tuple
    rgb_color = struct.unpack('BBB', binary_str)

    return rgb_color

def combine_waves(waves,colors,result,im,im_h,im_w):
    for i in range(im_h):
        for j in range(im_w):
            point_color=im[i,j]
            color_no=colors[point_color]
            wIm_h=waves[color_no].DIB_h
            wIm_w=waves[color_no].DIB_w
            result[i,j]=waves[color_no][i%wIm_h][j%wIm_w]

new_img= MicroBMP().load("Design.bmp")
colors={}
with open("Design2.txt","w") as f:
    """liste=new_img.palette
    i=0
    for item in liste:
        if not(item==b'\x00\x00\x00'):
            rgb_color = hex_to_rgb(item)
            print(rgb_color)
            colors[rgb_color]=i
            i=i+1
    print(colors,file=f)"""
    print(new_img.parray,file=f)
wave_files=['w1.bmp','w2.bmp','w3.bmp','w4.bmp']
waves={}

for index in range(len(wave_files)):
    wave_name=wave_files[index]
    img=MicroBMP().load(wave_name)
    waves[index]=img
result=MicroBMP(new_img.DIB_h,new_img.DIB_w,1)

new_img_data=parray_to_RGB_matrix(new_img.parray,new_img.DIB_h,new_img.DIB_w)
combine_waves(waves,result,colors,new_img_data,new_img.DIB_h,new_img.DIB_w)

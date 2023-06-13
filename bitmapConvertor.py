from PIL import Image
import numpy as np


def combine_images(images, im):
    pix=im.load()
    m, n = im.size
    data = np.zeros((m, n), dtype=np.uint8)#alan azaltmak için (m,n,3) yerine (m,n) yaz
    for i in range(m):
        for j in range(n):
            data_point = None###

            if pix[i,j] != 0: ###
                img_index = pix[i,j] - 1
                img = images[img_index]
                img_m, img_n = img.size
                data_point = img.load()[i % img_m, j % img_n]
            if data_point: ###
                data[i, j] = np.array(data_point) * 255
    return data

# örnek kullanım
im = Image.open("Design.bmp") # resim dosyasını yükle
# --------------------- döngü olabilir -----------
im1 = Image.open("w1.bmp") # desen dosyasını yükle
im2 = Image.open("w2.bmp") # desen dosyasını yükle
im3 = Image.open("w3.bmp") # desen dosyasını yükle
im4 = Image.open("w4.bmp") # desen dosyasını yükle
# renk sırasıyla aynı olmalı 
data = combine_images([im1, im2, im3, im4], im) # daha fazla özelleştirmek için map kullanabilirsin

bitmap = Image.new("1", (data.shape[1], data.shape[0]), color=0)
bitmap.putdata(data.flatten())
bitmap.save("1_bit.bmp")
# show image
#bitmap.show()

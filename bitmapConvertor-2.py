
from PIL import Image
import numpy as np

im = Image.open("Design2.bmp") # resim dosyasını yükle
# --------------------- döngü olabilir -----------
im1 = Image.open("w1.bmp") # desen dosyasını yükle
im2 = Image.open("w2.bmp") # desen dosyasını yükle
im3 = Image.open("w3.bmp") # desen dosyasını yükle
im4 = Image.open("w4.bmp") # desen dosyasını yükle
# desen listesi alındı  ------------------------------

m, n = im.size
pix = im.load() # pixel bilgilerini yükle

m1, n1 = im1.size
pix1 = im1.load() # pixel bilgilerini yükle

m2, n2 = im2.size
pix2 = im2.load() # pixel bilgilerini yükle

m3, n3 = im3.size
pix3 = im3.load() # pixel bilgilerini yükle

m4, n4 = im4.size
pix4 = im4.load() # pixel bilgilerini yükle

data = np.zeros((m,n), dtype=np.uint8)

renkler = dict() # farklı renk sayılarını burada tutacağız
def yaz(i,j):
    if(pix[i,j]==4):
        data[i,j]=pix1[i%m1,j%n1]*255
    elif(pix[i,j]==251):
        data[i,j]=pix2[i%m2,j%n2]*255
    elif(pix[i,j]==40):
        data[i,j]=pix3[i%m3,j%n3]*255
    else:
        data[i,j]=pix4[i%m4,j%n4]*255

color_num = -1
for i in range(m):
    for j in range(n):
        yaz(i,j)
        renk = pix[i,j]

bitmap = Image.new("1", (data.shape[1], data.shape[0]), color=0)
bitmap.putdata(data.flatten())
bitmap.save("1_bitV2.bmp")
# show image
bitmap.show()

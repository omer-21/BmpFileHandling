from PIL import Image
import numpy as np

im = Image.open("Design.bmp") # resim dosyasını yükle
m, n = im.size
data = np.zeros((m,n, 3), dtype=np.uint8)
pix = im.load() # pixel bilgilerini yükle

renkler = dict() # farklı renk sayılarını burada tutacağız

color_num = -1
for i in range(m):
    for j in range(n):
        #print(pix[i,j])
        if(pix[i,j]==4):
            data[i,j]=[255,255,0]
        elif(pix[i,j]==251):
            data[i,j]=[255,0,0]
        elif(pix[i,j]==247):
            data[i,j]=[0,255,0]
        else:
            data[i,j]=[155,155,155]
        renk = pix[i,j]
        if renk in renkler:
            pass
        else:
            renkler[renk] = color_num +1
            color_num +=1

# her rengin sayısını yazdır
for renk, sayi in renkler.items():
    print(renk, sayi)

    
img = Image.fromarray(data)

# save image as bmp
img.save("img2.bmp")

# show image
img.show()
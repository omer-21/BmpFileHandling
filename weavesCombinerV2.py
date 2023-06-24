from PIL import Image
import numpy as np
import math

def lcm(numbers):
    lcm_result = 1
    for num in numbers:
        lcm_result = (lcm_result * num) // math.gcd(lcm_result, num)
    return lcm_result

def save_bmp(data,name):
    bitmap = Image.new("1", (data.shape[1], data.shape[0]), color=0)
    bitmap.putdata(data.flatten())
    #rName='rotatedImage.bmp'
    #bitmap.save(name)
    bitmap.rotate(180).save(name)
    #bitmap.show()

a1=Image.open('2-1.bmp')
b1=Image.open('m3 1bit.bmp')
a2=Image.open('2-1.bmp')
b2=Image.open('m3 1bit.bmp')
#print(a.load()[0,0])
pixels = b2.load()

# Print pixel values
for y in range(b2.size[0]):
    for x in range(b2.size[1]):
        print(pixels[x, y])

#a=[[1,0],[0,1]]
#b=[[1,0,0],[0,1,0],[0,0,1]]
weaves=[a1,a2]
sequenceX=[1,1,2]
sequenceY=[1]
seqXSize=len(sequenceX)
seqYSize=len(sequenceY)
sequenceXDict={1:a1,2:b1}
sequenceYDict={1:a2,2:b2}
resultH=seqXSize*lcm([a1.size[0],b1.size[0],a2.size[0],b2.size[0]])
resultW=seqYSize*lcm([a1.size[1],b1.size[1],a2.size[1],b2.size[1]])

result=np.zeros((resultH,resultW),dtype=int)
indexesX={1:0,2:0}
indexesY={1:0,2:0}
for i in range(resultH):
    for j in range(resultW):
        #weave=sequenceDict[sequenceX[i%seqXSize]]
        wX=sequenceX[i%seqXSize]
        wY=sequenceY[j%seqYSize]
        weave=weaves[wX-1][wY-1]
        x=indexesX[sequenceX[i%seqXSize]]%weave.size[0]
        y=indexesY[sequenceY[j%seqYSize]]%weave.size[1]
        #result[i][j]=0 if weave.load()[x,y] > 0 else 1
        result[i][j]=weave.load()[x,y]
        indexesY[sequenceX[j%seqYSize]]=(indexesY[sequenceY[j%seqYSize]]+1)%weave.size[1]
    indexesX[sequenceX[i%seqXSize]]=(indexesX[sequenceX[i%seqXSize]]+1)%weave.size[0]
print(result)
save_bmp(result,'combined_weaves12.bmp')
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
    bitmap=bitmap.rotate(180)
    bitmap.save(name)
    bitmap.show()

a=Image.open('2-1.bmp')
b=Image.open('m3 1bit.bmp')
#print(a.load()[0,0])
#print(b.load())
#a=[[1,0],[0,1]]
#b=[[1,0,0],[0,1,0],[0,0,1]]

sequenceX=[1,1,2]
seqSize=len(sequenceX)
sequenceDict={1:a,2:b}
resultH=seqSize*lcm([a.size[0],b.size[0]])
resultW=lcm([a.size[1],b.size[1]])

result=np.zeros((resultH,resultW),dtype=int)
indexes={1:0,2:0}
for i in range(resultH):
    for j in range(resultW):
        weave=sequenceDict[sequenceX[i%seqSize]]
        x=indexes[sequenceX[i%seqSize]]
        y=j%weave.size[0]
        #result[i][j]=0 if weave.load()[x,y] > 0 else 1
        result[i][j]=weave.load()[x,y]
    indexes[sequenceX[i%seqSize]]=(indexes[sequenceX[i%seqSize]]+1)%weave.size[1]
print(result)
save_bmp(result,'combined_weaves1.bmp')
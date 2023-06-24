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
b=Image.open('2-1.bmp')
#print(a.load()[0,0])
#print(b.load())
#a=[[1,0],[0,1]]
#b=[[1,0,0],[0,1,0],[0,0,1]]

sequenceX=[1,2]
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

"""
The second operation
"""

a2=Image.open('m3 1bit.bmp')
b2=Image.open('m3 1bit.bmp')
#print(a.load()[0,0])
#print(b.load())
#a=[[1,0],[0,1]]
#b=[[1,0,0],[0,1,0],[0,0,1]]

sequence2X=[1,2]
seqSize2=len(sequence2X)
sequenceDict2={1:a2,2:b2}
result2H=seqSize2*lcm([a2.size[0],b2.size[0]])
result2W=lcm([a2.size[1],b2.size[1]])

result2=np.zeros((result2H,result2W),dtype=int)
indexes2={1:0,2:0}
for i in range(result2H):
    for j in range(result2W):
        weave=sequenceDict2[sequence2X[i%seqSize2]]
        x=indexes2[sequence2X[i%seqSize2]]
        y=j%weave.size[0]
        #result2[i][j]=0 if weave.load()[x,y] > 0 else 1
        result2[i][j]=weave.load()[x,y]
    indexes2[sequence2X[i%seqSize2]]=(indexes2[sequence2X[i%seqSize2]]+1)%weave.size[1]
print(result2)
save_bmp(result2,'combined_weaves2.bmp')


"""
The Third operation
"""

a3=Image.open('combined_weaves1.bmp')
b3=Image.open('combined_weaves2.bmp')
#print(a.load()[0,0])
#print(b.load())
#a=[[1,0],[0,1]]
#b=[[1,0,0],[0,1,0],[0,0,1]]

sequenceY=[1,2]
seqSize3=len(sequenceY)
sequenceDict3={1:a3,2:b3}
result3H=seqSize3*lcm([a3.size[1],b3.size[1]])
result3W=seqSize3*lcm([a3.size[0],b3.size[0]])

result3=np.zeros((result3H,result3W),dtype=int)
indexes3={1:0,2:0}
for i in range(result3H):
    #indexes3={1:0,2:0}
    for j in range(result3W):
        weave=sequenceDict3[sequenceY[j%seqSize3]]
        y=indexes3[sequenceY[j%seqSize3]]
        x=i%weave.size[0]
        #result2[i][j]=0 if weave.load()[x,y] > 0 else 1
        result3[i][j]=weave.load()[x,y]
    indexes3[sequenceY[j%seqSize3]]=(indexes3[sequenceY[j%seqSize3]]+1)%weave.size[1]
print(result3)
save_bmp(result3,'combined_weaves3.bmp')

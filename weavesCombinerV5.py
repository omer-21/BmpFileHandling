from PIL import Image
import numpy as np
import math
#ekok
def lcm(numbers):
    lcm_result = 1
    for num in numbers:
        lcm_result = (lcm_result * num) // math.gcd(lcm_result, num)
    return lcm_result
def get_images(file_paths):
    weaves=[]
    for file in file_paths:
        im1 = Image.open(file)
        weaves.append(im1)
    return weaves

def save_bmp(data,name):
    bitmap = Image.new("1", (data.shape[1], data.shape[0]), color=0)
    bitmap.putdata(data.flatten())
    #rName='rotatedImage.bmp'
    #bitmap.save(name)
    bitmap=bitmap.rotate(180)
    bitmap.save(name)
    bitmap.show()

def combine_weaves(weave_paths=['nu1.bmp','nu2.bmp'],sequenceX=[1,1,2,2]):
    weav_files=get_images(weave_paths)
    seqSize = len(sequenceX)
    oran=[]
    sequenceDict={}
    indexes={}
    for index,x  in enumerate(weav_files):
        sequenceDict[index+1]=x
        oran.append(lcm([x.size[1],sequenceX.count(index+1)])//sequenceX.count(index+1)) #1
        indexes[index+1]=0

    sonuc=lcm(oran) #3 
    resultH=seqSize*sonuc
    resultW=lcm([i.size[0] for i in weav_files]) ###
    result=np.zeros((resultH,resultW),dtype=int)
    #last update:swapped x and y
    for i in range(resultH):
        weave=sequenceDict[sequenceX[i%seqSize]]
        for j in range(resultW):
            y=indexes[sequenceX[i%seqSize]]
            print(weave.size)
            x=j%weave.size[0]
            #result[i][j]=0 if weave.load()[x,y] > 0 else 1
            value=weave.load()[x,y]
            result[i][j]=value
        indexes[sequenceX[i%seqSize]]=(indexes[sequenceX[i%seqSize]]+1)%weave.size[1]
    print(result)
    save_bmp(result,'combined_weaves.bmp')
if __name__=='__main__':
    combine_weaves()
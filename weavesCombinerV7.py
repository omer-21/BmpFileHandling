from PIL import Image
import numpy as np
from math import ceil, gcd,floor
#ekok
def lcm(numbers):
    lcm_result = 1
    for num in numbers:
        lcm_result = (lcm_result * num) // gcd(lcm_result, num)
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
    #bitmap=bitmap.rotate(180)
    bitmap.save(name)
    bitmap.show()

def get_weave_matrix(seqX,seqY):
    result=np.zeros((len(seqY),len(seqX)),dtype=np.uint8)
    for j in seqY:
        for i in seqX:
            result[i,j]

def combine_weaves_2d(weave_paths=['nu1.bmp','nu2-i.bmp','nu2.bmp','nu1-i.bmp'],weaves_dim=(2,2),sequenceX=[1,1,2],sequenceY=[1,2]):
    weave_files=get_images(weave_paths)
    seqXSize = len(sequenceX)
    seqYSize = len(sequenceY)
    oranH=[]
    oranW=[]
    sequenceDict={}
    indexes={}
    for index,x  in enumerate(weave_files):
        sequenceDict[index+1]=x
        lcm_v=lcm([x.size[1],sequenceX.count(index%weaves_dim[1]+1)])
        oranH.append(lcm_v//sequenceX.count((index%weaves_dim[1]+1))) #1
        lcm_v=lcm([x.size[0],sequenceY.count((index%weaves_dim[0]+1))])
        oranW.append(lcm_v//sequenceY.count((index%weaves_dim[0]+1))) #1
        indexes[index+1]=[0,0]
        #indexes[index+1]=0
    sonucH=lcm(oranH) #3 
    sonucW=lcm(oranW) #3 
    resultH=seqXSize*sonucH
    resultW=seqYSize*sonucW
    result=np.zeros((resultH,resultW),dtype=np.uint8)
    #last update:swapped x and y
    for i in range(resultH):
        for j in range(resultW):
            x_index=sequenceX[j%seqXSize]
            y_index=sequenceY[i%seqYSize]-1
            print(x_index,y_index)
            wn=int((x_index+(y_index)*(resultW/(resultW/2))))
            #wn=int((x_index+(y_index)*(resultW/(resultW/2))))
            #wn = int((y_index + (x_index-1) * seqYSize) % (weaves_dim[0] * weaves_dim[1]))
            weave = sequenceDict[wn]
            #x, y = indexes[wn]
            x=floor(j/seqXSize)%weave.size[0]
            y=floor(i/seqYSize)%weave.size[1]
            print(wn,'(',x,',',y,')',',','(',j,',',i,')')
            value = weave.load()[x, y]
            result[j, i-int(resultH/2)] =np.array(value)*255
            #indexes[wn][0]=(indexes[wn][0]+1)%weave.size[1]
            #if i%weave.size[0]==1:
            #indexes[wn][1]=j%weave.size[0]
    print(result)
    save_bmp(result,'combined_weaves_2d.bmp')
if __name__=='__main__':
    combine_weaves_2d()
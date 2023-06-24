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
    #bitmap=bitmap.rotate(180)
    bitmap.save(name)
    bitmap.show()

def combine_weaves_y(weave_paths=['nu1.bmp','nu2.bmp'],weaves_dim=(1,2),sequenceY=[1,2]):
    weave_files=get_images(weave_paths)
    seqYSize = len(sequenceY)
    oranH=[]
    oranW=[]
    sequenceDict={}
    indexes={}
    for index,x  in enumerate(weave_files):
        sequenceDict[index+1]=x
        lcm_v=lcm([x.size[0],sequenceY.count((index%weaves_dim[0]+1))])
        oranW.append(lcm_v//sequenceY.count((index%weaves_dim[0]+1))) #1
        indexes[index+1]=[0,0]
    sonucH=lcm(oranH) #3 
    sonucW=lcm(oranW) #3 
    resultH=2
    resultW=seqYSize*sonucW
    result=np.zeros((resultH,resultW),dtype=int)
    #last update:swapped x and y
    for i in range(resultH):
        wn=0
        y_index=sequenceY[i%seqYSize]-1
        for j in range(resultW):
            x_index=sequenceX[j%seqXSize]
            wn=int((x_index+(y_index)*(resultW/(resultW/2))))
            weave=sequenceDict[wn]
            y=indexes[wn][1]%weave.size[1]
            x=indexes[wn][0]%weave.size[0]
            print(x,y)
            #result[i][j]=0 if weave.load()[x,y] > 0 else 1
            value=weave.load()[x,y]
            result[i][j]=value
            indexes[wn][0]=(indexes[wn][0]+1)#%weave.size[1]
            if j%i==0:
                indexes[wn][1]=(indexes[wn][1]+1)#%weave.size[0]
    print(result)
    save_bmp(result,'combined_weaves_2d.bmp')
if __name__=='__main__':
    combine_weaves_y()
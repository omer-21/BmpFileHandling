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
def get_key(my_dict,search_value):
    for key, value in my_dict.items():
        if value == search_value:
            return  key

def get_weave_matrix(seqX,seqY):
    result=np.zeros((len(seqX),len(seqY)),dtype=int)
    print((len(seqY),len(seqX)))
    seq_d={}
    counter=0
    for x,j in enumerate(seqX):
        for y,i in enumerate(seqY):
            if [i,j] not in seq_d.values():
                seq_d[counter]=[i,j]#counter +1
                counter+=1

                result[-x-1,y]=counter
            else:
                result[-x-1,y]= get_key(seq_d,[i,j])+1
    print(result)
    return result

def get_indexes_matrix(seqX,seqY,width,height):
    seqXSize=len(seqX)
    seqYSize=len(seqY)
    dtype = np.dtype([('x', int), ('y', int)])
    resultM=np.zeros((height,width),dtype=dtype)

    counteri=2
    for i in range(height):
        for j in range(width):
            resultM[i,j]=(j//seqYSize,(i+(1%counteri))//seqXSize)
            #resultM[j,i]=int(str(i)+str(j))
        counteri+=1
    print(resultM)
    return resultM
def get_seq_matrix(seqX,seqY,w,h):
    result=np.zeros((w,h),dtype=np.uint8)
    seqX=seqX*(h/len(seqX))
    seqY=seqY*(h/len(seqY))
    for i in seqX:
        for j in seqY:
            result[i,j]=(j,j)
    print(result)
def combine_weaves_2d(weave_paths=['1-1.bmp','1-2.bmp','1-3.bmp','2-1.bmp','2-2.bmp','2-3.bmp'],weaves_dim=(3,2),sequenceX=[1,1,2],sequenceY=[1,2,3]):
    #seq_matrix=get_weave_matrix(sequenceX,sequenceY)
    weave_files=get_images(weave_paths)
    seqXSize = len(sequenceX)
    seqYSize = len(sequenceY)
    oranH=[]
    oranW=[]
    sequenceDict={}
    #indexes=np.zeros((weaves_dim[0],weaves_dim[1],2),dtype=np.uint8)
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
    seq_matrix=get_seq_matrix(sequenceX,sequenceY,resultW,resultH)
    #indexes_m=get_indexes_matrix(sequenceX,sequenceY,resultW,resultH)
    #last update:swapped x and y
    for i in range(resultH):
        for j in range(resultW):
            #x_index=sequenceX[j%seqXSize]
            #y_index=sequenceY[i%seqYSize]-1
            #print(x_index,y_index)
            wn=seq_matrix[i%seqXSize,j%seqYSize]

            #wn=int((x_index+(y_index)*(resultW/(resultW/2))))
            #wn = int((y_index + (x_index-1) * seqYSize) % (weaves_dim[0] * weaves_dim[1]))

            weave = sequenceDict[wn]

            #y=list(seq_matrix[j1][:i1]).count(wn)%weave.size[1] # başvuru sayısı
            #x=list(seq_matrix[i1][:j1]).count(wn)%weave.size[0] # başvuru sayısı
            #x=(weave.size[0]*indexes[wn]+j)%weave.size[0]
            #y=(weave.size[1]*indexes[wn]+i)%weave.size[1]

            #x=(j//(3))%weave.size[0]
            #y=(i//(2))%weave.size[1]
            #x,y=indexes_m[i,j]
            x=indexes[wn][0]%weave.size[0]
            y=indexes[wn][1]%weave.size[1]
            value = weave.load()[x,y]
            #print(wn,'(',x,',',y,')',',','(',j,',',i,')')

            #result[j, i-int(resultH/2)] =np.array(value)*255
            result[i,j] =np.array(value)*255
            indexes[wn][0]+=1
            for ind in range(((wn//weaves_dim[0])*weaves_dim[0]+1)%(weaves_dim[0]*weaves_dim[1]),(wn//weaves_dim[0])*weaves_dim[0]+weaves_dim[0]+1):
                print(ind)
                #indexes[ind][1]+=1
    print(result)
    save_bmp(result,'combined_weaves_2d.bmp')
if __name__=='__main__':
    combine_weaves_2d()
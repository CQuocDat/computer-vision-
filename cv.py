import cv2
import numpy as np
import math
import random
###########################################-->>Function<<--###########################################
def findNeighbour(dong, cot, seamTable,h,w):
    if cot>0 and cot<w-1:
        x=min(seamTable[dong-1,cot-1],seamTable[dong-1,cot],seamTable[dong-1,cot+1])
        if x==seamTable[dong-1,cot-1]:
            return dong-1,cot-1
        if x==seamTable[dong-1,cot]:
            return dong-1,cot
        if x==seamTable[dong-1,cot+1]:
            return dong-1,cot+1
    if cot==0:
        x=min(seamTable[dong-1,cot],seamTable[dong-1,cot+1])
        if x==seamTable[dong-1,cot]:
            return dong-1,cot
        if x==seamTable[dong-1,cot+1]:
            return dong-1,cot+1
    if cot==w-1:
        x=min(seamTable[dong-1,cot-1],seamTable[dong-1,cot])
        if x==seamTable[dong-1,cot-1]:
            return dong-1,cot-1
        if x==seamTable[dong-1,cot]:
            return dong-1,cot
def S(energyArr2D,dong,cot):#Return seamline

    seamTable=np.array(energyArr2D)
    for i in range(1,dong):
        for j in range(0,cot):
            if j==0:
                seamTable[i,j]=float(seamTable[i,j])+min(float(seamTable[i-1,j]),float(seamTable[i-1,j+1]))
            if j==cot-1:
                seamTable[i,j]=float(seamTable[i,j])+min(float(seamTable[i-1,j-1]),float(seamTable[i-1,j]))
            if j<0 and j<cot-1:
                seamTable[i,j]=float(seamTable[i,j])+min(float(seamTable[i-1,j-1]),float(seamTable[i-1,j]),float(seamTable[i-1,j+1]))
    # had seamTable 

    seam_sort=np.sort(seamTable[dong-1])
    min_=seam_sort[0]
    cot_=-1
    #for ii in range (0,cot):
    while(1):
        i=random.randint(0,cot-1)
        if seamTable[dong-1,i]==min_:
            cot_=i
            break
    # had the smallest value and position x,y of first pixel belong to seamTable

    seamArr=[]
    dong_=dong-1
    while(dong_>=0):
        row,col=findNeighbour(dong_,cot_,seamTable,dong,cot)
        seamArr.append([row,col])
        dong_=row
        cot_=col
    return seamArr
###########################################-->>Initiate<<--###########################################
###########################################-->>Initiate<<--###########################################
rawImage=cv2.imread('birds.jpg',0)
H,W=rawImage.shape
print H,W

myImage=np.array(rawImage)    #grayscale
energyArr2D=np.array(rawImage)#linelike
testImage=np.array(rawImage)
###########################################-->>Execute <<--###########################################
#newH=raw_input('input new height: ')
newH=raw_input('input new  Height: ')
newW=raw_input('input new  Width: ')

deltaX=int(newW)-int(W)
deltaH=int(newH)-int(H)
#for x co anh
if deltaX<0: # shorter
    d=abs(deltaX)
    while(d>0):
        #calculate energy
        h,w=myImage.shape

        #energyArr2D=cv2.Canny(myImage,100,5)
        for i in range(1,h-1):
            for j in range(1,w-1):
                x=(float(myImage[i,j+1])-float(myImage[i,j-1]))*3
                y=(float(myImage[i+1,j])-float(myImage[i-1,j]))*3
                energyArr2D[i,j]=math.sqrt(x*x+y*y)
        
        seam_arr=S(energyArr2D,h,w)

        py_image = [[0 for x in range(w)] for y in range(h)]
        py_energy = [[0 for x in range(w)] for y in range(h)]
        for i in range(0,h):
            for j in range(0,w):
                py_image[i][j]=myImage[i][j]
                py_energy[i][j]=energyArr2D[i][j]
        for pixel in seam_arr:
            y=pixel[0]
            x=pixel[1]
            testImage[y][x]=0
            del py_image[y][x]
            del py_energy[y][x]
        myImage=np.array(py_image)
        energyArr2D=np.array(py_energy)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d=d-1

if deltaH<0:
    r=abs(deltaH)
    rot_myImage=np.rot90(myImage)
    rot_energyArr2D=np.rot90(energyArr2D)
    while(r>0):
        #calculate energy
        h,w=rot_myImage.shape

        for i in range(1,h-1):
            for j in range(1,w-1):
                x=(float(rot_myImage[i,j+1])-float(rot_myImage[i,j-1]))
                y=(float(rot_myImage[i+1,j])-float(rot_myImage[i-1,j]))
                rot_energyArr2D[i,j]=math.sqrt(x*x+y*y)

        seam_arr=S(rot_energyArr2D,h,w)

        py_image = [[0 for x in range(w)] for y in range(h)]
        py_energy = [[0 for x in range(w)] for y in range(h)]
        for i in range(0,h):
            for j in range(0,w):
                py_image[i][j]=rot_myImage[i][j]
                py_energy[i][j]=rot_energyArr2D[i][j]

                
        for pixel in seam_arr:
            y=pixel[0]
            x=pixel[1]
            #testImage[y][x]=0
            del py_image[y][x]
            del py_energy[y][x]
        rot_myImage=np.array(py_image)
        rot_energyArr2D=np.array(py_energy)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        r=r-1
    myImage=np.rot90(rot_myImage,3)
    energyArr2D=np.rot90(rot_energyArr2D,3)

if deltaX>0: 
    dd=abs(deltaX)
    while(dd>0):
        #calculate energy
        h,w=myImage.shape
        #energyArr2D=cv2.Laplacian(myImage,cv2.CV_64F)
        
        for i in range(1,h-1):
            for j in range(1,w-1):
                x=3*(float(myImage[i,j+1])-float(myImage[i,j-1]))
                y=3*(float(myImage[i-1,j])-float(myImage[i+1,j]))
                energyArr2D[i,j]=math.sqrt(x*x+y*y)
        
        seam_arr=S(energyArr2D,h,w)

        
        py_image=cv2.resize(myImage, dsize=(w+1, h), interpolation=cv2.INTER_CUBIC)
        py_energy=cv2.resize(energyArr2D, dsize=(w+1, h), interpolation=cv2.INTER_CUBIC)
        
        for pixel in seam_arr:
            dong_=pixel[0]
            cot_=pixel[1]
            
            for j in range(0,w):
                py_image[dong_,j]=myImage[dong_,j]
                
                if j==cot_:
                    py_image[dong_,j]=(float(myImage[dong_,cot_-1])+float(myImage[dong_,cot_+1]))/2
                    for jj in range(j+1,w):
                        py_image[dong_,jj]=myImage[dong_,jj-1]
                    break

        myImage=np.array(py_image)
        energyArr2D=np.array(py_energy)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        dd=dd-1


if deltaH>0:
    dd=abs(deltaH)
    rot_myImage=np.rot90(myImage)
    rot_energyArr2D=np.rot90(energyArr2D)
    while(dd>0):
        #calculate energy
        h,w=rot_myImage.shape
        
        for i in range(1,h-1):
            for j in range(1,w-1):
                x=(float(rot_myImage[i,j+1])-float(rot_myImage[i,j-1]))
                y=(float(rot_myImage[i-1,j])-float(rot_myImage[i+1,j]))
                rot_energyArr2D[i,j]=math.sqrt(x*x+y*y)
        
        seam_arr=S(rot_energyArr2D,h,w)

        py_image=cv2.resize(rot_myImage, dsize=(w+1, h), interpolation=cv2.INTER_CUBIC)
        py_energy=cv2.resize(rot_energyArr2D, dsize=(w+1, h), interpolation=cv2.INTER_CUBIC)
    
        for pixel in seam_arr:
            dong_=pixel[0]
            cot_=pixel[1]
            
            for j in range(0,w):
                py_image[dong_,j]=rot_myImage[dong_,j]
                
                if j==cot_:
                    py_image[dong_,j]=(float(rot_myImage[dong_,cot_-1])+float(rot_myImage[dong_,cot_+1]))/2
                    for jj in range(j+1,w):
                        py_image[dong_,jj]=rot_myImage[dong_,jj-1]
                    break

        rot_myImage=np.array(py_image)
        rot_energyArr2D=np.array(py_energy)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        dd=dd-1
    myImage=np.rot90(rot_myImage,3)
    energyArr2D=np.rot90(rot_energyArr2D,3)


aa,bb=myImage.shape
print aa,bb

######################################################################################################
cv2.imshow('my Image', myImage)
#cv2.imshow('energy Image', energyArr2D)
cv2.imshow('raw Image', rawImage)


cv2.waitKey(0)
cv2.destroyAllWindows()
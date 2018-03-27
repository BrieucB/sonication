#!/usr/bin/python
# -*- coding: utf-8 -*-
####
#Created on Thu Jan 18 15:26:31 2018

#@author: brieuc

#Purpose : create a file containing several fields, for each fixation point :

# INPUT : spline_empty.dat, $file.jpg
# OUPUT : datafile.dat, colors.dat
####

import numpy as np
from skimage import io, color
import webcolors
import math as m
import sys

image1=sys.argv[1]

num_lines = sum(1 for line in open('spline_empty.dat'))
num_lines/=2

f_in=open("spline_empty.dat", "r")
f_out=open("datafile.dat", "w")
f_out2=open("colors.dat", "w")


#f_out.write("#| x | y | time (ms) | time spent (ms) |  brightness (0-100) | panoramic (%) | speed | (red, orange, yellow, green, blue, purple) rate |\n\n")

time=[]
brightness=[]
pos=[]
speed=[]
red_rate=[]
orange_rate=[]
yellow_rate=[]
green_rate=[]
blue_rate=[]
purple_rate=[]
X=[]
Y=[]
C_list=[]

red=0
orange=np.pi/4
yellow=np.pi/2
green=np.pi
blue=-np.pi/2
purple=-np.pi/4

delta_col=np.pi/2
bp=0.5

red_min=red-delta_col
red_max=red+delta_col
orange_min=orange-delta_col
orange_max=orange+delta_col
yellow_min=yellow-delta_col
yellow_max=yellow+delta_col
green_min=green-delta_col
green_max=green+delta_col
blue_min=blue-delta_col
blue_max=blue+delta_col
purple_min=purple-delta_col
purple_max=purple+delta_col


rgb = io.imread(image1)
lab = color.rgb2lab(rgb)

x_old=0
y_old=0
for line in f_in:
    w=line.split()
    if(w!=[]):
        x=int(float(w[1])) # pixel x coordinate
        y=int(float(w[2])) # pixel y coordinate
        X.append(x)
        Y.append(y)
            
        t=float(w[0])
        time.append(t)
            
        speed.append(np.sqrt((x-x_old)*(x-x_old)+(y-y_old)*(y-y_old)))
            
        Lstar=lab[-y][x][0]
        astar=lab[-y][x][1]
        bstar=lab[-y][x][2]
        
        r=rgb[-y][x][0]
        g=rgb[-y][x][1]
        b=rgb[-y][x][2]
        
        
        theta=m.atan2(bstar,astar)
        C=np.sqrt(astar*astar+bstar*bstar)
        f_out2.write(str(r))
        f_out2.write(" ")
        f_out2.write(str(g))
        f_out2.write(" ")
        f_out2.write(str(b))
        f_out2.write(" ")
        f_out2.write(str(theta))
        f_out2.write(" ")
        f_out2.write(str(C))
        f_out2.write("\n")
        
        if((theta>=red_min)&(theta<=red_max)):
            sigma=bp*m.fabs(red_max-red_min)/2
            mu=(red_max+red_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            red_rate.append(value)
        else:
            red_rate.append(0)
            
        if((theta>=orange_min)&(theta<=orange_max)):
            sigma=bp*m.fabs(orange_max-orange_min)/2
            mu=(orange_max+orange_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            orange_rate.append(value)
        else:
            orange_rate.append(0)
            
        if((theta>=yellow_min)&(theta<=yellow_max)):
            sigma=bp*m.fabs(yellow_max-yellow_min)/2
            mu=(yellow_max+yellow_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            yellow_rate.append(value)
        else:
            yellow_rate.append(0)
            
        if((theta>=green_min)&(theta<=green_max)):
            sigma=bp*m.fabs(green_max-green_min)/2
            mu=(green_max+green_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            green_rate.append(value)
        else:
            green_rate.append(0)
            
        if((theta>=blue_min)&(theta<=blue_max)):
            sigma=bp*m.fabs(blue_max-blue_min)/2
            mu=(blue_max+blue_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            blue_rate.append(value)
        else:
            blue_rate.append(0)
        
        if((theta>=purple_min)&(theta<=purple_max)):
            sigma=bp*m.fabs(purple_max-purple_min)/2
            mu=(purple_max+purple_min)/2
            value=100.*m.exp(-(theta-mu)*(theta-mu)/(2*sigma*sigma))
            purple_rate.append(value)
        else:
            purple_rate.append(0)
                       
        brightness.append(Lstar)
        C_list.append(C)
        
        x_old=x
        y_old=y
                
    
M=max(X)
m=min(X)
pan_min=0.0
pan_max=127.0
pente=(pan_min-pan_max)/(m-M)
ordo=pan_max-pente*M
pos=[]
for k in range(num_lines):
	pos.append(pente*X[k] + ordo)
	
T=0
for k in range(num_lines):
    if(k<num_lines-1):
        dt=time[k+1]-time[k]
    else:
        dt=1000
    	
    f_out.write(str(X[k]))
    f_out.write(" ")
    f_out.write(str(Y[k]))
    f_out.write(" ")
    f_out.write(str(float(T)))
    f_out.write(" ")
    f_out.write(str(dt))
    f_out.write(" ")
    f_out.write(str(int(brightness[k])))
    f_out.write(" ")
    f_out.write(str(int(pos[k])))
    f_out.write(" ")
    f_out.write(str(int(speed[k])))
    f_out.write(" ")
    f_out.write(str(int(red_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(orange_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(yellow_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(green_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(blue_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(purple_rate[k])))
    f_out.write(" ")
    f_out.write(str(int(C_list[k])))
    f_out.write("\n")
    #f_out.write("\n")

    T+=1
f_out.close()
f_out2.close()
    
    
    
    
    
    
    



